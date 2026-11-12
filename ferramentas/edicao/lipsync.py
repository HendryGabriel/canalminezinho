"""Lip sync simples: voz (wav) → estado da boca em cada quadro (0 fechada, 1 meio, 2 aberta).

Uso:   python -X utf8 lipsync.py voz.wav 30 [boca.json]
Saída: {"fps": 30, "estados": [0, 0, 1, 2, 2, 1, ...]}  (1 número por quadro do vídeo)
Teste: python -X utf8 lipsync.py --teste

Como funciona: volume (RMS) de cada quadro, comparado com o volume forte da voz (percentil 98).
Abre na hora que passa do limiar; só fecha quando cai bem abaixo dele (histerese), assim a boca não pisca.
"""
import json, math, subprocess, sys, tempfile, wave
from array import array
from pathlib import Path

SR = 16000


def estados(wav, fps=30, meio=.15, aberta=.45, histerese=.7):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(wav), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    a = array('h')
    a.frombytes(raw[:len(raw) // 2 * 2])
    passo = SR / fps
    rms = []
    for k in range(math.ceil(len(a) / passo)):
        w = a[round(k * passo):round((k + 1) * passo)]
        rms.append(math.sqrt(sum(x * x for x in w) / len(w)) if w else 0.0)
    ref = sorted(rms)[min(len(rms) - 1, int(len(rms) * .98))] or 1.0
    out, s = [], 0
    for r in rms:
        v = r / ref
        sobe = 2 if v >= aberta else 1 if v >= meio else 0
        if sobe > s:
            s = sobe
        elif s == 2 and v < aberta * histerese:
            s = 1 if v >= meio * histerese else 0
        elif s == 1 and v < meio * histerese:
            s = 0
        out.append(s)
    return out


def teste():
    # silêncio · tom forte · tom que oscila em volta do limiar (não pode piscar) · tom fraco · silêncio (0,5 s cada)
    trechos = [lambda k: 0, lambda k: .8, lambda k: .8 * (.40 if (k * 30 // SR) % 2 else .52), lambda k: .8 * .25, lambda k: 0]
    amostras = array('h')
    for i, amp in enumerate(trechos):
        for k in range(SR // 2):
            amostras.append(int(32767 * amp(k) * math.sin(2 * math.pi * 220 * k / SR)))
    arq = Path(tempfile.mkdtemp()) / 'tom.wav'
    with wave.open(str(arq), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(amostras.tobytes())
    e = estados(arq, 30)
    assert len(e) == 75, len(e)
    assert set(e[1:14]) == {0}, e[:15]
    assert set(e[16:29]) == {2}, e[15:30]
    assert set(e[31:44]) == {2}, ('histerese: oscilando perto do limiar a boca fica aberta', e[30:45])
    assert set(e[46:59]) == {1}, e[45:60]
    assert set(e[61:74]) == {0}, e[60:75]
    print('teste OK', ''.join(map(str, e)))


if __name__ == '__main__':
    if sys.argv[1:] == ['--teste']:
        teste(); sys.exit()
    fps = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    saida = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(sys.argv[1]).with_name('boca.json')
    saida.write_text(json.dumps({'fps': fps, 'estados': estados(sys.argv[1], fps)}), encoding='utf8')
    print('salvo em', saida)
