"""Efeitos prontos (guia 11 §4 e guia 14 §2). Cada função cria o efeito numa posição
e num intervalo de quadros [ini, fim]. Tudo é emissão: o brilho vem do Glare do look.

    import efeitos
    efeitos.aura((0, 0, 0), 1, 48, cor=(1, 0.8, 0.2))
    efeitos.raio((0, 0, 1.4), (6, 0, 1.4), 10, 30)
    efeitos.tremida_camera(cam, 12, 18, forca=0.15)

Lista: aura, raio, bola_energia, anel_choque, flash, linhas_velocidade, buraco_negro,
explosao, icone ("coracao", "!?", "!", "?"), coracoes, tremida_camera.
"""
import math
import random

import bmesh
import bpy
from mathutils import Matrix, Vector

import looks

rnd = random.Random(7)  # mesma semente = mesmo resultado a cada render


# ---------- ajudantes ----------

def _cena():
    return bpy.context.scene


def _marcar(o):
    """Marca como efeito: não faz sombra e não recebe toon/contorno."""
    o["efeito"] = True
    o.visible_shadow = False
    return o


def _add(op, **kw):
    """Cria uma forma pronta do Blender (cubo, esfera, toro...) e devolve o objeto."""
    op(**kw)
    return _marcar(bpy.context.active_object)


def _mat_brilho(nome, cor, forca, mascara=None):
    """Material de luz. Fade: animar o 'Fac' do nó devolvido (1 = aceso, 0 = some).
    mascara: função (nt) -> saída de 0..1 que recorta o brilho (ex.: ruído)."""
    mat = bpy.data.materials.new(nome)
    nt = mat.node_tree
    nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*cor, 1)
    em.inputs["Strength"].default_value = forca
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    if mascara:
        mult = nt.nodes.new("ShaderNodeMath")
        mult.operation = "MULTIPLY"
        nt.links.new(mascara(nt), mult.inputs[0])
        mult.inputs[1].default_value = 1
        nt.links.new(mult.outputs[0], mix.inputs[0])
        fade = mult.inputs[1]
    else:
        mix.inputs[0].default_value = 1
        fade = mix.inputs[0]
    nt.links.new(mix.outputs[0], nt.nodes.new("ShaderNodeOutputMaterial").inputs["Surface"])
    return mat, fade


def _chaves(alvo, prop, valores):
    """valores = {quadro: valor}. Ex.: _chaves(obj, "scale", {1: (0,0,0), 5: (1,1,1)})."""
    for f, v in valores.items():
        setattr(alvo, prop, v)
        alvo.keyframe_insert(prop, frame=f)


def _visivel(o, ini, fim):
    """Só aparece no render entre ini e fim."""
    _chaves(o, "hide_render", {ini - 1: True, ini: False, fim: False, fim + 1: True})
    o.hide_render = ini > _cena().frame_start


def _linear(o):
    for fc in looks.fcurves(o):
        for k in fc.keyframe_points:
            k.interpolation = "LINEAR"


def _luz(nome, pos, cor, energias, raio=0.2):
    """Luz pontual. energias = {quadro: watts}."""
    L = bpy.data.lights.new(nome, "POINT")
    L.color = cor
    L.shadow_soft_size = raio
    o = bpy.data.objects.new(nome, L)
    o.location = pos
    _cena().collection.objects.link(o)
    _chaves(L, "energy", energias)
    o["efeito"] = True
    return o


def _particulas(emissor, ini, fim, qtd, vida, tam, cor, forca=6, vel_normal=0.0, vel_z=0.0):
    """Cubinhos de luz saindo da superfície do emissor (o emissor some no render)."""
    inst = _add(bpy.ops.mesh.primitive_cube_add, size=1, location=(0, 0, -500))
    inst.name = emissor.name + "_part"
    inst.data.materials.append(_mat_brilho(inst.name, cor, forca)[0])
    inst.hide_render = True  # o original fica escondido; as cópias aparecem
    emissor.modifiers.new("Particulas", "PARTICLE_SYSTEM")
    ps = emissor.particle_systems[-1].settings
    ps.count = qtd
    ps.frame_start, ps.frame_end = ini, max(ini, fim - vida // 2)
    ps.lifetime = vida
    ps.lifetime_random = 0.3
    ps.emit_from = "FACE"
    ps.normal_factor = vel_normal
    ps.object_align_factor = (0, 0, vel_z)
    ps.factor_random = 0.2
    ps.effector_weights.gravity = 0
    ps.render_type = "OBJECT"
    ps.instance_object = inst
    ps.particle_size = tam
    ps.size_random = 0.5
    ps.use_rotations = True
    ps.rotation_factor_random = 1
    emissor.show_instancer_for_render = False
    return inst


def _alinhar(o, direcao):
    """Gira o objeto para o eixo Z dele apontar na direção dada."""
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = Vector(direcao).to_track_quat("Z", "Y")


def _ruido(nt, mapa, escala=3.0, borda=False):
    """Máscara de ruído (manchas de 0 a 1). borda=True: brilha mais nas bordas (aura).
    Guarda o nó Mapping em mapa["mp"] para animar o ruído."""
    coord = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    ru = nt.nodes.new("ShaderNodeTexNoise")
    ru.inputs["Scale"].default_value = escala
    ru.inputs["Detail"].default_value = 4
    rampa = nt.nodes.new("ShaderNodeValToRGB")
    rampa.color_ramp.elements[0].position = 0.4 if borda else 0.35
    rampa.color_ramp.elements[1].position = 0.65
    nt.links.new(coord.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs[0], ru.inputs["Vector"])
    nt.links.new(ru.outputs["Fac"], rampa.inputs["Fac"])
    mapa["mp"] = mp
    if not borda:
        return rampa.outputs["Color"]
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.75
    mult = nt.nodes.new("ShaderNodeMath")
    mult.operation = "MULTIPLY"
    mult.use_clamp = True
    nt.links.new(rampa.outputs["Color"], mult.inputs[0])
    nt.links.new(lw.outputs["Facing"], mult.inputs[1])
    return mult.outputs[0]


def _cor_ruido(mat, cores):
    """Pinta a emissão com manchas de ruído entre as cores dadas (fogo). Devolve o Mapping."""
    nt = mat.node_tree
    mapa = {}
    saida = _ruido(nt, mapa, escala=2.5)
    rampa = saida.node
    for i, c in enumerate(cores):
        e = rampa.color_ramp.elements[i] if i < 2 else rampa.color_ramp.elements.new(0)
        e.position = 0.35 + 0.3 * i / (len(cores) - 1)  # ruído fica quase todo entre 0,3 e 0,7
        e.color = (*c, 1)
    em = next(n for n in nt.nodes if n.type == "EMISSION")
    nt.links.new(saida, em.inputs["Color"])
    return mapa["mp"]


# ---------- efeitos ----------

def aura(pos, ini, fim, cor=(0.3, 0.6, 1.0), altura=2.0):
    """Casca de energia em volta do corpo (borda brilhante, ruído subindo) + partículas subindo."""
    c = Vector(pos) + Vector((0, 0, altura / 2))
    o = _add(bpy.ops.mesh.primitive_uv_sphere_add, radius=1, segments=32, ring_count=16, location=c)
    o.name = "Aura"

    mapa = {}
    mat, _ = _mat_brilho("Aura", cor, 6, lambda nt: _ruido(nt, mapa, borda=True))
    o.data.materials.append(mat)
    # o ruído sobe (a chama "corre" para cima)
    loc = mapa["mp"].inputs["Location"]
    _chaves(loc, "default_value", {ini: (0, 0, 0), fim: (0, 0, -(fim - ini) / 8)})
    escala = (0.5 * altura, 0.38 * altura, 0.62 * altura)
    _chaves(o, "scale", {ini: (0.01, 0.01, 0.01), ini + 4: escala})
    _visivel(o, ini, fim)
    # o emissor some no render, então as partículas saem de uma cópia (a casca continua visível)
    emissor = o.copy()
    emissor.animation_data_clear()
    emissor.scale = escala
    emissor.hide_render = False
    _cena().collection.objects.link(emissor)
    _particulas(emissor, ini, fim, qtd=10 * (fim - ini), vida=14, tam=0.05, cor=cor, forca=10, vel_z=1.8)
    _luz("Aura_luz", c, cor, {ini: 0, ini + 4: 400, fim: 400, fim + 1: 0})
    return o


def raio(de, para, ini, fim, cor=(0.3, 0.7, 1.0), grossura=0.25):
    """Raio de energia: núcleo branco + borda colorida, cresce em 3 quadros, luz andando junto."""
    de, para = Vector(de), Vector(para)
    d = para - de
    partes = []
    for nome, r, c, forca, fac in (("Raio_borda", grossura, cor, 4, 0.8),
                                    ("Raio_nucleo", grossura * 0.4, (1, 1, 1), 10, 1)):
        o = _add(bpy.ops.mesh.primitive_cylinder_add, radius=r, depth=1, vertices=24, location=de)
        o.name = nome
        o.data.transform(Matrix.Translation((0, 0, 0.5)))  # base na origem
        mat, fade = _mat_brilho(nome, c, forca)
        fade.default_value = fac
        o.data.materials.append(mat)
        _alinhar(o, d)
        _chaves(o, "scale", {ini: (1, 1, 0.01), ini + 3: (1, 1, d.length),
                             fim - 2: (1, 1, d.length), fim: (0.01, 0.01, d.length)})
        _visivel(o, ini, fim)
        partes.append(o)
    boca = _add(bpy.ops.mesh.primitive_uv_sphere_add, radius=grossura * 1.6, location=de)
    boca.data.materials.append(_mat_brilho("Raio_boca", (1, 1, 1), 8)[0])
    _visivel(boca, ini, fim)
    luz = _luz("Raio_luz", de, cor, {ini - 1: 0, ini: 3000, fim: 3000, fim + 1: 0}, raio=grossura)
    _chaves(luz, "location", {ini: de, ini + 3: para})
    return partes


def bola_energia(pos, ini, fim, cor=(0.6, 0.3, 1.0), raio=0.6):
    """Bola de luz crescendo, com partículas vindo de fora para dentro."""
    nucleo = _add(bpy.ops.mesh.primitive_uv_sphere_add, radius=1, location=pos)
    nucleo.data.materials.append(_mat_brilho("Bola_nucleo", (1, 0.95, 1), 10)[0])
    halo = _add(bpy.ops.mesh.primitive_uv_sphere_add, radius=1.5, location=pos)
    m, fade = _mat_brilho("Bola_halo", cor, 4)
    fade.default_value = 0.5
    halo.data.materials.append(m)
    for o in (nucleo, halo):
        _chaves(o, "scale", {ini: (0.05,) * 3, fim: (raio,) * 3})
        _visivel(o, ini, fim)
    # casca invisível grande: as partículas nascem nela e correm para o centro
    casca = _add(bpy.ops.mesh.primitive_ico_sphere_add, radius=raio * 4, subdivisions=2, location=pos)
    vida = 10
    vel = raio * 3.2 / (vida / _cena().render.fps)
    _particulas(casca, ini, fim, qtd=15 * (fim - ini), vida=vida, tam=0.035, cor=cor, forca=6,
                vel_normal=-vel)
    _luz("Bola_luz", pos, cor, {ini - 1: 0, ini: 50, fim: 1500, fim + 1: 0})
    return nucleo


def anel_choque(pos, ini, fim=None, cor=(1, 1, 1), raio=3.0, normal=(0, 0, 1)):
    """Anel de luz que cresce e some em 6–8 quadros."""
    fim = fim or ini + 7
    o = _add(bpy.ops.mesh.primitive_torus_add, major_radius=1, minor_radius=0.05,
             major_segments=64, minor_segments=8, location=pos)
    o.name = "Anel"
    mat, fade = _mat_brilho("Anel", cor, 8)
    o.data.materials.append(mat)
    _alinhar(o, normal)
    meio = ini + max(1, (fim - ini) // 3)
    _chaves(o, "scale", {ini: (0.2,) * 3, meio: (raio * 0.75,) * 3, fim: (raio,) * 3})
    _chaves(fade, "default_value", {ini: 1, meio: 1, fim: 0})
    _visivel(o, ini, fim)
    return o


def flash(pos, ini, fim=None, forca=1.0):
    """Flash de luz de 1–3 quadros: luz enorme + exposição da imagem subindo."""
    fim = fim or ini + 2
    _luz("Flash", pos, (1, 0.95, 0.9), {ini - 1: 0, ini: 2e5 * forca, fim: 5e4 * forca, fim + 1: 0},
         raio=1.0)
    vs = _cena().view_settings
    base = vs.exposure
    _chaves(vs, "exposure", {ini - 1: base, ini: base + 3 * forca, fim: base + 1.2 * forca,
                             fim + 1: base})


def linhas_velocidade(pos, ini, fim, forma="radial", eixo=None, cor=(1, 1, 1), qtd=28, cam=None):
    """Linhas de velocidade. forma radial: abrem em volta de pos (de frente para a câmera).
    paralelo: correm na direção 'eixo' (ex.: [1, 0, 0])."""
    pos = Vector(pos)
    if eixo is None:
        eixo = (cam.location - pos) if cam else Vector((0, -1, 0))
    n = Vector(eixo).normalized()
    u = n.orthogonal().normalized()
    v = n.cross(u)
    mat, _ = _mat_brilho("Linhas", cor, 6)
    linhas = []
    for i in range(qtd):
        o = _add(bpy.ops.mesh.primitive_cube_add, size=1, location=pos)
        o.data.materials.append(mat)
        comp = rnd.uniform(1.0, 2.5)
        if forma == "radial":
            ang = 2 * math.pi * i / qtd + rnd.uniform(-0.1, 0.1)
            d = u * math.cos(ang) + v * math.sin(ang)
            r0 = rnd.uniform(1.2, 2.5)
            o.scale = (0.012, 0.012, comp)
            _alinhar(o, d)
            _chaves(o, "location", {ini: pos + d * (r0 + comp / 2), fim: pos + d * (r0 + comp / 2 + 3)})
        else:
            lado = u * rnd.uniform(-3, 3) + v * rnd.uniform(-1.5, 1.5)
            o.scale = (0.015, 0.015, comp * 1.5)
            _alinhar(o, n)
            p0 = rnd.uniform(-2, 6)
            _chaves(o, "location", {ini: pos + lado + n * p0, fim: pos + lado + n * (p0 - 14)})
        _linear(o)
        # pisca: cada linha some em alguns quadros
        for f in range(ini, fim + 1):
            o.hide_render = rnd.random() < 0.3
            o.keyframe_insert("hide_render", frame=f)
        _chaves(o, "hide_render", {ini - 1: True, fim + 1: True})
        o.hide_render = ini > _cena().frame_start
        linhas.append(o)
    return linhas


def buraco_negro(pos, ini, fim, raio=1.0, cor=(1.0, 0.7, 0.25)):
    """Esfera preta com anel de luz dourado em volta."""
    bola = _add(bpy.ops.mesh.primitive_uv_sphere_add, radius=raio, segments=48, ring_count=24, location=pos)
    preto = bpy.data.materials.new("Preto")
    preto.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0, 0, 0, 1)
    preto.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1
    bola.data.materials.append(preto)
    objs = [bola]
    for nome, r, grosso, forca in (("BN_anel", 1.6, 0.10, 18), ("BN_anel2", 2.3, 0.04, 8)):
        a = _add(bpy.ops.mesh.primitive_torus_add, major_radius=raio * r, minor_radius=raio * grosso,
                 major_segments=96, minor_segments=12, location=pos)
        a.scale.z = 0.25
        a.rotation_euler = (math.radians(75), 0, math.radians(10))
        mat, fade = _mat_brilho(nome, cor, forca)
        a.data.materials.append(mat)
        meio = (ini + fim) // 2
        _chaves(fade, "default_value", {ini: 0.7, meio: 1.0, fim: 0.7})  # pulsa
        objs.append(a)
    for o in objs:
        _chaves(o, "scale", {ini: Vector(o.scale) * 0.01, ini + 5: Vector(o.scale)})
        _visivel(o, ini, fim)
    _luz("BN_luz", pos, cor, {ini: 0, ini + 5: 2000, fim: 2000, fim + 1: 0}, raio=raio)
    return bola


def explosao(pos, ini, fim=None, cor=(1.0, 0.22, 0.0), tamanho=2.5, detritos=12):
    """Bola de fogo que cresce e some + flash + anel no chão + blocos voando (keyframes)."""
    fim = fim or ini + 18
    pos = Vector(pos)
    centro = pos + Vector((0, 0, tamanho * 0.5))  # não fica meio enterrada no chão
    for nome, cores, forca, t, apaga in (
            ("Fogo", [(0.4, 0.02, 0.0), cor, (1, 0.55, 0.05)], 0.9, tamanho, fim),
            ("Fogo_nucleo", [cor, (1, 0.6, 0.1), (1, 0.9, 0.5)], 1.5, tamanho * 0.6, ini + 8)):
        o = _add(bpy.ops.mesh.primitive_ico_sphere_add, radius=1, subdivisions=3, location=centro)
        o.name = nome
        mat, fade = _mat_brilho(nome, cor, forca)
        mp = _cor_ruido(mat, cores)
        o.data.materials.append(mat)
        _chaves(mp.inputs["Location"], "default_value", {ini: (0, 0, 0), fim: (0, 0, -1.5)})
        _chaves(o, "scale", {ini: (0.1,) * 3, ini + 6: (t,) * 3, fim: (t * 1.2,) * 3})
        _chaves(fade, "default_value", {ini: 1, ini + 6: 1, apaga: 0})
        _visivel(o, ini, apaga)
    flash(pos + Vector((0, 0, 1)), ini, ini + 1, forca=0.6)
    anel_choque(pos + Vector((0, 0, 0.1)), ini, ini + 8, cor=(1, 0.85, 0.6), raio=tamanho * 1.6)
    # blocos voando em arco (gravidade de verdade, calculada quadro a quadro)
    fps = _cena().render.fps
    terra = looks.mat_pixel("Detrito", (0.45, 0.33, 0.22), semente=3)
    for i in range(detritos):
        b = _add(bpy.ops.mesh.primitive_cube_add, size=rnd.uniform(0.15, 0.35), location=pos)
        b.visible_shadow = True
        b.data.materials.append(terra)
        ang = rnd.uniform(0, 2 * math.pi)
        vh, vz = rnd.uniform(2, 5), rnd.uniform(4, 8)
        giro = Vector([rnd.uniform(-12, 12) for _ in range(3)])
        for f in range(ini, fim + 1, 2):
            t = (f - ini) / fps
            z = max(0.12, pos.z + 0.3 + vz * t - 4.9 * t * t)
            b.location = pos + Vector((math.cos(ang) * vh * t, math.sin(ang) * vh * t, 0))
            b.location.z = z
            b.rotation_euler = giro * t
            b.keyframe_insert("location", frame=f)
            b.keyframe_insert("rotation_euler", frame=f)
        _visivel(b, ini, fim)


CORACAO = [".XX.XX.", "XXXXXXX", "XXXXXXX", ".XXXXX.", "..XXX..", "...X..."]


def icone(tipo, pos, ini, fim, cam=None, cor=None, tamanho=0.5):
    """Ícone de emoção estilo kids: "coracao" (de pixels), "!?", "!" ou "?". Sempre de frente
    para a câmera, aparece com 'pop' e sobe devagar."""
    if tipo == "coracao":
        cor = cor or (1, 0.15, 0.25)
        me = bpy.data.meshes.new("Coracao")
        bm = bmesh.new()
        px = 1 / 7
        for lin, s in enumerate(CORACAO):
            for col, ch in enumerate(s):
                if ch == "X":
                    r = bmesh.ops.create_cube(bm, size=px)
                    bmesh.ops.translate(bm, verts=r["verts"],
                                        vec=((col - 3) * px, (2.5 - lin) * px, 0))
        bm.to_mesh(me)
        bm.free()
        o = bpy.data.objects.new("Coracao", me)
        _cena().collection.objects.link(o)
        _marcar(o)
    else:
        cor = cor or (1, 0.85, 0.1)
        txt = bpy.data.curves.new("Icone", "FONT")
        txt.body = tipo
        txt.align_x, txt.align_y = "CENTER", "CENTER"
        txt.extrude = 0.08
        txt.size = 1.0
        o = bpy.data.objects.new("Icone", txt)
        _cena().collection.objects.link(o)
        _marcar(o)
    o.data.materials.append(_mat_brilho("Icone_" + tipo, cor, 1.3)[0])
    o.location = pos
    if cam:
        c = o.constraints.new("TRACK_TO")
        c.target = cam
        c.track_axis, c.up_axis = "TRACK_Z", "UP_Y"
    t = tamanho
    _chaves(o, "scale", {ini: (0.01,) * 3, ini + 3: (t * 1.3,) * 3, ini + 5: (t,) * 3,
                         max(ini + 5, fim - 2): (t,) * 3, fim: (0.01,) * 3})
    _chaves(o, "location", {ini: Vector(pos), fim: Vector(pos) + Vector((0, 0, 0.4))})
    _visivel(o, ini, fim)
    return o


def coracoes(pos, ini, fim, cam=None, qtd=3):
    """Alguns corações subindo em volta de pos, um depois do outro."""
    for i in range(qtd):
        p = Vector(pos) + Vector((rnd.uniform(-0.6, 0.6), 0, rnd.uniform(-0.2, 0.3)))
        icone("coracao", p, ini + i * 3, fim, cam=cam, tamanho=rnd.uniform(0.3, 0.45))


def tremida_camera(cam, ini, fim, forca=0.15):
    """Câmera chacoalhando entre ini e fim (modificador Noise nas curvas de posição)."""
    if not any(fc.data_path == "location" for fc in looks.fcurves(cam)):
        cam.keyframe_insert("location", frame=ini)
    for fc in looks.fcurves(cam):
        if fc.data_path != "location":
            continue
        m = fc.modifiers.new("NOISE")
        m.scale = 1.0
        m.strength = 2 * forca
        m.phase = rnd.uniform(0, 100)
        m.use_restricted_range = True
        m.frame_start, m.frame_end = ini, fim
        m.blend_in = m.blend_out = 1
