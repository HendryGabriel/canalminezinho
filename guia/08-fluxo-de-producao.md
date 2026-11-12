# Fluxo de produção de 1 vídeo (do zero ao upload)

Ordem de trabalho para fazer um vídeo no estilo TheLuics com o Claude Code + MCP do Minecraft.
Cada vídeo fica numa pasta `videos/NN_tema/`.

## 0. Ferramentas (instalar 1 vez)
- Minecraft Java 1.21.11 Fabric + mods e MCP (guia 06).
- Blender (para estúdio 3D e espaço) + Mineways (exporta construção do jogo para o Blender).
- DaVinci Resolve (montagem) ou ffmpeg + Remotion (montagem por script, já usado no canal Zé Cinza).
- Narração: voz real (como o TheLuics) ou voz de IA (AI Studio, já usada no Zé Cinza; marcar "conteúdo sintético = Sim" no Studio).
- Trilha livre (YouTube Audio Library / Epidemic) e sons do jogo (guia 05).

## 1. Ideia (30 min)
- Pergunta sobre **o jogo inteiro** que todo jogador já se fez (tamanho, limite, "e se", "é possível").
- Teste: cabe numa pergunta de até 7 palavras com "MINECRAFT"? Tem uma escala que cresce? Tem um final emocional?
- Pesquise os fatos na Minecraft Wiki (minecraft.wiki). Anote cada número com a fonte em `fatos.md`.

## 2. Roteiro (guia 02)
- `roteiro.md` com o molde de % do tempo, 130-145 palavras/min.
- Marque no texto: `[PAUSA 15 s]`, `[TEXTO: 10.000 m]`, `[SFX: boom]`, `[MÚSICA: épica]`, `[ESQUETE]`.
- Rode o checklist do guia 02 §8.

## 3. Lista de planos (o Claude faz)
`planos.md`, 1 linha por frase/plano:
| nº | tempo | frase | tipo (cinematic / estúdio / vazio / espaço / mapa / esquete) | cenário e comandos | câmera | texto | som |

## 4. Gravar as cenas do jogo (MCP + Flashback)
1. Abrir a instância Fabric, mundo de gravação, F3+P.
2. O Claude monta cada cenário pelo MCP e manda o print. Você aprova.
3. Você grava no Flashback (F1), monta a câmera em keyframes e exporta `cenas/NNN.mp4` (1440p 60 fps).

## 5. Estúdio 3D e espaço (Blender)
- Exportar a construção com Mineways → Blender → fundo cinza com grade, luz suave, câmera em órbita → `cenas/NNN.mp4`.
- Planetas de blocos, mapa como cubo, multidões de personagens: Blender.

## 6. Narração
- Gravar ou gerar por blocos. Cortar respiros nas partes rápidas; manter as pausas do roteiro.

## 7. Montagem (guia 03)
- Plano a plano seguindo `planos.md`. 2-4 s por plano; 10-20 s nas pausas.
- Textos pop/digitando, contadores, réguas (Remotion ou Fusion).

## 8. Som (guia 05)
- 3 trilhas: voz, música, efeitos. Efeito em todo texto e revelação. Música muda com a emoção, abaixa na fala, sobe nas pausas.
- Master -14 LUFS, pico -1 dB.

## 9. Thumbnail e título (guia 04)
- 3 thumbs (A/B/C) com 1-3 palavras em fonte grossa 3D branca + 1 imagem de escala. Testar e comparar no YouTube.

## 10. Upload
- Título em CAIXA ALTA com MINECRAFT; descrição de 2-3 frases + capítulos + apoio; hashtags `#minecraft #minecraftjava #mcpe` (+ da série).
- Tags só do assunto.
- Ligar a dublagem automática (o canal dele ganha audiência em inglês assim).
- Fazer 2 Shorts do mesmo tema (guia 07).

## Tempo esperado
O TheLuics posta 1 longo a cada 1-2 meses (produção pesada de 3D). Comece com 1 vídeo de **escala/ranking** (o mais simples: estruturas do jogo, `/place structure`, estúdio 3D, contas) antes de tentar esquetes animadas.
