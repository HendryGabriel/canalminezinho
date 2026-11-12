---
name: minecraft-documentario
description: Planeja e produz vídeos de documentário de Minecraft no estilo do canal TheLuics (escala, "E se...?", "É possível...?", 20-30 min, cinematic com shader, estúdio 3D, esquetes, final emocional) usando o Claude Code e o MCP do Minecraft para montar as cenas. Cobre ideia, roteiro, lista de planos, comandos de cena, gravação no Flashback, Blender, edição, efeitos sonoros, música, thumbnail, título e Shorts. Use SEMPRE que o usuário falar em vídeo de Minecraft, canal de Minecraft, documentário de Minecraft, TheLuics, canalminezinho, MCP do Minecraft para vídeo, ou pedir roteiro/thumbnail/edição de vídeo de Minecraft, mesmo que não diga "skill".
---

# Documentário de Minecraft (método TheLuics)

Fonte de tudo: o repositório `canalminezinho` (github.com/HendryGabriel/canalminezinho).
Neste PC o clone fica em `C:\Users\Vini\Desktop\PROJETO SITES\ESTUDOS\canalminezinho\`. Em outro PC, ache o clone (ou clone de novo) e leia os guias de lá.

## Leia antes de começar
| Etapa | Guia |
|---|---|
| Entender o formato | `guia/01-o-canal.md` |
| Roteiro | `guia/02-roteiro.md` (+ exemplos em `analises/roteiros/`) |
| Imagem e montagem | `guia/03-edicao-visual.md` |
| Thumb e título | `guia/04-thumbnails-e-titulos.md` |
| Efeitos e música | `guia/05-som-e-musica.md` (+ `analises/gemini/`) |
| MCP e gravação | `guia/06-minecraft-mcp-e-captura.md` |
| Shorts | `guia/07-shorts.md` |
| Passo a passo | `guia/08-fluxo-de-producao.md` |

## Regras que não mudam
1. Tema = pergunta sobre **o jogo inteiro** (tamanho, limite, "e se", "é possível"), título em CAIXA ALTA com MINECRAFT.
2. 1ª frase = a pergunta do título. Promessa até 25 s. Sem "olá".
3. Narração em "você", 130-145 palavras/min, conta passo a passo + comparação com o mundo real.
4. Escala que cresce até o fim; re-gancho a cada 1-3 min; piada a cada 1-2 min; 4-7 pausas de 10-20 s só com música.
5. Virada "mas não é o fim" perto de 85%; final com lição pessoal de 1 linha; despedida curta.
6. Planos de 2-4 s; 6 tipos de imagem (cinematic com shader, estúdio 3D cinza quadriculado, construção no vazio escuro, espaço, mapa de cima, esquete).
7. Texto só em palavra-chave/número (pop ou digitando); contador "DIA: X"; sem legenda corrida.
8. Efeito sonoro em todo texto e revelação; música troca com a emoção, abaixa na fala, sobe nas pausas; master -14 LUFS.
9. Thumb: 1-3 palavras em fonte grossa branca com volume 3D + 1 imagem de escala; 3 versões para teste A/B.
10. Não copiar a obra dele (skin, Steve Bo, "Anomalias do Minecraft", roteiros). Não usar a trilha oficial do Minecraft (Content ID).

## Fluxo com o MCP
1. Roteiro → `planos.md` (nº, frase, tipo de imagem, cenário/comandos, câmera, texto, som).
2. Para cada plano de jogo: montar a cena pelo MCP (`command_execute` com /tp, /time, /weather, /gamerule, /place structure, /summon, WorldEdit) e mandar o print (`view_capture`) para o usuário aprovar.
3. O usuário grava no Flashback (o MCP não grava vídeo) e exporta em `cenas/NNN.mp4`.
4. Estúdio 3D/espaço no Blender; montagem, textos e som conforme os guias.

Se o MCP não estiver instalado, mostre o passo de instalação do guia 06 e pare para o usuário instalar o Minecraft/mods (é download e instalação de programa: peça confirmação).

## Estudar outro vídeo/canal do mesmo jeito
Scripts em `ferramentas/`: `vtt2txt.py` (legenda automática do YouTube → texto com minutagem), `medir_video.py` (cortes por minuto e LUFS), `transcrever.py` (Whisper local), `prompt_gemini.txt` (análise de edição/som pelo Gemini).
Baixar com `python -m yt_dlp --js-runtimes node ...` (sem o node o YouTube devolve 403).
