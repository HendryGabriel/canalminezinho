"""Acha o início e o fim de cada frase do roteiro (F001, F002...) dentro da gravação da voz.

Uso:   python -X utf8 alinhar_voz.py videos/NN_tema/roteiro.md videos/NN_tema/voz.wav
Saída: videos/NN_tema/tempos.json  +  tabela na tela
Teste: python -X utf8 alinhar_voz.py --teste

Como funciona: o Whisper (local) transcreve a voz com o tempo de cada palavra;
o difflib casa as palavras do roteiro com as palavras ouvidas, então erro de transcrição
ou palavra trocada não estraga o resto. Frase sem nenhuma palavra casada fica entre as vizinhas
e sai marcada com "conferir": true.
"""
import difflib, json, re, sys, unicodedata
from pathlib import Path

LINHA_F = re.compile(r'^\s*(F\d+)\s*(?:\[([^\]]*)\])?\s*(.+)$')
PAUSA = re.compile(r'\[pausa( de cena)?\s*([\d,\.]+)(?:\s*[–-]\s*([\d,\.]+))?\s*s\]', re.I)


def norm(p):
    p = unicodedata.normalize('NFD', p.lower())
    return ''.join(c for c in p if c.isalnum() and not unicodedata.combining(c))


def ler_roteiro(texto):
    falas = []
    for linha in texto.splitlines():
        m = LINHA_F.match(linha)
        if m:
            fala = PAUSA.sub('', m[3]).strip()
            falas.append({'id': m[1], 'tom': (m[2] or '').strip(), 'texto': fala,
                          'pausa_roteiro': 0.0, 'pausa_de_cena': False})
        elif falas and (p := PAUSA.search(linha)):
            falas[-1]['pausa_roteiro'] = float((p[3] or p[2]).replace(',', '.'))
            falas[-1]['pausa_de_cena'] = bool(p[1])
    return falas


def alinhar(falas, palavras):
    """palavras = [(texto, inicio, fim), ...] na ordem da voz. Preenche inicio/fim em cada fala."""
    rot, dono = [], []
    for i, f in enumerate(falas):
        for w in f['texto'].split():
            if norm(w):
                rot.append(norm(w)); dono.append(i)
    ouv = [norm(w) for w, _, _ in palavras]
    casa = {}
    for a, b, n in difflib.SequenceMatcher(None, rot, ouv, autojunk=False).get_matching_blocks():
        for k in range(n):
            casa[a + k] = b + k
    for i, f in enumerate(falas):
        idx = [casa[j] for j in range(len(rot)) if dono[j] == i and j in casa]
        f['conferir'] = not idx
        if idx:
            f['inicio'], f['fim'] = palavras[min(idx)][1], palavras[max(idx)][2]
    # frases sem casamento: ficam no buraco entre as vizinhas
    for i, f in enumerate(falas):
        if f['conferir']:
            ant = next((g['fim'] for g in reversed(falas[:i]) if not g['conferir']), 0.0)
            prox = next((g['inicio'] for g in falas[i + 1:] if not g['conferir']), palavras[-1][2] if palavras else ant)
            f['inicio'], f['fim'] = ant, max(ant, prox)
    for i, f in enumerate(falas):
        prox = falas[i + 1]['inicio'] if i + 1 < len(falas) else f['fim']
        f['pausa_real'] = round(max(0.0, prox - f['fim']), 2)
        f['inicio'], f['fim'] = round(f['inicio'], 2), round(f['fim'], 2)
    return falas


def transcrever(audio):
    from faster_whisper import WhisperModel
    m = WhisperModel('small', device='cpu', compute_type='int8')
    segs, _ = m.transcribe(str(audio), language='pt', word_timestamps=True, vad_filter=False)
    return [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]


def teste():
    rot = """F001 [curioso] Quanto vale o seu mundo?
    [pausa 1 s]
F002 [leve] Imagina que você acha um diamante.
F003 [épico] Ele vale mais que a Terra.
    [pausa de cena 15 s]"""
    falas = ler_roteiro(rot)
    assert [f['id'] for f in falas] == ['F001', 'F002', 'F003']
    assert falas[0]['pausa_roteiro'] == 1.0 and falas[2]['pausa_de_cena'] and falas[2]['pausa_roteiro'] == 15.0
    # voz com 1 palavra errada ("mundos") e 1 frase toda errada (F002 virou ruído)
    ouv = [('Quanto', 0.0, .3), ('vale', .3, .6), ('o', .6, .7), ('seu', .7, .9), ('mundos?', .9, 1.4),
           ('blá', 2.5, 2.8), ('blé', 2.8, 3.4),
           ('Ele', 4.0, 4.2), ('vale', 4.2, 4.5), ('mais', 4.5, 4.7), ('que', 4.7, 4.8), ('a', 4.8, 4.9), ('Terra.', 4.9, 5.5)]
    a = alinhar(falas, ouv)
    assert (a[0]['inicio'], a[0]['fim']) == (0.0, 0.9), a[0]
    assert a[1]['conferir'] and a[1]['inicio'] == 0.9 and a[1]['fim'] == 4.0, a[1]
    assert (a[2]['inicio'], a[2]['fim']) == (4.0, 5.5) and not a[2]['conferir']
    print('teste OK')


if __name__ == '__main__':
    if sys.argv[1:] == ['--teste']:
        teste(); sys.exit()
    roteiro, audio = Path(sys.argv[1]), Path(sys.argv[2])
    palavras = transcrever(audio)
    # tempo de cada palavra: serve para a legenda palavra por palavra dos Shorts (guia 07 §0)
    roteiro.with_name('palavras.json').write_text(json.dumps(
        [{'p': w, 'inicio': round(a, 2), 'fim': round(b, 2)} for w, a, b in palavras], ensure_ascii=False), encoding='utf8')
    falas = alinhar(ler_roteiro(roteiro.read_text(encoding='utf8')), palavras)
    saida = roteiro.with_name('tempos.json')
    saida.write_text(json.dumps(falas, ensure_ascii=False, indent=1), encoding='utf8')
    for f in falas:
        aviso = '  <- CONFERIR' if f['conferir'] else ''
        print(f"{f['id']}  {f['inicio']:7.2f}-{f['fim']:7.2f}  pausa {f['pausa_real']:5.2f}s (roteiro {f['pausa_roteiro']}){aviso}")
    print('salvo em', saida)
