"""Ajusta os tempos das palavras (Whisper) pela forma de onda: o Whisper marca a palavra que vem depois
de uma pausa antes de a fala voltar (0,1-0,3 s cedo). Aqui cada palavra que comeca dentro de um silencio
passa a comecar no fim dele, e a palavra anterior termina no comeco do silencio.
uso: ajustar_tempos.py <narracao.wav> <palavras.json> <saida.json> [limiar_dB=-32] [min_silencio=0.08]"""
import json, re, subprocess, sys

wav, pin, pout = sys.argv[1:4]
th = sys.argv[4] if len(sys.argv) > 4 else '-32'
md = sys.argv[5] if len(sys.argv) > 5 else '0.08'
log = subprocess.run(['ffmpeg', '-v', 'info', '-i', wav, '-af', f'silencedetect=n={th}dB:d={md}', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
ini = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]
fim = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
S = list(zip(ini, fim))

W = json.load(open(pin, encoding='utf-8'))
mov = 0
for a, b in S:
    # primeira palavra cujo inicio cai dentro do silencio (ou ate 0,25 s antes do fim dele)
    for i, w in enumerate(W):
        if a - 0.05 <= w[0] < b - 0.04:
            nova = round(b, 3)
            if nova > w[0]:
                W[i][0] = nova; W[i][1] = max(W[i][1], nova + 0.08); mov += 1
                if i > 0 and W[i - 1][1] > a:
                    W[i - 1][1] = round(max(W[i - 1][0] + 0.06, a), 3)
            break
# mantem a ordem (nenhuma palavra antes da anterior)
for i in range(1, len(W)):
    if W[i][0] < W[i - 1][0] + 0.04:
        W[i][0] = round(W[i - 1][0] + 0.04, 3); W[i][1] = max(W[i][1], W[i][0] + 0.06)
json.dump(W, open(pout, 'w', encoding='utf-8'), ensure_ascii=False)
print(pout, 'silencios', len(S), 'palavras movidas', mov)
