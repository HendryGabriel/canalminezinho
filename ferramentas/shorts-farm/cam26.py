"""Camera cinematografica para 26.3 (sem CinematicTools): jogador montado num block_display com
teleport_duration (o cliente interpola a posicao entre ticks) + rotacao suave no cliente (control.look a 60 Hz).
cam_path(pontos, dur): pontos = [(x,y,z,yaw,pitch), ...] interpolados em Catmull-Rom (hermite)."""
import math, time, threading
from fl import *

TAG = 'camrig'
EYE = 1.02  # altura do olho do jogador montado acima da base do display (ajustada em calibrar)
RIDE_OFF = 0.0
TDUR = 3
LEAD = 0.15


def rig_criar(x, y, z):
    C(f'kill @e[tag={TAG}]')
    C('summon block_display %s %s %s {Tags:["%s"],teleport_duration:%d,block_state:{Name:"minecraft:air"}}' % (x, y, z, TAG, TDUR))
    time.sleep(0.2)
    C('gamemode creative @J')
    C(f'ride @J mount @e[tag={TAG},limit=1]')


def rig_tp(x, y, z):
    C(f'tp @e[tag={TAG},limit=1] {x:.3f} {y:.3f} {z:.3f}')


def rig_fim():
    C('ride @J dismount'); C(f'kill @e[tag={TAG}]')


def _cr(p0, p1, p2, p3, t):
    t2, t3 = t * t, t * t * t
    return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


def amostra(pts, u):
    """u em [0,1] ao longo de todos os segmentos; ease in/out global"""
    u = u * u * (3 - 2 * u)
    n = len(pts) - 1
    if n == 0:
        return pts[0]
    s = min(n - 1e-9, u * n); i = int(s); t = s - i
    P = [pts[max(0, i - 1)], pts[i], pts[i + 1], pts[min(n, i + 2)]]
    out = []
    for k in range(5):
        vals = [p[k] for p in P]
        if k == 3:  # yaw: desenrola
            for j in range(1, 4):
                while vals[j] - vals[j - 1] > 180: vals[j] -= 360
                while vals[j] - vals[j - 1] < -180: vals[j] += 360
        out.append(_cr(*vals, t))
    return out


def cam_path(pts, dur, acoes=None):
    """roda a camera. acoes(t) chamada num thread separado (recebe nada)."""
    p0 = amostra(pts, 0)
    rig_tp(p0[0], p0[1] - EYE, p0[2]); mc.call('control.look', {'yaw': p0[3], 'pitch': p0[4]})
    time.sleep(0.3)
    stop = {'v': False}

    def girar():
        t0 = time.time()
        while not stop['v']:
            u = min(1.0, (time.time() - t0) / dur)
            p = amostra(pts, u)
            mc.call('control.look', {'yaw': p[3], 'pitch': p[4]})
            if u >= 1: break
            time.sleep(1 / 60)
    th = threading.Thread(target=girar, daemon=True); th.start()
    if acoes:
        ta = threading.Thread(target=acoes, daemon=True); ta.start()
    t0 = time.time()
    while True:
        u = min(1.0, (time.time() - t0 + LEAD) / dur)  # adianta a interpolacao do cliente
        p = amostra(pts, u)
        rig_tp(p[0], p[1] - EYE, p[2])
        if time.time() - t0 >= dur: break
        time.sleep(0.05)
    stop['v'] = True; th.join(1)


def olhando(c, alvo):
    return (*c, *yp(c, alvo))
