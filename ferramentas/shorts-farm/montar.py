"""Monta um short a partir de receita JSON.
receita: {
  "brutos": "brutos/mel", "saida": "final/mel.mp4", "tmp": "tmp/mel",
  "narracao": "audio/mel.wav", "narr_delay": 0.3, "trilha": "audio/mixkit_1072.mp3", "ganho_trilha": 0.09, "ganho_jogo": 0.5,
  "ass": "tmp/mel/legendas.ass",
  "segs": [{"take": "m12_close", "a": 1.2, "b": 4.0, "dur": 2.8, "mudo": false}, ...]
}
a/b = segundos desde o 1o quadro da tomada. velocidade = (b-a)/dur. Acima de 2,5x o som do jogo sai mudo."""
import json, subprocess, sys, os

R = json.load(open(sys.argv[1], encoding='utf-8'))
ROOT = os.environ.get('SHORTS_PROJETO', os.getcwd())
J = lambda p: os.path.join(ROOT, p)
class _Info(dict):
    def __missing__(self, k):
        pasta, nome = k.split('/') if '/' in k else ('', k)
        d = json.load(open(os.path.join(J(R['brutos']), pasta, 'info.json')))
        self[k] = d[nome]; return self[k]


INFO = _Info()
TMP = J(R['tmp']); os.makedirs(TMP, exist_ok=True)
FF = ['ffmpeg', '-v', 'error', '-y']


def atempo(s):
    f = []
    while s > 2.0: f.append('atempo=2.0'); s /= 2.0
    while s < 0.5: f.append('atempo=0.5'); s /= 0.5
    f.append(f'atempo={s:.5f}'); return ','.join(f)


parts = []; total = 0.0
for i, sg in enumerate(R['segs']):
    tk, a, b, d = sg['take'], sg['a'], sg['b'], sg['dur']
    sp = (b - a) / d
    inf = INFO[tk]; base = os.path.join(J(R['brutos']), *tk.split('/'))
    o = os.path.join(TMP, f'seg{i:02d}.mkv')
    zoom = sg.get('zoom', 1.0)
    zf = ''
    if zoom != 1.0:
        cx, cy = sg.get('cx', 0.5), sg.get('cy', 0.5)
        zf = f"crop=iw/{zoom}:ih/{zoom}:(iw-iw/{zoom})*{cx}:(ih-ih/{zoom})*{cy},"
    vf = f"setpts=(PTS-STARTPTS)/{sp:.6f},fps=60,{zf}scale=1080:1920:flags=lanczos,setsar=1,trim=0:{d:.4f}"
    mudo = sg.get('mudo', sp > 2.5)
    if mudo:
        cmd = FF + ['-ss', f'{a:.3f}', '-i', base + '.mkv', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                    '-filter_complex', f'[0:v]{vf}[v];[1:a]atrim=0:{d:.4f}[a]']
    else:
        af = f"{atempo(sp)},aresample=48000,apad,atrim=0:{d:.4f}"
        cmd = FF + ['-ss', f'{a:.3f}', '-i', base + '.mkv', '-ss', f'{max(0, a - inf["a_off"]):.3f}', '-i', base + '.wav',
                    '-filter_complex', f'[0:v]{vf}[v];[1:a]{af}[a]']
    cmd += ['-map', '[v]', '-map', '[a]', '-c:v', 'h264_nvenc', '-preset', 'p6', '-cq', '15', '-pix_fmt', 'yuv420p',
            '-c:a', 'pcm_s16le', '-t', f'{d:.4f}', o]
    subprocess.run(cmd, check=True)
    parts.append(o); total += d
lst = os.path.join(TMP, 'lista.txt')
open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
vid = os.path.join(TMP, 'video.mkv')
subprocess.run(FF + ['-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', vid], check=True)
print('timeline', round(total, 2))

g_game, g_mus = R.get('ganho_jogo', 0.5), R.get('ganho_trilha', 0.09)
dl = int(R.get('narr_delay', 0.3) * 1000)
ass = J(R['ass']).replace('\\', '/').replace(':', '\\:')
fdir = J('fontes/usar').replace('\\', '/').replace(':', '\\:')
fc = (f"[0:a]volume={g_game}[g];"
      f"[1:a]aresample=48000,adelay={dl}|{dl},volume=1.0[n];"
      f"[2:a]aloop=loop=-1:size=2e9,atrim=0:{total:.3f},volume={g_mus},afade=t=in:d=0.6,afade=t=out:st={total - 1.5:.3f}:d=1.5[m];"
      f"[n]asplit=2[n1][n2];[m][n2]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=350[md];"
      f"[g][n1][md]amix=inputs=3:normalize=0,alimiter=limit=0.95,loudnorm=I=-14:TP=-1.5:LRA=11[a];"
      f"[0:v]subtitles='{ass}':fontsdir='{fdir}'[v]")
saida = J(R['saida']); os.makedirs(os.path.dirname(saida), exist_ok=True)
subprocess.run(FF + ['-i', vid, '-i', J(R['narracao']), '-i', J(R['trilha']), '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
                     '-c:v', 'h264_nvenc', '-preset', 'p6', '-rc', 'vbr', '-cq', '19', '-b:v', '18M', '-maxrate', '28M',
                     '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart',
                     '-t', f'{total:.3f}', saida], check=True)
print('OK', saida, round(total, 2))
