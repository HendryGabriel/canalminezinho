"""Colocacao com orientacao certa (jogador invisivel posicionado e olhando na direcao certa)."""
from fl import *

YAW = {'south': 0, 'west': 90, 'north': 180, 'east': -90}
OPP = {'south': 'north', 'north': 'south', 'east': 'west', 'west': 'east', 'up': 'down', 'down': 'up'}
VEC = {'south': (0, 0, 1), 'north': (0, 0, -1), 'east': (1, 0, 0), 'west': (-1, 0, 0), 'up': (0, 1, 0), 'down': (0, -1, 0)}
SOLID_SKIP = ('minecraft:air', 'minecraft:water', 'minecraft:short_grass', 'minecraft:cave_air')


def apoio(x, y, z, pref=None):
    """acha um vizinho solido para clicar. devolve (bx,by,bz,face)"""
    ordem = ([pref] if pref else []) + ['down', 'north', 'south', 'east', 'west', 'up']
    for d in ordem:
        v = VEC[d]
        b = st(x + v[0], y + v[1], z + v[2])['id']
        if b not in SOLID_SKIP and 'redstone_wire' not in b and 'flower' not in b:
            return x + v[0], y + v[1], z + v[2], OPP[d]
    return None


def olhar(direcao, x, y, z, dist=2.6):
    """posiciona o jogador para olhar na 'direcao' ate o bloco (x,y,z)"""
    if direcao in ('up', 'down'):
        py = y + 0.5 - (dist if direcao == 'up' else -dist) - 1.62
        tpme(x + 0.5, round(py, 2), z + 0.5, 0, -90 if direcao == 'up' else 90)
        return
    v = VEC[direcao]
    px, pz = x + 0.5 - v[0] * dist, z + 0.5 - v[2] * dist
    tpme(round(px, 2), y - 0.6, round(pz, 2), YAW[direcao], 15)


def bloco(slot, x, y, z, olhar_para=None, fix=None, pref=None, sneak=True):
    """olhar_para = direcao do olhar do jogador ao colocar (define a orientacao)."""
    if olhar_para:
        olhar(olhar_para, x, y, z)
    else:
        tpme(x + 0.5, y + 1.2, z + 3.0, 180, 30)
    time.sleep(0.12)
    a = apoio(x, y, z, pref)
    if not a:
        print('SEM APOIO', x, y, z); return None
    r = place(slot, a[0], a[1], a[2], a[3], sneak)
    if fix:
        time.sleep(0.15)
        s = state(x, y, z)
        if s.split('[')[0] != fix.split('[')[0] or (('[' in fix) and any(p not in s for p in fix.split('[')[1].rstrip(']').split(','))):
            C(f'setblock {x} {y} {z} {fix}')
            print('FIX', x, y, z, s, '->', fix)
    return r
