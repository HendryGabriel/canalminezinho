"""Cenas de historia da LA e da ALGA (26.3). uso: hist2.py <cena> [...]"""
from hist import *

ROSTO = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rosto.json')))
WX0, WY1, WZ = 20, 141, 247  # parede: x 20..51, y 110..141, la em z=246 (face norte), fundo em z=247
ESC = 4
CX = 35.5  # centro da parede
CAMZ = 203.0  # camera longe (vertical 9:16 precisa de ~42 blocos para caber a parede)


def pix(bx, by):
    return ROSTO[by // ESC][bx // ESC]


def wx(bx):  # vista do norte: x cresce para a esquerda da tela
    return WX0 + 31 - bx


def parede_moldura():
    C(f'fill {WX0 - 1} 109 {WZ - 2} {WX0 + 32} {WY1 + 2} {WZ + 1} air')
    C(f'fill {WX0 - 1} 109 {WZ} {WX0 + 32} {WY1 + 1} {WZ} birch_planks')
    C(f'fill {WX0 - 1} {WY1 + 2} {WZ - 2} {WX0 + 32} {WY1 + 2} {WZ} dark_oak_slab')  # beiral (protege da chuva)
    C(f'fill {WX0 - 1} 109 {WZ - 1} {WX0 + 32} 109 {WZ - 1} dark_oak_log[axis=x]')


def linha(by, filtro=None):
    y = WY1 - by; bx = 0
    while bx < 32:
        c = pix(bx, by); e = bx
        while e + 1 < 32 and pix(e + 1, by) == c: e += 1
        if filtro is None or filtro(c):
            C(f'fill {wx(e)} {y} {WZ - 1} {wx(bx)} {y} {WZ - 1} {c}_wool')
        bx = e + 1


def parede(modo='vazia', linhas=32):
    """modo: vazia | sem_marrom | completa"""
    parede_moldura()
    if modo == 'vazia':
        return
    for by in range(min(32, linhas)):
        linha(by, (lambda c: c != 'brown') if modo == 'sem_marrom' else None)


def cam_parede(z0=CAMZ, z1=CAMZ + 3, y0=125.5, y1=125.5, dur=6.0):
    a = olhando((CX, y0, z0), (CX, 125.5, WZ)); b = olhando((CX, y1, z1), (CX, 125.5, WZ))
    return [a, b]


def l_s1():
    parede('vazia')
    for by in range(28, 32):  # so as 4 linhas de baixo comecadas
        for bx in range(0, 12):
            C(f'setblock {wx(bx)} {WY1 - by} {WZ - 1} {pix(bx, by)}_wool')
    heroi(37.5, 110, 241.5, 0, 'white_wool')
    pts = [olhando((39.0, 111.4, 236.0), (37.5, 111.6, 241.5)), olhando((CX, 124.0, 212.0), (CX, 125.5, WZ))]
    rig_criar(39, 111, 236)
    gravar('L_s1_parede', lambda ev: cam_path(pts, 6.0), 6.3)


def l_s2():
    C('fill 10 110 204 16 112 210 air'); C('fill 10 110 204 16 110 210 oak_fence'); C('fill 11 110 205 15 110 209 air')
    C('kill @e[type=sheep,x=13,y=110,z=207,distance=..5]')
    for i, cor in enumerate([0, 0, 0]):
        C(f'summon sheep {12 + i * 1.2:.1f} 110 {207.5} {{Color:0b,PersistenceRequired:1b,Tags:["ov{i}"],NoAI:1b,Rotation:[90f,0f]}}')
    heroi(13.3, 110, 205.6, 0, 'shears')
    pts = [olhando((17.0, 111.6, 203.0), (13.0, 110.8, 207.0)), olhando((16.3, 111.4, 203.8), (13.0, 110.8, 207.0))]
    rig_criar(17, 111, 203)

    def fn(ev):
        def acao():
            for i in range(3):
                time.sleep(1.1)
                C(f'data merge entity @e[tag=ov{i},limit=1] {{Sheared:1b}}'); snd('minecraft:entity.sheep.shear', 13, 110.5, 207.5)
                for k in range(2):
                    C(f'summon item {12 + i * 1.2:.1f} 110.8 207.5 {{Item:{{id:"minecraft:white_wool",count:1}},Motion:[{random.uniform(-.1, .1):.2f},0.25,{random.uniform(-.1, .1):.2f}],PickupDelay:32767}}')
                ev('tosa')
        cam_path(pts, 5.0, acao)
    gravar('L_s2_tosa', fn, 5.3)
    C('kill @e[type=item,x=13,y=110,z=207,distance=..5]')


def l_s3():
    parede('vazia'); heroi(CX, 110, 240.0, 0)
    pts = cam_parede(CAMZ + 4, CAMZ + 1)
    rig_criar(CX, 125, CAMZ + 4)

    def fn(ev):
        def acao():
            for by in range(31, -1, -1):
                linha(by, lambda c: c != 'brown')
                if by % 2 == 0: snd('minecraft:block.wool.place', CX, WY1 - by, WZ - 2, 1.0, 1.0)
                time.sleep(0.11)
            ev('sem_marrom')
        cam_path(pts, 6.5, acao)
    gravar('L_s3_sem_marrom', fn, 6.8)


def selva():
    x, z = 56, 196
    C(f'fill {x - 3} 110 {z - 3} {x + 3} 122 {z + 3} air')
    C(f'fill {x} 110 {z} {x} 119 {z} jungle_log')
    C(f'fill {x - 3} 118 {z - 3} {x + 3} 120 {z + 3} jungle_leaves[persistent=true] replace air')
    C(f'fill {x - 2} 121 {z - 2} {x + 2} 121 {z + 2} jungle_leaves[persistent=true] replace air')
    for y, f in [(112, 'south'), (114, 'west'), (113, 'east'), (115, 'south')]:
        d = {'south': (0, 1), 'west': (-1, 0), 'east': (1, 0)}[f]
        opp = {'south': 'north', 'west': 'east', 'east': 'west'}[f]
        C(f'setblock {x + d[0]} {y} {z + d[1]} cocoa[age=2,facing={opp}]')
    for dx, dz in [(-3, 2), (3, -2), (-2, -3), (2, 3)]:
        C(f'setblock {x + dx} 110 {z + dz} fern')


def l_s4():
    selva(); heroi(56.5, 110, 199.6, 180)
    pts = [olhando((59.5, 111.0, 202.5), (56.5, 112.5, 197.0)), olhando((59.0, 113.5, 202.0), (56.5, 113.5, 197.0))]
    rig_criar(59, 111, 202)

    def fn(ev):
        def acao():
            time.sleep(1.8); C('setblock 56 112 197 air'); snd('minecraft:block.wood.break', 56.5, 112.5, 197.5)
            C('summon item 56.5 112.3 197.6 {Item:{id:"minecraft:cocoa_beans",count:3},PickupDelay:32767,Motion:[0.0,0.2,0.1]}'); ev('cacau')
        cam_path(pts, 3.6, acao)
    gravar('L_s4_cacau', fn, 3.9)


def l_s5():
    parede('sem_marrom'); heroi(CX, 110, 240.0, 0)
    pts = cam_parede(CAMZ + 12, CAMZ, 120.0, 125.5)
    rig_criar(CX, 120, CAMZ + 12)

    def fn(ev):
        def acao():
            time.sleep(0.4)
            cel = [(bx, by) for by in range(32) for bx in range(32) if pix(bx, by) == 'brown']
            random.shuffle(cel)
            for i in range(0, len(cel), 12):
                for bx, by in cel[i:i + 12]:
                    C(f'setblock {wx(bx)} {WY1 - by} {WZ - 1} brown_wool')
                snd('minecraft:block.wool.place', CX, 125, WZ - 2)
                time.sleep(0.06)
            ev('completa')
        cam_path(pts, 5.5, acao)
    gravar('L_s5_completa', fn, 5.8)


def l_s6():
    parede('completa'); heroi(CX, 110, 238.0, 0)
    C('weather thunder'); C('time set 13000')
    pts = cam_parede(CAMZ + 2, CAMZ + 4)
    rig_criar(CX, 125, CAMZ + 2)

    def fn(ev):
        def acao():
            time.sleep(1.8); C(f'summon lightning_bolt 31.5 110 {WZ - 1.5}'); ev('raio')
        cam_path(pts, 4.0, acao)
    gravar('L_s6_raio', fn, 4.3)


def l_s7():
    """fogo real se espalhando (acelerado), continuacao do raio"""
    pts = cam_parede(CAMZ + 4, CAMZ + 7)
    rig_criar(CX, 125, CAMZ + 4)

    def fn(ev):
        def acao():
            C('tick rate 60'); ev('acelerado'); time.sleep(7.0); C('tick rate 20'); ev('fim_acel')
        cam_path(pts, 9.0, acao)
    gravar('L_s7_fogo', fn, 9.3)


def l_s8():
    """Steve olhando a parede queimada, sorri e sai"""
    C('weather clear'); C('time set 3000')
    heroi(CX, 110, 240.0, 0)
    pts = [olhando((CX + 1.6, 111.6, 237.0), (CX, 111.6, 240.0)), olhando((CX + 3.0, 112.4, 235.0), (CX, 115.0, 245.0))]
    rig_criar(CX + 1, 111, 237)

    def fn(ev):
        def acao():
            time.sleep(1.6); andar(CX - 4, 232.0, 2.6)
        cam_path(pts, 4.5, acao)
    gravar('L_s8_sai', fn, 4.8)


# ---------------- ALGA ----------------
EST = (2, 222, 13, 234)  # estufa


def estufa(frac=0.4, areia=True):
    x0, z0, x1, z1 = EST
    C(f'fill {x0 - 1} 110 {z0 - 1} {x1 + 1} 118 {z1 + 1} air')
    C(f'fill {x0} 109 {z0} {x1} 109 {z1} polished_andesite')
    alt = max(1, int(round(6 * frac)))
    for y in range(110, 110 + alt):
        C(f'fill {x0} {y} {z0} {x1} {y} {z1} glass'); C(f'fill {x0 + 1} {y} {z0 + 1} {x1 - 1} {y} {z1 - 1} air')
    if frac >= 1:
        C(f'fill {x0} 116 {z0} {x1} 116 {z1} glass')
        C(f'fill {x0 + 1} 117 {z0 + 1} {x1 - 1} 117 {z1 - 1} glass')
    for x, z in [(x0, z0), (x1, z0), (x0, z1), (x1, z1)]:
        C(f'fill {x} 110 {z} {x} {109 + (7 if frac >= 1 else alt)} {z} stripped_oak_log')
    C(f'fill {x0 + 5} 110 {z1} {x0 + 6} 111 {z1} air')
    if areia:
        C('fill 16 110 226 19 112 229 sand'); C('fill 17 113 227 18 113 228 sand'); C('fill 15 110 230 16 110 231 sand')


def a_s1():
    C('time set 3000'); estufa(0.35); heroi(9.0, 110, 236.0, 180, 'glass')
    pts = [olhando((22.5, 116.0, 220.0), (9.0, 111.0, 229.0)), olhando((20.0, 114.0, 222.0), (8.5, 111.0, 229.5))]
    rig_criar(22, 116, 220)
    gravar('A_s1_estufa', lambda ev: cam_path(pts, 5.0), 5.3)


def a_s2():
    x, z = 6, 216  # fornalha
    C(f'setblock {x} 110 {z} furnace[facing=south,lit=true]')
    C(f'item replace block {x} 110 {z} container.0 with sand 64')
    C(f'item replace block {x} 110 {z} container.1 with coal 12')
    heroi(x + .5, 110, z + 2.2, 180, 'coal')
    pts = [olhando((x + 2.6, 111.4, z + 3.0), (x + .5, 110.6, z + .5)), olhando((x + 2.0, 111.1, z + 2.2), (x + .5, 110.6, z + .5))]
    rig_criar(x + 2, 111, z + 3)
    gravar('A_s2_fornalha', lambda ev: cam_path(pts, 5.0), 5.3)


def mina():
    C('fill 4 96 239 16 99 241 air'); C('fill 3 95 238 17 95 242 stone')
    C('fill 3 100 238 17 100 242 stone'); C('fill 3 96 238 17 99 238 stone'); C('fill 3 96 242 17 99 242 stone')
    C('fill 17 96 239 17 99 241 stone')
    for x in (6, 11, 15):
        C(f'setblock {x} 98 239 wall_torch[facing=south]')
    for x, y in [(8, 96), (13, 99), (16, 97)]:
        C(f'setblock {x} {y} 242 coal_ore')


def a_s3():
    mina(); heroi(5.5, 96, 240.5, -90, 'iron_pickaxe')
    pts = [olhando((4.4, 97.6, 239.4), (9.0, 97.0, 240.5)), olhando((7.5, 97.6, 239.4), (13.0, 97.0, 240.5))]
    rig_criar(4, 97, 239)

    def fn(ev):
        andar_bg(14.5, 240.5, 2.4); cam_path(pts, 4.5)
    gravar('A_s3_mina', fn, 4.8)


def a_s4():
    C('time set 3000'); heroi(59.0, 110, 236.5, 90)
    pts = [olhando((61.5, 112.8, 233.0), (52.0, 106.0, 237.0)), olhando((55.0, 108.6, 236.5), (47.0, 105.0, 237.0))]
    rig_criar(61, 112, 233)
    gravar('A_s4_lagoa', lambda ev: cam_path(pts, 5.5), 5.8)


def a_s5():
    """noite -> manha na farm de alga (tempo real acelerado pelo /time)"""
    C('kill @e[type=mannequin,tag=heroi]'); C('time set 14000')
    pts = [olhando((49.5, 118.0, 218.0), (43.5, 114.0, 211.0)), olhando((48.5, 117.4, 217.0), (43.5, 114.0, 211.0))]
    rig_criar(49, 118, 218)

    def fn(ev):
        def acao():
            time.sleep(0.8)
            for t in range(14000, 24001, 250):
                C(f'time set {t}'); time.sleep(0.05)
            ev('manha')
        cam_path(pts, 4.5, acao)
    gravar('A_s5_noite', fn, 4.8)
    C('time set 1000')


def a_s7():
    estufa(1.0, areia=False); C('kill @e[type=mannequin,tag=heroi]'); C('time set 11800')
    heroi(7.5, 110, 237.0, 180)
    pts = []
    pts = [olhando((7.5, 128.0, 252.0), (7.5, 112, 228)), olhando((7.5, 122.0, 246.0), (7.5, 112, 228))]
    rig_criar(7, 128, 252)
    gravar('A_s7_estufa_pronta', lambda ev: cam_path(pts, 6.0), 6.3)


def a_s8():
    C('time set 12300'); time.sleep(1.5)
    x0, z0, x1, z1 = EST
    pos = [(x0 - 1, z0 + 2), (x0 - 1, z1 - 2), (x1 + 1, z0 + 2), (x1 + 1, z1 - 2), (x0 + 3, z1 + 1), (x0 + 8, z1 + 1), (x0 + 3, z0 - 1), (x0 + 8, z0 - 1)]
    pts = [olhando((7.5, 114.5, 245.5), (7.5, 111.5, 230.0)), olhando((7.5, 114.0, 243.0), (7.5, 111.5, 230.0))]
    rig_criar(7, 114, 245)

    def fn(ev):
        def acao():
            time.sleep(0.8)
            for x, z in pos:
                C(f'setblock {x} 110 {z} torch'); snd('minecraft:block.wood.place', x, 110, z); time.sleep(0.3)
        cam_path(pts, 4.0, acao)
    gravar('A_s8_tochas', fn, 4.3)


if __name__ == '__main__':
    os.makedirs(BH, exist_ok=True)
    for t in sys.argv[1:]:
        globals()[t]()
        time.sleep(0.5)
    rig_fim()
