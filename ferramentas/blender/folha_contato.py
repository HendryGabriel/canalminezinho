"""Folha de contato: 1 linha por plano, 6 quadros espalhados. Roda FORA do Blender (Pillow).

    python folha_contato.py "C:/.../canalminezinho-testes/blender"
Gera folha_contato.png dentro da pasta.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

pasta = Path(sys.argv[1])
por_linha = int(sys.argv[2]) if len(sys.argv) > 2 else 6
planos = sorted(p for p in pasta.iterdir() if p.is_dir() and list(p.glob("*.png")))
linhas = []
for p in planos:
    quadros = sorted(p.glob("*.png"))
    passo = max(1, (len(quadros) - 1) / max(1, por_linha - 1))
    escolha = sorted({quadros[round(i * passo)] for i in range(por_linha) if round(i * passo) < len(quadros)})
    linhas.append((p.name, escolha))

w, h = Image.open(linhas[0][1][0]).size
folha = Image.new("RGB", (w * por_linha, (h + 18) * len(linhas)), "white")
d = ImageDraw.Draw(folha)
for y, (nome, quadros) in enumerate(linhas):
    for x, q in enumerate(quadros):
        folha.paste(Image.open(q).convert("RGB"), (x * w, y * (h + 18) + 18))
        d.text((x * w + 4, y * (h + 18) + 3), f"{nome}  q{q.stem}", fill="black")
folha.save(pasta / "folha_contato.png")
print(pasta / "folha_contato.png")
