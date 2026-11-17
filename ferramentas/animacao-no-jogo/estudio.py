import os as _os
PROJ = _os.environ.get('ANIM_PROJETO', _os.getcwd())
"""Preparo/restauro do cliente para gravar (26.3) e gravacao de um plano."""
import os, time, json
import mc, fl, rec
from motor import C, PL

B = _os.path.join(PROJ, 'brutos')


def preparar(hud=True):
    for c in ['gamerule send_command_feedback false', 'gamerule advance_time false', 'gamerule advance_weather false',
              'gamerule random_tick_speed 0', 'gamerule spawn_mobs false', 'time set noon', 'weather clear',
              f'effect give {PL} invisibility infinite 0 true', 'team add semnome',
              'team modify semnome nametagVisibility never', 'team modify semnome seeFriendlyInvisibles false', f'team join semnome {PL}',
              'kill @e[type=item]']:
        C(c)
    mc.call('inventory.selectHotbar', {'slot': 8})
    if hud:
        fl.f1()


SESSAO = {'rec': None, 'takes': {}}


def sessao_inicio(nome='sessao', maxs=1800):
    """uma captura longa para todos os takes (iniciar o WGC a cada take ficou lento/instavel)"""
    SESSAO['rec'] = rec.Rec(os.path.join(B, nome), maxs); SESSAO['nome'] = nome; SESSAO['takes'] = {}


def sessao_fim():
    R = SESSAO['rec']; print(R.stop().strip())
    base = os.path.join(B, SESSAO['nome'])
    json.dump(SESSAO['takes'], open(base + '_takes.json', 'w'))
    SESSAO['rec'] = None


def cortar(nome='sessao'):
    """gera <take>.mkv/.wav/.json/_events.json a partir da sessao (pts de epoca preservados)"""
    import subprocess
    base = os.path.join(B, nome)
    takes = json.load(open(base + '_takes.json'))
    js = json.load(open(base + '.json'))
    p = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-read_intervals', '%+#1', '-show_entries',
                        'packet=pts_time', '-of', 'csv=p=0', base + '.mkv'], capture_output=True, text=True).stdout.split()
    v0 = float(p[0])
    for tk, evs in takes.items():
        t0 = evs[0][1] - 1.0; t1 = evs[-1][1] + 0.5
        out = os.path.join(B, tk)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t0 - v0:.3f}', '-to', f'{t1 - v0:.3f}', '-i', base + '.mkv',
                        '-copyts', '-c', 'copy', out + '.mkv'])
        a0 = js['audio_start_epoch']
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{max(0, t0 - a0):.3f}', '-to', f'{t1 - a0:.3f}', '-i', base + '.wav',
                        out + '.wav'])
        json.dump({'audio_start_epoch': max(a0, t0)}, open(out + '.json', 'w'))
        json.dump(evs, open(out + '_events.json', 'w'))
        print('cortado', tk)


def gravar(nome, fn, total, maxs=120):
    if SESSAO['rec'] is not None:
        evs = []
        ev = lambda n: evs.append((n, time.time()))
        t0 = time.time(); ev('inicio')
        fn(ev)
        rest = total - (time.time() - t0)
        if rest > 0:
            time.sleep(rest)
        ev('fim'); SESSAO['takes'][nome] = evs
        json.dump(SESSAO['takes'], open(os.path.join(B, SESSAO['nome']) + '_takes.json', 'w'))
        print(nome, 'GRAVADO (sessao)', flush=True)
        return
    out = os.path.join(B, nome)
    os.makedirs(B, exist_ok=True)
    R = rec.Rec(out, maxs)
    t0 = time.time(); R.ev('inicio')
    fn(R.ev)
    rest = total - (time.time() - t0)
    if rest > 0:
        time.sleep(rest)
    R.ev('fim')
    print(nome, R.stop().strip())
    return out


def folha(nome, fps=4, cols=8, larg=200):
    """folha de contato de um take: retorna caminho png"""
    import subprocess
    src = os.path.join(B, nome + '.mkv'); dst = os.path.join(B, nome + '_folha.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf',
                    f'setpts=PTS-STARTPTS,fps={fps},scale={larg}:-1,tile={cols}x4', '-frames:v', '1', dst])
    return dst
