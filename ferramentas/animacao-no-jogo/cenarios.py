import os as _os
PROJ = _os.environ.get('ANIM_PROJETO', _os.getcwd())
"""Monta os cenarios: lago, campo de terra, rodovia, nuvens. Salva checkpoint antes de mexer."""
import json, math, random, sys, os
import mc
from motor import C

CK = _os.path.join(PROJ, 'checkpoints')
os.makedirs(CK, exist_ok=True)
MAPA = json.load(open(_os.path.join(PROJ, 'tmp', 'mapa1.json')))['H']


def g(x, z):
    return MAPA[f'{x},{z}'][0]


def checkpoint(nome, x0, y0, z0, x1, y1, z1):
    blocos = []
    for cx in range(x0, x1 + 1, 16):
        for cz in range(z0, z1 + 1, 16):
            r = mc.call('world.getBlocks', {'from': {'x': cx, 'y': y0, 'z': cz}, 'to': {'x': min(cx + 15, x1), 'y': y1, 'z': min(cz + 15, z1)},
                                             'includeState': True, 'includeAir': False})
            blocos += r['blocks']
    json.dump({'box': [x0, y0, z0, x1, y1, z1], 'blocks': blocos}, open(f'{CK}/{nome}.json', 'w'))
    print('checkpoint', nome, len(blocos))


def lago(cx=345, cz=1980, r=13, prof=4):
    cols = [(x, z) for x in range(cx - r - 3, cx + r + 4) for z in range(cz - r - 3, cz + r + 4)]
    dentro = [(x, z) for x, z in cols if math.hypot(x - cx, (z - cz) * 1.15) <= r]
    L = min(g(x, z) for x, z in dentro)
    print('nivel da agua', L)
    hs = [g(x, z) for x, z in cols]
    checkpoint('lago', cx - r - 3, L - prof - 1, cz - r - 3, cx + r + 3, max(hs) + 4, cz + r + 3)
    for x, z in cols:
        d = math.hypot(x - cx, (z - cz) * 1.15) + random.uniform(-0.8, 0.8)
        gz = g(x, z)
        if d <= r:
            fundo = L - max(1, int(prof * (1 - (d / r) ** 2)) + 1)
            C(f'fill {x} {fundo} {z} {x} {L} {z} water')
            C(f'fill {x} {fundo - 1} {z} {x} {fundo - 1} {z} gravel')
            if gz + 3 > L:
                C(f'fill {x} {L + 1} {z} {x} {gz + 3} {z} air')
        elif d <= r + 3 and gz > L:
            # margem: rebaixa ate L (grama)
            C(f'fill {x} {L + 1} {z} {x} {gz + 3} {z} air')
            C(f'setblock {x} {L} {z} grass_block')
    C(f'kill @e[type=item,x={cx},y={L},z={cz},distance=..40]')


def campo(x0=312, z0=2000, x1=334, z1=2018):
    hs = [g(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)]
    checkpoint('campo', x0, min(hs) - 2, z0, x1, max(hs) + 4, z1)
    base = int(sorted(hs)[len(hs) // 2])
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            gz = g(x, z)
            if gz > base:
                C(f'fill {x} {base + 1} {z} {x} {gz + 3} {z} air')
            elif gz < base:
                C(f'fill {x} {gz} {z} {x} {base - 1} {z} dirt')
            else:
                C(f'fill {x} {base + 1} {z} {x} {base + 3} {z} air')
            b = 'coarse_dirt' if (x + z * 3) % 5 else 'dirt'
            if (x - x0) % 4 == 0: b = 'rooted_dirt'
            C(f'setblock {x} {base} {z} {b}')
    C(f'kill @e[type=item,x={(x0 + x1) // 2},y={base},z={(z0 + z1) // 2},distance=..40]')
    return base


def nuvens(cx, cz, raio=180, n=70, y0=232, seed=7):
    """nuvens de blocos (concreto branco + neve) num raio em volta de (cx,cz)"""
    random.seed(seed)
    caixas = []
    for i in range(n):
        a = random.uniform(0, 2 * math.pi); d = raio * math.sqrt(random.random())
        x, z = int(cx + d * math.cos(a)), int(cz + d * math.sin(a))
        y = y0 + random.randint(-4, 6)
        w, l = random.randint(8, 22), random.randint(8, 22)
        caixas.append((x - w // 2, y, z - l // 2, x + w // 2, y + random.randint(2, 4), z + l // 2))
        for k in range(random.randint(3, 6)):
            ox, oz = random.randint(-w // 2, w // 2), random.randint(-l // 2, l // 2)
            ww, ll = random.randint(4, 10), random.randint(4, 10)
            hh = random.randint(3, 7)
            caixas.append((x + ox - ww // 2, y, z + oz - ll // 2, x + ox + ww // 2, y + hh, z + oz + ll // 2))
    json.dump(caixas, open(f'{CK}/nuvens_caixas.json', 'w'))
    for (a, b, c, d, e, f) in caixas:
        C(f'fill {a} {b} {c} {d} {e} {f} white_concrete keep')
        # sombra: base cinza clara
        C(f'fill {a} {b} {c} {d} {b} {f} light_gray_concrete replace white_concrete')
    print('nuvens', len(caixas))


def rodovia(x0, z0, comp=120, y=None):
    """rodovia norte-sul plana a partir de (x0,z0): 2 pistas por sentido"""
    y = y or 0
    checkpoint('rodovia', x0 - 8, y - 2, z0, x0 + 8, y + 12, z0 + comp)
    C(f'fill {x0 - 8} {y + 1} {z0} {x0 + 8} {y + 12} {z0 + comp} air')
    C(f'fill {x0 - 8} {y - 2} {z0} {x0 + 8} {y - 1} {z0 + comp} dirt')
    C(f'fill {x0 - 8} {y} {z0} {x0 + 8} {y} {z0 + comp} grass_block')
    C(f'fill {x0 - 6} {y} {z0} {x0 + 6} {y} {z0 + comp} gray_concrete')
    C(f'fill {x0} {y} {z0} {x0} {y} {z0 + comp} light_gray_concrete')
    C(f'fill {x0 - 6} {y} {z0} {x0 - 6} {y} {z0 + comp} white_concrete')
    C(f'fill {x0 + 6} {y} {z0} {x0 + 6} {y} {z0 + comp} white_concrete')
    for z in range(z0, z0 + comp, 6):
        for xx in (x0 - 3, x0 + 3):
            C(f'fill {xx} {y} {z} {xx} {y} {z + 2} yellow_concrete')


if __name__ == '__main__':
    eval(sys.argv[1])


def restaurar(nome):
    d = json.load(open(f'{CK}/{nome}.json'))
    x0, y0, z0, x1, y1, z1 = d['box']
    for y in range(y0, y1 + 1, 8):
        C(f'fill {x0} {y} {z0} {x1} {min(y + 7, y1)} {z1} air')
    C('gamerule block_drops false') if False else None
    # primeiro blocos solidos, depois os que dependem de suporte
    dep = ('snow', 'grass', 'fern', 'flower', 'torch', 'lantern', 'sapling', 'berry', 'carpet', 'button', 'door', 'rail')
    bs = sorted(d['blocks'], key=lambda b: (any(s in b['id'] for s in dep), b['y']))
    for b in bs:
        st = b.get('state', b['id'])
        C(f"setblock {b['x']} {b['y']} {b['z']} {st}")
    C(f'kill @e[type=item,x={(x0 + x1) // 2},y={(y0 + y1) // 2},z={(z0 + z1) // 2},distance=..60]')
    print('restaurado', nome, len(bs))


def lago2(cx=345, cz=1972, r=12, borda=8, L=None, prof=4):
    R2 = r + borda
    cols = [(x, z) for x in range(cx - R2 - 1, cx + R2 + 2) for z in range(cz - R2 - 1, cz + R2 + 2)]
    dist = {}
    for x, z in cols:
        dist[(x, z)] = math.hypot(x - cx, (z - cz) * 1.1) + 0.9 * math.sin(math.atan2(z - cz, x - cx) * 3 + 1.3)
    if L is None:
        L = int(sorted(g(x, z) for x, z in cols if dist[(x, z)] <= r)[len([1 for c in cols if dist[c] <= r]) // 3])
    print('L', L)
    top = max(g(x, z) for x, z in cols) + 35
    checkpoint('lago2', cx - R2 - 1, L - prof - 2, cz - R2 - 1, cx + R2 + 1, top, cz + R2 + 1)
    for x, z in cols:
        d = dist[(x, z)]
        if d > R2:
            continue
        gz = g(x, z)
        if d <= r:
            fundo = L - max(1, int(round(prof * (1 - (d / r) ** 2))))
            C(f'fill {x} {fundo + 1} {z} {x} {top} {z} air')
            C(f'fill {x} {fundo + 1} {z} {x} {L} {z} water')
            C(f'setblock {x} {fundo} {z} {"gravel" if d > r - 2 else "clay"}')
            if d > r - 1.2:
                pass
        else:
            u = (d - r) / borda; s = u * u * (3 - 2 * u)
            h = int(round((L + 1) * (1 - s) + gz * s))
            C(f'fill {x} {h + 1} {z} {x} {top} {z} air')
            C(f'fill {x} {min(h, gz) - 3} {z} {x} {h - 1} {z} dirt replace air')
            C(f'fill {x} {min(h, gz) - 3} {z} {x} {h - 1} {z} dirt replace water')
            C(f'setblock {x} {h} {z} {"sand" if d < r + 1.5 else "grass_block"}')
            if d >= r + 1.5:
                C(f'setblock {x} {h + 1} {z} snow')
    C(f'kill @e[type=item,x={cx},y={L},z={cz},distance=..60]')


def perfil_rodovia(x0=268, z0=2035, z1=2155):
    H = json.load(open(_os.path.join(PROJ, 'tmp', 'rod.json')))
    raw = {}
    for z in range(z0 - 3, z1 + 4):
        hs = sorted(H[f'{x},{z}'][0] for x in range(x0 - 8, x0 + 9) if f'{x},{z}' in H)
        raw[z] = hs[len(hs) // 2]
    Y = {}
    for z in range(z0, z1 + 1):
        Y[z] = int(round(sum(raw[k] for k in range(z - 3, z + 4)) / 7))
    # no maximo 1 bloco de degrau por 3 blocos
    return Y


def rodovia2(x0=268, z0=2035, z1=2155):
    H = json.load(open(_os.path.join(PROJ, 'tmp', 'rod.json')))
    Y = perfil_rodovia(x0, z0, z1)
    ys = list(Y.values())
    checkpoint('rodovia2', x0 - 9, min(ys) - 4, z0, x0 + 9, max(ys) + 18, z1)
    for z in range(z0, z1 + 1):
        y = Y[z]
        C(f'fill {x0 - 9} {y + 1} {z} {x0 + 9} {y + 18} {z} air')
        C(f'fill {x0 - 9} {y - 4} {z} {x0 + 9} {y - 1} {z} dirt replace #minecraft:air')
        C(f'fill {x0 - 9} {y} {z} {x0 + 9} {y} {z} snow_block')
        C(f'fill {x0 - 6} {y} {z} {x0 + 6} {y} {z} gray_concrete')
        for xx in (x0 - 6, x0 + 6):
            C(f'setblock {xx} {y} {z} white_concrete')
        C(f'setblock {x0} {y} {z} light_gray_concrete')
        if z % 6 < 3:
            for xx in (x0 - 3, x0 + 3):
                C(f'setblock {xx} {y} {z} yellow_concrete')
    C(f'kill @e[type=item,x={x0},y={min(ys)},z={(z0 + z1) // 2},distance=..90]')
    json.dump(Y, open(f'{CK}/rodovia_perfil.json', 'w'))
