"""Thumbnail 1280×720: fundo + 1 a 3 palavras grossas (branco, contorno escuro, falso 3D) + seta/círculo vermelho.

Uso:   python -X utf8 thumb.py fundo.jpg "MUNDO INFINITO" saida.jpg [--fonte F.ttf] [--lugar cima|centro|baixo]
                              [--seta x0,y0,x1,y1] [--circulo x,y,raio]
Teste: python -X utf8 thumb.py --teste [saida.jpg]
Fonte: padrão Arial Black (vem no Windows). Lilita One ou Luckiest Guy (Google Fonts, licença OFL) ficam melhores.
"""
import argparse, math, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

W, H = 1280, 720
FONTE = r'C:\Windows\Fonts\ariblk.ttf'
VERMELHO = (235, 25, 25)


def texto(img, frase, fonte, lugar):
    # 1 linha se couber grande; senão quebra em 2 linhas
    palavras = frase.split()
    linhas = [frase]
    tam = lambda ls: min(int(H * .26), *(int(W * .9 / ImageFont.truetype(fonte, 100).getlength(l) * 100) for l in ls))
    if len(palavras) > 1 and tam(linhas) < H * .2:
        meio = (len(palavras) + 1) // 2
        linhas = [' '.join(palavras[:meio]), ' '.join(palavras[meio:])]
    s = tam(linhas)
    f = ImageFont.truetype(fonte, s)
    borda, prof = max(6, s // 11), max(6, s // 9)
    alt = int(s * 1.05)
    y0 = {'cima': H * .06, 'centro': (H - alt * len(linhas)) / 2, 'baixo': H * .94 - alt * len(linhas)}[lugar]
    camada = Image.new('RGBA', (W, H))
    d = ImageDraw.Draw(camada)
    for n, l in enumerate(linhas):
        x, y = (W - f.getlength(l)) / 2, y0 + n * alt
        for k in range(prof, 0, -1):  # extrusão: cópias escuras andando na diagonal
            d.text((x + k, y + k), l, font=f, fill=(30, 30, 45), stroke_width=borda, stroke_fill=(30, 30, 45))
        d.text((x, y), l, font=f, fill='white', stroke_width=borda, stroke_fill=(12, 12, 12))
    sombra = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sombra.putalpha(camada.getchannel('A').point(lambda a: a * 160 // 255).filter(ImageFilter.GaussianBlur(14)))
    img.alpha_composite(sombra, (prof + 6, prof + 10))
    img.alpha_composite(camada)


def seta(img, x0, y0, x1, y1):
    d = ImageDraw.Draw(img)
    ang, L, lg = math.atan2(y1 - y0, x1 - x0), 95, 30
    bx, by = x1 - L * math.cos(ang), y1 - L * math.sin(ang)
    ponta = [(x1, y1), (bx + L * .65 * math.cos(ang + math.pi / 2), by + L * .65 * math.sin(ang + math.pi / 2)),
             (bx + L * .65 * math.cos(ang - math.pi / 2), by + L * .65 * math.sin(ang - math.pi / 2))]
    d.line([(x0, y0), (bx, by)], fill='white', width=lg + 14)
    d.polygon(ponta, fill='white', outline='white', width=14)
    d.line([(x0, y0), (bx, by)], fill=VERMELHO, width=lg)
    d.polygon(ponta, fill=VERMELHO)


def circulo(img, x, y, r):
    d = ImageDraw.Draw(img)
    d.ellipse([x - r, y - r, x + r, y + r], outline='white', width=24)
    d.ellipse([x - r + 4, y - r + 4, x + r - 4, y + r - 4], outline=VERMELHO, width=16)


def thumb(fundo, frase, saida, fonte=FONTE, lugar='cima', seta_=None, circulo_=None):
    img = ImageOps.fit(Image.open(fundo).convert('RGB'), (W, H), Image.LANCZOS)
    img = ImageEnhance.Contrast(ImageEnhance.Color(img).enhance(1.25)).enhance(1.1).convert('RGBA')
    if circulo_:
        circulo(img, *circulo_)
    if seta_:
        seta(img, *seta_)
    texto(img, frase, str(fonte), lugar)
    img.convert('RGB').save(saida, quality=92)
    return saida


def teste(saida=None):
    p = Path(tempfile.mkdtemp())
    fundo = Image.linear_gradient('L').resize((W, H)).convert('RGB')
    fundo = Image.merge('RGB', (fundo.getchannel(0).point(lambda v: v // 2), fundo.getchannel(0).point(lambda v: 60 + v // 3),
                                fundo.getchannel(0).point(lambda v: 40)))
    fundo.save(p / 'fundo.png')
    saida = Path(saida or p / 'thumb.jpg')
    thumb(p / 'fundo.png', 'MUNDO INFINITO', saida, seta_=(900, 600, 1080, 470), circulo_=(1080, 400, 90))
    im = Image.open(saida)
    assert im.size == (W, H)
    faixa = im.crop((0, 0, W, H // 2)).convert('L')
    brancos = sum(faixa.histogram()[245:])
    assert brancos > 10000, ('texto branco não apareceu', brancos)
    print('teste OK', saida)


if __name__ == '__main__':
    if sys.argv[1:2] == ['--teste']:
        teste(sys.argv[2] if len(sys.argv) > 2 else None); sys.exit()
    ap = argparse.ArgumentParser()
    ap.add_argument('fundo'); ap.add_argument('frase'); ap.add_argument('saida')
    ap.add_argument('--fonte', default=FONTE)
    ap.add_argument('--lugar', default='cima', choices=['cima', 'centro', 'baixo'])
    num = lambda s: [int(v) for v in s.split(',')]
    ap.add_argument('--seta', type=num)
    ap.add_argument('--circulo', type=num)
    a = ap.parse_args()
    print(thumb(a.fundo, a.frase, a.saida, a.fonte, a.lugar, a.seta, a.circulo))
