"""Folha de contato de varios takes: 1 quadro a cada N s. uso: folha.py <saida.jpg> <cada> <base1> [base2...]"""
import sys, subprocess, os
from PIL import Image, ImageDraw

out, cada, bases = sys.argv[1], float(sys.argv[2]), sys.argv[3:]
W, Hh = 162, 288
tiles = []
for base in bases:
    mkv = base + '.mkv'
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mkv], capture_output=True, text=True).stdout or 0)
    n = os.path.basename(base)
    tmp = base + '_f%03d.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mkv, '-vf', f'setpts=PTS-STARTPTS,fps=1/{cada},scale={W}:{Hh}', tmp])
    k = 1
    while os.path.exists(base + f'_f{k:03d}.png'):
        p = base + f'_f{k:03d}.png'
        im = Image.open(p).convert('RGB'); d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W, 14], fill=(0, 0, 0)); d.text((2, 1), f'{n[:16]} {(k - 1) * cada:.0f}s', fill=(255, 255, 0))
        tiles.append(im); os.remove(p); k += 1
cols = min(10, len(tiles)); rows = (len(tiles) + cols - 1) // cols
S = Image.new('RGB', (cols * W, rows * Hh))
for i, im in enumerate(tiles):
    S.paste(im, ((i % cols) * W, (i // cols) * Hh))
S.save(out, quality=82)
print(out, len(tiles))
