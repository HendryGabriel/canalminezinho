import os as _os
PROJ = _os.environ.get('ANIM_PROJETO', _os.getcwd())
"""Moldura do cenario: costa natural (ilha) + serra verde/rochosa atras da floresta (esconde o fim do mapa).
uso: python moldura.py costa serra arvores_serra   (retomavel: checkpoints/moldura_feito.txt)"""
import sys, os, math, random
from motor import C
from set_queda import SET, Y, tile_iter, carregar, descarregar

X0, Z0, X1, Z1 = SET['canvas']           # 20, -1730, 580, -1110  (sul = +z)
MAR = 62                                  # superficie da agua
BASE = 54                                 # fundacao (debaixo d'agua)
PROG = _os.path.join(PROJ, 'checkpoints', 'moldura_feito.txt')
FEITO = set(open(PROG).read().split()) if os.path.exists(PROG) else set()


def marcar(k):
    open(PROG, 'a').write(k + '\n'); FEITO.add(k)


def onda(seed, termos):
    r = random.Random(seed)
    w = [(a, 2 * math.pi / l, r.uniform(0, 6.3), r.uniform(0, 6.3)) for a, l in termos]
    return lambda x, z: sum(a * math.sin(k * x + p) * math.cos(k * 0.7 * z + q) for a, k, p, q in w)


LARG = onda(3, [(14, 170), (8, 70), (4, 31)])      # largura extra da costa


def _linha(x, z, dx, dz):
    w = int(max(8, 22 + LARG(x, z)))                  # 8..48 blocos para fora
    xa, za = x + dx * (w - 6), z + dz * (w - 6)
    xs, zs = sorted((x, xa)), sorted((z, za))
    C(f'fill {xs[0]} {BASE} {zs[0]} {xs[1]} {Y - 1} {zs[1]} dirt')
    C(f'fill {xs[0]} {Y} {zs[0]} {xs[1]} {Y} {zs[1]} grass_block')
    for i, yy in enumerate([Y - 1, MAR, MAR - 1, MAR - 2, MAR - 3]):   # praia descendo ate a agua
        px, pz = x + dx * (w - 5 + i), z + dz * (w - 5 + i)
        C(f'fill {px} {BASE} {pz} {px} {yy} {pz} sand')
    C(f'fill {x - dx * 3} {Y} {z - dz * 3} {x} {Y} {z} grass_block replace sand')


def costa():
    lados = [('o', [(X0 - 1, z) for z in range(Z0 - 2, Z1 + 1)], -1, 0),
             ('l', [(X1 + 1, z) for z in range(Z0 - 2, Z1 + 1)], 1, 0),
             ('n', [(x, Z0 - 1) for x in range(X0 - 2, X1 + 3)], 0, -1)]
    for nome, pts, dx, dz in lados:
        for i in range(0, len(pts), 48):
            k = f'c{nome}{i}'
            if k in FEITO: continue
            grupo = pts[i:i + 48]
            xs = [p[0] for p in grupo] + [p[0] + dx * 50 for p in grupo]
            zs = [p[1] for p in grupo] + [p[1] + dz * 50 for p in grupo]
            carregar(min(xs) - 4, min(zs) - 4, max(xs) + 4, max(zs) + 4)
            for (x, z) in grupo:
                _linha(x, z, dx, dz)
            descarregar(min(xs) - 4, min(zs) - 4, max(xs) + 4, max(zs) + 4)
            marcar(k)
            print('costa', nome, i, flush=True)
    C('kill @e[type=item]')


RIDGE = onda(9, [(1.0, 150), (0.6, 64), (0.3, 27)])
COL = onda(5, [(1.0, 220), (0.5, 90)])


def h_serra(x, z):
    """altura (acima de Y) da serra ao sul do canvas"""
    zz = z - Z1
    sobe = min(1.0, max(0.0, (zz + 10) / 80))
    desce = min(1.0, max(0.0, (300 - zz) / 70))
    s = sobe * sobe * (3 - 2 * sobe) * desce
    r = 1 - abs(RIDGE(x, z) / 1.9)
    h = s * (38 + 42 * r * r + 10 * COL(x, z))
    ext = min(1.0, max(0.0, (x - (X0 - 70)) / 60), max(0.0, ((X1 + 70) - x) / 60))
    return h * ext


def serra():
    xa, xb, za, zb = X0 - 70, X1 + 70, Z1 - 10, Z1 + 300
    for a, b, c, d in tile_iter(xa, za, xb, zb, 64):
        k = f's{a},{b}'
        if k in FEITO: continue
        carregar(a, b, c, d)
        passo = 2 if b - Z1 < 120 else 4
        for x in range(a, c + 1, passo):
            for z in range(b, d + 1, passo):
                h = int(round(h_serra(x + passo / 2, z + passo / 2)))
                if h < 1:
                    continue
                x2, z2 = min(c, x + passo - 1), min(d, z + passo - 1)
                top = Y + h
                C(f'fill {x} {BASE} {z} {x2} {top - 1} {z2} stone')
                if h < 44:
                    C(f'fill {x} {top} {z} {x2} {top} {z2} grass_block')
        descarregar(a, b, c, d)
        marcar(k)
        print('serra', a, b, flush=True)
    C('kill @e[type=item]')


def arvores_serra(n=260, seed=8):
    rnd = random.Random(seed)
    if 'arvores_serra' in FEITO: return
    feitas = 0
    for _ in range(n * 6):
        x, z = rnd.randint(X0 - 60, X1 + 60), rnd.randint(Z1 + 10, Z1 + 250)
        h = h_serra(x, z)
        if not (6 < h < 36): continue
        carregar(x - 3, z - 3, x + 3, z + 3)
        C(f'place feature minecraft:{rnd.choice(["oak", "birch", "oak", "dark_oak"])} {x} {Y + int(round(h)) + 1} {z}')
        descarregar(x - 3, z - 3, x + 3, z + 3)
        feitas += 1
        if feitas >= n: break
    marcar('arvores_serra')
    print('arvores serra', feitas)




MANCHA = onda(13, [(1.0, 60), (0.5, 23)])


def verdejar():
    """topo da serra verde (pedra so nos picos e em manchas), para nao parecer um muro cinza"""
    xa, xb, za, zb = X0 - 70, X1 + 70, Z1 - 10, Z1 + 300
    for a, b, c, d in tile_iter(xa, za, xb, zb, 64):
        k = f'v{a},{b}'
        if k in FEITO: continue
        carregar(a, b, c, d)
        passo = 2 if b - Z1 < 120 else 4
        for x in range(a, c + 1, passo):
            for z in range(b, d + 1, passo):
                h = int(round(h_serra(x + passo / 2, z + passo / 2)))
                if h < 44: continue
                m = MANCHA(x, z)
                top = Y + h
                x2, z2 = min(c, x + passo - 1), min(d, z + passo - 1)
                if h > 84 or m > 0.9:
                    continue
                b2 = 'moss_block' if m < -0.9 else ('coarse_dirt' if m > 0.6 else 'grass_block')
                C(f'fill {x} {top} {z} {x2} {top} {z2} {b2}')
                C(f'fill {x} {top - 2} {z} {x2} {top - 1} {z2} dirt')
        descarregar(a, b, c, d)
        marcar(k)
    print('verdejado', flush=True)


def arvores_serra2(n=500, seed=21):
    rnd = random.Random(seed)
    if 'arvores_serra2' in FEITO: return
    feitas = 0
    for _ in range(n * 6):
        x, z = rnd.randint(X0 - 60, X1 + 60), rnd.randint(Z1 + 10, Z1 + 260)
        h = h_serra(x, z)
        if not (6 < h < 80) or MANCHA(x, z) > 0.9: continue
        carregar(x - 3, z - 3, x + 3, z + 3)
        C(f'place feature minecraft:{rnd.choice(["oak", "birch", "spruce", "oak", "dark_oak", "pine"])} {x} {Y + int(round(h)) + 1} {z}')
        descarregar(x - 3, z - 3, x + 3, z + 3)
        feitas += 1
        if feitas >= n: break
    marcar('arvores_serra2')
    print('arvores serra2', feitas)


if __name__ == '__main__':
    for e in sys.argv[1:]:
        print('==', e, flush=True)
        globals()[e]()
