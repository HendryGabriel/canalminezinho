"""Monta o vídeo final a partir de uma lista de edição (montagem.json). Formato no README.md.

Uso:   python -X utf8 montar.py videos/NN_tema/montagem.json
Teste: python -X utf8 montar.py --teste   (só as contas de tempo; o teste completo com vídeo é o teste.py)

Passadas (cada uma simples, todas com ffmpeg):
 1. voz: estica as pausas de cena (põe silêncio no meio da pausa) → voz_esticada.wav
 2. planos: cada plano vira um pedaço com o número exato de quadros → base.mp4 (concat sem recodificar)
 3. som: voz + música (abaixa quando a voz fala, sidechaincompress) + sfx → loudnorm -14 LUFS em 2 passadas
 4. final: base.mp4 + efeitos + textos (PNG do Pillow) + som → final.mp4
"""
import json, re, subprocess, sys, wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import efeitos

FONTE = r'C:\Windows\Fonts\ariblk.ttf'
IMAGEM = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}
REF = re.compile(r'^(F\d+)(?::(inicio|início|fim))?\s*(?:([+-])\s*([\d.,]+))?$', re.I)
DUCKING = 'threshold=0.03:ratio=8:attack=20:release=400'  # receita do guia 05 §7


def run(cmd):
    subprocess.run([str(c) for c in cmd], check=True)


def duracao(arq):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(arq)],
                                capture_output=True, text=True, check=True).stdout)


# ---------- tempo ----------
def esticos(falas):
    """Onde pôr silêncio na voz: [(segundo na voz original, quanto)] para cada pausa de cena curta demais."""
    return [(f['fim'] + f['pausa_real'] / 2, f['pausa_roteiro'] - f['pausa_real'])
            for f in falas if f.get('pausa_de_cena') and f['pausa_real'] < f['pausa_roteiro']]


def mapear(t, est):
    """Segundo da voz original → segundo do vídeo final."""
    return t + sum(add for pos, add in est if pos < t)


def tempo(x, falas, est):
    """'F004' (início), 'F004:fim', 'F004+0,5', 'F004:fim-0.2' ou número (segundos do vídeo final)."""
    if isinstance(x, (int, float)):
        return float(x)
    m = REF.match(str(x).strip())
    if not m:
        return float(str(x).replace(',', '.'))
    if m[1] not in falas:
        raise KeyError(f'{m[1]} não está no tempos.json')
    f = falas[m[1]]
    t = mapear(f['fim'] if (m[2] or '').lower() == 'fim' else f['inicio'], est)
    if m[3]:
        t += float(m[4].replace(',', '.')) * (1 if m[3] == '+' else -1)
    return t


# ---------- 1. voz ----------
def esticar_voz(voz, est, saida):
    pcm = saida.with_name('voz_pcm.wav')
    run(['ffmpeg', '-y', '-v', 'error', '-i', voz, '-ar', 48000, '-ac', 1, '-c:a', 'pcm_s16le', pcm])
    # ponytail: a voz inteira na memória (~140 MB para 25 min); ler em blocos se um dia faltar memória
    with wave.open(str(pcm)) as w:
        p, dados = w.getparams(), w.readframes(w.getnframes())
    bloco, partes, ult = p.sampwidth * p.nchannels, [], 0
    for pos, add in sorted(est):
        k = min(round(pos * p.framerate), p.nframes) * bloco
        partes += [dados[ult:k], bytes(round(add * p.framerate) * bloco)]
        ult = k
    partes.append(dados[ult:])
    with wave.open(str(saida), 'wb') as w:
        w.setparams(p)
        w.writeframes(b''.join(partes))


# ---------- 2. planos ----------
def plano(p, n, W, H, fps, saida, base):
    arq = p.get('arquivo', 'preto')
    if arq == 'preto':
        ent = ['-f', 'lavfi', '-i', f'color=black:s={W}x{H}:r={fps}']
    elif '%' in arq:  # sequência de PNG: pasta/%04d.png
        ent = ['-framerate', p.get('fps', fps), '-i', base / arq]
    elif Path(arq).suffix.lower() in IMAGEM:
        ent = ['-loop', 1, '-framerate', fps, '-i', base / arq]
    else:
        ent = ['-ss', p.get('in', 0)] + (['-t', p['out'] - p.get('in', 0)] if 'out' in p else []) + ['-i', base / arq]
    z = p.get('zoom')
    if z:
        z0, z1 = {True: (1, 1.12), 'in': (1, 1.12), 'out': (1.12, 1)}.get(z if not isinstance(z, list) else None, z)
        # ponytail: upscale 3x antes do zoompan tira o tremido de arredondamento (lição do canal-dark)
        vf = (f"fps={fps},scale={3 * W}:{3 * H}:force_original_aspect_ratio=increase,crop={3 * W}:{3 * H},"
              f"zoompan=z='{z0}+{z1 - z0}*on/{max(n - 1, 1)}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={W}x{H}:fps={fps}")
    else:
        vf = f"fps={fps},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
    # clipe mais curto que o espaço dele: segura o último quadro
    # todo plano sai igual (bt709, faixa tv): se a cor de um pedaço muda no meio do base.mp4, o ffmpeg
    # reinicia o filtergraph e os efeitos/textos depois dali somem (aconteceu no teste com smptebars)
    vf = vf.replace('force_original_aspect_ratio=increase', 'force_original_aspect_ratio=increase:out_color_matrix=bt709:out_range=tv', 1)
    vf += (',tpad=stop_mode=clone:stop_duration=86400,setsar=1,format=yuv420p,'
           'setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709')
    run(['ffmpeg', '-y', '-v', 'error', *ent, '-vf', vf, '-frames:v', n, '-an', '-r', fps,
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', 16, saida])


# ---------- 3. som ----------
def som(c, voz, total, T, base, saida, pasta):
    fmt = 'aformat=sample_rates=48000:channel_layouts=stereo'
    ent = ['-i', voz]
    g = [f'[0:a]{fmt},apad,atrim=0:{total:.3f},asplit=2[voz][sc]']
    mix, mus, k = ['[voz]'], [], 1
    for j, m in enumerate(c.get('musicas', [])):
        a = T(m.get('inicio', 0))
        d = min(T(m['fim']) if 'fim' in m else total, total) - a
        f = float(m.get('fade', 1))
        ent += ['-stream_loop', -1, '-i', base / m['arquivo']]  # música curta repete
        g.append(f"[{k}:a]{fmt},atrim=0:{d:.3f},volume={m.get('volume', -6)}dB,afade=t=in:d={f},"
                 f"afade=t=out:st={max(d - f, 0):.3f}:d={f},adelay={round(a * 1000)}:all=1[m{j}]")
        mus.append(f'[m{j}]')
        k += 1
    if mus:
        g.append(f"{''.join(mus)}amix=inputs={len(mus)}:normalize=0,apad,atrim=0:{total:.3f}[mb];"
                 f"[mb][sc]sidechaincompress={c.get('ducking', DUCKING)}[duck]")
        mix.append('[duck]')
    else:
        g.append('[sc]anullsink')
    for s in c.get('sfx', []):
        ent += ['-i', base / s['arquivo']]
        g.append(f"[{k}:a]{fmt},volume={s.get('volume', 0)}dB,adelay={round(T(s['tempo']) * 1000)}:all=1[s{k}]")
        mix.append(f'[s{k}]')
        k += 1
    mixf = f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first,atrim=0:{total:.3f}"
    # loudnorm em 2 passadas (1 passada errava 2 dB no canal-dark). TP -1,5 porque o AAC sobe o pico ~0,3 dB
    ln = 'loudnorm=I=-14:TP=-1.5:LRA=11'
    gt = pasta / 'som.txt'
    gt.write_text(';'.join(g + [f'{mixf},{ln}:print_format=json[aout]']), encoding='utf8')
    r = subprocess.run([str(x) for x in ['ffmpeg', '-y', '-hide_banner', *ent, '-/filter_complex', gt,
                                         '-map', '[aout]', '-f', 'null', '-']], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr[-3000:])
    m = json.loads(r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}') + 1])
    gt.write_text(';'.join(g + [f"{mixf},{ln}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
                                f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
                                f"offset={m['target_offset']}:linear=true,aresample=48000[aout]"]), encoding='utf8')
    run(['ffmpeg', '-y', '-v', 'error', *ent, '-/filter_complex', gt, '-map', '[aout]', '-c:a', 'pcm_s16le', saida])


# ---------- 4. textos ----------
def texto_quadros(t, W, H, fps, fonte, pasta, i):
    """Desenha o texto (branco, contorno escuro, sombra dura) quadro a quadro da animação de entrada."""
    from PIL import Image, ImageDraw, ImageFont
    tam = int(t.get('tamanho', H // 8))
    f = ImageFont.truetype(str(fonte), tam)
    borda, sombra = max(3, tam // 12), max(4, tam // 14)
    l, tp, r, b = f.getbbox(t['texto'], stroke_width=borda)
    w0, h0 = r - l + sombra, b - tp + sombra

    def desenha(s):
        im = Image.new('RGBA', (w0, h0))
        d = ImageDraw.Draw(im)
        d.text((-l + sombra, -tp + sombra), s, font=f, fill=(0, 0, 0, 190), stroke_width=borda, stroke_fill=(0, 0, 0, 190))
        d.text((-l, -tp), s, font=f, fill=t.get('cor', 'white'), stroke_width=borda, stroke_fill=(15, 15, 15))
        return im

    cheio, estilo, quadros = desenha(t['texto']), t.get('estilo', 'pop'), []
    if estilo == 'pop':  # 50% → passa um pouco de 100% → 100% (bounce) em 0,25 s
        cw, ch = round(w0 * 1.1) + 2, round(h0 * 1.1) + 2
        n = max(2, round(.25 * fps))
        for k in range(n + 1):
            q = k / n - 1
            s = .5 + .5 * (1 + 2.70158 * q ** 3 + 1.70158 * q ** 2)
            im = Image.new('RGBA', (cw, ch))
            p = cheio.resize((max(1, round(w0 * s)), max(1, round(h0 * s))), Image.LANCZOS)
            im.alpha_composite(p, ((cw - p.width) // 2, (ch - p.height) // 2))
            quadros.append(im)
    elif estilo == 'digitando':  # 1 letra a cada 0,05 s, alinhado à esquerda
        por_letra = max(1, round(.05 * fps))
        for k in range(1, len(t['texto']) + 1):
            quadros += [desenha(t['texto'][:k])] * por_letra
    else:
        quadros = [cheio]
    for k, im in enumerate(quadros):
        im.save(pasta / f't{i:02d}_{k:03d}.png')
    return pasta / f't{i:02d}_%03d.png'


def posicao(pos, W, H):
    if isinstance(pos, list):  # [x, y] do centro do texto, em pixels
        return f'{pos[0]}-w/2', f'{pos[1]}-h/2'
    return '(W-w)/2', {'centro': '(H-h)/2', 'cima': 'H*0.1', 'baixo': 'H*0.88-h'}[pos]


# ---------- tudo ----------
def montar(arq_json):
    arq_json = Path(arq_json).resolve()
    base = arq_json.parent
    c = json.loads(arq_json.read_text(encoding='utf8'))
    W, H = (1080, 1920) if c.get('formato') == '9:16' else (1920, 1080)
    fps = int(c.get('fps', 30))
    lista = json.loads((base / c['tempos']).read_text(encoding='utf8'))
    falas, est = {f['id']: f for f in lista}, esticos(lista)
    T = lambda x: tempo(x, falas, est)
    pasta = base / c.get('pasta_temp', '_montagem')
    pasta.mkdir(exist_ok=True)
    for velho in pasta.glob('t??_*.png'):
        velho.unlink()

    voz = pasta / 'voz_esticada.wav'
    esticar_voz(base / c['voz'], est, voz)
    total = T(c['fim']) if 'fim' in c else duracao(voz)
    Q = round(total * fps)

    # planos: cada um vai até o começo do próximo; antes do 1º, preto
    planos = sorted(c['planos'], key=lambda p: T(p['quando']))
    ini = [T(p['quando']) for p in planos]
    if not planos or ini[0] > 0:
        planos.insert(0, {'arquivo': 'preto'})
        ini.insert(0, 0.0)
    qs = [min(round(t * fps), Q) for t in ini] + [Q]
    segs = []
    for i, p in enumerate(planos):
        n = qs[i + 1] - qs[i]
        if n > 0:
            segs.append(pasta / f'p{i:03d}.mp4')
            plano(p, n, W, H, fps, segs[-1], base)
    (pasta / 'planos.txt').write_text(''.join(f"file '{s.as_posix()}'\n" for s in segs), encoding='utf8')
    run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', 0, '-i', pasta / 'planos.txt', '-c', 'copy', pasta / 'base.mp4'])

    som(c, voz, total, T, base, pasta / 'som.wav', pasta)

    # efeitos primeiro, textos por cima (o texto fica legível no impacto/tremida)
    efs = [{**e, 'tempo': T(e['tempo'])} for e in c.get('efeitos', [])]
    args, g, cur, n_in = efeitos.grafo(efs, W, H, fps, pasta, pasta / 'base.mp4', '[0:v]', 2)
    for i, t in enumerate(c.get('textos', [])):
        a = round(T(t['tempo']) * fps) / fps
        d = float(t.get('duracao', 1.5))
        args += ['-framerate', fps, '-i', texto_quadros(t, W, H, fps, c.get('fonte', FONTE), pasta, i)]
        x, y = posicao(t.get('posicao', 'centro'), W, H)
        g.append(f"[{n_in}:v]format=rgba,tpad=stop_mode=clone:stop_duration={d:.3f},trim=duration={d:.3f},"
                 f"fade=t=out:st={max(d - .15, 0):.3f}:d=0.15:alpha=1,setpts=PTS-STARTPTS+{a:.4f}/TB[tx{i}];"
                 f"{cur}[tx{i}]overlay=x='{x}':y='{y}':eof_action=pass[vt{i}]")
        cur, n_in = f'[vt{i}]', n_in + 1
    (pasta / 'final.txt').write_text(';'.join(g + [f'{cur}format=yuv420p[vout]']), encoding='utf8')
    saida = base / c.get('saida', 'final.mp4')
    run(['ffmpeg', '-y', '-v', 'error', '-reinit_filter', 0, '-i', pasta / 'base.mp4', '-i', pasta / 'som.wav', *args,
         '-/filter_complex', pasta / 'final.txt', '-map', '[vout]', '-map', '1:a', '-r', fps,
         '-c:v', 'libx264', '-preset', 'medium', '-crf', 18, '-c:a', 'aac', '-b:a', '320k', '-ar', 48000,
         '-t', f'{total:.3f}', '-movflags', '+faststart', saida])
    print(f'ok: {saida}  {total:.2f} s  {W}x{H} {fps} fps  {len(segs)} planos  '
          f'{len(efs)} efeitos  {len(c.get("textos", []))} textos  pausas esticadas: {len(est)}')
    return saida, total


def teste():
    falas = [{'id': 'F001', 'inicio': 0.3, 'fim': 2.0, 'pausa_real': 0.6, 'pausa_roteiro': 0.5, 'pausa_de_cena': False},
             {'id': 'F002', 'inicio': 2.6, 'fim': 4.0, 'pausa_real': 2.0, 'pausa_roteiro': 15, 'pausa_de_cena': True},
             {'id': 'F003', 'inicio': 6.0, 'fim': 7.0, 'pausa_real': 0, 'pausa_roteiro': 0, 'pausa_de_cena': False}]
    est = esticos(falas)
    assert est == [(5.0, 13.0)], est
    fd = {f['id']: f for f in falas}
    T = lambda x: tempo(x, fd, est)
    assert T('F002:fim') == 4.0            # a pausa começa no mesmo lugar
    assert T('F003') == 19.0               # a frase depois da pausa anda 13 s
    assert T('F003:fim+0,5') == 20.5 and T('F001-0.3') == 0.0 and T(3) == 3.0 and T('2,5') == 2.5
    print('teste OK')


if __name__ == '__main__':
    if sys.argv[1:] == ['--teste']:
        teste(); sys.exit()
    montar(sys.argv[1])
