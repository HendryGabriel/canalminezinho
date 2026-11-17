"""Acha arvore + posicao de camera com visada livre para as cenas de pouso."""
import math, json, mc

SOLIDO_IGN = ('air', 'snow', 'short_grass', 'fern', 'tall_grass', 'large_fern')


def blocos(x0, y0, z0, x1, y1, z1):
    S = {}
    for cx in range(x0, x1 + 1, 16):
        for cz in range(z0, z1 + 1, 16):
            r = mc.call('world.getBlocks', {'from': {'x': cx, 'y': y0, 'z': cz}, 'to': {'x': min(cx + 15, x1), 'y': y1, 'z': min(cz + 15, z1)}})
            for b in r['blocks']:
                S[(b['x'], b['y'], b['z'])] = b['id'].split(':')[1]
    return S


def livre(S, a, b, passo=0.25):
    d = math.dist(a, b); n = int(d / passo)
    for i in range(1, n):
        u = i / n
        p = tuple(int(math.floor(a[k] + (b[k] - a[k]) * u)) for k in range(3))
        bid = S.get(p, 'air')
        if bid not in SOLIDO_IGN:
            return False
    return True


def achar(x0=370, z0=2035, x1=430, z1=2100, y0=62, y1=100):
    S = blocos(x0, y0, z0, x1, y1, z1)
    logs = {}
    for (x, y, z), b in S.items():
        if b == 'spruce_log':
            k = (x, z); logs.setdefault(k, []).append(y)
    res = []
    for (x, z), ys in logs.items():
        top, bot = max(ys), min(ys)
        if top - bot < 6: continue
        g = bot - 1
        # lugar de pouso: coluna vizinha (a 1 bloco do tronco) com chao
        for dx, dz in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            px, pz = x + dx + 0.5, z + dz + 0.5
            alvo_baixo = (px, g + 1.5, pz)
            alvo_alto = (px, top - 1, pz)
            for R in (6, 7, 8):
                for ang in range(0, 360, 20):
                    a = math.radians(ang)
                    for h in (2.5, 3.5):
                        c = (px + R * math.cos(a), g + h, pz + R * math.sin(a))
                        cb = tuple(int(math.floor(v)) for v in c)
                        if S.get(cb, 'air') not in SOLIDO_IGN: continue
                        if S.get((cb[0], cb[1] + 1, cb[2]), 'air') not in SOLIDO_IGN: continue
                        if not livre(S, c, alvo_baixo): continue
                        ok_alto = livre(S, c, (px, g + 6, pz))
                        res.append(((x, z), (px, pz), g, top, c, ok_alto))
    return res


if __name__ == '__main__':
    r = achar()
    boas = [a for a in r if a[5]]
    print(len(r), len(boas))
    vist = set()
    for a in boas:
        if a[0] in vist: continue
        vist.add(a[0]); print(a)
        if len(vist) > 12: break
