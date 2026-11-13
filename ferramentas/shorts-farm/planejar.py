"""Gera receita.json (montar.py) e extras.json (legendas.py) a partir do plano por frase + tempos das palavras.
uso: planejar.py <plano.json> <palavras_alinhadas.json> <pasta_saida_tmp>
plano: {"brutos","trilha","narracao","saida","narr_delay","cauda",
        "batidas": [{"frases":[0], "segs":[{"take","a","b","w"|"vel"}], "rotulos":[{"texto","cor","de":0.0,"ate":1.0}],
                     "numeros":[{"texto","palavra":"cinco","n":1,"dur":1.2,"pos":[x,y]}]}]}"""
import json, sys, os, re, unicodedata

PL = json.load(open(sys.argv[1], encoding='utf-8'))
W = json.load(open(sys.argv[2], encoding='utf-8'))
out = sys.argv[3]; os.makedirs(out, exist_ok=True)
ROOT = os.environ.get('SHORTS_PROJETO', os.getcwd())
class _Info(dict):
    def __missing__(self, k):
        pasta, nome = k.split('/') if '/' in k else ('', k)
        d = json.load(open(os.path.join(ROOT, PL['brutos'], pasta, 'info.json')))
        self[k] = d[nome]; return self[k]


INFO = _Info()
nd = PL.get('narr_delay', 0.3)
norm = lambda s: unicodedata.normalize('NFKD', re.sub(r'[^\w]', '', s.lower())).encode('ascii', 'ignore').decode()

# frases -> indices de palavras
fr, cur = [], []
for i, w in enumerate(W):
    cur.append(i)
    if w[2].endswith('.'):
        fr.append(cur); cur = []
if cur: fr.append(cur)
print('frases', len(fr), 'batidas', len(PL['batidas']))
usadas = sorted(f for b in PL['batidas'] for f in b['frases'])
assert usadas == list(range(len(fr))), ('frases nao batem', usadas, len(fr))

bt = PL['batidas']
ini = []
for k, b in enumerate(bt):
    t = W[fr[b['frases'][0]][0]][0] + nd
    ini.append(0.0 if k == 0 else max(0.0, t - 0.18))
fim_total = W[-1][1] + nd + PL.get('cauda', 1.4)
segs, rot, num, tags = [], [], [], []
t = 0.0
for k, b in enumerate(bt):
    t0 = ini[k]; t1 = ini[k + 1] if k + 1 < len(bt) else fim_total
    span = t1 - t0
    fixos = [s for s in b['segs'] if 'vel' in s]
    nflex = len(b['segs']) - len(fixos)
    rest = span - sum((s['b'] - s['a']) / s['vel'] for s in fixos)
    if nflex and rest < 0.9 * nflex:  # falta tempo: encurta os fixos pelo inicio
        falta = 0.9 * nflex - rest
        for s in fixos:
            corte = min(falta, (s['b'] - s['a']) / s['vel'] - 0.8)
            s['a'] += corte * s['vel']; falta -= corte
        rest = span - sum((s['b'] - s['a']) / s['vel'] for s in fixos)
    ws = sum(s.get('w', 1) for s in b['segs'] if 'vel' not in s) or 1
    tt = t0
    for s in b['segs']:
        d = (s['b'] - s['a']) / s['vel'] if 'vel' in s else rest * s.get('w', 1) / ws
        a, bb = s['a'], s['b']
        if 'vel' not in s and s.get('ancora_fim'):
            pass
        sp = (bb - a) / d
        if sp < 0.6 and 'vel' not in s:  # evita camera lenta demais: estende a fonte se der
            lim = INFO[s['take']]['dur'] - 0.4
            if s.get('ancora_fim'):
                a = max(1.2, bb - 0.6 * d)
            else:
                bb = min(lim, a + 0.6 * d)
            sp = (bb - a) / d
        seg = {'take': s['take'], 'a': round(a, 3), 'b': round(bb, 3), 'dur': round(d, 4)}
        for kk in ('zoom', 'cx', 'cy', 'mudo'):
            if kk in s: seg[kk] = s[kk]
        segs.append(seg)
        if sp > 2.5 or s.get('tag'):
            tags.append({'de': round(tt, 2), 'ate': round(tt + d, 2), 'texto': s.get('tag', f'ACELERADO {round(sp)}x')})
        tt += d
    for r in b.get('rotulos', []):
        rot.append({'de': round(t0 + span * r.get('de', 0.0), 2), 'ate': round(t0 + span * r.get('ate', 1.0), 2), 'texto': r['texto'], 'cor': r.get('cor', 'vermelho')})
    for n in b.get('numeros', []):
        idx = [i for f in b['frases'] for i in fr[f] if norm(W[i][2]) == norm(n['palavra'])]
        i = idx[n.get('n', 1) - 1]
        a = W[i][0] + nd
        num.append({'de': round(a, 2), 'ate': round(a + n.get('dur', 1.3), 2), 'texto': n['texto'], **({'pos': n['pos']} if 'pos' in n else {})})
receita = {'brutos': PL['brutos'], 'saida': PL['saida'], 'tmp': out.replace(ROOT + os.sep, ''), 'narracao': PL['narracao'],
           'narr_delay': nd, 'trilha': PL['trilha'], 'ganho_trilha': PL.get('ganho_trilha', 0.09), 'ganho_jogo': PL.get('ganho_jogo', 0.5),
           'ass': os.path.join(out, 'legendas.ass').replace(ROOT + os.sep, ''), 'segs': segs}
json.dump(receita, open(os.path.join(out, 'receita.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
json.dump({'rotulos': rot, 'numeros': num, 'tags': tags}, open(os.path.join(out, 'extras.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
for s in segs:
    print(f"{s['take']:16s} {s['a']:7.2f}-{s['b']:7.2f} dur {s['dur']:5.2f} vel {(s['b'] - s['a']) / s['dur']:5.2f}")
print('total', round(sum(s['dur'] for s in segs), 2), 'rotulos', len(rot), 'numeros', len(num), 'tags', len(tags))
