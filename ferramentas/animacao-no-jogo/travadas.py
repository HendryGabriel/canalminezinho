"""Mede travadas: quadros repetidos (diff ~0) no video. uso: travadas.py <video> [inicio] [dur]"""
import subprocess, sys, numpy as np
src = sys.argv[1]; ss = sys.argv[2] if len(sys.argv) > 2 else '0'; t = sys.argv[3] if len(sys.argv) > 3 else '999'
W, H = 108, 192
b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', ss, '-t', t, '-i', src, '-vf', f'scale={W}:{H},format=gray', '-f', 'rawvideo', '-'],
                   capture_output=True).stdout
f = np.frombuffer(b, np.uint8).reshape(-1, H, W).astype(np.float32)
# ignora a faixa da legenda (y 0.55-0.75) e o contador (topo)
m = f[:, int(H * 0.2):int(H * 0.5), :]
d = np.abs(np.diff(m, axis=0)).mean(axis=(1, 2))
fps = 30
rep = d < 0.15
print('quadros', len(f), 'repetidos', int(rep.sum()), f'({rep.mean():.1%})')
runs, i = [], 0
while i < len(rep):
    if rep[i]:
        j = i
        while j < len(rep) and rep[j]: j += 1
        if j - i >= 2: runs.append((round(float(ss) + (i + 1) / fps, 2), j - i))
        i = j
    else:
        i += 1
print('congelamentos >=2 quadros (t, n):', runs)
mov = d[~rep]
print('irregularidade do movimento (cv da diferenca entre quadros):', round(float(mov.std() / mov.mean()), 2))
