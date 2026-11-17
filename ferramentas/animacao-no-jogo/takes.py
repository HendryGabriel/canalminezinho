import os as _os
PROJ = _os.environ.get('ANIM_PROJETO', _os.getcwd())
"""Tomadas do short 'Queda sem paraquedas'. uso: python takes.py t01 [t02 ...]
Cada take: prepara fora da gravacao, grava, limpa."""
import sys, time, math, random, json
import motor as M
import estudio as E
import mc
from motor import C, snd, snd_cam

random.seed(3)
cam = M.Camera()


def esperar_chunks(s=3.0):
    time.sleep(s)


def limpar_tudo():
    for t in ('pato', 'deb', 'fogo', 'carro', 'marc', 'aviao_d'):
        mc.cmd(f'kill @e[tag={t}]')
    mc.cmd('kill @e[type=armor_stand]')
    mc.cmd('kill @e[type=item]')


def fim():
    cam.fim(); limpar_tudo()
    mc.cmd('stopsound @a')


# ======================= aviao =======================
AV = dict(x0=335, x1=357, y=292, z=1990)


def aviao_blocos():
    x0, x1, y, z = AV['x0'], AV['x1'], AV['y'], AV['z']
    B = []
    for x in range(x0, x1 + 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                b = 'white_concrete'
                if dy == 0 and dz != 0 and x % 2 == 0 and x0 + 3 < x < x1 - 2: b = 'light_blue_stained_glass'
                if dy == -1: b = 'light_gray_concrete'
                B.append((x, y + dy, z + dz, b))
    for dy in (-1, 0):
        B.append((x1 + 1, y + dy, z, 'white_concrete'))
    B.append((x1 + 1, y, z - 1, 'light_blue_stained_glass')); B.append((x1 + 1, y, z + 1, 'light_blue_stained_glass'))
    for x in range(x0 + 9, x0 + 14):
        for dz in range(-11, 12):
            if abs(dz) <= 1: continue
            if x - (x0 + 9) > 4 - abs(dz) // 4: continue
            B.append((x, y - 1, z + dz, 'white_concrete' if abs(dz) < 10 else 'red_concrete'))
    for dz in (-5, 5):
        for x in range(x0 + 9, x0 + 12):
            B.append((x, y - 2, z + dz, 'gray_concrete'))
    for x in range(x0, x0 + 3):
        for dy in range(2, 6 - (x - x0)):
            B.append((x, y + dy, z, 'red_concrete'))
        for dz in range(-4, 5):
            if abs(dz) <= 1: continue
            B.append((x, y + 1, z + dz, 'white_concrete'))
    return B


def aviao_montar():
    for (x, y, z, b) in aviao_blocos():
        C(f'setblock {x} {y} {z} {b}')


def aviao_explodir():
    B = aviao_blocos()
    C(f"fill {AV['x0'] - 1} {AV['y'] - 3} {AV['z'] - 12} {AV['x1'] + 2} {AV['y'] + 6} {AV['z'] + 12} air")
    M.bola_fogo(AV['x0'] + 12, AV['y'], AV['z'], r=7, dur=16)
    snd('entity.generic.explode', AV['x0'] + 12, AV['y'], AV['z'], 4, 0.8)
    random.shuffle(B)
    for (x, y, z, b) in B[:70]:
        cx, cz = AV['x0'] + 12, AV['z']
        dx, dy, dz = x - cx, y - AV['y'], z - cz
        n = math.sqrt(dx * dx + dy * dy + dz * dz) + 0.5
        v = random.uniform(0.3, 0.8)
        s = random.uniform(0.5, 1.2)
        m = M.R(random.uniform(0, 360), random.uniform(-80, 80), random.uniform(-80, 80)) @ M.T(-s / 2, -s / 2, -s / 2) @ M.S(s, s, s)
        g = random.randint(0, 3)
        C('summon armor_stand %.2f %.2f %.2f {Tags:["deb","deb_c"],Invisible:1b,Small:1b,Silent:1b,Invulnerable:1b,'
          'Motion:[%.3f,%.3f,%.3f],Passengers:[{id:"minecraft:block_display",Tags:["deb","deb_d","deb_g%d"],'
          'block_state:"minecraft:%s",transformation:%s}]}'
          % (x + 0.5, y, z + 0.5, dx / n * v, dy / n * v + 0.25, dz / n * v, g, b, M.mat_nbt(m)))
    import threading
    threading.Thread(target=M._girar, args=('deb', 6, 0.4), daemon=True).start()


def t01():
    """0.0-4.0 aviao explode, pato e arremessado na direcao da camera"""
    limpar_tudo()
    aviao_montar()
    cx, cy, cz = AV['x0'] + 12, AV['y'], AV['z']
    cpos = (cx + 9, cy + 1.5, cz + 17)
    yaw, pit = M.yp(cpos, (cx - 2, cy + 0.5, cz))
    cam.criar(*cpos, yaw, pit)
    p = M.Pato()
    esperar_chunks(4)
    alvo = (cpos[0] - 2.2, cpos[1] - 2.0, cpos[2] - 4.5)

    def acao(ev):
        time.sleep(0.5)
        ev('explode')
        aviao_explodir()
        p.criar(cx + 1, cy, cz + 1, ori=(30, 0, 0), pose='estrela')
        ev('pato')
        ori = [30, 0, 0]

        def tick(t):
            u = min(1.0, t / 3.0); e = 1 - (1 - u) ** 2
            x = cx + 1 + (alvo[0] - cx - 1) * e
            y = cy + (alvo[1] - cy) * e + 3.0 * math.sin(math.pi * u)
            z = cz + 1 + (alvo[2] - cz - 1) * e
            p.mover(x, y, z)
            if int(t * 20) % 5 == 0:
                ori[1] += 40; ori[2] += 22
                p.posar(ori=tuple(ori), dur=5)
        M.Relogio(3.4, tick)
    E.gravar('t01', acao, 4.4)
    fim()
    C(f"fill {AV['x0'] - 1} {AV['y'] - 3} {AV['z'] - 12} {AV['x1'] + 2} {AV['y'] + 6} {AV['z'] + 12} air")


ROSTO = {}
OLHO = 1.02      # olho da camera acima do display do rig
SUBIR = 6.0      # graus a mais para baixo: personagem fica um pouco acima do centro (longe da legenda)


LAG = 0.0   # testado: compensar adiantamento piorou (v4); sem compensacao o centro bate (v3)


def mirar(off, ori=None, local=None, k=1.0, vel=(0, 0, 0)):
    """yaw/pitch que poem o centro do personagem (ou o ponto 'local' do corpo, ex. a cabeca) no centro do quadro.
    vel = velocidade do rig (blocos/s): compensa o adiantamento dos passageiros em movimento"""
    vx, vy, vz = off[0] + vel[0] * LAG, off[1] - OLHO + vel[1] * LAG, off[2] + vel[2] * LAG
    if local is not None:
        w = M.R(*ori)[:3, :3] @ [local[0] * k, local[1] * k, local[2] * k]
        vx, vy, vz = vx + w[0], vy + w[1], vz + w[2]
    yaw = math.degrees(math.atan2(-vx, vz))
    pitch = -math.degrees(math.atan2(vy, math.hypot(vx, vz))) + SUBIR
    return yaw, pitch


def queda_montada(nome, base, yaw, pitch, off, ori, pose, dur, vel, extra=None, vento=True, k=1.0):
    """camera e pato no mesmo rig descendo a 'vel' b/s. extra(t, p) chamado a cada tick."""
    limpar_tudo()
    x, y, z = base
    yaw, pitch = mirar(off, ori, ROSTO.pop('_alvo', None), k, (0, -vel, 0))
    cam.criar(x, y, z, yaw, pitch)
    p = M.Pato(escala=k)
    for a in ('fechar', 'boca_ab', 'brava'):
        if a in ROSTO: setattr(p, a, ROSTO.pop(a))
    p.criar(x, y, z, ori=ori, pose=pose, off=off)
    p.montar()
    esperar_chunks(3)

    def acao(ev):
        ev('inicio_acao')
        if vento:
            snd_cam('item.elytra.flying', 0.8, 1.0)

        def tick(t):
            cam.mover(x, y - vel * t, z)
            if extra: extra(t, p, ev)
        M.Relogio(dur, tick)
    E.gravar(nome, acao, dur + 0.4)
    fim()
    return p


def t02():
    """4.0-8.5 ar rarefeito, desmaia: pato girando devagar, olhos fecham"""
    st = {'o': [180, 20, 0], 'f': False}

    def extra(t, p, ev):
        k = int(t * 20)
        if k % 10 == 0:
            st['o'][2] += 18; st['o'][1] += 8
            p.olhos_fechados = t > 2.4
            pose = 'desmaio' if t > 2.4 else 'estrela2'
            if t > 2.4 and not st['f']:
                st['f'] = True; ev('desmaia')
            p.posar(pose=pose, ori=tuple(st['o']), dur=10)
    queda_montada('t02', (420, 300, 1950), 0, 8, (0, -0.45, 3.2), (180, 20, 0), 'estrela2', 4.9, 6, extra)


def t03():
    """8.5-10.8 acorda mais embaixo, atravessando as nuvens"""
    def extra(t, p, ev):
        if abs(t - 0.6) < 0.03:
            p.olhos_fechados = False; p.posar(pose='estrela', dur=6); ev('acorda')
    queda_montada('t03', (345, 256, 1990), 0, 28, (0, -1.3, 2.6), (180, 25, 0), 'desmaio', 2.9, 11, extra)


def t04():
    """10.8-14.1 caindo de cabeca"""
    def extra(t, p, ev):
        p.posar(ori=(0, 180, math.sin(t * 3) * 8), dur=3) if int(t * 20) % 3 == 0 else None
    queda_montada('t04', (500, 228, 1900), 90, 2, (-3.2, -0.2, 0), (0, 180, 0), 'mergulho', 3.7, 20, extra)


def t05():
    """14.1-17.6 abre bracos e pernas, vento empurra (camera embaixo olhando pra cima)"""
    def extra(t, p, ev):
        if abs(t - 0.5) < 0.03:
            ev('abre'); p.posar(pose='estrela', dur=14)
        if t > 1.4 and int(t * 20) % 4 == 0:
            p.posar(juntas={'braco_e': (random.uniform(-6, 6), 0, 115 + random.uniform(-6, 6)),
                            'braco_d': (random.uniform(-6, 6), 0, -115 + random.uniform(-6, 6))}, dur=4)
    queda_montada('t05', (450, 210, 1960), 180, -55, (0, 2.6, -2.2), (0, 90, 0), 'mergulho', 3.9, 12, extra)


ROD = None


def rod_y(z):
    global ROD
    if ROD is None:
        ROD = {int(k): v for k, v in json.load(open(_os.path.join(PROJ, 'checkpoints', 'rodovia_perfil.json'))).items()}
    z0 = int(math.floor(z)); f = z - z0
    a, b = ROD.get(z0, ROD[min(ROD)]), ROD.get(z0 + 1, ROD[min(ROD)])
    return a + (b - a) * f


def aplainar_rodovia(x0=268, z0=2100, z1=2145, y=75):
    for z in range(z0, z1 + 1):
        C(f'fill {x0 - 9} {y + 1} {z} {x0 + 9} {y + 6} {z} air')
        C(f'fill {x0 - 9} {y - 3} {z} {x0 + 9} {y - 1} {z} dirt replace air')
        C(f'fill {x0 - 9} {y} {z} {x0 + 9} {y} {z} snow_block')
        C(f'fill {x0 - 6} {y} {z} {x0 + 6} {y} {z} gray_concrete')
        for xx in (x0 - 6, x0 + 6):
            C(f'setblock {xx} {y} {z} white_concrete')
        C(f'setblock {x0} {y} {z} light_gray_concrete')
        if z % 6 < 3:
            for xx in (x0 - 3, x0 + 3):
                C(f'setblock {xx} {y} {z} yellow_concrete')
    C('kill @e[type=item]')


def t06():
    """17.6-21.4 duas vezes mais rapido que um carro: camera atras do pato, carro embaixo ficando pra tras"""
    limpar_tudo()
    Y = 75; X = 265.5
    vc, vp, dur = 5.0, 10.0, 3.9
    zc0, zp0 = 2104.0, 2096.0
    cam.criar(X - 1.5, Y + 10, zp0, 0, 30)
    p = M.Pato(escala=1.3)
    p.criar(X - 1.5, Y + 10, zp0, ori=(0, 75, 0), pose='estrela', off=(1.5, -2.6, 5.5))
    p.montar()
    car = M.Modelo(M.CARRO, 'carro')
    car.criar(X - 2.5, Y + 1, zc0, ori=(0, 0, 0), brilho=False)
    esperar_chunks(4)

    def acao(ev):
        ev('inicio_acao')
        snd_cam('item.elytra.flying', 0.7, 1.2)
        st = {'p': False}

        def tick(t):
            cam.mover(X - 1.5, Y + 10 - 0.5 * t, zp0 + vp * t)
            car.mover(X - 2.5, Y + 1, zc0 + vc * t)
            if not st['p'] and zp0 + 5.5 + vp * t > zc0 + vc * t:
                st['p'] = True; ev('ultrapassa')
            if int(t * 20) % 6 == 0:
                p.posar(ori=(random.uniform(-3, 3), 75, random.uniform(-5, 5)), dur=6)
        M.Relogio(dur, tick)
    E.gravar('t06', acao, dur + 0.3)
    fim()


def t07():
    """21.4-26.0 vento alto, dificil manter os olhos abertos (close no rosto)"""
    def extra(t, p, ev):
        k = int(t * 20)
        if k % 3 == 0:
            p.olhos_fechados = (t > 2.6 and (k // 6) % 3 != 0)
            p.posar(ori=(180, 75 + random.uniform(-3, 3), random.uniform(-4, 4)),
                    juntas={'cabeca': (-60 + random.uniform(-4, 4), random.uniform(-6, 6), 0)}, dur=3)
        if abs(t - 2.6) < 0.03: ev('olhos')
    queda_montada('t07', (560, 250, 2000), 0, -38, (0, 1.05, 1.5), (180, 75, 0), 'estrela', 4.9, 14, extra)


def t08():
    """26.0-28.0 procurando lugar pra pousar (visao do pato, olhando pra baixo)"""
    def extra(t, p, ev):
        if int(t * 20) % 8 == 0:
            p.posar(juntas={'braco_e': (0, 0, 100 + random.uniform(-5, 5)), 'braco_d': (0, 0, -100 + random.uniform(-5, 5))}, dur=8)
    queda_montada('t08', (335, 215, 1985), 0, 88, (0, -1.6, -0.95), (0, 90, 0), 'estrela', 2.5, 7, extra, k=1.2)


LAGO = dict(cx=345, cz=1972, L=98)


def t09():
    """28.0-31.8 lago: nessa velocidade a agua bate como concreto"""
    limpar_tudo()
    cx, cz, L = LAGO['cx'], LAGO['cz'], LAGO['L']
    y0, y1, dur = L + 70, L + 32, 4.2
    cam.criar(cx, y0, cz - 6, 0, 82)
    esperar_chunks(4)

    def acao(ev):
        ev('inicio_acao')
        snd_cam('item.elytra.flying', 0.6, 1.2)
        st = {'c': False}

        def tick(t):
            u = t / dur; u = u * u * (3 - 2 * u)
            cam.mover(cx, y0 + (y1 - y0) * u, cz - 6 + 4 * u)
            if t > 2.3 and not st['c']:
                st['c'] = True; ev('concreto')
                C(f'fill {cx - 22} {L} {cz - 22} {cx + 22} {L} {cz + 22} light_gray_concrete replace water')
                snd(f'block.anvil.land', cx, L + 20, cz, 2, 0.6)
                snd('block.stone.break', cx, L + 20, cz, 2, 0.6)
        M.Relogio(dur, tick)
    E.gravar('t09', acao, dur + 0.3)
    fim()
    C(f'fill {cx - 22} {L} {cz - 22} {cx + 22} {L} {cz + 22} water replace light_gray_concrete')


def voo(nome, pts, dur, sons=None, wait=4):
    """camera sozinha por pontos [(x,y,z,yaw,pitch)], ease global"""
    limpar_tudo()
    p0 = pts[0]
    cam.criar(*p0)
    esperar_chunks(wait)

    def acao(ev):
        ev('inicio_acao')
        if sons: sons()

        def tick(t):
            u = t / dur; u = u * u * (3 - 2 * u)
            n = len(pts) - 1; s = min(n - 1e-9, u * n); i = int(s); f = s - i
            a, b = pts[i], pts[i + 1]
            q = [a[j] + (b[j] - a[j]) * f for j in range(5)]
            cam.mover(q[0], q[1], q[2])
            cam.olhar(q[3], q[4])
        M.Relogio(dur, tick)
    E.gravar(nome, acao, dur + 0.3)
    fim()


def t10a():
    """31.8-33.6 cidade: telhado e rua"""
    voo('t10a', [(302, 190, 1932, 0, 86), (304, 168, 1938, 20, 88)], 2.4)


def t10b():
    """33.6-35.2 campo de terra dura"""
    voo('t10b', [(323, 150, 2006, 0, 86), (323, 132, 2009, -15, 88)], 2.2)


def t11a():
    """35.2-37.35 floresta coberta de neve (ampla)"""
    voo('t11a', [(390, 175, 1985, 0, 32), (390, 160, 2005, 0, 34)], 2.6)


def t11b():
    """37.35-40.5 galhos e neve funda (perto das copas)"""
    voo('t11b', [(378, 96, 2045, -40, 22), (392, 92, 2055, -60, 28)], 3.6)


def anel(cx, cz, y, r, n=40, tag='marc'):
    for i in range(n):
        a = 2 * math.pi * i / n
        x, z = cx + r * math.cos(a), cz + r * math.sin(a)
        yaw = -math.degrees(a)
        m = M.R(yaw + 90, 0, 0) @ M.T(-1.6, 0, -0.9) @ M.S(3.2, 0.4, 1.8)
        C('summon block_display %.2f %.2f %.2f {Tags:["%s"],view_range:20f,brightness:{sky:15,block:15},glow_color_override:16776960,Glowing:1b,'
          'block_state:"minecraft:yellow_concrete",transformation:%s}' % (x, y, z, tag, M.mat_nbt(m)))


def t12a():
    """40.5-43.7 mapa visto de cima: a floresta fica longe, pro lado (anel + linha tracejada)"""
    limpar_tudo()
    cx, cz = 371, 2007
    cam.criar(cx, 224, cz, 180, 90)
    pato_xz = (360, 1978); flo = (393, 2062)
    p = M.Pato(escala=5)
    p.criar(pato_xz[0], 175, pato_xz[1], ori=(-30, 90, 0), pose='estrela')
    esperar_chunks(6)

    def acao(ev):
        time.sleep(0.3)
        ev('anel')
        anel(flo[0], flo[1], 92, 20, n=34)
        snd_cam('block.note_block.chime', 1, 1.2)
        time.sleep(0.6)
        ev('linha')
        dx, dz = flo[0] - pato_xz[0], flo[1] - pato_xz[1]
        L = math.hypot(dx, dz); ux, uz = dx / L, dz / L
        yaw = math.degrees(math.atan2(-dx, dz))
        d = 7
        while d < L - 21:
            x, z = pato_xz[0] + ux * d, pato_xz[1] + uz * d
            m = M.R(yaw, 0, 0) @ M.T(-1.0, 0, -2.5) @ M.S(2.0, 0.4, 5.0)
            C('summon block_display %.2f %.2f %.2f {Tags:["marc"],view_range:20f,brightness:{sky:15,block:15},'
              'block_state:"minecraft:red_concrete",transformation:%s}' % (x, 125, z, M.mat_nbt(m)))
            snd_cam('block.note_block.hat', 0.6, 1.5)
            time.sleep(0.12)
            d += 8
    E.gravar('t12a', acao, 3.8)
    fim()


def t12b():
    """43.7-46.0 inclina o corpo pra frente e vai como um planador"""
    def extra(t, p, ev):
        cam.mover(380, 200 - 7 * t, 1990 + 16 * t)
        if abs(t - 0.4) < 0.03:
            ev('inclina'); p.posar(pose='planador', ori=(0, 65, 0), dur=10)
        if t > 1 and int(t * 20) % 6 == 0:
            p.posar(ori=(random.uniform(-4, 4), 65, random.uniform(-8, 8)), dur=6)
    queda_montada_h('t12b', (380, 200, 1990), 0, 28, (0, -1.6, 3.6), (0, 85, 0), 'estrela', 2.8, extra)


def queda_montada_h(nome, base, yaw, pitch, off, ori, pose, dur, extra, k=1.0):
    """igual queda_montada mas o extra controla a camera"""
    limpar_tudo()
    x, y, z = base
    yaw, pitch = mirar(off, ori, ROSTO.pop('_alvo', None), k, ROSTO.pop('_vel', (0, 0, 0)))
    cam.criar(x, y, z, yaw, pitch)
    p = M.Pato(escala=k)
    for a in ('fechar', 'boca_ab', 'brava'):
        if a in ROSTO: setattr(p, a, ROSTO.pop(a))
    p.criar(x, y, z, ori=ori, pose=pose, off=off)
    p.montar()
    esperar_chunks(3)

    def acao(ev):
        ev('inicio_acao')
        snd_cam('item.elytra.flying', 0.7, 1.0)
        M.Relogio(dur, lambda t: extra(t, p, ev))
    E.gravar(nome, acao, dur + 0.4)
    fim()


def t13():
    """46.0-49.3 funciona, mas devagar. a floresta chegando mais perto"""
    def extra(t, p, ev):
        cam.mover(386, 150 - 9 * t, 2000 + 11 * t)
        if int(t * 20) % 6 == 0:
            p.posar(ori=(random.uniform(-4, 4), 65, random.uniform(-6, 6)), dur=6)
    queda_montada_h('t13', (386, 150, 2000), 0, 30, (0, -1.5, 3.3), (0, 65, 0), 'planador', 3.7, extra)


def t14():
    """49.3-54.6 o chao vindo rapido: pes pra frente, dobra joelhos, abraca a cabeca"""
    def extra(t, p, ev):
        cam.mover(396, 165 - 13 * t, 2048)
        if abs(t - 1.4) < 0.03:
            ev('pes'); p.posar(pose='pouso', ori=(0, 0, 0), dur=10)
        if abs(t - 2.9) < 0.03:
            ev('joelhos'); p.posar(pose='pouso', ori=(0, 0, 0), juntas={'perna_e': (-75, 0, 8), 'perna_d': (-75, 0, -8)}, dur=8)
        if abs(t - 4.2) < 0.03:
            ev('abraca'); p.posar(pose='encolhido', ori=(0, 10, 0), dur=8)
    queda_montada_h('t14', (396, 165, 2048), 90, 12, (-4.3, -0.4, 0), (0, 40, 0), 'planador', 5.6, extra)


ARV = dict(x=298.5, z=2101.5, g=71)
CAM_CHAO = (292.5, 75.0, 2100.5)
CAM_GALHO = (294.3, 81.0, 2100.2)


def t15():
    """54.6-57.5 atravessa os galhos, cada um freia um pouco mais"""
    limpar_tudo()
    x, z = ARV['x'], ARV['z']
    cpos = CAM_GALHO
    yaw, pit = M.yp(cpos, (x, 79, z))
    cam.criar(*cpos, yaw, pit)
    p = M.Pato(escala=1.0)
    p.criar(x, 92, z, ori=(-70, 0, 0), pose='encolhido')
    esperar_chunks(4)

    def acao(ev):
        ev('inicio_acao')
        st = {'y': 92.0, 'v': 12.0, 'feito': set()}

        def tick(t):
            dt = 0.05
            st['y'] -= st['v'] * dt
            y = st['y']
            p.mover(x, y, z)
            by = int(math.floor(y + 0.3))
            for yy in (by, by + 1):
                if yy in st['feito'] or yy < 74: continue
                r = mc.call('world.getBlocks', {'from': {'x': int(x) - 1, 'y': yy, 'z': int(z) - 1}, 'to': {'x': int(x) + 1, 'y': yy, 'z': int(z) + 1}})
                folhas = [b for b in r.get('blocks', []) if 'leaves' in b['id'] or b['id'].endswith(':snow')]
                st['feito'].add(yy)
                if folhas:
                    ev(f'galho{yy}')
                    C(f'fill {int(x) - 1} {yy} {int(z) - 1} {int(x) + 1} {yy} {int(z) + 1} air replace #minecraft:leaves')
                    C(f'fill {int(x) - 1} {yy} {int(z) - 1} {int(x) + 1} {yy} {int(z) + 1} air replace snow')
                    M.destrocos(x, yy + 0.5, z, ['spruce_leaves', 'spruce_leaves', 'snow_block'], n=7, vel=0.35, vy=0.25,
                                tam=(0.25, 0.6), tag='deb', espalhar=0.9, giro=False)
                    snd('block.azalea_leaves.break', x, yy, z, 1.5, 0.8)
                    snd('block.snow.break', x, yy, z, 1.2, 1.0)
                    st['v'] = max(5.0, st['v'] * 0.72)
            if y < 75.5:
                st['v'] = max(st['v'], 6.0)
            if y < 73.0:
                st['v'] = 0
        M.Relogio(3.0, tick)
    E.gravar('t15', acao, 3.3)
    fim()


def preparar_pouso():
    """monte de neve no pouso (ao lado da arvore)"""
    x, z, g = int(ARV['x']), int(ARV['z']), ARV['g']
    C(f'fill {x - 2} {g + 1} {z - 2} {x + 2} {g + 1} {z + 2} snow_block replace #minecraft:replaceable')
    C(f'fill {x - 2} {g + 1} {z - 2} {x + 2} {g + 1} {z + 2} snow_block replace snow')
    C(f'fill {x - 1} {g + 2} {z - 1} {x + 1} {g + 2} {z + 1} snow[layers=4] replace air')
    C(f'fill {x - 2} {g - 5} {z - 2} {x + 2} {g} {z + 2} snow_block')


def t16():
    """57.5-59.9 bate na neve e afunda bem fundo"""
    limpar_tudo()
    preparar_pouso()
    x, z, g = ARV['x'], ARV['z'], ARV['g']
    cpos = CAM_CHAO
    yaw, pit = M.yp(cpos, (x, g + 2.2, z))
    cam.criar(*cpos, yaw, pit)
    p = M.Pato()
    p.criar(x, g + 6, z, ori=(-70, 10, 0), pose='encolhido')
    esperar_chunks(4)

    def acao(ev):
        ev('inicio_acao')
        st = {'y': g + 6.0, 'imp': False}

        def tick(t):
            if not st['imp']:
                st['y'] -= 7 * 0.05
                if st['y'] <= g + 2.2:
                    st['imp'] = True; ev('impacto')
                    xi, zi = int(x), int(z)
                    C(f'fill {xi - 1} {g - 1} {zi - 1} {xi + 1} {g + 2} {zi + 1} air replace snow_block')
                    C(f'fill {xi - 1} {g - 1} {zi - 1} {xi + 1} {g + 2} {zi + 1} air replace snow')
                    C(f'fill {xi - 1} {g - 1} {zi - 1} {xi + 1} {g + 2} {zi + 1} air replace grass_block')
                    C(f'fill {xi - 1} {g - 1} {zi - 1} {xi + 1} {g + 2} {zi + 1} air replace dirt')
                    C(f'fill {xi - 1} {g - 1} {zi - 1} {xi + 1} {g + 2} {zi + 1} air replace #minecraft:replaceable')
                    C(f'fill {xi - 1} {g - 2} {zi - 1} {xi + 1} {g - 2} {zi + 1} powder_snow')
                    M.destrocos(x, g + 2.2, z, ['snow_block'], n=26, vel=0.45, vy=0.55, tam=(0.3, 0.8), tag='deb', espalhar=1.2)
                    snd('block.snow.break', x, g + 2, z, 3, 0.6); snd('block.powder_snow.break', x, g + 2, z, 3, 0.7)
                    snd('entity.generic.big_fall', x, g + 2, z, 2, 0.8)
            else:
                st['y'] = max(g - 1.2, st['y'] - 4 * 0.05)
            p.mover(x, st['y'], z)
        M.Relogio(2.4, tick)
    E.gravar('t16', acao, 2.8)
    cam.fim()


def t17():
    """59.9-61.0 tudo fica em silencio (buraco na neve)"""
    x, z, g = ARV['x'], ARV['z'], ARV['g']
    C('kill @e[tag=deb]')
    xi, zi = int(x), int(z)
    C(f'fill {xi - 1} {g - 2} {zi - 1} {xi + 1} {g - 2} {zi + 1} snow_block')
    C(f'fill {xi - 1} {g - 1} {zi - 1} {xi + 1} {g - 1} {zi + 1} snow[layers=3]')
    voo('t17', [(x - 2.6, g + 3.6, z - 0.6, -75, 50), (x - 2.0, g + 3.1, z - 0.5, -75, 56)], 2.8, wait=2)


def t18():
    """61.0-63.8 se desenterra e fica de pe. voce conseguiu."""
    limpar_tudo()
    x, z, g = ARV['x'], ARV['z'], ARV['g']
    cpos = (CAM_CHAO[0] + 2.6, CAM_CHAO[1] - 0.6, CAM_CHAO[2] + 0.3)
    yaw, pit = M.yp(cpos, (x, g + 2.0, z))
    cam.criar(*cpos, yaw, pit)
    p = M.Pato()
    p.criar(x, g - 1.2, z, ori=(80, 0, 0), pose='encolhido')
    xi, zi = int(x), int(z)
    C(f'fill {xi - 2} {g + 2} {zi - 2} {xi + 1} {g + 5} {zi + 2} air replace #minecraft:leaves')
    esperar_chunks(3)

    def acao(ev):
        time.sleep(0.2)
        ev('sai')
        M.destrocos(x, g + 1.5, z, ['snow_block'], n=14, vel=0.3, vy=0.4, tam=(0.25, 0.6), tag='deb', espalhar=1.0)
        snd('block.snow.break', x, g + 1, z, 2, 0.9)
        p.posar(pose='pe', dur=12)

        def tick(t):
            y = g - 1.2 + min(1.0, t / 1.0) * 2.4
            p.mover(x, y, z)
            if abs(t - 1.9) < 0.03:
                ev('conseguiu'); p.posar(pose='bracos_cima', dur=6)
                snd('entity.player.levelup', x, g + 2, z, 1, 1.0)
        M.Relogio(3.4, tick)
    E.gravar('t18', acao, 4.4)
    fim()


if __name__ == '__main__':
    for n in sys.argv[1:]:
        print('==', n)
        globals()[n]()
