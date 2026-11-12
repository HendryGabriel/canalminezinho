"""Boneco de blocos ORIGINAL para testes (não é nenhum personagem conhecido).

Medidas de 1 "pixel" = 1/16 m: cabeça 8, corpo 8x4x12, braços e pernas 4x4x12 → 2 m de altura.
Cada braço, perna e a cabeça têm um "pivô" (empty) no ombro/quadril/pescoço,
então girar o pivô gira a parte no lugar certo.

    import boneco
    raiz = boneco.criar("Tito", pos=(0, 0, 0), rot_z=0)
    boneco.posar("Tito", 10, braco_d=(-90, 0, 0))   # graus, no quadro 10
    boneco.andar("Tito", 1, 24)                      # balança braços e pernas
Partes: cabeca, braco_d, braco_e, perna_d, perna_e. A frente do boneco olha para -Y.
"""
import math

import bmesh
import bpy

import looks

PX = 1 / 16
CORES = dict(pele=(0.85, 0.62, 0.45), camisa=(0.85, 0.55, 0.12), calca=(0.28, 0.22, 0.18),
             cabelo=(0.55, 0.15, 0.08), olho=(0.05, 0.05, 0.05), branco=(0.95, 0.95, 0.95))


def _cubo(nome, tam, centro, mat, pai):
    """Cubo de tamanho tam (em pixels), centro relativo ao pai (em pixels)."""
    me = bpy.data.meshes.new(nome)
    bm = bmesh.new()
    bm.loops.layers.uv.new()
    bmesh.ops.create_cube(bm, size=1, calc_uvs=True)
    bmesh.ops.scale(bm, vec=[t * PX for t in tam], verts=bm.verts)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat)
    o = bpy.data.objects.new(nome, me)
    o.location = [c * PX for c in centro]
    o.parent = pai
    bpy.context.scene.collection.objects.link(o)
    return o


def _pivo(nome, pos_px, pai):
    e = bpy.data.objects.new(nome, None)
    e.empty_display_size = 0.1
    e.location = [c * PX for c in pos_px]
    e.parent = pai
    bpy.context.scene.collection.objects.link(e)
    return e


def criar(nome, pos=(0, 0, 0), rot_z=0, cores=None):
    c = dict(CORES, **(cores or {}))
    m = {k: looks.mat_pixel(f"{nome}_{k}", v, semente=i) for i, (k, v) in enumerate(c.items())}

    raiz = _pivo(nome, (0, 0, 0), None)
    raiz.location = pos
    raiz.rotation_euler.z = math.radians(rot_z)
    raiz["boneco"] = True

    _cubo(f"{nome}_corpo", (8, 4, 12), (0, 0, 18), m["camisa"], raiz)
    # cabeça gira no pescoço (z = 24 px)
    cab = _pivo(f"{nome}_cabeca", (0, 0, 24), raiz)
    _cubo(f"{nome}_cabeca_m", (8, 8, 8), (0, 0, 4), m["pele"], cab)
    _cubo(f"{nome}_cabelo", (8.4, 8.4, 2), (0, 0, 8), m["cabelo"], cab)
    for lado in (-1, 1):  # olhos: branco + pupila, na frente (-Y)
        _cubo(f"{nome}_olho_b{lado}", (2, 0.4, 1), (lado * 2, -4.1, 4), m["branco"], cab)
        _cubo(f"{nome}_olho_p{lado}", (1, 0.5, 1), (lado * 1.5, -4.15, 4), m["olho"], cab)
    # braços giram no ombro (z = 22 px), pernas no quadril (z = 12 px)
    for lado, s in (("d", -1), ("e", 1)):
        b = _pivo(f"{nome}_braco_{lado}", (s * 6, 0, 22), raiz)
        _cubo(f"{nome}_braco_{lado}_m", (4, 4, 12), (0, 0, -4), m["camisa"], b)
        _cubo(f"{nome}_mao_{lado}", (4.1, 4.1, 4), (0, 0, -8), m["pele"], b)
        p = _pivo(f"{nome}_perna_{lado}", (s * 2, 0, 12), raiz)
        _cubo(f"{nome}_perna_{lado}_m", (4, 4, 12), (0, 0, -6), m["calca"], p)
    return raiz


def posar(nome, frame, **partes):
    """posar("Tito", 10, braco_d=(-90, 0, 0), cabeca=(0, 0, 30)) — graus."""
    for parte, rot in partes.items():
        o = bpy.data.objects[f"{nome}_{parte}"]
        o.rotation_euler = [math.radians(a) for a in rot]
        o.keyframe_insert("rotation_euler", frame=frame)


def mover(nome, de, para, ini, fim):
    raiz = bpy.data.objects[nome]
    raiz.location = de
    raiz.keyframe_insert("location", frame=ini)
    raiz.location = para
    raiz.keyframe_insert("location", frame=fim)


def andar(nome, ini, fim, passo=8, angulo=35):
    """Balança braços e pernas (perna direita junto com braço esquerdo)."""
    f, s = ini, 1
    while f <= fim:
        a = s * angulo
        posar(nome, f, perna_d=(a, 0, 0), perna_e=(-a, 0, 0), braco_d=(-a, 0, 0), braco_e=(a, 0, 0))
        f += passo
        s = -s


def objetos(nome):
    """Todos os objetos do boneco (raiz + filhos)."""
    raiz = bpy.data.objects[nome]
    return [raiz] + list(raiz.children_recursive)
