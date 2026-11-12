"""Converte legenda automática .vtt do YouTube em texto com minutagem (1 linha a cada ~10 s).
Uso: python vtt2txt.py arquivo.vtt > saida.txt"""
import re, sys
txt = open(sys.argv[1], encoding='utf8').read()
seen, out, bloco, t0 = set(), [], [], None
for cue in txt.split('\n\n'):
    m = re.search(r'(\d+):(\d+):(\d+)\.\d+ -->', cue)
    if not m: continue
    t = int(m[1])*3600 + int(m[2])*60 + int(m[3])
    for line in cue.split('\n')[1:]:
        line = re.sub(r'<[^>]+>', '', line).strip()
        if not line or line in seen or '-->' in line: continue
        seen.add(line)
        if t0 is None: t0 = t
        bloco.append(line)
    if bloco and t - t0 >= 10:
        out.append(f'[{t0//60:02d}:{t0%60:02d}] ' + ' '.join(bloco)); bloco, t0 = [], None
if bloco: out.append(f'[{t0//60:02d}:{t0%60:02d}] ' + ' '.join(bloco))
print('\n'.join(out))
