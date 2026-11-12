"""Looks (estilos de imagem) para o Blender 5.2.

Uso dentro do Blender:
    import looks
    p = looks.aplicar_look("kids")             # motor, cor, céu, névoa, luz, compositor, fps
    p = looks.aplicar_look("epico", nevoa=0.0)  # qualquer valor da tabela pode ser trocado

Também tem:
    toon_material(obj)          sombra dura de anime (só funciona no Eevee)
    contorno(obj)               linha preta em volta (casca invertida)
    animacao_em_dois(obj)       anima "em dois" (segura cada pose 2 quadros)
    mat_pixel(nome, cor)        material com textura de pixel (filtro Closest)

Convenção de cena: a câmera olha mais ou menos para +Y. A luz de borda (rim) vem de trás (+Y).
"""
import math
import random

import bpy
from bpy_extras import anim_utils

# Tabela dos looks (vem do analises/animacao/sintese.md §6).
# motor: EEVEE ou CYCLES · vt/look: gestão de cor · sat: saturação no compositor
# ceu: cor do céu · nevoa: densidade da névoa (0 = sem) · nevoa_tam: tamanho da caixa de névoa (m)
# sol: força · sol_angulo: maciez da sombra (graus) · sol_altura: altura do sol (graus)
# rim: (cor, força) da luz de borda ou None · fstop: desfoque (None = sem DOF)
# blur: shutter do motion blur (0 = desligado) · glare: força do brilho
# vinheta: escura (0–1) · vinheta_branca: branca borrada (0–1, flashback)
# aberracao: aberração cromática (0–0.1) · letterbox: faixas pretas 2.39:1
LOOKS = {
    "humor": dict(motor="CYCLES", amostras=64, vt="AgX", look="AgX - Base Contrast", sat=0.9,
                  ceu=(0.55, 0.62, 0.70), ceu_forca=1.0, nevoa=0.004,
                  sol=1.8, sol_cor=(1.0, 0.97, 0.92), sol_angulo=12, sol_altura=50, rim=None,
                  fstop=2.8, blur=0.5, glare=0.3, vinheta=0.15, vinheta_branca=0,
                  aberracao=0, letterbox=False, fps=24),
    "epico": dict(motor="EEVEE", amostras=32, vt="AgX", look="AgX - High Contrast", sat=1.0,
                  ceu=(0.08, 0.09, 0.18), ceu_forca=1.0, nevoa=0.02,
                  sol=2.5, sol_cor=(1.0, 0.6, 0.35), sol_angulo=3, sol_altura=12,
                  rim=((0.3, 0.5, 1.0), 6.0),
                  fstop=2.0, blur=0.8, glare=1.0, vinheta=0.45, vinheta_branca=0,
                  aberracao=0, letterbox=True, fps=24),
    "kids": dict(motor="EEVEE", amostras=16, vt="AgX", look="AgX - Punchy", sat=1.2,
                 ceu=(0.35, 0.65, 1.0), ceu_forca=1.2, nevoa=0,
                 sol=4.5, sol_cor=(1.0, 0.98, 0.95), sol_angulo=1, sol_altura=55, rim=None,
                 fstop=4.0, blur=0.5, glare=0.25, vinheta=0, vinheta_branca=0,
                 aberracao=0, letterbox=False, fps=30),
    "toon": dict(motor="EEVEE", amostras=16, vt="Standard", look="None", sat=1.1,
                 ceu=(0.45, 0.72, 1.0), ceu_forca=1.0, nevoa=0,
                 sol=4.0, sol_cor=(1.0, 1.0, 1.0), sol_angulo=0.5, sol_altura=45,
                 rim=((1.0, 1.0, 1.0), 2.0),
                 fstop=None, blur=0, glare=0.6, vinheta=0.1, vinheta_branca=0,
                 aberracao=0, letterbox=False, fps=24),
}


def aplicar_look(nome, **troca):
    """Aplica o look na cena atual e devolve a tabela usada (com as trocas)."""
    p = dict(LOOKS[nome], **troca)
    cena = bpy.context.scene

    # motor e amostras
    if p["motor"] == "CYCLES":
        cena.render.engine = "CYCLES"
        cena.cycles.samples = p["amostras"]
        cena.cycles.use_denoising = True
    else:
        cena.render.engine = "BLENDER_EEVEE"
        cena.eevee.taa_render_samples = p["amostras"]
        cena.eevee.use_raytracing = nome == "epico"
        cena.eevee.volumetric_end = 200  # névoa até 200 m

    # cor
    cena.view_settings.view_transform = p["vt"]
    cena.view_settings.look = p["look"]
    cena.render.fps = p["fps"]

    # motion blur
    cena.render.use_motion_blur = p["blur"] > 0
    cena.render.motion_blur_shutter = p["blur"] or 0.5

    _mundo(p)
    _luzes(p)
    _compositor(p)
    return p


def _mundo(p):
    """Céu de cor lisa (sem HDRI) e névoa por volume (caixa)."""
    w = bpy.data.worlds.new("Mundo")
    bpy.context.scene.world = w
    nt = w.node_tree
    nt.nodes.clear()
    saida = nt.nodes.new("ShaderNodeOutputWorld")
    fundo = nt.nodes.new("ShaderNodeBackground")
    fundo.inputs["Color"].default_value = (*p["ceu"], 1)
    fundo.inputs["Strength"].default_value = p["ceu_forca"]
    nt.links.new(fundo.outputs[0], saida.inputs["Surface"])
    if p["nevoa"] > 0:
        # ponytail: névoa numa caixa grande, não no World. No Blender 5.2 o volume no World
        # deixou o quadro todo preto (Eevee e Cycles). Cena maior que a caixa? Aumente nevoa_tam.
        bpy.ops.mesh.primitive_cube_add(size=p.get("nevoa_tam", 120))
        caixa = bpy.context.active_object
        caixa.name = "Nevoa"
        caixa["efeito"] = True  # toon/contorno não mexem nela
        caixa.visible_shadow = False
        mat = bpy.data.materials.new("Nevoa")
        mat.node_tree.nodes.clear()
        vol = mat.node_tree.nodes.new("ShaderNodeVolumePrincipled")
        vol.inputs["Density"].default_value = p["nevoa"]
        vol.inputs["Color"].default_value = (*p["ceu"], 1)
        mat.node_tree.links.new(vol.outputs[0], mat.node_tree.nodes.new("ShaderNodeOutputMaterial").inputs["Volume"])
        caixa.data.materials.append(mat)


def _luzes(p):
    cena = bpy.context.scene
    sol = bpy.data.lights.new("Sol", "SUN")
    sol.energy = p["sol"]
    sol.color = p["sol_cor"]
    sol.angle = math.radians(p["sol_angulo"])
    o = bpy.data.objects.new("Sol", sol)
    # sol vindo da frente-esquerda, na altura pedida
    o.rotation_euler = (math.radians(90 - p["sol_altura"]), 0, math.radians(-35))
    cena.collection.objects.link(o)
    if p["rim"]:
        cor, forca = p["rim"]
        rim = bpy.data.lights.new("Rim", "SUN")
        rim.energy = forca
        rim.color = cor
        r = bpy.data.objects.new("Rim", rim)
        # vem de trás (+Y) e de cima, apontando para a câmera
        r.rotation_euler = (math.radians(-60), 0, math.radians(20))
        cena.collection.objects.link(r)


def _compositor(p):
    """Glare, saturação, aberração, vinheta (escura ou branca) e letterbox."""
    cena = bpy.context.scene
    ng = bpy.data.node_groups.new("Compositor", "CompositorNodeTree")
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    cena.compositing_node_group = ng
    n, L = ng.nodes, ng.links
    w, h = cena.render.resolution_x, cena.render.resolution_y

    img = n.new("CompositorNodeRLayers").outputs["Image"]

    if p["glare"] > 0:
        g = n.new("CompositorNodeGlare")
        g.inputs["Type"].default_value = "Bloom"
        g.inputs["Quality"].default_value = "High"
        g.inputs["Threshold"].default_value = 1.0
        g.inputs["Strength"].default_value = p["glare"]
        g.inputs["Size"].default_value = 0.7
        L.new(img, g.inputs["Image"])
        img = g.outputs["Image"]

    if p["sat"] != 1:
        s = n.new("CompositorNodeHueSat")
        s.inputs["Saturation"].default_value = p["sat"]
        L.new(img, s.inputs["Image"])
        img = s.outputs["Image"]

    if p["aberracao"] > 0:
        a = n.new("CompositorNodeLensdist")
        a.inputs["Dispersion"].default_value = p["aberracao"]
        L.new(img, a.inputs["Image"])
        img = a.outputs["Image"]

    def borda(cor, forca, tamanho, borrao):
        # máscara oval borrada: 1 no meio, 0 nas bordas
        m = n.new("CompositorNodeEllipseMask")
        m.inputs["Size"].default_value = tamanho
        b = n.new("CompositorNodeBlur")
        b.inputs["Size"].default_value = (w * borrao, h * borrao)
        b.inputs["Extend Bounds"].default_value = False
        L.new(m.outputs["Mask"], b.inputs["Image"])
        # fator = máscara*forca + (1-forca): força 0 = não muda nada
        f = n.new("ShaderNodeMath")
        f.operation = "MULTIPLY_ADD"
        L.new(b.outputs["Image"], f.inputs[0])
        f.inputs[1].default_value = forca
        f.inputs[2].default_value = 1 - forca
        return _mix(ng, img, cor, f.outputs[0])

    if p["vinheta"] > 0:
        img = borda((0, 0, 0, 1), p["vinheta"], (1.15, 1.15), 0.18)
    if p["vinheta_branca"] > 0:
        img = borda((1, 1, 1, 1), p["vinheta_branca"], (0.85, 0.75), 0.25)

    if p["letterbox"]:
        caixa = n.new("CompositorNodeBoxMask")
        caixa.inputs["Size"].default_value = (2.0, (w / h) / 2.39)
        img = _mix(ng, img, (0, 0, 0, 1), caixa.outputs["Mask"])

    saida = n.new("NodeGroupOutput")
    L.new(img, saida.inputs[0])


def _sock(lista, ident):
    """Pega a entrada/saída pelo identificador (o nó Mix tem nomes repetidos: A, B...)."""
    return next(x for x in lista if x.identifier == ident)


def _mix(ng, img, cor, fator):
    """Mistura: onde fator = 1 fica a imagem, onde fator = 0 fica a cor."""
    m = ng.nodes.new("ShaderNodeMix")
    m.data_type = "RGBA"
    _sock(m.inputs, "A_Color").default_value = cor
    ng.links.new(img, _sock(m.inputs, "B_Color"))
    ng.links.new(fator, _sock(m.inputs, "Factor_Float"))
    return _sock(m.outputs, "Result_Color")


# ---------- materiais ----------

def textura_pixel(nome, cor, tam=8, var=0.12, semente=1):
    """Imagem pequena (8x8) com variação de cor por pixel, estilo bloco do Minecraft."""
    img = bpy.data.images.new(nome, tam, tam)
    rnd = random.Random(semente)
    px = []
    for _ in range(tam * tam):
        k = 1 + rnd.uniform(-var, var)
        px += [min(1, c * k) for c in cor[:3]] + [1]
    img.pixels.foreach_set(px)
    img.pack()
    return img


def mat_pixel(nome, cor, semente=1):
    """Material com textura de pixel (sem filtro = Closest)."""
    mat = bpy.data.materials.new(nome)
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = 0.9
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = textura_pixel(nome, cor, semente=semente)
    tex.interpolation = "Closest"
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    return mat


def pixel_closest(obj):
    """Deixa toda textura do objeto sem filtro (pixel nítido)."""
    for slot in obj.material_slots:
        if slot.material and slot.material.node_tree:
            for nd in slot.material.node_tree.nodes:
                if nd.type == "TEX_IMAGE":
                    nd.interpolation = "Closest"


def toon_material(obj, degraus=(0.45, 0.75, 1.0)):
    """Troca o material por sombra dura de anime (Shader to RGB + Color Ramp constante).
    Mantém a textura de pixel (Closest). Só funciona no Eevee."""
    for slot in obj.material_slots:
        mat = slot.material
        if not mat or not mat.node_tree or mat.get("toon"):
            continue
        nt = mat.node_tree
        saida = next(nd for nd in nt.nodes if nd.type == "OUTPUT_MATERIAL")
        tex = next((nd for nd in nt.nodes if nd.type == "TEX_IMAGE"), None)
        bsdf = next((nd for nd in nt.nodes if nd.type == "BSDF_PRINCIPLED"), None)

        luz = nt.nodes.new("ShaderNodeBsdfDiffuse")
        rgb = nt.nodes.new("ShaderNodeShaderToRGB")
        rampa = nt.nodes.new("ShaderNodeValToRGB")
        rampa.color_ramp.interpolation = "CONSTANT"
        els = rampa.color_ramp.elements
        els[0].position, els[0].color = 0.0, (degraus[0],) * 3 + (1,)
        els[1].position, els[1].color = 0.25, (degraus[1],) * 3 + (1,)
        e = els.new(0.6)
        e.color = (degraus[2],) * 3 + (1,)
        mult = nt.nodes.new("ShaderNodeMix")
        mult.data_type = "RGBA"
        mult.blend_type = "MULTIPLY"
        _sock(mult.inputs, "Factor_Float").default_value = 1
        if tex:
            tex.interpolation = "Closest"
            nt.links.new(tex.outputs["Color"], _sock(mult.inputs, "A_Color"))
        elif bsdf:
            _sock(mult.inputs, "A_Color").default_value = bsdf.inputs["Base Color"].default_value
        emis = nt.nodes.new("ShaderNodeEmission")
        nt.links.new(luz.outputs[0], rgb.inputs[0])
        nt.links.new(rgb.outputs["Color"], rampa.inputs["Fac"])
        nt.links.new(rampa.outputs["Color"], _sock(mult.inputs, "B_Color"))
        nt.links.new(_sock(mult.outputs, "Result_Color"), emis.inputs["Color"])
        nt.links.new(emis.outputs[0], saida.inputs["Surface"])
        mat["toon"] = True


def contorno(obj, espessura=0.025, cor=(0, 0, 0)):
    """Linha em volta do objeto: casca invertida (Solidify + material com backface culling)."""
    mat = bpy.data.materials.get("Contorno")
    if not mat:
        mat = bpy.data.materials.new("Contorno")
        mat.use_backface_culling = True
        nt = mat.node_tree
        nt.nodes.clear()
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Color"].default_value = (*cor, 1)
        nt.links.new(em.outputs[0], nt.nodes.new("ShaderNodeOutputMaterial").inputs["Surface"])
    if not obj.data.materials:
        obj.data.materials.append(bpy.data.materials.new("Base"))
    obj.data.materials.append(mat)
    s = obj.modifiers.new("Contorno", "SOLIDIFY")
    s.thickness = espessura
    s.offset = 1
    s.use_flip_normals = True
    s.use_rim = False
    s.material_offset = len(obj.data.materials) - 1  # passa do fim = usa o último (contorno)


def fcurves(obj):
    """Curvas de animação do objeto (Blender 5 usa 'slots' nas actions)."""
    ad = obj.animation_data
    if not ad or not ad.action:
        return []
    cb = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
    return cb.fcurves if cb else []


def animacao_em_dois(obj, passo=2):
    """Animação 'em dois' (anime): cada pose fica 'passo' quadros parada."""
    for fc in fcurves(obj):
        if not any(m.type == "STEPPED" for m in fc.modifiers):
            m = fc.modifiers.new("STEPPED")
            m.frame_step = passo
