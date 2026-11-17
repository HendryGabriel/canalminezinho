import os as _os
PROJ = _os.environ.get('ANIM_PROJETO', _os.getcwd())
"""v5 'Capivara': ~1 plano por segundo, personagem em todo plano, camera perto, nuvens passando.
Cada plano e gravado separado (camera lisa por velocidade no servidor). A lista PLANOS e a fonte unica:
gravacao (este arquivo) e montagem (montar_v5.py, via planos_v5.json).
uso: python v5.py todos | NOME [NOME...] | nuvens"""
import sys, os, time, math, random, json
import numpy as np
import motor as M
M.Steve = M.Capivara                      # personagem do canal em todos os planos
M.Pato = M.Capivara
import takes as T0
import takes2 as T2
import takes3 as T3
import abertura as AB
T3.SOBRA = 1.2
import estudio as E
import mc
from motor import C, snd, snd_cam
from takes3 import Vel, rodar, limpar_tudo, cam
from set_queda import SET, Y, carregar, descarregar

LX, LZ, LR = SET['lago']
VX, VZ = SET['vila']
FX0, FZ0, FX1, FZ1 = SET['campo']
FCX, FCZ, FRX, FRZ = SET['floresta']
RX, RZ0, RZ1 = SET['rodovia']
COL = (300.5, -1662.5)                     # coluna de queda (com nuvens em volta)
SOBRA = 1.2
OLHO = 1.02
RAIZ = _os.path.join(PROJ)
CENTRO_ROSTO = M.Capivara.CABECA


# ---------------- utilitarios ----------------
def unit(v):
    v = np.array(v, float); return v / (np.linalg.norm(v) + 1e-9)


def ang(d):
    """yaw/pitch do vetor d (convencao do Minecraft)"""
    yaw = math.degrees(math.atan2(-d[0], d[2]))
    pitch = -math.degrees(math.atan2(d[1], math.hypot(d[0], d[2])))
    return yaw, pitch


def rosto_mundo(P, ori, k=1.0):
    w = M.R(*ori)[:3, :3] @ (np.array(CENTRO_ROSTO) * k)
    return np.array(P) + w


PLANOS = []


def plano(nome, t0, t1, linhas=None, s0=0.0, take=None):
    """registra o plano na lista (montagem). take = nome do take gravado (padrao = nome)"""
    PLANOS.append(dict(nome=nome, t0=t0, t1=t1, take=take or nome, s0=s0, linhas=linhas))


# ---------------- plano generico: personagem preso a camera ----------------
def queda(nome, P, ori, pose, dur, v3=(0, -10, 0), rel=None, ombro=None, mira='corpo', acoes=(), agitar=7, giro=(0, 0, 0),
          rosto=None, k=1.0, som='item.elytra.flying', subir=4.0):
    """P = centro da capivara no mundo (inicio). Camera em P+rel, ou 'ombro' = (alvo, dist, alt):
    camera atras do personagem olhando para o alvo (lugar ao fundo)."""
    limpar_tudo()
    P = np.array(P, float)
    if ombro:
        T, d, h = ombro
        u = unit(np.array(T) - P)
        hz = unit([u[0], 0, u[2]]) if abs(u[1]) < 0.99 else np.array([0, 0, 1.0])
        lado = np.array([hz[2], 0, -hz[0]])
        Cw = P + lado * d * 0.85 - u * d * 0.35 + np.array([0, h, 0])
        dirv = unit(0.3 * unit(np.array(T) - Cw) + 0.7 * unit(P - Cw))
        face = unit(0.5 * unit(np.array(T) - P) + 0.5 * unit(Cw - P))
        ori = (ang(face)[0], 40, 0)
    else:
        Cw = P + np.array(rel, float)
        alvo = rosto_mundo(P, ori, k) if mira == 'rosto' else P
        dirv = alvo - Cw
    yaw, pitch = ang(dirv)
    pitch -= subir
    cam.criar(*Cw, yaw, pitch)
    rig = Cw - np.array([0, OLHO, 0])
    off = tuple(P - rig)
    c = M.Capivara(escala=k)
    for a, v in (rosto or {}).items(): setattr(c, a, v)
    c.criar(*Cw, ori=ori, pose=pose, off=off)
    c.montar()
    T0.esperar_chunks(1.6)
    D = dur + SOBRA
    tc = Vel(f'@e[tag={M.CAM}]', v3, 'cam')
    fila = sorted(acoes, key=lambda a: a[0])
    st = {'ori': list(ori), 'pose': pose, 'k': -1}

    def acao(ev):
        ev('inicio_acao')
        if som: snd_cam(som, 0.8, 1.0)

        def ex(t):
            kk = int(t * 20)
            if kk == st['k']: return
            st['k'] = kk
            mudou = False
            while fila and t >= fila[0][0]:
                _, a = fila.pop(0)
                for chave in ('fechar', 'boca_ab', 'brava'):
                    if chave in a: setattr(c, chave, a[chave]); mudou = True
                if 'pose' in a: st['pose'] = a['pose']; mudou = True
                if 'ori' in a: st['ori'] = list(a['ori']); mudou = True
                if 'som' in a: snd_cam(*a['som'])
                if 'ev' in a: ev(a['ev'])
            if kk % 6 == 0 or mudou:
                for i in range(3): st['ori'][i] += giro[i] * 0.3
                jun = None
                if agitar:
                    base = M.POSES_CAPI[st['pose']]
                    fase = kk / 6.0
                    jun = {}
                    for n_, j in enumerate(('braco_e', 'braco_d', 'perna_e', 'perna_d')):
                        b = base.get(j, (0, 0, 0))
                        w = agitar * math.sin(fase * 1.9 + n_ * 1.3)
                        jun[j] = (b[0] + w, b[1], b[2] + 0.6 * w)
                c.posar(pose=st['pose'], ori=tuple(st['ori']), juntas=jun, dur=5 if mudou else 7)
        rodar(D, tc, extra=ex)
    E.gravar(nome, acao, D + 0.2)
    T0.fim()


def piscar(t, dur=0.15, volta=0.45):
    return [(t, {'fechar': 1.0}), (t + dur, {'fechar': volta})]


# ======================= PLANOS =======================
# alturas: a queda acontece na coluna COL; os lugares sao vistos de onde fazem sentido
CX, CZ = COL
F = {'boca_ab': 0.0}


def p_A1():
    """corre pelo corredor (camera atras)"""
    AB.montar(); AB.t01a()


def p_A2():
    """de frente: a capivara correndo em direcao a camera, desesperada"""
    AB.montar()
    V = 8.0
    P = (AB.X1 - 14.5, AB.Y0 + 1.0 + 13.4 * M.U, AB.CZ + 0.5)
    ori = (-90, 6, 0)
    rel = (3.4, 1.1, 0)
    acoes = [(i * 0.2, {'pose': 'corre1' if i % 2 == 0 else 'corre2'}) for i in range(10)]
    _corrida('A2', P, ori, rel, V, acoes, rosto={'fechar': 0.0, 'boca_ab': 1.0, 'brava': 0.6})


def _corrida(nome, P, ori, rel, V, acoes, rosto):
    limpar_tudo()
    P = np.array(P); Cw = P + np.array(rel)
    yaw, pitch = ang(P - Cw)
    cam.criar(*Cw, yaw, pitch - 3)
    rig = Cw - np.array([0, OLHO, 0])
    c = M.Capivara()
    for a, v in rosto.items(): setattr(c, a, v)
    c.criar(*Cw, ori=ori, pose='corre1', off=tuple(P - rig)); c.montar()
    T0.esperar_chunks(1.5)
    D = 1.0 + SOBRA
    tc = Vel(f'@e[tag={M.CAM}]', (V, 0, 0), 'cam')
    fila = list(acoes)

    def acao(ev):
        ev('inicio_acao'); snd_cam('block.fire.ambient', 1.0, 1.0)

        def ex(t):
            while fila and t >= fila[0][0]:
                _, a = fila.pop(0); c.posar(pose=a['pose'], dur=4); snd_cam('block.metal.step', 0.6, 1.2)
            if int(t * 20) % 6 == 0: AB.fumaca(2)
        rodar(D, tc, extra=ex)
    E.gravar(nome, acao, D + 0.2)
    T0.fim()


def p_A3():
    """de fora: a capivara sai voando pela porta traseira e passa pela camera"""
    AB.montar()
    limpar_tudo()
    door = np.array([AB.X1 + 0.5, AB.Y0 + 1.6, AB.CZ + 0.5])
    Cw = door + np.array([7.0, -2.5, 3.5])
    yaw, pitch = ang(door - Cw)
    cam.criar(*Cw, yaw, pitch)
    c = M.Capivara(); c.fechar = 0.0; c.boca_ab = 1.0; c.brava = 0.3
    c.criar(*(door - np.array([2.5, 0, 0])), ori=(-90, 0, 0), pose='salto', tdur=3)
    T0.esperar_chunks(1.5)
    D = 0.9 + SOBRA

    def f(t):
        return (door[0] - 2.5 + 11 * t, door[1] + 1.5 * t - 6 * t * t, door[2] + 1.4 * t)
    tr = T3.Trajeto('@e[tag=steve]', f, passo=0.15)
    tc = Vel(f'@e[tag={M.CAM}]', (0, -1.5, 0), 'cam')
    st = {'o': [-90, 0, 0]}

    def acao(ev):
        ev('inicio_acao'); snd_cam('entity.player.attack.sweep', 0.9, 0.7); snd_cam('item.elytra.flying', 0.7, 1.2)

        def ex(t):
            if int(t * 20) % 3 == 0:
                st['o'][1] += 12; st['o'][2] += 8
                c.posar(pose='estrela', ori=tuple(st['o']), dur=4)
        rodar(D, tc, tr, extra=ex)
    E.gravar('A3', acao, D + 0.2)
    T0.fim()


def p_B1():
    """caindo de frente, o aviao explode atras"""
    AB.t01b()


def p_B2():
    """de baixo: capivara girando, destrocos chovendo do aviao que explodiu"""
    AB.montar()
    limpar_tudo()
    P = np.array([AB.X1 - 12.0, AB.Y0 - 4.0, AB.CZ + 8.5])
    _ = None
    queda_b2(P)


def queda_b2(P):
    """camera caindo devagar; a capivara cai mais rapido, girando, e atravessa o quadro de cima pra baixo"""
    Cw = P + np.array([2.5, -0.8, 4.0])
    yaw, pitch = ang(P + np.array([0, 0.3, 0]) - Cw)
    cam.criar(*Cw, yaw, pitch)
    c = M.Capivara(); c.fechar = 0.0; c.boca_ab = 1.0; c.brava = 0.5
    c.criar(*(P + np.array([0, 3.2, 0])), ori=(0, -60, 0), pose='estrela', tdur=4)
    T0.esperar_chunks(1.2)
    D = 0.85 + SOBRA
    tc = Vel(f'@e[tag={M.CAM}]', (0, -5, 0), 'cam')
    tr = T3.Trajeto('@e[tag=steve]', lambda t: (P[0], P[1] + 3.2 - 9.0 * t, P[2]), passo=0.2)
    st = {'o': [0, -60, 0]}

    def acao(ev):
        ev('inicio_acao'); import threading; threading.Thread(target=AB.explodir, daemon=True).start(); snd_cam('entity.generic.explode', 1.0, 0.9)

        def ex(t):
            if int(t * 20) % 4 == 0:
                st['o'][0] += 16; st['o'][2] += 11
                c.posar(pose='estrela2' if int(t * 5) % 2 else 'estrela', ori=tuple(st['o']), dur=5)
        rodar(D, tc, tr, extra=ex)
    E.gravar('B2', acao, D + 0.2)
    T0.fim()


Y1 = 268    # camada de nuvens alta
Y2 = 232    # camada baixa


def p_C1():
    """'mas o ar aqui em cima...' plano aberto: capivara pequena atravessando a camada de nuvens"""
    queda('C1', (CX, Y1 + 9, CZ), (0, 30, 0), 'estrela2', 1.0, v3=(0, -11, 0), rel=(0.6, 2.6, 5.5), giro=(0, 20, 30),
          rosto={'fechar': 0.0, 'boca_ab': 0.6})


def p_C2():
    """'rarefeito demais pra respirar': close do rosto, boca abrindo e fechando (ofegante)"""
    a = []
    for i in range(8):
        a.append((i * 0.2, {'boca_ab': 1.0 if i % 2 == 0 else 0.3}))
    queda('C2', (CX, Y1 + 34, CZ), (0, 70, 0), 'estrela', 1.7, v3=(0, -9, 0), rel=(0, -0.9, 1.9), mira='rosto',
          acoes=a, rosto={'fechar': 0.0, 'brava': 0.9}, agitar=10)


def p_C3():
    """'entao voce desmaia': close, olhos fechando devagar"""
    a = [(0.15, {'fechar': 0.6}), (0.45, {'fechar': 0.85}), (0.7, {'fechar': 1.0, 'boca_ab': 0.4, 'brava': 0.0})]
    queda('C3', (CX, Y1 + 22, CZ), (0, 70, 0), 'estrela2', 0.9, v3=(0, -9, 0), rel=(0.6, -0.8, 1.8), mira='rosto',
          acoes=a, rosto={'fechar': 0.2, 'boca_ab': 0.6, 'brava': 0.6}, agitar=4)


def p_C4():
    """corpo mole girando (aberto)"""
    queda('C4', (CX + 2, Y1 + 12, CZ - 1), (0, 30, 20), 'desmaio', 0.9, v3=(0, -10, 0), rel=(-2.5, 3.0, 4.0), giro=(30, 50, 40),
          rosto={'fechar': 1.0, 'boca_ab': 0.4}, agitar=0)


def p_D1():
    """'voce acorda': close, pisca e abre os olhos"""
    a = [(0.25, {'fechar': 0.5}), (0.4, {'fechar': 1.0}), (0.55, {'fechar': 0.0, 'boca_ab': 0.8, 'brava': 0.0}),
         (0.9, {'fechar': 1.0}), (1.0, {'fechar': 0.0})]
    queda('D1', (CX + 130, Y2 + 22, CZ), (0, 65, 0), 'desmaio', 1.33, v3=(0, -10, 0), rel=(0.5, 0.4, 1.9), mira='rosto', acoes=a, giro=(0, 0, 18),
          rosto={'fechar': 1.0, 'boca_ab': 0.3}, agitar=3)


def p_D2():
    """'onde o ar e mais denso': atravessa a camada baixa de nuvens (lateral)"""
    queda('D2', (CX + 130, Y2 + 9, CZ), (90, 20, 0), 'estrela', 1.03, v3=(0, -12, 0), rel=(-4.0, 0.4, 0.3),
          rosto={'fechar': 0.0, 'boca_ab': 0.5})


def p_E1():
    """'agora voce esta caindo de cabeca' (lateral, de cabeca pra baixo)"""
    queda('E1', (CX + 130, 205, CZ + 8), (0, 180, 0), 'mergulho', 1.72, v3=(0, -20, 0), rel=(-3.6, 0.3, 0.6),
          rosto={'fechar': 0.3, 'boca_ab': 0.7, 'brava': 0.6}, agitar=4)


def p_E2():
    """'o jeito mais rapido' de baixo pra cima, mergulhando na camera"""
    queda('E2', (CX + 130, 180, CZ + 8), (0, 180, 0), 'mergulho', 0.8, v3=(0, -20, 0), rel=(0.3, -3.4, 1.4),
          rosto={'fechar': 0.3, 'boca_ab': 0.9, 'brava': 0.8}, agitar=4)


def p_E3():
    """'de cair': de cima, a capivara mergulhando e o mapa la embaixo"""
    queda('E3', (CX + 130, 165, CZ + 8), (0, 180, 0), 'mergulho', 0.8, v3=(0, -20, 0), rel=(0.4, 3.6, 0.6),
          rosto={'fechar': 0.3, 'boca_ab': 0.9}, agitar=4, subir=0)


def p_F1():
    """'entao voce abre bem os bracos': de frente, abre"""
    a = [(0.2, {'pose': 'estrela', 'ori': (180, 75, 0)})]
    queda('F1', (CX + 130, 150, CZ - 4), (0, 120, 0), 'mergulho', 1.36, v3=(0, -15, 0), rel=(0, -1.0, 3.2), acoes=a,
          rosto={'fechar': 0.0, 'boca_ab': 0.5, 'brava': 0.5}, agitar=6)


def p_F2():
    """'e as pernas' de baixo, X perfeito"""
    queda('F2', (CX + 130, 135, CZ - 4), (180, 90, 0), 'estrela', 0.78, v3=(0, -12, 0), rel=(0.2, 3.8, 0.4),
          rosto={'fechar': 0.3, 'brava': 0.8}, agitar=9, subir=0)


def p_F3():
    """'o vento empurra contra voce': close do rosto tremendo no vento"""
    a = [(i * 0.15, {'boca_ab': 0.2 + 0.5 * (i % 2), 'fechar': 0.55 + 0.25 * (i % 2)}) for i in range(9)]
    queda('F3', (CX + 130, 125, CZ - 4), (0, 75, 0), 'estrela', 1.32, v3=(0, -12, 0), rel=(0.3, -0.8, 1.8), mira='rosto',
          acoes=a, rosto={'brava': 1.0}, agitar=10)


def p_G1():
    """'mesmo assim, voce ainda esta duas vezes' — lateral, rodovia la embaixo"""
    queda('G1', (RX - 3, Y + 60, RZ0 + 120), (90, 75, 0), 'estrela', 1.9, v3=(0, -12, 4), rel=(-3.8, 1.8, 1.0),
          rosto={'fechar': 0.4, 'boca_ab': 0.5, 'brava': 0.7}, subir=-6)


def p_G2():
    T3.t06()


def p_H1():
    """'nessa velocidade o vento e tao alto': close, careta"""
    a = [(i * 0.12, {'boca_ab': 0.3 + 0.4 * (i % 2)}) for i in range(10)]
    queda('H1', (CX + 130, 140, CZ + 60), (0, 75, 0), 'estrela', 1.22, v3=(0, -12, 0), rel=(0, 0.5, 1.9), mira='rosto',
          acoes=a, rosto={'fechar': 0.6, 'brava': 1.0}, agitar=10)


def p_H2():
    """'que voce nao ouve nada': tapa as orelhas"""
    a = [(0.15, {'pose': 'ouvidos', 'fechar': 1.0, 'boca_ab': 0.2})]
    queda('H2', (CX + 130, 128, CZ + 60), (0, 70, 0), 'estrela', 2.14, v3=(0, -12, 0), rel=(0.8, 1.6, 2.4), acoes=a,
          rosto={'fechar': 0.6, 'brava': 1.0, 'boca_ab': 0.5}, agitar=3)


def p_H3():
    """'difícil manter os olhos abertos': close, olhos se fechando no vento"""
    a = [(i * 0.18, {'fechar': 0.9 if i % 3 else 0.6}) for i in range(9)]
    queda('H3', (CX + 130, 110, CZ + 60), (0, 75, 0), 'estrela', 1.6, v3=(0, -12, 0), rel=(-0.4, 0.5, 1.8), mira='rosto',
          acoes=a, rosto={'brava': 1.0, 'boca_ab': 0.3}, agitar=8)


def p_I1():
    """'voce comeca a procurar': olha pra um lado e pro outro"""
    a = [(0.0, {'ori': (-35, 80, 0)}), (0.5, {'ori': (35, 80, 0)})]
    queda('I1', (430.5, 175, -1600), (0, 80, 0), 'estrela', 0.95, v3=(0, -8, 0), rel=(0, -1.6, 3.0), acoes=a,
          rosto={'fechar': 0.0, 'boca_ab': 0.0}, agitar=5)


def p_I2():
    """'um lugar pra pousar': por cima do ombro, o mapa inteiro la embaixo"""
    queda('I2', (300.5, 205, -1620), (0, 90, 0), 'estrela', 0.96, v3=(0, -8, 0), rel=(0, 3.2, -1.6), subir=-18,
          rosto={'fechar': 0.0})


def p_J1():
    """'tem um lago la embaixo': por cima do ombro, o lago"""
    queda('J1', (300.5, 135, -1612), (0, 70, 0), 'estrela', 1.08, v3=(0, -8, 2), ombro=((LX, Y, LZ), 3.6, 1.0),
          rosto={'fechar': 0.0})


def p_J2():
    """'mas nessa velocidade': close, preocupada"""
    queda('J2', (420.5, 120, -1580), (0, 75, 0), 'estrela', 1.08, v3=(0, -8, 0), rel=(0, -0.9, 1.8), mira='rosto',
          rosto={'fechar': 0.0, 'brava': 0.0, 'boca_ab': 0.2}, acoes=[(0.5, {'boca_ab': 0.7})], agitar=5)


def p_J3():
    """'a agua bate como concreto': rente ao lago, a agua vira concreto e um bloco explode nela"""
    limpar_tudo()
    Cw = np.array([LX + 0.5, Y + 22.0, LZ - LR - 12.0])     # ao norte do lago (a vila fica do outro lado, longe)
    yaw, pitch = ang(np.array([LX, Y + 1, LZ + 2]) - Cw)
    cam.criar(*Cw, yaw, pitch)
    T0.esperar_chunks(2)
    D = 1.64 + SOBRA
    tc = Vel(f'@e[tag={M.CAM}]', (0, -3.0, 3.0), 'cam')      # desce em direcao a agua
    st = {'c': False}

    def acao(ev):
        ev('inicio_acao')

        def ex(t):
            if t > 0.94 and not st['c']:
                st['c'] = True; ev('concreto')
                C(f'fill {LX - LR - 2} {Y} {LZ - LR - 2} {LX + LR + 2} {Y} {LZ + LR + 2} light_gray_concrete replace water')
                for _ in range(6):
                    x, z = LX + random.randint(-12, 12), LZ + random.randint(-10, 10)
                    C(f'fill {x} {Y} {z} {x + random.randint(0, 4)} {Y} {z} gray_concrete replace light_gray_concrete')
                M.destrocos(LX, Y + 1.5, LZ, ['light_gray_concrete', 'gray_concrete', 'stone', 'water'], n=40, vel=0.8, vy=0.95,
                            tam=(0.4, 1.3), tag='deb', espalhar=2.0)
                C(f'particle explosion {LX} {Y + 1} {LZ} 3 0.5 3 0 14 force')
                C(f'particle block{{block_state:"minecraft:stone"}} {LX} {Y + 1} {LZ} 4 1 4 0.3 300 force')
                snd('block.anvil.land', LX, Y + 4, LZ, 3, 0.5); snd('entity.generic.explode', LX, Y + 4, LZ, 2, 1.4)
        rodar(D, tc, extra=ex)
    E.gravar('J3', acao, D + 0.2)
    T0.fim()
    C(f'fill {LX - LR - 2} {Y} {LZ - LR - 2} {LX + LR + 2} {Y} {LZ + LR + 2} water replace light_gray_concrete')
    C(f'fill {LX - LR - 2} {Y} {LZ - LR - 2} {LX + LR + 2} {Y} {LZ + LR + 2} water replace gray_concrete')


def p_K1():
    """'a cidade e so telhado e rua': por cima do ombro, a vila"""
    queda('K1', (300.5, 128, -1545), (0, 70, 0), 'estrela', 0.9, v3=(0, -6, 3), ombro=((VX, Y + 3, VZ), 3.4, 0.9),
          rosto={'fechar': 0.0})


def p_K2():
    """rasante sobre os telhados com a capivara"""
    queda('K2', (VX - 18, Y + 26, VZ + 8), (-90, 60, 0), 'planador', 0.89, v3=(14, -2, 0), rel=(-3.2, 2.0, 1.4),
          rosto={'fechar': 0.0, 'boca_ab': 0.3}, subir=-14)


def p_L1():
    """'e o campo do lado e terra dura': por cima do ombro, o campo"""
    queda('L1', (300.5, 118, -1450), (0, 70, 0), 'estrela', 1.53, v3=(0, -6, 3), ombro=(((FX0 + FX1) / 2, Y, (FZ0 + FZ1) / 2), 3.4, 0.9),
          rosto={'fechar': 0.0, 'boca_ab': 0.2})


def p_M1():
    """'ai voce ve uma floresta': close, olhos arregalam de alegria"""
    a = [(0.25, {'fechar': 0.0, 'boca_ab': 1.0, 'brava': 0.0})]
    queda('M1', (300.5, 110, -1440), (0, 75, 0), 'estrela', 1.0, v3=(0, -6, 0), rel=(0, -0.8, 1.9), mira='rosto', acoes=a,
          rosto={'fechar': 0.45, 'boca_ab': 0.0})


def p_M2():
    """'coberta de neve funda': por cima do ombro, a floresta branca la longe (serra ao fundo)"""
    queda('M2', (300.5, 112, -1430), (0, 60, 0), 'estrela', 1.2, v3=(0, -5, 4), ombro=((FCX, Y + 10, FCZ), 3.4, 0.8),
          rosto={'fechar': 0.0, 'boca_ab': 0.6})


def p_N1():
    T3.t11b()


def p_O1():
    T3.t12a()


def p_P1():
    """'entao voce inclina o corpo pra frente' (lateral)"""
    a = [(0.25, {'pose': 'planador', 'ori': (0, 65, 0)})]
    queda('P1', (300.5, 150, -1500), (0, 85, 0), 'estrela', 1.34, v3=(0, -7, 16), rel=(-3.6, 0.4, 0.4), acoes=a,
          rosto={'fechar': 0.0, 'brava': 0.8})


def p_P2():
    """'e vai ate ela': de tras, a floresta na frente"""
    queda('P2', (300.5, 140, -1478), (0, 65, 0), 'planador', 1.38, v3=(0, -7, 16), ombro=((FCX, Y + 10, FCZ), 3.4, 0.9),
          rosto={'fechar': 0.0, 'brava': 0.8})


def p_P3():
    """'como um planador': de baixo, silhueta de planador"""
    queda('P3', (300.5, 130, -1456), (0, 65, 0), 'planador', 1.02, v3=(0, -7, 16), rel=(1.5, -3.4, 1.0), subir=0,
          rosto={'fechar': 0.0, 'brava': 0.8})


def p_Q1():
    """'funciona, mas devagar': de frente, determinada"""
    queda('Q1', (300.5, 122, -1430), (0, 65, 0), 'planador', 1.2, v3=(0, -6, 18), rel=(0, 0.6, 3.0), mira='rosto',
          rosto={'fechar': 0.3, 'brava': 1.0, 'boca_ab': 0.0})


def p_Q2():
    """'voce ve a floresta chegando mais perto': de tras, a floresta crescendo"""
    queda('Q2', (300.5, 112, -1360), (0, 65, 0), 'planador', 1.88, v3=(0, -6, 24), ombro=((FCX, Y + 10, FCZ), 3.2, 0.8),
          rosto={'fechar': 0.0})


AX, AZ = SET['arvore']


def p_R1():
    """'agora o chao esta vindo rapido': de cima, o chao da floresta se aproximando"""
    queda('R1', (AX + 2, 130, AZ - 8), (0, 90, 0), 'planador', 1.36, v3=(0, -16, 0), rel=(0.3, 3.4, -0.8), subir=0,
          rosto={'fechar': 0.0, 'boca_ab': 1.0})


def p_R2():
    """'voce poe os pes pra frente' (lateral)"""
    a = [(0.6, {'pose': 'pouso', 'ori': (0, 0, 0)})]
    queda('R2', (AX + 2, 110, AZ - 8), (0, 40, 0), 'planador', 1.56, v3=(0, -10, 0), rel=(-3.8, 0.3, 0.3), acoes=a,
          rosto={'fechar': 0.0, 'boca_ab': 0.6})


def p_R3():
    """'dobra os joelhos'"""
    a = [(0.1, {'pose': 'joelhos'})]
    queda('R3', (AX + 2, 96, AZ - 8), (0, 0, 0), 'pouso', 0.9, v3=(0, -10, 0), rel=(-3.0, -0.6, 2.4), acoes=a,
          rosto={'fechar': 0.0, 'boca_ab': 0.6}, agitar=3)


def p_R4():
    """'e abraca a cabeca com os bracos'"""
    a = [(0.1, {'pose': 'encolhido', 'fechar': 1.0, 'boca_ab': 1.0})]
    queda('R4', (AX + 2, 92, AZ - 8), (0, 10, 0), 'joelhos', 1.46, v3=(0, -8, 0), rel=(2.4, -0.5, 2.8), acoes=a,
          rosto={'fechar': 0.3, 'boca_ab': 0.6}, agitar=2)


def preparar_pouso_v5():
    """neve funda natural (montinho de camadas, sem caixa/buraco) sobre a clareira restaurada"""
    import cenarios as K
    x, z, g = int(T2.PX), int(T2.PZ), T2.G
    C(f'forceload add {x - 16} {z - 16} {x + 16} {z + 16}'); time.sleep(1.5)
    K.restaurar('pouso_v2')
    # chao de neve uniforme (sem caixa nem buraco de takes antigos), sem tocar nos troncos
    for a in ('air', 'snow', 'snow_block', 'powder_snow'):
        C(f'fill {x - 6} {g + 1} {z - 6} {x + 6} {g + 3} {z + 6} air replace {a}')
        C(f'fill {x - 6} {g - 2} {z - 6} {x + 6} {g} {z + 6} snow_block replace {a}')
    C(f'fill {x - 6} {g + 1} {z - 6} {x + 6} {g + 1} {z + 6} snow[layers=3] replace air')
    C('kill @e[type=item]')
    C(f'forceload remove {x - 16} {z - 16} {x + 16} {z + 16}')


ST_CR = {'feita': False}


def cratera():
    """afundamento suave na neve (sem paredes retas): centro rebaixado, borda com neve empilhada"""
    x, z, g = int(T2.PX), int(T2.PZ), T2.G
    for dx in range(-3, 4):
        for dz in range(-3, 4):
            d = math.hypot(dx, dz) + 0.3 * math.sin(dx * 2.1 + dz * 1.3)
            X, Z = x + dx, z + dz
            if d <= 1.25:
                C(f'fill {X} {g + 1} {Z} {X} {g + 2} {Z} air')
                C(f'setblock {X} {g} {Z} snow[layers=2]')
            elif d <= 2.1:
                C(f'fill {X} {g + 1} {Z} {X} {g + 1} {Z} snow[layers=1] replace snow')
            elif d <= 3.0:
                C(f'fill {X} {g + 1} {Z} {X} {g + 1} {Z} snow[layers=5] replace snow')


def _c_pouso(cmd):
    """intercepta os buracos quadrados dos takes antigos e troca pela cratera irregular"""
    x, z, g = int(T2.PX), int(T2.PZ), T2.G
    if cmd.startswith(f'fill {x - 1} ') and f' {z - 1} {x + 1} ' in cmd:
        if 'air replace' in cmd and not ST_CR['feita']:
            ST_CR['feita'] = True; cratera()
        return {'success': True}
    return C(cmd)


def p_S1():
    preparar_pouso_v5()
    T3.t15()


def p_T1():
    ST_CR['feita'] = False
    T3.C = _c_pouso
    velho = T2.preparar_pouso
    T2.preparar_pouso = lambda: None        # sem a caixa de neve antiga
    try:
        T3.t16()
    finally:
        T3.C = C; T2.preparar_pouso = velho


def p_T2():
    T3.C = _c_pouso
    try:
        T3.t17()
    finally:
        T3.C = C


def p_U1():
    T3.t18()


# roteiro de cortes (tempos de saida = tempos das palavras da narracao)
ORDEM = [
    ('A1', 0.00, 0.88, None), ('A2', 0.88, 1.36, None), ('A3', 1.36, 2.06, 'sobe'),
    ('B1', 2.06, 3.24, 'sobe'), ('B2', 3.24, 4.07, 'sobe'),
    ('C1', 4.07, 5.06, 'sobe'), ('C2', 5.06, 6.74, 'sobe'), ('C3', 6.74, 7.60, 'sobe'), ('C4', 7.60, 8.48, 'sobe'),
    ('D1', 8.48, 9.81, 'sobe'), ('D2', 9.81, 10.84, 'sobe'),
    ('E1', 10.84, 12.56, 'sobe'), ('E2', 12.56, 13.36, 'radial'), ('E3', 13.36, 14.16, 'radial'),
    ('F1', 14.16, 15.52, 'sobe'), ('F2', 15.52, 16.30, 'radial'), ('F3', 16.30, 17.62, 'sobe'),
    ('G1', 17.62, 19.52, 'sobe'), ('G2', 19.52, 21.14, 'sobe'),
    ('H1', 21.14, 22.36, 'sobe'), ('H2', 22.36, 24.50, 'sobe'), ('H3', 24.50, 26.10, 'sobe'),
    ('I1', 26.10, 27.05, 'sobe'), ('I2', 27.05, 28.06, 'radial'),
    ('J1', 28.06, 29.14, 'radial'), ('J2', 29.14, 30.22, 'sobe'), ('J3', 30.22, 31.86, None),
    ('K1', 31.86, 32.76, 'radial'), ('K2', 32.76, 33.65, None), ('L1', 33.65, 35.18, 'radial'),
    ('M1', 35.18, 36.18, 'sobe'), ('M2', 36.18, 37.38, None),
    ('N1', 37.38, 40.50, None), ('O1', 40.50, 42.52, None),
    ('P1', 42.52, 43.86, 'sobe'), ('P2', 43.86, 45.24, None), ('P3', 45.24, 46.26, None),
    ('Q1', 46.26, 47.46, 'sobe'), ('Q2', 47.46, 49.34, None),
    ('R1', 49.34, 50.70, 'radial'), ('R2', 50.70, 52.26, 'sobe'), ('R3', 52.26, 53.16, 'sobe'), ('R4', 53.16, 54.62, 'sobe'),
    ('S1', 54.62, 57.56, None), ('T1', 57.56, 59.97, None), ('T2', 59.97, 61.05, None), ('U1', 61.05, 64.60, None),
]
TAKE_DE = {'A1': 't01a', 'B1': 't01b', 'G2': 't06', 'N1': 't11b', 'O1': 't12a', 'S1': 't15', 'T1': 't16', 'T2': 't17', 'U1': 't18'}


def salvar_planos():
    S0 = {}   # alinha o evento 'concreto' (o laco atrasou ~1 s nesse take) com a palavra
    pl = [dict(nome=n, t0=a, t1=b, take=TAKE_DE.get(n, n), s0=S0.get(n, 0.0), linhas=l) for n, a, b, l in ORDEM]
    json.dump(pl, open(RAIZ + r'\roteiro\planos_v5.json', 'w'), indent=1)


# ---------------- nuvens densas na coluna de queda (com um tubo vazio para a camera) ----------------
def nuvens(colunas=None):
    rnd = random.Random(17)
    for (cx, cz, yb) in (colunas or [(int(COL[0]), int(COL[1]), Y1), (int(COL[0]), int(COL[1]), Y2)]):
        caixas = []
        for _ in range(55):
            a = rnd.uniform(0, 2 * math.pi); d = 70 * math.sqrt(rnd.random())
            x, z = int(cx + d * math.cos(a)), int(cz + d * math.sin(a))
            w, l = rnd.randint(7, 18), rnd.randint(7, 18)
            y = yb + rnd.randint(-2, 2)
            caixas.append((x - w // 2, y, z - l // 2, x + w // 2, y + rnd.randint(2, 4), z + l // 2))
            for _k in range(rnd.randint(2, 5)):
                ox, oz = rnd.randint(-w // 2, w // 2), rnd.randint(-l // 2, l // 2)
                ww, ll = rnd.randint(4, 9), rnd.randint(4, 9)
                caixas.append((x + ox - ww // 2, y, z + oz - ll // 2, x + ox + ww // 2, y + rnd.randint(3, 6), z + oz + ll // 2))
        carregar(cx - 90, cz - 90, cx + 90, cz + 90)
        for (a1, b1, c1, d1, e1, f1) in caixas:
            C(f'fill {a1} {b1} {c1} {d1} {e1} {f1} white_concrete keep')
        # tubo vazio (raio 6) para a camera atravessar a camada
        for x in range(cx - 7, cx + 8):
            for z in range(cz - 7, cz + 8):
                if math.hypot(x - cx, z - cz) <= 6.2:
                    C(f'fill {x} {yb - 3} {z} {x} {yb + 8} {z} air')
        descarregar(cx - 90, cz - 90, cx + 90, cz + 90)
    print('nuvens ok')


if __name__ == '__main__':
    salvar_planos()
    args = sys.argv[1:]
    if args == ['nuvens']:
        nuvens(); sys.exit()
    if args == ['nuvens2']:
        nuvens([(int(CX) + 130, int(CZ) + 8, 186), (int(CX) + 130, int(CZ) - 4, 141)]); sys.exit()
    if args == ['planos']:
        sys.exit()
    nomes = [n for n, *_ in ORDEM] if args == ['todos'] else args
    E.sessao_inicio(os.environ.get('SESSAO', 'sessao_v5'))
    try:
        for n in nomes:
            print('==', n, flush=True)
            try:
                globals()['p_' + n]()
            except Exception as e:
                import traceback; traceback.print_exc()
                print('ERRO no plano', n, e, flush=True)
                T0.fim()
    finally:
        E.sessao_fim()
