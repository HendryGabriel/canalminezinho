"""Mede a regularidade do deslocamento da imagem por quadro (correlacao de fase).
uso: passo_img.py <video> [inicio] [dur]  -> desvio relativo do deslocamento (0 = perfeitamente constante)"""
import subprocess, sys, numpy as np
src = sys.argv[1]; ss = sys.argv[2] if len(sys.argv) > 2 else '0'; t = sys.argv[3] if len(sys.argv) > 3 else '999'
W, H = 270, 480
b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', ss, '-t', t, '-i', src, '-vf', f'scale={W}:{H},format=gray', '-f', 'rawvideo', '-'],
                   capture_output=True).stdout
f = np.frombuffer(b, np.uint8).reshape(-1, H, W).astype(np.float32)
f = f[:, int(H * 0.25):int(H * 0.5), :]          # faixa sem legenda/contador
win = np.outer(np.hanning(f.shape[1]), np.hanning(f.shape[2]))
sh = []
for a, c in zip(f, f[1:]):
    A = np.fft.fft2(a * win); Cc = np.fft.fft2(c * win)
    R = A * np.conj(Cc); R /= np.abs(R) + 1e-9
    r = np.fft.ifft2(R).real
    y, x = np.unravel_index(np.argmax(r), r.shape)
    if y > r.shape[0] // 2: y -= r.shape[0]
    if x > r.shape[1] // 2: x -= r.shape[1]
    sh.append(np.hypot(x, y))
sh = np.array(sh)
print('desloc px/quadro: media %.2f  desvio %.2f  zeros %d/%d' % (sh.mean(), sh.std(), int((sh < 0.5).sum()), len(sh)))
print(' '.join(f'{v:.0f}' for v in sh[:60]))
