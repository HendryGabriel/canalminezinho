"""Tomadas v4 (suaves): todo movimento de camera e de personagem solto e feito em segmentos lineares
interpolados pelo cliente (teleport_duration), em vez de um tp por tick (que tremia com o jitter do Python).
Camera sem rotacao durante o plano; planos parados ganham um deslize lento; cada plano grava 0,8 s a mais.
uso: python takes3.py t01 [...]"""
import sys, os, time, math, random
import motor as M
import takes as T0
import takes2 as T2
import estudio as E
import mc
from motor import C, snd, snd_cam
from set_queda import SET, Y

M.Pato = M.Steve
cam = T0.cam
mirar, ROSTO, limpar_tudo, esperar_chunks = T0.mirar, T0.ROSTO, T2.limpar_tudo, T0.esperar_chunks
LX, LZ, LR = SET['lago']
VX, VZ = SET['vila']
FX0, FZ0, FX1, FZ1 = SET['campo']
FCX, FCZ, FRX, FRZ = SET['floresta']
AX, AZ = SET['arvore']
RX, RZ0, RZ1 = SET['rodovia']
SOBRA = 0.8


class Trajeto:
    """sel percorre f(t)->(x,y,z) em segmentos de 'passo' s; o cliente interpola cada segmento.
    teleport_duration = passo+1 tick: o proximo tp chega antes do fim, entao nunca para."""
    def __init__(self, sel, f, passo=0.5, dy=0.0):
        self.sel, self.f, self.passo, self.dy = sel, f, passo, dy
        self.tk = min(59, int(round(passo * 20)) + 1)
        self.prox = None

    def preparar(self):
        C(f'execute as {self.sel} run data merge entity @s {{teleport_duration:{self.tk}}}')

    def _tp(self, t):
        x, y, z = self.f(t)
        C(f'tp {self.sel} {x:.3f} {y + self.dy:.3f} {z:.3f}')

    def tick(self, t):
        if self.prox is None:
            self._tp(self.passo); self.prox = self.passo
        elif t >= self.prox - 0.026:
            self.prox += self.passo; self._tp(self.prox)


class Vel:
    """velocidade constante aplicada pelo SERVIDOR a cada tick (datapack queda: tick -> tp ~vx ~vy ~vz).
    Unico jeito de a camera (jogador montado) andar liso: o cliente segue o veiculo tick a tick."""
    def __init__(self, sel, v3, canal='cam'):
        self.sel, self.v3, self.canal = sel, v3, canal
        self.tag = 'voa_cam' if canal == 'cam' else 'voa_b'
        self.on = False

    def preparar(self):
        vx, vy, vz = (c / 20 for c in self.v3)
        C(f'data merge storage queda:{self.canal} {{vx:{vx:.5f}d,vy:{vy:.5f}d,vz:{vz:.5f}d}}')

    def tick(self, t):
        if not self.on:
            C(f'tag {self.sel} add {self.tag}'); self.on = True

    def parar(self):
        C(f'tag {self.sel} remove {self.tag}')


def cam_trajeto(f, passo=None):
    """f linear -> velocidade constante no servidor"""
    a, b = f(0.0), f(1.0)
    return Vel(f'@e[tag={M.CAM}]', tuple(b[i] - a[i] for i in range(3)), 'cam')


def vel_b(sel, f):
    a, b = f(0.0), f(1.0)
    return Vel(sel, tuple(b[i] - a[i] for i in range(3)), 'b')


def rodar(dur, *coisas, extra=None):
    """laco de 20 Hz que alimenta os trajetos e o extra(t)"""
    for c in coisas: c.preparar()
    time.sleep(0.12)      # o cliente recebe a nova teleport_duration antes do 1o tp
    def tick(t):
        for c in coisas: c.tick(t)
        if extra: extra(t)
    try:
        M.Relogio(dur, tick)
    finally:
        for c in coisas:
            if hasattr(c, 'parar'): c.parar()


# ---------------- moldes novos ----------------
def queda_montada(nome, base, yaw, pitch, off, ori, pose, dur, vel, extra=None, vento=True, k=1.0, v3=None):
    """camera + Steve no mesmo rig, velocidade constante (v3 = vetor; padrao: cai a 'vel')"""
    limpar_tudo()
    v3 = v3 or (0, -vel, 0)
    x, y, z = base
    yaw, pitch = mirar(off, ori, ROSTO.pop('_alvo', None), k, v3)
    cam.criar(x, y, z, yaw, pitch)
    p = M.Pato(escala=k)
    for a in ('fechar', 'boca_ab', 'brava'):
        if a in ROSTO: setattr(p, a, ROSTO.pop(a))
    p.criar(x, y, z, ori=ori, pose=pose, off=off)
    p.montar()
    esperar_chunks(3)
    D = dur + SOBRA
    tr = cam_trajeto(lambda t: (x + v3[0] * t, y + v3[1] * t, z + v3[2] * t), passo=min(2.5, D))

    def acao(ev):
        ev('inicio_acao')
        if vento:
            snd_cam('item.elytra.flying', 0.8, 1.0)
        rodar(D, tr, extra=(lambda t: extra(t, p, ev)) if extra else None)
    E.gravar(nome, acao, D + 0.3)
    T0.fim()
    return p


def queda_montada_h(nome, base, yaw, pitch, off, ori, pose, dur, extra, k=1.0, v3=(0, 0, 0)):
    return queda_montada(nome, base, yaw, pitch, off, ori, pose, dur, 0, extra=extra, k=k, v3=v3)


def voo(nome, pts, dur, sons=None, wait=4):
    """camera em linha reta do 1o ao ultimo ponto, velocidade constante, olhar fixo (o do 1o ponto)"""
    limpar_tudo()
    a, b = pts[0], pts[-1]
    cam.criar(*a)
    esperar_chunks(wait)
    D = dur + SOBRA
    tr = cam_trajeto(lambda t: tuple(a[j] + (b[j] - a[j]) * t / dur for j in range(3)), passo=min(2.5, D))

    def acao(ev):
        ev('inicio_acao')
        if sons: sons()
        rodar(D, tr)
    E.gravar(nome, acao, D + 0.3)
    T0.fim()


for mod in (T0, T2):
    mod.queda_montada, mod.queda_montada_h, mod.voo = queda_montada, queda_montada_h, voo


# ---------------- planos redefinidos ----------------
def t01():
    """aviao voando (displays, 1 segmento linear), explode, Steve arremessado em segmentos; camera recua devagar"""
    limpar_tudo()
    AV = T0.AV
    cx, cy, cz = AV['x0'] + 12, AV['y'], AV['z']
    cpos = (cx - 6, cy + 3.0, cz + 42)
    yaw, pit = M.yp(cpos, (cx - 6, cy + 0.5, cz))
    cam.criar(*cpos, yaw, pit)
    C(f"fill {AV['x0'] - 30} {cy - 3} {cz - 12} {AV['x1'] + 3} {cy + 6} {cz + 12} air")
    VXA, DUR_VOO = 7.0, 1.5
    x_ini = cx - VXA * DUR_VOO
    for (x, y, z, b) in T0.aviao_blocos():
        C('summon block_display %.2f %.2f %.2f {Tags:["aviao_d"],teleport_duration:31,view_range:6f,'
          'block_state:"minecraft:%s",transformation:{translation:[%.2ff,%.2ff,%.2ff],left_rotation:[0f,0f,0f,1f],'
          'scale:[1f,1f,1f],right_rotation:[0f,0f,0f,1f]}}' % (x_ini, cy, cz, b, x - cx, y - cy, z - cz))
    p = M.Steve()
    esperar_chunks(4)
    alvo = (cpos[0] - 1.0, cpos[1] - 2.0, cpos[2] - 9.0)
    D = 4.4 + SOBRA
    tc = cam_trajeto(lambda t: (cpos[0], cpos[1] + 0.25 * t, cpos[2] + 0.6 * t), passo=2.6)

    def acao(ev):
        ev('voo')
        snd('entity.minecart.riding', cx, cy, cz, 3, 0.5)
        C(f'tp @e[tag=aviao_d] {cx:.2f} {cy} {cz}')
        tc.preparar()
        st = {'exp': False, 'tr': None, 'ori': [30, 0, 0], 'te': 0}

        def tick(t):
            tc.tick(t)
            if not st['exp'] and t >= DUR_VOO:
                st['exp'] = True; st['te'] = t; ev('explode')
                M.bola_fogo(cx, cy, cz, r=7, dur=16)
                snd('entity.generic.explode', cx, cy, cz, 4, 0.8)
                C('kill @e[tag=aviao_d]')
                bf = M.bola_fogo; M.bola_fogo = lambda *a, **k: None
                try:
                    T0.aviao_explodir()
                finally:
                    M.bola_fogo = bf
                p.fechar = 1.0; p.boca_ab = 1.0
                p.criar(cx + 1, cy, cz + 1, ori=(30, 0, 0), pose='estrela', tdur=6)

                def f(u):
                    u = min(1.0, u / 3.0); e = 1 - (1 - u) ** 2
                    return (cx + 1 + (alvo[0] - cx - 1) * e, cy + (alvo[1] - cy) * e + 3.0 * math.sin(math.pi * u),
                            cz + 1 + (alvo[2] - cz - 1) * e)
                st['tr'] = Trajeto('@e[tag=steve]', f, passo=0.25); st['tr'].preparar()
            if st['tr']:
                u = t - st['te']
                st['tr'].tick(u)
                if int(u * 20) % 5 == 0:
                    st['ori'][1] += 40; st['ori'][2] += 22
                    p.posar(ori=tuple(st['ori']), dur=6)
        try:
            M.Relogio(D, tick)
        finally:
            tc.parar()
    E.gravar('t01', acao, D + 0.2)
    T0.fim()
    C('kill @e[tag=aviao_d]')
    C(f"fill {AV['x0'] - 1} {cy - 3} {cz - 12} {AV['x1'] + 2} {cy + 6} {cz + 12} air")


def t02():
    """ar rarefeito: Steve girando devagar, olhos fecham com 'desmaia' (~2,7-3,3 s)"""
    st = {'o': [180, 20, 0], 'f': False}

    def extra(t, p, ev):
        k = int(t * 20)
        mud = False
        if k % 10 == 0:
            st['o'][2] += 18; st['o'][1] += 8; mud = True
        if 2.6 < t < 3.5 and k % 3 == 0:
            p.fechar = min(1.0, (t - 2.6) / 0.7); mud = True
        if t > 3.2 and not st['f']:
            st['f'] = True; ev('desmaia')
        if mud:
            p.posar(pose='desmaio' if t > 3.2 else 'estrela2', ori=tuple(st['o']),
                    juntas={'cabeca': (40, 0, 25)} if t > 3.2 else None, dur=10)
    queda_montada('t02', (300, 310, -1620), 0, 10, (0, -0.55, 3.0), (180, 20, 0), 'estrela2', 4.9, 6, extra)


def t06():
    """mais rapido que um carro: camera+Steve num segmento linear, carro num segmento linear"""
    limpar_tudo()
    X = RX - 0.5
    vc, vp = 5.0, 10.0
    zc0, zp0 = RZ0 + 60.0, RZ0 + 52.0
    off = (1.5, -2.6, 5.5)
    cam.criar(X - 1.5, Y + 10, zp0, *mirar(off))
    p = M.Steve(); p.k = 1.3
    p.criar(X - 1.5, Y + 10, zp0, ori=(0, 75, 0), pose='estrela', off=off)
    p.montar()
    car = M.Modelo(M.CARRO, 'carro')
    car.criar(X - 2.5, Y + 1, zc0, ori=(0, 0, 0), brilho=False)
    esperar_chunks(4)
    D = 3.9 + SOBRA
    tc = cam_trajeto(lambda t: (X - 1.5, Y + 10 - 0.5 * t, zp0 + vp * t), passo=2.4)
    tcar = vel_b('@e[tag=carro]', lambda t: (X - 2.5, Y + 1, zc0 + vc * t))

    def acao(ev):
        ev('inicio_acao'); snd_cam('item.elytra.flying', 0.7, 1.2)

        def ex(t):
            if int(t * 20) % 6 == 0:
                p.posar(ori=(random.uniform(-3, 3), 75, random.uniform(-5, 5)), dur=7)
        rodar(D, tc, tcar, extra=ex)
    E.gravar('t06', acao, D + 0.3)
    T0.fim()


def t09():
    """lago logo abaixo (descida linear); agua vira concreto em ~2,7 s"""
    limpar_tudo()
    y0, dur = Y + 75, 4.2
    D = dur + SOBRA
    cam.criar(LX, y0, LZ - 5, 0, 84)
    esperar_chunks(4)
    tc = cam_trajeto(lambda t: (LX, y0 - 9.0 * t, LZ - 5 + 0.9 * t), passo=2.5)

    def acao(ev):
        ev('inicio_acao'); snd_cam('item.elytra.flying', 0.6, 1.2)
        st = {'c': False}

        def ex(t):
            if t > 2.7 and not st['c']:
                st['c'] = True; ev('concreto')
                C(f'fill {LX - LR - 2} {Y} {LZ - LR - 2} {LX + LR + 2} {Y} {LZ + LR + 2} light_gray_concrete replace water')
                snd('block.anvil.land', LX, Y + 20, LZ, 2, 0.6); snd('block.stone.break', LX, Y + 20, LZ, 2, 0.6)
        rodar(D, tc, extra=ex)
    E.gravar('t09', acao, D + 0.3)
    T0.fim()
    C(f'fill {LX - LR - 2} {Y} {LZ - LR - 2} {LX + LR + 2} {Y} {LZ + LR + 2} water replace light_gray_concrete')


def t10a():
    voo('t10a', [(VX, 160, VZ - 12, 0, 86), (VX + 2, 140, VZ - 6, 0, 86)], 2.4)


def t10b():
    cx = (FX0 + FX1) / 2
    voo('t10b', [(cx, 175, FZ0 - 5, 0, 80), (cx, 152, FZ0 + 20, 0, 80)], 2.2)


def t11a():
    """floresta nevada unica e longe; serra ao fundo esconde o fim do mapa"""
    voo('t11a', [(VX, 150, VZ - 20, 0, 22), (VX, 146, VZ, 0, 22)], 2.6)


def t11b():
    voo('t11b', [(FCX - 30, Y + 30, FCZ - 18, -40, 22), (FCX - 16, Y + 27, FCZ - 7, -40, 22)], 3.6)


def t12a():
    """mapa de cima, descendo devagar (zoom natural)"""
    limpar_tudo()
    cx, cy, cz = T2.CAM_MAPA
    cam.criar(cx, cy, cz, 180, 90)
    f = 0.09
    px, py, pz = cx + (LX - cx) * f, cy + (Y - cy) * f, cz + (LZ - cz) * f
    p = M.Steve(); p.k = 0.9
    p.criar(px, py, pz, ori=(0, 90, 0), pose='estrela')
    esperar_chunks(6)
    D = 3.6 + SOBRA
    tc = cam_trajeto(lambda t: (cx, cy - 2.5 * t, cz), passo=2.2)
    tp = vel_b('@e[tag=steve]', lambda t: (px, py - 2.5 * t * 0.97, pz))

    def acao(ev):
        ev('mapa')

        def ex(t):
            if int(t * 20) % 8 == 0:
                p.posar(juntas={'braco_e': (0, 0, 115 + random.uniform(-8, 8)), 'braco_d': (0, 0, -115 + random.uniform(-8, 8))}, dur=9)
        rodar(D, tc, tp, extra=ex)
    E.gravar('t12a', acao, D + 0.2)
    T0.fim()


def t12b():
    def extra(t, p, ev):
        if abs(t - 0.4) < 0.03:
            ev('inclina'); p.posar(pose='planador', ori=(0, 65, 0), dur=10)
        if t > 1 and int(t * 20) % 6 == 0:
            p.posar(ori=(random.uniform(-4, 4), 65, random.uniform(-8, 8)), dur=7)
    queda_montada_h('t12b', (300, 150, -1520), 0, 30, (0, -1.6, 3.6), (0, 85, 0), 'estrela', 3.6, extra, v3=(0, -7, 16))


def t13():
    def extra(t, p, ev):
        if int(t * 20) % 6 == 0:
            p.posar(ori=(random.uniform(-4, 4), 65, random.uniform(-6, 6)), dur=7)
    queda_montada_h('t13', (300, 128, -1420), 0, 26, (0, -1.5, 3.3), (0, 65, 0), 'planador', 3.7, extra, v3=(0, -6, 22))


def t14():
    """pes (2,25 s), joelhos (3,25 s), abraca a cabeca (3,85 s) — no tempo da fala"""
    def extra(t, p, ev):
        if abs(t - 2.25) < 0.03:
            ev('pes'); p.posar(pose='pouso', ori=(0, 0, 0), dur=8)
        if abs(t - 3.25) < 0.03:
            ev('joelhos'); p.posar(pose='joelhos', ori=(0, 0, 0), dur=7)
        if abs(t - 3.85) < 0.03:
            ev('abraca'); p.fechar = 1.0; p.boca_ab = 1.0; p.posar(pose='encolhido', ori=(0, 10, 0), dur=7)
    queda_montada_h('t14', (AX + 6, 140, AZ - 10), 90, 14, (-4.3, -0.4, 0), (0, 40, 0), 'planador', 5.6, extra, v3=(0, -12, 0))


def _queda_steve(x, z, ys, fps=20):
    """ys = lista de alturas por tick -> funcao f(t) para Trajeto"""
    def f(t):
        i = t * fps
        a = int(min(len(ys) - 1, max(0, math.floor(i)))); b = min(len(ys) - 1, a + 1)
        u = min(1.0, max(0.0, i - a))
        return (x, ys[a] + (ys[b] - ys[a]) * u, z)
    return f


def t15():
    """atravessa os galhos: trajetoria precalculada (freia em cada camada de folhas), camera desliza devagar"""
    limpar_tudo()
    x, z = T2.PX, T2.PZ
    G = T2.G
    yaw, pit = M.yp(T2.CAM_GALHO, (x, G + 6, z))
    cam.criar(*T2.CAM_GALHO, yaw, pit)
    # camadas com folha na coluna do Steve
    r = mc.call('world.getBlocks', {'from': {'x': int(x) - 1, 'y': G + 3, 'z': int(z) - 1}, 'to': {'x': int(x) + 1, 'y': G + 22, 'z': int(z) + 1}})
    camadas = sorted({b['y'] for b in r.get('blocks', []) if 'leaves' in b['id'] or b['id'].endswith(':snow')}, reverse=True)
    y, v, ys, hits, feitos = G + 12.0, 9.0, [], [], set()
    for k in range(int(3.6 * 20) + 2):
        ys.append(y)
        for c in camadas:
            if c not in feitos and y <= c + 0.8:
                feitos.add(c); hits.append((k / 20, c)); v = max(4.0, v * 0.75)
        y = max(G - 1.6, y - max(v, 5.0) / 20)   # continua caindo e afunda na neve (nunca para em cima)
    p = M.Steve()
    p.criar(x, ys[0], z, ori=(-60, 0, 0), pose='encolhido')
    p.fechar = 1.0; p.posar(dur=1)
    esperar_chunks(3)
    D = 3.0 + SOBRA
    c0 = T2.CAM_GALHO
    tc = cam_trajeto(lambda t: (c0[0] - 0.15 * t, c0[1] - 0.35 * t, c0[2] + 0.1 * t), passo=1.9)
    ts = Trajeto('@e[tag=steve]', _queda_steve(x, z, ys), passo=0.15)

    def acao(ev):
        ev('inicio_acao')
        pend = list(hits)

        def ex(t):
            while pend and t >= pend[0][0]:
                _, yy = pend.pop(0); ev(f'galho{yy}')
                C(f'fill {int(x) - 1} {yy} {int(z) - 1} {int(x) + 1} {yy} {int(z) + 1} air replace #minecraft:leaves')
                C(f'fill {int(x) - 1} {yy} {int(z) - 1} {int(x) + 1} {yy} {int(z) + 1} air replace snow')
                M.destrocos(x, yy + 0.5, z, ['spruce_leaves', 'spruce_leaves', 'snow_block'], n=7, vel=0.35, vy=0.25,
                            tam=(0.25, 0.6), tag='deb', espalhar=0.9, giro=False)
                snd('block.azalea_leaves.break', x, yy, z, 1.5, 0.8); snd('block.snow.break', x, yy, z, 1.2, 1.0)
        rodar(D, tc, ts, extra=ex)
    E.gravar('t15', acao, D + 0.3)
    T0.fim()


CAM_POUSO = (293.5, 69.2, -1221.5)


def t16():
    """bate na neve (0,4 s) e afunda; camera desliza devagar"""
    limpar_tudo(); T2.preparar_pouso()
    x, z, g = T2.PX, T2.PZ, T2.G
    c0 = CAM_POUSO
    yaw, pit = M.yp(c0, (x, g + 2.4, z))
    cam.criar(*c0, yaw, pit)
    ys, y, imp = [], g + 3.4, None
    for k in range(int(3.4 * 20) + 2):
        ys.append(y)
        if imp is None:
            y -= 6 / 20
            if y <= g + 2.2: imp = k / 20
        else:
            y = max(g - 1.6, y - 7 / 20)
    p = M.Steve(); p.fechar = 1.0; p.boca_ab = 0.8
    p.criar(x, ys[0], z, ori=(-60, 10, 0), pose='encolhido')
    esperar_chunks(3)
    D = 2.4 + SOBRA
    tc = cam_trajeto(lambda t: (c0[0] - 0.2 * t, c0[1] + 0.12 * t, c0[2] + 0.15 * t), passo=1.7)
    ts = Trajeto('@e[tag=steve]', _queda_steve(x, z, ys), passo=0.15)

    def acao(ev):
        ev('inicio_acao')
        st = {'imp': False}

        def ex(t):
            if not st['imp'] and t >= imp:
                st['imp'] = True; ev('impacto')
                xi, zi = int(x), int(z)
                for b in ['snow_block', 'snow', '#minecraft:replaceable']:
                    C(f'fill {xi - 1} {g - 1} {zi - 1} {xi + 1} {g + 2} {zi + 1} air replace {b}')
                C(f'fill {xi - 1} {g - 2} {zi - 1} {xi + 1} {g - 2} {zi + 1} powder_snow')
                M.destrocos(x, g + 2.2, z, ['snow_block'], n=26, vel=0.45, vy=0.55, tam=(0.3, 0.8), tag='deb', espalhar=1.2)
                snd('block.snow.break', x, g + 2, z, 3, 0.6); snd('block.powder_snow.break', x, g + 2, z, 3, 0.7)
                snd('entity.generic.big_fall', x, g + 2, z, 2, 0.8)
        rodar(D, tc, ts, extra=ex)
    E.gravar('t16', acao, D + 0.3)
    cam.fim()


def t17():
    """silencio: buraco na neve, camera recua devagar (linear)"""
    x, z, g = T2.PX, T2.PZ, T2.G
    C('kill @e[tag=deb]')
    xi, zi = int(x), int(z)
    C(f'fill {xi - 1} {g - 2} {zi - 1} {xi + 1} {g - 2} {zi + 1} snow_block')
    C(f'fill {xi - 1} {g - 1} {zi - 1} {xi + 1} {g - 1} {zi + 1} snow[layers=3]')
    c0 = (CAM_POUSO[0] + 0.8, g + 5.2, CAM_POUSO[2] - 0.8)
    y0, p0 = M.yp(c0, (x, g - 0.5, z))
    voo('t17', [(*c0, y0, p0), (c0[0] - 0.4, c0[1] + 0.35, c0[2] + 0.4, y0, p0)], 2.8, wait=2)


def t18():
    """se desenterra (subida em segmentos), pisca, bracos pra cima com 'conseguiu' (2,1 s)"""
    limpar_tudo()
    x, z, g = T2.PX, T2.PZ, T2.G
    cpos = (T2.CAM_CHAO[0] + 0.8, T2.CAM_CHAO[1] - 0.6, T2.CAM_CHAO[2])
    yaw, pit = M.yp(cpos, (x, g + 1.6, z))
    cam.criar(*cpos, yaw, pit)
    p = M.Steve()
    face = M.yp((x, 0, z), (cpos[0], 0, cpos[2]))[0]
    p.criar(x, g - 1.4, z, ori=(face, 0, 0), pose='encolhido')
    xi, zi = int(x), int(z)
    C(f'fill {xi - 2} {g + 2} {zi - 2} {xi + 2} {g + 5} {zi + 2} air replace #minecraft:leaves')
    esperar_chunks(3)
    D = 3.4 + SOBRA
    tc = cam_trajeto(lambda t: (cpos[0] + 0.12 * t, cpos[1] + 0.05 * t, cpos[2] + 0.18 * t), passo=2.1)

    def subida(t):
        u = min(1.0, max(0.0, (t - 0.2) / 1.0)); u = u * u * (3 - 2 * u)
        return (x, g - 1.4 + u * 2.4, z)
    ts = Trajeto('@e[tag=steve]', subida, passo=0.2)

    def acao(ev):
        ev('sai')
        C('kill @e[tag=deb]')
        M.destrocos(x, g + 1.5, z, ['snow_block'], n=10, vel=0.45, vy=0.5, tam=(0.2, 0.45), tag='deb', espalhar=1.0)
        snd('block.snow.break', x, g + 1, z, 2, 0.9)
        p.posar(pose='pe', dur=14)
        st = set()

        def ex(t):
            for (tt, nome) in ((0.9, 'limpa'), (1.1, 'pisca'), (1.3, 'abre'), (2.1, 'conseguiu')):
                if t >= tt and nome not in st:
                    st.add(nome)
                    if nome == 'limpa': C('kill @e[tag=deb]')
                    if nome == 'pisca': p.fechar = 1.0; p.posar(dur=2)
                    if nome == 'abre': p.fechar = 0.0; p.posar(dur=2)
                    if nome == 'conseguiu':
                        ev('conseguiu'); p.boca_ab = 0.7; p.posar(pose='bracos_cima', dur=6)
                        snd('entity.player.levelup', x, g + 2, z, 1, 1.0)
        rodar(D, tc, ts, extra=ex)
    E.gravar('t18', acao, D + 0.2)
    T0.fim()


for n in ('t03', 't04', 't05', 't07', 't08'):
    globals()[n] = getattr(T2, n)


if __name__ == '__main__':
    E.sessao_inicio(os.environ.get('SESSAO', 'sessao_v10'))
    try:
        for n in sys.argv[1:]:
            print('==', n, flush=True)
            globals()[n]()
    finally:
        E.sessao_fim()
