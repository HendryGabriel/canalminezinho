import os as _os
PROJ = _os.environ.get('ANIM_PROJETO', _os.getcwd())
"""Montagem v5 (capivara): planos de roteiro/planos_v5.json, cor tratada, legenda de 1 palavra, altitude em caixinha,
linhas de velocidade por tipo de plano, whoosh nos cortes, master -12 LUFS. Gera final/queda_capivara.mp4"""
import json, os, subprocess, sys, math
import numpy as np
import montar_queda as MQ
from montar_queda import P, TMP, FPS, run, fonte, mapa_ass

END = 64.6
OUT = P + r'\final\queda_capivara.mp4'
PL = json.load(open(P + r'\roteiro\planos_v5.json'))
SEG = [(p['t0'], min(END, p['t1']), p['take'], p['s0'], 1.0, p['linhas']) for p in PL]
COR = 'eq=saturation=1.4:contrast=1.08:gamma=0.97,vibrance=intensity=0.3,colorbalance=bs=0.04:bm=0.02:rh=0.02,vignette=angle=0.42'


def seg_video(i, s):
    a, b, tk, s0, v, linhas = s
    dur = b - a
    mkv, _, st, _ = fonte(tk, s0)
    st += inicio_mov(mkv, st)
    out = f'{TMP}\\v{i:02d}.mp4'
    vf = (f'setpts=PTS-STARTPTS,trim=start=0:duration={dur + 0.2},fps={FPS},scale=1080:1920:flags=lanczos,setsar=1,{COR},'
          f'trim=duration={dur},tpad=stop_mode=clone:stop_duration=1,trim=duration={dur}')
    run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{st:.3f}', '-i', mkv, '-vf', vf, '-an', '-c:v', 'libx264', '-crf', '16',
         '-preset', 'fast', '-pix_fmt', 'yuv420p', out])
    if linhas:
        ov = P + rf'\overlays\{linhas}_v5.mov'
        o2 = f'{TMP}\\l{i:02d}.mp4'
        run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-stream_loop', '-1', '-i', ov, '-filter_complex',
             f'[1]format=rgba[o];[0][o]overlay=shortest=1,trim=duration={dur}', '-an',
             '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', o2])
        os.replace(o2, out)
    return out


def inicio_mov(mkv, st, jan=0.9, lim=0.6):
    """pula quadros parados no comeco do plano (o corte entra ja em movimento)"""
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{st:.3f}', '-t', str(jan), '-i', mkv, '-vf',
                        'fps=30,scale=90:160,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    f = np.frombuffer(b, np.uint8).reshape(-1, 160, 90).astype(np.float32)
    if len(f) < 3: return 0.0
    d = np.abs(np.diff(f[:, 30:110], axis=0)).mean(axis=(1, 2))
    for i in range(len(d) - 1):
        if d[i] > 0.6 and d[i + 1] > 0.6:
            return min(lim, i / 30.0)
    return 0.0


def ts(t):
    return f'{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}'


def legendas():
    W = json.load(open(P + r'\audio\pal_aj.json', encoding='utf-8'))
    ev = []
    for i, (a, b, w) in enumerate(W):
        prox = W[i + 1][0] if i + 1 < len(W) else b + 0.5
        fim = prox if prox - b < 0.5 else b + 0.2
        txt = w.strip('.,;:!?')
        ev.append(f'Dialogue: 1,{ts(a)},{ts(fim)},Fala,,0,0,0,,{{\\fscx88\\fscy88\\t(0,70,\\fscx100\\fscy100)}}{txt}')
    # altitude (caixinha no topo) de 2,0 s ate o impacto
    t = 2.0
    while t < 57.5:
        u = (t - 2.0) / (57.5 - 2.0)
        alt = 10600 * (1 - u) ** 1.25 + 4 * (1 - u)
        ev.append(f'Dialogue: 2,{ts(t)},{ts(min(57.5, t + 0.1))},Alt,,0,0,0,,{int(alt):,} m'.replace(',', '.'))
        t += 0.1
    ev += mapa_ass()
    hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Fala,Monocraft,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,1,0,1,4,3,2,60,60,700,1
Style: Alt,Monocraft,40,&H00FFFFFF,&H00FFFFFF,&H50101010,&H50101010,-1,0,0,0,100,100,1,0,3,10,0,8,0,0,330,1
Style: Desenho,Arial,20,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    out = P + r'\tmp\leg_v5.ass'
    open(out, 'w', encoding='utf-8-sig').write(hdr + '\n'.join(ev) + '\n')
    return out


def whoosh():
    """whoosh curto (ruido filtrado com varredura) em cada corte, gerado em numpy"""
    sr = 48000
    tot = np.zeros(int(END * sr) + sr, np.float32)
    rng = np.random.default_rng(3)
    cortes = [p['t0'] for p in PL[1:]]
    for c in cortes:
        n = int(0.32 * sr)
        x = rng.standard_normal(n).astype(np.float32)
        # passa-faixa simples: diferenca de medias moveis com janela variando (varredura grave->agudo)
        env = np.sin(np.linspace(0, math.pi, n)) ** 2
        k = np.linspace(40, 6, n).astype(int)
        cs = np.cumsum(np.concatenate([[0], x]))
        y = np.array([(cs[i + 1] - cs[max(0, i + 1 - k[i])]) / k[i] for i in range(n)], np.float32)
        y = y - np.convolve(y, np.ones(60) / 60, 'same')
        y = y / (np.abs(y).max() + 1e-9) * env * 0.22
        i0 = int(max(0, c - 0.16) * sr)
        tot[i0:i0 + n] += y
    import wave
    w = wave.open(TMP + r'\whoosh.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((np.clip(tot, -1, 1) * 32767).astype('<i2').tobytes()); w.close()
    return TMP + r'\whoosh.wav'


def main():
    pular = '--so-final' in sys.argv
    vs, as_ = [], []
    for i, s in enumerate(SEG):
        if pular:
            vs.append(f'{TMP}\\v{i:02d}.mp4'); as_.append(TMP + '/a%02d.wav' % i); continue
        vs.append(seg_video(i, s)); as_.append(MQ.seg_audio(i, s)); print('seg', i, s[2], flush=True)
    lst = TMP + r'\lista.txt'
    open(lst, 'w').write(''.join(f"file '{v}'\n" for v in vs))
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', TMP + r'\video.mp4'])
    run(['ffmpeg', '-v', 'error', '-y'] + sum([['-i', a] for a in as_], []) +
        ['-filter_complex', ''.join(f'[{k}]' for k in range(len(as_))) + f'concat=n={len(as_)}:v=0:a=1', TMP + r'\jogo.wav'])
    ass = legendas()
    wh = whoosh()
    musica = _os.environ.get('ANIM_MUSICA', _os.path.join(PROJ, 'audio', 'musica.mp3'))
    fonts = _os.path.join(PROJ, 'fontes', 'usar')
    assf = ass.replace('\\', '/').replace(':', '\\:')
    fdir = fonts.replace('\\', '/').replace(':', '\\:')
    fc = (f"[0:v]subtitles='{assf}':fontsdir='{fdir}'[v];"
          f"[1:a]volume=1.0,apad,asplit=2[nar][sc];"
          f"[2:a]volume=0.6[jogo];"
          f"[3:a]volume=0.26,afade=t=out:st={END - 1.5}:d=1.5[mus];"
          f"[4:a]volume=0.9,aformat=channel_layouts=stereo[wh];"
          f"[mus][sc]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=300[musd];"
          f"[nar][jogo][musd][wh]amix=inputs=4:normalize=0:duration=first,atrim=duration={END},"
          f"loudnorm=I=-12:TP=-1.0:LRA=9[a]")
    run(['ffmpeg', '-v', 'error', '-y', '-i', TMP + r'\video.mp4', '-i', P + r'\audio\narracao.wav', '-i', TMP + r'\jogo.wav',
         '-stream_loop', '-1', '-i', musica, '-i', wh, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', str(END),
         '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS),
         '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', OUT])
    print('OK', OUT)


if __name__ == '__main__':
    main()
