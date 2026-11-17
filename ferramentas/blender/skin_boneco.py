"""Personagem do Minecraft com a SKIN 64x64 aplicada (formato clássico, braço de 4 px), com camada externa.

Mesmos nomes de pivôs do boneco.py (`NOME`, `NOME_cabeca`, `NOME_braco_d/e`, `NOME_perna_d/e`),
então `boneco.posar`, `boneco.andar` e `boneco.mover` funcionam do mesmo jeito.
Medidas: 1 pixel = 1/16 m → 2 m de altura. A frente olha para -Y (personagem à direita = -X).

    import skin_boneco
    skin_boneco.criar("Kael", r"C:/.../kael_base.png", pos=(0, 0, 0), rot_z=0, escala=1.0)
    skin_boneco.trocar_skin("Kael", r"C:/.../kael_desperto.png")   # troca de textura no mesmo modelo
"""
import math

import bmesh
import bpy

PX = 1 / 16
# parte: (origem base, origem camada externa, w, h, d, pivô (px), centro da caixa relativo ao pivô (px))
PARTES = {
    "cabeca": ((0, 0), (32, 0), 8, 8, 8, (0, 0, 24), (0, 0, 4)),
    "corpo": ((16, 16), (16, 32), 8, 12, 4, (0, 0, 0), (0, 0, 18)),
    "braco_d": ((40, 16), (40, 32), 4, 12, 4, (-6, 0, 22), (0, 0, -4)),
    "braco_e": ((32, 48), (48, 48), 4, 12, 4, (6, 0, 22), (0, 0, -4)),
    "perna_d": ((0, 16), (0, 32), 4, 12, 4, (-2, 0, 12), (0, 0, -6)),
    "perna_e": ((16, 48), (0, 48), 4, 12, 4, (2, 0, 12), (0, 0, -6)),
}


def _material(nome, png, camada_externa):
    mat = bpy.data.materials.new(nome)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    saida = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Roughness"].default_value = 1.0
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(png, check_existing=True)
    tex.interpolation = "Closest"
    tex.label = "skin"
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    if camada_externa:
        nt.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
        mat.blend_method = "HASHED" if hasattr(mat, "blend_method") else None
    nt.links.new(bsdf.outputs["BSDF"], saida.inputs["Surface"])
    return mat


def _caixa(nome, origem, w, h, d, crescer, mat, pai, centro_px):
    """Caixa w (X) × d (Y) × h (Z) em px, com UV da skin 64x64. `crescer` engorda a caixa (camada externa)."""
    ox, oy = origem
    hx, hy, hz = (w + crescer) / 2 * PX, (d + crescer) / 2 * PX, (h + crescer) / 2 * PX
    # face: (região da textura em px: x, y, largura, altura), cantos TL, TR, BR, BL (3D)
    faces = {
        "frente": ((ox + d, oy + d, w, h), [(-hx, -hy, hz), (hx, -hy, hz), (hx, -hy, -hz), (-hx, -hy, -hz)]),
        "costas": ((ox + d + w + d, oy + d, w, h), [(hx, hy, hz), (-hx, hy, hz), (-hx, hy, -hz), (hx, hy, -hz)]),
        "dir": ((ox, oy + d, d, h), [(-hx, hy, hz), (-hx, -hy, hz), (-hx, -hy, -hz), (-hx, hy, -hz)]),
        "esq": ((ox + d + w, oy + d, d, h), [(hx, -hy, hz), (hx, hy, hz), (hx, hy, -hz), (hx, -hy, -hz)]),
        "topo": ((ox + d, oy, w, d), [(-hx, hy, hz), (hx, hy, hz), (hx, -hy, hz), (-hx, -hy, hz)]),
        "baixo": ((ox + d + w, oy, w, d), [(-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz)]),
    }
    me = bpy.data.meshes.new(nome)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for (px, py, pw, ph), (tl, tr, br, bl) in faces.values():
        u0, u1 = px / 64, (px + pw) / 64
        vt, vb = 1 - py / 64, 1 - (py + ph) / 64
        # ordem anti-horária vista de fora: BL, BR, TR, TL
        verts = [bm.verts.new(c) for c in (bl, br, tr, tl)]
        f = bm.faces.new(verts)
        for loop, (u, v) in zip(f.loops, ((u0, vb), (u1, vb), (u1, vt), (u0, vt))):
            loop[uv].uv = (u, v)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat)
    o = bpy.data.objects.new(nome, me)
    o.location = [c * PX for c in centro_px]
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


def criar(nome, skin_png, pos=(0, 0, 0), rot_z=0, escala=1.0):
    mat_base = _material(f"{nome}_skin", skin_png, False)
    mat_ext = _material(f"{nome}_skin_ext", skin_png, True)
    raiz = _pivo(nome, (0, 0, 0), None)
    raiz.location = pos
    raiz.rotation_euler.z = math.radians(rot_z)
    raiz.scale = (escala, escala, escala)
    raiz["boneco"] = True
    for parte, (o_base, o_ext, w, h, d, pivo, centro) in PARTES.items():
        if parte == "corpo":
            pai = raiz
            c = (centro[0], centro[1], centro[2])
        else:
            pai = _pivo(f"{nome}_{parte}", pivo, raiz)
            c = centro
        _caixa(f"{nome}_{parte}_m", o_base, w, h, d, 0, mat_base, pai, c)
        _caixa(f"{nome}_{parte}_o", o_ext, w, h, d, 1.0, mat_ext, pai, c)
    return raiz


def trocar_skin(nome, skin_png):
    """Troca a imagem da skin do personagem (ex.: Kael normal → desperto)."""
    img = bpy.data.images.load(skin_png, check_existing=True)
    for m in bpy.data.materials:
        if m.name.startswith(f"{nome}_skin") and m.node_tree:
            for n in m.node_tree.nodes:
                if n.type == "TEX_IMAGE":
                    n.image = img
