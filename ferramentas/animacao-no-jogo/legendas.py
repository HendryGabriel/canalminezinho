"""Legendas ASS em fonte pixelada (Monocraft): blocos de 1-3 palavras, palavra falada em amarelo,
rotulos no topo e numeros grandes com 'pop'.
uso: legendas.py <palavras.json [[ini,fim,palavra],...]> <saida.ass> <extras.json|-> [desloc]
extras: {"rotulos": [{"de","ate","texto","cor": "vermelho|verde|cinza"}], "numeros": [{"de","ate","texto"}]}"""
import json, sys, re

W = json.load(open(sys.argv[1], encoding='utf-8'))
out = sys.argv[2]
X = json.load(open(sys.argv[3], encoding='utf-8')) if sys.argv[3] != '-' else {}
off = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0


def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f'{h}:{m:02d}:{s:05.2f}'


chunks, cur = [], []
for w in W:
    cur.append(w)
    if len(cur) >= 3 or re.search(r'[.,:;!?]$', w[2]):
        chunks.append(cur); cur = []
if cur: chunks.append(cur)

ev = []
for ci, ch in enumerate(chunks):
    nxt = chunks[ci + 1][0][0] if ci + 1 < len(chunks) else ch[-1][1] + 0.6
    end_chunk = nxt if nxt - ch[-1][1] < 0.45 else ch[-1][1] + 0.25
    words = [re.sub(r'[.,:;!?]$', '', w[2]).upper() for w in ch]
    for k, w in enumerate(ch):
        a = w[0]; b = ch[k + 1][0] if k + 1 < len(ch) else end_chunk
        pop = r'{\fscx112\fscy112\t(0,90,\fscx100\fscy100)}' if k == 0 else ''
        txt = pop + ' '.join(('{\\c&H00E6FF&}' + x + '{\\c&HFFFFFF&}') if j == k else x for j, x in enumerate(words))
        ev.append(f'Dialogue: 0,{ts(a + off)},{ts(b + off)},Fala,,0,0,0,,{txt}')

COR = {'vermelho': '&H002A2AD0&', 'verde': '&H0030A040&', 'cinza': '&H00303030&', 'amarelo': '&H0000A8E0&'}
for r in X.get('rotulos', []):
    c = COR.get(r.get('cor', 'vermelho'))
    pop = r'{\fscx70\fscy70\t(0,110,\fscx106\fscy106)\t(110,200,\fscx100\fscy100)}'
    ev.append(f"Dialogue: 1,{ts(r['de'])},{ts(r['ate'])},Rot,,0,0,0,,{{\\3c{c}}}{pop}{r['texto']}")
for r in X.get('tags', []):
    ev.append(f"Dialogue: 1,{ts(r['de'])},{ts(r['ate'])},Tag,,0,0,0,,{r['texto']}")
for n in X.get('numeros', []):
    pos = n.get('pos', [540, 760])
    pop = r'{\pos(%d,%d)\fscx40\fscy40\t(0,120,\fscx118\fscy118)\t(120,240,\fscx100\fscy100)}' % tuple(pos)
    ev.append(f"Dialogue: 2,{ts(n['de'])},{ts(n['ate'])},Num,,0,0,0,,{pop}{n['texto']}")

hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Fala,Monocraft,104,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,8,5,2,50,50,560,1
Style: Rot,Monocraft,66,&H00FFFFFF,&H00FFFFFF,&H002A2AD0,&H00000000,-1,0,0,0,100,100,0,0,3,16,0,8,80,80,250,1
Style: Tag,Monocraft,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,2,0,3,10,0,9,60,60,140,1
Style: Num,Monocraft,230,&H0000E6FF,&H0000E6FF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,12,8,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open(out, 'w', encoding='utf-8-sig').write(hdr + '\n'.join(ev) + '\n')
print(out, len(ev))
