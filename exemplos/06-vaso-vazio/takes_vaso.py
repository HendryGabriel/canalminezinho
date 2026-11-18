r"""Gravacao deterministica em 30 fps dos 43 planos (P01..P43) de 'O Vaso Vazio' no Minecraft via MCP Fabric.
- Video: captura direta do framebuffer OpenGL (vision.screenshot) com /tick rate 3.4 (sub-tick liso, zero drop,
  pre-roll de velocidade para 0% de quadros iniciais repetidos), ja escalado em 1080x1920 + color grading -> tmp/seg/vXX.mp4.
- Audio in-game: mixagem exata dos arquivos .ogg oficiais do Minecraft (via minecraft/sounds.json do Modrinth) nos
  instantes reais de cada acao -> tmp/seg/aXX.wav.
Uso:
  python takes_vaso.py todos [--refazer]
  python takes_vaso.py P08 P14 --refazer
"""
import sys, os, time, math, random, json, base64, subprocess, http.client
import numpy as np

DIR_FERR = os.path.dirname(os.path.abspath(__file__))
if DIR_FERR not in sys.path:
    sys.path.insert(0, DIR_FERR)
_FERR_REPO = os.path.abspath(os.path.join(DIR_FERR, '..', '..', 'ferramentas', 'animacao-no-jogo'))
if os.path.isdir(_FERR_REPO) and _FERR_REPO not in sys.path:
    sys.path.insert(0, _FERR_REPO)

PROJ = os.environ.get('ANIM_PROJETO', os.getcwd())
os.environ['ANIM_PROJETO'] = PROJ

import mc
import motor as M
import montar_vaso as MV
from takes3 import Vel
from config_vaso import SET, Y, YP, YJ
from elenco import (
    PingCapivara, Rei, Rival, ModeloRico, posar_varios,
    criar_vaso, criar_regador, criar_panela_fervendo,
    criar_semente_hashi, criar_coroa_imperial
)

C = M.C
cam = M.Camera(tdur=2)

FPS = 30
TICK_RATE = 3.4
K_SLOW = 20.0 / TICK_RATE
DT_WALL = K_SLOW / FPS
TMP_SEG = os.path.join(PROJ, 'tmp', 'seg')
os.makedirs(TMP_SEG, exist_ok=True)

# Superficies exatas dos pisos construidos em set_vaso.py:
YS = float(YP + 1)      # 69.0 = piso do Salao Imperial e Cozinha Real (bloco y=68)
YT1 = float(YP + 2)     # 70.0 = 1o degrau do trono (bloco y=69)
YT2 = float(YP + 3)     # 71.0 = 2o degrau do trono (bloco y=70)
YG = float(YJ + 1)      # 66.0 = piso do Jardim, Varanda e interior da Casa do Ping (bloco y=65)
YMESA = YG + 1.0        # 67.0 = tampo da bancada ensolarada (1414, 66, -1332 slab top)
YPEIT = YG + 1.0        # 67.0 = topo do peitoril da janela (1420, 66, -1328)

TAGS_ELENCO = (
    'ping', 'rei', 'riv1', 'riv2', 'riv3',
    'vaso', 'vaso1', 'vaso2', 'vaso3',
    'regador', 'panela', 'sem_hashi', 'coroa_solta',
    'semente_mao', 'terra_mao', 'gota', 'deb'
)

PLANOS_LIST = json.load(open(os.path.join(PROJ, 'roteiro', 'planos.json'), encoding='utf-8'))
PLANOS_IDX = {p['nome']: (i, p) for i, p in enumerate(PLANOS_LIST)}

# ==============================================================================
# CONEXAO KEEP-ALIVE PARA CAPTURA RAPIDA DO FRAMEBUFFER E BANCO DE SONS (.OGG)
# ==============================================================================

_BRIDGE = json.load(open(os.path.expanduser(r'~/.mcpfabric/bridge.json')))
_HP = _BRIDGE['url'].replace('http://', '').replace('https://', '').split('/')[0]
_HDR = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + _BRIDGE['token'], 'Connection': 'keep-alive'}
_CONN = None
_SHOT_ID = 0


def _capturar_png():
    global _CONN, _SHOT_ID
    _SHOT_ID += 1
    body = json.dumps({'jsonrpc': '2.0', 'id': _SHOT_ID, 'method': 'vision.screenshot', 'params': {}}).encode()
    for tent in range(3):
        try:
            if _CONN is None:
                _CONN = http.client.HTTPConnection(_HP, timeout=20)
            _CONN.request('POST', '/rpc', body=body, headers=_HDR)
            raw = _CONN.getresponse().read()
            r = json.loads(raw)
            return base64.b64decode(r['result']['base64'])
        except Exception:
            try:
                if _CONN:
                    _CONN.close()
            except Exception:
                pass
            _CONN = None
            time.sleep(0.1)
    raise RuntimeError('Falha ao capturar vision.screenshot')


def _descobrir_assets_mc():
    cand = [
        os.environ.get('MC_ASSETS_DIR', ''),
        os.path.expandvars(r'%APPDATA%\ModrinthApp\meta\assets'),
        os.path.expandvars(r'%APPDATA%\.minecraft\assets'),
        os.path.expanduser('~/.minecraft/assets'),
    ]
    for root in cand:
        idx_dir = os.path.join(root, 'indexes') if root else ''
        if os.path.isdir(idx_dir):
            arqs = sorted(
                [f for f in os.listdir(idx_dir) if f.endswith('.json')],
                key=lambda nm: (int(nm[:-5]) if nm[:-5].isdigit() else -1, nm),
                reverse=True,
            )
            for arq in arqs:
                objs = json.load(open(os.path.join(idx_dir, arq), encoding='utf-8')).get('objects', {})
                if 'minecraft/sounds.json' in objs:
                    sh = objs['minecraft/sounds.json']['hash']
                    reg = json.load(open(os.path.join(root, 'objects', sh[:2], sh), encoding='utf-8'))
                    return root, objs, reg
    return '', {}, {}


_ASSETS_ROOT, _ASSETS_IDX, _SOUNDS_REG = _descobrir_assets_mc()
_RND_SND = random.Random(42)


def _ogg_de_evento(ev_nome):
    chave = ev_nome.replace('minecraft:', '')
    info = _SOUNDS_REG.get(chave)
    if not info:
        return None
    escolhas = []
    for s in info.get('sounds', []):
        nm = s['name'] if isinstance(s, dict) else s
        tp = s.get('type', 'file') if isinstance(s, dict) else 'file'
        if tp == 'event':
            p = _ogg_de_evento(nm)
            if p:
                escolhas.append(p)
        else:
            ak = f"minecraft/sounds/{nm.replace('minecraft:', '')}.ogg"
            if ak in _ASSETS_IDX:
                h = _ASSETS_IDX[ak]['hash']
                escolhas.append(os.path.join(_ASSETS_ROOT, 'objects', h[:2], h))
    return _RND_SND.choice(escolhas) if escolhas else None


_EVENTOS_SOM = []
_T_ATUAL = 0.0


def snd_cam(som, vol=1.0, pitch=1.0):
    _EVENTOS_SOM.append((_T_ATUAL, som, float(vol), float(pitch)))


def snd(som, x, y, z, vol=1.0, pitch=1.0):
    _EVENTOS_SOM.append((_T_ATUAL, som, float(vol), float(pitch)))


def render_audio_plano(out_wav, dur, eventos):
    validos = []
    for t_s, nome_s, vol, pitch in eventos:
        ogg = _ogg_de_evento(nome_s)
        if ogg and os.path.exists(ogg):
            validos.append((max(0.0, float(t_s)), ogg, min(1.5, vol * 0.65), max(0.5, min(2.0, pitch))))
    if not validos:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                        '-t', f'{dur:.4f}', out_wav], check=True)
        return
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'anullsrc=r=48000:cl=stereo:d={dur:.4f}']
    filtros = []
    tags = ['[0:a]']
    for idx, (t_s, ogg, vol, pitch) in enumerate(validos, start=1):
        cmd += ['-i', ogg]
        ms = int(round(t_s * 1000))
        filtros.append(
            f'[{idx}:a]asetrate=48000*{pitch:.3f},aresample=48000,aformat=channel_layouts=stereo,'
            f'volume={vol:.3f},adelay={ms}|{ms}[s{idx}]'
        )
        tags.append(f'[s{idx}]')
    fc = ';'.join(filtros + [
        f"{''.join(tags)}amix=inputs={len(tags)}:normalize=0:duration=first,"
        f"atrim=duration={dur:.4f},afade=t=in:d=0.03,afade=t=out:st={max(0.0, dur - 0.05):.4f}:d=0.05[out]"
    ])
    cmd += ['-filter_complex', fc, '-map', '[out]', '-ar', '48000', '-ac', '2', out_wav]
    subprocess.run(cmd, check=True)


# ==============================================================================
# TRAJETO SINCRONIZADO EM TEMPO DE JOGO (COMPATIVEL COM /TICK RATE REDUZIDO)
# ==============================================================================

class TrajetoJogo:
    """Interpola movimento de personagem/objeto em tempo de jogo (20 ticks/seg de jogo)."""
    def __init__(self, sel, f, passo=0.15, dy=0.0):
        self.sel, self.f, self.passo, self.dy = sel, f, passo, dy
        self.tk = max(2, min(59, int(round(passo * 20)) + 1))
        self.prox = None

    def preparar(self):
        C(f'execute as {self.sel} run data merge entity @s {{teleport_duration:{self.tk}}}')

    def _tp(self, t_jogo):
        x, y, z = self.f(t_jogo)
        C(f'tp {self.sel} {x:.3f} {y + self.dy:.3f} {z:.3f}')

    def tick(self, t_jogo):
        if self.prox is None:
            self._tp(self.passo)
            self.prox = self.passo
        elif t_jogo >= self.prox - 0.025:
            self.prox += self.passo
            self._tp(self.prox)


# ==============================================================================
# HELPERS DE GEOMETRIA E DIRECAO DE CENA
# ==============================================================================

def ang(d):
    yaw = math.degrees(math.atan2(-d[0], d[2]))
    pitch = -math.degrees(math.atan2(d[1], math.hypot(d[0], d[2])))
    return yaw, pitch


def mirar_ponto(cpos, alvo, subir=0.0):
    d = np.array(alvo, float) - np.array(cpos, float)
    yw, pt = ang(d)
    return yw, pt - subir


def ori_para(pos_ator, pos_alvo, offset_yaw=0.0, pitch=0.0, roll=0.0):
    """Retorna (yaw, pitch, roll) para pos_ator olhar exatamente para pos_alvo (+ offset_yaw)."""
    yw, _ = M.yp(pos_ator, pos_alvo)
    return (yw + offset_yaw, pitch, roll)


def limpar_cena(tempo_sol=3500):
    C('tick rate 20')
    C(f'ride {M.PL} dismount')
    for tg in TAGS_ELENCO:
        C(f'kill @e[tag={tg}]')
    C('kill @e[type=item]')
    C(f'time set {tempo_sol}')
    C('weather clear')


def preparar_estudo_mcp():
    for c in [
        'gamerule send_command_feedback false',
        'gamerule advance_time false',
        'gamerule advance_weather false',
        'gamerule random_tick_speed 0',
        'gamerule spawn_mobs false',
        'time set 3500',
        'weather clear',
        f'effect clear {M.PL} invisibility',
        f'effect give {M.PL} invisibility infinite 0 true',
        'team add semnome',
        'team modify semnome nametagVisibility never',
        'team modify semnome seeFriendlyInvisibles false',
        f'team join semnome {M.PL}',
        'kill @e[type=item]',
        'forceload add 1410 -1476 1460 -1320',
    ]:
        C(c)
    time.sleep(0.45)
    # Garante ajustes finos de marcenaria no trono (assento plano y=71.50 sem degrau frontal!), varanda e janela:
    C('fill 1419 71 -1471 1421 71 -1471 mangrove_slab[type=bottom]')
    C('setblock 1418 72 -1471 bamboo_slab[type=bottom]')
    C('setblock 1422 72 -1471 bamboo_slab[type=bottom]')
    C('fill 1414 66 -1330 1415 66 -1330 spruce_slab[type=bottom]')
    C('fill 1419 66 -1326 1421 66 -1326 spruce_slab[type=bottom]')
    C('forceload remove 1410 -1476 1460 -1320')
    try:
        mc.call('screen.close')
        mc.call('inventory.selectHotbar', {'slot': 8})
    except Exception:
        pass


def gravar_plano(nome, cpos, alvo, v_cam, fn_setup, fn_tick=None, fn_inicio=None, subir=0.0, espera=0.85, tempo_sol=3500):
    """Captura deterministica dos quadros do plano em 30fps e gera tmp/seg/vXX.mp4 + aXX.wav."""
    global _T_ATUAL
    idx, meta = PLANOS_IDX[nome]
    dur = round(float(meta['t1']) - float(meta['t0']), 4)
    n_frames = max(3, int(round(dur * FPS)))

    out_v = os.path.join(TMP_SEG, f'v{idx:02d}.mp4')
    out_a = os.path.join(TMP_SEG, f'a{idx:02d}.wav')

    limpar_cena(tempo_sol=tempo_sol)
    _EVENTOS_SOM.clear()
    _T_ATUAL = 0.0

    # Recua levemente cpos em -0.05s * v_cam para compensar o pre-roll de 0.05s de jogo
    pre_game = 0.06
    cpos_pre = tuple(cpos[k] - v_cam[k] * pre_game for k in range(3))
    yw, pt = mirar_ponto(cpos, alvo, subir=subir)
    cam.criar(cpos_pre[0], cpos_pre[1], cpos_pre[2], yw, pt)

    extras_traj = fn_setup() or []
    if not isinstance(extras_traj, (list, tuple)):
        extras_traj = [extras_traj]
    for tr in extras_traj:
        tr.preparar()

    time.sleep(espera)

    vf = f'scale=1080:1920:flags=lanczos,setsar=1,{MV.COR}'
    ff = subprocess.Popen([
        'ffmpeg', '-v', 'error', '-y',
        '-f', 'image2pipe', '-framerate', str(FPS), '-vcodec', 'png', '-i', '-',
        '-vf', vf, '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', out_v
    ], stdin=subprocess.PIPE)

    tc = Vel(f'@e[tag={M.CAM}]', v_cam, 'cam')
    tc.preparar()
    C(f'tick rate {TICK_RATE}')
    tc.tick(0.0)
    # Pre-roll de ~0.32s reais (~0.055s de jogo) para a velocidade do servidor ja estar em movimento no quadro 0!
    time.sleep(pre_game * K_SLOW)

    ev = lambda _n: None
    if fn_inicio:
        _T_ATUAL = 0.0
        fn_inicio(ev)

    st_k = -1
    t0 = time.perf_counter()
    try:
        for f in range(n_frames):
            alvo_wall = t0 + f * DT_WALL
            agora = time.perf_counter()
            if alvo_wall > agora:
                time.sleep(alvo_wall - agora)

            t_jogo = f / float(FPS)
            _T_ATUAL = t_jogo
            for tr in extras_traj:
                tr.tick(t_jogo)

            kk = int(round(t_jogo * 20))
            if fn_tick and kk != st_k:
                st_k = kk
                fn_tick(t_jogo, kk, ev)

            ff.stdin.write(_capturar_png())
    finally:
        tc.parar()
        C('tick rate 20')
        cam.fim()
        ff.stdin.close()
        rc = ff.wait()
        if rc != 0:
            raise RuntimeError(f'FFmpeg falhou ao gravar {nome}')

    render_audio_plano(out_a, dur, list(_EVENTOS_SOM))
    print(f'  -> OK {nome} -> v{idx:02d}.mp4 ({n_frames}f, {dur:.2f}s) em {time.perf_counter() - t0:.1f}s reais', flush=True)


# ==============================================================================
# HELPERS DE ELENCO EM CENA
# ==============================================================================

def spawn_fila_jovens(com_vasos=False, pose_riv='recebe', pose_ping='recebe', z_fila=-1448.0):
    xs = [1416.0, 1418.8, 1421.6, 1424.2]
    cores = ['green_terracotta', 'blue_terracotta', 'brown_terracotta']
    flores = ['flor_rosa', 'flor_ouro', 'flor_azul']
    rivs, vasos = [], []
    for i in range(3):
        r = Rival(tag=f'riv{i+1}', cor=cores[i])
        r.criar(xs[i], YS + r.ALT_CHAO, z_fila, ori=(180, 0, 0), pose=pose_riv)
        rivs.append(r)
        if com_vasos:
            v = criar_vaso(tag=f'vaso{i+1}', tipo=flores[i])
            v.criar(xs[i], YS + 0.80, z_fila - 0.48, ori=(180, 0, 0))
            vasos.append(v)
    ping = PingCapivara(tag='ping')
    if pose_ping is not None:
        ping.criar(xs[3], YS + ping.ALT_CHAO, z_fila, ori=(180, 0, 0), pose=pose_ping)
        if com_vasos:
            vp = criar_vaso(tag='vaso', tipo='vazio')
            vp.criar(xs[3], YS + 0.46, z_fila - 0.56, ori=(180, 0, 0))
            vasos.append(vp)
    return rivs, ping, vasos


def spawn_semente_pequena(tag, x, y, z):
    m = ModeloRico({
        's1': ('lime_terracotta', (-0.055, 0.0, -0.065), (0.11, 0.075, 0.13)),
        's2': ('lime_concrete', (-0.032, 0.06, -0.04), (0.065, 0.04, 0.08)),
    }, tag)
    m.criar(x, y, z)
    return m


# ==============================================================================
# BLOCO 1: P01..P04 — Entrega da semente no Salao Imperial
# ==============================================================================

def p_P01():
    """Salao Imperial vermelho e dourado: Rei em pe diante da fila de jovens."""
    st = {}
    def setup():
        rei = Rei('rei'); rei.sorriso = 0.1
        rei.criar(1420.5, YS + rei.ALT_CHAO, -1451.8, ori=(0, 0, 0), pose='entrega')
        rivs, ping, _ = spawn_fila_jovens(com_vasos=False, pose_riv='recebe', pose_ping='recebe', z_fila=-1448.0)
        st['rei'] = rei; st['ping'] = ping
    def tick(t, kk, ev):
        if kk == 6:
            st['rei'].posar(juntas={'braco_d': (-88, 0, 10)}, dur=8)
    gravar_plano('P01', (1416.2, YS + 2.15, -1445.0), (1420.5, YS + 1.6, -1450.5), (0.55, -0.06, -0.45), setup, tick)


def p_P02():
    """Super close em perfil limpo: mao do Rei depositando uma semente verde nas patinhas abertas de Ping."""
    st = {}
    def setup():
        rei = Rei('rei'); rei.sorriso = 0.25
        rei.criar(1419.86, YS + rei.ALT_CHAO, -1449.20, ori=(-90, 0, 0), pose='entrega')
        ping = PingCapivara('ping'); ping.fechar = 0.05; ping.sorriso = 0.45
        ping.criar(1421.26, YS + ping.ALT_CHAO, -1449.20, ori=(90, 0, 0), pose='recebe')
        spawn_semente_pequena('semente_mao', 1420.52, YS + 1.20, -1449.12)
        tr = TrajetoJogo('@e[tag=semente_mao]',
                         lambda t: (1420.52 + min(0.18, 0.22 * t), max(YS + 0.78, YS + 1.20 - 0.46 * t), -1449.12),
                         passo=0.15)
        st['rei'] = rei; st['ping'] = ping
        return [tr]
    def ini(ev):
        snd_cam('item.crop.plant', 0.9, 1.2)
    def tick(t, kk, ev):
        if kk == 10:
            snd_cam('item.crop.plant', 0.75, 1.35)
            st['ping'].sorriso = 0.9; st['ping'].posar(dur=6)
    gravar_plano('P02', (1420.58, YS + 1.18, -1447.02), (1420.60, YS + 0.98, -1449.20), (0.04, -0.03, -0.18), setup, tick, ini)


def p_P03():
    """Travelling lateral pela fila de jovens perfilados olhando suas sementes nas maos diante do Rei."""
    st = {}
    def setup():
        rei = Rei('rei')
        rei.criar(1420.5, YS + rei.ALT_CHAO, -1452.0, ori=(0, 0, 0), pose='maos_costas')
        rivs, ping, _ = spawn_fila_jovens(com_vasos=False, pose_riv='recebe', pose_ping='recebe', z_fila=-1448.0)
        for i, xk in enumerate([1416.0, 1418.8, 1421.6, 1424.2]):
            spawn_semente_pequena('semente_mao', xk, YS + (0.98 if i < 3 else 0.74), -1448.46 if i < 3 else -1448.62)
        ping.sorriso = 0.75; ping.posar(dur=2)
        st['rivs'] = rivs; st['ping'] = ping
    def tick(t, kk, ev):
        if kk == 8:
            posar_varios([(st['rivs'][1], {'juntas': {'cabeca': (14, -8, 0)}}), (st['ping'], {'juntas': {'cabeca': (8, 8, 0)}})], dur=8)
    gravar_plano('P03', (1414.6, YS + 1.66, -1450.5), (1420.8, YS + 1.35, -1448.0), (1.45, 0.0, 0.0), setup, tick)


def p_P04():
    """Contra-plongee solene do Rei erguendo a mao direita ao lado em instrucao final aos jovens."""
    st = {}
    def setup():
        rei = Rei('rei'); rei.brava = 0.2
        rei.criar(1420.5, YS + rei.ALT_CHAO, -1452.2, ori=(0, 0, 0), pose='pe')
        spawn_fila_jovens(com_vasos=False, pose_riv='recebe', pose_ping='recebe', z_fila=-1447.8)
        st['rei'] = rei
    def tick(t, kk, ev):
        if kk == 4:
            st['rei'].boca_ab = 0.5; st['rei'].posar(juntas={'braco_d': (-92, 0, -16), 'cabeca': (6, 0, 0)}, dur=8)
        elif kk == 14:
            st['rei'].boca_ab = 0.15; st['rei'].posar(juntas={'braco_d': (-132, 0, -24), 'cabeca': (4, -4, 0)}, dur=8)
    gravar_plano('P04', (1419.2, YS + 1.22, -1449.5), (1420.5, YS + 2.22, -1452.2), (0.22, 0.08, -0.25), setup, tick)


# ==============================================================================
# BLOCO 2: P05..P07 — Rei velho pensativo no Trono Dourado
# ==============================================================================

def _rei_no_trono(sorriso=0.0, brava=0.25):
    rei = Rei('rei'); rei.sorriso = sorriso; rei.brava = brava; rei.fechar = 0.2
    # Sentado sobre a almofada y=71.50 (z=-1471..-1470) com joelhos em 90 graus e botas no tapete y=71.00!
    rei.criar(1420.5, 72.08, -1470.42, ori=(0, 0, 0), pose='sentado')
    return rei


def p_P05():
    """Close no rosto envelhecido do Rei de barba branca longa e coroa imperial dourada."""
    st = {}
    def setup():
        st['rei'] = _rei_no_trono(sorriso=0.0, brava=0.25)
    def tick(t, kk, ev):
        if kk == 8:
            st['rei'].fechar = 0.75; st['rei'].posar(juntas={'cabeca': (12, 6, 0)}, dur=8)
        elif kk == 16:
            st['rei'].fechar = 0.22; st['rei'].posar(juntas={'cabeca': (8, 5, 0)}, dur=7)
    gravar_plano('P05', (1419.78, 72.72, -1468.32), (1420.5, 72.68, -1470.42), (0.15, 0.02, -0.26), setup, tick)


def p_P06():
    """Plano medio do Rei sentado perfeitamente no trono dourado esculpido, refletindo."""
    st = {}
    def setup():
        st['rei'] = _rei_no_trono(sorriso=0.0, brava=0.2)
    def tick(t, kk, ev):
        if kk == 7:
            st['rei'].posar(juntas={'braco_d': (-64, 0, -14), 'cabeca': (11, -7, 0)}, dur=10)
    gravar_plano('P06', (1418.45, 72.22, -1466.75), (1420.5, 72.25, -1470.42), (0.42, 0.05, -0.35), setup, tick)


def p_P07():
    """Plano aberto simetrico em contra-plongee destacando o Trono Dourado em degrau alto."""
    def setup():
        _rei_no_trono(sorriso=0.0, brava=0.15)
    gravar_plano('P07', (1420.5, 70.40, -1463.35), (1420.5, 72.55, -1470.8), (0.0, 0.16, -0.65), setup)


# ==============================================================================
# BLOCO 3: P08..P12 — Jardim florido e cuidados de Ping com a semente
# ==============================================================================

def p_P08():
    """Jardim florido com cerejeiras rosas, bambus e montanhas ao fundo, Capivara Ping grande em 3/4."""
    cpos = (1423.35, YG + 1.48, -1337.1)
    ppos = (1425.6, YG + PingCapivara.ALT_CHAO, -1340.0)
    st = {}
    def setup():
        ping = PingCapivara('ping'); ping.sorriso = 0.95; ping.fechar = 0.1
        ori = ori_para(ppos, cpos, offset_yaw=-18)
        ping.criar(*ppos, ori=ori, pose='segura_vaso')
        rad = math.radians(-ori[0])
        v = criar_vaso('vaso', 'vazio')
        v.criar(ppos[0] - math.sin(rad) * 0.56, YG + 0.46, ppos[2] + math.cos(rad) * 0.56, ori=ori)
        st['ping'] = ping
    def ini(ev):
        snd_cam('block.amethyst_block.chime', 0.75, 1.2)
    def tick(t, kk, ev):
        if kk == 8:
            st['ping'].posar(juntas={'cabeca': (-6, 8, 5)}, dur=8)
        elif kk == 18:
            st['ping'].posar(juntas={'cabeca': (2, -4, -3)}, dur=8)
    gravar_plano('P08', cpos, (1425.85, YG + 1.18, -1340.6), (0.35, -0.05, -0.35), setup, tick, ini)


def p_P09():
    """Close medio da Capivara Ping sorridente ajoelhada no jardim florido plantando a semente no vaso."""
    cpos = (1424.45, YG + 1.18, -1338.15)
    ppos = (1426.0, YG + PingCapivara.ALT_CHAO - 0.10, -1340.15)
    st = {}
    def setup():
        ping = PingCapivara('ping'); ping.sorriso = 0.95; ping.fechar = 0.12
        ori = ori_para(ppos, cpos, offset_yaw=14)
        ping.criar(*ppos, ori=ori, pose='agacha_planta')
        rad = math.radians(-ori[0])
        v = criar_vaso('vaso', 'semente')
        v.criar(ppos[0] - math.sin(rad) * 0.64, YG + 0.02, ppos[2] + math.cos(rad) * 0.64)
        st['ping'] = ping
    def ini(ev):
        snd_cam('item.crop.plant', 1.0, 1.0)
    def tick(t, kk, ev):
        if kk == 6:
            st['ping'].posar(juntas={'braco_d': (-78, 0, 14), 'braco_e': (-68, 0, -12), 'cabeca': (14, 0, 4)}, dur=6)
            snd_cam('block.rooted_dirt.place', 0.85, 1.15)
        elif kk == 14:
            st['ping'].posar(juntas={'braco_d': (-60, 0, 10), 'braco_e': (-58, 0, -10), 'cabeca': (8, 0, -4)}, dur=7)
    gravar_plano('P09', cpos, (1425.75, YG + 0.68, -1339.75), (0.20, -0.04, -0.20), setup, tick, ini)


def p_P10():
    """Close do regador na patinha direita de Ping jorrando agua cristalina sobre o vaso na bancada."""
    def setup():
        ping = PingCapivara('ping'); ping.sorriso = 0.85; ping.fechar = 0.12
        # Ping sobre o banquinho y=66.5 atras da mesa (z=-1330.32 -> 100% livre da mesa z=-1331..-1332!)
        ping.criar(1414.65, YG + 0.5 + ping.ALT_CHAO, -1330.32, ori=(180, 0, 0), pose='rega')
        v = criar_vaso('vaso', 'vazio')
        v.criar(1414.48, YMESA, -1331.42)
        reg = criar_regador('regador')
        reg.criar(1414.08, YMESA + 0.44, -1331.02, ori=(152, 28, 0))
    def ini(ev):
        snd_cam('item.bucket.empty', 0.85, 1.25)
    def tick(t, kk, ev):
        if kk % 2 == 0:
            C('particle splash 1414.46 67.38 -1331.40 0.06 0.08 0.06 0.02 8 force')
            C('particle falling_water 1414.34 67.54 -1331.28 0.04 0.08 0.04 0.0 5 force')
        if kk == 10:
            snd_cam('entity.generic.splash', 0.45, 1.55)
    gravar_plano('P10', (1413.15, YMESA + 0.72, -1332.95), (1414.52, YMESA + 0.42, -1330.95), (0.18, -0.03, 0.18), setup, tick, ini)


def p_P11():
    """Plano medio frontal/3-4 do vaso sob o sol dourado na varanda com Ping sorrindo e cerejeiras ao fundo."""
    cpos = (1416.25, YMESA + 0.58, -1333.65)
    ppos = (1415.15, YG + 0.5 + PingCapivara.ALT_CHAO, -1330.35)
    st = {}
    def setup():
        v = criar_vaso('vaso', 'vazio')
        v.criar(1414.45, YMESA, -1331.52)
        ping = PingCapivara('ping'); ping.sorriso = 0.95; ping.fechar = 0.12
        ori = ori_para(ppos, (1414.95, YMESA + 0.4, -1332.6), offset_yaw=0)
        ping.criar(*ppos, ori=ori, pose='apoia_rosto')
        st['ping'] = ping
    def tick(t, kk, ev):
        if kk == 6:
            C('particle end_rod 1414.45 67.62 -1331.52 0.25 0.25 0.25 0.005 4 force')
            st['ping'].posar(juntas={'cabeca': (4, -8, -5)}, dur=9)
    gravar_plano('P11', cpos, (1414.65, YMESA + 0.36, -1331.05), (-0.24, -0.02, 0.22), setup, tick, tempo_sol=2200)


def p_P12():
    """Close das patinhas de Ping afofando terra escura rica dentro do vaso (sem encostar na bancada)."""
    st = {}
    def setup():
        ping = PingCapivara('ping'); ping.sorriso = 0.85; ping.fechar = 0.12
        ping.criar(1414.5, YG + 0.5 + ping.ALT_CHAO, -1330.32, ori=(180, 0, 0), pose='recebe')
        v = criar_vaso('vaso', 'vazio')
        v.criar(1414.5, YMESA, -1331.32)
        st['ping'] = ping
    def ini(ev):
        snd_cam('block.rooted_dirt.place', 1.0, 0.95)
    def tick(t, kk, ev):
        if kk in (4, 12, 20):
            af = -76 if kk != 12 else -64
            st['ping'].posar(juntas={'braco_e': (af, 0, -14), 'braco_d': (af, 0, 14)}, dur=5)
            C('particle block{block_state:"minecraft:rooted_dirt"} 1414.5 67.38 -1331.32 0.08 0.04 0.08 0.02 12 force')
            snd_cam('block.mud.place', 0.75, 1.15)
    gravar_plano('P12', (1413.38, YMESA + 0.74, -1332.68), (1414.5, YMESA + 0.42, -1330.92), (0.14, -0.04, 0.18), setup, tick, ini)


# ==============================================================================
# BLOCO 4: P13..P15 — Vigilia na janela, passagem de tempo e frustracao
# ==============================================================================

def p_P13():
    """Close terno da Capivara Ping pela janela aberta vigiando o vaso no peitoril (zero colisao!)."""
    st = {}
    def setup():
        v = criar_vaso('vaso', 'vazio')
        v.criar(1420.5, YPEIT, -1327.62)
        ping = PingCapivara('ping'); ping.fechar = 0.0; ping.sorriso = 0.4
        ping.criar(1420.5, YG + 0.5 + ping.ALT_CHAO, -1326.25, ori=(180, 0, 0), pose='apoia_rosto')
        st['ping'] = ping
    def tick(t, kk, ev):
        if kk == 7:
            st['ping'].fechar = 0.95; st['ping'].posar(dur=3)
        elif kk == 10:
            st['ping'].fechar = 0.0; st['ping'].posar(juntas={'cabeca': (10, -8, 5)}, dur=6)
        elif kk == 18:
            st['ping'].posar(juntas={'cabeca': (10, 8, -4)}, dur=6)
    gravar_plano('P13', (1419.82, YPEIT + 0.68, -1329.25), (1420.5, YPEIT + 0.48, -1326.85), (0.15, -0.02, 0.22), setup, tick)


def p_P14():
    """Vista externa pela janela de madeira da casa com o vaso no peitoril e Ping esperando na passagem do dia."""
    st = {}
    def setup():
        v = criar_vaso('vaso', 'vazio')
        v.criar(1420.5, YPEIT, -1327.62)
        ping = PingCapivara('ping'); ping.fechar = 0.2; ping.sorriso = 0.1
        ping.criar(1420.5, YG + 0.5 + ping.ALT_CHAO, -1326.22, ori=(180, 0, 0), pose='pe')
        st['ping'] = ping
    def tick(t, kk, ev):
        hora = int(1500 + min(1.0, t / 1.55) * 11200)
        C(f'time set {hora}')
        if kk == 8:
            st['ping'].posar(juntas={'cabeca': (10, 10, 0)}, dur=8)
        elif kk == 18:
            st['ping'].fechar = 0.55; st['ping'].posar(juntas={'cabeca': (14, 4, 0)}, dur=8)
    gravar_plano('P14', (1420.35, YPEIT + 0.72, -1331.45), (1420.5, YPEIT + 0.52, -1326.9), (0.18, 0.0, 0.25), setup, tick, tempo_sol=1500)


def p_P15():
    """Close triste da Capivara Ping cabisbaixa olhando o vaso so com terra nua, sem nenhum broto."""
    st = {}
    def setup():
        v = criar_vaso('vaso', 'vazio')
        v.criar(1420.5, YPEIT, -1327.62)
        ping = PingCapivara('ping'); ping.fechar = 0.55; ping.brava = 0.0; ping.sorriso = 0.0
        ping.criar(1420.5, YG + 0.5 + ping.ALT_CHAO, -1326.25, ori=(180, 0, 0), pose='triste_vaso')
        st['ping'] = ping
    def tick(t, kk, ev):
        if kk == 6:
            st['ping'].fechar = 0.82; st['ping'].posar(juntas={'cabeca': (15, 0, -4)}, dur=10)
    gravar_plano('P15', (1421.18, YPEIT + 0.68, -1329.15), (1420.5, YPEIT + 0.46, -1326.85), (-0.14, -0.02, 0.18), setup, tick)


# ==============================================================================
# BLOCO 5: P16..P20 — O grande dia no Palacio e as plantas gigantes dos rivais
# ==============================================================================

def p_P16():
    """Fachada vermelha e dourada do Palacio Imperial com Ping inteiro em perfil/3-4 sobre a avenida de pedra (y=65.0)."""
    cpos = (1418.65, 66.25, -1407.4)
    ppos = (1419.65, 65.0 + PingCapivara.ALT_CHAO, -1411.4)
    def setup():
        ping = PingCapivara('ping'); ping.fechar = 0.15; ping.sorriso = 0.0
        ori = (128, 0, 0)   # Perfil 3/4 mostrando nitidamente focinho, olho, tunica, pernas e vaso vazio!
        ping.criar(*ppos, ori=ori, pose='segura_vaso')
        rad = math.radians(-ori[0])
        vp = criar_vaso('vaso', 'vazio')
        vp.criar(ppos[0] - math.sin(rad) * 0.56, 65.46, ppos[2] + math.cos(rad) * 0.56, ori=ori)
        r1 = Rival('riv1', 'green_terracotta'); r1.criar(1419.2, 69.0 + r1.ALT_CHAO, -1425.5, ori=(180, 0, 0), pose='segura_vaso')
        r2 = Rival('riv2', 'blue_terracotta'); r2.criar(1421.8, 68.0 + r2.ALT_CHAO, -1423.5, ori=(180, 0, 0), pose='segura_vaso')
    gravar_plano('P16', cpos, (1420.2, 69.6, -1430.0), (0.08, 0.14, -1.10), setup)


def p_P17():
    """Interior solene do Salao Imperial por cima do ombro de Ping a direita olhando o Rei diante do trono."""
    def setup():
        rei = Rei('rei'); rei.criar(1420.5, YT2 + rei.ALT_CHAO, -1469.2, ori=(0, 0, 0), pose='maos_costas')
        spawn_fila_jovens(com_vasos=True, pose_riv='orgulhoso', pose_ping='triste_vaso', z_fila=-1448.0)
    gravar_plano('P17', (1424.05, YS + 2.05, -1444.5), (1420.5, YS + 1.80, -1465.0), (-0.22, -0.04, -1.30), setup)


def p_P18():
    """Plano conjunto dos tres jovens rivais alinhados e orgulhosos estufando o peito atras de seus vasos."""
    st = {}
    def setup():
        rivs, _, _ = spawn_fila_jovens(com_vasos=True, pose_riv='orgulhoso', pose_ping=None, z_fila=-1448.0)
        for r in rivs:
            r.sorriso = 0.85; r.posar(dur=2)
        st['rivs'] = rivs
    def tick(t, kk, ev):
        if kk == 6:
            posar_varios([(st['rivs'][0], {'juntas': {'cabeca': (-16, -8, 4)}}),
                          (st['rivs'][1], {'juntas': {'cabeca': (-18, 6, -4)}}),
                          (st['rivs'][2], {'juntas': {'cabeca': (-14, 10, 4)}})], dur=8)
    gravar_plano('P18', (1416.0, YS + 1.65, -1451.5), (1418.8, YS + 1.45, -1448.0), (0.85, 0.02, 0.0), setup, tick)


def p_P19():
    """Contra-plongee impressionante de um vaso rival exibindo arbusto gigante e folhagem exuberante."""
    def setup():
        spawn_fila_jovens(com_vasos=True, pose_riv='orgulhoso', pose_ping=None, z_fila=-1448.0)
    gravar_plano('P19', (1417.95, YS + 0.95, -1449.75), (1418.8, YS + 1.62, -1448.42), (0.28, 0.14, 0.12), setup)


def p_P20():
    """Travelling proximo destacando as flores enormes e vibrantes rosa, dourada e azul nos vasos dos rivais."""
    def setup():
        spawn_fila_jovens(com_vasos=True, pose_riv='orgulhoso', pose_ping=None, z_fila=-1448.0)
    def ini(ev):
        snd_cam('block.azalea_leaves.place', 0.65, 1.2)
    gravar_plano('P20', (1415.2, YS + 1.72, -1449.75), (1418.8, YS + 1.56, -1448.48), (2.2, 0.0, 0.0), setup, fn_inicio=ini)


# ==============================================================================
# BLOCO 6: P21..P25 — Vaso vazio de Ping e a coragem de leva-lo mesmo assim
# ==============================================================================

def p_P21():
    """Plano medio contrastante da pequena Capivara Ping encolhida ao lado das plantas gigantes."""
    st = {}
    def setup():
        rivs, ping, _ = spawn_fila_jovens(com_vasos=True, pose_riv='orgulhoso', pose_ping='triste_vaso', z_fila=-1448.0)
        ping.fechar = 0.55; ping.sorriso = 0.0; ping.posar(dur=2)
        st['ping'] = ping
    def tick(t, kk, ev):
        if kk == 8:
            st['ping'].posar(juntas={'cabeca': (14, -8, 0)}, dur=8)
    gravar_plano('P21', (1422.35, YS + 1.48, -1450.85), (1423.65, YS + 1.02, -1448.25), (0.35, -0.05, 0.22), setup, tick)


def p_P22():
    """Detalhe nitido em plongee do vaso de barro de Ping contendo apenas terra escura lisa, vazio."""
    def setup():
        spawn_fila_jovens(com_vasos=True, pose_riv='orgulhoso', pose_ping='triste_vaso', z_fila=-1448.0)
    gravar_plano('P22', (1423.48, YS + 1.28, -1449.68), (1424.20, YS + 0.68, -1448.56), (0.12, -0.08, 0.16), setup)


def p_P23():
    """Close emocionante da Capivara Ping cabisbaixa olhando tristemente para seu vaso sem nenhuma planta."""
    st = {}
    def setup():
        _, ping, _ = spawn_fila_jovens(com_vasos=True, pose_riv='orgulhoso', pose_ping='triste_vaso', z_fila=-1448.0)
        ping.fechar = 0.65; ping.sorriso = 0.0; ping.posar(dur=2)
        st['ping'] = ping
    def tick(t, kk, ev):
        if kk == 6:
            st['ping'].fechar = 0.85; st['ping'].posar(juntas={'cabeca': (15, 0, 4)}, dur=9)
    gravar_plano('P23', (1425.05, YS + 1.32, -1449.85), (1424.2, YS + 0.98, -1448.30), (-0.12, -0.03, 0.20), setup, tick)


def p_P24():
    """Close de Ping na entrada do salao respirando fundo e erguendo a cabeca com coragem segurando o vaso."""
    st = {}
    def setup():
        ping = PingCapivara('ping'); ping.fechar = 0.65; ping.sorriso = 0.0
        ping.criar(1420.5, YS + ping.ALT_CHAO, -1434.0, ori=(180, 0, 0), pose='triste_vaso')
        vp = criar_vaso('vaso', 'vazio')
        vp.criar(1420.5, YS + 0.46, -1434.56, ori=(180, 0, 0))
        st['ping'] = ping
    def tick(t, kk, ev):
        if kk == 6:
            st['ping'].fechar = 0.1; st['ping'].brava = 0.25
            st['ping'].posar(pose='segura_vaso', juntas={'cabeca': (-4, 0, 0)}, dur=8)
            snd_cam('block.bamboo_wood.step', 0.7, 1.1)
    gravar_plano('P24', (1419.62, YS + 1.25, -1436.25), (1420.5, YS + 1.08, -1434.25), (0.14, 0.02, 0.25), setup, tick)


def p_P25():
    """Travelling acompanhando Ping caminhando firme pelo tapete vermelho imperial ate a fila."""
    st = {}
    def setup():
        rei = Rei('rei'); rei.criar(1420.5, YT2 + rei.ALT_CHAO, -1469.0, ori=(0, 0, 0), pose='maos_costas')
        spawn_fila_jovens(com_vasos=True, pose_riv='orgulhoso', pose_ping=None, z_fila=-1448.0)
        ping = PingCapivara('ping'); ping.fechar = 0.15; ping.brava = 0.2
        ping.criar(1423.8, YS + ping.ALT_CHAO, -1442.5, ori=(180, 0, 0), pose='anda_vaso1', tdur=4)
        vp = criar_vaso('vaso', 'vazio')
        vp.criar(1423.8, YS + 0.46, -1443.06, ori=(180, 0, 0), tdur=4)
        tp_p = TrajetoJogo('@e[tag=ping]', lambda t: (1423.8, YS + ping.ALT_CHAO, -1442.5 - 1.9 * t), passo=0.15)
        tp_v = TrajetoJogo('@e[tag=vaso]', lambda t: (1423.8, YS + 0.46, -1443.06 - 1.9 * t), passo=0.15)
        st['ping'] = ping
        return [tp_p, tp_v]
    def tick(t, kk, ev):
        if kk % 5 == 0:
            st['ping'].posar(pose='anda_vaso1' if (kk // 5) % 2 == 0 else 'anda_vaso2', dur=5)
            snd_cam('block.bamboo_wood.step', 0.65, 1.15)
    gravar_plano('P25', (1421.5, YS + 1.45, -1445.1), (1423.8, YS + 1.02, -1443.1), (0.0, 0.0, -1.75), setup, tick)


# ==============================================================================
# BLOCO 7: P26..P31 — Inspecao silenciosa do Rei, sorriso e anuncio do vencedor
# ==============================================================================

def p_P26():
    """Plano medio lateral do Rei caminhando serio diante da fila de rivais, inspecionando cada planta gigante."""
    st = {}
    def setup():
        spawn_fila_jovens(com_vasos=True, pose_riv='orgulhoso', pose_ping='triste_vaso', z_fila=-1448.0)
        rei = Rei('rei'); rei.brava = 0.35
        rei.criar(1415.8, YS + rei.ALT_CHAO, -1450.25, ori=(25, 0, 0), pose='anda_costas1', tdur=4)
        tr_r = TrajetoJogo('@e[tag=rei]', lambda t: (1415.8 + 2.3 * t, YS + rei.ALT_CHAO, -1450.25), passo=0.15)
        st['rei'] = rei
        return [tr_r]
    def tick(t, kk, ev):
        if kk % 6 == 0:
            st['rei'].posar(pose='anda_costas1' if (kk // 6) % 2 == 0 else 'anda_costas2', dur=6)
            snd_cam('block.bamboo_wood.step', 0.55, 0.85)
    gravar_plano('P26', (1413.4, YS + 1.85, -1449.25), (1417.6, YS + 1.62, -1449.1), (1.8, 0.0, 0.0), setup, tick)


def p_P27():
    """Close tenso do rosto serio e silencioso do Rei passando pelas flores coloridas sem dizer uma palavra."""
    st = {}
    def setup():
        spawn_fila_jovens(com_vasos=True, pose_riv='orgulhoso', pose_ping='triste_vaso', z_fila=-1448.0)
        rei = Rei('rei'); rei.brava = 0.45; rei.sorriso = 0.0; rei.boca_ab = 0.0
        rei.criar(1418.8, YS + rei.ALT_CHAO, -1450.25, ori=(-15, 0, 0), pose='anda_costas1', tdur=4)
        tr_r = TrajetoJogo('@e[tag=rei]', lambda t: (1418.8 + 2.1 * t, YS + rei.ALT_CHAO, -1450.25), passo=0.15)
        st['rei'] = rei
        return [tr_r]
    def tick(t, kk, ev):
        if kk % 6 == 0:
            st['rei'].posar(pose='anda_costas1' if (kk // 6) % 2 == 0 else 'anda_costas2',
                            juntas={'cabeca': (12, -18 if (kk // 6) % 2 == 0 else -8, 0)}, dur=6)
    gravar_plano('P27', (1419.4, YS + 2.12, -1448.45), (1419.1, YS + 2.12, -1450.25), (2.0, 0.0, 0.0), setup, tick)


def p_P28():
    """Plano duplo lateral limpo: o Rei para diante da pequena Capivara Ping encarando o vaso vazio."""
    st = {}
    def setup():
        _, ping, _ = spawn_fila_jovens(com_vasos=True, pose_riv='orgulhoso', pose_ping='triste_vaso', z_fila=-1448.0)
        rei = Rei('rei'); rei.brava = 0.3; rei.sorriso = 0.0
        rei.criar(1422.7, YS + rei.ALT_CHAO, -1450.05, ori=(0, 0, 0), pose='anda_costas1', tdur=4)
        def fr(t):
            x = min(1424.15, 1422.7 + 1.9 * t)
            return (x, YS + rei.ALT_CHAO, -1450.05)
        tr_r = TrajetoJogo('@e[tag=rei]', fr, passo=0.15)
        st['rei'] = rei; st['ping'] = ping
        return [tr_r]
    def tick(t, kk, ev):
        if kk == 4:
            st['rei'].posar(pose='anda_costas2', dur=5); snd_cam('block.bamboo_wood.step', 0.6, 0.85)
        elif kk == 14:
            st['rei'].posar(pose='maos_costas', juntas={'cabeca': (20, 0, 0)}, dur=7)
            st['ping'].fechar = 0.8; st['ping'].posar(juntas={'cabeca': (15, 0, 0)}, dur=7)
    gravar_plano('P28', (1427.65, YS + 1.62, -1449.02), (1424.15, YS + 1.42, -1449.02), (-0.20, -0.02, 0.0), setup, tick)


def p_P29():
    """Close luminoso do rosto do Rei desfazendo a seriedade e abrindo um sorriso caloroso para Ping."""
    st = {}
    def setup():
        _, ping, _ = spawn_fila_jovens(com_vasos=True, pose_riv='orgulhoso', pose_ping='triste_vaso', z_fila=-1448.0)
        rei = Rei('rei'); rei.brava = 0.25; rei.sorriso = 0.0; rei.fechar = 0.15
        rei.criar(1424.2, YS + rei.ALT_CHAO, -1450.25, ori=(0, 0, 0), pose='maos_costas')
        st['rei'] = rei
    def tick(t, kk, ev):
        if kk == 5:
            st['rei'].brava = 0.0; st['rei'].sorriso = 0.55; st['rei'].posar(juntas={'cabeca': (14, 0, 0)}, dur=6)
        elif kk == 10:
            st['rei'].sorriso = 1.0; st['rei'].posar(juntas={'cabeca': (12, 0, 3)}, dur=6)
            snd_cam('block.amethyst_block.chime', 0.85, 1.35)
    gravar_plano('P29', (1424.75, YS + 2.05, -1448.15), (1424.2, YS + 2.12, -1450.25), (-0.12, 0.02, -0.22), setup, tick)


def p_P30():
    """Plano medio triunfante diante do trono: o Rei ergue o braco da Capivara Ping anunciando-o vencedor."""
    st = {}
    def setup():
        rei = Rei('rei'); rei.sorriso = 1.0; rei.brava = 0.0
        rei.criar(1419.88, YT1 + rei.ALT_CHAO, -1465.80, ori=(-6, 0, 0), pose='anuncia')
        ping = PingCapivara('ping'); ping.sorriso = 0.95; ping.fechar = 0.05
        ping.criar(1421.12, YT1 + ping.ALT_CHAO, -1465.65, ori=(0, 0, 0), pose='vencedor')
        vp = criar_vaso('vaso', 'vazio')
        vp.criar(1421.38, YT1 + 0.46, -1465.09, ori=(0, 0, 0))
        st['rei'] = rei; st['ping'] = ping
    def ini(ev):
        snd_cam('entity.player.levelup', 0.65, 1.25)
    def tick(t, kk, ev):
        if kk == 6:
            st['rei'].boca_ab = 0.45; st['rei'].posar(juntas={'braco_e': (-156, 0, 22)}, dur=7)
            st['ping'].posar(juntas={'braco_d': (-166, 0, -18), 'cabeca': (-10, -8, 6)}, dur=7)
            C('particle end_rod 1420.55 72.15 -1465.5 0.5 0.5 0.4 0.01 8 force')
    gravar_plano('P30', (1420.55, YT1 + 1.65, -1462.15), (1420.55, YT1 + 1.55, -1465.8), (0.0, 0.06, -0.45), setup, tick, ini)


def p_P31():
    """Reacao em plano conjunto dos tres rivais boquiabertos e chocados atras de suas plantas enormes."""
    st = {}
    def setup():
        rivs = []
        cores = ['green_terracotta', 'blue_terracotta', 'brown_terracotta']
        flores = ['flor_rosa', 'flor_ouro', 'flor_azul']
        for i, xk in enumerate([1417.1, 1418.8, 1420.5]):
            r = Rival(tag=f'riv{i+1}', cor=cores[i])
            r.fechar = 0.0; r.boca_ab = 0.85; r.sorriso = 0.0
            r.criar(xk, YS + r.ALT_CHAO, -1448.0, ori=(180, 0, 0), pose='segura_vaso')
            rivs.append(r)
            v = criar_vaso(tag=f'vaso{i+1}', tipo=flores[i])
            v.criar(xk, YS + 0.80, -1448.48, ori=(180, 0, 0))
        st['rivs'] = rivs
    def tick(t, kk, ev):
        if kk == 4:
            for r in st['rivs']:
                r.boca_ab = 1.0
            posar_varios([(st['rivs'][0], {'pose': 'chocado', 'juntas': {'cabeca': (-8, 12, 0)}}),
                          (st['rivs'][1], {'pose': 'chocado', 'juntas': {'cabeca': (-10, 0, 0)}}),
                          (st['rivs'][2], {'pose': 'chocado', 'juntas': {'cabeca': (-8, -12, 0)}})], dur=5)
            snd_cam('entity.villager.no', 0.55, 1.2)
    gravar_plano('P31', (1418.8, YS + 1.72, -1452.65), (1418.8, YS + 1.52, -1448.2), (0.20, 0.03, 0.35), setup, tick)


# ==============================================================================
# BLOCO 8: P32..P35 — Flashback na Camara da Caldeira (sementes fervidas)
# ==============================================================================

def _montar_cena_panela():
    # Substitui temporariamente o campfire por magma_block para fumaca marrom densa nao tapar os closes!
    C('setblock 1456 69 -1456 magma_block')
    C('setblock 1456 70 -1456 air')
    pan = criar_panela_fervendo('panela')
    pan.criar(1456.5, YS + 1.0, -1455.5)
    return pan


def p_P32():
    """Flashback na camara real (vista frontal limpa pelo sul): Rei em pe atras do caldeirao fervendo."""
    def setup():
        _montar_cena_panela()
        rei = Rei('rei'); rei.brava = 0.25
        rei.criar(1456.5, YS + rei.ALT_CHAO, -1456.45, ori=(0, 0, 0), pose='hashi')
    def ini(ev):
        snd_cam('block.campfire.crackle', 1.0, 1.0)
    def tick(t, kk, ev):
        if kk % 4 == 0:
            C('particle bubble_pop 1456.5 70.50 -1455.5 0.18 0.04 0.18 0.02 8 force')
            C('particle splash 1456.5 70.52 -1455.5 0.18 0.02 0.18 0.02 6 force')
    gravar_plano('P32', (1456.15, YS + 2.02, -1452.55), (1456.5, YS + 1.55, -1455.85), (0.12, -0.04, -0.38), setup, tick, ini)


def p_P33():
    """Close frontal limpo do caldeirao fervendo enquanto o Rei despeja as sementes na agua borbulhante."""
    def setup():
        _montar_cena_panela()
        rei = Rei('rei'); rei.brava = 0.2
        rei.criar(1456.85, YS + rei.ALT_CHAO, -1456.42, ori=(18, 0, 0), pose='entrega')
        spawn_semente_pequena('semente_mao', 1456.52, 70.98, -1455.52)
        tr = TrajetoJogo('@e[tag=semente_mao]', lambda t: (1456.52, max(70.30, 70.98 - 0.82 * t), -1455.52), passo=0.15)
        return [tr]
    def ini(ev):
        snd_cam('block.campfire.crackle', 0.85, 1.1)
    def tick(t, kk, ev):
        if kk % 3 == 0:
            C('particle splash 1456.5 70.52 -1455.5 0.20 0.04 0.20 0.03 10 force')
            C('particle bubble_pop 1456.5 70.50 -1455.5 0.18 0.04 0.18 0.02 8 force')
        if kk == 8:
            snd_cam('entity.generic.splash', 0.65, 1.4)
    gravar_plano('P33', (1456.32, 70.88, -1453.85), (1456.55, 70.48, -1455.55), (0.08, -0.03, -0.22), setup, tick, ini)


def p_P34():
    """Plongee cristalino dentro da panela real mostrando todas as 6 sementes entre bolhas intensas."""
    def setup():
        _montar_cena_panela()
    def ini(ev):
        snd_cam('block.bubble_column.upwards_ambient', 1.0, 1.0)
    def tick(t, kk, ev):
        if kk % 3 == 0:
            C('particle bubble_pop 1456.5 70.50 -1455.5 0.22 0.05 0.22 0.02 12 force')
            C('particle splash 1456.5 70.52 -1455.5 0.18 0.03 0.18 0.02 6 force')
    gravar_plano('P34', (1456.5, 71.68, -1454.82), (1456.5, 70.30, -1455.52), (0.0, -0.16, -0.10), setup, tick, ini)


def p_P35():
    """Super close macro nitido de uma semente escura cozida e rachada erguida entre dois hashis de bambu."""
    st = {}
    def setup():
        _montar_cena_panela()
        sh = criar_semente_hashi('sem_hashi', cozida=True)
        sh.criar(1456.5, 71.35, -1455.5, ori=(0, 0, 0))
        st['sh'] = sh
    def ini(ev):
        snd_cam('block.campfire.crackle', 0.6, 1.2)
    def tick(t, kk, ev):
        if kk == 8:
            st['sh'].posar(ori=(14, 0, 0), dur=12)
    gravar_plano('P35', (1456.38, 71.42, -1454.38), (1456.5, 71.33, -1455.5), (0.08, 0.0, -0.15), setup, tick, ini)


# ==============================================================================
# BLOCO 9: P36..P39 — A sabedoria do Rei e a vergonha dos rivais que trapacearam
# ==============================================================================

def p_P36():
    """Retorno ao Salao Imperial: close firme do Rei olhando do alto com sabedoria."""
    st = {}
    def setup():
        rei = Rei('rei'); rei.sorriso = 0.35; rei.brava = 0.1
        rei.criar(1420.5, YT2 + rei.ALT_CHAO, -1469.5, ori=(0, 0, 0), pose='maos_costas')
        st['rei'] = rei
    def tick(t, kk, ev):
        if kk == 7:
            st['rei'].sorriso = 0.65; st['rei'].posar(juntas={'cabeca': (10, 5, 0)}, dur=9)
    gravar_plano('P36', (1419.8, YT2 + 2.22, -1467.0), (1420.5, YT2 + 2.15, -1469.5), (0.16, 0.02, -0.25), setup, tick)


def p_P37():
    """Plano pelas costas dos tres rivais diante do Rei ao fundo no trono, cocando a nuca tensos."""
    st = {}
    def setup():
        rei = Rei('rei'); rei.criar(1420.5, YT2 + rei.ALT_CHAO, -1469.5, ori=(0, 0, 0), pose='maos_costas')
        rivs = []
        cores = ['green_terracotta', 'blue_terracotta', 'brown_terracotta']
        flores = ['flor_rosa', 'flor_ouro', 'flor_azul']
        for i, xk in enumerate([1419.1, 1420.5, 1421.9]):
            r = Rival(f'riv{i+1}', cores[i])
            r.criar(xk, YS + r.ALT_CHAO, -1456.0, ori=(180, 0, 0), pose='coca_cabeca1' if i != 1 else 'pe')
            rivs.append(r)
            v = criar_vaso(f'vaso{i+1}', flores[i])
            v.criar(xk + 0.38, YS, -1456.45)
        st['rivs'] = rivs
    def tick(t, kk, ev):
        if kk % 5 == 0:
            p_alt = 'coca_cabeca2' if (kk // 5) % 2 == 0 else 'coca_cabeca1'
            posar_varios([(st['rivs'][0], {'pose': p_alt}), (st['rivs'][1], {'pose': p_alt}), (st['rivs'][2], {'pose': p_alt})], dur=5)
    gravar_plano('P37', (1420.5, YS + 1.92, -1451.6), (1420.5, YS + 1.75, -1461.5), (0.0, 0.03, -0.35), setup, tick)


def p_P38():
    """Close frontal conjunto dos tres rivais cocando a cabeca envergonhados por terem trapaceado."""
    st = {}
    def setup():
        rivs = []
        cores = ['green_terracotta', 'blue_terracotta', 'brown_terracotta']
        for i, xk in enumerate([1419.1, 1420.5, 1421.9]):
            r = Rival(f'riv{i+1}', cores[i]); r.fechar = 0.45; r.boca_ab = 0.0; r.sorriso = 0.0
            r.criar(xk, YS + r.ALT_CHAO, -1456.0, ori=(180, 0, 0), pose='coca_cabeca1')
            rivs.append(r)
        st['rivs'] = rivs
    def tick(t, kk, ev):
        if kk % 5 == 0:
            p_alt = 'coca_cabeca2' if (kk // 5) % 2 == 0 else 'coca_cabeca1'
            posar_varios([(st['rivs'][0], {'pose': p_alt}), (st['rivs'][1], {'pose': p_alt}), (st['rivs'][2], {'pose': p_alt})], dur=5)
    gravar_plano('P38', (1420.2, YS + 1.72, -1460.15), (1420.5, YS + 1.58, -1456.0), (0.24, -0.02, 0.18), setup, tick)


def p_P39():
    """Plano lateral dos rivais cabisbaixos desviando o olhar ao lado dos vasos com plantas falsas."""
    st = {}
    def setup():
        rivs, _, _ = spawn_fila_jovens(com_vasos=True, pose_riv='segura_vaso', pose_ping=None, z_fila=-1448.0)
        for r in rivs:
            r.fechar = 0.65
        posar_varios([(r, {'juntas': {'cabeca': (28, 18, 0)}}) for r in rivs], dur=2)
        st['rivs'] = rivs
    def tick(t, kk, ev):
        if kk == 7:
            posar_varios([(r, {'juntas': {'cabeca': (34, 24, 0)}}) for r in st['rivs']], dur=10)
    gravar_plano('P39', (1414.4, YS + 1.55, -1449.65), (1418.8, YS + 1.38, -1448.2), (0.45, -0.04, 0.12), setup, tick)


# ==============================================================================
# BLOCO 10: P40..P43 — Honestidade de Ping, Coroacao Imperial e Plano Final
# ==============================================================================

def p_P40():
    """Close sereno e iluminado da Capivara Ping honesta diante do degrau do trono segurando seu vaso vazio."""
    st = {}
    def setup():
        ping = PingCapivara('ping'); ping.fechar = 0.1; ping.sorriso = 0.65
        ping.criar(1420.5, YT1 + ping.ALT_CHAO, -1465.5, ori=(0, 0, 0), pose='segura_vaso')
        vp = criar_vaso('vaso', 'vazio')
        vp.criar(1420.5, YT1 + 0.46, -1464.94, ori=(0, 0, 0))
        st['ping'] = ping
    def tick(t, kk, ev):
        if kk == 7:
            st['ping'].sorriso = 0.95; st['ping'].posar(juntas={'cabeca': (-4, 0, 3)}, dur=8)
    gravar_plano('P40', (1419.85, YT1 + 1.35, -1463.25), (1420.5, YT1 + 1.18, -1465.3), (0.14, 0.02, -0.22), setup, tick)


def p_P41():
    """Detalhe solene das maos do Rei erguendo a Coroa Imperial dourada diante da Capivara Ping."""
    def setup():
        rei = Rei('rei', com_coroa=False); rei.sorriso = 0.85
        rei.criar(1420.5, YT1 + rei.ALT_CHAO, -1466.40, ori=(0, 0, 0), pose='coroando')
        ping = PingCapivara('ping'); ping.sorriso = 0.75; ping.fechar = 0.18
        ping.criar(1420.5, YT1 + ping.ALT_CHAO, -1465.35, ori=(0, 0, 0), pose='segura_vaso')
        vp = criar_vaso('vaso', 'vazio')
        vp.criar(1420.5, YT1 + 0.46, -1464.79, ori=(0, 0, 0))
        coroa = criar_coroa_imperial('coroa_solta')
        coroa.criar(1420.5, YT1 + 2.12, -1465.35, ori=(0, 0, 0), tdur=4)
        tr_c = TrajetoJogo('@e[tag=coroa_solta]', lambda t: (1420.5, YT1 + 2.12 - 0.18 * t, -1465.35), passo=0.15)
        return [tr_c]
    def ini(ev):
        snd_cam('block.amethyst_block.resonate', 0.8, 1.1)
    gravar_plano('P41', (1419.32, YT1 + 2.02, -1463.65), (1420.5, YT1 + 1.92, -1465.45), (0.18, -0.04, -0.18), setup, fn_inicio=ini)


def p_P42():
    """Contra-plongee emocionante do Rei descendo a Coroa Imperial dourada sobre a cabeca de Ping."""
    st = {}
    def setup():
        rei = Rei('rei', com_coroa=False); rei.sorriso = 0.95
        rei.criar(1420.5, YT1 + rei.ALT_CHAO, -1466.40, ori=(0, 0, 0), pose='coroando')
        ping = PingCapivara('ping'); ping.sorriso = 0.85; ping.fechar = 0.0; ping.boca_ab = 0.35
        ping.criar(1420.5, YT1 + ping.ALT_CHAO, -1465.35, ori=(0, 0, 0), pose='coroado')
        vp = criar_vaso('vaso', 'vazio')
        vp.criar(1420.5, YT1 + 0.46, -1464.79, ori=(0, 0, 0))
        coroa = criar_coroa_imperial('coroa_solta')
        coroa.criar(1420.5, YT1 + 2.02, -1465.35, ori=(0, 0, 0), tdur=4)
        tr_c = TrajetoJogo('@e[tag=coroa_solta]', lambda t: (1420.5, max(YT1 + 1.64, YT1 + 2.02 - 0.34 * t), -1465.35), passo=0.15)
        st['ping'] = ping; st['rei'] = rei
        return [tr_c]
    def ini(ev):
        snd_cam('block.amethyst_block.chime', 1.0, 1.0)
    def tick(t, kk, ev):
        if kk == 16:
            st['ping'].boca_ab = 0.0; st['ping'].sorriso = 1.0
            st['ping'].posar(juntas={'cabeca': (-3, 0, 0)}, dur=8)
            st['rei'].posar(juntas={'braco_e': (-96, 0, -18), 'braco_d': (-96, 0, 18)}, dur=8)
            C('particle end_rod 1420.5 71.78 -1465.35 0.35 0.25 0.35 0.01 10 force')
            snd_cam('entity.experience_orb.pickup', 0.65, 1.15)
    gravar_plano('P42', (1419.62, YT1 + 1.25, -1463.15), (1420.5, YT1 + 1.68, -1465.55), (0.16, 0.05, -0.22), setup, tick, ini)


def p_P43():
    """Plano final emocionante: Rei visivel ao lado/atras com a mao no ombro de Ping coroado segurando o vaso vazio."""
    st = {}
    def setup():
        rei = Rei('rei', com_coroa=False); rei.sorriso = 1.0; rei.fechar = 0.15
        rei.criar(1419.76, YT1 + rei.ALT_CHAO, -1465.92, ori=(-14, 0, 0), pose='ombro')
        ping = PingCapivara('ping'); ping.sorriso = 1.0; ping.fechar = 0.12
        ping.criar(1420.72, YT1 + ping.ALT_CHAO, -1465.25, ori=(0, 0, 0), pose='coroado')
        vp = criar_vaso('vaso', 'vazio')
        vp.criar(1420.72, YT1 + 0.46, -1464.69, ori=(0, 0, 0))
        coroa = criar_coroa_imperial('coroa_solta')
        coroa.criar(1420.72, YT1 + 1.64, -1465.25, ori=(0, 0, 0))
        st['ping'] = ping; st['rei'] = rei
    def ini(ev):
        snd_cam('block.amethyst_block.chime', 0.9, 1.25)
    def tick(t, kk, ev):
        if kk == 10:
            st['ping'].fechar = 0.9; st['ping'].posar(dur=3)
        elif kk == 13:
            st['ping'].fechar = 0.12; st['ping'].posar(juntas={'cabeca': (-4, 0, 3)}, dur=8)
            st['rei'].posar(juntas={'cabeca': (12, -10, 2)}, dur=10)
    gravar_plano('P43', (1420.28, YT1 + 1.54, -1462.55), (1420.28, YT1 + 1.46, -1465.55), (0.0, 0.02, -0.24), setup, tick, ini)


# ==============================================================================
# BLOCO 11: P44..P47 — Epilogo (> 1 min): Ping no Trono e o Reino Florescendo
# ==============================================================================

def p_P44():
    """Capivara Ping coroada sentada com nobreza no Trono Dourado enquanto o velho Rei sorri orgulhoso ao lado."""
    st = {}
    def setup():
        ping = PingCapivara('ping'); ping.sorriso = 1.0; ping.fechar = 0.10
        ping.criar(1420.5, 71.96, -1470.35, ori=(0, 0, 0), pose='sentado_trono')
        coroa = criar_coroa_imperial('coroa_solta')
        coroa.criar(1420.5, 72.80, -1470.35, ori=(0, 0, 0))
        rei = Rei('rei', com_coroa=False); rei.sorriso = 1.0; rei.fechar = 0.15
        # Em pe diante do braco esquerdo do trono (z=-1469.45) 100% visivel ao lado de Ping!
        rei.criar(1419.05, YT2 + rei.ALT_CHAO, -1469.45, ori=(-28, 0, 0), pose='maos_costas')
        st['ping'] = ping; st['rei'] = rei
    def ini(ev):
        snd_cam('block.amethyst_block.chime', 0.85, 1.15)
    def tick(t, kk, ev):
        if kk == 10:
            st['ping'].posar(juntas={'braco_d': (-128, 0, -22), 'cabeca': (-5, 5, 4)}, dur=8)
            C('particle end_rod 1420.8 73.15 -1470.1 0.35 0.25 0.25 0.008 4 force')
    gravar_plano('P44', (1421.25, 72.28, -1466.55), (1419.85, 72.25, -1470.15), (-0.24, 0.03, -0.30), setup, tick, ini)


def p_P45():
    """No Salao Imperial, Ping coroado entrega sementes vivas e verdes aos tres jovens sorridentes."""
    st = {}
    def setup():
        ping = PingCapivara('ping'); ping.sorriso = 1.0; ping.fechar = 0.10
        ping.criar(1420.5, YS + ping.ALT_CHAO, -1450.85, ori=(0, 0, 0), pose='recebe')
        coroa = criar_coroa_imperial('coroa_solta')
        coroa.criar(1420.5, YS + 1.64, -1450.85, ori=(0, 0, 0))
        rivs = []
        cores = ['green_terracotta', 'blue_terracotta', 'brown_terracotta']
        for i, xk in enumerate([1419.1, 1420.5, 1421.9]):
            r = Rival(f'riv{i+1}', cores[i]); r.sorriso = 0.95; r.fechar = 0.12
            ori_r = ori_para((xk, YS, -1448.95), (1420.5, YS, -1450.85))
            r.criar(xk, YS + r.ALT_CHAO, -1448.95, ori=ori_r, pose='recebe')
            rivs.append(r)
            spawn_semente_pequena('semente_mao', xk, YS + 0.98, -1449.42)
        spawn_semente_pequena('semente_mao', 1420.5, YS + 0.80, -1450.22)
        st['ping'] = ping; st['rivs'] = rivs
    def ini(ev):
        snd_cam('item.crop.plant', 0.9, 1.25)
    def tick(t, kk, ev):
        if kk == 10:
            posar_varios([(r, {'juntas': {'cabeca': (14, 0, 0)}}) for r in st['rivs']], dur=8)
            snd_cam('entity.experience_orb.pickup', 0.55, 1.3)
    gravar_plano('P45', (1417.05, YS + 1.68, -1449.85), (1420.5, YS + 1.28, -1449.90), (0.18, -0.02, -0.05), setup, tick, ini)


def p_P46():
    """Close radiante no jardim ensolarado: o vaso de Ping nas patinhas agora desabrocha numa grande flor dourada real."""
    st = {}
    def setup():
        ping = PingCapivara('ping'); ping.sorriso = 1.0; ping.fechar = 0.08
        ppos = (1425.7, YG + PingCapivara.ALT_CHAO, -1340.1)
        ori = (180, 0, 0)
        ping.criar(*ppos, ori=ori, pose='segura_vaso')
        coroa = criar_coroa_imperial('coroa_solta')
        coroa.criar(ppos[0], YG + 1.64, ppos[2], ori=ori)
        vf = criar_vaso('vaso', 'flor_ouro')
        vf.criar(ppos[0], YG + 0.46, ppos[2] - 0.58, ori=ori)
        st['ping'] = ping
    def ini(ev):
        snd_cam('block.amethyst_block.resonate', 0.9, 1.3)
    def tick(t, kk, ev):
        if kk % 4 == 0:
            C('particle cherry_leaves 1425.7 68.1 -1340.5 0.9 0.5 0.9 0.01 5 force')
    gravar_plano('P46', (1424.85, YG + 1.38, -1342.15), (1425.70, YG + 1.18, -1340.45), (0.12, 0.03, 0.14), setup, tick, ini)


def p_P47():
    """Plano final epico em grua no Jardim de Cerejeiras: Ping coroado com seu vaso florido ao lado do sabio Rei."""
    st = {}
    def setup():
        rei = Rei('rei', com_coroa=False); rei.sorriso = 1.0; rei.fechar = 0.15
        rei.criar(1426.68, YG + rei.ALT_CHAO, -1339.85, ori=(-168, 0, 0), pose='ombro')
        ping = PingCapivara('ping'); ping.sorriso = 1.0; ping.fechar = 0.10
        ping.criar(1425.72, YG + PingCapivara.ALT_CHAO, -1340.25, ori=(180, 0, 0), pose='coroado')
        coroa = criar_coroa_imperial('coroa_solta')
        coroa.criar(1425.72, YG + 1.64, -1340.25, ori=(180, 0, 0))
        vf = criar_vaso('vaso', 'flor_ouro')
        vf.criar(1425.72, YG + 0.46, -1340.83, ori=(180, 0, 0))
        # Tambem vasos floridos decorando o jardim ao redor
        v1 = criar_vaso('vaso1', 'flor_rosa'); v1.criar(1423.8, YG, -1341.2)
        v2 = criar_vaso('vaso2', 'flor_azul'); v2.criar(1427.8, YG, -1341.0)
        st['ping'] = ping; st['rei'] = rei
    def ini(ev):
        snd_cam('block.amethyst_block.chime', 1.0, 1.2)
    def tick(t, kk, ev):
        if kk % 4 == 0:
            C('particle cherry_leaves 1425.8 68.2 -1341.0 1.6 0.8 1.6 0.01 6 force')
        if kk == 16:
            st['ping'].posar(juntas={'cabeca': (-6, 0, 4)}, dur=10)
    gravar_plano('P47', (1426.15, YG + 1.58, -1343.25), (1426.15, YG + 1.48, -1340.15), (-0.08, 0.30, -0.55), setup, tick, ini)


# ==============================================================================
# EXECUCAO COMPLETA E RETOMAVEL
# ==============================================================================

TODOS = [f'P{i:02d}' for i in range(1, 48)]


def main():
    raw_args = [a for a in sys.argv[1:] if a != '--refazer']
    refazer = '--refazer' in sys.argv
    nomes = TODOS if (not raw_args or raw_args == ['todos']) else raw_args
    preparar_estudo_mcp()
    t_global = time.perf_counter()
    try:
        for n in nomes:
            idx, meta = PLANOS_IDX[n]
            out_v = os.path.join(TMP_SEG, f'v{idx:02d}.mp4')
            out_a = os.path.join(TMP_SEG, f'a{idx:02d}.wav')
            if not refazer and os.path.exists(out_v) and os.path.getsize(out_v) > 5000 and os.path.exists(out_a):
                print(f'=== PULANDO {n} (ja existe v{idx:02d}.mp4) ===', flush=True)
                continue
            print(f'=== [{idx+1}/43] GRAVANDO {n} ({float(meta["t1"]) - float(meta["t0"]):.2f}s) ===', flush=True)
            globals()['p_' + n]()
    finally:
        C('tick rate 20')
        C('setblock 1456 69 -1456 campfire[lit=true]')
        C('setblock 1456 70 -1456 water_cauldron[level=3]')
        limpar_cena(tempo_sol=3500)
        print(f'=== CONCLUIDO em {(time.perf_counter() - t_global) / 60:.1f} min ===', flush=True)


if __name__ == '__main__':
    main()
