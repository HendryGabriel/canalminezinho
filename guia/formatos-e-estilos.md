# Formatos, estilos e temas (o menu do começo)

Na 1ª mensagem de cada conversa nova o Claude mostra este menu (regras no `CLAUDE.md`).
Passo 1: **formato + voz**. Passo 2: **estilo + tema** (as opções dependem do formato).

## 1. Os 3 formatos
| # | Formato | O que é | Onde é feito | Guias |
|---|---|---|---|---|
| 1 | **Documentário** | curiosidade e ciência do jogo, narrador, escala, "e se", 15–30 min (estilo TheLuics) | Minecraft (MCP) + estúdio 3D no Blender | 00–09 |
| 2 | **Machinima** | histórias entre personagens: novelinha, comédia, mistério; itens da vida real; câmera de novela | Minecraft (MCP + mods de personagens) | 12, 09, 10 |
| 3 | **Animações complexas** | animação de cinema com personagens de Minecraft: luta, aventura, terror, comédia; efeitos (aura, raios, explosões, magia) | Blender (cenário do Minecraft via Mineways + MCprep) | 11, 10 |

Shorts saem de qualquer formato (guia 07).

## 2. Voz
- **Eu gravo** a minha voz → guia 13 §1.
- **TTS do Gemini** (Google AI Studio, pelo Claude in Chrome) → guia 13 §2.

## 3. Estilos por formato
### 1 — Documentário
| Estilo | Exemplo de pergunta |
|---|---|
| Medir o jogo (escala, peso, valor, idade) | "Quanto vale um mundo do Minecraft?" |
| "E se...?" (simulação de milhões de anos) | "E se o sol do Minecraft nunca nascesse?" |
| "É possível...?" (desafio total) | "É possível morrer de velhice no Minecraft?" |
| Ranking (do menor ao maior) | "Qual o lugar mais perigoso do Minecraft?" |
| Mistério / anomalia do jogo | "O bloco que nunca deveria existir" |

### 2 — Machinima
| Estilo | Clima | Música e luz |
|---|---|---|
| Novelinha / drama | família, segredo, romance, ciúme | trilha de novela, luz quente, close dramático |
| Comédia | situação absurda, personagem bobo | marimba/cômica, cortes rápidos, vinil arranhando |
| Mistério / terror leve | barulho à noite, casa abandonada | drone escuro, neblina, noite, tocha |
| Aventura | viagem, tesouro, missão | orquestral, paisagens, drone de câmera |
| Vida real / escola | primeiro dia, trabalho, vizinhos | leve/pop, luz do dia, itens da vida real |

### 3 — Animações complexas
| Estilo | O que pesa na cena | Efeitos principais |
|---|---|---|
| Luta estilo anime | poder, transformação, rivalidade | aura, raios de energia, choque de golpes, crateras, velocidade |
| Aventura épica | jornada, monstro gigante, mundo grande | paisagem volumétrica, voo, chefão, câmera ampla |
| Terror | perseguição, criatura, escuro | luz de lanterna, neblina, sustos, som grave |
| Comédia cartoon | exagero, corpo elástico, timing | squash and stretch, poeira de cartoon, caras exageradas |
| Fantasia / magia | magos, feitiços, reinos | partículas mágicas, runas brilhando, portais |
| Ficção científica | nave, robô, outro planeta | hologramas, lasers, espaço, metal brilhante |
| Drama cinematográfico | emoção, perda, amizade | luz de cinema, câmera lenta, chuva, música de piano |

Todos os estilos usam **personagens, nomes, poderes e histórias próprios** (sem copiar anime, filme ou canal).

## 4. Tema
- O usuário diz o tema, **ou** pede ideias.
- Pedido de ideias: o Claude traz 5 ideias no formato e estilo escolhidos.
  - Formato 1: com a nota do filtro do guia 00 (só 8/10 ou mais).
  - Formatos 2 e 3: cada ideia com 1 frase de premissa, quem quer o quê, o conflito, a virada e o final (ou o "continua...").
- O usuário escolhe 1 e o projeto começa.

## 5. Ferramentas que o Claude usa
O Claude pode usar neste PC: Blender (por script), ffmpeg, OBS (WebSocket), o Minecraft com o MCP, Python (Whisper, scripts do `ferramentas/`) e o Claude in Chrome (Gemini, Google AI Studio para vozes, sites de mods e referências).
Instalar programa ou mod novo, aceitar termos ou comprar algo: só com o OK do usuário.

## 6. Registro do projeto (`videos/NN_tema/projeto.md`)
```
formato: 3 — Animações complexas
estilo: Luta estilo anime
tema: dois irmãos rivais disputam o último cristal de energia do mundo
voz: TTS do Gemini
data: 2026-11-12
```
