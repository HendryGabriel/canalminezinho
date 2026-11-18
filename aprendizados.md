# Aprendizados (atualizar em todo vídeo)

O Claude lê este arquivo no começo de cada projeto e escreve aqui no fim. Assim cada vídeo sai melhor que o anterior.
Regra: 1 linha por aprendizado, com data e vídeo. O que virou regra fixa sobe para o guia certo.

## Técnica (o que funcionou / o que quebrou)
| Data | Vídeo | Aprendizado | Virou regra em |
|---|---|---|---|
| 2026-11-12 | — | Gemini pode errar "como é feito" (disse animação 3D num vídeo gravado no jogo): conferir sempre nos quadros. | guia 12 §0 |
| 2026-11-12 | — | O navegador bloqueia o áudio de vídeo sem clique real: para estudar som, baixar o vídeo (com o OK do usuário). | guia 14 |
| 2026-11-12 | shorts farms (mel/lã/alga) | João aprovou a edição (câmera, fonte pixelada, rótulos, números), mas rejeitou o roteiro de tutorial puro: quer storytelling com protagonista que tem um motivo, problema que justifica cada peça da farm e plot twist (referência: Zack D. Films). | guia 15 §1 |
| 2026-11-13 | shorts farms v4 | Protagonista sem 2º jogador: mannequin com `profile:{texture:"entity/player/wide/steve"}`; andar aplicando Motion por tick anima as pernas. | guia 15 §2 |
| 2026-11-13 | shorts farms v4 | `kill @e[type=copper_golem]` deixa golens sobrando/duplicados; mandar para baixo do mundo com `tp ... ~ -80 ~`. | guia 15 §2 |
| 2026-11-13 | shorts farms v4 | Parede de 32 blocos em 9:16 só cabe com a câmera a ~42 blocos; fundo claro para os pixels escuros aparecerem. | guia 15 §2 |
| 2026-11-13 | shorts farms v4 | Legenda fora de sincronia nos 3 v4: o Whisper adianta 0,1–0,3 s a palavra depois de cada pausa. Corrigido com `ajustar_tempos.py` (silencedetect). | guia 15 §4 |
| 2026-11-13 | shorts farms v4 | Cena de raio/noite muda o mundo: voltar `weather clear`, `time set` e `tick rate 20` antes da próxima tomada. | guia 15 §2 |

| 2026-11-16 | queda (capivara) | Cenário achado no mundo contradiz a narração ("campo de terra" virou um quadradinho na floresta). Construir o cenário pelo roteiro sobre o oceano, com bíblia frase→fato→plano e foto de cima antes de gravar. | guia 16 §2 |
| 2026-11-16 | queda (capivara) | Usuário rejeitou terreno plano: naturalizar com colinas por ruído (máscara que preserva as features) e bosques; esconder o fim do mapa com costa irregular e serra. | guia 16 §2 |
| 2026-11-17 | queda (capivara) | Câmera travada: `tp` por tick vindo do Python treme e `teleport_duration` não suaviza o jogador montado. Velocidade aplicada pelo servidor (datapack, macro `tp ~vx ~vy ~vz`): quadros repetidos 12,5 % → 2 %. | guia 16 §4 |
| 2026-11-17 | queda (capivara) | Rosto do personagem atrasado em relação à cabeça: mandar todas as partes num único `function` (lista em storage). | guia 16 §3 |
| 2026-11-17 | queda (capivara) | "Falta algo para viralizar": personagem próprio em todo plano, ~1 corte por palavra, câmera perto, 1 palavra de legenda, saturação +40 %, −12 LUFS, whoosh. | guia 16 §1 |
| 2026-11-17 | queda (capivara) | Explosão com dezenas de summon dentro do laço de 20 Hz faz o personagem "flutuar"; rodar em thread. `fill` longe da câmera falha sem `forceload` e deixa lixo de takes antigos (buraco antes do pouso). | guia 16 §2 e §4 |
| 2026-11-17 | vaso (capivara) | Capivara tem cabeça larga (`±6.5*U`) e focinho até `+0.62 m`: abrir pivôs dos ombros para `±6.8*U`, posicionar objetos segurados a `0.56 m` à frente (`y_piso + 0.46`) e limitar pitch da cabeça a `≤15°` para braços e objetos não entrarem no focinho/cabeça. | guia 16 §3 / skill vaso-vazio |
| 2026-11-17 | vaso (capivara) | Personagem com `escala != 1.0` exige `ALT_CHAO = 18 * U * escala` (senão afunda no piso); captura determinística via `vision.screenshot` com `/tick rate 3.4` + pré-roll de `0.06 s` entrega 0 % de quadros repetidos mesmo em sessão isolada sem `gfxcapture`. | guia 16 §3 e §4 / skill vaso-vazio |
| 2026-11-17 | vaso (capivara) | Pose sentada em trono exige dobrar joelho em 90° (`_rosto` dividindo coxa e canela) sobre assento `slab[type=bottom]` sem parede frontal; vídeos <60s ganham epílogo narrativo (4 planos) para passar de 1 min e monetizar no TikTok sem perder ritmo; auditar todos os `vXX.mp4` antes do render final. | `skill/vaso-vazio-shorts-3d/SKILL.md` |

## Resultado no YouTube
| Data | Vídeo | Views 48 h | Views 7 d | Retenção média | CTR | Thumb vencedora | O que mudar |
|---|---|---|---|---|---|---|---|

## Pendências do 1º teste
- [ ] Rig de câmera por comando (datapack.py) no jogo — ver `ferramentas/minecraft/README.md`.
- [ ] OBS pelo WebSocket com o OBS aberto.
- [ ] MCP do Minecraft no single player ou em servidor local.
- [ ] Easy NPC + Emotecraft: o emote toca no NPC humanoide?
- [ ] Mineways + MCprep no Blender 5.2 com um mundo real.
- [ ] Ducking da música na voz real (montagem testada só com sons sintéticos): ajustar `ducking`/`volume` no `montagem.json`.
- [ ] Explosão do Blender (`efeitos.py`) parece uma cúpula laranja clara: melhorar antes de usar em luta.
- [ ] Exemplo do documentário: cortar ~250 palavras (está com ~21 min), contar minérios em 5 chunks reais e atualizar os preços (ouro, dólar, ferro).
- [ ] Exemplos de machinima/animação: trocar os nomes de músicas "a definir" pelos reais da biblioteca.

## Técnica conferida em 12/11/2026
| Data | Vídeo | Aprendizado | Virou regra em |
|---|---|---|---|
| 2026-11-12 | testes | Blender 5.2: névoa como volume no World deixa todo quadro preto (Eevee e Cycles). Usar uma caixa grande com material de volume. | `ferramentas/blender/looks.py` |
| 2026-11-12 | testes | ffmpeg 8: `-loop 1`, `-ss/-t` na entrada e `trim` depois de `zoompan` travam o filtro; mudar a cor (bt601/sem tag) no meio reinicia os filtros e some com os efeitos. Normalizar tudo em bt709 e usar `-reinit_filter 0`. | `ferramentas/edicao/montar.py` |
| 2026-11-12 | testes | AAC sobe o pico ~0,3 dB: mirar -1,5 dBTP para sair abaixo de -1. | `ferramentas/edicao/montar.py` |
| 2026-11-12 | 01_luta-ceu-quebrado | 1.21.11 renomeou as gamerules (`advance_time`, `advance_weather`, `spawn_mobs`; antes `doDaylightCycle`...). O `pack_format` 94 vem de `data_major` no `version.json` do server.jar. | `videos/01_luta-ceu-quebrado/mapa/gerar_mapa.py` |
| 2026-11-12 | 01_luta-ceu-quebrado | Pelo MCP, `function_run`/`/function` do datapack responderam "failed", mas `/fill` solto e `block_fill_batch` funcionam: para montar mapa grande, mandar os fills em lote (1500 por chamada), com `forceload` antes. | `videos/01_luta-ceu-quebrado/mapa/README.md` |
| 2026-11-12 | 01_luta-ceu-quebrado | Servidor dedicado pausa sem jogador (`pause-when-empty-seconds=-1` resolve). O jogo pausa ao perder o foco: o `view_capture` só mostra o menu até apertar F3+P ou voltar ao jogo. | guia 06 |

## Short 02 (armaduras) — lições
- Janela do Minecraft parada no "Game Menu": dá para destravar pelo PowerShell (SetForegroundWindow + SendKeys {ESC}); ffmpeg gdigrab `-i title=Minecraft*...` captura a janela em tela cheia sem o MCP.
- AI Studio TTS (novo layout): busca de vozes em "Speaker settings"; "Enzo" existe (grave, "crisp and eager"). 1 Run de ~140 palavras = ~43 s.
- ffmpeg drawtext com `%` no texto: usar `expansion=none`.
- Câmera por `tp` + captura logo depois dá quadros fora de posição; melhor 1 quadro base fixo + crops/zoom no ffmpeg.

## Short 03 (farm de ferro) — lições técnicas (14/11/2026)
Scripts de gravação em `videos/03_farm-de-ferro/gravacao/` (dp.py, gen.py, gen2.py, rec.py, serie2.py); montagem em `videos/03_farm-de-ferro/montagem/`.
- **MCP Chapmanjw tem limite (~1,7 chamadas/s, balde de ~26) e bloqueia `/function`.** Solução: gerar um datapack (`ferro`, namespace `f`) na pasta do mundo, rodar `/reload` e disparar cada função com UMA chamada: `scoreboard players set #run go N` (o `tick.mcfunction` despacha por placar). Sequências temporizadas = `schedule function ... Nt` encadeado.
- `pack.mcmeta` do datapack precisa de `min_format`/`max_format` (94 no 1.21.11). Um `fill` acima de 32768 blocos **falha em silêncio** dentro da função (o terreno não limpava): quebrar em fatias.
- **Câmera sem mod:** jogador montado num `block_display` (`camrig`); ~~`teleport_duration` dá travelling suave com UM `tp`~~ **(errado: o jogador montado não interpola; saía ~10 fps, vídeo travado — ver v3)**; `rotate @p yaw pitch` fixa a direção (não interpola: escolher pose inicial e final com o mesmo ângulo). `spectate` no display NÃO interpola (pula).
- **Sombra do jogador no chão (shader):** `attribute @p minecraft:scale base set 0.0625` + invisibilidade; olho = rig_y + 1,02 × 0,0625.
- A gravação (gfxcapture) tem ~1 s parado antes da ação e o 1º quadro vem com defeito: a montagem detecta o início do movimento e corta antes.
- **Aldeões não geram golem em mundo plano** (testado de dia/noite, tick rate): o golem nasce por comando (`summon`) — vídeo encenado, dizer na descrição. Zumbi do barco fica `Invulnerable` para não queimar antes da hora (e é solto no sol na cena do "Mas").
- Lava vaza pelos portões abertos e vira pedra: refazer a frente do poço (`reset_frente`) antes de cada tomada.
- Nível 2 = `clone` do módulo em fila (z+16, +32, +48; retrato fica melhor em fila do que lado a lado). Nível 3: portal real no overworld; o "lado do Nether" foi **recriado no overworld** (clone do poço + netherrack + tinta roxa na pós) porque a câmera por rig não troca de dimensão.
- Voz Enzo do Gemini no AI Studio via Claude in Chrome (nunca o "Voice Design", que é pago). O Whisper erra "pra/golens/pé de"; casar as palavras ao roteiro com `difflib` e repartir os tempos.
- Trilha: chiptune sintetizado em Python (`montagem/musica.py`), sem direitos autorais; sons de pop/whoosh também sintéticos.

## Short 03 v2 (farm de ferro refeita) — lições (15/11/2026)
- **Golem de aldeão nasce sozinho no Java 1.21.11 se:** o aldeão dormiu nas últimas 24000 ticks, há 3+ aldeões a 10 blocos em pânico, o zumbi está a menos de 8 blocos **e visível** (qualquer bloco com colisão, até vidro, tampa a visão), nenhum golem a 16 blocos, e existe chão firme livre dentro da caixa ±8 em X/Z e ±6 em Y. A farm precisa ficar 7+ blocos acima do terreno e todo topo exposto na caixa precisa ser laje/muro/alçapão.
- **Ordem importa:** deixar os aldeões dormirem SEM zumbi (com zumbi à vista eles ficam em pânico e não dormem); depois de todos terem `last_slept`, pôr o zumbi. Cama colada em cama sem uma célula livre ao lado impede o aldeão de chegar à cama: deixar uma coluna de chão livre.
- Muros de 2 de altura dão chão para o golem nascer em cima do muro: usar muro até y+6 acima do aldeão (topo fora da caixa).
- Água só leva 7 blocos: calha em degraus com fonte nova no topo de cada degrau, fontes cobrindo a largura inteira; sobra de bloco antigo no volume não limpo bagunça o fluxo (limpar a calha inteira antes de reconstruir).
- Golens de 1,4 de largura em canal de 3 blocos às vezes ficam parados nas bordas (não resolvido); os do eixo central fluem bem.
- **Portal do Nether por comando:** `setblock nether_portal[axis=x]` dentro de moldura de obsidiana funciona e `/setblock` não derruba o portal se o chão for tirado (portal sem chão: o golem chega e cai). O portal do Overworld só liga com o do Nether se este estiver à mesma altura (a busca ordena por distância 3D): construir a câmara do Nether em y160, acima do bedrock, em x/8 e z/8. Água por `setblock` funciona no Nether.
- `tp @e[...] x y z` dentro de função manda a entidade para a dimensão de quem executa: câmera no Nether precisa de `execute in minecraft:the_nether run tp`.
- `entity_query` em `@e[type=...]` não filtra por dimensão em alguns campos: ler `dimensionId` no resultado.
- A lava vaza pela coluna aberta do baú: tampar com vidro.
- Gamerules da 1.21.11 mudaram de nome e `gamerule doDaylightCycle` dá erro: o tempo ficou parado (`time set` manda).

## Short 03 v3 (regravação sem travar + voz refeita) — lições (15/11/2026)
- **Câmera travada = o jogador montado não interpola com `teleport_duration`.** Correção: um `tp` + `rotate @p` **a cada tick** (passo=1, ease na posição e no olhar); o cliente interpola entre ticks e o vídeo sai a ~30 fps únicos (antes 10–20, irregulares). Teste: `gravacao/fluidez.py` (fração de quadros que mudam e maior sequência parada); v2 = 46%/22 quadros, v3 = 68%/8.
- **Cadeia de `schedule` maior que a tomada vaza para a próxima:** o `tp @e[tag=camrig]` da cadeia velha pega o rig novo e sequestra a câmera (T23 saiu com a vista do portal). Conferir duração da cadeia ≤ duração da tomada.
- **Janela do Minecraft para gravar em retrato:** cliente 608×1080 com a janela em (0,−32) e 624×1119 (título fora da tela; a parte fora da tela vira faixa preta). Janela sem foco pausa o jogo se `pauseOnLostFocus` estiver ligado (aqui está falso) e o HUD volta a aparecer: apertar F1 (`ferramentas/shorts-farm/keys.py`).
- **Voz cortada/embolada vinha do TTS gerado de uma vez só (287 palavras em 80 s = 255 palavras/min, rápido demais):** palavras engolidas ("bigorna pede" → "a pé de", "entope" → "em top", "pelo criador" → "pesucreador"). Solução: **8 blocos de 3 frases** no AI Studio (Gemini 3.8 Flash TTS, voz Enzo, estilo "pronuncie todas as palavras inteiras"), cada bloco conferido com Whisper (`voz_blocos/checar.py`: casamento com o roteiro, cortes secos), refazendo o bloco ruim; junção com corte de silêncio, fade de 12 ms e pausa de 0,2 s; velocidade final `atempo=1.10`. Palavra que o TTS pronuncia mal ("entope") → trocar no roteiro ("Nada trava").
- AI Studio mudou: a voz fica em "Speaker settings" (buscar "Enzo"), estilo no botão "Style", baixar pelo ícone de download com o player pausado.

## Short 04 (Enterrado vivo, Minecraft 26.3 + MCPFabric) — lições (16/11/2026)
- **MCPFabric** (`127.0.0.1:25599/rpc`, `ferramentas/minecraft/mcpfabric.py`): `command.run` aceita `function f:nome` (sem placar de despacho) e não tem o limite de ~1,7 chamadas/s do MCP antigo. `pack.mcmeta` da 26.3 usa `min_format/max_format 121`; `reload` + `datapack enable "file/NOME"` carrega o pack novo.
- **Comando que dá erro dentro da função aborta o resto, inclusive o `schedule` do próximo tick** (cadeia da câmera morre): `data merge entity @e[...]` com mais de uma entidade dá erro → usar `execute as @e[...] run data merge entity @s {...}`.
- `falling_block` por comando na 26.3 renderiza como areia (ignora o BlockState): para desabamento usar `block_display` com `start_interpolation`/`transformation.translation`, e depois `fill`. Terra sobre terra não aparece: contrastar (cascalho).
- Tábua `dark_oak` é escura demais para POV: usar abeto + `light[level=15]`; tábua clara de bétula marca o "ponto fraco".
- Texto 3D: `text_display` com `text:{text:...,color:...}` e `transformation.scale`. (Personagem deitado: ver a regra no CLAUDE.md.)
- Onde o jogo começa na tomada: ~0,5 s depois do início do arquivo (a montagem usa onset fixo de 0,5 s).
- TTS: blocos de 2–3 frases conferidos com Whisper; 6 blocos, `atempo 1.10` → 82 s (precisa de >1 min para monetizar no TikTok).
- **Nuvens da 26.3 ficam em y≈192:** cenário em y≈200 deixava uma faixa cinza no topo do quadro. Montar o cenário abaixo delas (y≈140) resolve sem mexer nas opções (clique por PostMessage não aciona botões de menu; `ui.*` do MCPFabric vem desligado no config).
- Poço em 1ª pessoa: `light` nível 10–14 nos blocos já cavados (sem isso o POV fica preto).
- **Câmera olhando para +z (sul): o leste (+x) aparece à ESQUERDA.** A cabeça da Alex estava do lado oposto ao buraco; `Rotation:[180f,0f]` no manequim deitado pôs a cabeça embaixo da tábua fraca.
- **Personagem "morto":** animar o manequim com `tp ... 180 0` a cada 2 ticks, **só no eixo y** (respira, ofega, se debate, trancos ritmados); sem `/damage` (o manequim fica `Invulnerable:1b`). Movimento em x/z gira o corpo (o yaw do corpo segue o deslocamento) e ele sai atravessado do caixão; essa rotação fica de uma tomada para a outra, então recriar o manequim (`kill` + `summon`) em cada reset.
- **Ilha flutuante:** o corte precisa ser grande (aqui 49×25 blocos, com deepslate até 46 blocos abaixo da grama) para nenhum plano mostrar o chão real nem as bordas. `fill` acima de 32768 blocos falha calado: dividir.
- **Manequim deitado (regra no CLAUDE.md e em `ferramentas/minecraft/deitado.py`):** a posição é a dos pés; o corpo vai ~1,8 × escala na direção do yaw (0 −x, 90 +z, 180 +x, 270 −z). Centralizar a entidade no caixão punha a cabeça dentro da parede. A luz vem do bloco dos pés (bloco ali = personagem preto e sufocando).
- **Final sem som no "Você conseguiu":** o `Achievement.mp3` do pacote tem 3 s de silêncio no começo; cortado em 2,2 s, sobrava só silêncio, e o `loudnorm` virava isso num deslocamento DC (−0,84) que esmagava o fim do mix. Correção na montagem: pular o silêncio inicial do SFX (3º campo no catálogo), `highpass` em cada efeito e depois da normalização final. Antes de usar um SFX novo, medir onde começa o som. Vídeo ganhou 2 s de cauda depois da última frase.
