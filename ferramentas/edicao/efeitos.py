"""Efeitos de pós do reel de luta (guia 14 §2), feitos só com ffmpeg.

Uso sozinho:  python -X utf8 efeitos.py entrada.mp4 saida.mp4 impacto@1.0 flash@2.5 tremida@3:0.4 linhas@4:0.5:paralelo
              (cada efeito = tipo@tempo[:duração[:opção]]; segundos. Opção: cor do tingido, modo das linhas, força)
Teste:        python -X utf8 efeitos.py --teste
No montar.py: grafo() devolve o pedaço de filtergraph que entra na passada final.

Tipos: impacto (negativo preto e branco) · flash (branco + some) · tingido (tela de 1 cor) · tremida (chacoalha)
       aberracao (borda vermelha/azul) · linhas (linhas de velocidade radial/paralelo) · smash_zoom (zoom brusco)
       eco (rastro/fantasma)
"""
import json, math, random, subprocess, sys, tempfile
from pathlib import Path

# duração padrão: número inteiro = quadros, número com ponto = segundos
PADRAO = {'impacto': 2, 'flash': 2, 'tingido': 2, 'tremida': .3, 'aberracao': .3,
          'linhas': .5, 'smash_zoom': .5, 'eco': .6}


def janela(e, fps):
    """(início, fim) do efeito em segundos, presos na grade de quadros."""
    p = PADRAO[e['tipo']]
    d = float(e['duracao']) if e.get('duracao') else (p / fps if isinstance(p, int) else p)
    a = round(float(e['tempo']) * fps) / fps
    return a, a + max(d, 1 / fps)


def cor(c):
    c = c.lstrip('#')
    return [int(c[k:k + 2], 16) / 255 for k in (0, 2, 4)]


def desenhar_linhas(png, W, H, modo, seed):
    """PNG transparente com linhas de velocidade, um pouco maior que a tela (sobra para tremer)."""
    from PIL import Image, ImageDraw
    r = random.Random(seed)
    m = W // 40
    im = Image.new('RGBA', (W + 2 * m, H + 2 * m))
    d = ImageDraw.Draw(im)
    cx, cy = im.width / 2, im.height / 2
    diag = math.hypot(cx, cy)
    for _ in range(90 if modo == 'radial' else 60):
        a = r.uniform(0, 255)
        if modo == 'radial':  # cunhas finas saindo do centro para fora
            ang, larg = r.uniform(0, 2 * math.pi), r.uniform(.004, .014)
            r0 = diag * r.uniform(.35, .6)
            pts = [(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)),
                   (cx + diag * math.cos(ang - larg), cy + diag * math.sin(ang - larg)),
                   (cx + diag * math.cos(ang + larg), cy + diag * math.sin(ang + larg))]
            d.polygon(pts, fill=(255, 255, 255, int(a)))
        else:  # riscos horizontais, mais longos nas bordas de cima e de baixo
            y = r.uniform(0, im.height)
            x0 = r.uniform(-W * .2, W * .8)
            d.line([(x0, y), (x0 + r.uniform(W * .2, W * .6), y)], fill=(255, 255, 255, int(a)), width=r.randint(2, 6))
    im.save(png)


def grafo(efeitos, W, H, fps, pasta, video, src='[0:v]', n_in=1):
    """efeitos = [{tipo, tempo (s), duracao?, cor?, modo?, forca?}].
    video = arquivo de onde sai o trecho do smash_zoom e do eco (o mesmo que entra em src).
    Devolve (args extras de entrada, partes do filtergraph, rótulo de saída, próximo índice de entrada)."""
    args, g, cur, trem = [], [], src, []
    h = .5 / fps  # meia janela de quadro: pega exatamente os quadros pedidos
    for i, e in enumerate(efeitos):
        a, b = janela(e, fps)
        en = f"enable='gte(t,{a - h:.4f})*lt(t,{b - h:.4f})'"
        out, tipo, forca = f'[ef{i}]', e['tipo'], float(e.get('forca', 1))
        if tipo == 'impacto':
            g.append(f"{cur}negate={en},hue=s=0:{en}{out}")
        elif tipo == 'flash':
            f = float(e.get('fade', .12))
            g.append(f"color=white:s={W}x{H}:r={fps}:d={b - a + f:.4f},format=yuva420p,"
                     f"fade=t=out:st={b - a:.4f}:d={f}:alpha=1,setpts=PTS+{a:.4f}/TB[fl{i}];"
                     f"{cur}[fl{i}]overlay=eof_action=pass{out}")
        elif tipo == 'tingido':  # tela em 1 cor: cinza (luminância) vezes a cor, um pouco mais claro
            rgb = cor(e.get('cor', '#ff2a2a'))
            mx = ':'.join(f'{c}{k}={v * w * 1.3:.3f}' for c, v in zip('rgb', rgb) for k, w in zip('rgb', (.3, .59, .11)))
            g.append(f"{cur}colorchannelmixer={mx}:{en}{out}")
        elif tipo == 'aberracao':
            k = max(2, round(W * .006 * forca))
            g.append(f"{cur}rgbashift=rh=-{k}:bh={k}:rv={k // 2}:bv=-{k // 2}:{en}{out}")
        elif tipo == 'linhas':
            png = Path(pasta) / f'linhas{i}.png'
            desenhar_linhas(png, W, H, e.get('modo', 'radial'), seed=i)
            # 1 quadro só + filtro loop. Entrada com -loop/-t travava o ffmpeg 8 no meio do vídeo (testado 12/11)
            args += ['-i', str(png)]
            j, nq = W // 40, max(1, round((b - a) * fps))  # a camada pula de lugar a cada quadro: parece animada
            g.append(f"[{n_in}:v]loop=loop={nq - 1}:size=1,setpts=N/({fps}*TB)+{a:.4f}/TB[ln{i}];"
                     f"{cur}[ln{i}]overlay=x='-{j}+mod(n*37,{2 * j})':y='-{j}+mod(n*53,{2 * j})':eof_action=pass{out}")
            n_in += 1
        elif tipo in ('smash_zoom', 'eco'):
            # ponytail: o trecho é recortado antes, num arquivo à parte, com o número exato de quadros.
            # split+trim guardaria na memória todos os quadros até o efeito; -ss/-t na entrada e trim
            # depois do zoompan travavam o ffmpeg 8 (testado 12/11)
            nq = max(1, round((b - a) * fps))
            pq = min(5, round(a * fps)) if tipo == 'eco' else 0  # o eco precisa de quadros antes para o rastro
            trecho = Path(pasta) / f'trecho{i}.mp4'
            subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{a - h - pq / fps:.4f}', '-i', str(video),
                            '-frames:v', str(pq + nq), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '12',
                            str(trecho)], check=True)
            args += ['-i', str(trecho)]
            if tipo == 'smash_zoom':
                z = 1 + .6 * forca
                fx = (f"scale={3 * W}:{3 * H},zoompan=z='1+{z - 1:.3f}*(1-pow(1-min(1,on/{max(1, nq - 1)}),3))':"
                      f"x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={W}x{H}:fps={fps}")
            else:
                fx = f"tmix=frames=6:weights='1 1 1 1 2 4',trim=start_frame={pq}"
            g.append(f"[{n_in}:v]setpts=PTS-STARTPTS,{fx},setpts=PTS-STARTPTS+{a:.4f}/TB[zz{i}];"
                     f"{cur}[zz{i}]overlay=eof_action=pass{out}")
            n_in += 1
        elif tipo == 'tremida':
            trem.append((a - h, b - h, forca))
            continue
        else:
            raise ValueError(f'efeito desconhecido: {tipo} (use {", ".join(PADRAO)})')
        cur = out
    if trem:  # todas as tremidas numa passada só: borda espelhada + recorte que pula de lugar
        m = 2 * (H // 100)
        w = '+'.join(f'{f}*gte(t,{x:.4f})*lt(t,{y:.4f})' for x, y, f in trem)
        g.append(f"{cur}pad=iw+{2 * m}:ih+{2 * m}:{m}:{m},fillborders=left={m}:right={m}:top={m}:bottom={m}:mode=mirror,"
                 f"crop={W}:{H}:x='{m}+{m}*clip(({w})*sin(n*12.9898),-1,1)':y='{m}+{m}*clip(({w})*sin(n*78.233),-1,1)'[eftr]")
        cur = '[eftr]'
    return args, g, cur, n_in


def aplicar(entrada, saida, efeitos, pasta=None):
    """Roda os efeitos num vídeo já pronto (mantém o som)."""
    pr = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                    'stream=width,height,r_frame_rate', '-of', 'json', str(entrada)],
                                   capture_output=True, text=True, check=True).stdout)['streams'][0]
    W, H = pr['width'], pr['height']
    n, dd = map(int, pr['r_frame_rate'].split('/'))
    fps = round(n / dd)
    pasta = Path(pasta or tempfile.mkdtemp())
    args, g, cur, _ = grafo(efeitos, W, H, fps, pasta, entrada)
    (pasta / 'efeitos.txt').write_text(';'.join(g + [f'{cur}format=yuv420p[vout]']), encoding='utf8')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-reinit_filter', '0', '-i', str(entrada), *args, '-/filter_complex', str(pasta / 'efeitos.txt'),
                    '-map', '[vout]', '-map', '0:a?', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium',
                    '-c:a', 'copy', str(saida)], check=True)


def amostra(video, t):
    """Cor média (r, g, b) do quadro no tempo t."""
    px = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.4f}', '-i', str(video), '-frames:v', '1',
                         '-vf', 'scale=1:1:flags=area', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                        capture_output=True, check=True).stdout
    return tuple(px[:3])


def teste():
    p = Path(tempfile.mkdtemp())
    ent, sai = p / 'ent.mp4', p / 'sai.mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i', 'testsrc2=s=640x360:r=30:d=4',
                    '-pix_fmt', 'yuv420p', str(ent)], check=True)
    efs = [{'tipo': 'impacto', 'tempo': .5}, {'tipo': 'flash', 'tempo': 1.0}, {'tipo': 'tingido', 'tempo': 1.5},
           {'tipo': 'tremida', 'tempo': 1.8}, {'tipo': 'aberracao', 'tempo': 2.2}, {'tipo': 'linhas', 'tempo': 2.6},
           {'tipo': 'smash_zoom', 'tempo': 3.0}, {'tipo': 'eco', 'tempo': 3.3}]
    aplicar(ent, sai, efs, p)
    nq = subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries',
                         'stream=nb_read_frames', '-of', 'csv=p=0', str(sai)], capture_output=True, text=True).stdout
    assert int(nq) == 120, nq  # nenhum quadro a mais nem a menos
    r, g, b = amostra(sai, 1.0 + .01)
    assert min(r, g, b) > 235, ('flash', r, g, b)
    r, g, b = amostra(sai, .5 + .01)
    assert max(r, g, b) - min(r, g, b) < 8, ('impacto sem cor', r, g, b)
    r, g, b = amostra(sai, 1.5 + .01)
    assert r > 2 * g and r > 2 * b, ('tingido vermelho', r, g, b)
    print('teste OK', p)


if __name__ == '__main__':
    if sys.argv[1:] == ['--teste']:
        teste(); sys.exit()
    efs = []
    for s in sys.argv[3:]:
        tipo, resto = s.split('@')
        parte = resto.split(':')
        e = {'tipo': tipo, 'tempo': float(parte[0])}
        if len(parte) > 1 and parte[1]:
            e['duracao'] = float(parte[1])
        if len(parte) > 2:
            e[{'tingido': 'cor', 'linhas': 'modo'}.get(tipo, 'forca')] = parte[2]
        efs.append(e)
    aplicar(sys.argv[1], sys.argv[2], efs)
