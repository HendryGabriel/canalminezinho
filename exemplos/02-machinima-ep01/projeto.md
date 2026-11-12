# Projeto: 02_pastelaria_ep01 (EXEMPLO de referência do formato 2)

formato: 2 Machinima
estilo: Gincana com números (ver "Por que este estilo" abaixo)
tema: três amigos têm um dia para vender cem pastéis e salvar a pastelaria da Vó Cida, enquanto as esmeraldas somem do baú
voz: Eu gravo (todas as vozes, uma por vez) · plano B: TTS do Gemini (fichas prontas em personagens.md)
duração alvo: 12 min (estimativa pelo roteiro: 12:28)
data de início: 2026-11-12
status: roteiro (exemplo pronto para gravar: ideia, personagens, roteiro, cenas e publicação)

## Por que este estilo (Gincana com números, e não Desenho dublado)
1. **Tudo é comando, sem mod:** placar (`/scoreboard`), timer do sol (`/bossbar`), "+10" e "UPGRADE!" (`/title`) e avisos (`tellraw`). É exatamente o que o MCP faz bem. O Desenho dublado depende de muita construção narrada e de música o tempo todo para esconder silêncio.
2. **O número na tela segura a retenção:** a pessoa sempre sabe quanto falta (0 → 1000) e quanto tempo resta (o sol). Cada cena muda o placar, então cada cena "acontece algo" (regra do guia 12: um acontecimento a cada 60–90 s).
3. **Motor de série barato:** mesmo cenário (praça + pastelaria), mesmo elenco, e cada episódio troca só a regra e o número (ex.: EP. 2 "entregar 50 pastéis no Nether", EP. 3 "pastelaria vs food truck dourado"). Título e thumb saem fáceis ("1000 esmeraldas", "-50", "999/1000").
4. **Pegamos o melhor do Desenho dublado também:** um fala por vez (dá para uma pessoa só dublar tudo ou usar TTS), cor por personagem na legenda das frases-chave e CTA fixo de 10 s.

## Como é gravado (decisão do guia 12 §0)
- **Base: 1ª pessoa do Toco** (braço laranja, HUD com placar e barra do sol). ~75% dos planos.
- **Câmera de novela** (rig de câmera do datapack, vários ângulos, TOCO-dublê em Easy NPC) **só nos momentos fortes**: explosão da placa, chegada da Lorena, carrinho voando no lago, baú vazio, acusação do Guga, banco das desculpas, cofre vazio da Lorena, chão quebrando, chuva de esmeraldas, pôr do sol com fogos.
- Mundo: `vila_pastel` (Pilha A: Fabric 1.21.11 + MCP + Easy NPC + Emotecraft x Easy NPC + Fresh Animations/EMF/ETF + Macaw's Furniture).

## Mapa de retenção (molde do estudo, em 12:28)
| % | Tempo | O que acontece |
|---|---|---|
| 0–3% | 0:00–0:20 | creeper chiando atrás do Guga, Toco pula do telhado, placa explode |
| até 1:30 | 0:46–1:30 | premissa: 1000 esmeraldas até o pôr do sol, senão vira estacionamento |
| 15–31% | 1:50–3:52 | primeiros pastéis: zumbi de capacete, pastel de vento, creeper paga em pólvora, buraco no chão (pista) |
| 31–48% | 3:52–6:00 | escala: Pastel Expresso (−50!), carrinho no lago, poção de velocidade, 600 |
| **~60%** | **7:30** | **virada 1:** baú vazio, Guga acusado, pelo laranja, a raposa corre para a torre da Lorena |
| 61–80% | 7:37–10:00 | desculpas no banco + história do "Obrigado" (momento emocional) + modo turbo (390) + invasão da torre |
| **~80%** | **10:00** | **virada 2:** a Lorena também foi roubada |
| 80–92% | 10:00–11:33 | clímax: chão quebrado, toca da raposa, chuva de esmeraldas, 990, pastel de emergência = 1000 no pôr do sol |
| 92–98% | 11:33–12:18 | fogos com a pólvora do creeper, aluguel pago, a raposa vira caixa (piada) |
| 98–100% | 12:18–12:28 | CTA fixo |

## Arquivos
- [x] ideia.md
- [x] personagens.md
- [x] roteiro.md
- [x] cenas.md
- [ ] voz.wav (ou vozes do TTS) → tempos.json
- [ ] cenas gravadas/renderizadas em cenas/
- [ ] final.mp4
- [ ] thumbs A/B/C
- [x] publicacao.md
- [ ] 2 Shorts
- [ ] aprendizados anotados em ../../aprendizados.md
