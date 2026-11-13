"""Gravacao do short MEL. uso: shoot_mel.py <take> [<take>...]"""
from fl2 import *
import random
BM = B + r'\mel'
H = (22, 111, 211)
HC = (22.5, 111.5, 211.5)
FLORES = [('poppy', 20, 213), ('dandelion', 24, 213), ('cornflower', 21, 214), ('allium', 23, 214),
          ('azure_bluet', 25, 214), ('oxeye_daisy', 19, 214), ('red_tulip', 22, 215), ('lily_of_the_valley', 24, 215)]
LOG = BM + r'\niveis.json'
# fio com 5 pedacos: so o sinal 5 do comparador chega ao fim (sinal cai 1 por bloco)
PEDRAS = [(22, 110, 209), (21, 110, 209), (21, 111, 209), (20, 110, 209), (20, 111, 209), (20, 110, 210), (20, 111, 210), (20, 110, 211), (20, 111, 211), (21, 110, 211)]
FIO = [(22, 111, 209), (21, 112, 209), (20, 112, 209), (20, 112, 210), (20, 112, 211)]


def kit():
    C('clear @J')
    for i, it in enumerate(['stone', 'beehive', 'comparator', 'redstone', 'dispenser', 'chest', 'hopper', 'poppy']):
        give(i, it, 16)


def nivel():
    s = state(*H)
    return int(s.split('honey_level=')[1][0]) if 'honey_level=' in s else -1


def t_colmeia():
    cam('m01', (26.8, 113.6, 217.4), (25.3, 112.7, 215.6), (22.5, 111.2, 211.5), 8000)

    def fn(ev):
        tpme(22.5, 110, 216, 180, 20); play('m01'); time.sleep(1.3)
        ev('pedra'); bloco(0, 22, 110, 211); time.sleep(0.9)
        ev('colmeia'); bloco(1, 22, 111, 211, 'north', 'minecraft:beehive[facing=south]'); time.sleep(1.2)
        ev('abelhas')
        for dx in (-0.8, 0.0, 0.8):
            C(f'summon bee {22.5 + dx} 112.6 {212.8} {{hive_pos:[I;22,111,211]}}'); time.sleep(0.25)
    shot('m01_colmeia', fn, 8.6, BM)


def t_semflor():
    pts = []
    for ang in (25, -20):
        a = math.radians(ang); c = (HC[0] + 5.2 * math.sin(a) * -1, 112.4, HC[2] + 5.2 * math.cos(a))
        pts.append((round(c[0], 2), c[1], round(c[2], 2), *yp(c, (22.5, 111.8, 211.5))))
    scene('m02', pts, 9000)
    shot('m02_semflor', lambda ev: (tpme(22.5, 110, 205, 0, 0), play('m02')), 9.5, BM)


def t_flores():
    cam('m03', (22.3, 114.3, 217.9), (23.2, 113.9, 217.0), (22.5, 110.6, 212.8), 9000)

    def fn(ev):
        play('m03'); time.sleep(1.2)
        for nome, x, z in FLORES:
            C(f'item replace entity @J hotbar.7 with {nome} 4'); time.sleep(0.05)
            ev('flor'); bloco(7, x, 110, z); time.sleep(0.5)
    shot('m03_flores', fn, 9.5, BM)


def t_comparador():
    cam('m04', (24.3, 116.3, 205.2), (23.7, 116.0, 205.8), (21.2, 110.8, 210.0), 16000)

    def fn(ev):
        play('m04'); time.sleep(1.2)
        ev('pedra'); bloco(0, 22, 110, 210); time.sleep(0.6)
        ev('comparador'); bloco(2, 22, 111, 210, 'north', 'minecraft:comparator[facing=south]'); time.sleep(0.9)
        for x, y, z in PEDRAS:
            ev('pedra'); bloco(0, x, y, z); time.sleep(0.22)
        for x, y, z in FIO:
            ev('fio'); bloco(3, x, y, z); time.sleep(0.3)
        ev('nivel_%d' % nivel())
    shot('m04_comparador', fn, 16.5, BM)


def t_ejetor():
    cam('m05', (18.2, 114.6, 215.2), (18.9, 114.2, 214.6), (21.3, 111.3, 211.0), 7000)

    def fn(ev):
        play('m05'); time.sleep(1.3)
        ev('ejetor'); bloco(4, 21, 111, 211, 'west', 'minecraft:dispenser[facing=east]'); time.sleep(0.3)
        C('item replace block 21 111 211 container.4 with shears')
        ev('nivel_%d' % nivel())
    print('nivel antes', nivel())
    shot('m05_ejetor', fn, 7.4, BM)


def esperar_colheita(nome, camera, maxs=420, rate=40, depois=4.0):
    """grava ate a colmeia chegar a 5 e ser colhida (volta a 0)."""
    scene(nome, camera, int(maxs * 1000))
    log = []

    def fn(ev):
        estacionar(); play(nome); time.sleep(0.8)
        C(f'tick rate {rate}')
        ult = nivel(); ev(f'nivel_{ult}'); t0 = time.time(); cheio = False
        while time.time() - t0 < maxs - 6:
            n = nivel()
            if n != ult:
                ev(f'nivel_{n}'); log.append((n, time.time())); print('nivel', n, round(time.time() - t0, 1))
                if ult == 5 and n == 0:
                    C('tick rate 20'); time.sleep(depois); break
                ult = n
            time.sleep(0.1)
        C('tick rate 20'); C(f'cinematic-server stop @J')
    out = shot(nome, fn, 1, BM, maxs=maxs + 10)
    return log


def t_contagem():
    cam_pts = [(25.6, 113.2, 216.2, *yp((25.6, 113.2, 216.2), (22.0, 111.2, 211.0))),
               (25.4, 113.1, 216.0, *yp((25.4, 113.1, 216.0), (22.0, 111.2, 211.0)))]
    return esperar_colheita('m06_contagem', cam_pts)


def t_favos_chao():
    q = mc.call('entities.query', {'radius': 6, 'x': 22.5, 'y': 111, 'z': 211.5})
    its = [e for e in q['entities'] if e['type'] == 'minecraft:item']
    print('itens', [(round(e['x'], 2), round(e['y'], 2), round(e['z'], 2)) for e in its])
    if its:
        cx = sum(e['x'] for e in its) / len(its); cz = sum(e['z'] for e in its) / len(its); cy = its[0]['y']
    else:
        cx, cy, cz = 22.5, 110.1, 212.5
    t = (cx, cy + 0.2, cz)
    cam('m07', (cx - 2.2, cy + 1.3, cz + 2.6), (cx - 1.6, cy + 1.0, cz + 2.0), t, 6000)
    shot('m07_favos_chao', lambda ev: play('m07'), 6.4, BM)


def t_funil():
    C('kill @e[type=item,x=22,y=111,z=211,distance=..8]')
    C('setblock 22 110 211 air')
    cam('m08', (25.6, 111.6, 214.6), (25.0, 111.4, 214.0), (22.6, 110.6, 211.4), 7500)

    def fn(ev):
        play('m08'); time.sleep(1.3)
        ev('bau'); bloco(5, 23, 110, 211, 'north', 'minecraft:chest[facing=south]'); time.sleep(0.9)
        ev('funil'); bloco(6, 22, 110, 211, None, 'minecraft:hopper[facing=east]', pref='east'); time.sleep(0.5)
    shot('m08_funil', fn, 7.8, BM)


def t_funil_colhe():
    cam_pts = [(25.2, 112.4, 214.8, *yp((25.2, 112.4, 214.8), (22.6, 110.9, 211.4))),
               (25.0, 112.3, 214.6, *yp((25.0, 112.3, 214.6), (22.6, 110.9, 211.4)))]
    log = esperar_colheita('m09_funil_colhe', cam_pts, depois=3.0)
    print('bau', C('data get block 23 110 211 Items')['output'])
    return log


def t_orbita():
    pts = []
    for ang in (55, 0, -55):
        a = math.radians(ang); c = (21.6 + 7.2 * math.sin(a), 114.8, 211.6 + 7.2 * math.cos(a))
        pts.append((round(c[0], 2), c[1], round(c[2], 2), *yp(c, (21.6, 111.0, 211.6))))
    scene('m11', pts, 12000)
    shot('m11_orbita', lambda ev: play('m11'), 12.5, BM)


def t_close():
    cam('m12', (23.9, 112.3, 208.6), (23.5, 112.1, 208.9), (22.3, 111.1, 210.4), 6000)
    shot('m12_close', lambda ev: play('m12'), 6.4, BM)


def t_tesouras():
    cam('m10', (18.4, 113.2, 213.6), (18.6, 113.1, 213.4), (21.3, 111.4, 211.3), 9000)
    C('clear @J')

    def fn(ev):
        play('m10'); time.sleep(0.8)
        tpme(18.5, 110, 211.5, -90, 10); time.sleep(0.2)
        mc.call('container.open', {'x': 21, 'y': 111, 'z': 211}); time.sleep(1.5); ev('gui')
        for s in [0, 1, 2, 3, 5, 6, 7, 8]:
            C(f'item replace block 21 111 211 container.{s} with shears')
            snd('minecraft:ui.button.click', 21.5, 111.5, 211.5, 0.6, 1.4); ev(f'slot{s}'); time.sleep(0.4)
        time.sleep(1.5); mc.call('screen.close'); ev('fecha')
    shot('m10_tesouras', fn, 8.5, BM)


if __name__ == '__main__':
    os.makedirs(BM, exist_ok=True)
    for t in sys.argv[1:]:
        if t == 'kit':
            kit()
        else:
            r = globals()['t_' + t]()
            if r:
                json.dump(r, open(BM + rf'\log_{t}.json', 'w'))
        time.sleep(0.8)
