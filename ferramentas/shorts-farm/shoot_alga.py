"""Gravacao do short ALGA. uso: shoot_alga.py <take> [...]"""
from fl2 import *
BA = B + r'\alga'
K = (44, 113, 211)  # base da alga
KC = (44.5, 114.5, 211.5)
PILAR = [(44, 110, 211), (44, 111, 211), (44, 112, 211), (44, 112, 210), (44, 112, 212), (43, 112, 211), (45, 112, 211)]
CIRC_PEDRAS = [(43, 112, 210), (43, 112, 209), (42, 112, 209), (41, 112, 209), (40, 112, 209), (39, 112, 209), (39, 112, 210),
               (39, 112, 211), (40, 112, 211), (41, 112, 211), (42, 112, 211)]
CIRC_FIO = [(43, 113, 209), (42, 113, 209), (41, 113, 209), (40, 113, 209), (39, 113, 209), (39, 113, 210), (39, 113, 211),
            (40, 113, 211), (41, 113, 211)]


def kit():
    C('clear @J')
    for i, it in enumerate(['stone', 'glass', 'kelp', 'redstone', 'chest', 'hopper', 'comparator', 'repeater']):
        give(i, it, 64)


def vidro_camada(y, ev=None):
    for p in [(44, y, 210), (44, y, 212), (43, y, 211), (45, y, 211)]:
        if ev: ev('vidro')
        bloco(1, *p); time.sleep(0.12)


def troca(x, y, z, estado, som='minecraft:block.stone.place'):
    C(f'setblock {x} {y} {z} {estado}')
    snd(som, x + .5, y + .5, z + .5)


def agua(x, y, z):
    C(f'setblock {x} {y} {z} water'); snd('minecraft:item.bucket.empty', x + .5, y + .5, z + .5)


def alga_col():
    return [state(44, y, 211).split('[')[0][10:] for y in range(113, 118)]


def t_coluna():
    cam('a01', (48.8, 117.4, 216.8), (47.4, 116.6, 215.4), (44.5, 113.8, 211.5), 21000)

    def fn(ev):
        tpme(44.5, 110, 216, 180, 10); play('a01'); time.sleep(1.2)
        for p in PILAR:
            ev('pilar'); bloco(0, *p); time.sleep(0.25)
        for y in range(113, 117):
            vidro_camada(y, ev)
        time.sleep(0.3)
        for y in range(113, 117):
            ev('agua'); agua(44, y, 211); time.sleep(0.35)
        time.sleep(0.4)
        ev('alga'); tpme(44.5, 114.5, 214.0, 180, 45); time.sleep(0.15); place(2, 44, 112, 211, 'up')
    shot('a01_coluna', fn, 21.4, BA)


def t_cresce():
    cam('a02', (47.2, 114.6, 214.8), (47.0, 115.6, 214.6), (44.5, 114.4, 211.5), 9000, (44.5, 115.4, 211.5))

    def fn(ev):
        play('a02'); time.sleep(0.6); C('gamerule randomTickSpeed 700'); ev('acelerado')
        t0 = time.time(); ult = None
        while time.time() - t0 < 8.0:
            c = alga_col()
            if c != ult: ev('alga_' + '-'.join(x[:5] for x in c)); ult = c
            if c[1] != 'water':
                C('gamerule randomTickSpeed 3')
            time.sleep(0.2)
        C('gamerule randomTickSpeed 3')
    shot('a02_cresce', fn, 9.4, BA)


def t_corte():
    cam('a03', (48.4, 117.2, 216.0), (47.9, 116.9, 215.4), (45.0, 114.6, 211.4), 20000)

    def fn(ev):
        play('a03'); time.sleep(1.2)
        ev('pistao'); troca(45, 114, 211, 'piston[facing=west]'); time.sleep(0.7)
        ev('observador'); troca(45, 115, 211, 'observer[facing=west]'); time.sleep(0.7)
        ev('pedra'); bloco(0, 46, 113, 211); time.sleep(0.25)
        ev('pedra'); bloco(0, 46, 114, 211); time.sleep(0.4)
        ev('fio'); bloco(3, 46, 115, 211); time.sleep(0.4)
        C('gamerule randomTickSpeed 900'); ev('acelerado')
        t0 = time.time(); ult = None; n = 0
        while time.time() - t0 < 14.0 and n < 2:
            p = state(45, 114, 211)
            if 'extended=true' in p and ult != 'x': ev('corte'); ult = 'x'; n += 1
            elif 'extended=false' in p: ult = None
            time.sleep(0.05)
        C('gamerule randomTickSpeed 3'); time.sleep(1.5)
    shot('a03_corte', fn, 20.4, BA)


def itens_alga(r=4):
    q = mc.call('entities.query', {'radius': r, 'center': {'x': 44.5, 'y': 116, 'z': 211.5}, 'types': ['minecraft:item'], 'includePlayers': False})
    return q.get('entities', [])


def t_presa():
    # garante alguns itens boiando no topo
    C('gamerule randomTickSpeed 150')
    t0 = time.time()
    while len(itens_alga()) < 3 and time.time() - t0 < 40:
        time.sleep(0.5)
    C('gamerule randomTickSpeed 3')
    print('itens', [(round(e['x'], 1), round(e['y'], 1), round(e['z'], 1)) for e in itens_alga()])
    cam('a04', (46.6, 118.6, 213.6), (46.2, 118.4, 213.2), (44.5, 116.6, 211.5), 6000)
    shot('a04_presa', lambda ev: play('a04'), 6.4, BA)


def t_corrente():
    cam('a05', (46.8, 120.0, 215.0), (46.0, 119.6, 214.4), (43.8, 116.8, 211.5), 11000)

    def fn(ev):
        play('a05'); time.sleep(1.2)
        ev('funil'); troca(43, 116, 211, 'hopper[facing=down]', 'minecraft:block.metal.place'); time.sleep(0.5)
        for p in [(44, 117, 210), (44, 117, 212), (45, 117, 210), (45, 117, 212), (43, 117, 210), (43, 117, 212),
                  (42, 117, 210), (42, 117, 212), (42, 117, 211), (46, 117, 210), (46, 117, 211)]:
            ev('vidro'); bloco(1, *p); time.sleep(0.1)
        time.sleep(0.2)
        ev('agua'); agua(45, 117, 211)
        C('gamerule randomTickSpeed 60')
    shot('a05_corrente', fn, 11.4, BA)
    C('gamerule randomTickSpeed 3')
    print('funil', C('data get block 43 116 211 Items')['output'])


def t_defumador():
    cam('a06', (39.4, 117.6, 215.8), (40.0, 117.2, 215.2), (42.8, 115.2, 211.5), 11000)

    def fn(ev):
        play('a06'); time.sleep(1.2)
        ev('defumador'); troca(43, 115, 211, 'smoker[facing=south]'); time.sleep(0.7)
        ev('pedra'); bloco(0, 42, 114, 211); time.sleep(0.4)
        ev('funil'); bloco(5, 42, 115, 211, None, 'minecraft:hopper[facing=east]', pref='east'); time.sleep(0.5)
        ev('bau'); bloco(4, 42, 116, 211, 'north', 'minecraft:chest[facing=south]'); time.sleep(0.3)
        C('item replace block 42 116 211 container.13 with dried_kelp_block 3')
        ev('combustivel')
        C('gamerule randomTickSpeed 60')
    shot('a06_defumador', fn, 11.4, BA)
    C('gamerule randomTickSpeed 3')


def t_crafter():
    cam('a07', (37.2, 117.4, 205.6), (37.8, 117.1, 206.2), (41.4, 112.8, 210.3), 17000)

    def fn(ev):
        play('a07'); time.sleep(1.2)
        ev('funil'); troca(43, 114, 211, 'hopper[facing=down]', 'minecraft:block.metal.place'); time.sleep(0.5)
        ev('crafter'); troca(43, 113, 211, 'crafter[orientation=down_north]'); time.sleep(0.5)
        ev('bau'); troca(43, 112, 211, 'chest[facing=south]', 'minecraft:block.wood.place'); time.sleep(0.5)
        ev('pedra'); bloco(0, 43, 112, 210, pref='south'); time.sleep(0.25)
        ev('comparador'); bloco(6, 43, 113, 210, 'north', 'minecraft:comparator[facing=south]'); time.sleep(0.6)
        for p in CIRC_PEDRAS[1:]:
            ev('pedra'); bloco(0, *p); time.sleep(0.15)
        for p in CIRC_FIO:
            ev('fio'); bloco(3, *p); time.sleep(0.2)
        ev('repetidor'); bloco(7, 42, 113, 211, 'east', 'minecraft:repeater[facing=west]'); time.sleep(0.4)
    shot('a07_crafter', fn, 17.4, BA)


def t_bloco(maxs=240):
    cam_pts = [(38.6, 116.4, 206.4, *yp((38.6, 116.4, 206.4), (41.6, 112.8, 210.2))),
               (38.8, 116.3, 206.6, *yp((38.8, 116.3, 206.6), (41.6, 112.8, 210.2)))]
    scene('a08', cam_pts, int(maxs * 1000))

    def fn(ev):
        estacionar(); play('a08'); time.sleep(0.8)
        C('gamerule randomTickSpeed 150'); C('tick rate 60'); ev('acelerado')
        t0 = time.time(); ult = -1
        while time.time() - t0 < maxs - 5:
            o = C('data get block 43 113 211 Items')['output'][0].count('Slot')
            if o != ult: ev(f'slots_{o}'); ult = o
            b = C('data get block 43 112 211 Items')['output'][0]
            if 'dried_kelp_block' in b:
                ev('bloco'); C('tick rate 20'); time.sleep(3); break
            time.sleep(0.15)
        C('tick rate 20'); C('gamerule randomTickSpeed 3'); C('cinematic-server stop @J')
    shot('a08_bloco', fn, 1, BA, maxs=maxs + 10)
    print('bau', C('data get block 43 112 211 Items')['output'])


def t_orbita():
    pts = []
    for ang in (330, 250, 170):
        a = math.radians(ang); c = (42.5 + 7.5 * math.sin(a), 118.5, 211 + 7.5 * math.cos(a))
        pts.append((round(c[0], 2), c[1], round(c[2], 2), *yp(c, (42.5, 114.2, 211))))
    scene('a09', pts, 13000)
    C('gamerule randomTickSpeed 60')
    shot('a09_orbita', lambda ev: play('a09'), 13.4, BA)
    C('gamerule randomTickSpeed 3')


def t_close_fumaca():
    cam('a10', (41.0, 116.0, 213.6), (41.3, 115.9, 213.3), (43.0, 115.4, 211.5), 6000)
    shot('a10_close', lambda ev: play('a10'), 6.4, BA)


if __name__ == '__main__':
    os.makedirs(BA, exist_ok=True)
    for t in sys.argv[1:]:
        if t == 'kit':
            kit()
        else:
            globals()['t_' + t]()
        time.sleep(0.8)
