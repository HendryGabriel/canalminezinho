# Cenas — QUANTO VALE UM MUNDO DO MINECRAFT?
Mundo de gravação: mv_cine (sobrevivência pré-gerado) + mv_void (estúdio vazio) · Versão: Java 1.21.11 Fabric (a do MCP) · Look: épico/documentário

Cobre F001–F183 (75 cenas). Os tempos `+N s` contam do início da 1ª frase da cena; o Claude troca por ticks com o `tempos.json` (guia 09 §4).
Mix de imagem (guia 03 §2), pelo tipo principal de cada cena: jogo 43 (8 delas com a tela/GUI do jogo) · estudio3d 17 · texto 7 · mapa 4 · espaço 4. Algumas cenas misturam 2 tipos (ex.: "estudio3d → jogo").

## Setup comum (rodar 1 vez por mundo, função `cenas:setup/<mundo>`)

### Mundos
| Mundo | O que é | Preparar |
|---|---|---|
| `mv_cine` | mundo normal, criativo com cheats. Seed: uma com vila de planície a < 500 blocos do spawn, montanha, badlands e lago de lava numa caverna funda (o Claude acha com `/locate structure minecraft:village_plains` e `/locate biome minecraft:badlands` e anota as coordenadas aqui) | `/chunky radius 3000` + `/chunky start` (o mapa de 2.000 × 2.000 e o Distant Horizons precisam) · shader Complementary Reimagined · DH 256+ chunks |
| `mv_void` | superflat vazio (camada só de ar), bioma `the_void` | palco: `/fill -10 63 -10 10 63 10 minecraft:black_concrete` (só quando a cena pede chão) · neblina do shader no máximo · fundo azul-escuro |
| Blender `estudio3d` | estúdio cinza com papel quadriculado e sombra suave (guia 03 §2, tipo 2) | `ferramentas/blender/montar_cena.py` + `looks.py`; blocos/itens exportados do jogo (Mineways) |
| Blender `espaco` | fundo de estrelas, Terra, quadrado do mapa | `ferramentas/blender/montar_cena.py` |
| `texto` | card de número/conta (Remotion ou `ferramentas/edicao/efeitos.py`) | fonte grossa branca com contorno (guia 03 §4) |
| `mapa` | render de cima do `mv_cine` (guia 06 §4) | grade de chunks e círculos na pós |

### Regras de mundo (os 2 mundos de jogo)
```
/gamerule doDaylightCycle false      # no 1.21.11 o nome pode ter mudado (ex.: advance_time): conferir com TAB
/gamerule doWeatherCycle false
/gamerule doMobSpawning false
/gamerule doTileDrops false           # nada cai no chão sem querer
/weather clear
```
Gravação: F1 (sem interface) e F3+P sempre, **menos** nas cenas marcadas "GUI" (aí a interface aparece de propósito, mira escondida na pós).

### Elenco fixo
- **VOCÊ** (o espectador): `mannequin` (Java 1.21.9+) com a skin do canal.
  `/summon minecraft:mannequin X Y Z {profile:{name:"<skin do canal>"},pose:"standing",immovable:1b,hide_description:1b,Tags:["voce"]}`
  ⚠️ campos do mannequin conferir no 1º teste (guia 09). Plano B: Easy NPC.
- **O Avaliador** (mascote, ver ideia.md): villager bibliotecário parado com monóculo.
  ```
  /summon minecraft:villager X Y Z {CustomName:"Avaliador",NoAI:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b,VillagerData:{type:"minecraft:plains",profession:"minecraft:librarian",level:5},Tags:["avaliador"]}
  /summon minecraft:item_display X Y Z {item:{id:"minecraft:tinted_glass",count:1},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0.12f,1.72f,-0.3f],scale:[0.12f,0.12f,0.02f]},Tags:["monoculo"]}
  /ride @e[tag=monoculo,limit=1] mount @e[tag=avaliador,limit=1]
  ```
  (ajustar `translation` até o monóculo cair no olho direito no print)
  "Falar": som `entity.villager.ambient` no início da fala + balão `text_display` opcional. "Não": `entity.villager.no` + partícula `angry_villager`. "Sim": `entity.villager.yes` + `happy_villager`.
- **Escritório do Avaliador** (salvar como estrutura `cenas:escritorio` e reusar em outros vídeos): em `mv_void`, palco de 7 × 7 de `dark_oak_planks` em Y 63, `lectern[facing=south]` em 0 64 1, estante (`bookshelf`) atrás, 2 lanternas. Avaliador em 0 64 2,5 olhando para o sul (câmera).

### Item gigante (usado em várias cenas)
```
/summon minecraft:item_display 0 66 0 {item:{id:"minecraft:diamond",count:1},billboard:"fixed",transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[4f,4f,4f]},Tags:["item_grande"]}
# girar devagar (função cenas:util/girar, a cada 40 ticks):
/data merge entity @e[tag=item_grande,limit=1] {start_interpolation:0,interpolation_duration:40,transformation:{left_rotation:{angle:3.1416f,axis:[0f,1f,0f]}}}
```
Texto 3D no jogo: `/summon minecraft:text_display X Y Z {text:{text:"R$ 1 BILHÃO",color:"white",bold:true},billboard:"center",background:0,shadow:1b,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[3f,3f,3f]},Tags:["txt"]}`

### Música (só da `biblioteca/`, com crédito; troca por bloco — guia 05 §3)
| Bloco | Clima | Buscar |
|---|---|---|
| B1 | mistério que sobe, para seco no título | `mystery riser`, `investigation` |
| B2–B3 | lo-fi/piano calmo nas contas | `lofi calm`, `tutorial` |
| B4 | pizzicato/marimba cômico (Avaliador) | `pizzicato`, `quirky` (Incompetech) |
| B5–B7 | orquestral que cresce a cada degrau | `epic orchestral build` |
| B8–B10 | épico grande + coral nas pausas | `epic choir`, `cinematic` (Scott Buckley) |
| B11 | silêncio → drone escuro | `dark ambient`, `drone` |
| B12 | piano + cordas, sobe na última frase | `emotional piano`, `hopeful` |
Ducking: música 15–20 dB abaixo da voz; nas `[pausa de cena]` sobe até ~−5 dB da voz (guia 05 §5).

---

## B1 — Abertura

### C001 — F001
tipo: jogo
mundo: mv_cine
local: veio de diamante numa caverna funda (o Claude acha com `/locate`/WorldEdit `//count` perto de Y −58) · overworld · hora 6000 · sem chuva · tick congelado: sim
cenário:
  - se o veio for pequeno: `/fill X −58 Z X+1 −57 Z+1 minecraft:deepslate_diamond_ore replace minecraft:deepslate`
  - `glow_lichen` em 2 paredes perto (luz azulada natural)
elenco: —
ações: —
câmera:
  movimento: dolly in, câmera baixa
  de: X−6 −57,7 Z · yaw −90 · pitch 5   →   para: X−2 −57,7 Z · yaw −90 · pitch 8
  duração: F001 inteira
efeitos (pós): leve vinheta escura
texto na tela: —
som: passos de caverna + gota d'água (som do jogo) · música: riser de mistério começa

### C002 — F002
tipo: jogo
mundo: mv_void
local: 0 66 0 · hora 18000 · tick congelado: sim
cenário:
  - 3 item_display (diamante em −3 66 0, barra de ouro em 0 66 0, lingote de ferro em 3 66 0), escala 2, girando (cenas:util/girar)
  - text_display "R$ ?" em cima de cada um, escala 1,5
elenco: —
ações: +0,0 diamante acende (aparece) · +1,2 ouro · +2,4 ferro (cada um com `/summon` no tempo)
câmera:
  movimento: travelling
  de: −5 66 −8 · yaw 0 · pitch 0   →   para: 5 66 −8 · yaw 0 · pitch 0
  duração: F002
efeitos (pós): —
texto na tela: "EM REAIS" (pop) na palavra "reais"
som: pop a cada item · ka-ching na palavra "reais"

### C003 — F003
tipo: jogo
mundo: mv_cine
local: mesmo veio da C001
elenco:
  - VOCÊ: mannequin, pose standing, com picareta de ferro na mão (`/item replace entity @e[tag=voce,limit=1] weapon.mainhand with minecraft:iron_pickaxe`), olhando para o minério
ações:
  +0,0  `/setblock X −58 Z air destroy` (partícula de quebra) + `/summon item X −58 Z {Item:{id:"minecraft:diamond",count:1}}`
  +0,8  VOCÊ: pulo curto (`/tp` em arco, 0,4 s) + partícula `happy_villager`
câmera:
  movimento: estática, depois zoom brusco no rosto do VOCÊ (zoom na pós) em "Eu sei"
  de: X−3 −57 Z+2 · yaw −120 · pitch 10
efeitos (pós): zoom brusco 1,0 → 1,6 em "Eu sei" + tremida curta
texto na tela: —
som: quebra de bloco + grito curto (SFX "yell") · disco arranhando em "Eu também grito"

### C004 — F004
tipo: jogo
mundo: mv_void
local: 0 66 0 · hora 18000 · tick congelado: não (para a interpolação andar)
cenário:
  - item_grande (diamante) escala 0,5 → 6 em 3 s (`interpolation_duration:60`)
  - text_display "R$ 1.000.000.000" em 0 72 0, aparece em "um bilhão"
câmera:
  movimento: câmera baixa, dolly out
  de: 0 64,5 −6 · yaw 0 · pitch −25   →   para: 0 64,5 −12 · yaw 0 · pitch −20
  duração: F004
efeitos (pós): flash branco curto quando o número aparece
texto na tela: "1 DIAMANTE" (pop) + o número 3D do jogo
som: boom grave em "um bilhão de reais"

### C005 — F005
tipo: espaco
mundo: Blender `espaco`
cenário: Terra à esquerda; à direita, um quadrado plano com textura do mapa do Minecraft, bem maior; pilha de notas de dinheiro (low poly) pequena em cima da Terra
câmera:
  movimento: órbita lenta 20°
  duração: F005
texto na tela: "> TODO O DINHEIRO DA TERRA" (digitando)
som: whoosh longo + boom grave em "Terra"

### C006 — F006 + pausa de cena 12 s
tipo: jogo
mundo: mv_cine
local: começa alto sobre o spawn, termina numa casinha de terra 5 × 5 perto do spawn (a mesma da C072) · hora 12500 (fim de tarde) · sem chuva · tick congelado: não
cenário:
  - casinha de terra feia (função `cenas:util/casa_terra` em XC YC ZC: paredes `dirt`, porta `oak_door`, 1 tocha) — **construir agora e não mexer até a C074**
câmera:
  movimento: drone que desce e termina na casinha
  de: XC 180 ZC−120 · yaw 0 · pitch 30   →   para: XC YC+4 ZC−10 · yaw 0 · pitch 15
  duração: do início da F006 até o fim da pausa
efeitos (pós): no meio da pausa entra o título "QUANTO VALE UM MUNDO DO MINECRAFT?" (fade) e sai em 4 s
texto na tela: título
som: música de mistério sobe e **para seco** no corte para a C007 · boom no título

## B2 — A regra do vídeo

### C007 — F007–F009
tipo: estudio3d
cenário: 1 bloco de pedra no centro; régua 3D "1 m" em cada aresta; ao lado, uma janela flutuante com print da página "Block" da Minecraft Wiki (trecho "1-cubic-meter cells" grifado)
planos:
  F007  bloco sozinho, câmera alta
  F008  régua desenhando as 3 arestas (1 m, 1 m, 1 m) → "1 m³"
  F009  janela da wiki entra deslizando, grifo amarelo
câmera: órbita 45° em volta do bloco
texto na tela: "1 m" ×3 · "1 m³" (pop) em F008
som: risco de giz nas réguas · clique de mouse na janela

### C008 — F010–F012
tipo: jogo (GUI)
mundo: mv_void (qualquer lugar)
local: jogador em criativo com `crafting_table` à frente
ações:
  F010  abre a mesa (clique) — gravar com interface
  F011  coloca os 9 diamantes; tira o bloco; depois desfaz o bloco em 9
  F012  —
câmera: 1ª pessoa, parada na GUI
efeitos (pós): zoom na grade 3 × 3; em F012 congela e desenha "1/9" em cima de um diamante
texto na tela: "9 = 1 BLOCO" (F011) · "1/9 m³" (F012)
som: clique de interface do jogo · pop

### C009 — F013
tipo: jogo
mundo: mv_cine
local: outro bloco de `deepslate_diamond_ore` · Y −58 · tick congelado: sim
ações:
  +0,0  `/setblock X Y Z air destroy` + `/summon item X Y Z {Item:{id:"minecraft:diamond",count:1}}`
câmera: estática, close no bloco (2 blocos de distância)
efeitos (pós): no "resto era pedra", silhueta do bloco fica cinza e o diamante fica colorido
texto na tela: "1 DIAMANTE + PEDRA"
som: quebra de bloco (som do jogo)

### C010 — F014–F016
tipo: estudio3d
cenário: cubo de 1 m³ de diamante de verdade (material vidro/diamante, refração) → se divide em 9 fatias; 1 fatia sai para a frente
planos:
  F014  cubo inteiro girando
  F015  corte em 9 (fatias se afastam)
  F016  1 fatia, close
texto na tela: "3.510 kg" (F015 início) · "÷ 9" · "390 kg" (pop, F016)
som: vidro tilintando no corte · ka-ching em "trezentos e noventa"

### C011 — F017–F018
tipo: estudio3d → jogo
cenário: (F017) balança antiga: de um lado 1 diamante do Minecraft (modelo do item, 3D), do outro 5 bonecos cinza de gente; a balança fica reta · (F018) corte para o jogo
planos:
  F017  estudio3d: balança equilibrando
  F018  jogo (mv_void, palco): VOCÊ pulando em loop (`/tp` em arco a cada 0,6 s) com inventário cheio na pós
câmera: F018 câmera baixa, VOCÊ de corpo inteiro
efeitos (pós): F018 mostra hotbar com 64 diamantes e "64 × 390 kg = 25 t"
texto na tela: "= 5 PESSOAS" (F017) · "25 TONELADAS" (F018)
som: rangido da balança · "boing" a cada pulo

### C012 — F019
tipo: texto
cenário: card escuro com a regra
texto na tela: "REGRA DO VÍDEO: 9 ITENS = 1 m³" (digitando) + nota cinza minúscula embaixo "culpa da mesa de trabalho"
som: máquina de escrever · música: lo-fi calmo continua

### C013 — F020–F021
tipo: estudio3d
cenário: balança de joalheiro com um diamantinho de 1 quilate; contador digital ao lado
planos:
  F020  close na balança: "0,2 g"
  F021  o contador dispara até 1.950.000
texto na tela: "1 QUILATE = 0,2 g" · "1.950.000 QUILATES" (contador)
som: tique de contador acelerado

### C014 — F022–F024
tipo: estudio3d → jogo
cenário: pedra de diamante bruta (modelo genérico, não foto) do tamanho de um punho ao lado de uma régua; depois o diamante do Minecraft ao lado, 628 × maior em volume
planos:
  F022  pedra bruta + "3.106 quilates · 621 g"
  F023  câmera recua e revela o item de diamante gigante ao lado
  F024  divide a tela: coroa estilizada (modelo próprio, sem foto) × jogo: mão do jogador segurando `diamond_hoe` (mv_cine, plantação de trigo)
câmera: F023 dolly out rápido (revelação)
texto na tela: "CULLINAN" (F022) · "× 628" (pop, F023)
som: whoosh na revelação · boom em "seiscentas e vinte e oito" · F024: som de enxada na terra (jogo)

## B3 — Um diamante

### C015 — F025–F028
tipo: estudio3d
cenário: à esquerda um brilhante lapidado numa vitrine; à direita um monte de pedras brutas pequenas e foscas
planos:
  F025  diamante bruto do Minecraft girando + "?"
  F026  vitrine com brilhante, etiqueta "$$$$"
  F027  monte de brutos, foscos
  F028  etiqueta "PREÇO MÉDIO DO BRUTO" cai no monte
texto na tela: "BRUTO" (F028)
som: sininho de loja (F026) · pedras rolando (F027)

### C016 — F029–F031
tipo: mapa
cenário: mapa-múndi simples (próprio) com pontos nas minas (Rússia, Botsuana, Canadá, Angola, África do Sul, Austrália)
planos:
  F029  pontos acendem um por um + contador "98,8 MI QUILATES"
  F030  contador "US$ 9,23 BI"
  F031  divisão aparece: "= US$ 93 / QUILATE"
texto na tela: os 3 contadores
som: sonar a cada ponto · ka-ching no resultado

### C017 — F032–F035
tipo: texto
cenário: conta montada linha por linha, fundo escuro com grade
planos:
  F032  "1.950.000 × US$ 93"
  F033  "= US$ 182 MILHÕES"
  F034  pedra bruta suja de terra no canto + carimbo "SEM LAPIDAR"
  F035  "× R$ 5,51" e os dígitos começam a girar
som: teclado rápido · tique de contador

### C018 — F036 + pausa de cena 10 s
tipo: jogo
mundo: mv_void
local: 0 66 0 · hora 18000 · tick congelado: não
cenário:
  - item_grande diamante, escala 6, girando
  - text_display "R$ 1.000.000.000" em 0 73 0 (aparece em "Um bilhão")
câmera:
  movimento: órbita 90° bem lenta (18 pontos)
  de: 0 67 −14 · yaw 0 · pitch 5   →   para: −14 67 0 · yaw −90 · pitch 5
  duração: F036 + pausa
efeitos (pós): flash branco + raios de luz do shader
texto na tela: "UM." (pop pequeno no fim da frase)
som: boom grave com reverb · música: piano sobe na pausa

### C019 — F037–F038
tipo: estudio3d
cenário: gema rosa lapidada (modelo próprio) num pedestal; ao lado 2,5 gemas "fantasmas" que somam o valor do diamante do Minecraft
planos:
  F037  gema rosa + "US$ 71,2 MI"
  F038  diamante do Minecraft desce do alto; aparecem as 2,5 gemas
texto na tela: "PINK STAR · 2017" · "× 2,5"
som: ding · pop

### C020 — F039
tipo: jogo
mundo: mv_cine
local: lago de lava numa caverna · Y −55 · tick congelado: não
ações: +0,0 `/summon item X Y+3 Z {Item:{id:"minecraft:diamond",count:1},Motion:[0.0,0.1,0.15]}` cai na lava e some
câmera: estática, plano médio da lava
efeitos (pós): câmera lenta 50% na queda
texto na tela: "R$ 1 BI" seguindo o item, depois "R$ 0"
som: chiado da lava (`entity.generic.burn`) · disco arranhando em "Eu vi"

### C021 — F040–F041
tipo: texto
cenário: calendário de parede passando folhas muito rápido
texto na tela: contador "47.600 ANOS" · F041: "SEM FÉRIAS" (carimbo vermelho)
som: folhas virando + relógio tiquetaqueando · carimbo

### C022 — F042–F043
tipo: jogo
mundo: mv_void
local: palco · hora 18000
cenário: 4 item_display em fila (diamante, ouro, ferro, esmeralda), escala 2, só o diamante aceso (os outros chegam em F042); em F043 o diamante desce 1 bloco
câmera: estática frontal, 0 66 −8
texto na tela: "?" sobre o diamante (F043)
som: pop por item · nota grave de mistério em F043 · música: corta para o pizzicato

## B4 — A tabela de preços

### C023 — F044–F046
tipo: jogo
mundo: mv_void
local: escritório do Avaliador (`/place template cenas:escritorio 0 63 0`) · hora 18000 · tick congelado: não
elenco:
  - AVALIADOR: villager bibliotecário com monóculo, atrás do púlpito, olhando para a câmera
ações:
  F044 início  porta abre (som) e a câmera entra
  F045 +0,8  zoom brusco no rosto (pós)
  F046 início  AVALIADOR: `entity.villager.ambient` + balão text_display "Hrmm." (1,5 s)
câmera:
  movimento: dolly in
  de: 0 65,5 −6 · yaw 0 · pitch 0   →   para: 0 65,5 −2,5 · yaw 0 · pitch 0
efeitos (pós): zoom brusco em F045 · cartão "O AVALIADOR" com fonte serifada pequena no canto
texto na tela: "O AVALIADOR" (F045)
som: porta de madeira do jogo · música: pizzicato cômico

### C024 — F047–F049
tipo: estudio3d
cenário: bloco de ouro se divide em 9 barras; 1 barra vai para uma balança de caminhão
planos:
  F047  bloco → 9 barras
  F048  "19.300 kg / m³"
  F049  barra na balança: "2.144 kg"
som: metal batendo · balança

### C025 — F050–F052
tipo: jogo
mundo: mv_void
local: escritório, item_display `gold_ingot` grande em cima do púlpito
ações: F052 início `/particle minecraft:wax_on 0 66 1 0.4 0.4 0.4 0 30` (brilho)
câmera: estática, close no púlpito, 0 65,8 −1,5
texto na tela: "R$ 714 / GRAMA" (F050) · contador "R$ 1,5 BI" (F052, pop)
som: ka-ching forte em "um bilhão e meio"

### C026 — F053–F055
tipo: jogo
mundo: mv_void
local: escritório + 2 pedestais (`quartz_pillar`) lado a lado
cenário: diamante num pedestal de 2 blocos, ouro num de 3 blocos (fica mais alto)
elenco: AVALIADOR olha para o ouro (`/rotate`), depois para a câmera
ações:
  F053 início  AVALIADOR `entity.villager.yes` + `happy_villager`
  F055  montagem rápida (3 planos de 0,7 s, gravados separados em mv_cine): relógio (item_display `clock`) · maçã dourada · piglin pegando barra de ouro (piglin NoAI com `gold_ingot` na mão, `/summon piglin ... {NoAI:1b,HandItems:[{id:"minecraft:gold_ingot",count:1},{}]}`)
câmera: F053–F054 estática nos 2 pedestais · F055 cortes secos
texto na tela: "+50%" (F054)
som: "hrmm" · pop em cada plano da F055 · som do piglin admirando

### C027 — F056–F060
tipo: estudio3d
cenário: lingote de ferro gigante; ao lado um celular simples (modelo low poly próprio)
planos:
  F056  lingote entra
  F057  "875 kg"
  F058  "US$ 90 / TONELADA"
  F059  contador para em "R$ 702"
  F060  celular aparece ao lado com o mesmo preço
texto na tela: os números acima
som: bigorna do jogo (`block.anvil.land`) em F056 · ka-ching fraquinho (efeito "triste") em F059

### C028 — F061–F063
tipo: jogo
mundo: mv_cine
local: vila de planície (coordenadas do /locate) · hora 6000
elenco:
  - golem de ferro andando pela rua (IA normal, só 1)
  - AVALIADOR (F063): corte para o escritório em mv_void
ações: F063 início AVALIADOR `entity.villager.no` + `angry_villager`, vira o rosto (`/rotate` 60°)
câmera:
  F061–F062: travelling ao lado do golem, câmera baixa
  de: XV−6 YV+1 ZV · yaw 90 · pitch 0   →   para: XV−6 YV+1 ZV+8 · yaw 90 · pitch 0
  F063: estática no Avaliador
texto na tela: "4 BLOCOS = R$ 25 MIL" (F061) · "< CARRO POPULAR" (F062)
som: passos pesados do golem · "no" do villager

### C029 — F064–F067
tipo: jogo
mundo: mv_void
local: palco · hora 18000
cenário: item_grande trocado para `emerald` (`/data merge entity @e[tag=item_grande,limit=1] {item:{id:"minecraft:emerald",count:1}}`), girando
câmera: órbita 60°, 0 67 −10 → −8 67 −6
texto na tela: "307 kg" (F065) · "1,5 MI QUILATES" · "US$ 9,72 / QUILATE" (F066) · "R$ 82 MI" (F067)
som: pop em cada número · ka-ching em F067

### C030 — F068–F070
tipo: jogo (GUI)
mundo: mv_cine
local: vila, fazendeiro com a troca "1 esmeralda → 6 pães" (se não vier: `/summon villager ... {VillagerData:{profession:"minecraft:farmer",level:1,type:"minecraft:plains"},Offers:{Recipes:[{buy:{id:"minecraft:emerald",count:1},sell:{id:"minecraft:bread",count:6},maxUses:12}]},NoAI:1b}`)
ações:
  F068  câmera no rosto do fazendeiro
  F069  abre a tela de troca (gravar com interface) — **silêncio de 1 s** antes
  F070  sai da tela; pães caem do céu (`/summon item` × 6 em cima da câmera)
câmera: 1ª pessoa
efeitos (pós): F069 zoom lento na linha da troca
texto na tela: "R$ 82 MI" sobre a esmeralda e "6 PÃES" (F069) · "R$ 13,7 MI / PÃO" (F070)
som: música corta seco em F069 · "hrmm" do villager · F070 "boing" e a música volta

### C031 — F071–F073
tipo: jogo (GUI) → jogo
mundo: mv_cine (troca) e mv_void (Avaliador)
local: armeiro nível 3 com a troca "1 diamante → 1 esmeralda" (mesmo truque de `Offers` da C030 com `buy:{id:"minecraft:diamond",count:1}`, `sell:{id:"minecraft:emerald",count:1}`)
ações:
  F071  tela de troca aberta
  F072  carimbo "GOLPE" na tela
  F073  corte: AVALIADOR vira de costas rápido (`/rotate @e[tag=avaliador,limit=1] 0 0`, 0,3 s) e assobia (balão "♪")
câmera: F073 estática no escritório
texto na tela: "R$ 1 BI → R$ 82 MI" (F071) · "GOLPE" (F072, carimbo vermelho)
som: disco arranhando no "golpe" · carimbo · assobio curto

### C032 — F074
tipo: jogo
mundo: mv_void
local: escritório; `netherite_ingot` (item_display) no púlpito
elenco: AVALIADOR
ações: +1,5 item_display desliza 1 bloco para fora do púlpito (interpolação 10 ticks) e cai do palco · AVALIADOR `entity.villager.no`
câmera: estática, close no púlpito
texto na tela: "SEM PREÇO" (carimbo cinza)
som: "no" do villager · objeto caindo longe (eco)

## B5 — Um pack

### C033 — F075–F077
tipo: jogo (GUI)
mundo: mv_void
ações:
  F075  inventário com 1 diamante → `/give @s minecraft:diamond 63` (pilha vira 64)
  F076  zoom no número "64"
  F077  baú simples aberto, 27 pilhas aparecendo uma por uma (`/item replace block X Y Z container.N with minecraft:diamond 64`, 1 por tick)
câmera: 1ª pessoa, GUI
texto na tela: "1 PACK = 64" (F076) · "27 PACKS" (F077)
som: pop de item do jogo a cada pilha (acelerando)

### C034 — F078–F081
tipo: estudio3d
cenário: 2 barras de gráfico 3D feitas de blocos: "1 PACK: 124,8 MI QUILATES" (mais alta) e "TODAS AS MINAS EM 2025: 98,8 MI" (mais baixa)
planos:
  F078  barra do pack sobe
  F079  barra das minas sobe e para abaixo
  F080  câmera passa por cima das duas
  F081  corte para slot do inventário (GUI) com zoom: "R$ 64 BI"
texto na tela: os rótulos das barras · "R$ 64 BI" (F081)
som: tique de contador nas barras · boom em F080

### C035 — F082–F083
tipo: jogo
mundo: mv_cine
local: começa em cima de uma planície, desce reto através do chão até uma caverna (espectador atravessa o chão) · hora 6000
câmera:
  movimento: tilt para baixo + descida (revelação ao contrário)
  de: X 90 Z · yaw 0 · pitch 60   →   para: X −40 Z · yaw 0 · pitch 70
  duração: F082–F083
efeitos (pós): escurece ao passar o chão
texto na tela: "QUANTO?" (F082)
som: whoosh grave descendo · música muda para eletrônica de aula

## B6 — Aula: quanto minério cabe num chunk

### C036 — F084–F086
tipo: mapa → estudio3d
cenário: (F084–F085) vista de cima do mv_cine com a grade de chunks desenhada na pós; um chunk destacado em amarelo · (F086) estúdio: coluna 16 × 16 × 384 (blocos) do céu à bedrock, com régua
planos:
  F084  mapa de cima, grade aparece
  F085  1 chunk acende
  F086  coluna 3D sobe do chão do estúdio até o "céu"
texto na tela: "16 × 16" (F085) · "384 BLOCOS" (F086)
som: beep de interface · whoosh longo subindo

### C037 — F087–F090
tipo: estudio3d
cenário: a mesma coluna, em corte; 4 dados (d6 de bloco) rolando; faixas coloridas nas alturas das 4 rodadas do diamante; um triângulo de distribuição ao lado; a parte do triângulo abaixo da bedrock fica vermelha
planos:
  F087  dados rolando
  F088  aparecem 7 + 4 + 2 veios nas alturas certas
  F089  1 veio grande brilha (texto "1 a cada 9 chunks")
  F090  metade do triângulo fica vermelha ("fora do mundo") + uma caverna "come" um veio
texto na tela: "7 + 4 + 2 + 1/9" (F088) · "FORA DO MUNDO" (F090)
som: dados de madeira · sonar a cada veio

### C038 — F091–F093
tipo: texto
cenário: tela "laboratório": histograma de 10.000 chunks simulados formando um sino; a média marcada
planos:
  F091  "FONTES DISCORDAM: 3,1 · 3,7 · 5 · ?" (riscados um por um)
  F092  histograma se montando
  F093  linha da média: "≈ 15 / CHUNK" + nota cinza minúscula "estimativa · faixa 10–20"
som: teclado · tique · ding na média

### C039 — F094
tipo: jogo
mundo: mv_cine
local: túnel dentro de uma montanha a Y 120 (bem longe do fundo) · hora 6000
elenco: VOCÊ com picareta, de costas, olhando para a parede de pedra
câmera: estática, plano médio; texto de altura na pós
texto na tela: "Y = 120" (pequeno, canto) · "LUGAR ERRADO" (F094 fim)
som: picareta batendo em pedra (som do jogo) × 3 · grilo (silêncio cômico)

### C040 — F095–F096
tipo: jogo
mundo: mv_cine
local: (F095) badlands do /locate · (F096) pico de montanha · hora 12500 · tick congelado: não
câmera: F095 drone lateral sobre as mesas · F096 drone subindo pela montanha
texto na tela: "+ OURO" (F095) · "+ FERRO" (F096) · "ouro ≈ 15 · ferro ≈ 50 por chunk" (pequeno)
som: whoosh entre os 2 planos

### C041 — F097–F098 + pausa de cena 10 s
tipo: jogo
mundo: mv_cine (cópia) → mv_void (cena)
preparo (antes de gravar, pelo MCP + WorldEdit):
  1. Em mv_cine, escolher 5 chunks fora de oceano: `//pos1 X0,-64,Z0` `//pos2 X0+15,319,Z0+15` → `//count diamond_ore,deepslate_diamond_ore` · `//count gold_ore,deepslate_gold_ore` · `//count iron_ore,deepslate_iron_ore`. Anotar no fatos.md §B. Usar o chunk mais perto da média.
  2. `//copy` → `//schem save chunk_real` → em mv_void: `//schem load chunk_real` → `//paste` com a base em 0 −64 0
  3. `//replace "!diamond_ore,deepslate_diamond_ore,gold_ore,deepslate_gold_ore,iron_ore,deepslate_iron_ore" air` (se o "!" não negar a lista toda: `//gmask` com a lista e `//set air` no inverso)
  4. Luz: `//replace air light[level=12]` dentro da mesma seleção (bloco de luz é invisível)
local: centro do chunk 8 128 8 · mv_void · hora 18000 · tick congelado: sim
cenário: só os minérios flutuando, nos lugares reais; nada mais
câmera:
  movimento: órbita completa 360° descendo (36 pontos), de cima até a altura do fundo
  de: 30 200 8 · yaw 90 · pitch 35   →   para: 30 −40 8 · yaw 450 · pitch 10 (raio 22)
  duração: F097–F098 + pausa
efeitos (pós): na pausa, contorno fino do chunk (linhas brancas)
texto na tela: "1 CHUNK DE VERDADE" (F097) · "15 · 15 · 50" pequenos com ícones (fim da pausa)
som: whoosh na entrada · boom grave em "Olha ele aqui" · música sobe na pausa

### C042 — F099–F102
tipo: jogo
mundo: mv_void
local: o mesmo chunk de minérios, câmera de frente
cenário: text_display flutuando ao lado de cada grupo (escala 2)
planos:
  F099  diamantes piscam (`/particle minecraft:glow` em cada um) + "15 × R$ 1 BI"
  F100  ouros piscam + "15 × R$ 1,5 BI"
  F101  ferros piscam + "50 × R$ 702"
  F102  tudo pisca + total
câmera: estática, 8 128 −30 · yaw 0 · pitch 0
texto na tela: "R$ 15 BI" · "R$ 23 BI" · "R$ 35 MIL" · "R$ 38 BILHÕES" (F102, grande)
som: ka-ching a cada grupo (o do ferro é um "plim" fraquinho) · boom no total

### C043 — F103
tipo: estudio3d
cenário: quadrado de grama 16 × 16 (blocos); embaixo dele, 97 gemas rosas em fila
câmera: travelling de cima, passando sobre as gemas
texto na tela: "≈ 97 PINK STARS"
som: tilintar de vidro em cascata

### C044 — F104–F106
tipo: mapa
cenário: mapa do Brasil (próprio, simples); Acre e Roraima acendem
planos:
  F104  estados acendem + "0,2% DO PIB (cada)"
  F105  "≈ R$ 22 BI / ANO"
  F106  barra "1 CHUNK = R$ 38 BI" passa por cima da barra do estado
texto na tela: os 3 números
som: beep · ka-ching · boom curto

### C045 — F107
tipo: jogo
mundo: mv_cine
local: planície · hora 6000
elenco: VOCÊ andando em direção a uma árvore com machado (`/tp` em passos a cada tick, 3 s)
câmera: travelling lateral
efeitos (pós): grade de chunks desenhada no chão, cada chunk que ele pisa pisca "R$ 38 BI"
texto na tela: "R$ 38 BI" piscando a cada passo
som: passos na grama + "plim" a cada chunk · música: orquestra começa a crescer

## B7 — O baú e o cubo de ouro

### C046 — F108–F110
tipo: jogo (GUI)
mundo: mv_void
cenário:
  - `/setblock 0 64 0 minecraft:chest[facing=south,type=left]` e `/setblock 1 64 0 minecraft:chest[facing=south,type=right]` (conferir no print se os lados casaram)
  - função `cenas:util/encher_bau_duplo`: 54 × `/item replace block <metade> container.N with minecraft:diamond_block 64`
ações:
  F108  baú fechado no palco, câmera chega
  F109  abre (som) → GUI com as 54 pilhas
  F110  zoom no "64" de uma pilha
câmera: F108 dolly in de 0 66 −6 → 0,5 65,6 −2 · F109–F110 1ª pessoa GUI
texto na tela: "54 × 64 BLOCOS" (F110)
som: baú abrindo (jogo) · coral curto "aah" na GUI

### C047 — F111–F114
tipo: estudio3d
cenário: 2 cubos de diamante de verdade (material diamante): "TODA A HISTÓRIA" = cubo de 7 m (6 bi ct = 1.200 t = 342 m³) e "1 BAÚ" = cubo de 15 m (60,7 bi ct = 12.130 t = 3.456 m³); bonequinho de 1,8 m entre eles
planos:
  F111  contador "31.104 DIAMANTES" → "60 BI QUILATES"
  F112  cubo pequeno aparece com "?"
  F113  rótulo "≈ 6 BI QUILATES · DESDE SEMPRE" + ícones aliança/colar/broca
  F114  cubo grande desce do céu ao lado: "× 10"
texto na tela: números acima
som: tique de contador · boom grave em F114

### C048 — F115–F117 + pausa de cena 12 s
tipo: jogo
mundo: mv_void
local: 0 64 0 · hora 13000 (pôr do sol do shader) · tick congelado: não
cenário: cubo de bloco de diamante 15 × 15 × 15 (`/fill 0 64 0 14 78 14 minecraft:diamond_block`, dividir em 2 comandos se passar do limite de 32.768: aqui são 3.375, cabe) + 81 blocos soltos em cima (o resto até 3.456)
elenco: VOCÊ no chão ao lado do cubo, olhando para cima
câmera:
  movimento: câmera baixa → revelação subindo
  de: −3 64,3 −4 · yaw −30 · pitch −40   →   para: −20 95 −20 · yaw −45 · pitch 30
  duração: F115 até o fim da pausa
texto na tela: "R$ 31 TRILHÕES" (F115) · "PIB DO BRASIL: R$ 12,7 TRI" (F116) · "≈ 2,5 BRASIS" (F117, pop)
som: boom em F115 · música épica sobe na pausa

### C049 — F118–F122
tipo: jogo
mundo: mv_void
local: 40 64 0 · hora 13000
cenário: cubo de ouro 22 × 23 × 22 (`/fill 40 64 0 61 86 21 minecraft:gold_block` = 11.132 blocos; dividir em 1 comando, cabe), construído em 3 camadas no tempo (efeito de "subir")
elenco: VOCÊ ao pé do cubo (escala)
planos:
  F118  terreno vazio
  F119  "≈ 220 MIL TONELADAS" (WGC)
  F120  cubo sobe em 3 etapas (`/fill` por terços)
  F121  plano geral do cubo pronto
  F122  prédio de 7 andares (silhueta 2D na pós) ao lado, mesma altura
câmera: órbita lenta, raio 45
texto na tela: "102 MIL BARRAS · 11.400 BLOCOS" (F120) · "22,5 BLOCOS" + régua (F121) · "≈ 7 ANDARES" (F122)
som: blocos colocados em sequência (som do jogo) · boom em F121

### C050 — F123
tipo: jogo
mundo: mv_void
local: ao lado do cubo de ouro
cenário: campo de abóboras 40 × 40 (`/fill 70 64 0 109 64 39 minecraft:pumpkin`) com água em linhas (/fill a cada 9 blocos)
câmera: drone alto passando do cubo de ouro para a farm
texto na tela: "MAIOR QUE TODO O OURO DA TERRA" (pequeno, irônico)
som: disco arranhando no fim · marimba cômica 2 s

### C051 — F124
tipo: jogo
mundo: mv_cine
local: o baú duplo copiado para perto do spawn, numa planície · hora 12500
câmera:
  movimento: revelação: sobe de 2 m até 250 m olhando para baixo
  de: X 66 Z−3 · yaw 0 · pitch 50   →   para: X 250 Z−60 · yaw 0 · pitch 60
efeitos (pós): no fim, o baú vira um pontinho com um círculo branco
texto na tela: —
som: whoosh longo subindo

### C052 — F125
tipo: jogo
mundo: mv_void (escritório)
elenco: AVALIADOR segurando um pão (item_display `bread` na frente da mão)
ações: +0,0 AVALIADOR `entity.villager.yes`
câmera: estática, plano médio
texto na tela: "SE INSCREVE · GRÁTIS" (pequeno, canto) · nota cinza "pão: R$ 13,7 mi"
som: pop · sem botão de inscrição animado chamativo (é 1 menção, leve)

## B8 — Em volta do spawn

### C053 — F126–F129
tipo: mapa
cenário: render de cima de 2.000 × 2.000 blocos em volta de 0,0 do mv_cine; ponto "SPAWN" no centro; grade de chunks
planos:
  F126  zoom out do spawn até ±1.000
  F127  grade acende chunk por chunk, contador "15.625 CHUNKS"
  F128  "× R$ 38 BI"
  F129  contador sobe até "R$ 594 TRILHÕES"
texto na tela: "1.000 BLOCOS" (régua, F126) · contadores
som: sonar · tique acelerado · boom em F129

### C054 — F130–F132
tipo: espaco
cenário: Terra girando com anel de barras de PIB de países em volta (genérico, sem bandeiras); ao lado, o quadrado do mapa 2.000 × 2.000
planos:
  F130  barras somam "US$ 117 TRI"
  F131  "= R$ 646 TRI"
  F132  barra do mapa sobe e para quase na mesma altura: "92%"
texto na tela: números acima
som: whoosh · boom

### C055 — F133–F135
tipo: jogo
mundo: mv_cine
planos:
  F133  VOCÊ em pé na frente de um baú vazio (GUI aberta vazia, 1 s) — pose triste (agachado)
  F134  3 planos rápidos (0,8 s cada): montanha, badlands, Nether (portal + `/execute in minecraft:the_nether run tp`), cada um com "+" na pós
  F135  drone sobe do spawn e o Distant Horizons mostra o terreno sumindo no horizonte
câmera: F135 de X 120 Z · pitch 20 → X 400 Z+200 · pitch 15
texto na tela: "SEM BALDE" (F133, pequeno) · "+ + +" (F134)
som: "hrmm" triste (pitch baixo) · whoosh × 3 · música cresce

## B9 — O mundo inteiro

### C056 — F136–F137
tipo: jogo → mapa
mundo: mv_cine
local: perto da borda: `/tp @s 29999900 100 0` (gera chunks lá, demora: pré-gerar com `/chunky center 29999900 0` + `/chunky radius 200`) · hora 6000
planos:
  F136  parede da borda listrada, câmera andando de frente até ela; coordenada X na pós
  F137  mapa: quadrado inteiro, spawn é um pixel; "60.000.000 × 60.000.000"
câmera: F136 dolly in até 3 blocos da borda
texto na tela: "X = 29.999.984" (F136) · "60 MILHÕES" (F137)
som: zumbido grave da borda · whoosh para o mapa

### C057 — F138–F139
tipo: espaco
cenário: a casca da Terra "descascada" em 7 placas iguais encostando no quadrado do Minecraft até cobrir tudo
texto na tela: "× 7 TERRAS" (F138) · "14 TRILHÕES DE CHUNKS" (F139)
som: placas encaixando (clunk) · boom

### C058 — F140–F141
tipo: jogo
mundo: mv_cine
local: estrada reta longa (`/fill` de 400 blocos de `dirt_path` numa planície plana) · hora passando (timelapse: `/time add 100` a cada tick só nesta cena)
elenco: VOCÊ andando (passos de `/tp` 4,317 m/s)
câmera: travelling ao lado, depois a câmera fica e ele some no horizonte
efeitos (pós): timelapse; contador "DIA 161"
texto na tela: "161 DIAS SEM PARAR" (F140) · pilha de pães na pós "R$ ???" (F141)
som: relógio tiquetaqueando · passos acelerados · "boing" em F141

### C059 — F142–F145
tipo: texto
cenário: contador gigante em fonte mono; dígitos correm até "R$ 535.000.000.000.000.000.000.000"
planos:
  F142  "14 TRI × R$ 38 BI"
  F143  número completo + "SEXTILHÕES"
  F144  calculadora de celular desenhada mostrando "5.35e23"
  F145  pilha de notas do mundo inteiro (ícone) "≈ US$ 100 TRI" + nota cinza "estimativas: 55 a 130"
som: tique acelerado → boom em F143 · beep de calculadora (F144)

### C060 — F146–F147 + pausa de cena 15 s
tipo: espaco → jogo
planos:
  F146  espaco: a pilha de dinheiro do mundo vira um ponto do lado do quadrado do Minecraft; "≈ 1 BILHÃO DE VEZES"
  F147 + pausa  jogo mv_cine: o maior voo do vídeo — drone longo sobre montanhas e oceano ao pôr do sol, DH 512 chunks
mundo: mv_cine · hora 12800 · tick congelado: não
câmera (jogo):
  movimento: drone para a frente, devagar, alto
  de: X 220 Z · yaw 30 · pitch 15   →   para: X+600 200 Z+350 · yaw 35 · pitch 12
  duração: F147 + pausa (≈ 23 s)
texto na tela: "R$ 535 SEXTILHÕES" some aos poucos
som: boom em F146 · música épica com coral no máximo na pausa

## B10 — Todas as seeds

### C061 — F148–F149
tipo: jogo (GUI)
mundo: menu do jogo
ações: tela "Criar novo mundo" → "Mais opções" → campo "Semente" digitando "QUANTO VALE ISSO" (texto vira número; piada escondida)
câmera: captura de tela, sem rig
efeitos (pós): zoom no campo
texto na tela: "2⁶⁴" (F149) · "18.446.744.073.709.551.616" rolando
som: teclado · clique

### C062 — F150
tipo: estudio3d
cenário: macro de areia (grãos como pequenos blocos de `sand` arredondados); ao lado, uma ampulheta
texto na tela: "7,5 × 10¹⁸ GRÃOS" vs "1,8 × 10¹⁹ SEEDS" · "× 2,5"
som: areia escorrendo

### C063 — F151–F152
tipo: estudio3d
cenário: parede de 64 "janelas" (prints do spawn de 64 seeds diferentes — o usuário cria os mundos e o Claude tira o print com F2; **manual**), a câmera recua e a parede vira um mosaico infinito
câmera: dolly out rápido
texto na tela: "14 TRI DE CHUNKS · CADA" (F151)
som: whoosh + cliques de câmera em cascata

### C064 — F153–F155
tipo: texto → jogo
planos:
  F153  número de 43 algarismos rolando na horizontal: "≈ 10 TREDECILHÕES"
  F154  o número fica tão comprido que sai da tela; carimbo "NINGUÉM MERECE"
  F155  jogo mv_void: item_grande diamante na frente de um monitor (moldura de `black_concrete` 8 × 5 com mapa do mundo pintado em `map` item_frame)
câmera: F155 dolly out lento
som: tique · carimbo · nota grave longa

## B11 — A virada

### C065 — F156–F157
tipo: jogo
mundo: mv_void
local: 0 64 0 · hora 18000 · neblina forte
cenário: montanha de blocos de diamante (`/fill` em degraus: 20 × 20 base, 6 camadas encolhendo) — guardar como estrutura `cenas:monte_diamante`
câmera: estática frontal de baixo, 0 64,5 −25 · pitch −10
efeitos (pós): dessatura 40%
texto na tela: —
som: **música corta seco** em F156 · drone escuro entra · silêncio de 1 s antes de F157

### C066 — F158–F161
tipo: estudio3d
cenário: gráfico de oferta e procura em blocos: linha de preço (feita de blocos de diamante) despencando
planos:
  F158  1 pack entra no mercado (caixa com o ícone)
  F159  linha despenca
  F160  rótulos "OFERTA" e "PROCURA"
  F161  diamante brilhando igual, etiqueta de preço encolhendo
texto na tela: "OFERTA E PROCURA" (F160)
som: queda de elevador (whoosh descendo) em F159

### C067 — F162–F164
tipo: estudio3d
cenário: pote de pó de diamante industrial com etiqueta "US$ 0,04 / QUILATE"; contador; ícone de apartamento simples
planos:
  F162  pote + etiqueta
  F163  diamante do Minecraft na balança + "?"
  F164  contador "R$ 429.780" + apartamento aparece
som: ka-ching pequeno · "hmm" curto

### C068 — F165
tipo: jogo
mundo: mv_void
local: a mesma montanha da C065
ações: +0,0 função `cenas:virar_cascalho`: de cima para baixo, 1 camada a cada 10 ticks, `/fill ... minecraft:gravel replace minecraft:diamond_block` (o cascalho cai e escorre)
câmera: estática geral, depois câmera baixa no cascalho caindo
texto na tela: "= CASCALHO" (F165 fim)
som: cascalho caindo (som do jogo, em camadas)

### C069 — F166–F168 + pausa de cena 12 s
tipo: jogo
mundo: mv_void
local: frente do monte de cascalho · hora 18000
elenco: VOCÊ em pé, sozinho, olhando o cascalho; em F168 vira a cabeça para a câmera (`/rotate` em 1 s)
câmera:
  movimento: dolly out bem lento
  de: 0 65,6 −4 · yaw 0 · pitch 5   →   para: 0 66 −16 · yaw 0 · pitch 5
  duração: F166 até o fim da pausa
efeitos (pós): na pausa, fade lento para a caverna da C001 (o veio de diamante)
texto na tela: —
som: drone some · **piano começa** na pausa

## B12 — A lição

### C070 — F169–F173
tipo: jogo
mundo: mv_cine
local: o veio da C001 · Y −58
elenco: VOCÊ (com `iron_pickaxe`) de frente para o minério
ações: F169 +1,0 o minério quebra (`/setblock ... air destroy`) e o diamante salta
câmera: câmera baixa, close no rosto do VOCÊ → no diamante
efeitos (pós): vinheta branca suave (memória) em toda a cena
texto na tela: "30 MIN × R$ 7,37" (F172) · "= R$ 3,69" (pop) · F173: "TEMPO" (branco, fino)
som: relógio tiquetaqueando baixo (F173) · piano

### C071 — F174–F176
tipo: jogo
mundo: mv_cine
local: casinha de terra da C006 · timelapse do dia (`/time add 40` por tick, 8 s)
efeitos (pós): contador "500 HORAS" · F175 "R$ 3.685" · F176 o número é riscado
câmera: estática, plano geral da casinha
som: piano · tique

### C072 — F177–F178
tipo: jogo
mundo: mv_cine
local: casinha de terra (XC YC ZC) · hora 23500 (nascer do sol) · tick congelado: não
cenário:
  - ponte de madeira pela metade sobre um rio perto (`/fill` de `oak_planks` 12 blocos + 3 blocos faltando + 1 `scaffolding`)
  - lobo deitado: `/summon minecraft:wolf XC+2 YC ZC−2 {CustomName:"Biscoito",CustomNameVisible:1b,Sitting:1b,NoAI:1b,Owner:<UUID do jogador de gravação>}` (o Claude pega o UUID com `/data get entity @s UUID`)
  - placa ao lado de uma cama vazia: `/setblock XC+1 YC ZC+3 minecraft:oak_sign[rotation=8]{front_text:{messages:["volto","amanhã","",""]}}`
planos:
  F177  casinha de terra, plano geral
  F178  3 planos: ponte pela metade · Biscoito · placa "volto amanhã" ao lado da cama vazia
câmera: F178 câmera baixa em cada plano, estática
texto na tela: — (nada: a imagem fala)
som: passarinhos (jogo) · lobo respirando · piano

### C073 — F179–F181
tipo: jogo
mundo: mv_cine
local: casinha de terra → céu · hora 0 (manhã)
câmera:
  movimento: revelação: sobe da porta da casinha até 300 m, DH mostrando o mundo enorme
  de: XC YC+1,6 ZC−3 · yaw 0 · pitch 0   →   para: XC 300 ZC−150 · yaw 0 · pitch 35
  duração: F179–F181
efeitos (pós): no fim, a casinha fica com um contorno branco fino (o único ponto marcado no mapa inteiro)
texto na tela: "1 DE 18.446.744.073.709.551.616" (F180, pequeno, embaixo)
som: piano + cordas sobem

### C074 — F182 + pausa de cena 10 s
tipo: jogo
mundo: mv_cine
local: casinha de terra, de perto · hora 0
elenco: VOCÊ na frente da casinha, mão para a frente
ações: F182 em "com a sua mão": `/setblock XC+3 YC ZC−1 minecraft:dirt` (1 bloco de terra aparece, com som de colocar) + partícula `happy_villager` suave
câmera:
  movimento: dolly in lento até o bloco novo
  de: XC+3 YC+1,2 ZC−6 · yaw 0 · pitch 10   →   para: XC+3 YC+0,8 ZC−2,5 · yaw 0 · pitch 15
  duração: F182 + pausa
efeitos (pós): na pausa, fade para branco lento
texto na tela: — (nenhum: deixa a frase sozinha)
som: som de colocar terra (jogo) bem nítido, música dá 1 s de silêncio antes e volta no máximo na pausa

### C075 — F183
tipo: texto
cenário: card final escuro com o nome do canal e o diamante girando pequeno
texto na tela: "OBRIGADO" + espaço para a tela final do YouTube (20 s)
som: piano fecha · música termina
