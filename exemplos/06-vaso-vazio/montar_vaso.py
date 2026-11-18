"""Montagem final do short 'O Vaso Vazio' (Capivara Ping & O Rei).
Le planos.json, narracao.wav, pal_aj.json, musica.mp3 e *_takes.json, aplica grade cinematografica
quente, legenda Monocraft de 1 palavra com micro-pop, whoosh suave nos cortes e master -12 LUFS.
Gera D:\\minecraft\\vaso\\final\\vaso_vazio.mp4"""
import glob
import json
import math
import os
import subprocess
import sys
import wave
import numpy as np

PROJ = os.environ.get('ANIM_PROJETO', os.getcwd())
BRUTOS = os.path.join(PROJ, 'brutos')
OUT_DIR = os.path.join(PROJ, 'final')
OUT = os.path.join(OUT_DIR, 'vaso_vazio.mp4')
TMP_ROOT = os.path.join(PROJ, 'tmp')
TMP = os.path.join(TMP_ROOT, 'seg')
FONTES_DIR = os.path.join(PROJ, 'fontes', 'usar')
if not os.path.isdir(FONTES_DIR):
    FONTES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'biblioteca', 'fontes'))

PLANOS_PATH = os.path.join(PROJ, 'roteiro', 'planos.json')
NARRACAO_PATH = os.path.join(PROJ, 'audio', 'narracao.wav')
PALAVRAS_PATH = os.path.join(PROJ, 'audio', 'pal_aj.json')
MUSICA_PATH = os.path.join(PROJ, 'audio', 'musica.mp3')

FPS = 30
LAT = 0.35
COR = (
    'eq=saturation=1.38:contrast=1.08:gamma=0.98,'
    'vibrance=intensity=0.28,'
    'colorbalance=rs=0.02:gs=0.01:rh=0.03,'
    'vignette=angle=0.38'
)

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

FONTES = {}
_V0 = {}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print('ERRO CMD:', ' '.join(cmd))
        print(r.stderr[-2500:])
        raise SystemExit(1)
    return r


def carregar_fontes():
    """Carrega mapa take -> (sessao_ou_base, inicio_epoch); gravacoes mais novas vencem."""
    FONTES.clear()
    arquivos = []
    for f in glob.glob(os.path.join(BRUTOS, '*_takes.json')):
        arquivos.append(('sessao', os.path.getmtime(f), f))
    for f in glob.glob(os.path.join(BRUTOS, '*_events.json')):
        arquivos.append(('avulso', os.path.getmtime(f), f))
    arquivos.sort(key=lambda x: x[1])

    for tipo, _, f in arquivos:
        dados = json.load(open(f, encoding='utf-8'))
        if tipo == 'sessao':
            ses = os.path.basename(f)[:-len('_takes.json')]
            for tk, evs in dados.items():
                ini = evs[1][1] if (len(evs) > 1 and evs[1][0] != 'fim') else evs[0][1]
                FONTES[tk] = (ses, ini)
        else:
            tk = os.path.basename(f)[:-len('_events.json')]
            if os.path.exists(os.path.join(BRUTOS, tk + '.mkv')) and dados:
                ini = dados[1][1] if (len(dados) > 1 and dados[1][0] != 'fim') else dados[0][1]
                FONTES[tk] = (tk, ini)
    return FONTES


def _v0(ses):
    if ses not in _V0:
        mkv = os.path.join(BRUTOS, f'{ses}.mkv')
        out = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v', '-read_intervals', '%+#1',
             '-show_entries', 'packet=pts_time', '-of', 'csv=p=0', mkv],
            capture_output=True, text=True
        ).stdout.split()
        _V0[ses] = float(out[0]) if out else 0.0
    return _V0[ses]


def fonte(tk, s0=0.0):
    """Retorna (mkv, wav, inicio_no_mkv, a_off) para o take solicitado."""
    if not FONTES:
        carregar_fontes()
    if tk not in FONTES:
        raise KeyError(f"Take {tk!r} nao encontrado em {BRUTOS}\\*_takes.json (disponiveis: {sorted(FONTES)})")
    ses, ini = FONTES[tk]
    v0 = _v0(ses)
    meta_path = os.path.join(BRUTOS, f'{ses}.json')
    a0 = json.load(open(meta_path, encoding='utf-8')).get('audio_start_epoch', v0) if os.path.exists(meta_path) else v0
    mkv = os.path.join(BRUTOS, f'{ses}.mkv')
    wav = os.path.join(BRUTOS, f'{ses}.wav')
    return mkv, wav, max(0.0, (ini - v0) + LAT + s0), a0 - v0


def duracao_audio(caminho):
    """Duracao real em segundos de um arquivo de audio (.wav via wave ou fallback ffprobe)."""
    if not os.path.exists(caminho):
        return 0.0
    try:
        with wave.open(caminho, 'rb') as w:
            return w.getnframes() / float(w.getframerate())
    except Exception:
        out = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', caminho],
            capture_output=True, text=True
        ).stdout.strip()
        return float(out) if out else 0.0


def carregar_planos_e_end():
    """Le roteiro/planos.json e determina END automaticamente pela duracao de narracao.wav (+0.35s) ou ultimo t1."""
    planos = json.load(open(PLANOS_PATH, encoding='utf-8'))
    dur_nar = duracao_audio(NARRACAO_PATH)
    ult_t1 = float(planos[-1]['t1']) if planos else 0.0
    if dur_nar > 0:
        end = max(round(dur_nar + 0.35, 3), ult_t1)
    else:
        end = ult_t1

    segs = []
    for idx, p in enumerate(planos):
        t0 = float(p['t0'])
        if t0 >= end:
            continue
        t1 = end if idx == len(planos) - 1 else min(end, float(p['t1']))
        if t1 <= t0:
            continue
        tk = p.get('take') or p.get('nome')
        s0 = float(p.get('s0', 0.0))
        vel = float(p.get('vel', p.get('v', 1.0)))
        linhas = p.get('linhas', None)
        segs.append((t0, t1, tk, s0, vel, linhas))
    return planos, segs, end


def inicio_mov(mkv, st, jan=0.9, lim=0.6):
    """Pula quadros iniciais parados no comeco do plano para o corte ja entrar vivo."""
    b = subprocess.run(
        ['ffmpeg', '-v', 'error', '-ss', f'{st:.3f}', '-t', str(jan), '-i', mkv,
         '-vf', 'fps=30,scale=90:160,format=gray', '-f', 'rawvideo', '-'],
        capture_output=True
    ).stdout
    frame_bytes = 160 * 90
    n_frames = len(b) // frame_bytes
    if n_frames < 3:
        return 0.0
    f = np.frombuffer(b[:n_frames * frame_bytes], np.uint8).reshape(n_frames, 160, 90).astype(np.float32)
    d = np.abs(np.diff(f[:, 30:130], axis=0)).mean(axis=(1, 2))
    for i in range(len(d) - 1):
        if d[i] > 0.55 and d[i + 1] > 0.55:
            return min(lim, i / 30.0)
    return 0.0


def seg_video(i, s):
    """Recorta e trata um plano em 1080x1920 30fps lanczos com grade quente e vibrante."""
    a, b, tk, s0, v, linhas = s
    dur = b - a
    mkv, _, st, _ = fonte(tk, s0)
    if v > 0:
        st += inicio_mov(mkv, st)
    out = os.path.join(TMP, f'v{i:02d}.mp4')

    if v == 0:
        vf = (
            f"setpts=PTS-STARTPTS,select=eq(n\\,0),loop=loop={int(dur * FPS) + 5}:size=1:start=0,"
            f"setpts=N/{FPS}/TB,scale=1296:2304:flags=lanczos,"
            f"zoompan=z='1+0.05*on/{max(1, int(dur * FPS))}':d=1:s=1080x1920:fps={FPS},"
            f"setsar=1,{COR},trim=duration={dur}"
        )
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{st:.3f}', '-i', mkv, '-vf', vf, '-an',
             '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', out])
    else:
        vf = (
            f'setpts=PTS-STARTPTS,trim=start=0:duration={dur * v + 0.25},setpts=(PTS-STARTPTS)/{v},'
            f'fps={FPS},scale=1080:1920:flags=lanczos,setsar=1,{COR},'
            f'tpad=stop_mode=clone:stop_duration=2,trim=duration={dur}'
        )
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{st:.3f}', '-i', mkv, '-vf', vf, '-an',
             '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', out])

    if linhas:
        ov = os.path.join(PROJ, 'overlays', f'{linhas}_v5.mov')
        if os.path.exists(ov):
            o2 = os.path.join(TMP, f'l{i:02d}.mp4')
            run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-stream_loop', '-1', '-i', ov,
                 '-filter_complex', f'[1]format=rgba[o];[0][o]overlay=shortest=1,trim=duration={dur}',
                 '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', o2])
            os.replace(o2, out)
    return out


def seg_audio(i, s):
    """Extrai o audio do jogo alinhado ao segmento de video."""
    a, b, tk, s0, v, _ = s
    dur = b - a
    _, wav, st_v, aoff = fonte(tk, s0)
    out = os.path.join(TMP, f'a{i:02d}.wav')
    if v == 0 or not os.path.exists(wav):
        run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
             '-t', f'{dur:.4f}', out])
        return out

    st = st_v - aoff
    at = f'atempo={v}' if abs(v - 1.0) > 1e-3 else 'anull'
    af = (
        f'atrim=start={max(0.0, st):.4f}:duration={dur * v:.4f},asetpts=PTS-STARTPTS,{at},'
        f'apad,atrim=duration={dur:.4f},afade=t=in:d=0.04,afade=t=out:st={max(0.0, dur - 0.06):.4f}:d=0.06'
    )
    if st < 0:
        atraso = int(-st * 1000)
        af = f'adelay={atraso}|{atraso},' + af.replace(f'atrim=start={max(0.0, st):.4f}', 'atrim=start=0')
    run(['ffmpeg', '-v', 'error', '-y', '-i', wav, '-af', af, '-ar', '48000', '-ac', '2', out])
    return out


def ts(t):
    t = max(0.0, float(t))
    return f'{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}'


def _ler_palavras(caminho):
    bruto = json.load(open(caminho, encoding='utf-8'))
    if isinstance(bruto, dict) and 'words' in bruto:
        bruto = bruto['words']
    out = []
    for item in bruto:
        if isinstance(item, (list, tuple)):
            a, b, w = float(item[0]), float(item[1]), str(item[2])
        else:
            a = float(item.get('start', item.get('t0', 0.0)))
            b = float(item.get('end', item.get('t1', a + 0.2)))
            w = str(item.get('word', item.get('texto', '')))
        w_limpo = w.strip().strip('.,;:!?"\'()[]—–-')
        if w_limpo:
            out.append((a, b, w_limpo))
    return out


def legendas():
    """Gera legenda .ass em Monocraft: 1 palavra por vez, branca com contorno preto e micro-pop."""
    W = _ler_palavras(PALAVRAS_PATH)
    ev = []
    for i, (a, b, txt) in enumerate(W):
        prox = W[i + 1][0] if i + 1 < len(W) else b + 0.45
        fim = prox if (prox - b) < 0.45 else b + 0.22
        if fim <= a + 0.04:
            fim = a + 0.08
        ev.append(
            f'Dialogue: 1,{ts(a)},{ts(fim)},Fala,,0,0,0,,'
            f'{{\\fscx88\\fscy88\\t(0,70,\\fscx100\\fscy100)}}{txt}'
        )

    hdr = (
        '[Script Info]\n'
        'ScriptType: v4.00+\n'
        'PlayResX: 1080\n'
        'PlayResY: 1920\n'
        'WrapStyle: 2\n'
        'ScaledBorderAndShadow: yes\n\n'
        '[V4+ Styles]\n'
        'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, '
        'Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, '
        'Alignment, MarginL, MarginR, MarginV, Encoding\n'
        'Style: Fala,Monocraft,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,'
        '-1,0,0,0,100,100,1,0,1,4,3,2,60,60,700,1\n\n'
        '[Events]\n'
        'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
    )
    out = os.path.join(TMP_ROOT, 'leg_vaso.ass')
    with open(out, 'w', encoding='utf-8-sig') as f:
        f.write(hdr + '\n'.join(ev) + '\n')
    return out


def whoosh(segs, end):
    """Gera whoosh.wav suave (0.26s, amplitude 0.16) em cada corte de camera."""
    sr = 48000
    tot = np.zeros(int(end * sr) + sr, np.float32)
    rng = np.random.default_rng(7)
    cortes = [s[0] for s in segs[1:]]
    dur_w = 0.26
    n = int(dur_w * sr)

    for c in cortes:
        x = rng.standard_normal(n).astype(np.float32)
        env = np.sin(np.linspace(0, math.pi, n)) ** 2
        k = np.linspace(38, 7, n).astype(int)
        cs = np.cumsum(np.concatenate([[0.0], x]))
        y = np.array([(cs[i + 1] - cs[max(0, i + 1 - k[i])]) / k[i] for i in range(n)], np.float32)
        y = y - np.convolve(y, np.ones(56) / 56.0, 'same')
        y = y / (np.abs(y).max() + 1e-9) * env * 0.16
        i0 = int(max(0.0, c - dur_w * 0.5) * sr)
        if i0 + n <= len(tot):
            tot[i0:i0 + n] += y

    out = os.path.join(TMP, 'whoosh.wav')
    with wave.open(out, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((np.clip(tot, -1.0, 1.0) * 32767).astype('<i2').tobytes())
    return out


def _esc_ff_filter_path(p):
    return p.replace('\\', '/').replace(':', '\\:')


def main():
    pular = '--so-final' in sys.argv
    carregar_fontes()
    _, segs, end = carregar_planos_e_end()
    if not segs:
        raise RuntimeError('Nenhum segmento encontrado em roteiro/planos.json')

    print(f'Montando {len(segs)} planos | END = {end:.2f}s', flush=True)
    vs, as_ = [], []
    for i, s in enumerate(segs):
        if pular:
            vs.append(os.path.join(TMP, f'v{i:02d}.mp4'))
            as_.append(os.path.join(TMP, f'a{i:02d}.wav'))
            continue
        vs.append(seg_video(i, s))
        as_.append(seg_audio(i, s))
        print(f'  [{i + 1:02d}/{len(segs):02d}] {s[2]} ({s[0]:.2f}s -> {s[1]:.2f}s)', flush=True)

    lst = os.path.join(TMP, 'lista.txt')
    with open(lst, 'w', encoding='utf-8') as f:
        for v in vs:
            vp = v.replace('\\', '/')
            f.write(f"file '{vp}'\n")

    video_concat = os.path.join(TMP, 'video.mp4')
    jogo_wav = os.path.join(TMP, 'jogo.wav')
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', video_concat])
    run(
        ['ffmpeg', '-v', 'error', '-y']
        + sum([['-i', a] for a in as_], [])
        + ['-filter_complex', ''.join(f'[{k}]' for k in range(len(as_))) + f'concat=n={len(as_)}:v=0:a=1', jogo_wav]
    )

    ass = legendas()
    wh = whoosh(segs, end)
    assf = _esc_ff_filter_path(ass)
    fdir = _esc_ff_filter_path(FONTES_DIR)
    fade_st = max(0.0, end - 1.8)

    fc = (
        f"[0:v]subtitles='{assf}':fontsdir='{fdir}'[v];"
        f"[1:a]volume=1.0,apad,asplit=2[nar][sc];"
        f"[2:a]volume=0.55[jogo];"
        f"[3:a]volume=0.24,afade=t=out:st={fade_st:.3f}:d=1.8[mus];"
        f"[4:a]volume=0.75,aformat=channel_layouts=stereo[wh];"
        f"[mus][sc]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=300[musd];"
        f"[nar][jogo][musd][wh]amix=inputs=4:normalize=0:duration=first,atrim=duration={end:.3f},"
        f"loudnorm=I=-12:TP=-1.0:LRA=9[a]"
    )

    run([
        'ffmpeg', '-v', 'error', '-y',
        '-i', video_concat,
        '-i', NARRACAO_PATH,
        '-i', jogo_wav,
        '-stream_loop', '-1', '-i', MUSICA_PATH,
        '-i', wh,
        '-filter_complex', fc,
        '-map', '[v]', '-map', '[a]', '-t', f'{end:.3f}',
        '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS),
        '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart',
        OUT
    ])
    print('OK', OUT, flush=True)


if __name__ == '__main__':
    main()
