import os as _os
PROJ = _os.environ.get('ANIM_PROJETO', _os.getcwd())
"""Cenario do short 'Queda' construido sobre o oceano (tela em branco plana e sem floresta em volta).
Tudo sai de SET: os takes leem as mesmas coordenadas. uso: python set_queda.py <etapa> [...]
etapas: base vila lago campo floresta rodovia nuvens limpar_arvores maquete"""
import sys, os, math, random, time, json
import mc
from motor import C, PL

Y = 64  # topo da grama
SET = {
    'canvas': (20, -1730, 580, -1110),
    'lago': (300, -1565, 22),               # cx, cz, raio  (Steve cai sobre ele)
    'vila': (300, -1490),                    # centro do place structure
    'campo': (240, -1435, 360, -1340),       # x0,z0,x1,z1 terra dura (grande, colado na vila)
    'floresta': (300, -1225, 62, 44),        # cx, cz, raio x, raio z (unica neve do mapa)
    'arvore': (300, -1225),                  # arvore-alvo do pouso (centro da floresta)
    'rodovia': (470, -1700, -1140),          # x, z0, z1
    'nuvens': (95, -1420, 75),               # cx, cz, raio (oeste, fora do quadro do mapa)
}


def tile_iter(x0, z0, x1, z1, t=64):
    for x in range(x0, x1 + 1, t):
        for z in range(z0, z1 + 1, t):
            yield x, z, min(x + t - 1, x1), min(z + t - 1, z1)


def carregar(x0, z0, x1, z1):
    C(f'forceload add {x0} {z0} {x1} {z1}')
    time.sleep(0.4)


def descarregar(x0, z0, x1, z1):
    C(f'forceload remove {x0} {z0} {x1} {z1}')


def base():
    x0, z0, x1, z1 = SET['canvas']
    C(f'gamemode spectator {PL}')
    for a, b, c, d in tile_iter(x0, z0, x1, z1, 128):
        C(f'tp {PL} {(a + c) // 2} 200 {(b + d) // 2}')
        carregar(a, b, c, d)
        for tx0, tz0, tx1, tz1 in tile_iter(a, b, c, d, 64):
            for y in range(Y + 1, 140, 8):
                C(f'fill {tx0} {y} {tz0} {tx1} {min(y + 7, 139)} {tz1} air')
            C(f'fill {tx0} {Y - 5} {tz0} {tx1} {Y - 1} {tz1} dirt')
            C(f'fill {tx0} {Y} {tz0} {tx1} {Y} {tz1} grass_block')
        descarregar(a, b, c, d)
        print('tile', a, b, flush=True)
    # praia em volta
    for (a, b, c, d) in [(x0 - 3, z0 - 3, x1 + 3, z0 - 1), (x0 - 3, z1 + 1, x1 + 3, z1 + 3), (x0 - 3, z0, x0 - 1, z1), (x1 + 1, z0, x1 + 3, z1)]:
        for tx0, tz0, tx1, tz1 in tile_iter(a, b, c, d, 64):
            carregar(tx0, tz0, tx1, tz1)
            C(f'fill {tx0} {Y - 5} {tz0} {tx1} {Y - 1} {tz1} sand')
            C(f'fill {tx0} {Y - 2} {tz0} {tx1} {Y - 2} {tz1} sand')
            descarregar(tx0, tz0, tx1, tz1)
    C('kill @e[type=item]'); C('kill @e[type=#minecraft:aquatic]')


def vila():
    x, z = SET['vila']
    C(f'tp {PL} {x} 150 {z}')
    carregar(x - 96, z - 96, x + 96, z + 96)
    r = C(f'place structure minecraft:village_plains {x} {Y + 1} {z}')
    print(r.get('output'))
    descarregar(x - 96, z - 96, x + 96, z + 96)


def lago():
    cx, cz, r = SET['lago']
    carregar(cx - r - 4, cz - r - 4, cx + r + 4, cz + r + 4)
    for x in range(cx - r - 3, cx + r + 4):
        for z in range(cz - r - 3, cz + r + 4):
            d = math.hypot(x - cx, (z - cz) * 1.15) + 1.1 * math.sin(math.atan2(z - cz, x - cx) * 3 + 0.7)
            if d <= r:
                prof = max(1, int(round(5 * (1 - (d / r) ** 2))))
                C(f'fill {x} {Y - prof} {z} {x} {Y + 6} {z} air')
                C(f'fill {x} {Y - prof} {z} {x} {Y} {z} water')
                C(f'setblock {x} {Y - prof - 1} {z} {"sand" if d > r - 2 else "clay"}')
            elif d <= r + 1.6:
                C(f'setblock {x} {Y} {z} sand'); C(f'setblock {x} {Y + 1} {z} air')
    descarregar(cx - r - 4, cz - r - 4, cx + r + 4, cz + r + 4)


def campo():
    x0, z0, x1, z1 = SET['campo']
    random.seed(11)
    carregar(x0, z0, x1, z1)
    for tx0, tz0, tx1, tz1 in tile_iter(x0, z0, x1, z1, 32):
        C(f'fill {tx0} {Y + 1} {tz0} {tx1} {Y + 8} {tz1} air')
        C(f'fill {tx0} {Y} {tz0} {tx1} {Y} {tz1} coarse_dirt')
    # manchas e rachaduras (terra seca)
    for _ in range(260):
        x, z = random.randint(x0, x1), random.randint(z0, z1)
        w = random.randint(1, 5)
        b = random.choice(['dirt', 'packed_mud', 'dirt', 'rooted_dirt', 'gravel'])
        C(f'fill {x} {Y} {z} {min(x1, x + w)} {Y} {min(z1, z + random.randint(0, 2))} {b}')
    for _ in range(40):  # rachaduras lineares
        x, z = random.randint(x0, x1), random.randint(z0, z1)
        for k in range(random.randint(4, 10)):
            x += random.choice([-1, 0, 1]); z += random.choice([0, 1])
            if x0 <= x <= x1 and z0 <= z <= z1:
                C(f'setblock {x} {Y} {z} brown_terracotta')
    # borda irregular (sem quadrado perfeito)
    for _ in range(120):
        lado = random.randint(0, 3)
        if lado == 0: x, z = random.randint(x0, x1), z0 + random.randint(-3, 2)
        elif lado == 1: x, z = random.randint(x0, x1), z1 + random.randint(-2, 3)
        elif lado == 2: x, z = x0 + random.randint(-3, 2), random.randint(z0, z1)
        else: x, z = x1 + random.randint(-2, 3), random.randint(z0, z1)
        C(f'fill {x} {Y} {z} {x + random.randint(0, 2)} {Y} {z + random.randint(0, 2)} {random.choice(["coarse_dirt", "grass_block"])}')
    descarregar(x0, z0, x1, z1)
    C('kill @e[type=item]')


def floresta():
    cx, cz, rx, rz = SET['floresta']
    random.seed(5)
    x0, z0, x1, z1 = cx - rx - 4, cz - rz - 4, cx + rx + 4, cz + rz + 4
    carregar(x0, z0, x1, z1)
    dentro = lambda x, z, m=0: ((x - cx) / (rx + m)) ** 2 + ((z - cz) / (rz + m)) ** 2 <= 1 + 0.08 * math.sin(math.atan2(z - cz, x - cx) * 5)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if dentro(x, z):
                C(f'setblock {x} {Y} {z} snow_block')
                C(f'setblock {x} {Y + 1} {z} snow[layers=3]')
            elif dentro(x, z, 3) and random.random() < 0.5:
                C(f'setblock {x} {Y + 1} {z} snow[layers=1]')
    ax, az = SET['arvore']
    pts = [(ax, az)]
    for _ in range(4000):
        x, z = random.randint(x0, x1), random.randint(z0, z1)
        if not dentro(x, z, -3): continue
        if math.hypot(x - ax, z - az) < 9 and (x, z) != (ax, az): continue   # clareira em volta da arvore-alvo
        if all(math.hypot(x - a, z - b) >= 5 for a, b in pts):
            pts.append((x, z))
    for (x, z) in pts:
        C(f'setblock {x} {Y} {z} dirt'); C(f'setblock {x} {Y + 1} {z} air')
        C(f'place feature minecraft:{"mega_spruce" if random.random() < 0.12 and (x, z) != (ax, az) else "spruce"} {x} {Y + 1} {z}')
        C(f'fill {x} {Y} {z} {x} {Y} {z} snow_block replace dirt')
    # neve sobre as folhas
    for tx0, tz0, tx1, tz1 in tile_iter(x0, z0, x1, z1, 16):
        r = mc.call('world.getBlocks', {'from': {'x': tx0, 'y': Y + 2, 'z': tz0}, 'to': {'x': tx1, 'y': Y + 40, 'z': tz1}})
        S = {(b['x'], b['y'], b['z']): b['id'] for b in r['blocks']}
        for (x, y, z), b in S.items():
            if 'leaves' in b and (x, y + 1, z) not in S:
                C(f'setblock {x} {y + 1} {z} snow[layers={2 if random.random() < 0.6 else 1}]')
    descarregar(x0, z0, x1, z1)
    print('arvores', len(pts))


def rodovia():
    x, z0, z1 = SET['rodovia']
    carregar(x - 8, z0, x + 8, z1)
    C(f'fill {x - 8} {Y + 1} {z0} {x + 8} {Y + 8} {z1} air')
    C(f'fill {x - 6} {Y} {z0} {x + 6} {Y} {z1} gray_concrete')
    C(f'fill {x - 6} {Y} {z0} {x - 6} {Y} {z1} white_concrete')
    C(f'fill {x + 6} {Y} {z0} {x + 6} {Y} {z1} white_concrete')
    C(f'fill {x} {Y} {z0} {x} {Y} {z1} light_gray_concrete')
    for z in range(z0, z1, 6):
        for xx in (x - 3, x + 3):
            C(f'fill {xx} {Y} {z} {xx} {Y} {min(z1, z + 2)} yellow_concrete')
    descarregar(x - 8, z0, x + 8, z1)


def nuvens():
    cx, cz, raio = SET['nuvens']
    random.seed(7)
    for i in range(60):
        a = random.uniform(0, 2 * math.pi); d = raio * math.sqrt(random.random())
        x, z = int(cx + d * math.cos(a)), int(cz + d * math.sin(a))
        y = 232 + random.randint(-4, 6)
        w, l = random.randint(8, 22), random.randint(8, 22)
        cx_ = [(x - w // 2, y, z - l // 2, x + w // 2, y + random.randint(2, 4), z + l // 2)]
        for k in range(random.randint(3, 6)):
            ox, oz = random.randint(-w // 2, w // 2), random.randint(-l // 2, l // 2)
            ww, ll = random.randint(4, 10), random.randint(4, 10)
            cx_.append((x + ox - ww // 2, y, z + oz - ll // 2, x + ox + ww // 2, y + random.randint(3, 7), z + oz + ll // 2))
        for (a1, b1, c1, d1, e1, f1) in cx_:
            carregar(a1, c1, d1, f1)
            C(f'fill {a1} {b1} {c1} {d1} {e1} {f1} white_concrete keep')
            C(f'fill {a1} {b1} {c1} {d1} {b1} {f1} light_gray_concrete replace white_concrete')
            descarregar(a1, c1, d1, f1)


def limpar_arvores():
    """remove arvores/neve fora da floresta (inclusive as que a vila gerou)"""
    x0, z0, x1, z1 = SET['canvas']
    cx, cz, rx, rz = SET['floresta']
    n = 0
    for tx0, tz0, tx1, tz1 in tile_iter(x0, z0, x1, z1, 32):
        if ((min(max(cx, tx0), tx1) - cx) / (rx + 6)) ** 2 + ((min(max(cz, tz0), tz1) - cz) / (rz + 6)) ** 2 <= 1:
            continue
        carregar(tx0, tz0, tx1, tz1)
        for b in ['#minecraft:logs', '#minecraft:leaves', 'snow']:
            for y in range(Y + 1, Y + 33, 8):
                r = C(f'fill {tx0} {y} {tz0} {tx1} {y + 7} {tz1} air replace {b}')
                n += r.get('resultValue', 0) if isinstance(r, dict) else 0
        descarregar(tx0, tz0, tx1, tz1)
    C('kill @e[type=item]')
    print('removidos', n)


def maquete(path=_os.path.join(PROJ, 'tmp', 'maquete.png'), y=340):
    import shot
    x0, z0, x1, z1 = SET['canvas']
    C(f'tp {PL} 300 {y} -1385 180 90')
    time.sleep(12)
    shot.shot(path)
    print(path)




# ---------------- naturalizar: colinas, variacao, mato, bosques ----------------
VILA_BOX = (222, -1592, 392, -1442)   # lago + vila


def _ruido(seed=21):
    rnd = random.Random(seed)
    ondas = []
    for (amp, lam) in [(5.0, 150), (3.0, 85), (1.6, 40), (0.7, 18)]:
        for _ in range(3):
            a = rnd.uniform(0, 2 * math.pi)
            ondas.append((amp / 3 * 1.6, math.cos(a) * 2 * math.pi / lam, math.sin(a) * 2 * math.pi / lam, rnd.uniform(0, 6.3)))
    return lambda x, z: sum(A * math.sin(kx * x + kz * z + f) for A, kx, kz, f in ondas)


def _dist_box(x, z, b):
    x0, z0, x1, z1 = b
    dx = max(x0 - x, 0, x - x1); dz = max(z0 - z, 0, z - z1)
    return math.hypot(dx, dz)


def mascara(x, z):
    """0 = preservar (feature), 1 = terreno livre. transicao de 22 blocos"""
    fx0, fz0, fx1, fz1 = SET['campo']
    cx, cz, rx, rz = SET['floresta']
    rxx, rz0, rz1 = SET['rodovia']
    d = min(_dist_box(x, z, VILA_BOX), _dist_box(x, z, (fx0 - 4, fz0 - 4, fx1 + 4, fz1 + 4)),
            _dist_box(x, z, (rxx - 9, rz0 - 50, rxx + 9, rz1 + 50)),
            max(0.0, (math.hypot((x - cx) / (rx + 5), (z - cz) / (rz + 5)) - 1) * min(rx, rz)))
    u = min(1.0, d / 22); return u * u * (3 - 2 * u)


def naturalizar():
    x0, z0, x1, z1 = SET['canvas']
    N = _ruido()
    alt = {}
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            w = mascara(x, z)
            if w > 0:
                h = N(x, z) * w
                if h < 0: h *= 0.35        # so 5 blocos de terra embaixo (depois e o oceano)
                alt[(x, z)] = int(round(h))
    json.dump({f'{k[0]},{k[1]}': v for k, v in alt.items() if v}, open(_os.path.join(PROJ, 'checkpoints', 'alturas.json'), 'w'))
    prog = _os.path.join(PROJ, 'checkpoints', 'naturalizar_feito.txt')
    feitos = set(open(prog).read().split()) if os.path.exists(prog) else set()
    ncmd = 0
    for a, b, c, d in tile_iter(x0, z0, x1, z1, 64):
        if f'{a},{b}' in feitos: continue
        carregar(a, b, c, d)
        for x in range(a, c + 1):
            z = b
            while z <= d:
                h = alt.get((x, z), 0); z2 = z
                while z2 + 1 <= d and alt.get((x, z2 + 1), 0) == h:
                    z2 += 1
                if h > 0:
                    C(f'fill {x} {Y} {z} {x} {Y + h - 1} {z2} dirt replace #minecraft:replaceable')
                    C(f'fill {x} {Y} {z} {x} {Y + h - 1} {z2} dirt replace grass_block')
                    C(f'fill {x} {Y + h} {z} {x} {Y + h} {z2} grass_block replace #minecraft:replaceable'); ncmd += 3
                elif h < 0:
                    C(f'fill {x} {Y + h + 1} {z} {x} {Y + 3} {z2} air replace #minecraft:dirt')
                    C(f'fill {x} {Y + h + 1} {z} {x} {Y + 3} {z2} air replace #minecraft:replaceable')
                    C(f'fill {x} {Y + h} {z} {x} {Y + h} {z2} grass_block'); ncmd += 3
                z = z2 + 1
        descarregar(a, b, c, d)
        open(prog, 'a').write(f'{a},{b}\n')
        print('tile', a, b, ncmd, flush=True)


def altura(x, z):
    if not hasattr(altura, 'H'):
        altura.H = json.load(open(_os.path.join(PROJ, 'checkpoints', 'alturas.json')))
    return Y + altura.H.get(f'{x},{z}', 0)


def decorar(seed=33):
    """mato, flores, manchas de terra/podzol e bosques verdes esparsos (longe das features)"""
    rnd = random.Random(seed)
    x0, z0, x1, z1 = SET['canvas']
    feats_mato = ['minecraft:patch_grass', 'minecraft:patch_grass', 'minecraft:patch_tall_grass', 'minecraft:flower_default',
                  'minecraft:flower_plain']
    for a, b, c, d in tile_iter(x0, z0, x1, z1, 64):
        carregar(a, b, c, d)
        for _ in range(60):
            x, z = rnd.randint(a, c), rnd.randint(b, d)
            w = mascara(x, z)
            if w < 0.3 and not (_dist_box(x, z, VILA_BOX) > 3 and w > 0): continue
            C(f'place feature {rnd.choice(feats_mato)} {x} {altura(x, z) + 1} {z}')
        for _ in range(6):
            x, z = rnd.randint(a, c), rnd.randint(b, d)
            if mascara(x, z) < 1: continue
            r = rnd.randint(2, 5); b2 = rnd.choice(['coarse_dirt', 'podzol', 'moss_block', 'gravel'])
            for _ in range(r * 3):
                xx, zz = x + rnd.randint(-r, r), z + rnd.randint(-r, r)
                C(f'fill {xx} {altura(xx, zz)} {zz} {xx} {altura(xx, zz)} {zz} {b2} replace grass_block')
        descarregar(a, b, c, d)
    # bosques verdes (carvalho/betula) em grupos pequenos, so onde a mascara e 1
    arvores = 0
    for g in range(22):
        for _ in range(50):
            gx, gz = rnd.randint(x0 + 10, x1 - 10), rnd.randint(z0 + 10, z1 - 10)
            if mascara(gx, gz) >= 1: break
        carregar(gx - 14, gz - 14, gx + 14, gz + 14)
        for _ in range(rnd.randint(2, 7)):
            x, z = gx + rnd.randint(-10, 10), gz + rnd.randint(-10, 10)
            if mascara(x, z) < 1: continue
            f = rnd.choice(['oak', 'oak', 'birch', 'fancy_oak', 'oak_bees_005'])
            C(f'place feature minecraft:{f} {x} {altura(x, z) + 1} {z}'); arvores += 1
        descarregar(gx - 14, gz - 14, gx + 14, gz + 14)
    # arvores solitarias
    for _ in range(25):
        x, z = rnd.randint(x0, x1), rnd.randint(z0, z1)
        if mascara(x, z) < 1: continue
        carregar(x - 4, z - 4, x + 4, z + 4)
        C(f'place feature minecraft:{rnd.choice(["oak", "birch"])} {x} {altura(x, z) + 1} {z}'); arvores += 1
        descarregar(x - 4, z - 4, x + 4, z + 4)
    C('kill @e[type=item]')
    print('arvores', arvores)


if __name__ == '__main__':
    for e in sys.argv[1:]:
        print('==', e, flush=True)
        globals()[e]()
