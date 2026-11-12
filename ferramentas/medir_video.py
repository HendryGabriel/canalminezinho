"""Mede um vídeo de referência: cortes (troca de cena), ritmo por minuto e volume (LUFS).
Uso: python medir_video.py video.mp4 [limiar=0.3]  -> imprime resumo e salva <video>_cortes.txt"""
import re, subprocess, sys, statistics as st
v = sys.argv[1]; lim = sys.argv[2] if len(sys.argv) > 2 else '0.3'
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', v, '-vf', f"select='gt(scene,{lim})',showinfo", '-an', '-f', 'null', '-'],
                   capture_output=True, text=True, errors='replace').stderr
cuts = [float(x) for x in re.findall(r'pts_time:([\d.]+)', r)]
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', v], capture_output=True, text=True).stdout)
open(v.rsplit('.', 1)[0] + '_cortes.txt', 'w').write('\n'.join(f'{c:.2f}' for c in cuts))
gaps = [b - a for a, b in zip([0] + cuts, cuts + [dur])]
print(f'{v}: {dur/60:.1f} min, {len(cuts)} cortes, plano médio {dur/(len(cuts)+1):.1f} s, mediana {st.median(gaps):.1f} s')
por_min = [sum(1 for c in cuts if m*60 <= c < (m+1)*60) for m in range(int(dur//60)+1)]
print('cortes por minuto:', por_min)
a = subprocess.run(['ffmpeg', '-hide_banner', '-i', v, '-af', 'ebur128', '-vn', '-f', 'null', '-'],
                   capture_output=True, text=True, errors='replace').stderr
print('volume:', ' '.join(re.findall(r'(I:\s+[-\d.]+ LUFS|LRA:\s+[\d.]+ LU)', a)[-2:]))
