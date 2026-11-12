# Aprendizados (atualizar em todo vídeo)

O Claude lê este arquivo no começo de cada projeto e escreve aqui no fim. Assim cada vídeo sai melhor que o anterior.
Regra: 1 linha por aprendizado, com data e vídeo. O que virou regra fixa sobe para o guia certo.

## Técnica (o que funcionou / o que quebrou)
| Data | Vídeo | Aprendizado | Virou regra em |
|---|---|---|---|
| 2026-11-12 | — | Gemini pode errar "como é feito" (disse animação 3D num vídeo gravado no jogo): conferir sempre nos quadros. | guia 12 §0 |
| 2026-11-12 | — | O navegador bloqueia o áudio de vídeo sem clique real: para estudar som, baixar o vídeo (com o OK do usuário). | guia 14 |

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
