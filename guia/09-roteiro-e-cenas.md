# Roteiro com tom e pausa + arquivo de cenas para o MCP

Cada vídeo tem 2 arquivos de texto, em `videos/NN_tema/`:
- `roteiro.md` — só o que **você fala**: cada frase com tom e pausa. É o que você lê para gravar.
- `cenas.md` — só o que o **Claude faz no jogo**: cenário, personagens, NPCs, expressões, movimentos e câmera, ligados às frases do roteiro.

Os 2 se ligam pelo código da frase: `F001`, `F002`...

## 1. Formato do roteiro (`roteiro.md`)
```
# QUANTO VALE UM MUNDO DO MINECRAFT?
Alvo: 22 min · ~3.100 palavras · 140 palavras/min

## B1 — Abertura (0:00–0:40)
F001 [curioso · devagar] Quanto vale o seu mundo do Minecraft?
     [pausa 1 s]
F002 [leve · normal] Imagina que você tá minerando, de boa, e acha um diamante.
     [pausa 0,5 s]
F003 [piada · cara séria] Você grita igual criança. Eu sei. Eu também.
     [pausa 1,5 s]
F004 [épico · grave · devagar] Nesse vídeo, eu vou mostrar que o seu mundo vale mais do que todo o dinheiro da Terra.
     [pausa de cena 15 s]
```
Regras:
- **1 frase = 1 linha = 1 código F.** Frase curta (até ~20 palavras). Frase longa vira 2 Fs.
- Tom sempre no começo, entre colchetes, com até 3 palavras do dicionário abaixo.
- Pausa sempre depois da frase.
- Os números escritos como você vai falar ("quatro vírgula sete", não "4,7"), para não travar na gravação.

### Dicionário de tons
| Tom | Como falar |
|---|---|
| curioso | sobe no fim, como pergunta de verdade, volume médio |
| leve | conversa com amigo, sorrindo |
| didático | claro e um pouco mais rápido, ênfase no número |
| empolgado | mais rápido e mais alto, energia |
| piada | cara séria, sem rir; a graça é o contraste |
| irônico | arrastado, como quem já sabe a resposta |
| mistério | baixo, devagar, quase sussurro |
| sério | firme, sem sorriso, velocidade normal |
| épico | grave, devagar, pausa entre blocos de palavras |
| espanto | começa normal e quebra ("isso é... absurdo") |
| triste | baixo, devagar, voz mais "para dentro" |
| personagem: NOME | voz do NPC (villager, robô...); diga como: aguda, grave, sotaque |

Velocidade: `devagar` (~110 palavras/min), `normal` (~140), `rápido` (~170).

### Dicionário de pausas
| Marca | Na gravação | Para que serve |
|---|---|---|
| `[pausa 0,5 s]` | respiro curto | separar ideias |
| `[pausa 1–2 s]` | silêncio de verdade | deixar o número ou a piada assentar |
| `[pausa de cena N s]` (5–20 s) | **deixe só 2 s**; o Claude estica na montagem até N | música sobe, câmera mostra a cena (as "pausas de música" do TheLuics) |

## 2. Gravar e mandar a voz
1. Leia o roteiro em voz alta 1 vez antes.
2. Grave em blocos (B1, B2...). Errou? Repita a frase inteira e corte o erro na edição.
3. Edite: corte erros e respiros, limpe ruído, deixe as pausas como no roteiro.
4. Exporte **1 arquivo**: `videos/NN_tema/voz.wav` (48 kHz, mono ou estéreo).
5. Diga ao Claude: "voz pronta do vídeo NN". O resto é dele.

O Claude roda `ferramentas/alinhar_voz.py` e gera `tempos.json` com o início e o fim de cada F na sua voz. Todo o vídeo é montado nesses tempos.

## 3. Formato das cenas (`cenas.md`)
Uma ficha por cena. Uma cena cobre 1 ou mais frases seguidas.
```
### C004 — F004 + pausa de cena 15 s
tipo: jogo            # jogo | estudio3d | espaco | mapa | texto
mundo: estudio_void    # qual mundo de gravação
local: 0 80 0 · overworld · hora 12500 (fim de tarde) · sem chuva · tick congelado: não
cenário:
  - /place structure minecraft:village_plains 0 64 0
  - pilha de 64 blocos de diamante em 20 70 5 (/fill)
elenco:
  - NARRADOR: mannequin com a skin do canal, pose standing, em 5 64 5, olhando para a pilha
  - VILLAGER "Zé": villager plains/armorer, NoAI, em 8 64 5
ações (tempo a partir do início da F004):
  +0,0  NARRADOR vira a cabeça para a câmera (0,5 s)
  +1,2  Zé: partícula happy_villager + som entity.villager.yes
  F004 fim  Zé anda 3 blocos até a pilha (1,5 s)
câmera:
  movimento: dolly in (vai para a frente devagar), curva suave
  de: 0 90 -20 · yaw 0 · pitch 20   →   para: 0 75 -5 · yaw 0 · pitch 10
  duração: do início da F004 até o fim da pausa de cena
texto na tela: "R$ ???" na F004 (pop)
som: boom grave no fim da F004 · música épica sobe na pausa
```

### Dicionário de câmera (o Claude transforma em comandos)
| Movimento | O que é | Como o Claude faz |
|---|---|---|
| estática | câmera parada | jogador parado em spectator/invisível na posição |
| dolly in / out | vai para a frente / para trás em linha reta | rig de câmera (abaixo) indo de A para B |
| travelling | anda de lado | rig de A para B na lateral |
| drone / sobrevoo | alto, devagar, sobre a paisagem | rig alto, pitch 20–35°, de A para B |
| órbita | gira em volta de algo | rig em pontos de um círculo (12–36 pontos) olhando para o centro |
| tilt / pan | só gira, sem andar | só muda yaw (pan) ou pitch (tilt) |
| revelação | sobe por trás de algo e mostra a cena | rig sobe em Y com pitch caindo |
| câmera baixa | ao nível do chão, faz tudo parecer gigante | Y = chão + 0,3 |
| zoom | aproxima | no jogo não dá zoom por comando: é dolly in; zoom de verdade só na montagem |

**Rig de câmera:** um `text_display` invisível com `teleport_duration` (suaviza o movimento) que o Claude move por uma função do datapack a cada poucos ticks; o jogador fica montado nele (`/ride`), invisível, com a interface escondida (F1).
⚠️ Ainda não testado neste PC. Se ficar tremido, o plano B é o Flashback (câmera manual em keyframes) para aquela cena.

### Dicionário de personagens e expressões
O Minecraft não tem rosto que mexe. "Expressão" vira corpo, cabeça, partícula e som:
| Quero | Como fazer |
|---|---|
| personagem principal (seu boneco) | entidade **mannequin** (Java 1.21.9+) com a sua skin no `profile` |
| pose | mannequin: `standing`, `crouching` (agachado), `sleeping` (deitado), `swimming`, `fall_flying` (voando) · armor stand: braços e pernas em qualquer ângulo (`Pose`) |
| olhar para algo / virar a cabeça | `/rotate` ou `/tp ... facing` em passos (vira em 0,5–1 s) |
| andar até um ponto | `/tp` em passos pequenos a cada tick (as pernas mexem sozinhas) |
| pular / cair | `/tp` em arco ou `Motion` |
| feliz | partícula `happy_villager` / `heart` + som de "yes" do villager |
| bravo | partícula `angry_villager` + som de "no" |
| assustado | recua 1 bloco rápido + som de "hurt" |
| triste | agachado/olhando para baixo + chuva/escuro |
| "falando" | balão com `text_display` em cima (opcional) e som "ambient" do villager |
| segurar item | `/item replace entity ... weapon.mainhand with diamond` |
| morrer | `/damage` ou `/kill` (vira fumaça) |
| ficar parado | NoAI:1b e `immovable` (mannequin) |

### Com mods: gestos, poses e rostos (pesquisa de 12/11/2026, ainda não testado)
Sem mod, a expressão é só corpo, cabeça, partícula e som (tabela acima). Com mods dá para ir além.
Todos precisam rodar na **mesma versão do MCP (Java 1.21.11 Fabric)**. Confira no Modrinth antes de instalar.

| Mod | O que dá | Por comando? | Versão |
|---|---|---|---|
| **Easy NPC** (bundle ou Core + Config UI) | personagens com qualquer skin, poses próprias (braços, pernas, cabeça), diálogos, spawn/despawn por comando | sim (`/easy_npc ...`) | Fabric 1.21.1 e 1.21.11 |
| **Emotecraft x Easy NPC** (+ Emotecraft) | gestos animados no NPC: acenar, bater palma, apontar, dançar, sentar, comemorar... | sim: `/enpcemote play <emote> [max_ticks]` no NPC | Fabric 1.21.9–1.21.11 |
| **Fresh Animations** (pacote de textura) + **EMF** + **ETF** | villagers e mobs piscam, mexem sobrancelha, respiram, rosto mais vivo | **não**: é automático (dá vida, não dá para mandar) | 1.21–1.21.11 |
| **Animated Java** (plugin do Blockbench, exporta datapack) | personagem próprio com rosto que muda (olhos, boca, sobrancelha) e qualquer animação | sim: cada animação é uma `/function` (sem mod) | conferir a versão antes |

Escolha padrão:
1. **Personagem principal e gestos:** Easy NPC + Emotecraft x Easy NPC (no lugar do mannequin). ⚠️ Testar primeiro: uma nota de versão do Easy NPC diz que NPCs humanoides passaram a ignorar "modelos, animações e poses de jogador personalizados". Se o emote não tocar, use um NPC do tipo jogador/outro tipo ou o Animated Java.
2. **Villagers vivos no fundo:** Fresh Animations + EMF + ETF.
3. **Personagem especial que fala e reage com o rosto:** Animated Java (mais tarde; precisa modelar e animar no Blockbench 1 vez).

#### Expressão → o que pôr no `cenas.md`
Com os mods, a ficha da cena usa estas ações. O Claude troca pelo comando certo.
| Expressão / ação | Com Easy NPC + Emotecraft | Com Animated Java | Sem mod (plano B) |
|---|---|---|---|
| acenar / dar oi | `emote: wave` | `anim: acenar` | braço do armor stand para cima e para baixo (`Pose`) |
| bater palma / comemorar | `emote: clap` / `emote: cheer` | `anim: comemorar` | pulos curtos + partícula `happy_villager` |
| apontar para algo | `emote: point` + virar a cabeça | `anim: apontar` | armor stand com braço esticado |
| pensar / dúvida | `emote: think` (mão no queixo) | `anim: pensar` + rosto "dúvida" | cabeça inclinada (`Pose.Head`) |
| surpresa / susto | `emote: shock` | rosto "surpreso" (olho grande, boca aberta) | recua 1 bloco + som de hurt |
| rir | `emote: laugh` | rosto "rindo" + corpo balançando | partícula `note` + som |
| triste | `emote: sad` (cabeça baixa) | rosto "triste" | agachado + olhando para baixo |
| bravo | `emote: angry` | rosto "bravo" (sobrancelha para baixo) | partícula `angry_villager` + som "no" |
| sentar | pose sentado do Easy NPC | `anim: sentar` | armor stand sentado (pernas a 270°) |
| dançar | `emote: dance` | `anim: dancar` | — |
| falar | `emote: talk` (gesto de mão) | boca abrindo e fechando no tempo da frase | balão com `text_display` |

Os nomes dos emotes (`wave`, `clap`...) dependem dos arquivos de emote instalados no Emotecraft. Na instalação, o Claude lista os emotes que existem e atualiza esta tabela com os nomes reais.

Exemplo na ficha:
```
ações (tempo a partir do início da F012):
  +0,0  NARRADOR emote: point (para a mansão), cabeça vira para a mansão
  +1,5  NARRADOR emote: shock
  F013 início  VILLAGER "Zé" emote: laugh
```

## 4. Como o Claude executa (depois de receber a voz)
1. `alinhar_voz.py` → `tempos.json` (início/fim de cada F e das pausas).
2. Para cada cena: converte segundos em ticks (1 s = 20 ticks) e escreve uma função de datapack com o cenário, o elenco, as ações e o caminho da câmera, tudo na hora certa (`/schedule`). Datapack em `saves/<mundo>/datapacks/cenas/`, depois `/reload`.
3. Pelo MCP: entra no mundo certo, roda a montagem do cenário e tira print (`view_capture`) para conferir.
4. Pelo OBS (websocket, porta 4455): começa a gravar → MCP roda `/function cenas:c004` → para a gravação no fim. Anota a diferença de tempo para cortar o começo.
5. Cenas de estúdio 3D/espaço: Blender (quando instalado).
6. Montagem pelos tempos da voz, textos, efeitos, música subindo nas pausas, master -14 LUFS (guias 03 e 05).

Limite do MCP: 60 pedidos por minuto. Por isso o movimento fica dentro do datapack (roda no jogo, a cada tick) e o MCP só dá a ordem.
