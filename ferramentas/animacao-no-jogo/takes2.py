"""Tomadas v2: Steve + cenario set_queda (coordenadas so de SET). uso: python takes2.py t01 [...]"""
import sys, os, time, math, random, json
import motor as M
M.Pato = M.Steve            # todos os takes usam o Steve
import takes as T0           # reaproveita voo, anel, aviao, limpar...
from takes import cam, fim, voo, anel, queda_montada, queda_montada_h, esperar_chunks, mirar, ROSTO
import estudio as E
import mc
from motor import C, snd, snd_cam
from set_queda import SET, Y

random.seed(4)
LX, LZ, LR = SET['lago']
VX, VZ = SET['vila']
FX0, FZ0, FX1, FZ1 = SET['campo']
FCX, FCZ, FRX, FRZ = SET['floresta']
AX, AZ = SET['arvore']
RX, RZ0, RZ1 = SET['rodovia']


def limpar_tudo():
    for t in ('pato', 'steve', 'deb', 'fogo', 'carro', 'marc', 'aviao_d'):
        mc.cmd(f'kill @e[tag={t}]')
    mc.cmd('kill @e[type=armor_stand]'); mc.cmd('kill @e[type=item]')


T0.limpar_tudo = limpar_tudo

# aviao sobre o lago (norte do mapa)
T0.AV.update(x0=288, x1=310, y=300, z=-1640)


def t01():
    """0.0-4.0 aviao (displays) voando no ceu, explode, Steve e arremessado"""
    limpar_tudo()
    AV = T0.AV
    cx, cy, cz = AV['x0'] + 12, AV['y'], AV['z']
    cpos = (cx - 4, cy + 4.0, cz + 46)
    yaw, pit = M.yp(cpos, (cx - 5, cy + 1.0, cz))
    cam.criar(*cpos, yaw, pit)          # teleporta antes: chunks carregados
    C(f"fill {AV['x0'] - 30} {cy - 3} {cz - 12} {AV['x1'] + 3} {cy + 6} {cz + 12} air")
    # aviao como displays (pode voar); posicao final = posicao das pecas da explosao
    VX, DUR_VOO = 7.0, 1.5
    x_ini = cx - VX * DUR_VOO
    for i, (x, y, z, b) in enumerate(T0.aviao_blocos()):
        C('summon block_display %.2f %.2f %.2f {Tags:["aviao_d"],teleport_duration:2,view_range:6f,'
          'block_state:"minecraft:%s",transformation:{translation:[%.2ff,%.2ff,%.2ff],left_rotation:[0f,0f,0f,1f],'
          'scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}' % (x_ini, cy, cz, b, x - cx, y - cy, z - cz))
    p = M.Steve()
    esperar_chunks(4)
    alvo = (cpos[0] - 1.0, cpos[1] - 2.0, cpos[2] - 9.0)

    def acao(ev):
        ev('voo')
        snd('entity.minecart.riding', cx, cy, cz, 3, 0.5)
        M.Relogio(DUR_VOO, lambda t: C(f'tp @e[tag=aviao_d] {x_ini + VX * (t + 0.05):.2f} {cy} {cz}'))
        ev('explode')
        M.bola_fogo(cx, cy, cz, r=7, dur=16)             # fogo primeiro, aviao some atras dele
        snd('entity.generic.explode', cx, cy, cz, 4, 0.8)
        C('kill @e[tag=aviao_d]')
        bf = M.bola_fogo; M.bola_fogo = lambda *a, **k: None
        try:
            T0.aviao_explodir()
        finally:
            M.bola_fogo = bf
        p.criar(cx + 1, cy, cz + 1, ori=(30, 0, 0), pose='estrela')
        p.fechar = 1.0; p.boca_ab = 1.0
        ori = [30, 0, 0]

        def tick(t):
            u = min(1.0, t / 3.0); e = 1 - (1 - u) ** 2
            p.mover(cx + 1 + (alvo[0] - cx - 1) * e, cy + (alvo[1] - cy) * e + 3.0 * math.sin(math.pi * u),
                    cz + 1 + (alvo[2] - cz - 1) * e)
            if int(t * 20) % 5 == 0:
                ori[1] += 40; ori[2] += 22
                p.posar(ori=tuple(ori), dur=5)
        M.Relogio(2.8, tick)
    E.gravar('t01', acao, 4.6)
    T0.fim()
    C('kill @e[tag=aviao_d]')
    C(f"fill {AV['x0'] - 1} {cy - 3} {cz - 12} {AV['x1'] + 2} {cy + 6} {cz + 12} air")


def t02():
    """ar rarefeito: bem alto, o mapa minusculo embaixo"""
    st = {'o': [180, 20, 0], 'f': False}

    def extra(t, p, ev):
        if int(t * 20) % 4 == 2 and 1.6 < t < 2.6:
            p.fechar = min(1.0, (t - 1.6) / 0.8); p.posar(dur=4)
        if int(t * 20) % 10 == 0:
            st['o'][2] += 18; st['o'][1] += 8
            pose = 'desmaio' if t > 2.4 else 'estrela2'
            if t > 2.4 and not st['f']:
                st['f'] = True; ev('desmaia')
            p.fechar = 0.0 if t < 1.6 else min(1.0, (t - 1.6) / 0.8)
            p.posar(pose=pose, ori=tuple(st['o']), juntas={'cabeca': (40, 0, 25)} if t > 2.4 else None, dur=10)
    queda_montada('t02', (300, 310, -1620), 0, 10, (0, -0.55, 3.0), (180, 20, 0), 'estrela2', 4.9, 6, extra)


def t03():
    """acorda mais embaixo atravessando as nuvens (nuvens a oeste)"""
    def extra(t, p, ev):
        k = int(t * 20)
        alvo = {4: 0.5, 7: 1.0, 9: 0.0, 16: 1.0, 18: 0.0}
        if k in alvo and abs(t * 20 - k) < 0.5:
            p.fechar = alvo[k]; p.posar(dur=2)
        if k == 12 and abs(t * 20 - k) < 0.5:
            p.posar(pose='estrela', dur=6); ev('acorda')
    ROSTO.update(fechar=1.0)
    queda_montada('t03', (46.5, 252, -1427.5), 0, 28, (0, -1.3, 2.6), (180, 25, 0), 'desmaio', 2.9, 8, extra)


def t04():
    def extra(t, p, ev):
        if int(t * 20) % 3 == 0:
            p.posar(ori=(0, 180, math.sin(t * 3) * 8), dur=3)
    queda_montada('t04', (300, 215, -1640), 90, 2, (-3.8, 0.3, 0), (0, 180, 0), 'mergulho', 3.7, 20, extra)


def t05():
    def extra(t, p, ev):
        if abs(t - 0.5) < 0.03:
            ev('abre'); p.brava = 0.8; p.fechar = 0.3; p.posar(pose='estrela', dur=14)
        if t > 1.4 and int(t * 20) % 4 == 0:
            p.posar(juntas={'braco_e': (random.uniform(-6, 6), 0, 120 + random.uniform(-6, 6)),
                            'braco_d': (random.uniform(-6, 6), 0, -120 + random.uniform(-6, 6))}, dur=4)
    queda_montada('t05', (300, 200, -1620), 180, -55, (0, 2.6, -2.2), (0, 90, 0), 'mergulho', 3.9, 12, extra)


def t06():
    """mais rapido que um carro na rodovia"""
    limpar_tudo()
    X = RX - 0.5
    vc, vp, dur = 5.0, 10.0, 3.9
    zc0, zp0 = RZ0 + 60.0, RZ0 + 52.0
    cam.criar(X - 1.5, Y + 10, zp0, *mirar((1.5, -2.6, 5.5), vel=(0, -0.5, 10.0)))
    p = M.Steve(); p.k = 1.3
    p.criar(X - 1.5, Y + 10, zp0, ori=(0, 75, 0), pose='estrela', off=(1.5, -2.6, 5.5))
    p.montar()
    car = M.Modelo(M.CARRO, 'carro')
    car.criar(X - 2.5, Y + 1, zc0, ori=(0, 0, 0), brilho=False)
    esperar_chunks(4)

    def acao(ev):
        ev('inicio_acao'); snd_cam('item.elytra.flying', 0.7, 1.2)

        def tick(t):
            cam.mover(X - 1.5, Y + 10 - 0.5 * t, zp0 + vp * t)
            car.mover(X - 2.5, Y + 1, zc0 + vc * t)
            if int(t * 20) % 6 == 0:
                p.posar(ori=(random.uniform(-3, 3), 75, random.uniform(-5, 5)), dur=6)
        M.Relogio(dur, tick)
    E.gravar('t06', acao, dur + 0.3)
    T0.fim()


def t07():
    """vento alto, dificil manter os olhos abertos: close no rosto, careta, olhos fechando"""
    def extra(t, p, ev):
        if int(t * 20) % 3 == 0:
            p.brava = 1.0
            p.boca_ab = 0.35 + 0.25 * math.sin(t * 9)
            p.fechar = (0.45 + 0.1 * math.sin(t * 13)) if t < 2.6 else (0.85 + 0.15 * math.sin(t * 17))
            p.posar(ori=(180, 75 + random.uniform(-3, 3), random.uniform(-5, 5)),
                    juntas={'cabeca': (-60 + random.uniform(-6, 6), random.uniform(-10, 10), random.uniform(-6, 6))}, dur=3)
        if abs(t - 2.6) < 0.03: ev('olhos')
    ROSTO.update(brava=1.0, fechar=0.4, _alvo=(0, 16 * M.U - M.Steve.CENTRO, 0))
    queda_montada('t07', (300, 250, -1680), 0, 0, (0, 1.6, 1.25), (180, 75, 0), 'estrela', 4.9, 14, extra)


def t08():
    """procurando lugar: visao de cima com o Steve no quadro, o mapa inteiro embaixo"""
    def extra(t, p, ev):
        if int(t * 20) % 8 == 0:
            p.posar(juntas={'braco_e': (0, 0, 110 + random.uniform(-5, 5)), 'braco_d': (0, 0, -110 + random.uniform(-5, 5))}, dur=8)
    queda_montada('t08', (300, 300, -1560), 0, 88, (0, -2.4, -0.4), (0, 90, 0), 'estrela', 2.5, 7, extra, k=1.0)


def t09():
    """lago logo abaixo; agua vira concreto"""
    limpar_tudo()
    y0, y1, dur = Y + 75, Y + 32, 4.2
    cam.criar(LX, y0, LZ - 5, 0, 84)
    esperar_chunks(4)

    def acao(ev):
        ev('inicio_acao'); snd_cam('item.elytra.flying', 0.6, 1.2)
        st = {'c': False}

        def tick(t):
            u = t / dur; u = u * u * (3 - 2 * u)
            cam.mover(LX, y0 + (y1 - y0) * u, LZ - 5 + 4 * u)
            if t > 2.3 and not st['c']:
                st['c'] = True; ev('concreto')
                C(f'fill {LX - LR - 2} {Y} {LZ - LR - 2} {LX + LR + 2} {Y} {LZ + LR + 2} light_gray_concrete replace water')
                snd('block.anvil.land', LX, Y + 20, LZ, 2, 0.6); snd('block.stone.break', LX, Y + 20, LZ, 2, 0.6)
        M.Relogio(dur, tick)
    E.gravar('t09', acao, dur + 0.3)
    T0.fim()
    C(f'fill {LX - LR - 2} {Y} {LZ - LR - 2} {LX + LR + 2} {Y} {LZ + LR + 2} water replace light_gray_concrete')


def t10a():
    """cidade: telhado e rua (lago na borda de cima)"""
    voo('t10a', [(VX, 160, VZ - 12, 0, 86), (VX + 2, 138, VZ - 6, 15, 88)], 2.4)


def t10b():
    """o campo do lado e terra dura: vila na borda de cima, campo grande enchendo o quadro"""
    cx = (FX0 + FX1) / 2
    voo('t10b', [(cx, 175, FZ0 - 5, 0, 80), (cx, 150, FZ0 + 20, 0, 84)], 2.2)


def t11a():
    """ai voce ve uma floresta coberta de neve: do alto da vila olhando pro sul, a floresta branca e unica, longe"""
    voo('t11a', [(VX, 200, VZ - 20, 0, 30), (VX, 192, VZ, 0, 31)], 2.6)


def t11b():
    """galhos e neve funda: rasante sobre as copas"""
    voo('t11b', [(FCX - 30, Y + 30, FCZ - 18, -40, 22), (FCX - 14, Y + 26, FCZ - 6, -60, 28)], 3.6)


CAM_MAPA = (300, 425, -1412)


def t12a():
    """mapa de cima. O Steve fica perto da camera, no raio camera->lago (aparece 'sobre o lago' sem passar
    do raio de rastreio de ~160 blocos). Anel e linha tracejada entram na edicao (como no video original)."""
    limpar_tudo()
    cx, cy, cz = CAM_MAPA
    cam.criar(cx, cy, cz, 180, 90)
    f = 0.09
    px, py, pz = cx + (LX - cx) * f, cy + (Y - cy) * f, cz + (LZ - cz) * f
    p = M.Steve(); p.k = 0.9
    p.criar(px, py, pz, ori=(0, 90, 0), pose='estrela')
    esperar_chunks(6)

    def acao(ev):
        ev('mapa')
        def tick(t):
            if int(t * 20) % 8 == 0:
                p.posar(juntas={'braco_e': (0, 0, 115 + random.uniform(-8, 8)), 'braco_d': (0, 0, -115 + random.uniform(-8, 8))}, dur=8)
        M.Relogio(3.6, tick)
    E.gravar('t12a', acao, 4.0)
    T0.fim()


def _anel_bonito(cx, cz, y, rx, rz, n=48):
    for i in range(n):
        a = 2 * math.pi * i / n
        x, z = cx + rx * math.cos(a), cz + rz * math.sin(a)
        m = M.R(-math.degrees(math.atan2(rz * math.cos(a), -rx * math.sin(a))) , 0, 0) @ M.T(-2.0, 0, -1.2) @ M.S(4.0, 0.5, 2.4)
        C('summon block_display %.2f %.2f %.2f {Tags:["marc"],view_range:30f,brightness:{sky:15,block:15},'
          'block_state:"minecraft:yellow_concrete",transformation:%s}' % (x, y, z, M.mat_nbt(m)))


def anel(cx, cz, y, r, n=48, tag='marc'):
    _anel_bonito(cx, cz, y, FRX + 8, FRZ + 8, n)


def t12b():
    """inclina e vai como planador: atras do Steve, a floresta la na frente"""
    def extra(t, p, ev):
        cam.mover(300, 150 - 7 * t, -1520 + 16 * t)
        if abs(t - 0.4) < 0.03:
            ev('inclina'); p.posar(pose='planador', ori=(0, 65, 0), dur=10)
        if t > 1 and int(t * 20) % 6 == 0:
            p.posar(ori=(random.uniform(-4, 4), 65, random.uniform(-8, 8)), dur=6)
    ROSTO['_vel'] = (0, -7, 16)
    queda_montada_h('t12b', (300, 150, -1520), 0, 30, (0, -1.6, 3.6), (0, 85, 0), 'estrela', 2.8, extra)


def t13():
    """funciona mas devagar: o campo passa embaixo, a floresta cresce no quadro"""
    def extra(t, p, ev):
        cam.mover(300, 128 - 6 * t, -1420 + 22 * t)
        if int(t * 20) % 6 == 0:
            p.posar(ori=(random.uniform(-4, 4), 65, random.uniform(-6, 6)), dur=6)
    ROSTO['_vel'] = (0, -6, 22)
    queda_montada_h('t13', (300, 128, -1420), 0, 26, (0, -1.5, 3.3), (0, 65, 0), 'planador', 3.7, extra)


def t14():
    """chao vindo rapido sobre a floresta: pes, joelhos, abraca a cabeca (vista lateral)"""
    def extra(t, p, ev):
        cam.mover(AX + 6, 140 - 12 * t, AZ - 10)
        if abs(t - 1.4) < 0.03:
            ev('pes'); p.posar(pose='pouso', ori=(0, 0, 0), dur=10)
        if abs(t - 2.9) < 0.03:
            ev('joelhos'); p.posar(pose='joelhos', ori=(0, 0, 0), dur=8)
        if abs(t - 4.2) < 0.03:
            ev('abraca'); p.fechar = 1.0; p.boca_ab = 1.0; p.posar(pose='encolhido', ori=(0, 10, 0), dur=8)
    ROSTO['_vel'] = (0, -12, 0)
    queda_montada_h('t14', (AX + 6, 140, AZ - 10), 90, 14, (-4.3, -0.4, 0), (0, 40, 0), 'planador', 5.6, extra)


# ---------------- pouso (arvore-alvo no centro da floresta) ----------------
G = Y                       # snow_block do chao
PX, PZ = AX - 1.5, AZ - 1.5  # ponto de pouso, colado no tronco
CAM_CHAO = (295.3, 67.6, -1223.3)
CAM_GALHO = (294.6, 71.0, -1222.6)


def preparar_pouso():
    x, z, g = int(PX), int(PZ), G
    C(f'fill {x - 2} {g - 5} {z - 2} {x + 2} {g} {z + 2} snow_block')
    C(f'fill {x - 2} {g + 1} {z - 2} {x + 2} {g + 1} {z + 2} snow_block replace #minecraft:replaceable')
    C(f'fill {x - 2} {g + 1} {z - 2} {x + 2} {g + 1} {z + 2} snow_block replace snow')
    C(f'fill {x - 1} {g + 2} {z - 1} {x + 1} {g + 2} {z + 1} snow[layers=4] replace air')


def t15():
    """atravessa os galhos: cada galho quebra e freia"""
    limpar_tudo()
    x, z = PX, PZ
    yaw, pit = M.yp(CAM_GALHO, (x, G + 6, z))
    cam.criar(*CAM_GALHO, yaw, pit)
    p = M.Steve()
    p.criar(x, G + 20, z, ori=(-60, 0, 0), pose='encolhido')
    esperar_chunks(3)

    def acao(ev):
        ev('inicio_acao')
        st = {'y': G + 20.0, 'v': 11.0, 'feito': set()}

        def tick(t):
            st['y'] -= st['v'] * 0.05
            y = st['y']; p.mover(x, y, z)
            by = int(math.floor(y + 0.3))
            for yy in (by, by + 1):
                if yy in st['feito'] or yy < G + 3: continue
                st['feito'].add(yy)
                r = mc.call('world.getBlocks', {'from': {'x': int(x) - 1, 'y': yy, 'z': int(z) - 1}, 'to': {'x': int(x) + 1, 'y': yy, 'z': int(z) + 1}})
                if any('leaves' in b['id'] or b['id'].endswith(':snow') for b in r.get('blocks', [])):
                    ev(f'galho{yy}')
                    C(f'fill {int(x) - 1} {yy} {int(z) - 1} {int(x) + 1} {yy} {int(z) + 1} air replace #minecraft:leaves')
                    C(f'fill {int(x) - 1} {yy} {int(z) - 1} {int(x) + 1} {yy} {int(z) + 1} air replace snow')
                    M.destrocos(x, yy + 0.5, z, ['spruce_leaves', 'spruce_leaves', 'snow_block'], n=7, vel=0.35, vy=0.25,
                                tam=(0.25, 0.6), tag='deb', espalhar=0.9, giro=False)
                    snd('block.azalea_leaves.break', x, yy, z, 1.5, 0.8); snd('block.snow.break', x, yy, z, 1.2, 1.0)
                    st['v'] = max(4.5, st['v'] * 0.75)
            if y < G + 2.4:
                st['v'] = 0
        M.Relogio(3.2, tick)
    E.gravar('t15', acao, 3.5)
    T0.fim()


def t16():
    """bate na neve e afunda"""
    limpar_tudo(); preparar_pouso()
    x, z, g = PX, PZ, G
    yaw, pit = M.yp(CAM_CHAO, (x, g + 2.2, z))
    cam.criar(*CAM_CHAO, yaw, pit)
    p = M.Steve()
    p.fechar = 1.0; p.boca_ab = 0.8
    p.criar(x, g + 6, z, ori=(-60, 10, 0), pose='encolhido')
    esperar_chunks(3)

    def acao(ev):
        ev('inicio_acao')
        st = {'y': g + 6.0, 'imp': False}

        def tick(t):
            if not st['imp']:
                st['y'] -= 7 * 0.05
                if st['y'] <= g + 2.2:
                    st['imp'] = True; ev('impacto')
                    xi, zi = int(x), int(z)
                    for b in ['snow_block', 'snow', '#minecraft:replaceable']:
                        C(f'fill {xi - 1} {g - 1} {zi - 1} {xi + 1} {g + 2} {zi + 1} air replace {b}')
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
    """silencio: o buraco na neve"""
    x, z, g = PX, PZ, G
    C('kill @e[tag=deb]')
    xi, zi = int(x), int(z)
    C(f'fill {xi - 1} {g - 2} {zi - 1} {xi + 1} {g - 2} {zi + 1} snow_block')
    C(f'fill {xi - 1} {g - 1} {zi - 1} {xi + 1} {g - 1} {zi + 1} snow[layers=3]')
    c0 = (CAM_CHAO[0] + 1.2, g + 4.2, CAM_CHAO[2] - 0.6)
    y0, p0 = M.yp(c0, (x, g, z))
    c1 = (CAM_CHAO[0] + 1.6, g + 3.8, CAM_CHAO[2] - 0.8)
    y1, p1 = M.yp(c1, (x, g, z))
    voo('t17', [(*c0, y0, p0), (*c1, y1, p1)], 2.8, wait=2)


def t18():
    """se desenterra, fica de pe, voce conseguiu"""
    limpar_tudo()
    x, z, g = PX, PZ, G
    cpos = (CAM_CHAO[0] + 0.8, CAM_CHAO[1] - 0.6, CAM_CHAO[2])
    yaw, pit = M.yp(cpos, (x, g + 1.6, z))
    cam.criar(*cpos, yaw, pit)
    p = M.Steve()
    face = M.yp((x, 0, z), (cpos[0], 0, cpos[2]))[0]
    p.criar(x, g - 1.4, z, ori=(face, 0, 0), pose='encolhido')
    xi, zi = int(x), int(z)
    C(f'fill {xi - 2} {g + 2} {zi - 2} {xi + 2} {g + 5} {zi + 2} air replace #minecraft:leaves')
    esperar_chunks(3)

    def acao(ev):
        time.sleep(0.2)
        ev('sai')
        M.destrocos(x, g + 1.5, z, ['snow_block'], n=14, vel=0.3, vy=0.4, tam=(0.25, 0.6), tag='deb', espalhar=1.0)
        snd('block.snow.break', x, g + 1, z, 2, 0.9)
        p.posar(pose='pe', dur=12)

        def tick(t):
            p.mover(x, g - 1.4 + min(1.0, t / 1.0) * 2.4, z)
            if abs(t - 1.9) < 0.03:
                ev('conseguiu'); p.boca_ab = 0.7; p.posar(pose='bracos_cima', dur=6)
            if abs(t - 0.9) < 0.03:
                p.fechar = 1.0; p.posar(dur=2)
            if abs(t - 1.1) < 0.03:
                p.fechar = 0.0; p.posar(dur=2)
                snd('entity.player.levelup', x, g + 2, z, 1, 1.0)
        M.Relogio(3.4, tick)
    E.gravar('t18', acao, 4.4)
    T0.fim()


if __name__ == '__main__':
    E.sessao_inicio(os.environ.get('SESSAO', 'sessao'))
    try:
        for n in sys.argv[1:]:
            print('==', n, flush=True)
            globals()[n]()
    finally:
        E.sessao_fim()
