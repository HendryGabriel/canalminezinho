"""Monta e renderiza planos a partir de uma lista em JSON (formato no README.md).

    blender -b -P montar_cena.py -- planos.json             # todos os planos
    blender -b -P montar_cena.py -- planos.json 03_raio     # só os planos com esses nomes

Cada plano vira uma cena nova: look, cenário, personagens, câmera, efeitos, render em PNG
(e MP4 com o ffmpeg, se ele estiver no PATH). O tempo por quadro vai para tempos.txt.
"""
import inspect
import json
import math
import os
import shutil
import subprocess
import sys
import time

import bpy
from mathutils import Vector

sys.dont_write_bytecode = True  # não cria __pycache__ no repositório
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boneco  # noqa: E402
import efeitos  # noqa: E402
import looks  # noqa: E402


def cenario(item):
    tipo = item["tipo"]
    if tipo == "chao":
        n = item.get("tamanho", 30)
        bpy.ops.mesh.primitive_plane_add(size=n)
        o = bpy.context.active_object
        o.name = "Chao"
        for d in o.data.uv_layers[0].data:  # 1 textura por bloco de 1 m
            d.uv *= n
        o.data.materials.append(looks.mat_pixel("Grama", item.get("cor", (0.33, 0.58, 0.22))))
        return o
    if tipo == "bloco":
        bpy.ops.mesh.primitive_cube_add(size=item.get("tamanho", 1), location=item["pos"])
        o = bpy.context.active_object
        o.data.materials.append(looks.mat_pixel("Bloco", item.get("cor", (0.5, 0.5, 0.5)),
                                                semente=len(bpy.data.objects)))
        return o
    if tipo == "obj":
        return importar_obj(item)
    raise ValueError(f"cenário desconhecido: {tipo}")


def importar_obj(item):
    """Importa um OBJ (Mineways, Blockbench...) dentro de um empty, com textura Closest."""
    antes = set(bpy.data.objects)
    bpy.ops.wm.obj_import(filepath=item["obj"])
    novos = [o for o in bpy.data.objects if o not in antes]
    raiz = bpy.data.objects.new(os.path.basename(item["obj"]), None)
    bpy.context.scene.collection.objects.link(raiz)
    for o in novos:
        if o.parent is None:
            o.parent = raiz
        if o.type == "MESH":
            looks.pixel_closest(o)
    raiz.location = item.get("pos", (0, 0, 0))
    raiz.rotation_euler.z = math.radians(item.get("rot_z", 0))
    raiz.scale = [item.get("escala", 1)] * 3
    # ponytail: MCprep não está instalado, este caminho NUNCA foi testado
    if item.get("mcprep") and "mcprep" in dir(bpy.ops):
        try:
            for o in novos:
                o.select_set(o.type == "MESH")
            bpy.ops.mcprep.prep_materials()
        except Exception as e:
            print("MCprep falhou:", e)
    return raiz


def personagem(item):
    nome = item["nome"]
    if "obj" in item:
        return importar_obj(item)
    boneco.criar(nome, item.get("pos", (0, 0, 0)), item.get("rot_z", 0), item.get("cores"))
    if "andar" in item:
        boneco.andar(nome, *item["andar"])
    if "mover" in item:
        m = item["mover"]
        boneco.mover(nome, item.get("pos", (0, 0, 0)), m["para"], *m["frames"])
    for pose in item.get("poses", []):
        pose = dict(pose)
        boneco.posar(nome, pose.pop("frame"), **pose)
    return bpy.data.objects[nome]


def camera(c, p, ini, fim):
    cam_d = bpy.data.cameras.new("Camera")
    cam_d.lens = c.get("lente", 35)
    cam = bpy.data.objects.new("Camera", cam_d)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    alvo = bpy.data.objects.new("Alvo", None)
    alvo.location = c.get("alvo", (0, 0, 1))
    bpy.context.scene.collection.objects.link(alvo)
    t = cam.constraints.new("TRACK_TO")
    t.target = alvo
    t.track_axis, t.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
    cam.location = c["de"]
    if "para" in c:
        cam.keyframe_insert("location", frame=ini)
        cam.location = c["para"]
        cam.keyframe_insert("location", frame=fim)
    if "alvo_para" in c:
        alvo.keyframe_insert("location", frame=ini)
        alvo.location = c["alvo_para"]
        alvo.keyframe_insert("location", frame=fim)
    fstop = c.get("fstop", p["fstop"])
    if fstop:
        cam_d.dof.use_dof = True
        cam_d.dof.aperture_fstop = fstop
        cam_d.dof.focus_object = alvo
    return cam


def efeito(e, cam):
    e = dict(e)
    tipo = e.pop("tipo")
    ini, fim = e.pop("frames")
    if tipo == "tremida_camera":
        return efeitos.tremida_camera(cam, ini, fim, **e)
    if tipo == "icone":
        e["tipo"] = e.pop("icone")
    f = getattr(efeitos, tipo)
    if "cam" in inspect.signature(f).parameters:
        e["cam"] = cam
    return f(ini=ini, fim=fim, **e)


def montar(plano):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cena = bpy.context.scene
    cena.render.resolution_x, cena.render.resolution_y = plano.get("resolucao", (1920, 1080))
    cena.render.resolution_percentage = 100
    ini, fim = plano.get("frames", (1, 24))
    cena.frame_start, cena.frame_end = ini, fim

    troca = dict(plano.get("look_extra", {}))
    if "motor" in plano:
        troca["motor"] = plano["motor"]
    if "fps" in plano:
        troca["fps"] = plano["fps"]
    p = looks.aplicar_look(plano["look"], **troca)

    for item in plano.get("cenario", []):
        cenario(item)
    personagens = [personagem(i) for i in plano.get("personagens", [])]
    cam = camera(plano["camera"], p, ini, fim)
    for e in plano.get("efeitos", []):
        cena.frame_set(ini)
        efeito(e, cam)

    if plano["look"] == "toon":
        bonecos = [o for r in personagens for o in [r] + list(r.children_recursive)]
        for o in cena.objects:
            if o.type == "MESH" and not o.get("efeito"):
                looks.toon_material(o)
                if o.name != "Chao":
                    looks.contorno(o)
        for o in bonecos:
            looks.animacao_em_dois(o, plano.get("passo", 2))
    cena.frame_set(ini)
    return cena


def renderizar(plano, pasta):
    cena = montar(plano)
    nome = plano["nome"]
    destino = os.path.join(pasta, nome)
    os.makedirs(destino, exist_ok=True)
    cena.render.filepath = os.path.join(destino, "")
    cena.render.image_settings.file_format = "PNG"
    cena.render.image_settings.color_mode = "RGB"
    if plano.get("salvar_blend"):
        bpy.context.preferences.filepaths.save_version = 0  # sem cópia .blend1
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(pasta, nome + ".blend"))

    t0 = time.perf_counter()
    bpy.ops.render.render(animation=True)
    quadros = cena.frame_end - cena.frame_start + 1
    por_quadro = (time.perf_counter() - t0) / quadros
    linha = f"{nome}: {quadros} quadros, {por_quadro:.2f} s/quadro ({cena.render.engine})"
    print("TEMPO", linha)
    with open(os.path.join(pasta, "tempos.txt"), "a", encoding="utf-8") as f:
        f.write(linha + "\n")

    if plano.get("video", True) and shutil.which("ffmpeg"):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(cena.render.fps),
                        "-start_number", str(cena.frame_start), "-i", os.path.join(destino, "%04d.png"),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                        os.path.join(pasta, nome + ".mp4")], check=True)


def main():
    args = sys.argv[sys.argv.index("--") + 1:]
    with open(args[0], encoding="utf-8") as f:
        dados = json.load(f)
    padrao = dados.get("padrao", {})
    pasta = padrao.get("saida", "render")
    os.makedirs(pasta, exist_ok=True)
    for plano in dados["planos"]:
        plano = {**padrao, **plano}
        if len(args) > 1 and plano["nome"] not in args[1:]:
            continue
        renderizar(plano, plano.get("saida", pasta))


if __name__ == "__main__":
    main()
