"""Teste completo da edição com material falso (ffmpeg lavfi): roteiro com pausa de cena, 5 planos, música,
2 sfx, 2 textos, todos os efeitos, versão Short 9:16 60 fps, lip sync e thumbnail.

Uso: python -X utf8 teste.py [pasta]
Padrão da pasta: ESTUDOS/canalminezinho-testes/edicao (fora do repositório, que é público).
No fim: quadros/folha.png (antes × durante de cada efeito) para olhar e thumb.jpg.
"""
import json, re, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path[:0] = [str(AQUI), str(AQUI.parent)]
import montar, efeitos, lipsync, thumb
from alinhar_voz import ler_roteiro

PASTA = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI.parents[2] / 'canalminezinho-testes' / 'edicao'
FALAS = {'F001': (0.3, 2.0), 'F002': (2.6, 4.6), 'F003': (5.2, 7.0), 'F004': (9.0, 11.0)}  # tempos da voz falsa
ROTEIRO = """F001 [curioso] Quanto vale um mundo?
     [pausa 0,5 s]
F002 [leve] Imagina achar um diamante.
     [pausa 0,5 s]
F003 [épico] Ele vale mais que a Terra.
     [pausa de cena 6 s]
F004 [espanto] Isso é gigante.
"""


def ff(*a):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', *map(str, a)], check=True)


def criar_material(p):
    (p / 'seq').mkdir(parents=True, exist_ok=True)
    fala = '+'.join(f'between(t,{a},{b})' for a, b in FALAS.values())
    ff('-f', 'lavfi', '-i', f"aevalsrc='0.4*(sin(2*PI*180*t)+0.5*sin(2*PI*360*t)+0.25*sin(2*PI*540*t))"
                            f"*(0.6+0.4*sin(2*PI*4*t))*({fala})':s=48000:d=12", p / 'voz.wav')
    ff('-f', 'lavfi', '-i', "aevalsrc='0.2*sin(2*PI*220*t)+0.15*sin(2*PI*277*t)+0.12*sin(2*PI*330*t)':s=48000:d=10",
       p / 'musica.wav')  # 10 s: menor que o vídeo, testa a repetição
    ff('-f', 'lavfi', '-i', "aevalsrc='0.9*sin(2*PI*55*t)*exp(-4*t)':s=48000:d=0.8", p / 'boom.wav')
    ff('-f', 'lavfi', '-i', 'anoisesrc=d=0.08:a=0.5', p / 'pop.wav')
    ff('-f', 'lavfi', '-i', 'testsrc2=s=1280x720:r=30:d=8', '-pix_fmt', 'yuv420p', p / 'cena1.mp4')
    ff('-f', 'lavfi', '-i', 'testsrc2=s=1920x1080:r=60:d=4', '-pix_fmt', 'yuv420p', p / 'cena2.mp4')
    ff('-f', 'lavfi', '-i', 'smptebars=s=1280x720:r=30:d=3', '-pix_fmt', 'yuv420p', p / 'cena3.mp4')
    ff('-f', 'lavfi', '-i', 'mandelbrot=s=1600x900', '-frames:v', 1, p / 'foto.png')
    ff('-f', 'lavfi', '-i', 'life=s=640x360:mold=10:r=10:ratio=0.1:life_color=#00ff00', '-frames:v', 20, p / 'seq' / '%03d.png')
    # roteiro → tempos.json (o mesmo leitor do alinhar_voz.py; os tempos são os da voz falsa)
    (p / 'roteiro.md').write_text(ROTEIRO, encoding='utf8')
    falas = ler_roteiro(ROTEIRO)
    for i, f in enumerate(falas):
        f['inicio'], f['fim'] = FALAS[f['id']]
        f['conferir'] = False
        prox = FALAS[falas[i + 1]['id']][0] if i + 1 < len(falas) else f['fim']
        f['pausa_real'] = round(prox - f['fim'], 2)
    (p / 'tempos.json').write_text(json.dumps(falas, ensure_ascii=False, indent=1), encoding='utf8')


MONTAGEM = {
    'voz': 'voz.wav', 'tempos': 'tempos.json', 'saida': 'final.mp4', 'formato': '16:9', 'fps': 30,
    'planos': [
        {'arquivo': 'cena1.mp4', 'quando': 0, 'in': 1.0},
        {'arquivo': 'foto.png', 'quando': 'F002', 'zoom': 'in'},
        {'arquivo': 'seq/%03d.png', 'quando': 'F003', 'fps': 10, 'zoom': [1.0, 1.2]},
        {'arquivo': 'cena2.mp4', 'quando': 'F003:fim'},  # pausa de cena: 6 s, o clipe tem 4 s (segura o fim)
        {'arquivo': 'cena3.mp4', 'quando': 'F004', 'zoom': 'out'}],
    'musicas': [{'arquivo': 'musica.wav', 'inicio': 0, 'volume': -6, 'fade': 1}],
    'sfx': [{'arquivo': 'boom.wav', 'tempo': 'F003:fim'}, {'arquivo': 'pop.wav', 'tempo': 'F003+0.2', 'volume': -6}],
    'textos': [{'texto': 'R$ ???', 'tempo': 'F003+0.2', 'duracao': 1.5, 'estilo': 'pop'},
               {'texto': 'GIGANTE', 'tempo': 'F004', 'duracao': 2.0, 'estilo': 'digitando', 'posicao': 'baixo'}],
    'efeitos': [{'tipo': 'impacto', 'tempo': 'F001+1'}, {'tipo': 'flash', 'tempo': 2.2},
                {'tipo': 'tingido', 'tempo': 'F002+1'}, {'tipo': 'tremida', 'tempo': 4.2, 'duracao': .4},
                {'tipo': 'aberracao', 'tempo': 2.9, 'forca': 2}, {'tipo': 'linhas', 'tempo': 'F003+1'},
                {'tipo': 'smash_zoom', 'tempo': 'F003:fim'}, {'tipo': 'eco', 'tempo': 9.0},
                {'tipo': 'linhas', 'tempo': 'F004+1', 'modo': 'paralelo'}],
}
SHORT = {'voz': 'voz.wav', 'tempos': 'tempos.json', 'saida': 'final_short.mp4', 'formato': '9:16', 'fps': 60,
         'pasta_temp': '_montagem_short', 'fim': 'F002:fim+0.5',
         'planos': [{'arquivo': 'cena1.mp4', 'quando': 0}, {'arquivo': 'foto.png', 'quando': 'F002', 'zoom': 'in'}],
         'musicas': [{'arquivo': 'musica.wav', 'volume': -8}],
         'textos': [{'texto': 'R$ ???', 'tempo': 'F002', 'estilo': 'pop'}],
         'efeitos': [{'tipo': 'flash', 'tempo': 'F002'}]}


def info(arq):
    s = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height,r_frame_rate:format=duration',
                                   '-of', 'json', str(arq)], capture_output=True, text=True, check=True).stdout)
    v = next(x for x in s['streams'] if x['codec_type'] == 'video')
    n, d = map(int, v['r_frame_rate'].split('/'))
    return float(s['format']['duration']), v['width'], v['height'], n / d


def volume(arq):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(arq), '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    resumo = r[r.rindex('Summary:'):]
    return float(re.search(r'I:\s+(-?[\d.]+) LUFS', resumo)[1]), float(re.search(r'Peak:\s+(-?[\d.]+) dBFS', resumo)[1])


def mudou(final, base, t):
    """Fração dos pixels que o efeito mudou: quadro do final.mp4 × mesmo quadro do base.mp4 (sem efeitos).
    Só o terço de cima da tela, onde não há texto no teste (senão o texto contaria como efeito)."""
    from PIL import Image, ImageChops
    q = lambda v: Image.frombytes('RGB', (1920, 1080), subprocess.run(
        ['ffmpeg', '-v', 'error', '-ss', f'{t:.4f}', '-i', str(v), '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
        capture_output=True, check=True).stdout)
    h = ImageChops.difference(q(final), q(base)).crop((0, 0, 1920, 360)).convert('L').histogram()
    return sum(h[40:]) / (1920 * 360)


def folha(final, fps, efs, T, p):
    """Para cada efeito: quadro 0,25 s antes × quadro durante. Salva quadros/folha.png.
    Confere também que cada efeito mudou pelo menos 0,5% do terço de cima (sem efeito: ~0%)."""
    from PIL import Image, ImageDraw, ImageFont
    q = p / 'quadros'
    q.mkdir(exist_ok=True)
    f = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', 22)
    ruido = mudou(final, p / '_montagem' / 'base.mp4', 0.5)  # sem efeito nem texto: só a recodificação
    assert ruido < .001, ('sem efeito o quadro devia ficar igual', ruido)
    pares = []
    for i, e in enumerate(efs):
        a, b = efeitos.janela({**e, 'tempo': T(e['tempo'])}, fps)
        t = a + .25 / fps if b - a < 3.5 / fps else a + .7 * (b - a)  # efeito de 2 quadros: o 1º; longo: perto do pico
        nome = f"{i}_{e['tipo']}"
        ff('-ss', f'{t:.4f}', '-i', final, '-frames:v', 1, q / f'{nome}.png')
        ff('-ss', f'{max(a - .25, 0):.4f}', '-i', final, '-frames:v', 1, q / f'{nome}_antes.png')
        m = mudou(final, p / '_montagem' / 'base.mp4', t)
        print(f'  {nome:14s} @ {t:5.2f} s  mudou {m:6.1%} da tela')
        assert m > .005, (nome, m)
        pares.append((nome, t))
    lado = Image.new('RGB', (2 * 640, len(pares) * 360), 'black')
    for k, (nome, t) in enumerate(pares):
        for j, suf in enumerate(('_antes', '')):
            lado.paste(Image.open(q / f'{nome}{suf}.png').resize((640, 360)), (j * 640, k * 360))
        ImageDraw.Draw(lado).text((650, k * 360 + 8), f'{nome} @ {t:.2f}s', font=f, fill='yellow', stroke_width=3, stroke_fill='black')
    lado.save(q / 'folha.png')
    return q / 'folha.png'


def main():
    p = PASTA
    p.mkdir(parents=True, exist_ok=True)
    montar.teste(); efeitos.teste(); lipsync.teste()
    criar_material(p)
    (p / 'montagem.json').write_text(json.dumps(MONTAGEM, ensure_ascii=False, indent=1), encoding='utf8')
    (p / 'montagem_short.json').write_text(json.dumps(SHORT, ensure_ascii=False, indent=1), encoding='utf8')

    final, total = montar.montar(p / 'montagem.json')
    dur, w, h, fps = info(final)
    esperado = 12 + (6 - 2)  # voz de 12 s + 4 s de silêncio na pausa de cena da F003 (6 s no roteiro, 2 s reais)
    assert abs(total - esperado) < .01 and abs(dur - esperado) < .05, (total, dur)
    assert (w, h, round(fps)) == (1920, 1080, 30)
    lufs, pico = volume(final)
    assert abs(lufs + 14) < .5 and pico <= -1.0, (lufs, pico)

    falas = {f['id']: f for f in json.loads((p / 'tempos.json').read_text(encoding='utf8'))}
    T = lambda x: montar.tempo(x, falas, montar.esticos(list(falas.values())))
    assert T('F004') == 13.0, T('F004')  # a frase depois da pausa de cena andou 4 s
    amostra = lambda e: efeitos.amostra(final, efeitos.janela({**e, 'tempo': T(e['tempo'])}, 30)[0] + .01)
    ef = {e['tipo']: e for e in MONTAGEM['efeitos']}
    r, g, b = amostra(ef['flash']); assert min(r, g, b) > 235, ('flash', r, g, b)
    r, g, b = amostra(ef['impacto']); assert max(r, g, b) - min(r, g, b) < 8, ('impacto', r, g, b)
    r, g, b = amostra(ef['tingido']); assert r > 2 * g and r > 2 * b, ('tingido', r, g, b)
    sheet = folha(final, 30, MONTAGEM['efeitos'], T, p)

    short, _ = montar.montar(p / 'montagem_short.json')
    sd, sw, sh, sf = info(short)
    assert (sw, sh, round(sf)) == (1080, 1920, 60) and abs(sd - 5.1) < .05, (sd, sw, sh, sf)
    slufs, spico = volume(short)

    boca = lipsync.estados(p / 'voz.wav', 30)
    ff('-ss', 7.6, '-i', final, '-frames:v', 1, p / 'fundo_thumb.png')
    thumb.thumb(p / 'fundo_thumb.png', 'MUNDO INFINITO', p / 'thumb.jpg', lugar='baixo',
                seta_=(240, 120, 420, 260), circulo_=(560, 300, 110))
    print(f'\nTUDO OK\n final.mp4: {dur:.3f} s (esperado {esperado}), {w}x{h} {fps:g} fps, {lufs} LUFS, pico {pico} dBTP'
          f'\n final_short.mp4: {sd:.3f} s, {sw}x{sh} {sf:g} fps, {slufs} LUFS, pico {spico} dBTP'
          f'\n boca: {len(boca)} quadros, {sum(1 for x in boca if x)} com boca aberta/meio'
          f'\n olhar: {sheet}  e  {p / "thumb.jpg"}')


if __name__ == '__main__':
    main()
