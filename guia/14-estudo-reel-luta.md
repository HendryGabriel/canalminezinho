# Estudo quadro a quadro: reel de luta estilo anime (12/11/2026)

Fonte: um reel do Instagram (conta de edição de fãs), animação 3D de uma luta entre 2 personagens de anime conhecidos. 2 min 13 s, horizontal 1024×576.
Método: Claude in Chrome. Os quadros foram tirados dentro da página (sem baixar o vídeo): 1 quadro por segundo do vídeo inteiro (133 quadros) + 3 trechos rápidos com 1 quadro a cada 0,1 s (0,8–2,7 s · 6,4–8,3 s · 111,6–113,5 s) + medida de troca de imagem a cada 1/12 s nos primeiros 34 s.
O áudio não foi medido: o navegador bloqueou o som sem um clique real. Para estudar o som é preciso baixar o vídeo (com o OK do usuário).

**Copiamos a técnica, nunca os personagens.** Para os nossos vídeos: lutadores próprios (formato 3, guia 11).

## 1. O que faz o vídeo parecer "incrível"
1. **Corte muito rápido:** nos primeiros 34 s, ~31 trocas de plano (1 plano novo a cada ~1,1 s), e dentro de cada golpe mais 2–4 quadros especiais de 1/12 s.
2. **Escala que só cresce** (igual ao TheLuics!): arena → céu → planeta → sistema solar (Terra, Júpiter, Sol) → galáxia → buraco negro → explosão final. Cada nível de poder leva a luta para um cenário maior.
3. **Paleta por fase:** azul (velocidade) → vermelho (poder subindo) → rosa/magenta (caos) → dourado/laranja (sol, buraco negro) → azul-branco (final). Toda a tela muda de cor junto com o poder.
4. **Quadros de impacto** em todo golpe forte (abaixo).
5. **Animação "em dois":** a pose fica parada 2–3 quadros e pula para a próxima (em 111,6–112,9 s as poses seguram ~0,1–0,3 s). É o que dá cara de anime, e não de jogo.
6. **Plano parado antes da explosão:** segura a imagem (carregando a energia), depois **flash branco** e o golpe.
7. **Final calmo:** pose do vencedor com fundo de linhas animadas em loop, poucos segundos, sem corte.

## 2. Dicionário de efeitos (o que se vê quadro a quadro)
| Efeito | Onde | O que é | Como fazer (Blender / ffmpeg / Minecraft) |
|---|---|---|---|
| quadro de impacto invertido | 7,00 s | 1 quadro preto e branco, cores invertidas, linhas radiais | compositor: invert + preto e branco + textura de linhas; ou `ffmpeg -vf negate,hue=s=0` em 1–2 quadros |
| flash branco | 113,0 s | 1–3 quadros quase todos brancos, depois a explosão | quadro branco + fade de 3 quadros; luz de emissão enorme no 3D |
| tela tingida | 6,6–6,7 s | quadro inteiro vermelho com manchas do golpe | camada de cor sólida em modo "multiplicar/tela" por 2 quadros |
| linhas de velocidade | 1,0–1,4 s · 7,2–8,1 s | linhas radiais (zoom) ou paralelas (corrida) por cima da imagem | planos finos com emissão no 3D, ou overlay PNG/vídeo na edição |
| rastro / fantasma | 2,0–2,7 s | o corpo aparece 2–3 vezes, meio transparente, no movimento | "echo" na edição (`ffmpeg tmix`) ou cópias do personagem com transparência |
| anéis de choque | 1,1–1,2 s | arcos brancos em volta do corpo no impulso | anel com emissão crescendo e sumindo em 6–8 quadros |
| aberração cromática | 112,x s | borda vermelha/azul separada nas silhuetas | compositor (Lens Distortion → Dispersion) ou `ffmpeg rgbashift` |
| tremida de câmera | golpes | câmera chacoalha 3–6 quadros | modificador Noise na câmera (Blender) ou `crop` com deslocamento aleatório |
| "smash zoom" | 1,0–1,5 s | o lutador voa até encher a tela em 0,5 s | câmera parada + personagem vindo; ou `zoompan` rápido |
| câmera de cima | 7,2–8,1 s | vista do alto da arena, o rastro vermelho cruzando | câmera top-down, lente longa |
| contra-plongée / ângulo torto | vários | câmera baixa e inclinada | câmera com roll de 10–25° |
| mapa de trajetória | 70–72 s · 115 s · 119 s | fundo preto com grade branca e 2 linhas curvas mostrando o caminho dos 2 lutadores | grade + curvas animadas (Grease Pencil, Remotion ou ffmpeg `drawbox`/overlay) |
| letreiro de tela cheia | 111 s | 1 símbolo enorme vermelho em fundo preto por ~1 s | cartela própria (nunca copiar a da obra) |
| plateia reagindo | 25 s | corte para o público espantado | figurantes + 1 plano de reação |
| carga de energia | 83–88 s | bola de luz crescendo na mão, partículas indo para dentro, depois o raio | esfera com emissão + partículas com força de atração + glare |
| buraco negro / anel de luz | 90–97 s · 124–127 s | anel brilhante dourado em volta de uma esfera preta | anel com emissão + esfera preta + glare + lente |

## 3. Ritmo de uma troca de golpes (molde de 3 s)
| Tempo | Quadro |
|---|---|
| 0,0–0,4 s | plano aberto: os 2 lutadores, câmera parada |
| 0,4–0,9 s | smash zoom: um avança até a câmera, linhas de velocidade |
| 0,9–1,0 s | **1 quadro de impacto** (invertido ou tingido) |
| 1,0–1,5 s | close do golpe, rastro + anel de choque, tremida |
| 1,5–1,6 s | flash ou quadro de cor |
| 1,6–2,4 s | plano de cima / de lado: o outro voando longe |
| 2,4–3,0 s | close do rosto de quem levou (reação), pose segurada |
Repita trocando o ângulo e subindo o cenário a cada 15–25 s.

## 4. Fazer no nosso estilo Minecraft
### Formato 3 (Blender) — o caminho que chega perto
1. **Personagens próprios** com rig do MCprep (cotovelo e joelho dobrando) e skins próprias.
2. **Look anime (toon):** material com "Shader to RGB" + Color Ramp em 2–3 degraus (sombra dura) + contorno (Freestyle ou casca invertida com Solidify). Texturas de pixel continuam (é o charme do Minecraft).
3. **Animação em dois:** F-Modifier "Stepped Interpolation" (passo 2) nas curvas dos personagens; câmera continua suave.
4. **Cenários:** arena e cidade do Minecraft (Mineways → MCprep); espaço, planetas de blocos e buraco negro feitos no Blender.
5. **Efeitos:** a tabela do §2 vira um arquivo `efeitos.blend` com cada efeito pronto (aura, raio, anel de choque, flash, linhas, buraco negro). O Claude coloca por script nos tempos certos.
6. **Pós por script (ffmpeg):** quadros de impacto, flash, tela tingida, aberração e tremida aplicados nos quadros marcados no `cenas.md`. Assim o Claude repete o efeito sem retrabalho no 3D.
7. **Cor por fase** (azul → vermelho → rosa → dourado → azul-branco) feita no compositor com 1 preset por fase.

### Formato 2 (no jogo) — versão simples
Dá para pegar parte da energia sem Blender: rig de câmera rápido (guia 09), partículas por comando (`/particle explosion_emitter`, `flash`, `end_rod`, `sonic_boom`), personagens com gestos (Easy NPC + Emotecraft), e todos os efeitos de pós do §2 feitos no ffmpeg (impacto invertido, flash, tingido, tremida, linhas por overlay). Fica mais "jogo" e menos "anime", mas é rápido.

### Som (a confirmar com o áudio)
Pelo gênero e pelos quadros: um baque grave em cada quadro de impacto, whoosh em cada smash zoom, silêncio de 0,3–1 s antes do flash branco, explosão longa com cauda no flash, música épica que acompanha as fases de cor. Para medir de verdade: baixar o reel (com o OK do usuário) e rodar `ferramentas/medir_video.py` + análise de picos do áudio.
