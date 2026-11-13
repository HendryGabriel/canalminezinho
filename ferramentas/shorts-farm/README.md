# ferramentas/shorts-farm — pipeline dos shorts de farm com história

Método: `guia/15-shorts-farm-com-historia.md`. Exemplo: `exemplos/04-shorts-farms-mel-la-alga/`.
Testado em 12–13/11/2026 (Windows 11, Minecraft Java 26.3 e 1.21.1 Fabric, ponte **MCP Fabric**).

## Configuração (variáveis de ambiente)
| Variável | Para que |
|---|---|
| `SHORTS_PROJETO` | pasta do vídeo (`brutos/`, `tmp/`, `final/`, `audio/`, `planos/`, `fontes/usar/`). Padrão: pasta atual |
| `MC_JOGADOR` | seu nick no jogo (nos scripts aparece como `@J`) |
| `MC_OPTIONS` | `options.txt` da instância (lê `pauseOnLostFocus`) |
| `MC_JANELA_X` | x do monitor onde a janela 608×1080 cabe inteira (parte fora da tela grava preta) |
| `GRAVAR_PYTHON` | python com `numpy` + `flexaudio` para o `gravar.py` (padrão: o atual) |

Precisa: ffmpeg 8+ (filtro `gfxcapture`; o vídeo sai em `h264_nvenc` — troque por `libx264` sem placa NVIDIA), Python com `numpy`, `pillow`, `flexaudio`; Whisper (`faster-whisper`) para alinhar a voz; fonte Monocraft (OFL, github.com/IdreesInc/Monocraft) em `<projeto>/fontes/usar/`.
A ponte lê URL e token de `~/.mcpfabric/bridge.json` (nunca imprime o token).

## Scripts
| Script | Faz |
|---|---|
| `mc.py` | cliente JSON-RPC da ponte (`call`, `cmd`, `shot`) |
| `keys.py`, `focus.py` | acha a janela do Minecraft, teclas reais (F1, F3+P) |
| `gravar.py`, `rec.py` | grava a janela (60 fps, pts = relógio) + áudio só do `javaw` + eventos |
| `fl.py` | `C()` comando, `preparar()/restaurar()`, `f1()`, `hud_texto()`, `put()` colocar bloco com orientação, `scene()/play()` (CinematicTools), `snd()`, `shot()` |
| `fl2.py` | colocação pelo jogador olhando na direção certa |
| `cam26.py` | câmera cinematográfica sem mod (rig `block_display` + spline): `rig_criar`, `olhando`, `cam_path`, `rig_fim` |
| `heroi.py` | protagonista mannequin com skin Steve: `heroi()`, `mao()`, `virar()`, `andar()` |
| `hist.py` / `hist2.py` | cenas de história do exemplo (mel / lã e alga) — uma função por tomada |
| `shoot_mel.py`, `shoot_la.py`, `shoot_alga.py` | tomadas técnicas: montagem das farms peça por peça (1.21.1 + CinematicTools) |
| `info.py` | lê as tomadas de uma pasta → `info.json` (duração, eventos em s) |
| `folha.py` | folha de contato de várias tomadas (`folha.py saida.jpg 1 brutos/x/a brutos/x/b`) |
| `alinhar.py` | casa as palavras do Whisper com o texto do roteiro |
| `ajustar_tempos.py` | corrige os tempos pela forma de onda: o Whisper adianta 0,1–0,3 s a palavra depois de cada pausa (legenda fora de sincronia). **Rodar sempre depois do alinhar** |
| `planejar.py` | plano por frase + tempos → `receita.json` + `extras.json` (rótulos, números) |
| `legendas.py` | legenda ASS pixelada (palavra falada em amarelo, rótulos, números) |
| `montar.py` | receita → MP4 final (velocidade por trecho, trilha com ducking, loudnorm −14) |
| `suavidade.py`, `fluxo.py` | medem tremida da câmera (diferença entre quadros / fluxo) |
| `rosto.json` | rosto do Steve 8×8 em cores de lã (parede de pixel art) |

As coordenadas dentro de `hist*.py` e `shoot_*.py` são do mundo do exemplo (área plana com grama em y=109, x 2..62, z 186..246). Num mundo novo, aplaine uma área e ajuste as coordenadas.

## Rodar uma cena
```
set SHORTS_PROJETO=D:\videos\05_meu_short
set MC_JOGADOR=SeuNick
python -c "from fl import *; preparar(); f1(); print(hud_texto())"
python hist.py m_s1 m_s3          # grava as tomadas em brutos/hist/
python info.py brutos/hist
python folha.py tmp/folha.jpg 1 brutos/hist/M_s1_deposito brutos/hist/M_s3_oxida
```
