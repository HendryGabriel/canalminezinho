"""Protagonista (mannequin com skin Steve) para as cenas de historia."""
import math, time, threading
from fl import *

STEVE = 'profile:{texture:"entity/player/wide/steve"}'


def heroi(x, y, z, yaw=0, item=None, pose='standing'):
    C('kill @e[type=mannequin,tag=heroi]')
    eq = f',equipment:{{mainhand:{{id:"minecraft:{item}",count:1}}}}' if item else ''
    C(f'summon mannequin {x} {y} {z} {{Tags:["heroi"],hide_description:1b,Rotation:[{yaw}f,0f],pose:"{pose}",{STEVE}{eq}}}')


def mao(item=None):
    if item:
        C(f'item replace entity @e[type=mannequin,tag=heroi,limit=1] weapon.mainhand with minecraft:{item}')
    else:
        C('item replace entity @e[type=mannequin,tag=heroi,limit=1] weapon.mainhand with air')


def virar(yaw, pitch=0):
    C(f'data merge entity @e[type=mannequin,tag=heroi,limit=1] {{Rotation:[{yaw}f,{pitch}f]}}')


def pos():
    o = C('data get entity @e[type=mannequin,tag=heroi,limit=1] Pos')['output'][0]
    v = [float(a.strip().rstrip('d')) for a in o.split('[')[-1].rstrip(']').split(',')]
    return v


def andar(x, z, vel=4.3, timeout=12):
    """anda ate (x,z) aplicando velocidade a cada tick (a perna anima pelo deslocamento)."""
    t0 = time.time()
    while time.time() - t0 < timeout:
        p = pos(); dx, dz = x - p[0], z - p[2]; d = math.hypot(dx, dz)
        if d < 0.25:
            break
        s = min(vel / 20, d) / max(d, 1e-6)
        yaw = math.degrees(math.atan2(-dx, dz))
        C(f'data merge entity @e[type=mannequin,tag=heroi,limit=1] {{Motion:[{dx * s:.4f},-0.08,{dz * s:.4f}],Rotation:[{yaw:.1f}f,0f]}}')
        time.sleep(0.05)
    C('data merge entity @e[type=mannequin,tag=heroi,limit=1] {Motion:[0.0,-0.08,0.0]}')


def andar_bg(x, z, vel=4.3):
    th = threading.Thread(target=andar, args=(x, z, vel), daemon=True); th.start(); return th
