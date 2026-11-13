"""Helpers do projeto shorts-farms (ponte MCP Fabric + CinematicTools + gravacao)."""
import sys, time, json, os, math, ctypes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc, keys, focus, rec

# --- configuracao (variaveis de ambiente) ---
P = os.environ.get('SHORTS_PROJETO', os.getcwd())          # pasta do video (brutos/, tmp/, final/)
OPT = os.environ.get('MC_OPTIONS', '')                      # options.txt da instancia (ler pauseOnLostFocus)
JOGADOR = os.environ.get('MC_JOGADOR', 'Jogador')           # seu nick no Minecraft (@J nos comandos)
JANELA_X = int(os.environ.get('MC_JANELA_X', '0'))          # x da janela 608x1080 (monitor onde ela cabe inteira)
G = 110  # primeiro bloco acima da grama (grama em y=109)


V26 = True  # instancia Video Maker (26.3): gamerules em snake_case
GR = {'sendCommandFeedback': 'send_command_feedback', 'doDaylightCycle': 'advance_time', 'doWeatherCycle': 'advance_weather',
      'randomTickSpeed': 'random_tick_speed', 'doMobSpawning': 'spawn_mobs'}


def C(c, show=False):
    c = c.replace('@J', JOGADOR)
    if V26 and c.startswith('gamerule '):
        for a, b in GR.items():
            c = c.replace('gamerule ' + a + ' ', 'gamerule ' + b + ' ')
    if V26 and c.startswith(f'effect give {JOGADOR} invisibility'):
        mc.cmd(f'effect clear {JOGADOR} invisibility')
    r = mc.cmd(c)
    if show or (isinstance(r, dict) and not r.get('success', True)):
        print(c, '->', r.get('output') if isinstance(r, dict) else r)
    return r


def st(x, y, z):
    return mc.call('world.getBlock', {'x': x, 'y': y, 'z': z})


def state(x, y, z):
    r = mc.call('world.getBlocks', {'from': {'x': x, 'y': y, 'z': z}, 'to': {'x': x, 'y': y, 'z': z}, 'includeState': True, 'includeAir': True})
    return r['blocks'][0].get('state', r['blocks'][0]['id'])


def give(slot, item, n=64):
    C(f'item replace entity @J hotbar.{slot} with {item} {n}')


def place(slot, bx, by, bz, face='up', sneak=False):
    """coloca o item do slot clicando no bloco VIZINHO (bx,by,bz) na face indicada (anima com A Good Place)"""
    mc.call('inventory.selectHotbar', {'slot': slot}); time.sleep(0.08)
    if sneak:
        mc.call('control.setInput', {'sneak': True}); time.sleep(0.12)
    r = mc.call('interact.placeBlock', {'x': bx, 'y': by, 'z': bz, 'face': face})
    if sneak:
        time.sleep(0.1); mc.call('control.setInput', {'sneak': False})
    mc.call('inventory.selectHotbar', {'slot': 8})
    return r.get('result') if isinstance(r, dict) else r


FACE = {'up': (0, 1, 0), 'down': (0, -1, 0), 'north': (0, 0, -1), 'south': (0, 0, 1), 'east': (1, 0, 0), 'west': (-1, 0, 0)}


def put(slot, x, y, z, face='up', sneak=False, fix=None):
    """coloca bloco em (x,y,z) clicando no vizinho do lado oposto a 'face'. fix=estado exato (corrige se o jogo orientar diferente)"""
    d = FACE[face]
    r = place(slot, x - d[0], y - d[1], z - d[2], face, sneak)
    if fix:
        time.sleep(0.12)
        s = state(x, y, z)
        if s != fix:
            C(f'setblock {x} {y} {z} {fix}')
            return (r, 'FIX', s)
    return r


def estacionar():
    C('tp @J 32.5 109 236.5 180 0')


def tpme(x, y, z, yaw=0, pitch=30):
    C(f'tp @J {x} {y} {z} {yaw} {pitch}')


def yp(c, t):
    dx, dy, dz = t[0] - c[0], t[1] - c[1], t[2] - c[2]
    yaw = math.degrees(math.atan2(-dx, dz))
    pitch = -math.degrees(math.atan2(dy, math.hypot(dx, dz)))
    return round(yaw, 2), round(pitch, 2)


def scene(name, pts, dur, mode='outside', interp='hermite'):
    C(f'cinematic-server remove {name}')
    C(f'cinematic-server create {name}')
    pts = [list(p) for p in pts]
    for i in range(1, len(pts)):
        while pts[i][3] - pts[i - 1][3] > 180: pts[i][3] -= 360
        while pts[i][3] - pts[i - 1][3] < -180: pts[i][3] += 360
    for p in pts:
        C(f'cinematic-server get {name} add {p[0]} {p[1]} {p[2]} {p[3]} {p[4]}')
    C(f'cinematic-server get {name} mode {mode}')
    C(f'cinematic-server get {name} interpolation {interp}')
    C(f'cinematic-server get {name} duration {int(dur)}ms')


def cam(name, a, b, target, dur, target_b=None):
    """camera de a ate b (posicoes) olhando para target (ou target->target_b)"""
    tb = target_b or target
    pa = (*a, *yp(a, target)); pb = (*b, *yp(b, tb))
    scene(name, [pa, pb], dur)


def play(name):
    C('cinematic-server stop @J')
    return C(f'cinematic-server start {name} @J')


def hud_texto():
    """conta pixels brancos na faixa do aviso 'AI has control' (0 = escondido)"""
    from PIL import Image
    f = P + '/tmp_hud.png'; mc.shot(f)
    im = Image.open(f).convert('RGB').crop((150, 990, 460, 1030))
    return sum(1 for p in im.getdata() if p[0] > 200 and p[1] > 200 and p[2] > 200)


def f1():
    prev, ok = focus.focus(); time.sleep(0.3); focus.key(0x3B); time.sleep(0.1); focus.key(0x3B, True); time.sleep(0.3); focus.restore(prev)
    return ok


def snd(sound, x, y, z, vol=1.0, pitch=1.0):
    C(f'playsound {sound} block @a {x} {y} {z} {vol} {pitch}')


def pause_flag():
    return open(OPT).read().split('pauseOnLostFocus:')[1][:4]


def toggle_pause():
    prev, ok = focus.focus(); time.sleep(0.3); mc.call('screen.close'); time.sleep(0.3)
    focus.key(0x3D); time.sleep(0.15); focus.key(0x19); time.sleep(0.1); focus.key(0x19, True); time.sleep(0.15); focus.key(0x3D, True); time.sleep(1.2)
    focus.restore(prev)


def janela(retrato=True):
    if not retrato:
        keys.set_client(854, 480, JANELA_X + 100, 155); return
    keys.set_client(608, 1080); h = keys.hwnd(); u = ctypes.windll.user32

    class R(ctypes.Structure):
        _fields_ = [('l', ctypes.c_long), ('t', ctypes.c_long), ('r', ctypes.c_long), ('b', ctypes.c_long)]
    wr = R(); u.GetWindowRect(h, ctypes.byref(wr)); pt = (ctypes.c_long * 2)(0, 0); u.ClientToScreen(h, pt)
    u.SetWindowPos(h, 0, JANELA_X - (pt[0] - wr.l), -(pt[1] - wr.t), 0, 0, 0x1 | 0x4 | 0x10)


def preparar():
    mc.call('screen.close'); time.sleep(0.3)
    if pause_flag() == 'true':
        toggle_pause()
    janela(True)
    for c in ['gamerule sendCommandFeedback false', 'gamerule doDaylightCycle false', 'gamerule doWeatherCycle false',
              'time set 3000', 'weather clear', 'effect give @J invisibility infinite 0 true',
              'team add semnome', 'team modify semnome nametagVisibility never', 'team modify semnome seeFriendlyInvisibles false', 'team join semnome @J']:
        C(c)


def restaurar():
    for c in ['effect clear @J invisibility', 'team leave @J', 'team remove semnome', 'gamerule sendCommandFeedback true',
              'gamerule doDaylightCycle true', 'gamerule doWeatherCycle true', 'gamerule randomTickSpeed 3', 'tick rate 20',
              'cinematic-server clear', 'clear @J', 'tp @J 24.49 112 207.3 -8.4 10.65']:
        C(c)
    if pause_flag() != 'true':
        toggle_pause()
    janela(False)


B = P + r'\brutos'


def shot(nome, fn, total, pasta=None, maxs=300):
    """grava um plano: fn(ev) roda as acoes; total = segundos de gravacao"""
    out = os.path.join(pasta or B, nome)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    R = rec.Rec(out, maxs)
    t0 = time.time(); R.ev('inicio')
    fn(R.ev)
    rest = total - (time.time() - t0)
    if rest > 0:
        time.sleep(rest)
    R.ev('fim')
    print(nome, R.stop().strip())
    return out
