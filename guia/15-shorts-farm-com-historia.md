# Guia 15 — Short de farm com história (gravado no jogo, editado por código)

Método testado em 12–13/11/2026 com 3 shorts (mel, lã, alga), ~60 s cada, 1080×1920 60 fps.
Exemplo completo (roteiros, planos de montagem, lista de cenas): `exemplos/04-shorts-farms-mel-la-alga/`.
Scripts: `ferramentas/shorts-farm/` (README lá dentro).

O resumo: **um personagem tem um problema real do jogo → cada peça da farm resolve um "Mas…" → virada no fim.**
Tudo é gravado no Minecraft aberto pela ponte MCP, a voz é TTS, e a montagem (cortes, legenda, números, trilha) sai de um JSON.

---

## 1. Roteiro: história, não tutorial

Tutorial puro foi **rejeitado**. A edição foi aprovada; o que mudou foi o roteiro.

- **Protagonista "Ele"** (Steve padrão), narrador em 3ª pessoa no passado, estilo Zack D. Films: começa no meio da ação ("Ele tinha seis golens de cobre…").
- **O motivo vem da própria jogabilidade**, coisas que acontecem com quem joga: golem de cobre que oxida e vira estátua, carvão que acaba no meio da obra, raio que queima lã, crafter que trava, enxame que ataca. História de fora do jogo (bilhete do avô etc.) não funcionou.
- **Uso real do item:** lã = construção / pixel art, não só cama. Alga seca = combustível para derreter areia de uma estufa.
- **Espinha problema → solução** (molde do short da Nixie "Existe um número que organiza o seu baú"): gancho com número → peça base → **Mas** (falha real) → **Então** (uma peça nova) → … → máquina completa → escala → payoff.
  Conectores fixos: *Porque / Mas / Então / Agora / Até que*. Cada "Mas" mostra algo dando errado **com ele**.
- **1 número verdadeiro por ciclo** (comparador da colmeia lê 0–5; sinal cai 1 por bloco de fio; bloco de alga seca queima 20 itens; 1 carvão derrete 8).
- **Virada**: no meio (o crafter travou de noite) e/ou no fim, irônica ("um raio caiu bem nela… ele sorriu e foi buscar mais lã"; "o carvão da mina? virou tocha").
- 150–230 palavras ≈ 60 s com TTS. Frases de 6–14 palavras. Sem "se inscreva".
- **Todo fato testado no jogo antes de escrever** (versão anotada). Os "Mas" saem do que de fato falha quando a farm está montada só até aquela etapa.

Mostre o roteiro ao usuário antes de gravar.

## 2. Dois tipos de tomada

| Tipo | O que mostra | Script modelo |
|---|---|---|
| **Técnica** | a farm sendo montada peça por peça e funcionando de verdade (comparador acendendo, ejetor tosando, alga sendo cortada) | `shoot_mel.py`, `shoot_la.py`, `shoot_alga.py` |
| **História** | o protagonista vivendo o problema: depósito bagunçado, golens virando estátua, abelhas atacando, parede de lã, raio + fogo, noite passando | `hist.py` (mel), `hist2.py` (lã e alga) |

Uma frase do roteiro = uma tomada curta (1,5–5 s). A técnica é sempre gameplay real; o encenado é a história.

### Protagonista sem segundo jogador
`heroi.py`: entidade **mannequin** (26.x) com a skin padrão:
```
summon mannequin x y z {Tags:["heroi"],hide_description:1b,profile:{texture:"entity/player/wide/steve"}}
```
- item na mão: `item replace entity @e[tag=heroi,limit=1] weapon.mainhand with minecraft:iron_axe`
- `pose:"sleeping"` funciona; andar = aplicar `Motion` a cada tick (`andar()`), as pernas animam sozinhas.

### Câmera cinematográfica (`cam26.py`)
O jogador (invisível, espectador da cena) monta num `block_display` com `teleport_duration` e o script move o display por uma spline Catmull-Rom, girando a visão a 60 Hz. `cam_path([pontos], seg)`; `olhando(posição, alvo)` calcula yaw/pitch.
Na instância 1.21.1 com CinematicTools os `shoot_*.py` usam `scene()/play()` (`/cinematic-server`).

### Truques que deram certo
- Golem de cobre oxidando: `data merge … {weather_state:"exposed"|"weathered"|"oxidized"}`; a estátua é bloco `oxidized_copper_golem_statue[copper_golem_pose=…]`. Raspar = trocar o bloco por um estado menos oxidado + som `item.axe.scrape` + partícula `scrape`.
- Abelhas atacando: `summon bee … {AngerTime:800,AngryAt:<UUID do mannequin>}`.
- Parede gigante de pixel art: `rosto.json` (8×8 cores de lã tiradas da skin), escala 4 → 32×32 blocos. Em 9:16 a câmera precisa de ~42 blocos de distância; fundo claro (bétula) para os pixels escuros aparecerem.
- Raio + fogo de verdade: `weather thunder`, `summon lightning_bolt`, `tick rate 60` durante o fogo, depois volte `tick rate 20`, `weather clear`, `time set` (as tomadas seguintes herdam tudo).
- Noite passando: laço de `time set` de 14000 a 24000 em ~2 s.
- `kill @e[type=copper_golem]` deixa sobreviventes/duplicatas; use `tp @e[type=copper_golem] ~ -80 ~`.

## 3. Gravação
`shot(nome, fn, segundos, pasta)` grava cada tomada: vídeo da janela (`gfxcapture`, 60 fps, NVENC) com **pts no relógio de parede**, áudio **só do processo do Minecraft** (não pega Discord/YouTube) e um JSON de eventos (`ev('raio')` marca o instante exato do acontecimento).
Antes: `preparar()` (janela 608×1080 inteira num monitor, jogo não pausa sem foco, jogador invisível sem nome) e `f1()` (esconde o HUD e o aviso "AI has control"; confira `hud_texto() == 0`). No fim: `restaurar()`.

Conferência: `info.py brutos/<pasta>` (duração + eventos) e `folha.py saida.jpg 1 <tomadas…>` → **uma** folha de contato 1 quadro/s de todas as tomadas, **uma** análise visual, refaz só as ruins.

## 4. Voz e alinhamento
- Um lote de TTS para os 3 vídeos (gasta 1 geração): separe os textos com `<break time="2s"/>` e corte o áudio nos silêncios. Voz usada: "Davi Andrei" (DarkPlanner). Gemini TTS também serve (guia 13). Voz de IA → marcar "conteúdo sintético" no YouTube.
- Whisper com tempo por palavra → `alinhar.py` casa com o texto do roteiro → `pal_<video>.json` = `[[ini, fim, "palavra"], …]` (a legenda usa o texto do roteiro, não o que o Whisper ouviu).

## 5. Montagem por plano (`planejar.py` → `legendas.py` → `montar.py`)
O plano (`planos/*.json`) diz, por frase do roteiro, quais trechos de tomada entram:
```json
{"frases":[4,5], "segs":[{"take":"hist/M_s3_oxida","a":0.5,"b":6.6}],
 "rotulos":[{"texto":"OXIDOU = VIROU ESTÁTUA","cor":"vermelho","de":0.45}],
 "numeros":[{"texto":"5","palavra":"cinco","dur":1.3}]}
```
- A duração de cada batida vem da fala; a velocidade de cada trecho = (b−a)/duração (0,7–3× fica bom; espera longa vira timelapse com `"w":1` + trecho em 1×).
- `rotulos` = caixa no topo; `numeros` = número grande amarelo no centro, sincronizado com a palavra falada.
- Legenda: fonte pixelada **Monocraft** (OFL), 1–3 palavras, palavra falada em amarelo, embaixo.
- Trilha Mixkit (licença livre) com ducking pela voz, loudnorm −14 LUFS.

```
python planejar.py planos/v4_mel.json audio/v4/pal_mel.json tmp/v4_mel
python legendas.py audio/v4/pal_mel.json tmp/v4_mel/legendas.ass tmp/v4_mel/extras.json 0.3
python montar.py tmp/v4_mel/receita.json
```
Conferir: folha 1 qps do vídeo final (`ffmpeg -vf "fps=1,scale=180:320,tile=11x6"`), sem tela preta, legenda presente, número na hora certa.

## 6. Armadilhas
- Jogador aparece na tomada: invisível + `team … seeFriendlyInvisibles false` + mão vazia + F1.
- `playsound` sem coordenadas fica mudo; passe a posição do bloco.
- Pó de redstone por `setblock` vira ponto e não aciona o vizinho: use `redstone_wire[north=side,…]` ou coloque pelo jogador.
- Funil embaixo de crafter rouba os ingredientes: baú direto embaixo.
- Comparador dispara cedo com sinal baixo: o comprimento do fio é o filtro (e vira o "porquê numérico" do roteiro).
- Refazer uma tomada do meio quebra a continuidade da montagem da farm: volte as peças até aquele ponto.
- mkv com pts de relógio: use `setpts=PTS-STARTPTS` antes de `fps`/`tile`.
