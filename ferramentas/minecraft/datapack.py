"""Gera o datapack de uma cena (câmera + ações no tempo certo) a partir de um JSON.

Uso:   python -X utf8 datapack.py cena_c004.json  <pasta do mundo>   [--pack-format N]
Teste: python -X utf8 datapack.py --teste

O Claude transforma a ficha do cenas.md + tempos.json neste JSON:
{
  "cena": "c004",
  "duracao": 12.5,                       # segundos
  "setup": ["time set 12500", "weather clear", "place structure minecraft:village_plains 0 64 0"],
  "camera": {                            # opcional
    "pontos": [ {"t": 0,   "pos": [0, 90, -20], "yaw": 0,  "pitch": 20},
                {"t": 12.5,"pos": [0, 75, -5],  "yaw": 10, "pitch": 10} ],
    "suave": true,                       # ease in/out em cada trecho
    "ajuste_y": -1.62                    # altura do olho do jogador montado no rig (calibrar no 1º teste)
  },
  "acoes": [ {"t": 1.2, "cmd": "particle minecraft:happy_villager 8 64 5 0.3 0.5 0.3 0 10"} ],
  "fim": ["say fim"]                     # opcional
}
Saída: <mundo>/datapacks/cenas/data/cenas/function/<cena>/{start,loop,passo,fim}.mcfunction
No jogo: /reload  →  /function cenas:<cena>/start

Como funciona: um placar conta os ticks (20 por segundo). A cada tick o `passo` roda só as linhas
daquele tick. A câmera é um text_display invisível com teleport_duration (o cliente suaviza o
movimento); o jogador fica montado nele, invisível, e a cabeça gira com /rotate a cada tick.
ponytail: 1 linha por tick no `passo` (cena de 30 s = 600 linhas); se ficar pesado, trocar por macros.
⚠️ Não testado dentro do Minecraft ainda (pack_format, /ride no text_display, ajuste_y).
"""
import json, math, sys
from pathlib import Path

TPS = 20


def suave(u):  # ease in/out
    return u * u * (3 - 2 * u)


def interp_yaw(a, b, u):  # pelo caminho mais curto (350 → 10 passa por 0)
    d = (b - a + 180) % 360 - 180
    return a + d * u


def ponto_camera(pontos, t, liso=True):
    if t <= pontos[0]['t']:
        p = pontos[0]; return p['pos'], p['yaw'], p['pitch']
    for a, b in zip(pontos, pontos[1:]):
        if a['t'] <= t <= b['t']:
            u = (t - a['t']) / ((b['t'] - a['t']) or 1)
            u = suave(u) if liso else u
            pos = [a['pos'][i] + (b['pos'][i] - a['pos'][i]) * u for i in range(3)]
            return pos, interp_yaw(a['yaw'], b['yaw'], u), a['pitch'] + (b['pitch'] - a['pitch']) * u
    p = pontos[-1]; return p['pos'], p['yaw'], p['pitch']


def gerar(cena):
    n = cena['cena']; total = round(cena['duracao'] * TPS)
    start = ['scoreboard objectives add cena dummy', f'scoreboard players set #t cena 0']
    start += cena.get('setup', [])
    cam = cena.get('camera')
    if cam:
        (x, y, z), yaw, pitch = ponto_camera(cam['pontos'], 0, cam.get('suave', True))
        ay = cam.get('ajuste_y', -1.62)
        start += [
            'kill @e[tag=cam_rig]',
            f'summon text_display {x:.3f} {y + ay:.3f} {z:.3f} {{Tags:["cam_rig"],teleport_duration:2,text:"" }}',
            'gamemode adventure @p',
            'effect give @p invisibility infinite 0 true',
            'ride @p mount @e[tag=cam_rig,limit=1]',
        ]
    start.append(f'schedule function cenas:{n}/loop 1t replace')

    linhas = {}
    if cam:
        for k in range(total + 1):
            (x, y, z), yaw, pitch = ponto_camera(cam['pontos'], k / TPS, cam.get('suave', True))
            linhas.setdefault(k, []).append(f'tp @e[tag=cam_rig,limit=1] {x:.3f} {y + ay:.3f} {z:.3f}')
            linhas[k].append(f'rotate @p {yaw:.2f} {pitch:.2f}')
    for a in cena.get('acoes', []):
        linhas.setdefault(round(a['t'] * TPS), []).append(a['cmd'].lstrip('/'))
    passo = [f'execute if score #t cena matches {k} run {c}' for k in sorted(linhas) for c in linhas[k]]

    loop = [f'function cenas:{n}/passo', 'scoreboard players add #t cena 1',
            f'execute if score #t cena matches ..{total} run schedule function cenas:{n}/loop 1t replace',
            f'execute if score #t cena matches {total + 1}.. run function cenas:{n}/fim']
    fim = ['ride @p dismount', 'kill @e[tag=cam_rig]', 'effect clear @p invisibility'] if cam else []
    fim += [c.lstrip('/') for c in cena.get('fim', [])]
    start = [c.lstrip('/') for c in start]
    return {'start': start, 'loop': loop, 'passo': passo, 'fim': fim}


def salvar(cena, mundo, pack_format=94):
    raiz = Path(mundo) / 'datapacks' / 'cenas'
    (raiz).mkdir(parents=True, exist_ok=True)
    (raiz / 'pack.mcmeta').write_text(json.dumps({'pack': {
        'description': 'Cenas do canal (gerado por datapack.py)',
        'pack_format': pack_format, 'min_format': 48, 'max_format': 999,
        'supported_formats': {'min_inclusive': 48, 'max_inclusive': 999}}}, indent=1), encoding='utf8')
    pasta = raiz / 'data' / 'cenas' / 'function' / cena['cena']
    pasta.mkdir(parents=True, exist_ok=True)
    for nome, ls in gerar(cena).items():
        (pasta / f'{nome}.mcfunction').write_text('\n'.join(ls) + '\n', encoding='utf8')
    return pasta


def teste():
    cena = {'cena': 'c900', 'duracao': 2, 'setup': ['/time set 12500'],
            'camera': {'pontos': [{'t': 0, 'pos': [0, 80, 0], 'yaw': 350, 'pitch': 20},
                                  {'t': 2, 'pos': [10, 80, 0], 'yaw': 10, 'pitch': 0}], 'suave': False},
            'acoes': [{'t': 1, 'cmd': '/say oi'}]}
    pos, yaw, pitch = ponto_camera(cena['camera']['pontos'], 1, liso=False)
    assert pos == [5, 80, 0] and abs(yaw % 360) < 1e-9 and pitch == 10, (pos, yaw, pitch)  # 350→10 passa por 0
    assert suave(0) == 0 and suave(1) == 1 and suave(0.5) == 0.5
    f = gerar(cena)
    assert f['start'][0].startswith('scoreboard') and 'time set 12500' in f['start']
    assert 'execute if score #t cena matches 20 run say oi' in f['passo']
    assert sum(1 for l in f['passo'] if ' run tp ' in l) == 41          # 2 s × 20 + o tick 0
    assert f['loop'][-1].endswith('run function cenas:c900/fim')
    assert all(not l.startswith('/') for ls in f.values() for l in ls)
    print('teste OK')


if __name__ == '__main__':
    if sys.argv[1:] == ['--teste']:
        teste(); sys.exit()
    pf = int(sys.argv[sys.argv.index('--pack-format') + 1]) if '--pack-format' in sys.argv else 94
    cena = json.loads(Path(sys.argv[1]).read_text(encoding='utf8'))
    print('salvo em', salvar(cena, sys.argv[2], pf), '→ no jogo: /reload e /function cenas:%s/start' % cena['cena'])
