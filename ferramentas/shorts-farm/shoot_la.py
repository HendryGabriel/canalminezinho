"""Gravacao do short LA. uso: shoot_la.py <take> [...]"""
from fl2 import *
BL = B + r'\la'
GX, GZ = 34, 201  # modulo demonstracao (grama em y=112)
CORES = ['white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray', 'cyan', 'purple', 'blue',
         'brown', 'green', 'red', 'black']
COR_DEMO = 14  # vermelho


def modulo(gx, gz):
    """blocos do modulo completo (para clonar)"""
    return {
        'vidro': [(gx - 1, 113, gz), (gx, 113, gz - 1), (gx, 113, gz + 1), (gx - 1, 114, gz), (gx, 114, gz - 1), (gx, 114, gz + 1),
                  (gx + 1, 114, gz), (gx, 115, gz)],
        'anel': [(gx - 1, 112, gz), (gx, 112, gz - 1), (gx, 112, gz + 1)],
    }


def kit():
    C('clear @J')
    for i, it in enumerate(['stone', 'glass', 'grass_block', 'redstone', 'chest', 'hopper', 'observer', 'dispenser']):
        give(i, it, 64)


def ovelha():
    return f'@e[type=sheep,limit=1,sort=nearest,x={GX + .5},y=113,z={GZ + .5},distance=..2]'


def tosada():
    o = C(f'data get entity {ovelha()} Sheared')['output']
    return '1b' in o[0] if o else None


def g():
    return state(GX, 112, GZ).split('[')[0][10:]


def inicio():
    """estado inicial (sem animacao): grama flutuando + celula de vidro + ovelha tosada"""
    C(f'setblock {GX} 112 {GZ} grass_block')
    for p in modulo(GX, GZ)['vidro']:
        C('setblock %d %d %d glass' % p)
    C(f'kill @e[type=sheep,x={GX},y=113,z={GZ},distance=..3]')
    C(f'summon sheep {GX + .5} 113 {GZ + .5} {{Color:{COR_DEMO}b,Sheared:1b,PersistenceRequired:1b}}')


def esperar(nome, camera, cond, maxs=200, depois=3.0, rate=20):
    scene(nome, camera, int(maxs * 1000))

    def fn(ev):
        estacionar(); play(nome); time.sleep(0.8); ev('pronto')
        if rate != 20: C(f'tick rate {rate}')
        t0 = time.time()
        while time.time() - t0 < maxs - 5:
            r = cond()
            if r:
                C('tick rate 20'); ev(r); time.sleep(depois); break
            time.sleep(0.05)
        C('tick rate 20'); C('cinematic-server stop @J')
    shot(nome, fn, 1, BL, maxs=maxs + 10)


CAM_CELA = lambda: [(GX + 3.4, 114.6, GZ + 3.6, *yp((GX + 3.4, 114.6, GZ + 3.6), (GX + .5, 113.0, GZ + .5))),
                    (GX + 3.2, 114.5, GZ + 3.4, *yp((GX + 3.2, 114.5, GZ + 3.4), (GX + .5, 113.0, GZ + .5)))]


def t_come():
    estado = {'ult': g()}

    def cond():
        if g() == 'dirt':
            return 'comeu'
    esperar('l01_come', CAM_CELA(), cond, maxs=280, rate=100)
    print('tosada?', tosada(), g())


def t_maquina():
    C(f'setblock {GX} 112 {GZ} grass_block')  # grama volta (fora de cena)
    C(f'setblock {GX + 2} 110 {GZ} stone')  # apoio
    cam('l02', (GX + 5.6, 115.4, GZ + 4.4), (GX + 5.0, 115.1, GZ + 3.9), (GX + 1.2, 112.8, GZ + .5), 9000)

    def fn(ev):
        play('l02'); time.sleep(1.2)
        ev('pedra'); bloco(0, GX + 2, 111, GZ); time.sleep(0.25)
        ev('pedra'); bloco(0, GX + 2, 112, GZ); time.sleep(0.4)
        ev('observador'); bloco(6, GX + 1, 112, GZ, 'west', f'minecraft:observer[facing=west]'); time.sleep(0.6)
        ev('fio'); bloco(3, GX + 2, 113, GZ); time.sleep(0.5)
        ev('ejetor'); bloco(7, GX + 1, 113, GZ, 'east', f'minecraft:dispenser[facing=west]'); time.sleep(0.2)
        C(f'item replace block {GX + 1} 113 {GZ} container.4 with shears')
        ev('pronto')
    shot('l02_maquina', fn, 9.4, BL)
    print('ovelha tosada?', tosada())


def t_tosa():
    def cond():
        if tosada():
            return 'tosou'
    esperar('l03_tosa', CAM_CELA(), cond, maxs=280, depois=3.5, rate=100)
    print(g(), tosada())


def t_la_presa():
    cam('l04', (GX - 1.8, 114.4, GZ + 2.6), (GX - 1.5, 114.3, GZ + 2.3), (GX + .5, 112.9, GZ + .5), 6000)
    shot('l04_la_presa', lambda ev: play('l04'), 6.4, BL)


def t_carrinho():
    cam('l05', (GX + 1.4, 111.2, GZ + 4.6), (GX + 1.0, 111.1, GZ + 4.1), (GX + .6, 111.2, GZ + .5), 9000)

    def fn(ev):
        play('l05'); time.sleep(1.2)
        ev('bau'); bloco(4, GX + 1, 110, GZ, 'north', 'minecraft:chest[facing=south]'); time.sleep(0.6)
        ev('funil'); bloco(5, GX, 110, GZ, None, 'minecraft:hopper[facing=east]', pref='east'); time.sleep(0.6)
        C('item replace entity @J hotbar.6 with rail 8'); time.sleep(0.05)
        ev('trilho'); bloco(6, GX, 111, GZ, pref='down'); time.sleep(0.6)
        estacionar()
        ev('carrinho'); C(f'summon hopper_minecart {GX + .5} 111.1 {GZ + .5}')
        snd('minecraft:block.metal.place', GX + .5, 111, GZ + .5)
        t0 = time.time()
        while time.time() - t0 < 4:
            o = C(f'execute positioned {GX + .5} 113 {GZ + .5} if entity @e[type=item,distance=..1.5]')['output']
            if 'failed' in str(o):
                ev('puxou'); break
            time.sleep(0.05)
    shot('l05_carrinho', fn, 9.4, BL)
    C('item replace entity @J hotbar.6 with observer 64')
    print('bau', C(f'data get block {GX + 1} 110 {GZ} Items')['output'])


def t_terra():
    cam('l06', (GX + 2.6, 114.0, GZ + 2.9), (GX + 2.4, 113.9, GZ + 2.7), (GX + .5, 112.6, GZ + .5), 6000)
    shot('l06_terra', lambda ev: play('l06'), 6.4, BL)


def t_grama():
    cam('l07', (GX - 3.0, 114.8, GZ + 4.0), (GX - 2.6, 114.6, GZ + 3.6), (GX + .2, 112.5, GZ + .4), 12000)

    def fn(ev):
        play('l07'); time.sleep(1.2)
        for p in modulo(GX, GZ)['anel']:
            ev('grama'); bloco(2, *p); time.sleep(0.45)
        time.sleep(0.5); C('gamerule randomTickSpeed 400'); ev('acelerado')
        t0 = time.time()
        while time.time() - t0 < 8:
            if g() == 'grass_block':
                ev('voltou'); C('gamerule randomTickSpeed 3'); break
            time.sleep(0.05)
        C('gamerule randomTickSpeed 3')
    shot('l07_grama', fn, 12.4, BL)
    print('G', g())


def t_ciclo():
    """grama de volta: espera comer -> tosar -> la vai para o bau"""
    def cond():
        if tosada() is False and g() == 'grass_block':
            return None
        if tosada() and g() == 'dirt':
            return 'tosou'
    print('antes', tosada(), g())
    esperar('l08_ciclo', CAM_CELA(), cond, maxs=280, depois=3.0, rate=100)
    print('bau', C(f'data get block {GX + 1} 110 {GZ} Items')['output'])


def mod_completo(gx, gz, cor):
    S = [(f'{gx} 110 {gz}', 'hopper[facing=east]'), (f'{gx + 1} 110 {gz}', 'chest[facing=south]'), (f'{gx} 111 {gz}', 'rail'),
         (f'{gx + 2} 110 {gz}', 'stone'), (f'{gx + 2} 111 {gz}', 'stone'), (f'{gx + 2} 112 {gz}', 'stone'),
         (f'{gx} 112 {gz}', 'grass_block'), (f'{gx + 1} 112 {gz}', 'observer[facing=west]'),
         (f'{gx + 2} 113 {gz}', 'redstone_wire[north=side,south=side,east=side,west=side]'), (f'{gx + 1} 113 {gz}', 'dispenser[facing=west]')]
    S += [('%d %d %d' % p, 'grass_block') for p in modulo(gx, gz)['anel']]
    S += [('%d %d %d' % p, 'glass') for p in modulo(gx, gz)['vidro']]
    for p, b in S:
        C(f'setblock {p} {b}')
    C(f'summon hopper_minecart {gx + .5} 111.1 {gz + .5}')
    C(f'summon sheep {gx + .5} 113 {gz + .5} {{Color:{cor}b,PersistenceRequired:1b}}')
    PEND.append((gx, gz))
    snd('minecraft:block.glass.place', gx + .5, 113, gz + .5)


PEND = []


def tesouras_pend():
    time.sleep(1.0)
    for gx, gz in PEND:
        C(f'item replace block {gx + 1} 113 {gz} container.4 with shears')
    PEND.clear()


POS = [(gx, gz) for gz in (201, 206) for gx in range(18, 49, 4)]  # 16 modulos


def t_escala():
    # camera de grua passando pelas duas fileiras
    cam('l09', (18.0, 118.0, 212.0), (36.0, 119.0, 212.5), (24.0, 112.8, 203.5), 12000, (42.0, 112.8, 203.5))
    ordem = [p for p in POS if p != (GX, GZ)]
    ordem.sort(key=lambda p: (p[0], p[1]))

    def fn(ev):
        play('l09'); time.sleep(0.8)
        cores = [c for c in range(16) if c != COR_DEMO]
        for k, (gx, gz) in enumerate(ordem):
            ev('modulo'); mod_completo(gx, gz, cores[k]); time.sleep(0.55)
    shot('l09_escala', fn, 12.4, BL)
    tesouras_pend()


def t_orbita():
    pts = []
    for ang in (35, 0, -35):
        a = math.radians(ang); c = (33 + 13 * math.sin(a), 119.5, 203.5 + 13 * math.cos(a))
        pts.append((round(c[0], 2), c[1], round(c[2], 2), *yp(c, (33, 112.5, 203.5))))
    scene('l10', pts, 13000)
    shot('l10_orbita', lambda ev: play('l10'), 13.4, BL)


def t_linha():
    cam('l11', (17.0, 115.2, 208.6), (30.0, 115.2, 208.6), (22.0, 113.0, 206.0), 10000, (35.0, 113.0, 206.0))
    shot('l11_linha', lambda ev: play('l11'), 10.4, BL)


if __name__ == '__main__':
    os.makedirs(BL, exist_ok=True)
    for t in sys.argv[1:]:
        if t == 'kit':
            kit()
        elif t == 'inicio':
            inicio()
        else:
            globals()['t_' + t]()
        time.sleep(0.8)
