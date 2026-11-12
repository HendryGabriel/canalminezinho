# Machinima: cenas de filme com Minecraft

Machinima = filme feito com um jogo. Serve para as esquetes dentro dos documentários e, se quiser, para episódios inteiros.

## 1. Três níveis
| Nível | Onde | Dá para fazer | Limite | Ferramentas |
|---|---|---|---|---|
| 1 — No jogo | Minecraft | personagens parados, andando, virando a cabeça, gestos, sentar, apontar; cortes de câmera | boca não mexe, corpo meio duro | MCP + Easy NPC + Emotecraft + Fresh Animations (guia 09) |
| 2 — Rosto no jogo | Minecraft | boca abrindo no tempo da fala, olhos e sobrancelhas, animações próprias | modelar e animar cada personagem 1 vez no Blockbench | Animated Java (guia 09) |
| 3 — Filme | Blender | atuação completa, luta, mãos pegando coisas, efeitos (aura, raio, explosão), luz de cinema | atuação é trabalho manual (dias por minuto) | Mineways + MCprep (guia 11) |

Regra: comece no nível 1 dentro dos documentários. Suba de nível só na cena que precisa.

## 2. Linguagem de cinema (o que vai no `cenas.md`)
### Planos
| Plano | O que mostra | Quando usar |
|---|---|---|
| grande plano geral | o lugar inteiro, personagem pequeno | abrir a cena, mostrar escala |
| plano geral | o personagem inteiro e o lugar | entrada, ação |
| plano médio | da cintura para cima | conversa |
| primeiro plano / close | rosto e ombros | emoção, fala importante |
| plano detalhe | um objeto (mão, item, bloco) | pista, revelação |
| sobre o ombro | por trás de um, olhando o outro | diálogo (campo e contracampo) |
| contra-plongée | câmera baixa olhando para cima | personagem forte, ameaçador, épico |
| plongée | câmera alta olhando para baixo | personagem fraco, derrotado, sozinho |
| ponto de vista (POV) | o que o personagem vê | susto, descoberta |

### Regras que deixam a cena "de filme"
- **Regra dos 180°:** num diálogo, a câmera fica sempre do mesmo lado da linha entre os 2 personagens. Quem olha para a direita continua olhando para a direita.
- **Campo e contracampo:** fala A → sobre o ombro de B; fala B → sobre o ombro de A.
- **Corte na ação:** corte no meio do movimento (o soco começa num plano e termina no outro).
- **Plano de reação:** depois de uma fala forte, mostre o rosto de quem ouviu.
- **Estabelecimento:** toda cena nova começa num plano geral do lugar (2–3 s).
- **Ritmo:** diálogo calmo = planos de 3–5 s; luta/ação = 0,5–1,5 s.
- **Luz:** 1 luz forte de um lado (sol, tocha, lava) e sombra do outro. Noite + tochas = drama; nevoeiro = mistério.

## 3. Diálogo no roteiro
Cada fala diz quem fala, além do tom:
```
F120 [personagem: KAI · bravo · rápido] Você destruiu a minha vila!
     [pausa 1 s]
F121 [personagem: RONAN · irônico · devagar] Destruí? Eu só... reorganizei.
     [pausa de cena 3 s]
F122 [narrador · sério] E foi aí que a luta começou.
```
- Você grava todas as vozes (como o TheLuics faz). Cada personagem com um jeito fixo de falar, escrito numa ficha `personagens.md` (voz grave/aguda, velocidade, mania).
- Na montagem o Claude pode mudar o tom por personagem (pitch, eco, rádio) para separar as vozes.
- `alinhar_voz.py` funciona igual: cada fala vira um tempo em `tempos.json`.

## 4. Cena no `cenas.md` com plano
```
### C040 — F120–F121
tipo: jogo · nível 1
local: vila destruída, noite, fumaça (campfire), chuva
elenco: KAI (Easy NPC, skin kai.png) em A · RONAN (Easy NPC, skin ronan.png) em B
planos:
  F120  sobre o ombro de RONAN → KAI · KAI emote: point · contra-plongée leve
  F120 fim  close de RONAN (reação), 1 s
  F121  sobre o ombro de KAI → RONAN · RONAN emote: shrug · câmera parada
  pausa  grande plano geral, os 2 pequenos na vila em chamas, travelling lento
som: chuva + fogo · música tensa baixa · trovão no fim da F121
```
Cada linha de `planos` vira uma tomada separada (gravada ou renderizada) e o corte é feito na montagem, no tempo da fala.

## 5. Boca no tempo da fala (lip sync automático)
- Nível 1: a boca não mexe. Disfarce: mostre quem fala de costas, de longe ou com gesto (`emote: talk`) e use o plano de reação.
- Nível 2 (Animated Java) e nível 3 (Blender): o Claude lê o volume da sua voz a cada quadro e abre a boca quando o som está alto (3 formas: fechada, meio aberta, aberta). Isso vira os keyframes da boca do personagem, sem trabalho manual.
- O script de lip sync ainda não existe: o Claude escreve quando o 1º personagem com boca estiver pronto.

## 6. Direitos (importante)
- Recriar cenas de anime ou filme (personagens, nomes, falas, música, trilha, dublagem) é obra derivada. Pode levar reivindicação ou derrubada, e o vídeo pode não monetizar.
- Caminho seguro: **personagens e história próprios** com os elementos de gênero (transformação, aura, raio de energia, luta no céu, cratera). Esses elementos não têm dono; personagens, nomes e cenas específicas têm.
- Nunca usar áudio, música ou dublagem do anime.
- Mais sobre isso no guia 11 §5 (Dragon Mine Z).
