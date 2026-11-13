"""Alinha as palavras do roteiro (grafia certa) aos tempos do Whisper.
uso: alinhar.py <roteiro.txt> <whisper.json> <saida.json> [desloc]"""
import json, sys, re, difflib, unicodedata

txt = open(sys.argv[1], encoding='utf-8').read().split()
Wh = json.load(open(sys.argv[2], encoding='utf-8'))
off = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
n = lambda s: unicodedata.normalize('NFKD', re.sub(r'[^\w]', '', s.lower())).encode('ascii', 'ignore').decode()
A = [n(w) for w in txt]; B = [n(w[2]) for w in Wh]
sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
T = [None] * len(txt)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            T[i1 + k] = Wh[j1 + k][:2]
    elif tag == 'replace' and j2 > j1:
        a0, b1 = Wh[j1][0], Wh[j2 - 1][1]; m = i2 - i1
        for k in range(m):
            T[i1 + k] = [a0 + (b1 - a0) * k / m, a0 + (b1 - a0) * (k + 1) / m]
# preenche faltantes por interpolacao
for i in range(len(T)):
    if T[i] is None:
        p = next((T[j][1] for j in range(i - 1, -1, -1) if T[j]), 0)
        q = next((T[j][0] for j in range(i + 1, len(T)) if T[j]), p + 0.3)
        T[i] = [p, max(p + 0.05, (p + q) / 2)]
out = [[round(t[0] + off, 3), round(t[1] + off, 3), w] for t, w in zip(T, txt)]
json.dump(out, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False)
print(sys.argv[3], len(out), 'similaridade', round(sm.ratio(), 3))
