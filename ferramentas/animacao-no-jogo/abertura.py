import os as _os
PROJ = _os.environ.get('ANIM_PROJETO', _os.getcwd())
"""Abertura nova (estilo do original): A = Steve correndo pelo corredor do aviao ate a porta aberta e pulando;
B = do lado de fora, caindo junto com o Steve, o aviao explode logo acima. uso: python abertura.py montar | t01a t01b"""
import sys, os, time, math, random
import motor as M
import takes as T0
import takes3 as T3
import estudio as E
import mc
from motor import C, PL, snd, snd_cam
from takes3 import Vel, cam_trajeto, rodar, limpar_tudo, esperar_chunks, mirar, cam

M.POSES_STEVE['corre1'] = {'braco_e': (70, 0, 0), 'braco_d': (-70, 0, 0), 'perna_e': (-60, 0, 0), 'perna_d': (55, 0, 0), 'cabeca': (-8, 0, 0)}
M.POSES_STEVE['corre2'] = {'braco_e': (-70, 0, 0), 'braco_d': (70, 0, 0), 'perna_e': (55, 0, 0), 'perna_d': (-60, 0, 0), 'cabeca': (-8, 0, 0)}
M.POSES_STEVE['salto'] = {'braco_e': (150, 0, 40), 'braco_d': (150, 0, -40), 'perna_e': (-40, 0, 10), 'perna_d': (30, 0, -10), 'cabeca': (-25, 0, 0)}

# aviao grande: frente em -x, porta traseira aberta em +x (rampa de carga)
X0, X1, Y0, CZ = 270, 312, 300, -1640     # Y0 = altura do piso (topo do bloco do piso = Y0)
INT = 2                                     # meia largura interna (z de CZ-2 a CZ+2)
ALT = 4                                     # altura interna (Y0+1 .. Y0+4)


def blocos():
    B = []
    for x in range(X0, X1 + 1):
        for z in range(CZ - INT - 1, CZ + INT + 2):
            B.append((x, Y0, z, 'light_gray_concrete'))                         # piso
            B.append((x, Y0 + ALT + 1, z, 'white_concrete'))                    # teto
        for y in range(Y0 + 1, Y0 + ALT + 1):
            for z in (CZ - INT - 1, CZ + INT + 1):
                jan = (y in (Y0 + 2, Y0 + 3)) and x % 3 == 0 and X0 + 2 < x < X1 - 1
                B.append((x, y, z, 'light_blue_stained_glass' if jan else 'white_concrete'))
    for z in range(CZ - INT - 1, CZ + INT + 2):                                  # nariz fechado
        for y in range(Y0, Y0 + ALT + 2):
            B.append((X0 - 1, y, z, 'white_concrete'))
    for x in range(X0 + 12, X0 + 22):                                            # asas
        for dz in range(4, 16):
            if x - (X0 + 12) > 9 - dz // 2: continue
            B.append((x, Y0 + 1, CZ - dz, 'white_concrete' if dz < 14 else 'red_concrete'))
            B.append((x, Y0 + 1, CZ + dz, 'white_concrete' if dz < 14 else 'red_concrete'))
    for x in range(X1 - 5, X1 + 1):                                              # cauda
        for dy in range(ALT + 2, ALT + 2 + (x - (X1 - 6))):
            B.append((x, Y0 + dy, CZ, 'red_concrete'))
    return B


def montar():
    C(f'tp {PL} {X0 + 20} {Y0 + 3} {CZ}')
    time.sleep(1.5)
    C(f'fill {X0 - 2} {Y0 - 1} {CZ - 17} {X1 + 2} {Y0 + 13} {CZ + 17} air')
    for (x, y, z, b) in blocos():
        C(f'setblock {x} {y} {z} {b}')
    for x in range(X0, X1 + 1):
        C(f'setblock {x} {Y0 + 1} {CZ} blue_carpet')                          # corredor
        if x % 2 == 0 and x < X1 - 3:
            for z in (CZ - 2, CZ - 1, CZ + 1, CZ + 2):
                C(f'setblock {x} {Y0 + 1} {z} dark_oak_stairs[facing=east]')  # poltronas
        if x % 4 == 0:
            C(f'setblock {x} {Y0 + ALT + 1} {CZ} redstone_lamp[lit=true]')   # luz de emergencia
            C(f'setblock {x} {Y0 + ALT} {CZ - 2} red_stained_glass')
            C(f'setblock {x} {Y0 + ALT} {CZ + 2} red_stained_glass')
    for z in range(CZ - INT, CZ + INT + 1):                                     # porta: traseira aberta
        for y in range(Y0 + 1, Y0 + ALT + 1):
            C(f'setblock {X1} {y} {z} air')
    C('kill @e[type=item]')


def fumaca(n=6):
    for _ in range(n):
        x = random.uniform(X0 + 4, X1 - 4)
        C(f'particle campfire_cosy_smoke {x:.1f} {Y0 + ALT - 0.5:.1f} {CZ + random.uniform(-1.5, 1.5):.1f} 0.6 0.2 0.6 0.01 3 force')
        C(f'particle flame {x:.1f} {Y0 + 2:.1f} {CZ + random.choice([-2.2, 2.2]):.1f} 0.2 0.3 0.1 0.01 6 force')


def t01a():
    """Steve correndo pelo corredor ate a porta aberta e pulando (camera atras, mesma velocidade)"""
    limpar_tudo()
    V = 8.0
    eye = (X1 - 19.5, Y0 + 3.9, CZ + 0.5)
    off = (3.4, -1.08, 0.0)          # capivara a frente da camera, pes no piso
    ori = (-90, 8, 0)                # olhando para +x (porta)
    yaw = -90.0; pitch = 27.0
    cam.criar(*eye, yaw, pitch)
    p = M.Steve()
    p.criar(*eye, ori=ori, pose='corre1', off=off)
    p.montar()
    esperar_chunks(2)
    D = 2.0 + T3.SOBRA
    tc = Vel(f'@e[tag={M.CAM}]', (V, 0, 0), 'cam')
    st = {'k': 0, 'salto': False}

    def acao(ev):
        ev('inicio_acao')
        snd_cam('entity.generic.explode', 0.5, 1.6)
        snd_cam('block.fire.ambient', 1.0, 1.0)

        def ex(t):
            k = int(t * 20)
            if k % 6 == 0 and k != st['k']:
                fumaca(3)
            if not st['salto'] and t < 1.75 and k % 4 == 0 and k != st['k']:
                p.posar(pose='corre1' if (k // 4) % 2 == 0 else 'corre2', dur=4)
                snd_cam('block.metal.step', 0.6, 1.2)
            if not st['salto'] and t >= 1.75:
                st['salto'] = True; ev('salto')
                p.posar(pose='salto', ori=(-90, 35, 0), dur=6)
                snd_cam('entity.player.attack.sweep', 0.8, 0.8)
            st['k'] = k
        rodar(D, tc, extra=ex)
    E.gravar('t01a', acao, D + 0.2)
    T0.fim()


def explodir():
    for i, xx in enumerate((X1 - 4, X1 - 16, X0 + 8)):
        M.bola_fogo(xx, Y0 + 2, CZ, r=7 - i, tag=f'fogo{i}', dur=16)
    time.sleep(0.15)                      # o fogo cobre o aviao antes de ele sumir
    C(f'fill {X0 - 2} {Y0 - 1} {CZ - 17} {X1 + 2} {Y0 + 13} {CZ + 17} air')
    snd('entity.generic.explode', X1 - 8, Y0 + 2, CZ, 4, 0.7)
    snd('entity.generic.explode', X0 + 10, Y0 + 2, CZ, 4, 0.9)
    B = blocos(); random.shuffle(B)
    cx = (X0 + X1) / 2
    for (x, y, z, b) in B[:90]:
        dx, dy, dz = x - cx, y - Y0, z - CZ
        n = math.sqrt(dx * dx + dy * dy + dz * dz) + 0.5
        v = random.uniform(0.25, 0.7); s = random.uniform(0.5, 1.3)
        m = M.R(random.uniform(0, 360), random.uniform(-80, 80), random.uniform(-80, 80)) @ M.T(-s / 2, -s / 2, -s / 2) @ M.S(s, s, s)
        C('summon armor_stand %.2f %.2f %.2f {Tags:["deb","deb_c"],Invisible:1b,Small:1b,Silent:1b,Invulnerable:1b,'
          'Motion:[%.3f,%.3f,%.3f],Passengers:[{id:"minecraft:block_display",Tags:["deb","deb_d","deb_g%d"],'
          'block_state:"minecraft:%s",transformation:%s}]}'
          % (x + 0.5, y, z + 0.5, dx / n * v, dy / n * v + 0.3, dz / n * v, random.randint(0, 3), b, M.mat_nbt(m)))
    import threading
    threading.Thread(target=M._girar, args=('deb', 6, 0.4), daemon=True).start()


def t01b():
    """do lado de fora: caindo junto com o Steve (de frente), o aviao explode logo acima/atras"""
    limpar_tudo()
    montar()
    eye = (X1 - 12, Y0 + 2.5, CZ + 24)
    yaw, pitch = 180.0, -4.0         # olhando para -z: o aviao de lado
    off = (0.0, 0.05, -3.6)
    ori = (0, -20, 0)                # Steve de frente para a camera (+z)
    cam.criar(*eye, yaw, pitch)
    p = M.Steve(); p.fechar = 0.0; p.boca_ab = 1.0; p.brava = 0.6
    # solta (nao montada): cai mais rapido que a camera e atravessa o quadro girando
    P0 = (eye[0], eye[1] - M.EYE + 1.02 + 2.2, eye[2] - 3.6)
    p.criar(*P0, ori=ori, pose='estrela', tdur=4)
    esperar_chunks(3)
    D = 2.1 + T3.SOBRA
    tc = Vel(f'@e[tag={M.CAM}]', (0, -6.0, 1.0), 'cam')
    tp = T3.Trajeto('@e[tag=steve]', lambda t: (P0[0], P0[1] - 6.0 * t - 2.6 * t * t, P0[2] + 1.0 * t), passo=0.2)
    st = {'b': False, 'o': [0, -20, 0]}

    def acao(ev):
        ev('inicio_acao')
        snd_cam('item.elytra.flying', 0.9, 1.0)

        def ex(t):
            k = int(t * 20)
            if not st['b'] and t >= 0.1:
                st['b'] = True; ev('explode')
                import threading; threading.Thread(target=explodir, daemon=True).start()   # nao bloqueia o laco do movimento
            if k % 4 == 0:
                st['o'][2] += 22; st['o'][1] += 15
                p.posar(pose='estrela2' if (k // 8) % 2 else 'estrela', ori=tuple(st['o']), dur=5)
        rodar(D, tc, tp, extra=ex)
    E.gravar('t01b', acao, D + 0.2)
    T0.fim()


if __name__ == '__main__':
    if sys.argv[1:] == ['montar']:
        montar(); sys.exit()
    E.sessao_inicio(os.environ.get('SESSAO', 'sessao_ab'))
    try:
        for n in sys.argv[1:]:
            print('==', n, flush=True)
            if n == 't01a': montar()
            globals()[n]()
    finally:
        E.sessao_fim()
