"""Cenas de historia (Minecraft 26.3, instancia Video Maker). uso: hist.py <cena> [...]"""
import json, random
import cam26
from cam26 import *
from heroi import *

BH = P + r'\brutos\hist'
cam26.TDUR = 4; cam26.LEAD = 0.2
ITENS = ['cobblestone', 'iron_ingot', 'oak_log', 'coal', 'wheat', 'redstone']
BAUS = [(4, 110, 191), (8, 110, 190), (12, 110, 191), (4, 110, 197), (8, 110, 198), (12, 110, 197)]
CC = (8, 110, 194)  # bau de cobre
GOL = [(6, 110, 193), (10, 110, 193), (6, 110, 196), (10, 110, 196), (5, 110, 194), (11, 110, 195)]


def gravar(nome, fn, total):
    return shot(nome, fn, total, BH)


def camfix(c, alvo):
    p = olhando(c, alvo); return [p, p]


# ---------------- MEL ----------------
def deposito(golens='vivos', baguncado=False):
    C('tp @e[type=copper_golem] ~ -80 ~'); C('kill @e[type=item,x=8,y=110,z=194,distance=..12]'); time.sleep(0.5)
    C('fill 1 110 187 15 116 201 air')
    C('fill 1 109 187 15 109 201 spruce_planks')
    C('fill 1 110 187 15 113 187 spruce_planks'); C('fill 1 110 188 1 113 201 spruce_planks'); C('fill 15 110 188 15 113 201 spruce_planks')
    for x in (1, 15):
        for z in (187, 194, 201):
            C(f'fill {x} 110 {z} {x} 113 {z} spruce_log')
    for x in (4, 8, 12):
        C(f'setblock {x} 112 188 lantern'); C(f'setblock {x} 111 188 spruce_planks')
    C(f'setblock {CC[0]} {CC[1]} {CC[2]} copper_chest[facing=south]')
    for (x, y, z), it in zip(BAUS, ITENS):
        C(f'setblock {x} {y} {z} chest[facing=south]'); C(f'item replace block {x} {y} {z} container.0 with {it} 16')
    for i, it in enumerate(ITENS * 2):
        C(f'item replace block {CC[0]} {CC[1]} {CC[2]} container.{i} with {it} 16')
    if golens == 'vivos':
        for k, (x, y, z) in enumerate(GOL):
            C(f'summon copper_golem {x + .5} {y} {z + .5} {{PersistenceRequired:1b,weather_state:"unaffected",next_weather_age:-2L}}')
    elif golens == 'estatua':
        poses = ['running', 'standing', 'sitting', 'running', 'star', 'standing']
        for (x, y, z), ps in zip(GOL, poses):
            C(f'setblock {x} {y} {z} oxidized_copper_golem_statue[copper_golem_pose={ps},facing={random.choice(["south", "east", "west"])}]')
    if baguncado:
        random.seed(3)
        for _ in range(26):
            it = random.choice(ITENS)
            C(f'summon item {random.uniform(3, 13):.2f} 110.2 {random.uniform(189, 199):.2f} {{Item:{{id:"minecraft:{it}",count:{random.randint(1, 16)}}},PickupDelay:32767,Age:-32768}}')


def m_s1():
    deposito('vivos'); heroi(8.5, 110, 196.0, 180, 'cobblestone')
    time.sleep(6)  # golens comecam a trabalhar
    pts = [olhando((8.5, 116.5, 205.5), (8.5, 110.6, 194.5)), olhando((8.5, 114.2, 202.0), (8.5, 110.5, 194.0)), olhando((11.5, 112.6, 200.0), (8.5, 110.6, 194.5))]
    rig_criar(8, 116, 205)

    def fn(ev):
        def acao():
            time.sleep(2.0); C('playsound minecraft:block.copper.place block @a 8 110 194')
            for i in range(3):
                C(f'summon item 8.5 111.2 195.4 {{Item:{{id:"minecraft:{ITENS[i]}",count:8}},Motion:[0.0,0.15,-0.12],PickupDelay:32767}}'); time.sleep(0.25)
        cam_path(pts, 8.0, acao)
    gravar('M_s1_deposito', fn, 8.3)


def m_s2():
    deposito('estatua', baguncado=True); heroi(8.5, 110, 205.5, 180)
    pts = [olhando((11.0, 111.4, 207.0), (8.5, 111.2, 203.0)), olhando((10.5, 111.7, 201.0), (7.5, 110.6, 195.5))]
    rig_criar(11, 111, 207)

    def fn(ev):
        andar_bg(8.5, 199.5, 2.2); cam_path(pts, 7.0)
    gravar('M_s2_caos', fn, 7.3)


def m_s3():
    C('kill @e[type=copper_golem]')
    x, y, z = 6, 110, 196
    C(f'setblock {x} {y} {z} air')
    C(f'summon copper_golem {x + .5} {y} {z + .5} {{Tags:["g1"],NoAI:1b,Rotation:[0f,0f],weather_state:"unaffected",PersistenceRequired:1b}}')
    pts = camfix((x + .5 + 0.4, y + 1.05, z + .5 + 2.1), (x + .5, y + 0.55, z + .5))
    pts = [pts[0], olhando((x + .5 + 0.2, y + 0.9, z + .5 + 1.6), (x + .5, y + 0.55, z + .5))]
    rig_criar(x, y + 1, z + 3)

    def fn(ev):
        def acao():
            for ws, t in [('exposed', 1.1), ('weathered', 1.1), ('oxidized', 1.3)]:
                time.sleep(t); C(f'data merge entity @e[tag=g1,limit=1] {{weather_state:"{ws}"}}'); ev(ws)
            time.sleep(1.0)
            C('kill @e[tag=g1]'); C(f'setblock {x} {y} {z} oxidized_copper_golem_statue[copper_golem_pose=standing,facing=south]')
            snd('minecraft:block.copper.place', x + .5, y + .5, z + .5); ev('estatua')
        cam_path(pts, 6.0, acao)
    gravar('M_s3_oxida', fn, 6.3)


def m_s4():
    x, y, z = 6, 110, 196
    C(f'setblock {x} {y} {z} oxidized_copper_golem_statue[copper_golem_pose=standing,facing=south]')
    heroi(x + 1.6, y, z + 1.4, 135, 'iron_axe')
    pts = [olhando((x - 1.2, y + 1.6, z + 3.4), (x + .9, y + .8, z + .9)), olhando((x - 0.8, y + 1.5, z + 3.0), (x + .9, y + .8, z + .9))]
    rig_criar(x - 1, y + 1, z + 3)

    def fn(ev):
        def acao():
            for est in ['weathered_', 'exposed_', '']:
                time.sleep(1.0)
                C(f'setblock {x} {y} {z} {est}copper_golem_statue[copper_golem_pose=standing,facing=south]')
                snd('minecraft:item.axe.scrape', x + .5, y + .5, z + .5)
                C(f'particle minecraft:scrape {x + .5} {y + .6} {z + .5} 0.4 0.4 0.4 1 12')
                ev('raspa')
            time.sleep(0.9)
            C(f'setblock {x} {y} {z} air'); snd('minecraft:item.axe.scrape', x + .5, y + .5, z + .5)
            C(f'summon copper_golem {x + .5} {y} {z + .5} {{Rotation:[180f,0f],PersistenceRequired:1b}}'); ev('vivo')
        cam_path(pts, 5.5, acao)
    gravar('M_s4_raspa', fn, 5.8)


def m_s5():
    deposito('vivos'); C('kill @e[type=mannequin,tag=heroi]')
    time.sleep(8)
    pts = [olhando((2.8, 113.5, 199.5), (8, 110.5, 193)), olhando((13.2, 113.5, 199.5), (8, 110.5, 193))]
    rig_criar(3, 113, 199)
    gravar('M_s5_golens', lambda ev: cam_path(pts, 7.0), 7.3)


def m_s7():
    x, z = 15, 238  # arvore com ninho em (15,113,237)
    C('kill @e[type=bee]')
    heroi(15.5, 110, 235.6, 180, 'shears')
    pts = [olhando((18.8, 112.0, 232.0), (15.5, 112.0, 236.2)), olhando((18.0, 111.6, 232.8), (15.5, 111.6, 236.0))]
    rig_criar(18, 111, 232)
    o = C('data get entity @e[type=mannequin,tag=heroi,limit=1] UUID')['output'][0]
    arr = '[I;' + o.split('[I;')[1].split(']')[0] + ']'

    def fn(ev):
        def acao():
            time.sleep(1.6); snd('minecraft:block.beehive.shear', 15.5, 113.5, 236.8); ev('tesoura')
            for k in range(5):
                C(f'summon bee {15.5 + random.uniform(-.6, .6):.2f} 113.6 {236.4:.2f} {{AngerTime:800,AngryAt:{arr},PersistenceRequired:1b}}')
                time.sleep(0.12)
            time.sleep(1.8); andar(15.5, 230.0, 3.2)
        cam_path(pts, 6.5, acao)
    gravar('M_s7_abelhas', fn, 6.8)


def m_s9():
    deposito('vivos'); C('tp @e[type=copper_golem] ~ -80 ~')
    x, y, z = 6, 110, 196
    C(f'summon copper_golem {x + .5} {y} {z + .5} {{Tags:["g1"],NoAI:1b,Rotation:[0f,0f],PersistenceRequired:1b}}')
    heroi(x + .5, y, z + 1.7, 180, 'honeycomb')
    pts = [olhando((x + 2.4, y + 1.3, z + 1.9), (x + .5, y + .7, z + .9)), olhando((x + 2.2, y + 1.2, z + 1.5), (x + .5, y + .7, z + .9))]
    rig_criar(x + 2, y + 1, z + 2)

    def fn(ev):
        def acao():
            time.sleep(1.2); snd('minecraft:item.honeycomb.wax_on', x + .5, y + .5, z + .5)
            C(f'particle minecraft:wax_on {x + .5} {y + .6} {z + .5} 0.35 0.45 0.35 1 25'); ev('cera')
            C(f'data merge entity @e[tag=g1,limit=1] {{next_weather_age:-2L}}')
        cam_path(pts, 3.5, acao)
    gravar('M_s9_cera', fn, 3.8)


def m_s10():
    deposito('vivos'); C('kill @e[type=mannequin,tag=heroi]')
    C(f'data merge block {CC[0]} {CC[1]} {CC[2]} {{Items:[]}}')
    for i in range(10):
        C(f'item replace block {CC[0]} {CC[1]} {CC[2]} container.{i} with honeycomb 16')
    C('setblock 8 110 198 chest[facing=south]'); C('item replace block 8 110 198 container.0 with honeycomb 1')
    time.sleep(5)
    pts = []
    for ang in (40, 0, -40):
        a = math.radians(ang); c = (8 + 7 * math.sin(a), 114.5, 194 + 7 * math.cos(a)); pts.append(olhando(c, (8, 110.6, 194)))
    rig_criar(8, 114, 201)
    gravar('M_s10_final', lambda ev: cam_path(pts, 9.0), 9.3)


def m_funil26():
    C('kill @e[type=mannequin,tag=heroi]'); C('tp @e[type=bee] ~ -80 ~')
    C('setblock 23 110 211 copper_chest[facing=south]'); C('setblock 22 110 211 air')
    C('tp @e[type=item,x=22,y=111,z=211,distance=..8] ~ -80 ~')
    pts = [olhando((25.8, 111.4, 214.6), (22.6, 110.6, 211.4)), olhando((25.0, 111.2, 214.0), (22.6, 110.6, 211.4))]
    rig_criar(25, 111, 214)

    def fn(ev):
        def acao():
            time.sleep(1.2); C('setblock 22 110 211 hopper[facing=east]'); snd('minecraft:block.metal.place', 22.5, 110.5, 211.5); ev('funil')
            time.sleep(1.2); C('summon item 22.5 112.3 211.5 {Item:{id:"minecraft:honeycomb",count:3},PickupDelay:0}'); ev('favo')
        cam_path(pts, 5.0, acao)
    gravar('M_funil26', fn, 5.3)


if __name__ == '__main__':
    os.makedirs(BH, exist_ok=True)
    for t in sys.argv[1:]:
        globals()[t]()
        time.sleep(0.5)
    rig_fim()
