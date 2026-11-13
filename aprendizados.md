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
