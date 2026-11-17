import os as _os
PROJ = _os.environ.get('ANIM_PROJETO', _os.getcwd())
"""Linhas de velocidade v5 (finas, rapidas, com rastro e fade): sobe (queda vista de lado) e radial (olhando pra baixo).
uso: linhas_v5.py"""
import math, random, subprocess
from PIL import Image, ImageDraw, ImageFilter

W, H, FPS, DUR = 1080, 1920, 30, 4.0


def gerar(tipo, out, seed):
    random.seed(seed)
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'qtrle', '-pix_fmt', 'argb', out], stdin=subprocess.PIPE)
    L = []
    for f in range(int(DUR * FPS)):
        for _ in range(random.choice([1, 1, 2, 2, 3])):
            if tipo == 'sobe':
                x = random.choice([random.uniform(0, W * 0.3), random.uniform(W * 0.7, W), random.uniform(0, W)])
                L.append({'x': x, 'y': H + random.uniform(0, 300), 'v': random.uniform(220, 380), 'l': random.uniform(160, 420),
                          'a': random.uniform(70, 150), 'vida': 0})
            else:
                L.append({'ang': random.uniform(0, 2 * math.pi), 'r': random.uniform(260, 520), 'v': random.uniform(40, 70),
                          'l': random.uniform(120, 300), 'a': random.uniform(70, 150), 'vida': 0})
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
        viva = []
        for s in L:
            s['vida'] += 1
            fade = min(1, s['vida'] / 2)
            if tipo == 'sobe':
                s['y'] -= s['v']
                if s['y'] + s['l'] < 0: continue
                # rastro: varios segmentos com alfa decrescente
                for k in range(4):
                    a = int(s['a'] * fade * (1 - k * 0.25))
                    y0 = s['y'] + k * s['l'] / 4
                    dr.line([(s['x'], y0), (s['x'], y0 + s['l'] / 4)], fill=(255, 255, 255, a), width=2)
            else:
                s['r'] += s['v']; s['v'] *= 1.12
                if s['r'] > 1500: continue
                cx, cy = W / 2, H * 0.45
                for k in range(4):
                    a = int(s['a'] * fade * (0.25 + k * 0.25))
                    r0 = s['r'] + k * s['l'] / 4
                    p0 = (cx + r0 * math.cos(s['ang']), cy + r0 * math.sin(s['ang']))
                    r1 = r0 + s['l'] / 4
                    p1 = (cx + r1 * math.cos(s['ang']), cy + r1 * math.sin(s['ang']))
                    dr.line([p0, p1], fill=(255, 255, 255, a), width=2 + k // 2)
            viva.append(s)
        L = viva
        ff.stdin.write(im.filter(ImageFilter.GaussianBlur(0.8)).tobytes())
    ff.stdin.close(); ff.wait()


if __name__ == '__main__':
    gerar('sobe', _os.path.join(PROJ, 'overlays', 'sobe_v5.mov'), 5)
    gerar('radial', _os.path.join(PROJ, 'overlays', 'radial_v5.mov'), 6)
    print('ok')
