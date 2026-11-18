"""Construcao completa e retomavel do cenario cinematografico 'O Vaso Vazio' (D:\\minecraft\\vaso).
Uso: python set_vaso.py <etapa> [...]   (ou 'tudo' para todas as etapas + 'fotos' para verificacao)
Etapas: estudio base serra naturalizar palacio cozinha jardim paisagismo fotos"""
import sys, os, math, random, time, json, http.client, base64

DIR_FERR = os.path.dirname(os.path.abspath(__file__))
if DIR_FERR not in sys.path:
    sys.path.insert(0, DIR_FERR)
_FERR_REPO = os.path.abspath(os.path.join(DIR_FERR, '..', '..', 'ferramentas', 'animacao-no-jogo'))
if os.path.isdir(_FERR_REPO) and _FERR_REPO not in sys.path:
    sys.path.insert(0, _FERR_REPO)

import mc
from config_vaso import SET, Y, MAR, YP, YJ

PL = os.environ.get('MC_JOGADOR', '@p')
BASE_Y = 56
PROJ = os.environ.get('ANIM_PROJETO', os.getcwd())
CK_DIR = os.path.join(PROJ, 'checkpoints')
TMP_DIR = os.path.join(PROJ, 'tmp')
os.makedirs(CK_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

PROG_FILE = os.path.join(CK_DIR, 'set_vaso_feito.txt')
FEITO = set(open(PROG_FILE).read().split()) if os.path.exists(PROG_FILE) else set()

# Conexao HTTP persistente para acelerar milhares de comandos via ponte MCP Fabric
_BRIDGE = json.load(open(os.path.expanduser(r'~/.mcpfabric/bridge.json')))
_HOST_PORT = _BRIDGE['url'].replace('http://', '').replace('https://', '').split('/')[0]
_CONN = None
_REQ_ID = 0


def _rpc(method, params=None, timeout=30):
    global _CONN, _REQ_ID
    _REQ_ID += 1
    body = json.dumps({"jsonrpc": "2.0", "id": _REQ_ID, "method": method, "params": params or {}}).encode()
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + _BRIDGE['token'], 'Connection': 'keep-alive'}
    for tent in range(3):
        try:
            if _CONN is None:
                _CONN = http.client.HTTPConnection(_HOST_PORT, timeout=timeout)
            _CONN.request('POST', '/rpc', body=body, headers=headers)
            resp = _CONN.getresponse()
            raw = resp.read()
            r = json.loads(raw)
            if 'error' in r:
                return {'error': r['error']}
            return r.get('result')
        except Exception:
            try:
                if _CONN:
                    _CONN.close()
            except Exception:
                pass
            _CONN = None
            if tent == 2:
                return mc.call(method, params, timeout=timeout)
            time.sleep(0.15)


def C(c):
    cmd_s = c.lstrip('/')
    if cmd_s.startswith('fill ') or cmd_s.startswith('fillbiome '):
        partes = cmd_s.split(None, 7)
        if len(partes) >= 8:
            op = partes[0]
            try:
                x0, y0, z0 = int(partes[1]), int(partes[2]), int(partes[3])
                x1, y1, z1 = int(partes[4]), int(partes[5]), int(partes[6])
                resto = partes[7]
                ax, bx = min(x0, x1), max(x0, x1)
                ay, by = min(y0, y1), max(y0, y1)
                az, bz = min(z0, z1), max(z0, z1)
                lim = 20000 if op == 'fillbiome' else 32000
                dx, dy, dz = bx - ax + 1, by - ay + 1, bz - az + 1
                if dx * dy * dz > lim:
                    if dx >= dy and dx >= dz:
                        m = (ax + bx) // 2
                        C(f'{op} {ax} {ay} {az} {m} {by} {bz} {resto}')
                        return C(f'{op} {m + 1} {ay} {az} {bx} {by} {bz} {resto}')
                    elif dz >= dx and dz >= dy:
                        m = (az + bz) // 2
                        C(f'{op} {ax} {ay} {az} {bx} {by} {m} {resto}')
                        return C(f'{op} {ax} {ay} {m + 1} {bx} {by} {bz} {resto}')
                    else:
                        m = (ay + by) // 2
                        C(f'{op} {ax} {ay} {az} {bx} {m} {bz} {resto}')
                        return C(f'{op} {ax} {m + 1} {az} {bx} {by} {bz} {resto}')
            except ValueError:
                pass

    r = _rpc('command.run', {'command': cmd_s})
    if isinstance(r, dict) and not r.get('success', True):
        out = r.get('output') or r.get('error') or ''
        # Ignora aviso inofensivo quando fill replace / keep nao altera blocos
        if 'No blocks were filled' not in str(out) and 'Nothing changed' not in str(out) and 'already' not in str(out):
            print('FALHOU:', cmd_s[:150], '->', out, flush=True)
    return r


def marcar(chave):
    if chave not in FEITO:
        with open(PROG_FILE, 'a') as f:
            f.write(chave + '\n')
        FEITO.add(chave)


def tile_iter(x0, z0, x1, z1, t=64):
    for x in range(x0, x1 + 1, t):
        for z in range(z0, z1 + 1, t):
            yield x, z, min(x + t - 1, x1), min(z + t - 1, z1)


def carregar(x0, z0, x1, z1, espera=0.35):
    ax, bx = min(x0, x1), max(x0, x1)
    az, bz = min(z0, z1), max(z0, z1)
    C(f'forceload add {ax} {az} {bx} {bz}')
    if espera > 0:
        time.sleep(espera)


def descarregar(x0, z0, x1, z1):
    ax, bx = min(x0, x1), max(x0, x1)
    az, bz = min(z0, z1), max(z0, z1)
    C(f'forceload remove {ax} {az} {bx} {bz}')


def limpar_itens():
    C('kill @e[type=item]')


def onda(seed, termos):
    r = random.Random(seed)
    w = [(a, 2 * math.pi / l, r.uniform(0, 6.283), r.uniform(0, 6.283)) for a, l in termos]
    return lambda x, z: sum(a * math.sin(k * x + p) * math.cos(k * 0.77 * z + q) for a, k, p, q in w)


def ondas_dir(seed, pares):
    rnd = random.Random(seed)
    termos = []
    for amp, lam in pares:
        for _ in range(3):
            a = rnd.uniform(0, 2 * math.pi)
            termos.append((amp / 3 * 1.55, math.cos(a) * 2 * math.pi / lam, math.sin(a) * 2 * math.pi / lam, rnd.uniform(0, 6.283)))
    return lambda x, z: sum(A * math.sin(kx * x + kz * z + f) for A, kx, kz, f in termos)


# ==============================================================================
# 0. ESTUDIO / GAMERULES
# ==============================================================================
def estudio():
    try:
        mc.call('screen.close')
    except Exception:
        pass
    cmds = [
        'gamerule send_command_feedback false',
        'gamerule advance_time false',
        'gamerule advance_weather false',
        'gamerule spawn_mobs false',
        'gamerule random_tick_speed 0',
        'time set 3500',
        'weather clear',
        f'gamemode spectator {PL}',
        'kill @e[type=item]',
    ]
    for c in cmds:
        C(c)
    print('Estudio configurado (time=3500, weather=clear, gamerules OK).', flush=True)


# ==============================================================================
# 1. BASE DA ILHA + PRAIAS ORGANICAS
# ==============================================================================
LARG_COSTA = onda(17, [(13, 150), (7, 62), (3.5, 25)])


def _linha_costa(x, z, dx, dz):
    w = int(max(9, 20 + LARG_COSTA(x, z)))
    xa, za = x + dx * (w - 6), z + dz * (w - 6)
    xs, zs = sorted((x, xa)), sorted((z, za))
    C(f'fill {xs[0]} {BASE_Y} {zs[0]} {xs[1]} {Y - 1} {zs[1]} dirt')
    C(f'fill {xs[0]} {Y} {zs[0]} {xs[1]} {Y} {zs[1]} grass_block')
    for i, yy in enumerate([Y - 1, MAR, MAR, MAR - 1, MAR - 2, MAR - 3]):
        px, pz = x + dx * (w - 5 + i), z + dz * (w - 5 + i)
        C(f'fill {px} {BASE_Y} {pz} {px} {yy} {pz} sand')
    C(f'fill {min(x, x - dx * 2)} {Y} {min(z, z - dz * 2)} {max(x, x - dx * 2)} {Y} {max(z, z - dz * 2)} grass_block replace sand')


def base():
    estudio()
    x0, z0, x1, z1 = SET['canvas']  # 1290, -1530, 1550, -1250
    for a, b, c, d in tile_iter(x0, z0, x1, z1, 128):
        k = f'base_{a}_{b}'
        if k in FEITO:
            continue
        C(f'tp {PL} {(a + c) // 2} 135 {(b + d) // 2}')
        carregar(a, b, c, d, 0.45)
        for tx0, tz0, tx1, tz1 in tile_iter(a, b, c, d, 64):
            for y in range(Y + 1, 136, 12):
                C(f'fill {tx0} {y} {tz0} {tx1} {min(y + 11, 135)} {tz1} air')
            C(f'fill {tx0} {BASE_Y} {tz0} {tx1} {Y - 3} {tz1} stone')
            C(f'fill {tx0} {Y - 2} {tz0} {tx1} {Y - 1} {tz1} dirt')
            C(f'fill {tx0} {Y} {tz0} {tx1} {Y} {tz1} grass_block')
            C(f'fillbiome {tx0} {BASE_Y} {tz0} {tx1} 135 {tz1} minecraft:flower_forest')
        descarregar(a, b, c, d)
        marcar(k)
        print('base tile', a, b, flush=True)

    # Costa organica nos 4 lados descendo ate MAR=62
    lados = [
        ('o', [(x0 - 1, z) for z in range(z0 - 2, z1 + 3)], -1, 0),
        ('l', [(x1 + 1, z) for z in range(z0 - 2, z1 + 3)], 1, 0),
        ('n', [(x, z0 - 1) for x in range(x0 - 2, x1 + 3)], 0, -1),
        ('s', [(x, z1 + 1) for x in range(x0 - 2, x1 + 3)], 0, 1),
    ]
    for nome, pts, dx, dz in lados:
        for i in range(0, len(pts), 48):
            k = f'costa_{nome}_{i}'
            if k in FEITO:
                continue
            grupo = pts[i:i + 48]
            xs = [p[0] for p in grupo] + [p[0] + dx * 42 for p in grupo]
            zs = [p[1] for p in grupo] + [p[1] + dz * 42 for p in grupo]
            carregar(min(xs) - 4, min(zs) - 4, max(xs) + 4, max(zs) + 4, 0.35)
            C(f'fillbiome {min(xs) - 2} {BASE_Y} {min(zs) - 2} {max(xs) + 2} 100 {max(zs) + 2} minecraft:flower_forest')
            for (px, pz) in grupo:
                _linha_costa(px, pz, dx, dz)
            descarregar(min(xs) - 4, min(zs) - 4, max(xs) + 4, max(zs) + 4)
            marcar(k)
            print('costa', nome, i, flush=True)
    limpar_itens()


# ==============================================================================
# 2. SERRAS AO NORTE, SUL E COLINAS LESTE/OESTE (ANEL 360 SEM FIM DE CHUNK)
# ==============================================================================
RIDGE_S = onda(29, [(1.0, 130), (0.62, 56), (0.32, 24)])
COL_S = onda(41, [(1.0, 180), (0.55, 75)])
MANCHA_S = onda(53, [(1.0, 52), (0.5, 21)])


def _smooth(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def h_anel_serra(x, z):
    """Retorna altura acima de Y=64 para o anfiteatro de serras N/S e colinas L/O."""
    x0, z0, x1, z1 = SET['canvas']  # 1290, -1530, 1550, -1250
    rid = 1.0 - min(1.0, abs(RIDGE_S(x, z)) / 1.85)
    ond = COL_S(x, z)

    # Serra Norte: Z = -1605 .. -1508 (pico em torno de Z=-1558)
    hn = 0.0
    if -1610 <= z <= -1506:
        sobe = _smooth((-1506 - z) / 38.0)
        desce = _smooth((z - (-1610)) / 42.0)
        ext = min(_smooth((x - 1215) / 55.0), _smooth((1625 - x) / 55.0))
        hn = sobe * desce * ext * (32 + 34 * rid * rid + 8 * ond)

    # Serra Sul: Z = -1264 .. -1170 (pico em torno de Z=-1215)
    hs = 0.0
    if -1266 <= z <= -1168:
        sobe = _smooth((z - (-1266)) / 38.0)
        desce = _smooth((-1168 - z) / 42.0)
        ext = min(_smooth((x - 1215) / 55.0), _smooth((1625 - x) / 55.0))
        hs = sobe * desce * ext * (29 + 31 * rid * rid + 7 * ond)

    # Colinas Oeste: X = 1220 .. 1316
    hw = 0.0
    if 1218 <= x <= 1318:
        sobe = _smooth((1318 - x) / 40.0)
        desce = _smooth((x - 1218) / 42.0)
        ext = min(_smooth((z - (-1600)) / 50.0), _smooth((-1175 - z) / 50.0))
        hw = sobe * desce * ext * (16 + 20 * rid * rid + 5 * ond)

    # Colinas Leste: X = 1524 .. 1622
    he = 0.0
    if 1522 <= x <= 1622:
        sobe = _smooth((x - 1522) / 40.0)
        desce = _smooth((1622 - x) / 42.0)
        ext = min(_smooth((z - (-1600)) / 50.0), _smooth((-1175 - z) / 50.0))
        he = sobe * desce * ext * (16 + 20 * rid * rid + 5 * ond)

    return max(hn, hs, hw, he)


def serra():
    estudio()
    xa, xb, za, zb = 1220, 1620, -1608, -1170
    for a, b, c, d in tile_iter(xa, za, xb, zb, 64):
        k = f'serra_{a}_{b}'
        if k in FEITO:
            continue
        # Verifica rapido se o tile tem alguma montanha
        amostra = max(h_anel_serra(tx, tz) for tx in range(a, c + 1, 8) for tz in range(b, d + 1, 8))
        if amostra < 1.0:
            marcar(k)
            continue
        C(f'tp {PL} {(a + c) // 2} 145 {(b + d) // 2}')
        carregar(a, b, c, d, 0.35)
        C(f'fillbiome {a} {BASE_Y} {b} {c} 150 {d} minecraft:flower_forest')
        passo = 2
        for x in range(a, c + 1, passo):
            z = b
            while z <= d:
                h = int(round(h_anel_serra(x + 0.5, z + 0.5)))
                if h < 1:
                    z += passo
                    continue
                z2 = z
                while z2 + passo <= d and int(round(h_anel_serra(x + 0.5, z2 + passo + 0.5))) == h:
                    z2 += passo
                x_end = min(c, x + passo - 1)
                z_end = min(d, z2 + passo - 1)
                top = Y + h
                m = MANCHA_S(x, z)
                rochoso = (h > 48 and m > 0.25) or (h > 34 and m > 0.85)
                if rochoso:
                    blk_top = 'andesite' if m > 0.6 else 'stone'
                    C(f'fill {x} {BASE_Y} {z} {x_end} {top} {z_end} {blk_top}')
                else:
                    blk_top = 'moss_block' if m < -0.75 else ('coarse_dirt' if m > 0.82 else 'grass_block')
                    C(f'fill {x} {BASE_Y} {z} {x_end} {max(BASE_Y, top - 4)} {z_end} stone')
                    # Usa grass_block nos 4 blocos superiores para nao expor faixa marrom de dirt em degraus ingremes!
                    C(f'fill {x} {max(BASE_Y, top - 3)} {z} {x_end} {top} {z_end} {blk_top}')
                z = z2 + passo
        descarregar(a, b, c, d)
        marcar(k)
        print('serra tile', a, b, flush=True)

    # Arvores variadas nas serras e colinas (oak, birch, spruce, cherry)
    if 'arvores_serra' not in FEITO:
        rnd = random.Random(77)
        feitas = 0
        alvos = [
            # Norte (atras do palacio) - bastante cherry, spruce e oak
            (1260, 1580, -1590, -1510, 170, ['oak', 'spruce', 'birch', 'cherry', 'oak', 'cherry', 'spruce']),
            # Sul (atras da casa do Ping) - muitas cerejeiras + carvalhos + betulas
            (1260, 1580, -1262, -1185, 160, ['cherry', 'oak', 'birch', 'cherry', 'spruce', 'oak']),
            # Colinas Oeste e Leste
            (1235, 1315, -1520, -1255, 85, ['oak', 'birch', 'cherry', 'spruce']),
            (1525, 1605, -1520, -1255, 85, ['oak', 'birch', 'cherry', 'spruce']),
        ]
        for (ax0, ax1, az0, az1, meta, tipos) in alvos:
            cnt = 0
            pts_usados = []
            for _ in range(meta * 8):
                tx = rnd.randint(ax0, ax1)
                tz = rnd.randint(az0, az1)
                h = int(round(h_anel_serra(tx, tz)))
                if not (3 <= h <= 46):
                    continue
                if MANCHA_S(tx, tz) > 0.65:
                    continue
                if any(abs(tx - ux) < 5 and abs(tz - uz) < 5 for ux, uz in pts_usados[-60:]):
                    continue
                pts_usados.append((tx, tz))
                top = Y + h
                carregar(tx - 6, tz - 6, tx + 6, tz + 6, 0.08)
                # Garante grass_block/dirt embaixo antes do place feature!
                C(f'fill {tx - 1} {top - 2} {tz - 1} {tx + 1} {top - 1} {tz + 1} dirt')
                C(f'fill {tx - 1} {top} {tz - 1} {tx + 1} {top} {tz + 1} grass_block')
                C(f'setblock {tx} {top + 1} {tz} air')
                esp = rnd.choice(tipos)
                C(f'place feature minecraft:{esp} {tx} {top + 1} {tz}')
                descarregar(tx - 6, tz - 6, tx + 6, tz + 6)
                cnt += 1
                feitas += 1
                if cnt >= meta:
                    break
            print('arvores serra regiao:', cnt, flush=True)
        limpar_itens()
        marcar('arvores_serra')
        print('Total arvores_serra:', feitas, flush=True)


def verdejar_serras():
    """Converte degraus de dirt expostos nas encostas das serras em grass_block vivo e reforca cerejeiras/bosques nos fundos."""
    estudio()
    faixas = [
        (1230, 1610, -1605, -1506),  # Serra Norte
        (1230, 1610, -1266, -1172),  # Serra Sul
        (1222, 1316, -1520, -1255),  # Colinas Oeste
        (1524, 1618, -1520, -1255),  # Colinas Leste
    ]
    for fx0, fx1, fz0, fz1 in faixas:
        for a, b, c, d in tile_iter(fx0, fz0, fx1, fz1, 64):
            C(f'tp {PL} {(a + c) // 2} 135 {(b + d) // 2}')
            carregar(a, b, c, d, 0.25)
            for y in range(65, 133, 8):
                C(f'fill {a} {y} {b} {c} {min(y + 7, 132)} {d} grass_block replace dirt')
                C(f'fill {a} {y} {b} {c} {min(y + 7, 132)} {d} grass_block replace coarse_dirt')
            descarregar(a, b, c, d)
            print('verdejar tile', a, b, flush=True)

    # Faixas de moss_block nas encostas ingremes (verde nas 6 faces, elimina degraus marrons laterais!)
    faixas_encosta = [
        (1320, 1520, -1585, -1506),  # Encosta visivel Serra Norte
        (1320, 1520, -1266, -1190),  # Encosta visivel Serra Sul
    ]
    for fx0, fx1, fz0, fz1 in faixas_encosta:
        for a, b, c, d in tile_iter(fx0, fz0, fx1, fz1, 64):
            carregar(a, b, c, d, 0.25)
            for y in range(66, 114, 8):
                C(f'fill {a} {y} {b} {c} {min(y + 7, 113)} {d} moss_block replace grass_block')
            descarregar(a, b, c, d)

    # Bosques densos de cerejeiras/carvalhos/pinheiros bem nos eixos de fundo Norte e Sul
    # (Com forceload de 16 blocos e clareira aerea para place feature funcionar 100%!)
    rnd = random.Random(314)
    extras = [
        (1355, 1485, -1555, -1512, 42, ['cherry', 'oak', 'spruce', 'cherry', 'birch']),
        (1355, 1485, -1260, -1218, 42, ['cherry', 'oak', 'birch', 'cherry', 'spruce']),
    ]
    for ax0, ax1, az0, az1, meta, tipos in extras:
        carregar(ax0 - 16, az0 - 16, ax1 + 16, az1 + 16, 0.45)
        cnt = 0
        usados = []
        for _ in range(meta * 10):
            tx, tz = rnd.randint(ax0, ax1), rnd.randint(az0, az1)
            h = int(round(h_anel_serra(tx, tz)))
            if not (3 <= h <= 34):
                continue
            if any(abs(tx - ux) < 6 and abs(tz - uz) < 6 for ux, uz in usados):
                continue
            top = Y + h
            C(f'fill {tx - 1} {top - 2} {tz - 1} {tx + 1} {top} {tz + 1} dirt')
            C(f'fill {tx - 1} {top} {tz - 1} {tx + 1} {top} {tz + 1} grass_block')
            C(f'fill {tx - 2} {top + 1} {tz - 2} {tx + 2} {top + 9} {tz + 2} air')
            r_tree = C(f'place feature minecraft:{rnd.choice(tipos)} {tx} {top + 1} {tz}')
            if isinstance(r_tree, dict) and r_tree.get('success'):
                usados.append((tx, tz))
                cnt += 1
                if cnt >= meta:
                    break
        descarregar(ax0 - 16, az0 - 16, ax1 + 16, az1 + 16)
        print('Bosque encosta plantado:', cnt, flush=True)
    limpar_itens()
    print('verdejar_serras concluido.', flush=True)


# ==============================================================================
# 3. RELEVO SUAVE (NATURALIZAR) COM MASCARA PROTETORA
# ==============================================================================
RUIDO_ILHA = ondas_dir(23, [(4.6, 130), (2.6, 68), (1.3, 32)])

# Caixas protegidas (mascara = 0)
BOX_PALACIO_AREA = (1380, -1492, 1470, -1412)
BOX_CAMINHO_AREA = (1408, -1426, 1432, -1358)
BOX_JARDIM_AREA = (1382, -1366, 1458, -1302)


def _dist_box(x, z, b):
    bx0, bz0, bx1, bz1 = b
    dx = max(bx0 - x, 0, x - bx1)
    dz = max(bz0 - z, 0, z - bz1)
    return math.hypot(dx, dz)


def mascara_ilha(x, z):
    """0 = area plana protegida (Palacio, Caminho, Jardim/Casa), 1 = colinas livres."""
    d = min(
        _dist_box(x, z, BOX_PALACIO_AREA),
        _dist_box(x, z, BOX_CAMINHO_AREA),
        _dist_box(x, z, BOX_JARDIM_AREA),
    )
    return _smooth(d / 20.0)


def naturalizar():
    estudio()
    x0, z0, x1, z1 = SET['canvas']
    alt_path = os.path.join(CK_DIR, 'alturas.json')
    alt = {}
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if h_anel_serra(x, z) >= 1.5:
                continue
            w = mascara_ilha(x, z)
            if w > 0.02:
                # Eleva suavemente as laterais leste/oeste da ilha para emoldurar o vale central
                borda_lat = _smooth(max(0.0, (1368 - x) / 55.0)) + _smooth(max(0.0, (x - 1472) / 55.0))
                h = (RUIDO_ILHA(x, z) + 3.8 * borda_lat) * w
                if h < 0:
                    h *= 0.25
                hi = int(round(h))
                if hi != 0:
                    alt[(x, z)] = hi

    json.dump({f'{k[0]},{k[1]}': v for k, v in alt.items()}, open(alt_path, 'w'))
    for a, b, c, d in tile_iter(x0, z0, x1, z1, 64):
        k = f'nat_{a}_{b}'
        if k in FEITO:
            continue
        carregar(a, b, c, d, 0.3)
        for x in range(a, c + 1):
            z = b
            while z <= d:
                h = alt.get((x, z), 0)
                z2 = z
                while z2 + 1 <= d and alt.get((x, z2 + 1), 0) == h:
                    z2 += 1
                if h > 0:
                    C(f'fill {x} {Y} {z} {x} {Y + h - 1} {z2} dirt')
                    C(f'fill {x} {Y + h} {z} {x} {Y + h} {z2} grass_block')
                elif h < 0:
                    C(f'fill {x} {Y + h + 1} {z} {x} {Y + 2} {z2} air')
                    C(f'fill {x} {Y + h} {z} {x} {Y + h} {z2} grass_block')
                z = z2 + 1
        descarregar(a, b, c, d)
        marcar(k)
        print('naturalizar tile', a, b, flush=True)
    limpar_itens()


def altura_ilha(x, z):
    hs = int(round(h_anel_serra(x, z)))
    if hs >= 2:
        return Y + hs
    if not hasattr(altura_ilha, '_H'):
        p = os.path.join(CK_DIR, 'alturas.json')
        altura_ilha._H = json.load(open(p)) if os.path.exists(p) else {}
    return Y + altura_ilha._H.get(f'{x},{z}', 0)


# ==============================================================================
# 4. GRANDE PALACIO IMPERIAL ORIENTAL VERMELHO E DOURADO
# ==============================================================================
def _telhado_pagode_camada(xa, za, xb, zb, y_base, altura_camada, preservar_box=None):
    """Constroi camada de telhado oriental curvado em dark_prismarine + bordas e cantos arrebitados dourados."""
    # Borda dourada + beiral sob o telhado (preservando o teto interno decorado se preservar_box for passado!)
    if preservar_box:
        pxa, pza, pxb, pzb = preservar_box
        C(f'fill {xa} {y_base} {za} {xb} {y_base} {pza - 1} dark_prismarine_slab[type=top]')
        C(f'fill {xa} {y_base} {pzb + 1} {xb} {y_base} {zb} dark_prismarine_slab[type=top]')
        C(f'fill {xa} {y_base} {pza} {pxa - 1} {y_base} {pzb} dark_prismarine_slab[type=top]')
        C(f'fill {pxb + 1} {y_base} {pza} {xb} {y_base} {pzb} dark_prismarine_slab[type=top]')
    else:
        C(f'fill {xa} {y_base} {za} {xb} {y_base} {zb} dark_prismarine_slab[type=top]')
    # Cantos dourados arrebitados estilo oriental (flying eaves)
    for cx, sx in [(xa, -1), (xb, 1)]:
        for cz, sz in [(za, -1), (zb, 1)]:
            C(f'fill {cx} {y_base} {cz} {cx + sx} {y_base} {cz + sz} gold_block')
            C(f'setblock {cx + sx} {y_base + 1} {cz + sz} yellow_terracotta')
            C(f'setblock {cx + sx * 2} {y_base + 1} {cz + sz * 2} bamboo_slab[type=bottom]')
            C(f'setblock {cx + sx * 2} {y_base + 2} {cz + sz * 2} gold_block')
            C(f'setblock {cx + sx * 2} {y_base} {cz + sz * 2} lantern[hanging=true]')
    # Friso dourado nas pontas das abas
    for x in range(xa + 1, xb):
        if (x - xa) % 4 == 0:
            C(f'setblock {x} {y_base} {za} yellow_terracotta')
            C(f'setblock {x} {y_base} {zb} yellow_terracotta')
    for z in range(za + 1, zb):
        if (z - za) % 4 == 0:
            C(f'setblock {xa} {y_base} {z} yellow_terracotta')
            C(f'setblock {xb} {y_base} {z} yellow_terracotta')

    # Degraus curvos subindo (curva concava oriental: 2 blocos por degrau no inicio, depois 1)
    cur_xa, cur_za, cur_xb, cur_zb = xa + 1, za + 1, xb - 1, zb - 1
    yy = y_base + 1
    for passo_i in range(altura_camada):
        if cur_xa > cur_xb or cur_za > cur_zb:
            break
        passo_in = 2 if passo_i < 2 else 1
        C(f'fill {cur_xa} {yy} {cur_za} {cur_xb} {yy} {cur_zb} dark_prismarine')
        # Escadas nas 4 bordas para suavizar a inclinacao
        C(f'fill {cur_xa} {yy} {cur_za} {cur_xb} {yy} {cur_za} dark_prismarine_stairs[facing=south]')
        C(f'fill {cur_xa} {yy} {cur_zb} {cur_xb} {yy} {cur_zb} dark_prismarine_stairs[facing=north]')
        C(f'fill {cur_xa} {yy} {cur_za} {cur_xa} {yy} {cur_zb} dark_prismarine_stairs[facing=east]')
        C(f'fill {cur_xb} {yy} {cur_za} {cur_xb} {yy} {cur_zb} dark_prismarine_stairs[facing=west]')
        # Nervuras douradas diagonais nos 4 cantos
        for rx, rz in [(cur_xa, cur_za), (cur_xa, cur_zb), (cur_xb, cur_za), (cur_xb, cur_zb)]:
            C(f'setblock {rx} {yy} {rz} yellow_terracotta')
        cur_xa += passo_in
        cur_xb -= passo_in
        cur_za += passo_in
        cur_zb -= passo_in
        yy += 1
    return cur_xa, cur_za, cur_xb, cur_zb, yy


def palacio():
    estudio()
    C(f'tp {PL} 1420 85 -1410 180 15')
    carregar(1382, -1492, 1470, -1412, 0.6)

    # Limpa volume aereo do Palacio + Praca frontal
    for y in range(Y + 1, 106, 10):
        C(f'fill 1384 {y} -1490 1468 {min(y + 9, 105)} -1414 air')
    # Garante base solida plana Y=64 ao redor
    C(f'fill 1384 {Y - 2} -1490 1468 {Y - 1} -1414 dirt')
    C(f'fill 1384 {Y} -1490 1468 {Y} -1414 grass_block')

    # Praca Imperial ao sul da escadaria (z=-1420..-1414)
    C(f'fill 1402 {Y} -1421 1438 {Y} -1414 polished_andesite')
    C(f'fill 1404 {Y} -1420 1436 {Y} -1415 stone_bricks')
    C(f'fill 1416 {Y} -1421 1424 {Y} -1414 smooth_quartz')
    C(f'fill 1418 {Y} -1421 1422 {Y} -1414 red_terracotta')

    # ------------------------------------------------------------------
    # 4.1 TERRACO ELEVADO NOBRE (x=1388..1452, z=-1486..-1424, Y=64 -> YP=68)
    # ------------------------------------------------------------------
    # Nivel inferior do terraco (y=65..66)
    C('fill 1388 65 -1486 1452 66 -1424 stone_bricks')
    C('fill 1388 66 -1486 1452 66 -1424 chiseled_stone_bricks replace stone_bricks')
    C('fill 1389 66 -1485 1451 66 -1425 polished_andesite')
    # Nivel superior do terraco (y=67..68)
    C('fill 1390 67 -1484 1450 68 -1425 polished_andesite')
    C('fill 1390 67 -1484 1450 67 -1425 stone_bricks')
    # Moldura dourada e marmore na borda de YP=68
    C('fill 1390 68 -1484 1450 68 -1484 yellow_terracotta')
    C('fill 1390 68 -1425 1450 68 -1425 yellow_terracotta')
    C('fill 1390 68 -1484 1390 68 -1425 yellow_terracotta')
    C('fill 1450 68 -1484 1450 68 -1425 yellow_terracotta')
    for x in range(1390, 1451, 6):
        C(f'setblock {x} 68 -1484 gold_block')
        C(f'setblock {x} 68 -1425 gold_block')
    for z in range(-1484, -1424, 6):
        C(f'setblock 1390 68 {z} gold_block')
        C(f'setblock 1450 68 {z} gold_block')

    # Guarda-corpo imperial de quartzo + postes dourados no perimetro do terraco (y=69)
    C('fill 1390 69 -1484 1450 69 -1484 smooth_quartz_slab[type=bottom]')
    C('fill 1390 69 -1425 1450 69 -1425 smooth_quartz_slab[type=bottom]')
    C('fill 1390 69 -1484 1390 69 -1425 smooth_quartz_slab[type=bottom]')
    C('fill 1450 69 -1484 1450 69 -1425 smooth_quartz_slab[type=bottom]')
    for x in range(1390, 1451, 6):
        for z in (-1484, -1425):
            C(f'setblock {x} 69 {z} chiseled_quartz_block')
            C(f'setblock {x} 70 {z} lantern')
    for z in range(-1484, -1424, 6):
        for x in (1390, 1450):
            C(f'setblock {x} 69 {z} chiseled_quartz_block')

    # Abre passagem no guarda-corpo sul para a Grande Escadaria Imperial (x=1408..1432)
    C('fill 1409 69 -1425 1431 70 -1425 air')

    # Grande Escadaria Imperial ao Sul (z=-1425..-1418, subindo de Y=64 ate YP=68)
    # Degraus largos com tapete imperial esculpido no centro
    degraus = [
        (-1418, 64, True),
        (-1419, 65, False),
        (-1420, 65, True),
        (-1421, 66, False),
        (-1422, 66, True),
        (-1423, 67, False),
        (-1424, 67, True),
        (-1425, 68, False),
    ]
    for zz, yy, eh_escada in degraus:
        C(f'fill 1408 64 {zz} 1432 {yy} {zz} stone_bricks')
        if eh_escada and yy < 68:
            C(f'fill 1409 {yy + 1} {zz} 1431 {yy + 1} {zz} smooth_quartz_stairs[facing=north]')
            # Rampa central vermelha e dourada
            C(f'fill 1417 {yy + 1} {zz} 1423 {yy + 1} {zz} mangrove_stairs[facing=north]')
            C(f'setblock 1416 {yy + 1} {zz} bamboo_stairs[facing=north]')
            C(f'setblock 1424 {yy + 1} {zz} bamboo_stairs[facing=north]')
        else:
            C(f'fill 1409 {yy} {zz} 1431 {yy} {zz} smooth_quartz')
            C(f'fill 1417 {yy} {zz} 1423 {yy} {zz} red_wool')
            C(f'setblock 1416 {yy} {zz} yellow_wool')
            C(f'setblock 1424 {yy} {zz} yellow_wool')
        # Balaustradas laterais da escadaria (x=1408 e x=1432)
        h_bal = min(69, yy + 2 if eh_escada else yy + 1)
        C(f'fill 1408 65 {zz} 1408 {h_bal} {zz} smooth_quartz')
        C(f'fill 1432 65 {zz} 1432 {h_bal} {zz} smooth_quartz')
        C(f'setblock 1408 {h_bal} {zz} yellow_terracotta')
        C(f'setblock 1432 {h_bal} {zz} yellow_terracotta')

    # Pilares monumentais na base e topo da escadaria
    for px in (1408, 1432):
        for pz, py in [(-1418, 66), (-1425, 70)]:
            C(f'fill {px} {py - 1} {pz} {px} {py} {pz} gold_block')
            C(f'setblock {px} {py + 1} {pz} lantern')

    # ------------------------------------------------------------------
    # 4.2 PISO DO SALAO IMPERIAL + TAPETE VERMELHO E DOURADO (YP=68)
    # ------------------------------------------------------------------
    # Salao interno: paredes em x=1395, x=1445, z=-1479, z=-1429 (palacio_box: 1392..1448, -1482..-1426)
    C('fill 1395 68 -1479 1445 68 -1429 oak_planks')
    for x in range(1396, 1445):
        for z in range(-1478, -1429):
            if (x - 1396) % 5 == 0 or (z + 1478) % 5 == 0:
                C(f'setblock {x} 68 {z} dark_oak_planks')
            elif ((x - 1396) // 5 + (z + 1478) // 5) % 2 == 0:
                C(f'setblock {x} 68 {z} stripped_oak_wood')

    # Tapete imperial central vermelho e dourado da entrada (z=-1426) ate o trono (z=-1468)
    C('fill 1416 68 -1468 1424 68 -1426 yellow_wool')
    C('fill 1417 68 -1468 1423 68 -1426 red_wool')
    for z in range(-1466, -1427, 6):
        C(f'setblock 1416 68 {z} gold_block')
        C(f'setblock 1424 68 {z} gold_block')
        C(f'setblock 1420 68 {z} yellow_terracotta')

    # ------------------------------------------------------------------
    # 4.3 PAREDES COM PAINEIS TRELICADOS CLAROS E SHROOMLIGHT AQUECIDO (y=69..79)
    # ------------------------------------------------------------------
    # Base das paredes (y=69..70): madeira escura + vermelho imperial + friso dourado
    for z in (-1479, -1429):
        C(f'fill 1395 69 {z} 1445 69 {z} dark_oak_planks')
        C(f'fill 1395 70 {z} 1445 70 {z} red_terracotta')
        C(f'fill 1395 78 {z} 1445 79 {z} red_concrete')
        C(f'fill 1395 77 {z} 1445 77 {z} yellow_terracotta')
    for x in (1395, 1445):
        C(f'fill {x} 69 -1479 {x} 69 -1429 dark_oak_planks')
        C(f'fill {x} 70 -1479 {x} 70 -1429 red_terracotta')
        C(f'fill {x} 78 -1479 {x} 79 -1429 red_concrete')
        C(f'fill {x} 77 -1479 {x} 77 -1429 yellow_terracotta')

    # Paineis trelicados claros estilo oriental (y=71..76):
    # Camada externa com shroomlight/birch_planks + trelica interna de oak_fence/quartz_pillar/bamboo_trapdoor
    # Paredes Norte e Sul (z=-1479 e z=-1429)
    for z_wall, z_out in [(-1479, -1480), (-1429, -1428)]:
        # Fundo luminoso aquecido na face externa dos paineis para brilhar luz 15 atraves das trelicas!
        C(f'fill 1396 71 {z_out} 1444 76 {z_out} birch_planks')
        for x in range(1397, 1444, 2):
            for y in (72, 75):
                C(f'setblock {x} {y} {z_out} shroomlight')
        # Moldura externa vermelha para o fundo luminoso nao parecer caixa lisa vista de fora
        for x in range(1395, 1446, 5):
            C(f'fill {x} 69 {z_out} {x} 79 {z_out} red_concrete')
            C(f'setblock {x} 69 {z_out} chiseled_quartz_block')
            C(f'setblock {x} 78 {z_out} gold_block')
        C(f'fill 1395 70 {z_out} 1445 70 {z_out} yellow_terracotta')
        C(f'fill 1395 77 {z_out} 1445 77 {z_out} gold_block')

        # Trelica na parede principal
        for x in range(1395, 1446):
            if (x - 1395) % 5 == 0:
                C(f'fill {x} 69 {z_wall} {x} 79 {z_wall} red_concrete')
                C(f'setblock {x} 69 {z_wall} chiseled_quartz_block')
                C(f'setblock {x} 77 {z_wall} gold_block')
            elif (x - 1395) % 5 in (1, 4):
                C(f'fill {x} 71 {z_wall} {x} 76 {z_wall} quartz_pillar')
                C(f'setblock {x} 71 {z_wall} red_terracotta')
                C(f'setblock {x} 76 {z_wall} red_terracotta')
            else:
                # Miolo claro trelicado de oak_fence + shroomlight/birch atras
                C(f'fill {x} 71 {z_wall} {x} 76 {z_wall} oak_fence')
                C(f'setblock {x} 73 {z_wall} birch_planks')

    # Paredes Oeste e Leste (x=1395 e x=1445)
    for x_wall, x_out in [(1395, 1394), (1445, 1446)]:
        C(f'fill {x_out} 71 -1478 {x_out} 76 -1430 birch_planks')
        for z in range(-1477, -1430, 2):
            for y in (72, 75):
                C(f'setblock {x_out} {y} {z} shroomlight')
        for z in range(-1479, -1428, 5):
            C(f'fill {x_out} 69 {z} {x_out} 79 {z} red_concrete')
            C(f'setblock {x_out} 69 {z} chiseled_quartz_block')
            C(f'setblock {x_out} 78 {z} gold_block')
        C(f'fill {x_out} 70 -1479 {x_out} 70 -1429 yellow_terracotta')
        C(f'fill {x_out} 77 -1479 {x_out} 77 -1429 gold_block')

        for z in range(-1479, -1428):
            if (z + 1479) % 5 == 0:
                C(f'fill {x_wall} 69 {z} {x_wall} 79 {z} red_concrete')
                C(f'setblock {x_wall} 69 {z} chiseled_quartz_block')
                C(f'setblock {x_wall} 77 {z} gold_block')
            elif (z + 1479) % 5 in (1, 4):
                C(f'fill {x_wall} 71 {z} {x_wall} 76 {z} quartz_pillar')
                C(f'setblock {x_wall} 71 {z} red_terracotta')
                C(f'setblock {x_wall} 76 {z} red_terracotta')
            else:
                C(f'fill {x_wall} 71 {z} {x_wall} 76 {z} oak_fence')
                C(f'setblock {x_wall} 73 {z} birch_planks')

    # Grande Portal Imperial Sul (entrada principal aberta em z=-1429..-1428, x=1416..1424, y=69..75)
    C('fill 1416 69 -1429 1424 75 -1428 air')
    # Pilares duplos monumentais ladeando o portal
    for px in (1415, 1425):
        C(f'fill {px} 69 -1430 {px} 78 -1428 red_concrete')
        C(f'fill {px} 69 -1430 {px} 69 -1428 chiseled_quartz_block')
        C(f'fill {px} 76 -1430 {px} 76 -1428 gold_block')
    # Verga imperial esculpida sobre o portal (y=76..77)
    C('fill 1416 76 -1429 1424 76 -1428 gold_block')
    C('fill 1417 75 -1429 1423 75 -1428 mangrove_stairs[facing=south,half=top]')
    C('setblock 1416 75 -1428 lantern[hanging=true]')
    C('setblock 1424 75 -1428 lantern[hanging=true]')
    C('setblock 1420 75 -1428 lantern[hanging=true]')
    # Portas secundarias laterais ao sul (x=1407..1408 e x=1432..1433)
    for ax, bx in [(1407, 1408), (1432, 1433)]:
        C(f'fill {ax} 69 -1429 {bx} 73 -1428 air')
        C(f'fill {ax} 74 -1429 {bx} 74 -1428 gold_block')

    # ------------------------------------------------------------------
    # 4.4 PILARES MONUMENTAIS INTERNOS + TETO CAISSON ILUMINADO (y=80)
    # ------------------------------------------------------------------
    # Colunata interna afastada do eixo central (x=1404 e x=1436, deixando 31 blocos livres no meio!)
    for px in (1404, 1436):
        for pz in (-1436, -1446, -1456, -1466, -1474):
            C(f'fill {px} 69 {pz} {px} 69 {pz} chiseled_quartz_block')
            for dx, dz in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                C(f'setblock {px + dx} 69 {pz + dz} smooth_quartz_stairs[facing={"east" if dx == -1 else "west" if dx == 1 else "south" if dz == -1 else "north"}]')
            C(f'fill {px} 70 {pz} {px} 77 {pz} red_concrete')
            C(f'setblock {px} 78 {pz} gold_block')
            # Capitel dougong dourado e vermelho (y=78..79)
            for dx, dz in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                C(f'setblock {px + dx} 78 {pz + dz} bamboo_stairs[facing={"west" if dx == -1 else "east" if dx == 1 else "north" if dz == -1 else "south"},half=top]')
                C(f'setblock {px + dx} 79 {pz + dz} red_terracotta')
            C(f'setblock {px} 79 {pz} gold_block')

    # Teto imperial em caixotao em y=80 (pe-direito interno livre = 11 blocos: y=69..79!)
    C('fill 1395 80 -1479 1445 80 -1429 dark_oak_planks')
    for x in range(1396, 1445):
        for z in range(-1478, -1429):
            if (x - 1404) % 8 == 0 or (z + 1474) % 8 == 0:
                C(f'setblock {x} 80 {z} red_terracotta')
            if (x - 1404) % 8 == 0 and (z + 1474) % 8 == 0:
                C(f'setblock {x} 80 {z} gold_block')
            elif (x - 1400) % 4 == 0 and (z + 1470) % 4 == 0:
                # Shroomlight embutido por todo o teto -> iluminacao 15 uniforme!
                C(f'setblock {x} 80 {z} shroomlight')

    # Lustres imperiais pendentes nas alas (y=77..79, altos para nunca cortar planos abertos!)
    for lx in (1410, 1430):
        for lz in (-1438, -1448, -1458, -1468):
            C(f'setblock {lx} 79 {lz} oak_fence')
            C(f'setblock {lx} 78 {lz} shroomlight')
            for dx, dz in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                C(f'setblock {lx + dx} 78 {lz + dz} bamboo_trapdoor[facing={"west" if dx == -1 else "east" if dx == 1 else "north" if dz == -1 else "south"},open=true]')
            C(f'setblock {lx} 77 {lz} lantern[hanging=true]')

    # ------------------------------------------------------------------
    # 4.5 TRONO IMPERIAL DOURADO EM SET['trono'] = (1420, 70, -1471) + BIOMBO
    # ------------------------------------------------------------------
    # Degrau 1 da plataforma imperial (y=69): x=1412..1428, z=-1477..-1467
    C('fill 1412 69 -1477 1428 69 -1467 smooth_quartz')
    C('fill 1413 69 -1476 1427 69 -1468 red_terracotta')
    C('fill 1412 69 -1467 1428 69 -1467 bamboo_stairs[facing=north]')
    C('fill 1417 69 -1467 1423 69 -1467 mangrove_stairs[facing=north]')
    C('fill 1412 69 -1477 1412 69 -1468 bamboo_stairs[facing=east]')
    C('fill 1428 69 -1477 1428 69 -1468 bamboo_stairs[facing=west]')
    C('setblock 1412 69 -1467 gold_block')
    C('setblock 1428 69 -1467 gold_block')
    C('setblock 1412 70 -1467 lantern')
    C('setblock 1428 70 -1467 lantern')

    # Degrau 2 da plataforma imperial (y=70): x=1414..1426, z=-1477..-1469
    C('fill 1414 70 -1477 1426 70 -1469 yellow_terracotta')
    C('fill 1415 70 -1476 1425 70 -1470 red_wool')
    C('fill 1414 70 -1469 1426 70 -1469 bamboo_stairs[facing=north]')
    C('fill 1418 70 -1469 1422 70 -1469 mangrove_stairs[facing=north]')
    C('setblock 1414 70 -1469 gold_block')
    C('setblock 1426 70 -1469 gold_block')
    # Tapete real subindo ate (1420, 70, -1471)
    C('fill 1418 70 -1473 1422 70 -1470 gold_block')
    C('fill 1419 70 -1472 1421 70 -1470 red_wool')

    # Cadeirao do Trono Imperial Dourado em (1420, 70, -1471):
    # Almofada plana em y=71.50 (mangrove_slab[type=bottom]) sem parede frontal, para sentar sem colisao!
    C('fill 1419 71 -1471 1421 71 -1471 mangrove_slab[type=bottom]')
    # Bracos de ouro proporcionais (x=1418 e x=1422, altura y=72.50 nos apoios)
    for bx in (1418, 1422):
        C(f'fill {bx} 71 -1472 {bx} 72 -1472 gold_block')
        C(f'fill {bx} 71 -1471 {bx} 71 -1470 gold_block')
        C(f'setblock {bx} 72 -1471 bamboo_slab[type=bottom]')
        C(f'setblock {bx} 72 -1470 bamboo_stairs[facing=north]')
        C(f'setblock {bx} 73 -1472 lantern')
    # Espaldar alto dourado e vermelho atras do assento (z=-1472, y=71..75)
    C('fill 1419 71 -1472 1421 74 -1472 gold_block')
    C('fill 1419 72 -1472 1421 73 -1472 red_concrete')
    C('setblock 1420 73 -1472 gold_block')
    C('setblock 1420 75 -1472 gold_block')
    C('setblock 1419 75 -1472 bamboo_stairs[facing=east]')
    C('setblock 1421 75 -1472 bamboo_stairs[facing=west]')
    C('setblock 1418 74 -1472 bamboo_stairs[facing=west,half=top]')
    C('setblock 1422 74 -1472 bamboo_stairs[facing=east,half=top]')

    # Grande Biombo Imperial Esculpido atras do Trono (z=-1475..-1474, x=1413..1427, y=71..77)
    # Centro em z=-1475 (x=1416..1424) e abas anguladas em z=-1474 (x=1413..1415 e x=1425..1427)
    C('fill 1416 71 -1475 1424 76 -1475 red_concrete')
    C('fill 1416 71 -1475 1424 71 -1475 dark_oak_planks')
    C('fill 1416 77 -1475 1424 77 -1475 gold_block')
    for px in (1416, 1420, 1424):
        C(f'fill {px} 71 -1475 {px} 77 -1475 gold_block')
    # Relevo dourado imperial no biombo central
    for px in (1418, 1422):
        C(f'fill {px} 73 -1475 {px} 75 -1475 yellow_glazed_terracotta')
        C(f'setblock {px} 74 -1475 shroomlight')
        C(f'setblock {px} 74 -1474 bamboo_trapdoor[facing=south,open=true]')
    # Abas laterais do biombo
    for ax, bx in [(1413, 1415), (1425, 1427)]:
        C(f'fill {ax} 71 -1474 {bx} 75 -1474 red_terracotta')
        C(f'fill {ax} 76 -1474 {bx} 76 -1474 gold_block')
        C(f'fill {ax} 71 -1474 {ax} 76 -1474 dark_oak_wood')
        C(f'fill {bx} 71 -1474 {bx} 76 -1474 dark_oak_wood')
        C(f'setblock {(ax + bx) // 2} 73 -1474 gold_block')
        C(f'setblock {(ax + bx) // 2} 74 -1474 yellow_glazed_terracotta')

    # Incensarios / vasos imperiais dourados nas laterais da plataforma
    for ix in (1415, 1425):
        C(f'setblock {ix} 71 -1471 gold_block')
        C(f'setblock {ix} 72 -1471 decorated_pot')

    # Lanternas quentes nas colunas internas + Grade 3D de light[level=15] invisivel em TODO o Salao!
    # Isso garante block light = 15 uniforme no piso, tapete, personagens, trono e teto sem nunca escurecer!
    for px, dir_l in [(1404, 1), (1436, -1)]:
        for pz in (-1436, -1446, -1456, -1466):
            C(f'setblock {px + dir_l} 73 {pz} bamboo_trapdoor[facing={"east" if dir_l == 1 else "west"},half=top,open=false]')
            C(f'setblock {px + dir_l} 72 {pz} lantern[hanging=true]')
    for x in range(1398, 1444, 4):
        for z in range(-1476, -1430, 4):
            for ly in (70, 74, 78):
                C(f'fill {x} {ly} {z} {x} {ly} {z} light[level=15] replace air')
    # Luz extra dedicada sobre o Trono e Biombo
    for x in (1416, 1420, 1424):
        for z in (-1473, -1470, -1467):
            C(f'fill {x} 72 {z} {x} 76 {z} light[level=15] replace air')

    # ------------------------------------------------------------------
    # 4.6 TELHADO PAGODE IMPERIAL EM DUAS CAMADAS CURVADAS (y=80..95)
    # ------------------------------------------------------------------
    # Camada 1: beiral amplo projetado (x=1390..1450, z=-1484..-1424, y=80..84), preservando teto interno 1396..1444, -1478..-1430!
    _telhado_pagode_camada(1390, -1484, 1450, -1424, 80, 4, preservar_box=(1396, -1478, 1444, -1430))

    # Pavimento superior ornamental (clerestorio imperial: x=1400..1440, z=-1474..-1434, y=84..87)
    C('fill 1400 84 -1474 1440 87 -1434 red_concrete')
    C('fill 1400 84 -1474 1440 84 -1434 yellow_terracotta')
    C('fill 1400 87 -1474 1440 87 -1434 gold_block')
    for x in range(1402, 1439, 3):
        for z in (-1474, -1434):
            C(f'fill {x} 85 {z} {x} 86 {z} shroomlight')
    for z in range(-1472, -1435, 3):
        for x in (1400, 1440):
            C(f'fill {x} 85 {z} {x} 86 {z} shroomlight')
    # Placa imperial dourada na fachada sul do pavimento superior
    C('fill 1417 85 -1433 1423 87 -1433 gold_block')
    C('fill 1418 86 -1433 1422 86 -1433 red_concrete')
    C('setblock 1420 86 -1433 gold_block')

    # Camada 2: grande telhado superior imperial (x=1396..1444, z=-1478..-1430, y=87..93)
    rxa, rza, rxb, rzb, ry_top = _telhado_pagode_camada(1396, -1478, 1444, -1430, 87, 6)
    # Cumeeira imperial dourada com caudas de dragao (chiwei) nas extremidades
    z_mid = -1454
    C(f'fill {rxa - 1} {ry_top} {z_mid - 1} {rxb + 1} {ry_top} {z_mid + 1} dark_prismarine')
    C(f'fill {rxa - 1} {ry_top + 1} {z_mid} {rxb + 1} {ry_top + 1} {z_mid} gold_block')
    for extrem_x in (rxa - 1, rxb + 1):
        C(f'fill {extrem_x} {ry_top + 1} {z_mid} {extrem_x} {ry_top + 3} {z_mid} gold_block')
        C(f'setblock {extrem_x} {ry_top + 4} {z_mid} yellow_terracotta')
    C(f'setblock 1420 {ry_top + 2} {z_mid} gold_block')
    C(f'setblock 1420 {ry_top + 3} {z_mid} shroomlight')

    descarregar(1382, -1492, 1470, -1412)
    limpar_itens()
    marcar('palacio')
    print('Palacio Imperial concluido.', flush=True)


# ==============================================================================
# 5. CAMARA REAL DA CALDEIRA (SET['cozinha'] = (1456, 68, -1456))
# ==============================================================================
def cozinha():
    estudio()
    C(f'tp {PL} 1456 73 -1450 180 20')
    carregar(1442, -1468, 1470, -1444, 0.45)

    # Limpa espaco da ala anexa leste (x=1448..1466, z=-1466..-1446)
    C('fill 1448 65 -1466 1467 86 -1446 air')

    # Terraco nobre da ala leste (x=1448..1465, z=-1465..-1447, y=64..68)
    C('fill 1448 64 -1465 1465 67 -1447 stone_bricks')
    C('fill 1448 68 -1465 1465 68 -1447 polished_andesite')
    C('fill 1448 68 -1465 1465 68 -1465 yellow_terracotta')
    C('fill 1448 68 -1447 1465 68 -1447 yellow_terracotta')
    C('fill 1465 68 -1465 1465 68 -1447 yellow_terracotta')

    # Passagem nobre coberta ligando o Salao do Palacio (x=1445) a Cozinha Real (x=1449)
    # Abre portal largo em x=1445..1449, z=-1458..-1454, y=69..73
    C('fill 1445 68 -1459 1449 68 -1453 stripped_oak_wood')
    C('fill 1445 68 -1457 1454 68 -1455 red_wool')
    C('fill 1445 69 -1458 1449 73 -1454 air')
    for zz in (-1459, -1453):
        C(f'fill 1446 69 {zz} 1448 74 {zz} red_concrete')
        C(f'fill 1446 74 {zz} 1448 74 {zz} gold_block')
    C('fill 1446 74 -1458 1448 74 -1454 dark_oak_planks')
    C('setblock 1447 74 -1456 shroomlight')
    C('fill 1446 75 -1460 1448 75 -1452 dark_prismarine_slab[type=bottom]')

    # Piso interno da Camara Real da Caldeira (x=1450..1463, z=-1463..-1449, y=68)
    C('fill 1449 68 -1464 1464 68 -1448 dark_oak_planks')
    C('fill 1451 68 -1462 1462 68 -1450 stripped_spruce_wood')
    # Ladrilho termico de pedra polida e tijolos sob o braseiro central (1456, 68, -1456)
    C('fill 1453 68 -1459 1459 68 -1453 polished_andesite')
    C('fill 1454 68 -1458 1458 68 -1454 stone_bricks')
    C('fill 1455 68 -1457 1457 68 -1455 bricks')

    # Paredes nobres da Camara (x=1449..1464, z=-1464..-1448, y=69..75)
    for z_w, z_out in [(-1464, -1465), (-1448, -1447)]:
        C(f'fill 1449 69 {z_w} 1464 70 {z_w} dark_oak_planks')
        C(f'fill 1449 71 {z_w} 1464 74 {z_w} red_terracotta')
        C(f'fill 1449 75 {z_w} 1464 75 {z_w} gold_block')
        # Paineis dourados iluminados
        for x in (1452, 1453, 1456, 1459, 1460):
            C(f'fill {x} 71 {z_out} {x} 73 {z_out} shroomlight')
            C(f'fill {x} 71 {z_w} {x} 73 {z_w} oak_fence')
        for px in (1449, 1454, 1458, 1464):
            C(f'fill {px} 69 {z_w} {px} 75 {z_w} red_concrete')
            C(f'setblock {px} 69 {z_w} chiseled_quartz_block')

    for x_w, x_out in [(1449, 1448), (1464, 1465)]:
        C(f'fill {x_w} 69 -1464 {x_w} 70 -1448 dark_oak_planks')
        C(f'fill {x_w} 71 -1464 {x_w} 74 -1448 red_terracotta')
        C(f'fill {x_w} 75 -1464 {x_w} 75 -1448 gold_block')
        if x_w == 1464:
            for z in (-1461, -1460, -1456, -1452, -1451):
                C(f'fill {x_out} 71 {z} {x_out} 73 {z} shroomlight')
                C(f'fill {x_w} 71 {z} {x_w} 73 {z} oak_fence')
        for pz in (-1464, -1459, -1453, -1448):
            C(f'fill {x_w} 69 {pz} {x_w} 75 {pz} red_concrete')
            C(f'setblock {x_w} 69 {pz} chiseled_quartz_block')

    # Reabre a passagem oeste (x=1449, z=-1458..-1454, y=69..73)
    C('fill 1449 69 -1458 1449 73 -1454 air')
    C('fill 1449 74 -1458 1449 74 -1454 gold_block')

    # Teto iluminado em y=76 (interior amplo y=69..75!)
    C('fill 1449 76 -1464 1464 76 -1448 dark_oak_planks')
    for x in (1452, 1456, 1460):
        for z in (-1460, -1456, -1452):
            C(f'setblock {x} 76 {z} shroomlight')
    for lx, lz in [(1452, -1460), (1460, -1460), (1452, -1452), (1460, -1452)]:
        C(f'setblock {lx} 75 {lz} oak_fence')
        C(f'setblock {lx} 74 {lz} lantern[hanging=true]')

    # ------------------------------------------------------------------
    # FORNALHA / BRASEIRO CENTRAL EM (1456, 68, -1456) COM CALDEIRAO FERVENDO
    # ------------------------------------------------------------------
    # Fogueira real acesa em (1456, 69, -1456) visivel na frente/verso + caldeirao d'agua em y=70!
    # A fumaca real do campfire sobe direto atraves do water_cauldron!
    C('setblock 1456 69 -1456 campfire[lit=true]')
    C('setblock 1456 70 -1456 water_cauldron[level=3]')
    # Suportes laterais de tijolos e cobre encerado (x=1455 e x=1457)
    C('setblock 1455 69 -1456 bricks')
    C('setblock 1457 69 -1456 bricks')
    C('setblock 1455 70 -1456 waxed_cut_copper_stairs[facing=east,half=bottom]')
    C('setblock 1457 70 -1456 waxed_cut_copper_stairs[facing=west,half=bottom]')
    # Bancada auxiliar lateral de preparo das sementes (x=1454, z=-1456)
    C('setblock 1454 69 -1456 stripped_dark_oak_wood')
    C('setblock 1454 70 -1456 flower_pot')
    C('setblock 1458 69 -1456 stripped_dark_oak_wood')
    C('setblock 1458 70 -1456 decorated_pot')
    # Coifa imperial de cobre suspensa no alto (y=75, deixando y=71..74 totalmente livre pro vapor e enquadramento!)
    C('fill 1455 75 -1457 1457 75 -1455 waxed_cut_copper_slab[type=top]')
    C('setblock 1456 75 -1456 shroomlight')
    # Luz invisivel uniforme block light = 15 em toda a Camara Real da Caldeira
    for lx in (1451, 1454, 1456, 1458, 1461):
        for lz in (-1461, -1458, -1456, -1454, -1451):
            for ly in (70, 73):
                C(f'fill {lx} {ly} {lz} {lx} {ly} {lz} light[level=15] replace air')

    # Decoracao rica nas bancadas de fundo (norte z=-1463 e leste x=1463) para planos profundos
    C('fill 1451 69 -1463 1461 69 -1463 barrel[facing=south]')
    C('setblock 1453 69 -1463 smoker[facing=south,lit=true]')
    C('setblock 1459 69 -1463 smoker[facing=south,lit=true]')
    for dx, item_b in [(1451, 'decorated_pot'), (1452, 'lantern'), (1455, 'decorated_pot'),
                       (1457, 'flower_pot'), (1460, 'lantern'), (1461, 'decorated_pot')]:
        C(f'setblock {dx} 70 -1463 {item_b}')
    # Bancada leste (x=1463)
    C('fill 1463 69 -1460 1463 69 -1452 stripped_spruce_wood')
    C('setblock 1463 70 -1459 decorated_pot')
    C('setblock 1463 70 -1456 lantern')
    C('setblock 1463 70 -1453 decorated_pot')

    # Telhado pagode da Camara Real (y=76..81, preservando teto interno) + chamine fumegante no topo
    _telhado_pagode_camada(1447, -1466, 1466, -1446, 76, 5, preservar_box=(1450, -1463, 1463, -1449))
    C('fill 1455 80 -1457 1457 82 -1455 bricks')
    C('setblock 1456 82 -1456 campfire[lit=true]')
    for cx, cz in [(1455, -1456), (1457, -1456), (1456, -1457), (1456, -1455)]:
        C(f'setblock {cx} 83 {cz} brick_wall')
    C('fill 1455 84 -1457 1457 84 -1455 dark_prismarine_slab[type=bottom]')

    descarregar(1442, -1468, 1470, -1444)
    limpar_itens()
    marcar('cozinha')
    print('Camara Real da Caldeira concluida.', flush=True)


# ==============================================================================
# 6. CAMINHO IMPERIAL + JARDIM FLORIDO + LAGO KOI + CASA DO PING
# ==============================================================================
def jardim():
    estudio()
    C(f'tp {PL} 1420 76 -1345 0 20')
    carregar(1380, -1422, 1460, -1300, 0.6)

    # Limpa volume aereo do caminho e jardim
    for y in range(Y + 1, 100, 12):
        C(f'fill 1384 {y} -1413 1456 {min(y + 11, 99)} -1302 air')

    # ------------------------------------------------------------------
    # 6.1 CAMINHO IMPERIAL DE PEDRA COM LANTERNAS E CEREJEIRAS (z=-1414..-1362)
    # ------------------------------------------------------------------
    rnd = random.Random(108)
    for z in range(-1414, -1362):
        desvio = int(round(1.8 * math.sin((z + 1414) * 0.09)))
        cx = 1420 + desvio
        for dx in range(-3, 4):
            x = cx + dx
            if abs(dx) == 3:
                b = rnd.choice(['grass_block', 'moss_block', 'gravel'])
            elif abs(dx) == 2:
                b = rnd.choice(['andesite', 'cobblestone', 'mossy_stone_bricks'])
            else:
                b = rnd.choice(['stone_bricks', 'stone_bricks', 'polished_andesite', 'cracked_stone_bricks', 'mossy_stone_bricks'])
            C(f'setblock {x} {Y} {z} {b}')
        # Lanternas orientais de pedra ao longo do caminho
        if (z + 1412) % 10 == 0:
            for lx in (cx - 4, cx + 4):
                C(f'setblock {lx} {Y} {z} chiseled_stone_bricks')
                C(f'setblock {lx} {Y + 1} {z} cobblestone_wall')
                C(f'setblock {lx} {Y + 2} {z} shroomlight')
                C(f'setblock {lx} {Y + 3} {z} stone_brick_slab[type=bottom]')
                for fx, fz in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    C(f'setblock {lx + fx} {Y + 2} {z + fz} spruce_trapdoor[facing={"west" if fx == -1 else "east" if fx == 1 else "north" if fz == -1 else "south"},open=true]')

    # Cerejeiras ladeando a avenida imperial (afastadas em x para nao tapar a fachada do palacio!)
    for (tx, tz) in [(1405, -1404), (1435, -1402), (1403, -1386), (1437, -1384), (1406, -1370), (1434, -1370)]:
        C(f'fill {tx - 1} {Y - 1} {tz - 1} {tx + 1} {Y} {tz + 1} grass_block')
        C(f'place feature minecraft:cherry {tx} {Y + 1} {tz}')

    # ------------------------------------------------------------------
    # 6.2 TERRACO VERDE DO JARDIM (jardim_box: 1390, -1362, 1450, -1308, piso YJ=65)
    # ------------------------------------------------------------------
    C(f'fill 1388 {Y} -1364 1452 {Y} -1306 dirt')
    C(f'fill 1389 {YJ} -1363 1451 {YJ} -1307 grass_block')
    # Transicao suave de degraus de pedra/grama na entrada norte (z=-1364)
    C(f'fill 1416 {YJ} -1364 1424 {YJ} -1364 stone_brick_slab[type=bottom]')
    # Bioma cherry_grove/flower_forest para agua cristalina azul-turquesa e grama viva
    C(f'fillbiome 1388 58 -1364 1452 95 -1306 minecraft:flower_forest')

    # Portal Torii / Entrada Oriental do Jardim em (1420, YJ, -1362)
    for px in (1416, 1424):
        C(f'setblock {px} {YJ + 1} -1362 chiseled_stone_bricks')
        C(f'fill {px} {YJ + 2} -1362 {px} {YJ + 6} -1362 red_concrete')
    C(f'fill 1414 {YJ + 6} -1362 1426 {YJ + 6} -1362 dark_oak_planks')
    C(f'fill 1413 {YJ + 7} -1362 1427 {YJ + 7} -1362 dark_prismarine_slab[type=bottom]')
    C(f'setblock 1413 {YJ + 7} -1362 gold_block')
    C(f'setblock 1427 {YJ + 7} -1362 gold_block')
    C(f'fill 1415 {YJ + 5} -1362 1425 {YJ + 5} -1362 red_terracotta')
    C(f'setblock 1420 {YJ + 6} -1362 gold_block')
    C(f'setblock 1417 {YJ + 4} -1362 lantern[hanging=true]')
    C(f'setblock 1423 {YJ + 4} -1362 lantern[hanging=true]')

    # ------------------------------------------------------------------
    # 6.3 LAGO KOI CRISTALINO + VITORIAS-REGIAS + PONTE ARQUEADA (cx=1404, cz=-1346)
    # ------------------------------------------------------------------
    lcx, lcz, rx, rz = 1404, -1346, 8.5, 6.5
    for x in range(1393, 1416):
        for z in range(-1355, -1337):
            d = math.hypot((x - lcx) / rx, (z - lcz) / rz) + 0.14 * math.sin(math.atan2(z - lcz, x - lcx) * 3 + 0.5)
            if d <= 1.0:
                prof = 2 if d < 0.7 else 1
                C(f'fill {x} {YJ - prof} {z} {x} {YJ} {z} water')
                fundo_b = rnd.choice(['sand', 'sand', 'gravel', 'clay'])
                if d < 0.65 and rnd.random() < 0.14:
                    # Manchas laranja/brancas/amarelas no fundo simulando carpas Koi!
                    fundo_b = rnd.choice(['orange_terracotta', 'white_terracotta', 'yellow_terracotta'])
                C(f'setblock {x} {YJ - prof - 1} {z} {fundo_b}')
                if d < 0.6 and rnd.random() < 0.12:
                    C(f'setblock {x} {YJ - prof} {z} sea_pickle[pickles=3,waterlogged=true]')
            elif d <= 1.18:
                b_marg = rnd.choice(['moss_block', 'mossy_cobblestone', 'andesite', 'grass_block', 'podzol'])
                C(f'setblock {x} {YJ} {z} {b_marg}')

    # Vitorias-regias (lily_pad) sobre o lago (fora da faixa da ponte z=-1347..-1345)
    for (lx, lz) in [(1400, -1350), (1403, -1351), (1407, -1349), (1401, -1342), (1406, -1341), (1409, -1343), (1398, -1348)]:
        C(f'setblock {lx} {YJ + 1} {lz} lily_pad')

    # Ponte arqueada oriental de madeira sobre o Lago Koi (x=1397..1411, z=-1347..-1345)
    arco = [
        (1397, YJ + 1, 'bottom'),
        (1398, YJ + 1, 'top'),
        (1399, YJ + 2, 'bottom'),
        (1400, YJ + 2, 'bottom'),
        (1401, YJ + 2, 'top'),
        (1402, YJ + 3, 'bottom'),
        (1403, YJ + 3, 'bottom'),
        (1404, YJ + 3, 'bottom'),
        (1405, YJ + 3, 'bottom'),
        (1406, YJ + 3, 'bottom'),
        (1407, YJ + 2, 'top'),
        (1408, YJ + 2, 'bottom'),
        (1409, YJ + 2, 'bottom'),
        (1410, YJ + 1, 'top'),
        (1411, YJ + 1, 'bottom'),
    ]
    for px, py, tipo in arco:
        C(f'fill {px} {py} -1347 {px} {py} -1345 spruce_slab[type={tipo}]')
        py_rail = py + 1
        for rz_b in (-1348, -1344):
            if px in (1397, 1401, 1404, 1407, 1411):
                C(f'fill {px} {YJ} {rz_b} {px} {py_rail} {rz_b} stripped_spruce_log')
                if px in (1397, 1404, 1411):
                    C(f'setblock {px} {py_rail + 1} {rz_b} lantern')
            else:
                C(f'setblock {px} {py_rail} {rz_b} oak_fence')

    # Trilha de pedras pelo jardim ligando entrada (-1362), ponte, canteiro_sol e varanda da casa (-1333)
    for z in range(-1362, -1333):
        px = 1420 + int(round(1.2 * math.sin((z + 1362) * 0.18)))
        for dx in (-1, 0, 1):
            if rnd.random() < 0.85:
                C(f'setblock {px + dx} {YJ} {z} {rnd.choice(["stone_bricks", "polished_andesite", "mossy_stone_bricks", "gravel"])}')
    # Ramal para a ponte (z=-1346, x=1412..1419)
    for x in range(1412, 1420):
        C(f'fill {x} {YJ} -1347 {x} {YJ} -1345 {rnd.choice(["stone_bricks", "polished_andesite", "mossy_stone_bricks"])}')

    # ------------------------------------------------------------------
    # 6.4 CASA / PAVILHAO DO PING (casa_centro: 1420, 65, -1322) + VARANDA + JANELA REAL
    # ------------------------------------------------------------------
    # Varanda ensolarada frontal aberta ao ceu (x=1411..1429, z=-1334..-1329, piso YJ=65)
    C(f'fill 1411 {YJ} -1334 1429 {YJ} -1329 spruce_planks')
    C(f'fill 1411 {YJ} -1334 1429 {YJ} -1334 stripped_spruce_wood')
    C(f'fill 1411 {YJ} -1334 1411 {YJ} -1329 stripped_spruce_wood')
    C(f'fill 1429 {YJ} -1334 1429 {YJ} -1329 stripped_spruce_wood')
    # Degrau suave na frente da varanda (z=-1335)
    C(f'fill 1418 {YJ} -1335 1422 {YJ} -1335 stone_brick_slab[type=top]')

    # BANCADA ENSOLARADA EM SET['varanda_mesa'] = (1414, 65, -1332):
    # Sem telhado em cima (z=-1332 tem sol direto!) e mesa na altura y=66 para apoiar o vaso/regar
    C(f'setblock 1413 {YJ + 1} -1332 spruce_stairs[facing=west,half=top]')
    C(f'setblock 1414 {YJ + 1} -1332 spruce_slab[type=top]')
    C(f'setblock 1415 {YJ + 1} -1332 spruce_stairs[facing=east,half=top]')
    # Banquinho baixo de madeira atras da bancada (y=66.5) para Ping alcancar o tampo sem encostar na mesa
    C(f'fill 1414 {YJ + 1} -1330 1415 {YJ + 1} -1330 spruce_slab[type=bottom]')
    # Apoios de jardinagem ao lado na ponta oeste da varanda (sem bloquear visao)
    C(f'setblock 1411 {YJ + 1} -1332 rooted_dirt')
    C(f'setblock 1411 {YJ + 1} -1331 spruce_trapdoor[facing=south,open=true]')
    C(f'setblock 1412 {YJ + 1} -1332 spruce_trapdoor[facing=east,open=true]')
    C(f'setblock 1411 {YJ + 1} -1330 water_cauldron[level=3]')
    C(f'setblock 1428 {YJ + 1} -1333 flower_pot')
    C(f'setblock 1428 {YJ + 1} -1330 lantern')

    # Estrutura da Casa/Pavilhao do Ping: x=1412..1428, z=-1328..-1315, piso y=65 (YJ), teto interno em y=71
    C(f'fill 1412 {YJ} -1328 1428 {YJ} -1315 spruce_planks')
    for x in range(1413, 1428):
        for z in range(-1327, -1315):
            if (x + z) % 4 == 0:
                C(f'setblock {x} {YJ} {z} stripped_spruce_wood')

    # Pilares estruturais de stripped_spruce_log (y=66..70)
    for px in (1412, 1417, 1423, 1428):
        for pz in (-1328, -1322, -1315):
            if pz == -1322 and px in (1417, 1423):
                continue  # interior livre!
            C(f'fill {px} {YJ + 1} {pz} {px} {YJ + 5} {pz} stripped_spruce_log')

    # Paredes base (y=66) e verga superior (y=70)
    for pz in (-1328, -1315):
        C(f'fill 1412 {YJ + 1} {pz} 1428 {YJ + 1} {pz} spruce_planks')
        C(f'fill 1412 {YJ + 5} {pz} 1428 {YJ + 5} {pz} stripped_spruce_wood')
    for px in (1412, 1428):
        C(f'fill {px} {YJ + 1} -1328 {px} {YJ + 1} -1315 spruce_planks')
        C(f'fill {px} {YJ + 5} -1328 {px} {YJ + 5} -1315 stripped_spruce_wood')

    # Paredes laterais e parede sul (y=67..69): paineis claros aconchegantes (birch_planks + janelas trelicadas)
    for px in (1412, 1428):
        C(f'fill {px} {YJ + 2} -1327 {px} {YJ + 4} -1316 birch_planks')
        for zz in (-1325, -1324, -1319, -1318):
            C(f'fill {px} {YJ + 2} {zz} {px} {YJ + 3} {zz} oak_fence')
    # Parede sul de fundo (z=-1315, vista atras do Ping quando filmado pela janela frontal!)
    C(f'fill 1413 {YJ + 2} -1315 1427 {YJ + 4} -1315 birch_planks')
    for xx in (1415, 1416, 1424, 1425):
        C(f'fill {xx} {YJ + 2} -1315 {xx} {YJ + 3} -1315 oak_fence')
        C(f'fill {xx} {YJ + 2} -1314 {xx} {YJ + 3} -1314 shroomlight')

    # Parede frontal Norte (z=-1328):
    C(f'fill 1413 {YJ + 2} -1328 1427 {YJ + 4} -1328 spruce_planks')
    # Porta de entrada de abeto entreaberta na ala oeste (x=1415, z=-1328, y=66..67) + painel na ala oeste
    C(f'fill 1413 {YJ + 2} -1328 1414 {YJ + 3} -1328 bamboo_trapdoor[facing=north,open=false]')
    C(f'fill 1415 {YJ + 1} -1328 1415 {YJ + 2} -1328 air')
    C(f'setblock 1415 {YJ + 1} -1328 spruce_door[facing=south,half=lower,hinge=left,open=true]')
    C(f'setblock 1415 {YJ + 2} -1328 spruce_door[facing=south,half=upper,hinge=left,open=true]')
    C(f'setblock 1415 {YJ + 3} -1328 stripped_spruce_wood')
    # Painel oriental na ala leste da fachada (x=1425..1426)
    C(f'fill 1425 {YJ + 2} -1328 1426 {YJ + 3} -1328 bamboo_trapdoor[facing=north,open=false]')

    # *** JANELA FRONTAL REAL EM SET['janela'] = (1420, 66, -1328) ***
    # Peitoril solido de madeira nobre em y=66 (x=1418..1422, z=-1328) -> o vaso pousa sobre (1420, 66, -1328)!
    C('fill 1418 66 -1328 1422 66 -1328 stripped_oak_wood')
    # Banquinho interno de madeira (z=-1326, topo y=66.5) para Ping vigiar o vaso pela janela sem colidir no peitoril
    C('fill 1419 66 -1326 1421 66 -1326 spruce_slab[type=bottom]')
    # Vao central 100% ABERTO (sem nenhum bloco tampando!) em x=1419..1421, y=67..69, z=-1328
    C('fill 1419 67 -1328 1421 69 -1328 air')
    # Trelicas/venezianas orientais abertas nas laterais do vao (x=1418 e x=1422, y=67..69)
    for wx in (1418, 1422):
        C(f'fill {wx} 67 -1328 {wx} 69 -1328 oak_fence')
    # Moldura externa charmosa nas laterais da janela (z=-1329, x=1418 e x=1422) sem obstruir o centro!
    for wx, face in [(1418, 'west'), (1422, 'east')]:
        C(f'fill {wx} 67 -1329 {wx} 69 -1329 oak_trapdoor[facing={face},open=true]')
    # Lanternas aquecendo a fachada nas colunas x=1417 e x=1423 (y=69, z=-1329)
    C('setblock 1417 69 -1329 lantern')
    C('setblock 1423 69 -1329 lantern')

    # Interior iluminado (luz 15) e decorado atras do Ping (Ping fica em z=-1326, camera ve z=-1325..-1316!)
    C(f'fill 1412 {YJ + 6} -1328 1428 {YJ + 6} -1315 spruce_planks')
    for lx in (1415, 1420, 1425):
        for lz in (-1325, -1321, -1318):
            C(f'setblock {lx} {YJ + 6} {lz} shroomlight')
    for lx, lz in [(1418, -1323), (1422, -1323), (1420, -1319)]:
        C(f'setblock {lx} {YJ + 5} {lz} oak_fence')
        C(f'setblock {lx} {YJ + 4} {lz} lantern[hanging=true]')

    # Tapete aconchegante no centro da casa (sem atrapalhar z=-1326)
    C(f'fill 1418 {YJ} -1324 1422 {YJ} -1319 yellow_wool')
    C(f'fill 1419 {YJ} -1323 1421 {YJ} -1320 orange_wool')
    # Estante botanica e decoracao de fundo na parede sul (z=-1316, exatamente no fundo do quadro da janela!)
    C(f'fill 1418 {YJ + 1} -1316 1422 {YJ + 2} -1316 bookshelf')
    C(f'setblock 1420 {YJ + 2} -1316 chiseled_bookshelf[facing=north]')
    C(f'setblock 1417 {YJ + 1} -1316 barrel[facing=up]')
    C(f'setblock 1417 {YJ + 2} -1316 decorated_pot')
    C(f'setblock 1423 {YJ + 1} -1316 barrel[facing=up]')
    C(f'setblock 1423 {YJ + 2} -1316 lantern')
    C(f'setblock 1419 {YJ + 3} -1316 flower_pot')
    C(f'setblock 1421 {YJ + 3} -1316 decorated_pot')
    # Cantinho de dormir / bancada interna nas laterais (x=1426..1427 e x=1413)
    C(f'setblock 1426 {YJ + 1} -1318 crafting_table')
    C(f'setblock 1426 {YJ + 2} -1318 flower_pot')
    C(f'setblock 1413 {YJ + 1} -1320 barrel[facing=east]')
    C(f'setblock 1413 {YJ + 2} -1320 lantern')
    # Grade de light[level=15] invisivel no interior da Casa do Ping e na Varanda/Janela para luz 15 perfeita!
    for lx in range(1413, 1428, 3):
        for lz in range(-1333, -1315, 3):
            for ly in (YJ + 2, YJ + 4):
                C(f'fill {lx} {ly} {lz} {lx} {ly} {lz} light[level=15] replace air')

    # Telhado Oriental Charmoso da Casa do Ping (y=71..76, preservando teto de madeira e shroomlight interno!)
    _telhado_pagode_camada(1410, -1330, 1430, -1313, 71, 5, preservar_box=(1413, -1327, 1427, -1316))
    # Cumeeira de madeira/ouro da casa do Ping
    C('fill 1415 76 -1322 1425 76 -1321 stripped_spruce_wood')
    C('setblock 1415 77 -1322 bamboo_slab[type=bottom]')
    C('setblock 1425 77 -1322 bamboo_slab[type=bottom]')

    # ------------------------------------------------------------------
    # 6.5 CANTEIRO ABERTO AO SOL (SET['canteiro_sol'] = (1426, 65, -1340)) + FLORES + BAMBUS + CEREJEIRAS
    # ------------------------------------------------------------------
    # Canteiro principal em redor de (1426, 65, -1340), mantendo (1426, 65, -1340) e arredores limpos pro Ping!
    C(f'fill 1424 {YJ} -1342 1428 {YJ} -1338 moss_block')
    C(f'fill 1425 {YJ} -1341 1427 {YJ} -1339 grass_block')
    # Dois canteiros baixos floridos emoldurando (sem bloquear camera) em x=1430..1433 e z=-1345..-1343
    for (cx0, cz0, cx1, cz1) in [(1430, -1343, 1433, -1338), (1424, -1346, 1429, -1344)]:
        C(f'fill {cx0} {YJ} {cz0} {cx1} {YJ} {cz1} rooted_dirt')
        for x in range(cx0, cx1 + 1):
            for z in range(cz0, cz1 + 1):
                flr = rnd.choice(['pink_tulip', 'red_tulip', 'orange_tulip', 'white_tulip', 'allium', 'cornflower', 'oxeye_daisy'])
                C(f'setblock {x} {YJ + 1} {z} {flr}')

    # Cerejeiras rosas (cherry) emoldurando o Jardim (nas bordas para vista limpa e cinematografica!)
    cerejeiras_jardim = [
        (1440, -1354), (1443, -1338), (1439, -1322), (1434, -1310),
        (1394, -1356), (1391, -1336), (1396, -1318), (1408, -1310), (1420, -1308),
    ]
    for (tx, tz) in cerejeiras_jardim:
        C(f'fill {tx - 1} {YJ - 1} {tz - 1} {tx + 1} {YJ} {tz + 1} grass_block')
        C(f'setblock {tx} {YJ + 1} {tz} air')
        C(f'place feature minecraft:cherry {tx} {YJ + 1} {tz}')

    # Bambuzal oriental nas bordas oeste (perto do lago) e leste
    bambus = [
        (1392, -1349), (1393, -1347), (1392, -1345), (1394, -1343), (1393, -1341),
        (1445, -1348), (1446, -1346), (1444, -1345), (1446, -1330), (1445, -1328),
        (1405, -1322), (1406, -1320), (1434, -1326), (1435, -1324),
    ]
    for (bx, bz) in bambus:
        alt_b = rnd.randint(5, 9)
        C(f'setblock {bx} {YJ} {bz} podzol')
        for by in range(YJ + 1, YJ + 1 + alt_b):
            folha_b = 'large' if by >= YJ + alt_b - 2 else ('small' if by >= YJ + alt_b - 4 else 'none')
            C(f'setblock {bx} {by} {bz} bamboo[age=1,leaves={folha_b},stage=0]')

    # Tapete rico de petalas rosas (pink_petals) e flores coloridas pelo jardim (preservando piso limpo em canteiro_sol e varanda!)
    flores_jardim = [
        'pink_petals[flower_amount=4]', 'pink_petals[flower_amount=3]', 'pink_tulip', 'white_tulip',
        'allium', 'azure_bluet', 'oxeye_daisy', 'poppy', 'dandelion', 'blue_orchid', 'short_grass',
    ]
    for _ in range(220):
        fx = rnd.randint(1390, 1450)
        fz = rnd.randint(-1361, -1309)
        # Nao coloca em cima da casa, varanda ou centro exato do canteiro_sol
        if 1410 <= fx <= 1430 and -1335 <= fz <= -1313:
            continue
        if 1424 <= fx <= 1428 and -1342 <= fz <= -1338:
            continue
        if 1393 <= fx <= 1416 and -1355 <= fz <= -1337:
            continue
        flr = rnd.choice(flores_jardim)
        C(f'fill {fx} {YJ + 1} {fz} {fx} {YJ + 1} {fz} {flr} replace air')

    # Limpa qualquer folha de arvore que tenha invadido muito baixo sobre a janela ou canteiro_sol
    C(f'fill 1416 {YJ + 1} -1335 1424 {YJ + 5} -1328 air replace cherry_leaves')
    C(f'fill 1422 {YJ + 1} -1344 1430 {YJ + 6} -1336 air replace cherry_leaves')

    descarregar(1380, -1422, 1460, -1300)
    limpar_itens()
    marcar('jardim')
    print('Jardim Florido, Lago Koi e Casa do Ping concluidos.', flush=True)


# ==============================================================================
# 7. PAISAGISMO GERAL DA ILHA (BOSQUES, CEREJEIRAS, FLORES E GRAMA)
# ==============================================================================
def paisagismo():
    estudio()
    if 'paisagismo' in FEITO:
        return
    rnd = random.Random(91)
    x0, z0, x1, z1 = SET['canvas']

    # Grama baixa, flores e manchas naturais de musgo/podzol pelos campos da ilha
    feats_campo = ['minecraft:patch_grass', 'minecraft:patch_grass', 'minecraft:flower_default', 'minecraft:flower_plain']
    for a, b, c, d in tile_iter(x0, z0, x1, z1, 64):
        carregar(a, b, c, d, 0.25)
        for _ in range(48):
            tx, tz = rnd.randint(a, c), rnd.randint(b, d)
            if mascara_ilha(tx, tz) < 0.25 or h_anel_serra(tx, tz) > 3:
                continue
            ty = altura_ilha(tx, tz)
            C(f'place feature {rnd.choice(feats_campo)} {tx} {ty + 1} {tz}')
        for _ in range(6):
            tx, tz = rnd.randint(a, c), rnd.randint(b, d)
            if mascara_ilha(tx, tz) < 0.8 or h_anel_serra(tx, tz) > 3:
                continue
            ty = altura_ilha(tx, tz)
            b_chao = rnd.choice(['moss_block', 'coarse_dirt', 'podzol'])
            C(f'fill {tx - 1} {ty} {tz - 1} {tx + 1} {ty} {tz + 1} {b_chao} replace grass_block')
        descarregar(a, b, c, d)

    # Bosques harmoniosos de cerejeiras, carvalhos, betulas e pinheiros nas colinas da ilha
    # (Preservando o corredor visual central x=1402..1438 entre Palacio e Jardim!)
    arvores = 0
    for _ in range(130):
        tx = rnd.randint(x0 + 12, x1 - 12)
        tz = rnd.randint(z0 + 12, z1 - 12)
        if mascara_ilha(tx, tz) < 0.65:
            continue
        if 1400 <= tx <= 1440 and -1425 <= tz <= -1360:
            continue
        if h_anel_serra(tx, tz) > 6:
            continue
        ty = altura_ilha(tx, tz)
        carregar(tx - 6, tz - 6, tx + 6, tz + 6, 0.08)
        C(f'fill {tx - 1} {ty - 1} {tz - 1} {tx + 1} {ty} {tz + 1} grass_block')
        C(f'setblock {tx} {ty + 1} {tz} air')
        esp = rnd.choice(['cherry', 'oak', 'birch', 'oak', 'cherry', 'spruce'])
        C(f'place feature minecraft:{esp} {tx} {ty + 1} {tz}')
        descarregar(tx - 6, tz - 6, tx + 6, tz + 6)
        arvores += 1

    limpar_itens()
    marcar('paisagismo')
    print('Paisagismo da ilha concluido. Arvores plantadas:', arvores, flush=True)


# ==============================================================================
# 8. SCREENSHOTS DE VERIFICACAO (mc.shot)
# ==============================================================================
def _angulo(cpos, alvo):
    dx, dy, dz = alvo[0] - cpos[0], alvo[1] - cpos[1], alvo[2] - cpos[2]
    yaw = math.degrees(math.atan2(-dx, dz))
    pitch = -math.degrees(math.atan2(dy, math.hypot(dx, dz)))
    return round(yaw, 2), round(pitch, 2)


def fotos():
    estudio()
    try:
        mc.call('screen.close')
    except Exception:
        pass
    C(f'gamemode spectator {PL}')
    C('time set 3500')
    C('weather clear')
    limpar_itens()

    vistas = [
        # 1. Fachada completa do Palacio + avenida de cerejeiras + serra norte ao fundo
        ('vista_palacio_ext.png', (1420.5, 79.5, -1374.0), (1420.5, 78.5, -1456.0), (1350, -1590, 1490, -1370)),
        # 2. Interior amplo e iluminado do Salao olhando para o Trono Imperial Dourado
        ('vista_salao_trono.png', (1420.5, 72.3, -1439.0), (1420.5, 72.8, -1472.0), (1390, -1485, 1450, -1425)),
        # 3. Jardim florido + lago koi + ponte + cerejeiras + casa do Ping + serra sul verde ao fundo
        ('vista_jardim_casa.png', (1407.5, 73.5, -1358.5), (1419.5, 68.5, -1322.0), (1365, -1365, 1475, -1185)),
        # 4. Enquadramento da janela frontal real da casa do Ping (z=-1333 olhando para +z)
        ('vista_janela.png', (1420.5, 67.85, -1333.3), (1420.5, 67.35, -1324.0), (1405, -1340, 1435, -1310)),
        # 5. Camara Real da Caldeira (fornalha + campfire fumegando + water_cauldron)
        ('vista_cozinha.png', (1451.8, 71.2, -1451.8), (1456.5, 69.8, -1456.5), (1445, -1466, 1466, -1446)),
    ]

    for nome, cpos, alvo, fl_box in vistas:
        yaw, pitch = _angulo(cpos, alvo)
        carregar(*fl_box, espera=0.6)
        C(f'tp {PL} {cpos[0]} {cpos[1]} {cpos[2]} {yaw} {pitch}')
        try:
            mc.call('screen.close')
        except Exception:
            pass
        time.sleep(3.8)
        out_path = os.path.join(TMP_DIR, nome)
        mc.shot(out_path)
        descarregar(*fl_box)
        print('Screenshot salva:', out_path, flush=True)


def tudo():
    estudio()
    base()
    serra()
    verdejar_serras()
    naturalizar()
    palacio()
    cozinha()
    jardim()
    paisagismo()
    fotos()


if __name__ == '__main__':
    etapas = sys.argv[1:] or ['tudo']
    for e in etapas:
        print(f'=== Executando etapa: {e} ===', flush=True)
        globals()[e]()
