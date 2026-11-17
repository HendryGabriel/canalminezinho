import json, sys, collections
from PIL import Image, ImageDraw
src, out, x0, z0 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
d = json.load(open(src)); H = d['H']; T = d['TOP']
xs = [int(k.split(',')[0]) for k in H]; zs = [int(k.split(',')[1]) for k in H]
W, Hh = max(xs) - x0 + 1, max(zs) - z0 + 1
im = Image.new('RGB', (W, Hh))
col = {'water': (40, 80, 200), 'grass_block': (80, 150, 60), 'dirt': (120, 90, 60), 'podzol': (110, 80, 40), 'snow_block': (240, 240, 250),
       'stone': (130, 130, 130), 'coarse_dirt': (110, 85, 60), 'gravel': (140, 140, 140), 'sand': (220, 210, 150), 'ice': (160, 200, 255), 'dirt_path': (170, 150, 90), 'powder_snow': (230, 230, 255)}
for k, (y, b) in H.items():
    x, z = map(int, k.split(','))
    c = col.get(b, (200, 0, 200)); t = T.get(k)
    if t and t[1] in ('snow',) : c = (235, 235, 245)
    if t and ('leaves' in t[1]): c = tuple(int(v * 0.55) for v in c)
    f = 0.6 + 0.4 * (y - 60) / 40
    im.putpixel((x - x0, z - z0), tuple(max(0, min(255, int(v * f))) for v in c))
im = im.resize((W * 4, Hh * 4), Image.NEAREST); dr = ImageDraw.Draw(im)
for i in range(0, W, 16): dr.text((i * 4, 0), str(x0 + i), fill='white')
for i in range(0, Hh, 16): dr.text((0, i * 4), str(z0 + i), fill='white')
im.save(out)
print(collections.Counter(b for y, b in H.values()).most_common(8))
print(collections.Counter(t[1] for t in T.values()).most_common(8))
