# Cenas — SALVAMOS A PASTELARIA DA VÓ (EP. 1)
Mundo de gravação: vila_pastel · Versão: Fabric 1.21.11 (Pilha A do guia 12 §3) · Look (formato 3): — (formato 2, jogo sem shader pesado)

## 0. Montagem fixa da série (fazer 1 vez, salvar como estrutura, reusar em todo episódio)
Legenda dos planos:
- **POV-A** = 1ª pessoa do Toco jogada **ao vivo** por você (mão e HUD na tela), com a voz-guia do roteiro tocando no fone. Use quando o Toco faz algo com as mãos (fritar, pular, quebrar, andar de carrinho).
- **POV-T** = 1ª pessoa no **trilho**: o datapack move o jogador com `/tp @p x y z facing ...` a cada tick (mão e HUD aparecem; HUD ligado, sem F1).
- **NOVELA** = rig de câmera do `ferramentas/minecraft/datapack.py` (text_display + `/ride`, F1 ligado, sem HUD). A cena roda de novo, igual, para cada ângulo (guia 12 §4). O Toco aparece como **TOCO-dublê** (Easy NPC com `skins/toco.png`). ⚠️ rig ainda não testado no jogo: plano B = Flashback.
- Todas as fichas usam os nomes genéricos de emote do guia 09; o Claude troca pelos comandos reais do Easy NPC/Emotecraft na instalação.

Mapa (`/gamerule doDaylightCycle false` — na 1.21.11 a regra pode ter outro nome, conferir com Tab · `/gamerule doMobSpawning false` · `/weather clear`):
| Lugar | Onde | Como montar |
|---|---|---|
| Praça | piso de 31×31 centrado em 0 63 0 | `/fill -15 63 -15 15 63 15 minecraft:polished_andesite` + borda de `stone_bricks`, 4 postes com `lantern` |
| Pastelaria | caixa de -5 64 10 a 5 69 17, porta em 0 64 10 (frente para a praça, −Z) | paredes `white_terracotta` + cantos `stripped_oak_log`, telhado de `orange_terracotta` em y 70, toldo de `orange_wool`/`white_wool` listrado em z 9 |
| Placa | `text_display` em 0 71 9.4 virado para −Z | `text:{"text":"PASTELARIA DA VÓ CIDA","color":"gold","bold":true}`, `background:-1442840576`, `scale:[2,2,2]`, tag `placa` |
| Escada | `ladder` em 3 64 9 até 3 69 9 | Guga segura em 3 64 8 |
| Balcão | z 11, de -3 a 3, `smooth_quartz_slab` em cima de `oak_planks` (ou balcão do Macaw's) | caixa registradora = `item_display` de `minecraft:lodestone` em 2 65.1 11 |
| Baú do dinheiro | `chest` em 2 64 13 (atrás do balcão) | tag do bloco nada; o conteúdo é só visual |
| Buraco do chão | `-1 64 12` = ar, com `brown_carpet` em volta; embaixo, túnel de 1×2 descendo até a toca | o pastel cai aqui no C012 |
| Mesa da massa | `-3 64 14` (Macaw's table) + `item_display` de massa (`white_carpet` achatado) | |
| Tacho | `water_cauldron[level=3]` em 0 64 15 em cima de `campfire` em 0 63 15 | partícula `bubble_pop` + `smoke` quando frita |
| Cadeira da Vó | cadeira de balanço do Macaw's em 4 64 15, virada para o balcão | |
| Banco da praça | `oak_stairs` em 8 64 -6 e 9 64 -6 + `oak_leaves` de uma árvore ao lado (`/place feature minecraft:oak` em 11 64 -6) | |
| Torre Dourada | base 7×7 de 27 64 -23 a 33 88 -17, `gold_block` + `yellow_stained_glass`, porta em 30 64 -17 | janelinha 1×1 aberta em 33 66 -20; tapete `yellow_carpet` de 28 64 -21 a 32 64 -21; cofre = sala 3×3 em 28 64 -23 com `chest` dourado (pacote) e 6 `gold_block` |
| Vila | `/place structure minecraft:village_plains 0 64 70` | aldeões figurantes ficam na fila, não andam (NoAI) |
| Trilho | saída lateral 6 64 13 → volta pela vila → **rampa sem fim** em -28 67 26 apontando para o lago | `powered_rail` a cada 8 blocos + `redstone_block` embaixo |
| Lago | -45 60 20 a -30 62 40, `water` | |
| Toca da raposa | sala de -4 56 11 a 4 61 17 embaixo da pastelaria + túnel 1×2 para leste até 20 58 14 | chão de `coarse_dirt`, `rooted_dirt`, raízes `hanging_roots`; tesouro abaixo |

Tesouro da toca (montado só no C034; antes fica vazio): 6 `emerald_block` + pilhas de `item_display` de `emerald` (scale 2), 6 `gold_block`, `bell` em 0 57 15, 12 `item_display` de pastel, 2 `golden_helmet` (as "coroas") e 1 `glass_pane` com moldura (o "espelho").

Pacote de textura do canal (`vila_recursos`): modelos `vila:pastel` (meia-lua amarela com marcas de garfo), `vila:pastel_queimado` (preto), `vila:caderno` (caderninho verde-água), `vila:bengala`, `vila:contrato` (papel dourado). Itens: `/give @p minecraft:bread[minecraft:item_model="vila:pastel",minecraft:item_name="Pastel"]`.

HUD da gincana (função `vila:hud/iniciar`, roda 1 vez no C006):
```
/scoreboard objectives add placar dummy {"text":"PASTELARIA DA VÓ","color":"gold","bold":true}
/scoreboard objectives setdisplay sidebar placar
/scoreboard players set Esmeraldas placar 0
/scoreboard players set Meta placar 1000
/bossbar add vila:sol {"text":"☀ PÔR DO SOL","color":"yellow"}
/bossbar set vila:sol max 100
/bossbar set vila:sol value 100
/bossbar set vila:sol style notched_10
/bossbar set vila:sol players @a
/title @a times 3 25 8
```
Toda ficha diz **HUD:** o número do placar e do sol na cena. "+10" = `/title @a subtitle {"text":"+10","color":"green"}` + `/title @a title ""` + som `entity.experience_orb.pickup` + ka-ching (Freesound CC0 `cash register`). O placar e o sol são **da história**, não do relógio: cada cena começa com os valores da ficha.

Nomes em cima da cabeça: ligados, na cor-assinatura (`CustomNameVisible`), estilo gincana. Ex.: Easy NPC "Nina" com nome verde-água.

Legenda: só **frases-chave**, em fonte Lilita One, na cor de quem fala, com pop (lista em "texto na tela"). Música: mix voz 100% · efeitos 60% · música 20–30%; a música some nas falas importantes (guia 12 §0).

---

### C001 — F001–F006
tipo: jogo
mundo: vila_pastel
local: telhado da pastelaria, Toco em 2 70 11 · overworld · hora `/time set 1000` (manhã) · sol, sem chuva · tick congelado: não
cenário:
  - placa nova (`text_display` tag `placa`) ainda **na mão**: `item_display` de `oak_sign` grande em 2 70.6 10.5
  - escada `ladder` em 3 64..69 9
elenco:
  - TOCO: jogador (POV-A), em pé no telhado, olhando para baixo, para o Guga
  - GUGA: Easy NPC skin guga.png, em 3 64 8, pose segurando a escada (braço direito esticado), pastel na mão esquerda (`item replace ... weapon.offhand`)
ações (tempo a partir do início da F001):
  +0,0  TOCO segura a placa (item na mão), olha para o Guga
  F002 início  GUGA emote: wave com a mão do pastel (a escada balança: `ladder` some e volta 1 bloco, 2 vezes)
  F004 início  GUGA emote: eat + som `entity.generic.eat` ×3
  F006 fim  GUGA emote: shrug
planos:
  F001–F006  POV-A de cima para baixo (pitch 50), o Guga pequeno lá embaixo
  F003  corte de 1,5 s: NOVELA close do Guga mastigando, contra-plongée leve (reação)
câmera:
  movimento: POV-A livre; o close é estática
  de: 3 65.6 6.5 · yaw 0 · pitch -10   →   para: igual
  duração: 1,5 s
efeitos (pós): nenhum
texto na tela: "TESTANDO." (amarelo-mostarda, pop) em F004
som: passarinhos (ambiente de manhã) · mastigada · música: "Monkeys Spinning Monkeys" (Kevin MacLeod, CC BY 4.0) entra baixa em F001

### C002 — F007–F010 (+ pausa de cena 3 s)
tipo: jogo
mundo: vila_pastel
local: frente da pastelaria · hora 1000 · tick congelado: não
cenário:
  - igual ao C001
elenco:
  - CREEPER: `creeper` NoAI, em 4 64 7, atrás do Guga, olhando para ele
  - GUGA: igual
  - TOCO: jogador (POV-A) no telhado; TOCO-dublê nos planos de novela
ações (tempo a partir do início da F007):
  +0,0  som `entity.creeper.primed` (e repete a cada 1,5 s até a explosão)
  F008 início  GUGA vira a cabeça para a esquerda, depois direita (0,4 s cada)
  F009 início  CREEPER infla: `/data merge entity @e[type=creeper,limit=1] {ignited:1b}` (não explode: o datapack mata antes)
  F010 início  TOCO pula do telhado (POV-A: pular para frente, cair em 2 64 7 em cima de feno `hay_block` escondido), empurra o Guga
  F010 fim +0,3  GUGA vai para 0 64 6 (`/tp` em arco, 0,5 s) · CREEPER `/kill` + `/particle explosion_emitter 4 65 7` + som `entity.generic.explode`
  F010 fim +0,4  placa: `/data merge entity @e[tag=placa,limit=1] {text:{"text":"PASTEL... A VÓ","color":"gold","bold":true}}` + `/particle smoke 0 71 9 1 0.5 0.2 0.02 60`
planos:
  F007  POV-A olhando o creeper atrás do Guga (descobre)
  F008  NOVELA plano médio do Guga olhando para os lados, o creeper atrás dele (piada visual)
  F009  POV-A: o Toco corre na beira do telhado
  F010  NOVELA plano geral da fachada: o TOCO-dublê pula do telhado (corte na ação: pulo começa no POV e termina aqui)
  pausa  NOVELA plano geral, explosão; câmera lenta 50% na edição por 1 s; fumaça baixando
câmera:
  movimento: estática no plano geral; tremida no pós
  de: 0 66 -8 · yaw 0 · pitch 10   →   para: igual
  duração: F010 até o fim da pausa
efeitos (pós): flash 2 quadros + tremida @ F010 fim +0,3 s · câmera lenta 1 s
texto na tela: —
som: chiado do creeper · whoosh do pulo · BOOM com cauda · música corta seco na explosão (silêncio 0,5 s) e volta

### C003 — F011–F013 (+ reação: GUGA)
tipo: jogo
mundo: vila_pastel
local: frente da pastelaria, fumaça baixando · hora 1000
cenário:
  - `hay_block` some; placa já mostra "PASTEL... A VÓ"; escada derrubada: `ladder` some, 3 `item_display` de escada caídos no chão em 3 64 7
elenco:
  - GUGA: deitado (pose sleeping/Easy NPC deitado) em 0 64 6, pastel no peito
  - NINA: Easy NPC skin nina.png, chega correndo de 6 64 -4 até 2 64 5 (1,2 s), caderno na mão
  - TOCO: POV-A de pé ao lado do Guga
ações (tempo a partir do início da F011):
  +0,0  GUGA senta (pose sentado), levanta o pastel: partícula `happy_villager`
  F012 início  TOCO olha a escada quebrada
  F013 início  NINA emote: point para a placa
  F013 fim  [reação GUGA] GUGA emote: shock, olha a placa
planos:
  F011  POV-A olhando o Guga no chão
  F012  POV-A pan para a escada quebrada
  F013  NOVELA contra-plongée da placa "PASTEL... A VÓ" (plano detalhe), depois close da Nina
  reação  NOVELA close do Guga, 1 s
câmera:
  movimento: tilt para cima na placa
  de: 0 65 4 · yaw 0 · pitch -10   →   para: 0 65 4 · yaw 0 · pitch -35
  duração: F013 inteira
efeitos (pós): nenhum
texto na tela: "PASTEL... A VÓ" já está na placa (nada a mais)
som: tosse de fumaça · "boing" pequeno quando o Guga senta · vinil arranhando no fim da F013

### C004 — F014–F015 (+ pausa de cena 3 s)
tipo: jogo
mundo: vila_pastel
local: praça, a Lorena chega da direção da Torre Dourada · hora 1000
cenário:
  - igual
elenco:
  - LORENA: Easy NPC skin lorena.png, anda de 12 64 -8 até 3 64 3 (3 s), óculos escuros
  - GUGA, NINA: em pé (Guga com o pastel)
ações (tempo a partir do início da F014):
  -2,0  LORENA começa a andar (passos dourados: partícula `wax_on` nos pés)
  F014 início  LORENA emote: clap devagar (3 palmas)
  F015 início  LORENA emote: wave com um braço só, de costas para a turma, olhando a placa
  pausa  LORENA vira e vai até 6 64 4 (fica para a cena seguinte)
planos:
  F014  NOVELA contra-plongée da Lorena chegando (câmera baixa, ela "grande"), dolly in lento
  F015  POV-A: a Lorena acenando para a placa
  pausa  NOVELA plano geral da praça: Torre Dourada brilhando ao fundo + pastelaria queimada (contraste rico × pobre)
câmera:
  movimento: câmera baixa + dolly in
  de: 4 64.3 -2 · yaw 160 · pitch -15   →   para: 4 64.3 0 · yaw 160 · pitch -18
  duração: F014 inteira
efeitos (pós): brilho (glare) nos detalhes dourados
texto na tela: "LORENA" (dourado, pop) em F014 · "TCHAUZINHO, PLACA." em F015
som: passos de salto (Freesound CC0 `high heels`) · "pling" dourado · música: corta a cômica, entra 1 nota grave "dum-dum" (riser curto)

### C005 — F016–F022 (+ pausa de cena 2 s)
tipo: jogo
mundo: vila_pastel
local: frente da pastelaria · hora 1000
cenário:
  - Vó Cida na porta: cadeira de balanço movida para 1 64 9
elenco:
  - LORENA em 3 64 4 · VÓ CIDA (Easy NPC, sentada) em 1 64 9 · NINA em 0 64 5 · GUGA em -1 64 6
ações (tempo a partir do início da F016):
  F016 início  TOCO (POV-A) vira para a câmera... para o espectador: olha a Lorena e depois a torre
  F017 início  LORENA emote: point para o chão da pastelaria
  F018 início  LORENA segura `vila:contrato` (`weapon.mainhand`)
  F018 fim  [reação TOCO] POV-A dá 1 passo para trás
  F019 início  VÓ CIDA emote: talk, mão aberta
  F020 início  LORENA emote: point para a praça inteira (vira 90° em 1 s)
  F021 início  GUGA emote: think
  F022 fim  LORENA vai embora andando até 12 64 -8; NINA emote: angry
planos:
  F016  POV-A: pan da Lorena até a Torre Dourada ao fundo
  F017–F018  NOVELA sobre o ombro do TOCO-dublê → Lorena (plano médio)
  F018  plano detalhe: o contrato dourado com "1000" (gravar o `item_display` do contrato bem perto)
  F019  NOVELA close da Vó, sobre o ombro da Lorena (campo/contracampo; regra dos 180°: a Lorena sempre à direita da tela)
  F020  NOVELA sobre o ombro da Vó → Lorena
  F021  POV-A no Guga
  F022  NOVELA close da Lorena; pausa: plano geral, ela indo embora
câmera:
  movimento: estática nos closes; dolly out na pausa
  de: 1 65.5 6 · yaw 200 · pitch 0   →   para: 1 66 2 · yaw 200 · pitch 5
  duração: pausa
efeitos (pós): nenhum
texto na tela: "1000 ESMERALDAS" (verde, grande, pop) em F018 · "ATÉ O PÔR DO SOL" (amarelo) logo abaixo · "ESTACIONAMENTO DOURADO?" em F020
som: papel abrindo · "dun dun DUN" curto em F018 · ka-ching triste em F019 · música tensa leve (Audio Library `quirky suspense`)

### C006 — F023–F031 (+ pausa de cena 3 s)
tipo: jogo
mundo: vila_pastel
local: frente da pastelaria · hora 1000
cenário:
  - roda `vila:hud/iniciar` em F029 início (placar e sol aparecem na tela)
elenco:
  - VÓ CIDA sentada · NINA · GUGA · TOCO (POV-A)
ações (tempo a partir do início da F023):
  F023 início  TOCO olha a Vó
  F024 início  VÓ CIDA emote: sad, mão no joelho (cabeça baixa)
  F025 início  NINA emote: think → F026 início abre o caderno (item `vila:caderno`)
  F027 início  GUGA levanta o pastel
  F028 início  NINA emote: shrug
  F029 início  NINA emote: point para o canto (placar) e depois para o céu (sol)
  F031 início  TOCO (POV-A) levanta o braço; NINA e GUGA emote: cheer
planos:
  F023–F025  POV-A, a turma na frente da Vó
  F026  NOVELA close da Nina com o caderno (plano médio), dolly in
  F027–F028  POV-A Guga → Nina (pingue-pongue rápido)
  F029–F030  POV-A olhando o placar aparecer; F030 o Toco olha para a câmera do espectador (fala "você")
  F031 + pausa  NOVELA plano geral, os 3 com o braço para cima, a Vó sorrindo; drone subindo e mostrando o sol
câmera:
  movimento: revelação (sobe por trás da turma até ver o sol)
  de: 0 65 3 · yaw 180 · pitch 0   →   para: 0 75 -2 · yaw 180 · pitch -25
  duração: F031 + pausa
efeitos (pós): nenhum
texto na tela: "100 PASTÉIS" (pop) em F026 · "META: 1000" em F029 · "DÁ RUIM, MAS DÁ CERTO!" (laranja) em F031
som: "ding" quando o placar aparece · riser + "tchan" no fim · música: "Monkeys Spinning Monkeys" volta, mais alta na pausa
HUD: Esmeraldas 0 · Meta 1000 · sol 100

### C007 — F032–F037
tipo: jogo
mundo: vila_pastel
local: dentro da pastelaria, cozinha · hora 2000
cenário:
  - massa na mesa (`item_display` `white_carpet` scale [0.8,0.1,0.8]) em -3 65 14
  - tacho fervendo: `/particle bubble_pop 0 65.1 15 0.2 0 0.2 0 3` a cada 10 ticks
elenco:
  - VÓ CIDA sentada na cadeira em 4 64 15 · GUGA em -2 64 13 com pastel · NINA no balcão 1 64 12 · TOCO (POV-A) na mesa
ações (tempo a partir do início da F032):
  F033 início  VÓ CIDA emote: point para a mesa
  F034 início  TOCO (POV-A) "monta" o pastel: clica na mesa 3 vezes (o `item_display` troca: massa → massa+recheio → pastel)
  F036 início  VÓ CIDA vira a cabeça para o Guga, emote: angry curto (1 s)
  F037 início  GUGA emote: eat, recheio na boca (partícula `item{item:"minecraft:yellow_dye"}` saindo)
planos:
  F032–F035  POV-A na mesa, mão montando o pastel
  F036  NOVELA plano médio da Vó apontando, Guga no fundo comendo
  F037  NOVELA close do Guga (reação)
câmera:
  movimento: estática
  de: 2 65.6 14 · yaw 90 · pitch 5   →   para: igual
  duração: F036–F037
efeitos (pós): nenhum
texto na tela: "NADA DE PRESSA" (roxo-lilás) em F034
som: chiado de fritura · tic tic do garfo · mastigada do Guga · música cômica baixa
HUD: Esmeraldas 0 · sol 95

### C008 — F038–F043
tipo: jogo
mundo: vila_pastel
local: balcão da pastelaria · hora 2500
cenário:
  - igual · fila: 10 aldeões de 0 64 9 até 0 64 -2 (ver C009)
elenco:
  - ALDEÃO 1 (`villager` farmer, NoAI) no balcão em 0 64 10 · NINA atrás do balcão · TOCO (POV-A)
ações (tempo a partir do início da F038):
  F038 início  NINA emote: point para o aldeão
  F039 início  TOCO entrega o pastel (POV-A: clica no aldeão; `item_display` do pastel vai da mão até o aldeão em 0,4 s)
  F039 fim  ALDEÃO som `entity.villager.yes` + `happy_villager`
  F040 início  "+10" na tela
  F041 início  NINA mostra o caderno (emote: point para o caderno)
  F042 início  GUGA emote: laugh
  F043 início  NINA emote: shrug
planos:
  F038–F040  POV-A no balcão
  F041–F043  NOVELA plano médio Nina + Guga (2 personagens), câmera de lado
câmera:
  movimento: travelling curto da Nina até o Guga
  de: 3 65.5 11 · yaw 90 · pitch 0   →   para: 3 65.5 12.5 · yaw 90 · pitch 0
  duração: F041–F043
efeitos (pós): nenhum
texto na tela: "+10" (verde, pop) em F040 · "ESPIRROS: 12" (verde-água) em F043
som: ka-ching + `entity.experience_orb.pickup` no +10 · espirro (Freesound CC0 `sneeze`) em F042
HUD: Esmeraldas 0 → 10 · sol 92

### C009 — F044–F049
tipo: jogo
mundo: vila_pastel
local: balcão olhando para a praça · hora 3000
cenário:
  - fila de 10 aldeões (profissões variadas) de 0 64 9 a 0 64 -2, NoAI, olhando para o balcão
  - ZUMBI DE CAPACETE em 1 64 -3 (`zombie` NoAI + `item replace entity @e[type=zombie,limit=1] armor.head with iron_helmet`)
elenco:
  - GUGA ao lado do balcão · ALDEÃOZINHO (`villager` com `Age:-24000`) no balcão · TOCO (POV-A)
ações (tempo a partir do início da F044):
  F044 início  GUGA emote: point para a fila
  F046 início  ZUMBI bate no capacete (som `entity.zombie.attack_iron_door` bem baixo)
  F047 início  ALDEÃOZINHO pula 2 vezes
  F049 início  TOCO "fecha" o pastel vazio; som de "fuu" de ar; ALDEÃOZINHO `happy_villager`; "+10"
planos:
  F044  POV-A: pan pela fila inteira até o zumbi no fim
  F045–F046  NOVELA close do zumbi de capacete, contra-plongée (piada: zumbi "esperto")
  F047–F049  POV-A no balcão, aldeãozinho pulando
câmera:
  movimento: dolly in lento no zumbi
  de: 1 64.8 -6 · yaw 0 · pitch -5   →   para: 1 64.8 -5 · yaw 0 · pitch -5
  duração: F045–F046
efeitos (pós): nenhum
texto na tela: "PASTEL DE VENTO" (pop) em F047 · "+10" em F049
som: "plim" do capacete · sopro de ar · ka-ching
HUD: Esmeraldas 10 → 20 · sol 90

### C010 — F050–F055
tipo: jogo
mundo: vila_pastel
local: tacho e balcão · hora 3500
cenário:
  - tacho com fogo alto: `/particle flame 0 65.2 15 0.2 0.1 0.2 0 10` + `large_smoke`
elenco:
  - VÓ CIDA sentada · GUGA · NINA · ZUMBI DE CAPACETE agora no balcão em 0 64 10
ações (tempo a partir do início da F050):
  F050 início  TOCO (POV-A) clica rápido no tacho (5 cliques em 2 s)
  F051 início  VÓ CIDA emote: angry curto, cabeça inclinada
  F052 início  item na mão vira `vila:pastel_queimado` + fumaça preta
  F053 início  ZUMBI estende o braço (pose de zumbi), `item_display` de `carrot` aparece no balcão; som `entity.zombie.ambient` "feliz"
  F054 início  NINA emote: shrug
  F055 início  TOCO pega a cenoura
planos:
  F050  POV-A tacho, mão rápida
  F051  NOVELA close da Vó (bronca), 2 s
  F052  POV-A olhando o pastel preto na mão
  F053–F055  NOVELA plano médio zumbi + Nina no balcão (campo/contracampo com o TOCO-dublê)
câmera:
  movimento: estática
  de: -1 65.5 12.5 · yaw 200 · pitch 0   →   para: igual
  duração: F053–F055
efeitos (pós): tela tingida de preto 2 quadros quando o pastel queima
texto na tela: "CARVÃO." (preto com contorno branco) em F052 · "CENOURA ≠ ESMERALDA" em F054
som: fritura alta → "fssss" + "poof" · vinil arranhando em F052 · grunhido de zumbi contente
HUD: Esmeraldas 20 (não muda) · sol 88

### C011 — F056–F063
tipo: jogo
mundo: vila_pastel
local: balcão · hora 4000
cenário:
  - igual
elenco:
  - BIBLIOTECÁRIA (`villager` librarian) no balcão · CREEPER (NoAI) na fila em 0 64 6, 3 lugares atrás · NINA · GUGA
ações (tempo a partir do início da F056):
  F057 início  TOCO entrega o pastel; "+10"
  F058 início  GUGA emote: shock, aponta para a fila; som `entity.creeper.primed` curto
  F059 início  os aldeões da fila dão 1 passo para o lado (`/tp` ~0.8 em X), o CREEPER anda até o balcão (2 s)
  F060 início  `item_display` de `gunpowder` no balcão; NINA emote: shrug
  F061 início  TOCO entrega o pastel ao creeper bem devagar; CREEPER vai embora andando de costas
  F062 início  NINA anota (emote: think)
planos:
  F056–F057  POV-A balcão
  F058–F059  NOVELA plano geral da fila abrindo caminho para o creeper (piada visual)
  F060–F061  POV-A, o creeper no balcão, bem perto
  F062–F063  NOVELA plano detalhe do caderno: "creeper: 1 pastel, pólvora :(" (textura do caderno trocada)
câmera:
  movimento: estática no plano geral; dolly in no caderno
  de: -4 66 2 · yaw 300 · pitch 15   →   para: igual
  duração: F058–F059
efeitos (pós): nenhum
texto na tela: "+10" em F057 · "PAGO EM PÓLVORA" em F060
som: chiado curto · passos dos aldeões · "glup" do Toco · música para 1 s quando o creeper chega
HUD: Esmeraldas 20 → 30 · sol 86

### C012 — F064–F068 (+ pausa de cena 3 s)
tipo: jogo
mundo: vila_pastel
local: atrás do balcão, buraco do chão em -1 64 12 · hora 4500
cenário:
  - buraco aberto; embaixo, túnel escuro
  - **Easter egg (pago na F137):** o rabo da raposa aparece no buraco por 8 quadros em F067 (fox `NoAI` em -1 62.6 12 e some com `/tp` para a toca)
elenco:
  - GUGA ao lado do buraco · NINA · DUQUESA (só o rabo, 0,4 s)
ações (tempo a partir do início da F064):
  F064 início  GUGA deixa cair o pastel: `item_display` cai no buraco em 0,6 s (some em y 62)
  F066 início  GUGA emote: point para baixo
  F067 início  som `entity.fox.ambient` (o "ié-ié") 2 vezes, baixo e com eco
  F068 início  TOCO (POV-A) vira para o tacho
  pausa  MONTAGEM: 6 planos rápidos de 0,5 s (pastéis saindo, aldeões pagando, "+10" em cascata)
planos:
  F064–F066  POV-A olhando para baixo (pitch 70), o buraco
  F067  NOVELA close da Nina, cabeça inclinada (ouvindo) — no fundo, o rabo no buraco
  F068  POV-A pan para o tacho
  pausa  montagem POV-A + NOVELA geral do balcão com a fila andando (`/tp` em sequência)
câmera:
  movimento: estática
  de: 0 65.4 13.5 · yaw 120 · pitch 5   →   para: igual
  duração: F067
efeitos (pós): nenhum na F067 (a pista tem de ser discreta) · na montagem, "+10" pulando
texto na tela: "+10 +10 +10" na montagem
som: "ploft" do pastel caindo · eco do "ié-ié" · música acelera na montagem · ka-ching a cada +10
HUD: Esmeraldas 30 → 150 (sobe durante a montagem) · sol 80

### C013 — F069–F072 (+ pausa de cena 2 s)
tipo: jogo
mundo: vila_pastel
local: balcão vazio, fim da fila · hora 5000
elenco:
  - NINA com o caderno · GUGA com o pastel de emergência
ações (tempo a partir do início da F069):
  F069 início  NINA emote: point para o placar
  F070 início  GUGA guarda o pastel no "bolso" (`item_display` some com `/tp` para dentro do corpo) e dá 2 tapinhas na barriga
  F072 início  GUGA olha para longe, sério (cabeça 20° para cima)
planos:
  F069  POV-A no placar e na Nina
  F070–F071  NOVELA plano médio Guga + Nina
  F072  NOVELA close do Guga com dolly in lento + música dramática de brincadeira
câmera:
  movimento: dolly in
  de: -3 65.6 9 · yaw 330 · pitch 0   →   para: -2.2 65.6 10.2 · yaw 330 · pitch 0
  duração: F072 + pausa
efeitos (pós): vinheta escura leve na F072 (drama falso)
texto na tela: "150 / 1000" em F069 · "PASTEL DE EMERGÊNCIA" (amarelo-mostarda) em F070
som: acorde dramático exagerado (Audio Library `dramatic sting`) na F072
HUD: Esmeraldas 150 · sol 78

### C014 — F073–F081 (+ pausas de cena 3 s e 2 s)
tipo: jogo
mundo: vila_pastel
local: praça vazia · hora 5500
cenário:
  - na pausa de 3 s: time-lapse do trilho sendo colocado (`/fill` de `rail` em trechos de 10 blocos, 1 por segundo), de 6 64 13 até a vila
  - carrinho (`minecart`) parado em 6 64 13 com um `bell` em `item_display` em cima
elenco:
  - NINA · GUGA · TOCO (POV-A)
ações (tempo a partir do início da F073):
  F073 início  TOCO olha a praça vazia (pan)
  F074 início  TOCO aponta (POV-A: segura `rail` e mira a vila)
  F075 início  NINA emote: think
  F077 início  placar vai para −50
  F077 fim  [reação GUGA] GUGA emote: shock
  F080 início  `/title @a title {"text":"UPGRADE!","color":"gold"}` + `subtitle "PASTEL EXPRESSO"`
planos:
  F073  POV-A praça vazia, vento
  F074–F076  POV-A Toco/Nina
  F077  POV-A no placar "−50" (zoom no HUD na edição)
  reação  NOVELA close do Guga
  F078–F079  NOVELA plano médio Nina + Guga
  pausa 3 s  NOVELA drone alto acompanhando o trilho crescer pela vila
  F080–F081  POV-A no carrinho com o sino
câmera:
  movimento: drone / sobrevoo
  de: 6 90 13 · yaw 0 · pitch 50   →   para: 6 90 50 · yaw 0 · pitch 50
  duração: pausa de 3 s
efeitos (pós): zoom de edição no "−50" (1,2×) em F077
texto na tela: "−50" (vermelho, tremendo) em F077 · "UPGRADE!" é do jogo (/title), sem texto extra
som: "wah-wah" de trombone em F077 · marteladas no time-lapse · "UPGRADE" = som `ui.toast.challenge_complete`
HUD: Esmeraldas 150 → −50 · sol 74

### C015 — F082–F085 (+ pausa de cena 3 s)
tipo: jogo
mundo: vila_pastel
local: estação do carrinho, lateral da pastelaria · hora 5600
elenco:
  - GUGA entra no carrinho (Easy NPC `/ride` no `minecart` de trás) · NINA fica em pé · TOCO (POV-A) no carrinho da frente
ações (tempo a partir do início da F082):
  F083 início  GUGA pula no carrinho (emote: cheer)
  F084 início  NINA emote: shrug (cruza os braços)
  F085 início  TOCO bate no sino (som `block.bell.use`), carrinho parte (o `powered_rail` liga)
  pausa  carrinho acelerando pela vila
planos:
  F082–F085  POV-A dentro do carrinho
  pausa  POV-A carrinho em alta (gravado ao vivo, 3 tomadas) + NOVELA travelling de lado acompanhando os 2 carrinhos
câmera:
  movimento: travelling
  de: 10 66 20 · yaw 90 · pitch 5   →   para: 10 66 45 · yaw 90 · pitch 5
  duração: pausa
efeitos (pós): linhas de velocidade leves (overlay próprio) na pausa
texto na tela: —
som: sino · `entity.minecart.riding` · música: corrida cômica (Audio Library `funny chase`)
HUD: Esmeraldas −50 · sol 72

### C016 — F086–F088 (+ pausa de cena 3 s)
tipo: jogo
mundo: vila_pastel
local: rampa sem fim em -28 67 26, lago à frente · hora 5800
cenário:
  - rampa de trilho subindo 3 blocos e acabando no ar
elenco:
  - GUGA no carrinho de trás com o pastel para cima · TOCO (POV-A)
ações (tempo a partir do início da F086):
  F086 início  GUGA emote: point para a frente
  F088 início  os carrinhos saem da rampa (física real do jogo) e caem no lago
  F088 fim  splash: `/particle splash -38 62 30 2 1 2 0 200` + `/particle bubble_column_up`
planos:
  F086–F087  POV-A vendo o fim do trilho chegar
  F088  NOVELA plano geral lateral, carrinhos voando (câmera lenta 40% na edição)
  pausa  NOVELA grande plano geral do lago, splash; depois POV-A debaixo d'água 1 s
câmera:
  movimento: estática larga
  de: -30 70 45 · yaw 160 · pitch 15   →   para: igual
  duração: F088 + pausa
efeitos (pós): câmera lenta na saída da rampa · flash branco 2 quadros no splash
texto na tela: "DÁ RUIM..." (laranja) em F088
som: grito dos dois · whoosh · música corta no ar (silêncio 0,6 s) · SPLASH enorme

### C017 — F089–F095
tipo: jogo
mundo: vila_pastel
local: lago, depois a margem · hora 6000 (meio-dia)
cenário:
  - minecart boiando: `item_display` de `minecart` na água balançando (`/tp` +0,1/−0,1 em Y)
  - FERREIRO, PESCADOR e BIBLIOTECÁRIA na margem em -30 63 30
elenco:
  - GUGA na água, só a cabeça e o braço com o pastel para cima (pose do Easy NPC nadando + braço levantado) · NINA chega correndo na margem
ações (tempo a partir do início da F089):
  F091 início  GUGA levanta o pastel como troféu: partícula `happy_villager` em volta
  F093 início  minecart boiando gira devagar
  F094 início  FERREIRO, PESCADOR, BIBLIOTECÁRIA: `entity.villager.yes` em sequência; 3 "+10/+20/+30"
  F095 início  TOCO (POV-A) sai da água, NINA emote: clap
planos:
  F089–F093  POV-A na água, Guga ao lado
  F091  NOVELA close do pastel seco no alto (plano detalhe), contra-plongée com o céu
  F094  NOVELA plano geral da margem com os aldeões
  F095  POV-A
câmera:
  movimento: estática
  de: -36 62.6 29 · yaw 90 · pitch -30   →   para: igual
  duração: F091
efeitos (pós): brilho "de troféu" (estrelinhas) no pastel na F091
texto na tela: "+10 +20 +30" em F094 · "PROPAGANDA!" em F095
som: água · "aaah" de coral de troféu (Freesound CC0 `angelic choir short`) na F091 · ka-ching triplo
HUD: Esmeraldas −50 → 10 · sol 65

### C018 — F096–F099 (+ pausa de cena 3 s)
tipo: jogo
mundo: vila_pastel
local: balcão · hora 6200
cenário:
  - `tellraw` de pedidos chovendo no chat: `/tellraw @a {"text":"[PEDIDO] Casa 7: 2 de queijo","color":"yellow"}` (8 linhas em 2 s)
elenco:
  - BRUXA (`witch`, NoAI) no balcão · GUGA · NINA
ações (tempo a partir do início da F096):
  F097 início  `item_display` de `potion` azul (`potion_contents:{potion:"minecraft:swiftness"}`) no balcão
  F098 início  NINA emote: shock, mão estendida
  F099 início  GUGA bebe (emote: eat) · `/effect give` no NPC não vale para animação: o datapack dobra a velocidade dos `/tp` dele · partícula `effect` azul em volta
planos:
  F096  POV-A no chat cheio de pedidos
  F097  POV-A na bruxa e na poção
  F098  NOVELA close da Nina
  F099  NOVELA plano médio do Guga bebendo, depois tremendo (vibra ±0,05 bloco a cada tick por 0,5 s)
  pausa  Guga sai em disparada (corte na ação)
câmera:
  movimento: estática, tremida na F099
  de: 2 65.5 8.5 · yaw 210 · pitch 0   →   para: igual
  duração: F098–F099
efeitos (pós): tremida + aberração cromática 6 quadros quando ele bebe
texto na tela: "POÇÃO AZUL?" em F097
som: glub glub · "zing" de energia · `entity.witch.celebrate`
HUD: Esmeraldas 10 · sol 62

### C019 — F100–F102 (+ pausa de cena 3 s)
tipo: jogo
mundo: vila_pastel
local: vila inteira (montagem) · hora 6400 → 7000
cenário:
  - casas da vila com aldeões nas portas (NoAI) para receber
elenco:
  - GUGA correndo (velocidade 3×: `/tp` em passos maiores, partícula `cloud` nos pés)
ações (tempo a partir do início da F100):
  F100  GUGA entrega em 4 casas (1 s cada); na 4ª, porta fechada: ele volta de ré
  F101  placar sobe sozinho (+10 a cada 0,3 s)
planos:
  F100  NOVELA 4 planos de 1 s em casas diferentes + 1 plano de ré (cortes rápidos, estilo gincana)
  F101  POV-A olhando o HUD subir
  F102 + pausa  NOVELA drone alto: o rastro de nuvem do Guga cruzando a vila
câmera:
  movimento: drone
  de: 0 95 60 · yaw 0 · pitch 60   →   para: 0 95 80 · yaw 0 · pitch 60
  duração: F102 + pausa
efeitos (pós): avanço rápido 2× e linhas de velocidade nos planos do Guga
texto na tela: "300!" "400!" "500!" junto da fala da Nina em F102
som: whoosh a cada entrega · ka-ching em cascata · música corrida mais rápida (pitch +1)
HUD: Esmeraldas 10 → 590 · sol 55

### C020 — F103–F108 (+ pausa de cena 2 s)
tipo: jogo
mundo: vila_pastel
local: frente da pastelaria · hora 7000
elenco:
  - GUGA deitado no chão, cansado (pose deitado) · NINA · LORENA chega de 12 64 -8 até 4 64 4
ações (tempo a partir do início da F103):
  F103 início  "+10" final → 600; NINA emote: cheer
  F104 início  GUGA levanta só um braço
  F106 início  LORENA emote: clap devagar (ironia)
  F107 início  TOCO (POV-A) acena com a mão: `emote: wave` do TOCO-dublê no plano de novela
  F108 início  LORENA emote: angry + `angry_villager`, bate o pé
planos:
  F103–F105  POV-A Nina e Guga
  F106  NOVELA contra-plongée da Lorena
  F107  NOVELA close do TOCO-dublê acenando, sorrindo (1ª vez que vemos o rosto dele com calma)
  F108 + pausa  NOVELA close da Lorena brava; ela vai embora pisando forte
câmera:
  movimento: estática
  de: 4 64.5 1.5 · yaw 180 · pitch -15   →   para: igual
  duração: F106
efeitos (pós): nenhum
texto na tela: "600!" em F103 · "TCHAUZINHO, LORENA." (laranja) em F107 · "O TCHAUZINHO É MEU!" (dourado, tremendo) em F108
som: risadinha da turma · passos fortes · música cômica
HUD: Esmeraldas 590 → 600 · sol 50

### C021 — F109 (+ pausa de cena 2 s)
tipo: jogo
mundo: vila_pastel
local: atrás do balcão, baú em 2 64 13 · hora 7200
cenário:
  - **Easter egg (pago na F137):** a raposa passa no fundo, atrás da cadeira da Vó, por 0,5 s (de 5 64 16 a 3 64 16), com o rabo laranja
elenco:
  - NINA guarda as esmeraldas no baú · DUQUESA no fundo
ações (tempo a partir do início da F109):
  +0,0  NINA abre o baú (`/data merge` não abre a tampa: usar o som `block.chest.open` + Easy NPC emote: point)
  +1,5  `item_display` de pilha de esmeraldas some dentro do baú
  F109 fim  NINA fecha (som `block.chest.close`), anota no caderno
planos:
  F109  NOVELA plano médio da Nina no baú; raposa passa no fundo, fora de foco
  pausa  plano detalhe do baú fechado, dolly in lento (prenúncio)
câmera:
  movimento: dolly in
  de: 0 65.4 13 · yaw 270 · pitch 10   →   para: 1 65.2 13 · yaw 270 · pitch 15
  duração: pausa
efeitos (pós): nenhum (a raposa não pode ter destaque)
texto na tela: "600 NO BAÚ" (verde-água) em F109
som: baú abrindo/fechando · tilintar · nota grave de suspense na pausa (bem baixa)
HUD: Esmeraldas 600 · sol 48

### C022 — F110–F113 (+ reação: TOCO · pausa de cena 3 s)
tipo: jogo
mundo: vila_pastel
local: atrás do balcão · hora 8000
cenário:
  - baú vazio; 1 pelo laranja = `item_display` de `orange_dye` achatado dentro do baú (aparece no C026)
elenco:
  - NINA no baú · TOCO (POV-A) no tacho com uma bandeja de pastéis
ações (tempo a partir do início da F110):
  F111 início  NINA emote: shock, se afasta do baú 1 bloco
  F111 fim  [reação TOCO] TOCO larga a bandeja: 6 `item_display` de pastel caem no chão
  F113 início  placar de 600 → 0 (ver C023)
planos:
  F110  POV-A no tacho
  F111  NOVELA close da Nina com dolly in lento (frase dramática)
  reação  NOVELA close do TOCO-dublê, os pastéis caindo
  F112–F113  POV-A olhando dentro do baú vazio (pitch 60)
  pausa  NOVELA plongée (câmera alta) da turma em volta do baú: eles pequenos, derrotados
câmera:
  movimento: dolly in (F111) · plongée estática (pausa)
  de: 2 66.2 11.5 · yaw 0 · pitch 15   →   para: 2 65.8 12.3 · yaw 0 · pitch 15
  duração: F111
efeitos (pós): zoom de edição no baú vazio 1,3× · cor esfria (−20% saturação) até o fim do B5
texto na tela: "0" (vermelho, enorme) na pausa
som: música corta seco em F111 · "dun" grave · bandeja caindo · na pausa: "Investigations" (Kevin MacLeod, CC BY 4.0) entra baixa
HUD: Esmeraldas 600 · sol 45

### C023 — F114–F120
tipo: jogo
mundo: vila_pastel
local: pastelaria + cortes para os suspeitos · hora 8000
cenário:
  - "fotos de suspeito": CREEPER parado em 6 64 -2 e ZUMBI DE CAPACETE em -6 64 -2, cada um num plano com fundo liso
elenco:
  - NINA (detetive: caderno na mão) · GUGA · VÓ CIDA · TOCO (POV-A)
ações (tempo a partir do início da F114):
  F114 início  placar cai de 600 para 0 em 1 s (contando para trás, 1 linha por tick)
  F117 início  VÓ CIDA emote: sad
  F118 início  corte: creeper parado; texto "SUSPEITO 1" + carimbo "NÃO TEM MÃO"
  F119 início  corte: zumbi de capacete comendo cenoura; "SUSPEITO 2" + "SÓ CENOURA"
  F120 início  NINA vira devagar para o Guga (1 s)
planos:
  F114  POV-A no HUD
  F115–F116  NOVELA plano médio Guga + Nina
  F117  NOVELA close da Vó
  F118  NOVELA close do creeper, câmera parada (cartela de suspeito)
  F119  NOVELA close do zumbi, idem
  F120  NOVELA dolly in na Nina, olhando para o lado
câmera:
  movimento: dolly in (F120)
  de: 0 65.6 14 · yaw 180 · pitch 0   →   para: 0 65.6 13.2 · yaw 180 · pitch 0
  duração: F120
efeitos (pós): cartelas de suspeito com borda de foto, "carimbo" vermelho com pop
texto na tela: "SUSPEITO 1 / NÃO TEM MÃO" em F118 · "SUSPEITO 2 / SÓ CENOURA" em F119 · "SUSPEITO 3..." em F120
som: contador descendo (`counter ticking`) · carimbo (Freesound CC0 `stamp`) · música de mistério leve
HUD: Esmeraldas 600 → 0 · sol 44

### C024 — F121–F126 (+ reação: TOCO · pausa de cena 3 s)
tipo: jogo
mundo: vila_pastel
local: atrás do balcão · hora 8200
elenco:
  - GUGA com farelo (partícula `item{item:"minecraft:bread"}` caindo dele) · NINA · TOCO (POV-A)
ações (tempo a partir do início da F121):
  F121 início  NINA, VÓ e TOCO viram a cabeça para o Guga ao mesmo tempo
  F123 início  GUGA emote: angry, aponta para a própria roupa
  F124 início  NINA emote: point para o Guga
  F125 início  GUGA emote: sad
  reação  TOCO-dublê baixa a cabeça
  F126 fim  GUGA sai andando devagar até o banco da praça (8 64 -6), 4 s; senta
planos:
  F121  NOVELA plano geral: os 3 olhando para o Guga (ele sozinho do outro lado da tela)
  F122  POV-A no Guga
  F123  NOVELA close do Guga, sobre o ombro da Nina
  F124  NOVELA close da Nina, sobre o ombro do Guga (campo/contracampo; Guga sempre à esquerda)
  F125  NOVELA close do Guga com dolly in
  reação  NOVELA close do TOCO-dublê
  F126 + pausa  NOVELA grande plano geral: o Guga atravessando a praça vazia até o banco, câmera alta (plongée), sozinho
câmera:
  movimento: grua subindo devagar
  de: 2 66 8 · yaw 160 · pitch 10   →   para: 2 76 6 · yaw 160 · pitch 35
  duração: F126 + pausa
efeitos (pós): saturação −30% na pausa
texto na tela: "EU NÃO ROUBO NINGUÉM." (amarelo-mostarda) em F126
som: música de mistério sai; na F125 entra piano triste (Scott Buckley, faixa calma de piano, CC BY 4.0) · passos lentos · vento

### C025 — F127–F130
tipo: jogo
mundo: vila_pastel
local: atrás do balcão · hora 8300
elenco:
  - NINA · VÓ CIDA · TOCO (POV-A); ao fundo, pela porta, o Guga pequeno no banco
ações (tempo a partir do início da F127):
  F127 início  TOCO olha pela porta (pan)
  F129 início  VÓ CIDA emote: talk, sério
  F130 início  TOCO-dublê emote: sad
planos:
  F127  POV-A pela porta: Guga no banco, longe
  F128  NOVELA close da Nina
  F129  NOVELA close da Vó, câmera baixa
  F130  NOVELA close do TOCO-dublê
câmera:
  movimento: estática
  de: 3 65.5 13 · yaw 120 · pitch 0   →   para: igual
  duração: F129
efeitos (pós): saturação −30% continua
texto na tela: —
som: piano continua baixo

### C026 — F131–F137 (+ pausas de cena 3 s e 2 s)
tipo: jogo
mundo: vila_pastel
local: baú → praça → Torre Dourada · hora 8400
cenário:
  - pelo laranja dentro do baú (`item_display` `orange_dye`)
  - DUQUESA em 2 64 -2 com esmeralda na boca: `/item replace entity @e[type=fox,limit=1] weapon.mainhand with minecraft:emerald`
elenco:
  - NINA · TOCO (POV-A) · DUQUESA correndo de 2 64 -2 até a janelinha da torre em 33 66 -20 (6 s, pulo final de 2 blocos)
ações (tempo a partir do início da F131):
  F131 início  NINA pega o pelo (emote: point)
  F133 início  som `entity.fox.ambient` longe
  F134 início  DUQUESA aparece na praça, para, olha para a câmera (2 s), e corre
  F136 início  DUQUESA pula na janelinha da torre e some
  F137 início  TOCO (POV-A) vira para quem assiste (olha para a câmera, pitch 0)
  pausa 2 s  replay rápido: os 2 easter eggs (rabo no buraco no C012, raposa atrás da Vó no C021) com círculo vermelho
planos:
  F131–F132  POV-A no pelo laranja (plano detalhe)
  F133  NOVELA close da Nina, ouvindo
  F134  POV-A: a raposa na praça com a esmeralda (zoom de edição)
  F135  NOVELA plano geral: a raposa correndo até a torre
  F136 + pausa  NOVELA contra-plongée da Torre Dourada, dolly in na janelinha; música de virada
  F137 + pausa  POV-A + replay dos easter eggs
câmera:
  movimento: dolly in na torre
  de: 20 66 -5 · yaw 135 · pitch -20   →   para: 26 68 -12 · yaw 135 · pitch -15
  duração: F136 + pausa de 3 s
efeitos (pós): círculo vermelho + seta (thumb.py / overlay) no replay · cor volta ao normal na F134 (energia volta)
texto na tela: "PELO LARANJA?" em F131 · "FOI A LORENA?!" (laranja, grande) em F136 · "VOCÊ VIU?" em F137
som: "ié-ié" · riser · "dun dun DUN" na F136 · rewind (`tape rewind`) no replay
HUD: Esmeraldas 0 · sol 40

### C027 — F138–F143 (+ pausas de cena 3 s e 2 s)
tipo: jogo
mundo: vila_pastel
local: banco da praça em 8 64 -6 · hora 9000 (tarde, luz dourada)
elenco:
  - GUGA sentado no banco (pose sentado) · TOCO-dublê e NINA chegam e sentam ao lado
ações (tempo a partir do início da F138):
  F138 + pausa  TOCO (POV-A) atravessa a praça até o banco
  F139 início  TOCO-dublê senta ao lado do Guga
  F140 início  NINA emote: sad, cabeça baixa
  F141 início  GUGA levanta a cabeça, emote: laugh pequeno
  F143 início  os 3 riem: partícula `heart` pequena
planos:
  F138 + pausa  POV-A andando até o banco (o Guga de costas, pequeno)
  F139  NOVELA plano médio: os 3 no banco, de frente (câmera baixa, árvore ao lado)
  F140  NOVELA close da Nina
  F141  NOVELA close do Guga
  F142–F143  NOVELA plano médio dos 3; pausa: plano geral de longe, banco + árvore + sol baixo
câmera:
  movimento: dolly out lento na pausa
  de: 8.5 65 -9 · yaw 0 · pitch 0   →   para: 8.5 66 -14 · yaw 0 · pitch 5
  duração: pausa de 2 s
efeitos (pós): cor quente (+laranja) no B6 inteiro
texto na tela: "DESCULPA, GUGA." (laranja) em F139
som: piano continua, mais claro (nota maior) · passarinhos de fim de tarde

### C028 — F144–F150 (+ reação: GUGA · pausas de cena 3 s e 2 s)
tipo: jogo
mundo: vila_pastel
local: banco da praça · hora 9500
cenário:
  - **memória (F145–F147):** mesmo banco, céu igual; TOCO-criança = Easy NPC com `skins/toco.png` e escala 0,6 (atributo `scale`), sozinho no banco; VÓ CIDA mais nova (sem bengala) chega com um pastel
elenco:
  - VÓ CIDA chega devagar com a bengala (de 2 64 -2 até 7 64 -5, 4 s), fica de pé · GUGA · NINA · TOCO-dublê
ações (tempo a partir do início da F144):
  F144 início  VÓ CIDA emote: talk lento
  F145 início  corte para a memória: TOCO-criança sentado, olhando o chão
  F146 início  memória: VÓ dá o pastel (`item_display` passa da mão dela para a dele)
  F147 início  memória: TOCO-criança levanta a cabeça; partícula `heart` 1 vez · volta ao presente no fim da F147
  reação  GUGA emote: sad → sorri
  F148 início  VÓ CIDA põe a mão no ombro do TOCO-dublê (emote: talk) · partícula `heart`
  F149 início  GUGA emote: eat (chorando e comendo)
  F150 início  VÓ CIDA emote: laugh pequeno
planos:
  F144  NOVELA plano médio da Vó
  F145–F147  memória: NOVELA plano geral do banco com o Toco pequeno → close do Toco-criança dizendo "Obrigado"
  reação  NOVELA close do Guga
  F148  NOVELA close da Vó, dolly in lento; pausa: plano geral dos 4 no banco
  F149–F150  NOVELA plano médio Guga + Vó (alívio cômico)
câmera:
  movimento: dolly in (F148)
  de: 7 65.6 -9 · yaw 20 · pitch 0   →   para: 7 65.6 -8 · yaw 20 · pitch 0
  duração: F148
efeitos (pós): memória com **vinheta branca borrada** + cor lavada (−40% saturação) + leve desfoque nas bordas
texto na tela: "OBRIGADO." (branco, pequeno) em F147 · "É FEITA DE GENTE." (roxo-lilás) em F148
som: na memória, só caixinha de música (Audio Library `music box`, sem atribuição) · música sobe na pausa da F148 e cai na piada da F149

### C029 — F151–F158 (+ pausas de cena 3 s e 3 s)
tipo: jogo
mundo: vila_pastel
local: banco → pastelaria (linha de montagem) · hora 10000 → 10800
cenário:
  - linha de montagem: mesa (Nina) → mesa (Guga) → tacho (Toco); 12 `item_display` de pastel andando no balcão (`/tp` a cada 5 ticks) = esteira
elenco:
  - os 3 + VÓ CIDA sentada na cadeira comandando (emote: point em loop)
ações (tempo a partir do início da F151):
  F151 início  TOCO-dublê levanta do banco (emote: cheer)
  F153 início  NINA emote: point para o sol (bossbar)
  F155 início  VÓ CIDA bate a bengala no chão (som `block.wood.hit`)
  pausa 3 s  MONTAGEM turbo: 8 planos de 0,4 s
  F156–F157  placar sobe em degraus de 100
  F158 início  NINA emote: point para a torre
planos:
  F151–F152  NOVELA contra-plongée do TOCO-dublê de pé, sol atrás (plano "herói")
  F153–F155  POV-A voltando para a pastelaria, cada um vai para o seu posto
  pausa + F156–F157  montagem: POV-A no tacho + NOVELA plano detalhe da esteira + close da Vó gritando
  F158 + pausa  NOVELA drone: da pastelaria até a Torre Dourada ao fundo
câmera:
  movimento: drone
  de: 0 75 5 · yaw 135 · pitch 25   →   para: 15 80 -5 · yaw 135 · pitch 20
  duração: F158 + pausa
efeitos (pós): avanço rápido 1,5× na montagem · "TURBO!" com linhas de velocidade
texto na tela: "MODO TURBO!" em F153 · "100! 200! 300!" na montagem · "390" em F158
som: música épica-cômica (Audio Library `epic comedy` ou `quirky orchestral`) · ka-ching em cascata
HUD: Esmeraldas 0 → 390 · sol 40 → 25 (cor `/bossbar set vila:sol color red` a partir de 25)

### C030 — F159–F166 (+ pausa de cena 2 s)
tipo: jogo
mundo: vila_pastel
local: dentro da Torre Dourada, corredor do tapete · hora 11000
cenário:
  - placa `oak_wall_sign` em 28 65 -21: "NÃO PISE NO / TAPETE DOURADO"
  - MORDOMO: `villager` nitwit NoAI em 31 64 -19, `text_display` "z z z" em cima subindo e sumindo
  - alarme = função `vila:torre/alarme` (sinos `block.bell.use` ×6, `/fill` de `redstone_lamp[lit=true]` no teto, `/particle dust{color:[1,0.8,0],scale:1.5}`)
elenco:
  - TOCO (POV-A agachado: shift), NINA e GUGA (Easy NPC agachados, pose crouching) atrás
ações (tempo a partir do início da F159):
  F159 início  TOCO entra pela porta agachado
  F161 início  MORDOMO som `entity.villager.ambient` em pitch baixo ("hrmm") a cada 2 s
  F163 início  GUGA aponta a placa
  F165 início  GUGA pisa no tapete (vai 0,5 bloco para a frente) → `function vila:torre/alarme`
  F166 início  GUGA emote: shrug, um pé levantado
planos:
  F159–F164  POV-A agachado, corredor dourado (lento, furtivo)
  F161  NOVELA close do mordomo roncando (piada)
  F165  NOVELA plano detalhe: o pé do Guga no tapete
  pausa  NOVELA plano geral do corredor: lâmpadas acendendo em sequência, sinos
  F166  NOVELA close do Guga
câmera:
  movimento: estática (detalhe) · travelling do teto na pausa
  de: 28 68 -21 · yaw 90 · pitch 40   →   para: 32 68 -21 · yaw 90 · pitch 40
  duração: pausa
efeitos (pós): luz piscando amarela/vermelha na pausa (overlay de cor 3 vezes)
texto na tela: "NÃO PISE NO TAPETE DOURADO" (já na placa) · "OPS." em F165
som: "Sneaky Snitch" (Kevin MacLeod, CC BY 4.0) nas F159–F164 · ronco · música para no "Ops." · sinos e alarme
HUD: Esmeraldas 390 · sol 18

### C031 — F167–F172
tipo: jogo
mundo: vila_pastel
local: sala do cofre da torre, 28 64 -23 · hora 11200
cenário:
  - cofre aberto e vazio: `chest` aberto (som) + `gold_block` sumiu (só os buracos no chão: `/fill` para `air` em 6 blocos)
elenco:
  - LORENA desce a escada da torre (de 30 70 -20 até 30 64 -21, 2 s) · TOCO (POV-A) · NINA · GUGA
ações (tempo a partir do início da F167):
  F167 início  LORENA emote: angry
  F168 início  TOCO-dublê emote: point para a Lorena
  F169 início  LORENA emote: shock, mãos para cima
  F170 início  LORENA emote: point para o cofre; anda até ele
  F171 início  LORENA emote: sad, olhando os buracos no chão
  F172 início  NINA emote: sad
planos:
  F167  NOVELA contra-plongée da Lorena na escada
  F168  POV-A
  F169  NOVELA close da Lorena (surpresa de verdade, sem pose)
  F170  NOVELA plano geral do cofre vazio (revelação: virada 2), câmera sobe por trás da Lorena
  F171  NOVELA close da Lorena, dolly in (1º momento "humano" dela)
  F172  NOVELA close da Nina
câmera:
  movimento: revelação (F170)
  de: 30 64.8 -20 · yaw 180 · pitch 0   →   para: 30 67 -19.5 · yaw 180 · pitch 30
  duração: F170
efeitos (pós): flash leve na F170 · cor dourada perde 30% de saturação na F171
texto na tela: "O MEU COFRE TAMBÉM!" (dourado) em F170 · "TODO MUNDO ACUSOU TODO MUNDO." em F172
som: alarme some · "dun" grave na F170 · piano triste curto na F171–F172

### C032 — F173–F177 (+ pausa de cena 3 s)
tipo: jogo
mundo: vila_pastel
local: cofre da torre → corrida pela praça → pastelaria · hora 11500 (sol bem baixo)
elenco:
  - os 4 (Lorena junto) correndo
ações (tempo a partir do início da F173):
  F173 início  NINA emote: think
  F175 início  TOCO-dublê emote: point (ideia!)
  F176 início  `/bossbar set vila:sol value 5` + `color red` · NINA emote: shock
  F177 início  LORENA emote: point para si mesma
  pausa  corrida: TOCO (POV-A) corre (sprint) da torre até a pastelaria; NINA, GUGA, LORENA atrás (`/tp` em passos)
planos:
  F173–F175  POV-A, rostos em sequência (cortes de 1 s)
  F176  POV-A no bossbar quase vazio (zoom de edição)
  F177  NOVELA close da Lorena
  pausa  POV-A correndo + NOVELA travelling lateral dos 4 correndo na praça, sol se pondo atrás
câmera:
  movimento: travelling
  de: 25 66 -5 · yaw 270 · pitch 0   →   para: 5 66 -5 · yaw 270 · pitch 0
  duração: pausa
efeitos (pós): linhas de velocidade · tique-taque visual no bossbar
texto na tela: "A TOCA!" em F175 · "2 MINUTOS!" (vermelho) em F176
som: tique-taque (relógio) a partir da F176 até o fim do B7 · música de corrida épica (Audio Library `epic run`)
HUD: Esmeraldas 390 · sol 5 (vermelho)

### C033 — F178–F184 (+ pausa de cena 3 s)
tipo: jogo
mundo: vila_pastel
local: atrás do balcão, buraco em -1 64 12 · hora 11700
cenário:
  - na pausa: `/fill -2 64 11 2 64 15 minecraft:air destroy` em 3 ondas de 0,3 s (pedaços de bloco voando) e depois `/fill` do chão abaixo até a toca (escada natural de `dirt`)
elenco:
  - VÓ CIDA na cadeira · LORENA dá a `golden_pickaxe` ao Toco (sai da mão dela e aparece na hotbar do jogador: `/give @p golden_pickaxe` no F181 fim)
ações (tempo a partir do início da F178):
  F178 início  VÓ CIDA emote: shock (sentada)
  F180 início  VÓ CIDA emote: point para o chão, depois para o teto
  F181 início  LORENA estende a picareta (emote: point)
  F183 início  LORENA ajeita o cabelo (emote: shrug)
  F184 início  TOCO (POV-A) levanta a picareta
  pausa  TOCO quebra o chão (cliques reais no jogo; o datapack completa o buraco)
planos:
  F178–F180  POV-A Vó Cida
  F181–F183  NOVELA plano detalhe da picareta de ouro brilhando + close Lorena
  F184  POV-A, picareta para o alto
  pausa  POV-A quebrando + NOVELA plongée de cima: o chão se abrindo
câmera:
  movimento: estática de cima
  de: 0 69 13 · yaw 0 · pitch 85   →   para: igual
  duração: pausa
efeitos (pós): tremida a cada bloco quebrado · flash quando abre o buraco
texto na tela: "TUDO DE OURO." (dourado) em F183 · "DÁ RUIM, MAS DÁ CERTO!" (laranja) em F184
som: "pling" da picareta · blocos quebrando em sequência (`block.stone.break`) · riser
HUD: Esmeraldas 390 · sol 4

### C034 — F185–F192
tipo: jogo
mundo: vila_pastel
local: toca da raposa, -4 56 11 a 4 61 17 · hora 11800
cenário:
  - tesouro montado (ver §0): esmeraldas, ouro, sino, 12 pastéis, 2 coroas, espelho
  - luz: 4 `glow_lichen` + 2 `lantern` "da raposa" (a toca brilha verde por causa das esmeraldas: `/particle happy_villager` lento)
  - DUQUESA dormindo em cima da pilha: `fox` com `Sleeping:1b` em 0 58 14
elenco:
  - os 4 descem a escada de terra (`/tp` em passos) · DUQUESA
ações (tempo a partir do início da F185):
  F185 início  todos param na beira (emote: shock em sequência, 0,3 s um do outro)
  F186 início  NINA emote: point em 3 direções (esmeraldas, ouro, sino)
  F187 início  LORENA corre até as coroas
  F188 início  TOCO-dublê emote: point para a raposa
  F189 início  GUGA emote: love (se não existir: `heart`)
  F190 início  GUGA abraça um pastel (pega o `item_display`)
  F191 início  LORENA emote: cheer em cima do ouro
  F192 início  DUQUESA acorda (`Sleeping:0b`), pega 1 esmeralda e foge pelo túnel leste (2 s)
planos:
  F185  NOVELA **grande plano geral** da toca: os 4 pequenos lá no alto, a pilha brilhando embaixo (o plano mais bonito do episódio)
  F186  POV-A pan pelo tesouro
  F187  NOVELA close da Lorena com as coroas
  F188–F189  NOVELA close da raposa dormindo (fofa) + reação do Guga
  F190–F191  POV-A rápido entre Guga e Lorena
  F192  NOVELA plano geral, a raposa correndo para o túnel
câmera:
  movimento: órbita lenta em volta da pilha no grande plano geral
  de: 3 61 11 · yaw 210 · pitch 35   →   para: -3 61 11 · yaw 150 · pitch 35
  duração: F185–F186
efeitos (pós): brilho (glare) nas esmeraldas · "chuva de esmeraldas" no fim da F191: `/particle item{item:"minecraft:emerald"} 0 60 14 2 1 2 0.2 150` (conferir a sintaxe na 1.21.11)
texto na tela: "A TOCA!" em F185 · "LADRA FOFA" (amarelo-mostarda) em F189
som: coral "aaah" ao revelar · tilintar de moedas · `entity.fox.sleep` · `entity.fox.ambient` na fuga · música épica no máximo do episódio
HUD: Esmeraldas 390 · sol 3

### C035 — F193–F195 (+ reação: TOCO)
tipo: jogo
mundo: vila_pastel
local: toca · hora 11900
elenco:
  - NINA no meio com o caderno · os outros em volta
ações (tempo a partir do início da F193):
  F193 início  NINA emote: point para o caderno, depois aponta cada pilha (Lorena / pastelaria / vila)
  F194 início  `item_display` das 600 esmeraldas sobe da pilha e "voa" para o Toco (4 `/tp` em arco); placar sobe
  F194 fim  [reação TOCO] TOCO-dublê emote: shock
planos:
  F193  NOVELA plano médio da Nina com o caderno aberto (plano detalhe da página: lista com nomes)
  F194  POV-A: o placar subindo
  reação  NOVELA close do TOCO-dublê
  F195  POV-A olhando para o buraco lá em cima: luz laranja de pôr do sol entrando
câmera:
  movimento: estática
  de: 0 59 16.5 · yaw 180 · pitch 0   →   para: igual
  duração: F193
efeitos (pós): nenhum
texto na tela: "990" (verde, grande) em F194 · "FALTAM 10" (vermelho) em F195
som: ka-ching rápido ×60 (subindo) · tique-taque mais alto
HUD: Esmeraldas 390 → 990 · sol 2

### C036 — F196–F201 (+ pausas de cena 3 s e 3 s)
tipo: jogo
mundo: vila_pastel
local: toca → saída do buraco, pastelaria ao pôr do sol · hora 12000 → 12300
elenco:
  - GUGA tira o pastel de emergência do "bolso" (`item_display` aparece na mão) · LORENA · NINA · TOCO (POV-A)
ações (tempo a partir do início da F196):
  F196 início  GUGA emote: point para cima (solene); luz de "milagre": `/particle end_rod` em volta do pastel
  F197 início  NINA emote: shock
  F198 início  GUGA estende o pastel para a Lorena
  F199 início  LORENA vira o rosto (emote: shrug) · som de barriga roncando (Freesound CC0 `stomach growl`)
  F200 início  LORENA pega o pastel, `item_display` de 10 esmeraldas vai para o Guga
  pausa 3 s  "+10" → **1000**; `/bossbar set vila:sol value 0`; o sol encosta no horizonte (`/time set 12300`)
  F201 + pausa 3 s  os 4 pulam (emote: cheer); `/title @a title {"text":"1000!","color":"green"}`
planos:
  F196  NOVELA contra-plongée do Guga com o pastel (épico de brincadeira)
  F197  NOVELA close da Nina
  F198  NOVELA sobre o ombro do Guga → Lorena
  F199  NOVELA close da Lorena (barriga ronca: 1 s de silêncio antes)
  F200  plano detalhe: pastel indo, esmeraldas vindo
  pausa  POV-A no HUD: 990 → 1000, sol zerado (câmera lenta 50% no número virando)
  F201 + pausa  NOVELA plano geral de fora: o buraco do chão com os 4 pulando, a pastelaria contra o pôr do sol
câmera:
  movimento: revelação (sobe e mostra o sol se pondo atrás da pastelaria)
  de: 0 66 6 · yaw 0 · pitch 0   →   para: 0 74 0 · yaw 0 · pitch 10
  duração: F201 + pausa
efeitos (pós): câmera lenta no "1000" · flash branco 2 quadros
texto na tela: "PASTEL DE EMERGÊNCIA" (amarelo-mostarda) em F196 · "1000!" é o /title do jogo
som: coral "aaah" em F196 · ronco de barriga · silêncio total 0,5 s antes do 1000 · ka-ching + `ui.toast.challenge_complete` + música de vitória
HUD: Esmeraldas 990 → 1000 · sol 0

### C037 — F202–F207
tipo: jogo
mundo: vila_pastel
local: praça, frente da pastelaria · hora 12600 (céu laranja e roxo) · fogos
cenário:
  - fogos: função `vila:fogos` com 8 `firework_rocket` lançados de 5 pontos da praça, a cada 0,5 s, cores laranja (#F2811D), verde-água (#2EC4B6), amarelo, roxo e dourado (as 5 cores-assinatura):
    `/summon firework_rocket 0 64 -6 {LifeTime:30,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:2,explosions:[{shape:"large_ball",colors:[I;15892765,3064502]}]}}}}`
  - tesouro devolvido ao lado: sino de volta na torre do sino da vila (nada a filmar)
elenco:
  - os 4 + VÓ CIDA na porta, na cadeira · `item_display` de saco/pilha de 1000 esmeraldas entregue
ações (tempo a partir do início da F202):
  F202 início  TOCO-dublê e NINA emote: clap · fogos começam
  F204 início  TOCO aponta para os fogos (POV-A) · `item_display` de `gunpowder` aparece e some na mão da Nina (lembrança)
  F205 início  VÓ CIDA estende o saco (emote: point) · LORENA recebe
  F206 início  LORENA emote: eat (morde o pastel) · partícula `heart` pequena (ela tenta esconder)
  F207 início  LORENA emote: wave, vai embora devagar · 1 `heart` sai dela de novo
planos:
  F202–F203  NOVELA plano geral da praça com fogos no céu
  F204  POV-A olhando os fogos
  F205  NOVELA plano médio Vó + Lorena (2 personagens)
  F206  NOVELA close da Lorena comendo (com o coração escapando)
  F207  NOVELA plano geral, ela indo embora com os fogos atrás
câmera:
  movimento: estática + dolly out na F207
  de: 2 66 2 · yaw 180 · pitch 10   →   para: 2 68 -6 · yaw 180 · pitch 15
  duração: F207
efeitos (pós): glare nos fogos
texto na tela: "VALEU, CREEPER!" (laranja) em F204 · "PAGO" (carimbo verde) em F205
som: fogos (`entity.firework_rocket.launch`, `large_blast`, `twinkle`) · música de festa (Audio Library `happy brass` / `celebration`) · música baixa nas falas

### C038 — F208–F217 (+ pausa de cena 2 s)
tipo: jogo
mundo: vila_pastel
local: frente da pastelaria, anoitecendo · hora 13000 · lanternas acesas
cenário:
  - placa ainda "PASTEL... A VÓ"; escada nova encostada (`ladder`)
  - balcão com 1 `item_display` de caixa registradora
elenco:
  - NINA · TOCO-dublê / POV-A · GUGA · VÓ CIDA · DUQUESA (volta da esquerda com um pastel na boca: `weapon.mainhand` = `bread` com `item_model` "vila:pastel")
ações (tempo a partir do início da F208):
  F208 início  NINA fecha o caderno (emote: clap)
  F209 início  TOCO-dublê aponta a placa
  F210 início  GUGA segura a escada com as 2 mãos (pose)
  F211 início  VÓ CIDA emote: point para a boca do Guga
  F212 início  GUGA emote: sad, mãos vazias
  F213 início  NINA emote: point para a esquerda; DUQUESA entra (2 s)
  F214 início  DUQUESA solta o pastel no pé do Guga (som `entity.fox.spit`); GUGA emote: love/`heart`
  F215 início  DUQUESA pula no balcão e senta ao lado da caixa (Sitting:1b)
  F216 início  TOCO-dublê emote: shock
  F217 início  VÓ CIDA emote: laugh · DUQUESA vira a cabeça para o baú
  pausa  DUQUESA dá uma olhadinha para o baú e para a câmera (piada final)
planos:
  F208–F211  NOVELA plano geral dos 4 na frente da pastelaria (luz de lanterna)
  F212  NOVELA close do Guga triste
  F213–F214  NOVELA plano médio Guga + raposa
  F215  POV-A: a raposa no balcão
  F216  NOVELA close do TOCO-dublê
  F217  NOVELA close da Vó (sorriso)
  pausa  NOVELA close da raposa olhando o baú → olhando a câmera; corte seco para o CTA
câmera:
  movimento: estática; dolly in curto na raposa
  de: 1 65.3 9 · yaw 0 · pitch 10   →   para: 1 65.2 9.6 · yaw 0 · pitch 10
  duração: pausa
efeitos (pós): nenhum
texto na tela: "COM AS DUAS MÃOS." em F210 · "CAIXA: DUQUESA" (placa de nome, roxo-lilás) em F215
som: grilos · "aww" (Freesound CC0 `crowd aww`) em F214 · vinil arranhando no fim da F217 · "ié-ié" na pausa

### C039 — F218–F219 (CTA fixo de 10 s)
tipo: jogo
mundo: vila_pastel
local: balcão da pastelaria, de frente para a câmera · hora 1000 (sempre o mesmo, gravado 1 vez para a série)
elenco:
  - TOCO-dublê atrás do balcão, de avental, com um pastel · os outros ao fundo
ações (tempo a partir do início da F218):
  F218 início  TOCO-dublê emote: wave
  F219 início  TOCO-dublê emote: point para o canto da tela (onde a tela final põe o vídeo) · "Dá ruim, mas dá certo!" = todos emote: cheer
planos:
  F218–F219  NOVELA plano médio frontal, fixo (é o mesmo em todo episódio)
câmera:
  movimento: estática
  de: 0 65.6 7 · yaw 0 · pitch 0   →   para: igual
  duração: 10 s
efeitos (pós): botão de inscrição animado (próprio) + espaço livre à direita para os 2 vídeos da tela final
texto na tela: "SE INSCREVE!" (laranja) em F218
som: vinheta curta da série (5 notas de ukulele, Audio Library) · clique do botão
