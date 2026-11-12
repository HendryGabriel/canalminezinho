# Edição automática (ffmpeg + Python)

Monta o vídeo nos tempos da voz: planos, pausas de cena esticadas, música que abaixa quando a voz fala,
efeitos sonoros, textos, efeitos de pós e o volume final em -14 LUFS. Também faz lip sync simples e thumbnail.

Precisa de: Python 3.12, ffmpeg no PATH, Pillow (textos, linhas e thumb). Nada mais.
Sempre rode com `python -X utf8`.

| Arquivo | Faz | Teste rápido |
|---|---|---|
| `montar.py` | lê `montagem.json` e gera `final.mp4` | `python -X utf8 montar.py --teste` |
| `efeitos.py` | 8 efeitos de pós; roda sozinho num mp4 pronto | `python -X utf8 efeitos.py --teste` |
| `lipsync.py` | voz → boca fechada/meio/aberta por quadro | `python -X utf8 lipsync.py --teste` |
| `thumb.py` | thumbnail 1280×720 | `python -X utf8 thumb.py --teste saida.jpg` |
| `teste.py` | teste completo com material falso | `python -X utf8 teste.py` |

`teste.py` grava tudo em `ESTUDOS/canalminezinho-testes/edicao/` (fora do repositório). No fim, olhe
`quadros/folha.png` (cada efeito: antes × durante) e `thumb.jpg`.

## Fluxo
1. `ferramentas/alinhar_voz.py roteiro.md voz.wav` → `tempos.json`.
2. Escreva `videos/NN_tema/montagem.json` a partir do `cenas.md` (planos, efeitos, textos, som).
3. `python -X utf8 ferramentas/edicao/montar.py videos/NN_tema/montagem.json` → `final.mp4`.

## Como o montar.py trabalha (4 passadas)
1. **Voz:** onde o roteiro tem `[pausa de cena N s]` e a pausa gravada é menor que N, põe silêncio no meio
   da pausa até dar N. Tudo o que vem depois anda junto (planos, música, textos).
2. **Planos:** cada plano vira um pedaço com o número exato de quadros e os pedaços são colados sem recodificar.
   Cada plano vai do seu `quando` até o `quando` do próximo. Antes do 1º plano: preto.
   Clipe mais curto que o espaço: segura o último quadro.
3. **Som:** voz + músicas (abaixam sozinhas quando a voz fala: `sidechaincompress`; nas pausas sobem de novo)
   + sfx → `loudnorm` em 2 passadas: -14 LUFS integrado, pico abaixo de -1 dBTP.
4. **Final:** efeitos de pós, textos por cima, som → `final.mp4` (H.264 CRF 18, AAC 320k).

## Tempo (vale para `quando`, `inicio`, `fim`, `tempo`)
| Escrita | Quer dizer |
|---|---|
| `"F004"` ou `"F004:inicio"` | começo da frase F004 |
| `"F004:fim"` | fim da frase F004 (= começo da pausa) |
| `"F004+0,5"` · `"F004:fim-0.2"` | com ajuste em segundos (vírgula ou ponto) |
| `12.5` | segundo 12,5 **do vídeo final** (já com as pausas esticadas) |

## montagem.json
Caminhos relativos à pasta do `montagem.json`.
```json
{
  "voz": "voz.wav",
  "tempos": "tempos.json",
  "saida": "final.mp4",
  "formato": "16:9",
  "fps": 60,
  "fonte": "C:/Windows/Fonts/ariblk.ttf",
  "fim": "F120:fim+3",
  "ducking": "threshold=0.03:ratio=8:attack=20:release=400",
  "planos": [
    {"arquivo": "gravacoes/c001.mp4", "quando": 0, "in": 2.0, "out": 9.5},
    {"arquivo": "estudio/escala.png", "quando": "F002", "zoom": "in"},
    {"arquivo": "blender/c003/%04d.png", "quando": "F003", "fps": 24, "zoom": [1.0, 1.2]},
    {"arquivo": "gravacoes/c004.mp4", "quando": "F004:fim"},
    {"arquivo": "preto", "quando": "F010:fim"}
  ],
  "musicas": [
    {"arquivo": "../../biblioteca/musica/misterio.mp3", "inicio": 0, "fim": "F030:fim+1", "volume": -6, "fade": 1.5}
  ],
  "sfx": [
    {"arquivo": "../../biblioteca/sfx/boom.wav", "tempo": "F004:fim", "volume": -3}
  ],
  "textos": [
    {"texto": "R$ ???", "tempo": "F004+0,3", "duracao": 1.5, "estilo": "pop", "posicao": "centro"},
    {"texto": "GIGAN...", "tempo": "F006", "duracao": 2, "estilo": "digitando", "posicao": "baixo", "tamanho": 120, "cor": "#ffe14d"}
  ],
  "efeitos": [
    {"tipo": "impacto", "tempo": "F004:fim"},
    {"tipo": "tingido", "tempo": "F005", "cor": "#ff2a2a"},
    {"tipo": "tremida", "tempo": "F005+0.1", "duracao": 0.4, "forca": 1.5},
    {"tipo": "linhas", "tempo": "F006", "modo": "paralelo"}
  ]
}
```

| Campo | Padrão | O que é |
|---|---|---|
| `formato` | `"16:9"` | `"16:9"` = 1920×1080 · `"9:16"` = 1080×1920 (Shorts) |
| `fps` | 30 | 30 ou 60 |
| `fim` | fim da voz | onde o vídeo acaba (para a música tocar depois da última fala) |
| `pasta_temp` | `_montagem` | pasta dos arquivos intermediários (pode apagar depois) |
| `ducking` | receita do guia 05 §7 | opções do `sidechaincompress`; `ratio` maior = música abaixa mais na fala |
| **planos[]** | | |
| `arquivo` | — | mp4/mov, imagem (png/jpg/webp), sequência `pasta/%04d.png` ou `"preto"` |
| `quando` | — | começo do plano (o fim é o começo do próximo) |
| `in` / `out` | 0 / fim | corte do clipe em segundos do próprio clipe |
| `fps` | fps do vídeo | só sequência de PNG: em que velocidade ela foi renderizada |
| `zoom` | sem | zoom lento (Ken Burns): `"in"` (1→1,12), `"out"`, `true` ou `[início, fim]` |
| **musicas[]** | | |
| `inicio` / `fim` | 0 / fim do vídeo | música curta repete sozinha |
| `volume` | -6 | dB sobre o arquivo (é o volume nas pausas; na fala ela abaixa mais) |
| `fade` | 1 | segundos de entrada e de saída |
| **sfx[]** | `tempo`, `volume` (0 dB) | toca 1 vez inteiro |
| **textos[]** | | |
| `estilo` | `pop` | `pop` (50%→100% com bounce em 0,25 s) · `digitando` (1 letra a cada 0,05 s) · `fixo` |
| `posicao` | `centro` | `centro` · `cima` · `baixo` · `[x, y]` (centro do texto em pixels) |
| `duracao` | 1,5 | segundos; some com fade de 0,15 s |
| `tamanho` / `cor` | altura/8 · branco | contorno escuro e sombra dura são automáticos |
| **efeitos[]** | `tipo`, `tempo`, `duracao`, opções | tabela abaixo |

## Efeitos (guia 14 §2)
| tipo | Padrão | O que faz | Opções |
|---|---|---|---|
| `impacto` | 2 quadros | negativo preto e branco | — |
| `flash` | 2 quadros + some em 0,12 s | tela branca | `fade` |
| `tingido` | 2 quadros | tela toda de 1 cor | `cor` (`#ff2a2a`) |
| `tremida` | 0,3 s | chacoalha (recorte que pula, borda espelhada) | `forca` (1) |
| `aberracao` | 0,3 s | borda vermelha/azul separada | `forca` (1 = 12 px em 1080p) |
| `linhas` | 0,5 s | linhas de velocidade por cima, mexendo | `modo`: `radial` · `paralelo` |
| `smash_zoom` | 0,5 s | zoom brusco até 1,6× | `forca` (1) |
| `eco` | 0,6 s | rastro/fantasma (`tmix`) | — |

Duração em `duracao` (segundos). Os textos ficam por cima dos efeitos (continuam legíveis).
Sozinho num vídeo pronto: `python -X utf8 efeitos.py ent.mp4 sai.mp4 impacto@1.0 tingido@2:0.07:#3070ff linhas@3:0.5:paralelo`.

## Lip sync
`python -X utf8 lipsync.py voz.wav 30 boca.json` → `{"fps": 30, "estados": [0, 1, 2, ...]}`.
Use no Blender/Animated Java para trocar a textura da boca em cada quadro.
Ajustes em `estados(...)`: `meio=.15`, `aberta=.45` (fração do volume forte da voz), `histerese=.7`.

## Thumbnail
`python -X utf8 thumb.py fundo.png "MUNDO INFINITO" thumb.jpg --lugar baixo --seta 240,120,420,260 --circulo 560,300,110`
1 a 3 palavras; quebra em 2 linhas se não couber grande. Fonte padrão: Arial Black (do Windows).
**Lilita One** ou **Luckiest Guy** (Google Fonts, licença OFL) ficam melhores: baixe e use `--fonte`.

## Limites
- O som dos clipes é descartado. Som do jogo entra como `sfx`.
- Planos não se sobrepõem: corte seco sempre. Fusão/whip pan: faça no clipe antes.
- A música sobe nas pausas só pelo compressor (sem keyframe de volume). Quer mais alto numa pausa: 2ª música
  (`inicio`/`fim` na pausa) com `volume` maior.
- Efeitos e textos não se mexem com a câmera (são da tela). Contador, régua e seta animada: Remotion/Blender.
- Zoom lento usa upscale 3× (mais lento em clipe de vídeo longo).
- A voz inteira fica na memória ao esticar (~140 MB para 25 min).
- `aberracao` só aparece onde a imagem tem vermelho e azul; em imagem de 1 cor só (ex.: verde puro) não muda nada.
- `tremida` em imagem lisa (céu, gradiente) quase não se nota: use em plano com detalhe.
- Ducking e volume da música foram medidos só com som falso (seno). Na 1ª voz de verdade, ouça e ajuste
  `ducking`/`volume`.

## Armadilhas do ffmpeg 8 que o código já evita (12/11/2026)
- Entrada com `-loop 1`, ou `-ss/-t` na entrada, ou `trim` depois do `zoompan`: o ffmpeg travou no meio da
  passada final. Por isso as linhas usam 1 quadro + filtro `loop`, e o smash_zoom/eco usam um trecho recortado antes.
- Se a cor (bt709/bt601, faixa) muda de um plano para o outro, o ffmpeg reinicia os filtros e tudo depois
  dali perde os efeitos. Por isso todo plano sai em bt709 e a passada final usa `-reinit_filter 0`.
