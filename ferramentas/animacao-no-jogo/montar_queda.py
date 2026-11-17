import os as _os
PROJ = _os.environ.get('ANIM_PROJETO', _os.getcwd())
"""Montagem do short 'Queda sem paraquedas' (PT). Gera final/queda_pt.mp4"""
import json, subprocess, os, math
P = _os.path.join(PROJ)
B = P + r'\brutos'
OUT = P + r'\final'
TMP = P + r'\tmp\seg'
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
import glob
FONTES = {}   # take -> (sessao, inicio_epoch); a sessao mais nova vence
for f in sorted(glob.glob(B + r'\*_takes.json'), key=os.path.getmtime):
    ses = os.path.basename(f)[:-len('_takes.json')]
    for tk, evs in json.load(open(f)).items():
        FONTES[tk] = (ses, evs[1][1])     # 1o evento de acao: o movimento comeca ai
_V0 = {}


def _v0(ses):
    if ses not in _V0:
        _V0[ses] = float(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-read_intervals', '%+#1', '-show_entries',
                                         'packet=pts_time', '-of', 'csv=p=0', f'{B}/{ses}.mkv'], capture_output=True, text=True).stdout.split()[0])
    return _V0[ses]


def fonte(tk, s0):
    """(mkv, wav, inicio_no_arquivo, a_off): takes saem das capturas de sessao"""
    ses, ini = FONTES[tk]; v0 = _v0(ses)
    a0 = json.load(open(f'{B}/{ses}.json'))['audio_start_epoch']
    return f'{B}/{ses}.mkv', f'{B}/{ses}.wav', (ini - v0) + LAT + s0, a0 - v0


LAT = 0.35   # evento -> quadro na tela (tag de velocidade entra ~0,2 s depois do evento)
FPS = 30
END = 64.6

# (inicio_saida, fim_saida, take, src_inicio, velocidade, linhas_de_vento)
SEG = [   # src_inicio = segundos depois do inicio do movimento; tudo em velocidade 1
    (0.00, 2.00, 't01a', 0.00, 1.00, False),
    (2.00, 4.07, 't01b', 0.00, 1.00, True),
    (4.07, 8.48, 't02', 0.00, 1.00, True),
    (8.48, 10.84, 't03', 0.00, 1.00, True),
    (10.84, 14.16, 't04', 0.00, 1.00, True),
    (14.16, 17.62, 't05', 0.00, 1.00, True),
    (17.62, 21.14, 't06', 0.00, 1.00, True),
    (21.14, 26.10, 't07', 0.00, 1.00, True),
    (26.10, 28.06, 't08', 0.00, 1.00, True),
    (28.06, 31.86, 't09', 0.00, 1.00, False),
    (31.86, 33.65, 't10a', 0.00, 1.00, False),
    (33.65, 35.18, 't10b', 0.00, 1.00, False),
    (35.18, 37.38, 't11a', 0.00, 1.00, False),
    (37.38, 40.50, 't11b', 0.00, 1.00, False),
    (40.50, 42.52, 't12a', 0.00, 1.00, False),
    (42.52, 46.26, 't12b', 0.00, 1.00, True),
    (46.26, 49.34, 't13', 0.00, 1.00, True),
    (49.34, 54.62, 't14', 0.00, 1.00, True),
    (54.62, 57.56, 't15', 0.00, 1.00, False),
    (57.56, 59.97, 't16', 0.00, 1.00, False),
    (59.97, 61.05, 't17', 0.00, 1.00, False),
    (61.05, END, 't18', 0.00, 1.00, False),
]


def run(a):
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode:
        print(' '.join(a)); print(r.stderr[-2000:]); raise SystemExit(1)


def seg_video(i, s):
    a, b, tk, s0, v, linhas = s
    dur = b - a
    mkv, _, s0, _ = fonte(tk, s0)
    out = f'{TMP}\\v{i:02d}.mp4'
    base = 'scale=1080:1920:flags=lanczos,setsar=1'
    if v == 0:
        vf = (f'setpts=PTS-STARTPTS,select=eq(n\\,0),loop=loop={int(dur * FPS) + 5}:size=1:start=0,setpts=N/{FPS}/TB,'
              f'scale=1296:2304,zoompan=z=\'1+0.06*on/{int(dur * FPS)}\':d=1:s=1080x1920:fps={FPS},trim=duration={dur}')
        run(['ffmpeg', '-v', 'error', '-y', '-i', mkv, '-vf', vf, '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', out])
    else:
        vf = (f'setpts=PTS-STARTPTS,trim=start=0:duration={dur * v + 0.2},setpts=(PTS-STARTPTS)/{v},fps={FPS},{base},'
              f'trim=duration={dur},tpad=stop_mode=clone:stop_duration=1,trim=duration={dur}')
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{s0:.3f}', '-i', mkv, '-vf', vf, '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', out])
    if linhas:
        ov = P + r'\overlays\sobe.mov'
        o2 = f'{TMP}\\l{i:02d}.mp4'
        run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-stream_loop', '-1', '-i', ov, '-filter_complex',
             f'[1]format=rgba,colorchannelmixer=aa=0.55[o];[0][o]overlay=shortest=1,trim=duration={dur}', '-an',
             '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', o2])
        os.replace(o2, out)
    return out


def seg_audio(i, s):
    """audio do jogo do take, alinhado ao video (a_off) e com a mesma velocidade"""
    a, b, tk, s0, v, _ = s
    dur = b - a
    _, wav, s0, aoff = fonte(tk, s0); out = TMP + '/a%02d.wav' % i
    if v == 0 or not os.path.exists(wav):
        run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'anullsrc=r=48000:cl=stereo', '-t', str(dur), out]); return out
    st = s0 - aoff
    at = f'atempo={v}' if abs(v - 1) > 1e-3 else 'anull'
    af = (f'atrim=start={max(0, st)}:duration={dur * v},asetpts=PTS-STARTPTS,{at},apad,atrim=duration={dur},'
          f'afade=t=in:d=0.04,afade=t=out:st={max(0, dur - 0.06)}:d=0.06')
    if st < 0:
        af = f'adelay={int(-st * 1000)}|{int(-st * 1000)},' + af.replace(f'atrim=start={max(0, st)}', 'atrim=start=0')
    run(['ffmpeg', '-v', 'error', '-y', '-i', wav, '-af', af, '-ar', '48000', '-ac', '2', out])
    return out


def contador_ass():
    """altitude caindo (0-17.6 s) + 200 KM/H + rotulos"""
    ev = []

    def ts(t):
        return f'{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}'
    t = 0.0
    while t < 17.6:
        alt = 10600 - (10600 - 2400) * (t / 17.6) ** 1.1
        txt = f'{int(alt):,}'
        ev.append(f'Dialogue: 3,{ts(t)},{ts(min(17.6, t + 0.1))},Alt,,0,0,0,,{txt}')
        t += 0.1
    ev.append(f'Dialogue: 3,{ts(0.0)},{ts(17.6)},AltL,,0,0,0,,ALTITUDE')
    return ev


def mapa_ass(t0=40.62, t1=42.52):
    """anel amarelo na floresta + linha tracejada do Steve ate ela (sobre o plano de cima, como no original)"""
    def ts(t):
        return f'{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}'
    cx, cy, rx, ry = 541, 1587, 245, 180
    k = 0.5523
    d = (f'm {cx} {cy - ry} b {cx + k * rx:.0f} {cy - ry} {cx + rx} {cy - k * ry:.0f} {cx + rx} {cy} '
         f'b {cx + rx} {cy + k * ry:.0f} {cx + k * rx:.0f} {cy + ry} {cx} {cy + ry} '
         f'b {cx - k * rx:.0f} {cy + ry} {cx - rx} {cy + k * ry:.0f} {cx - rx} {cy} '
         f'b {cx - rx} {cy - k * ry:.0f} {cx - k * rx:.0f} {cy - ry} {cx} {cy - ry}')
    ev = [f'Dialogue: 4,{ts(t0)},{ts(t1)},Desenho,,0,0,0,,{{\\an7\\pos(0,0)\\org({cx},{cy})\\1a&HFF&\\3c&H00D7FF&\\bord14\\shad0'.replace('\\\\', '\\')
          + f'\\fscx40\\fscy40\\t(0,180,\\fscx108\\fscy108)\\t(180,280,\\fscx100\\fscy100)\\p1}}{d}']
    y0, y1, n = 505, cy - ry - 25, 9
    passo = (y1 - y0) / n
    for i in range(n):
        a = y0 + i * passo; b = a + passo * 0.55
        if b > 1110 and a < 1340:      # nao passa por cima da legenda
            continue
        ti = t0 + 0.35 + i * 0.09
        ev.append(f'Dialogue: 4,{ts(ti)},{ts(t1)},Desenho,,0,0,0,,{{\\an7\\pos(0,0)\\1c&H2A2AE0&\\3c&H000000&\\bord5\\shad0\\p1}}'
                  f'm {cx - 11} {a:.0f} l {cx + 11} {a:.0f} l {cx + 11} {b:.0f} l {cx - 11} {b:.0f}')
    return [e.replace(chr(92) * 2, chr(92)) for e in ev]


def legendas():
    ex = {'numeros': [{'de': 19.1, 'ate': 21.0, 'texto': '200 KM/H', 'pos': [540, 700]},
                      {'de': 2.2, 'ate': 4.0, 'texto': '3 MIN', 'pos': [540, 700]}],
          'rotulos': [{'de': 30.4, 'ate': 31.86, 'texto': 'ÁGUA = CONCRETO', 'cor': 'vermelho'},
                      {'de': 32.0, 'ate': 33.6, 'texto': 'TELHADO E RUA', 'cor': 'vermelho'},
                      {'de': 33.7, 'ate': 35.15, 'texto': 'TERRA DURA', 'cor': 'vermelho'},
                      {'de': 36.0, 'ate': 40.45, 'texto': 'NEVE FUNDA', 'cor': 'verde'}]}
    json.dump(ex, open(P + r'\tmp\extras.json', 'w', encoding='utf-8'), ensure_ascii=False)
    ass = P + r'\tmp\leg.ass'
    run(['python', P + r'\ferramentas\legendas.py', P + r'\audio\pal_aj.json', ass, P + r'\tmp\extras.json'])
    s = open(ass, encoding='utf-8-sig').read()
    s = s.replace('[Events]', '')
    estilos = ('Style: Alt,Monocraft,120,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,9,5,8,0,0,300,1\n'
               'Style: Desenho,Arial,20,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1\n'
               'Style: AltL,Monocraft,52,&H0000E6FF,&H0000E6FF,&H00000000,&H96000000,-1,0,0,0,100,100,4,0,1,6,4,8,0,0,240,1\n')
    s = s.replace('\nFormat: Layer', '\n[Events]\nFormat: Layer')
    s = s.replace('Style: Num,', estilos + 'Style: Num,')
    s = s.rstrip('\n') + '\n' + '\n'.join(contador_ass() + mapa_ass()) + '\n'
    open(ass, 'w', encoding='utf-8-sig').write(s)
    return ass


def main():
    vs, as_ = [], []
    import sys
    pular = '--so-final' in sys.argv
    for i, s in enumerate(SEG):
        if pular:
            vs.append(TMP + '/v%02d.mp4' % i); as_.append(TMP + '/a%02d.wav' % i); continue
        vs.append(seg_video(i, s)); as_.append(seg_audio(i, s)); print('seg', i, s[2])
    lst = TMP + r'\lista.txt'
    open(lst, 'w').write(''.join(f"file '{v}'\n" for v in vs))
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', TMP + r'\video.mp4'])
    run(['ffmpeg', '-v', 'error', '-y'] + sum([['-i', a] for a in as_], []) +
        ['-filter_complex', ''.join(f'[{k}]' for k in range(len(as_))) + f'concat=n={len(as_)}:v=0:a=1', TMP + r'\jogo.wav'])
    ass = legendas()
    musica = _os.environ.get('ANIM_MUSICA', _os.path.join(PROJ, 'audio', 'musica.mp3'))
    fonts = _os.path.join(PROJ, 'fontes', 'usar')
    assf = ass.replace('\\', '/').replace(':', '\\:')
    fdir = fonts.replace('\\', '/').replace(':', '\\:')
    fc = (f"[0:v]subtitles='{assf}':fontsdir='{fdir}'[v];"
          f"[1:a]volume=1.0,apad,asplit=2[nar][sc];"
          f"[2:a]volume=0.55[jogo];"
          f"[3:a]volume=0.22,afade=t=out:st={END - 1.5}:d=1.5[mus];"
          f"[mus][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[musd];"
          f"[nar][jogo][musd]amix=inputs=3:normalize=0:duration=first,atrim=duration={END},loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    run(['ffmpeg', '-v', 'error', '-y', '-i', TMP + r'\video.mp4', '-i', P + r'\audio\narracao.wav', '-i', TMP + r'\jogo.wav',
         '-stream_loop', '-1', '-i', musica, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', str(END),
         '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS),
         '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', OUT + r'\queda_pt.mp4'])
    print('OK', OUT + r'\queda_pt.mp4')


if __name__ == '__main__':
    main()
