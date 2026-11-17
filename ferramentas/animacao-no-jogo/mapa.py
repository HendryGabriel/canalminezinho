"""Heightmap do chao (ignora folhas, troncos, plantas, neve fina)."""
import json, sys, mc

IGN = ('leaves', 'log', 'wood', 'short_grass', 'tall_grass', 'fern', 'snow', 'flower', 'bush', 'vine', 'berry', 'mushroom', 'sapling',
       'dandelion', 'poppy', 'tulip', 'allium', 'orchid', 'daisy', 'cornflower', 'lily', 'torch', 'fence', 'leaf', 'moss_carpet')


def chao(x0, z0, x1, z1, y0=55, y1=120):
    H, TOP = {}, {}
    for cx in range(x0, x1 + 1, 16):
        for cz in range(z0, z1 + 1, 16):
            r = mc.call('world.getBlocks', {'from': {'x': cx, 'y': y0, 'z': cz},
                                             'to': {'x': min(cx + 15, x1), 'y': y1, 'z': min(cz + 15, z1)}})
            for b in r['blocks']:
                k = (b['x'], b['z']); bid = b['id'].split(':')[1]
                if b['y'] > TOP.get(k, (-999,))[0]:
                    TOP[k] = (b['y'], bid)
                if bid == 'snow_block' or not any(s in bid for s in IGN):
                    if b['y'] > H.get(k, (-999,))[0]:
                        H[k] = (b['y'], bid)
    return H, TOP


if __name__ == '__main__':
    x0, z0, x1, z1 = map(int, sys.argv[1:5])
    H, TOP = chao(x0, z0, x1, z1)
    json.dump({'H': {f'{k[0]},{k[1]}': v for k, v in H.items()}, 'TOP': {f'{k[0]},{k[1]}': v for k, v in TOP.items()}},
              open(sys.argv[5], 'w'))
    print(len(H))
