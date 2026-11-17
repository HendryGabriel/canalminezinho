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
