---
name: minecraft-documentario
description: Planeja e produz vídeos de Minecraft em 3 formatos (documentário, machinima/novelinha, animações complexas no Blender em qualquer estilo: luta estilo anime, aventura, terror, comédia...) com Shorts e, no formato principal, vídeos de documentário de Minecraft no estilo do canal TheLuics (escala, "E se...?", "É possível...?", 20-30 min, cinematic com shader, estúdio 3D, esquetes, final emocional) usando o Claude Code e o MCP do Minecraft para montar as cenas. Cobre ideia, roteiro, lista de planos, comandos de cena, gravação no Flashback, Blender, edição, efeitos sonoros, música, thumbnail, título e Shorts. Use SEMPRE que o usuário falar em vídeo de Minecraft, canal de Minecraft, documentário de Minecraft, TheLuics, canalminezinho, MCP do Minecraft para vídeo, ou pedir roteiro/thumbnail/edição de vídeo de Minecraft, mesmo que não diga "skill".
---

# Documentário de Minecraft (método TheLuics)

Fonte de tudo: o repositório `canalminezinho` (github.com/HendryGabriel/canalminezinho).
Neste PC o clone fica em `C:\Users\Vini\Desktop\PROJETO SITES\ESTUDOS\canalminezinho\`. Em outro PC, ache o clone (ou clone de novo) e leia os guias de lá.

## Material pronto no repositório
`aprendizados.md` (ler primeiro) · `modelos/` (copiar e preencher) · `exemplos/` (1 projeto completo por formato) · `checklists.md` · `biblioteca/` (assets com licença) · scripts em `ferramentas/` (`alinhar_voz.py`, `edicao/`, `blender/`, `minecraft/`), cada um com `--teste`.

## Leia antes de começar
| Etapa | Guia |
|---|---|
| Ideia (sempre o 1º passo) | `guia/00-ideias.md` |
| Roteiro com tom/pausa + arquivo de cenas | `guia/09-roteiro-e-cenas.md` |
| Machinima / cenas de filme / diálogo | `guia/10-machinima.md` |
| Minecraft → Blender, efeitos (aura, raio, explosão) | `guia/11-minecraft-para-blender.md` |
| Luta rápida estilo anime: cortes, quadros de impacto, flash, efeitos | `guia/14-estudo-reel-luta.md` |
| Entender o formato | `guia/01-o-canal.md` |
| Roteiro | `guia/02-roteiro.md` (+ exemplos em `analises/roteiros/`) |
| Imagem e montagem | `guia/03-edicao-visual.md` |
| Thumb e título | `guia/04-thumbnails-e-titulos.md` |
| Efeitos e música | `guia/05-som-e-musica.md` (+ `analises/gemini/`) |
| MCP e gravação | `guia/06-minecraft-mcp-e-captura.md` |
| Shorts (método DonJone: afirmação forte, imagem por palavra, legenda 1–2 palavras, loop) | `guia/07-shorts.md` §0 + `analises/shorts-donjone.md` |
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

## 1ª coisa em cada conversa nova (1 vez só)
Menu em 2 passos (AskUserQuestion), regras no `CLAUDE.md` do repositório e opções em `guia/formatos-e-estilos.md`:
1. **formato** (1 Documentário · 2 Machinima · 3 Animações complexas no Blender) + **voz** (eu gravo · TTS do Gemini no AI Studio);
2. **estilo** do formato + **tema** (o usuário diz, ou o Claude traz 5 ideias).
Grave em `videos/NN_tema/projeto.md`. Não repita o menu na mesma conversa.
- Formato 3: `guia/11-minecraft-para-blender.md` (qualquer estilo: luta estilo anime, aventura, terror, comédia cartoon, fantasia, ficção científica, drama).
- Formato 2: `guia/12-novelinha.md` (episódio, ficha de personagem, itens da vida real, cobertura de câmera de novela com a cena repetida por datapack).
- Voz por TTS: `guia/13-vozes.md` (voz fixa por personagem em `personagens.md`, até 2 falantes por Run, ~45 Runs/dia por conta).

## Divisão do trabalho (pedido do usuário, 12/11/2026)
O usuário só **escolhe a ideia, grava e edita a própria voz**. O Claude faz todo o resto, guiado pelo tempo da fala.

1. **Ideia primeiro** (`guia/00-ideias.md`): proponha 5-10 ideias com a nota do filtro (precisa de 8/10), título, thumb em 3 palavras, escada de degraus e virada. Não refaça temas do TheLuics. Ele escolhe.
2. **Fatos**: confira cada número na Minecraft Wiki → `videos/NN_tema/fatos.md`.
3. **`roteiro.md`**: só a fala. Cada frase = `F001 [tom · velocidade] texto` + `[pausa N s]` ou `[pausa de cena N s]`. Dicionários de tom e pausa no `guia/09-roteiro-e-cenas.md`. Nada de câmera ou NPC no roteiro.
4. **`cenas.md`** (arquivo separado): ficha por cena ligada aos Fs — tipo, mundo, local, cenário (comandos), elenco (Easy NPC ou mannequin = personagem; villagers/mobs), gestos (`emote:` do Emotecraft x Easy NPC → `/enpcemote play`) ou animações (`anim:` do Animated Java → `/function`), tabela "Expressão → o que pôr no cenas.md" do guia 09, ações com tempo relativo à frase, expressões (pose, cabeça, partícula, som), câmera (de → para, movimento, duração), texto na tela, som. Formato e dicionários no guia 09.
5. **Voz pronta** (`voz.wav`): rode `python -X utf8 ferramentas/alinhar_voz.py videos/NN_tema/roteiro.md videos/NN_tema/voz.wav` → `tempos.json`. Frase "CONFERIR" = ouça e acerte à mão. Estique as pausas de cena até o valor do roteiro.
6. **Cenas no jogo**: segundos → ticks; escreva um datapack (`saves/<mundo>/datapacks/cenas/`) com cenário, elenco, ações e rig de câmera (`text_display` com `teleport_duration` + `/ride`) agendados com `/schedule`; `/reload`. Pelo MCP: montar → `view_capture` para conferir → OBS grava (WebSocket 4455) → `/function cenas:cNNN` → parar. O movimento roda no datapack (limite do MCP: 60 pedidos/min). Rig tremido → plano B: Flashback manual, e avise o usuário.
7. **Montagem** nos tempos da voz (guias 03 e 05), thumbs A/B/C, título, descrição, 2 Shorts. O usuário aprova antes de subir.

Se o MCP não estiver instalado, mostre o passo de instalação do guia 06 e pare para o usuário instalar o Minecraft/mods (é download e instalação de programa: peça confirmação).

## Estudar outro vídeo/canal do mesmo jeito
Scripts em `ferramentas/`: `vtt2txt.py` (legenda automática do YouTube → texto com minutagem), `medir_video.py` (cortes por minuto e LUFS), `transcrever.py` (Whisper local), `prompt_gemini.txt` (análise de edição/som pelo Gemini).
Baixar com `python -m yt_dlp --js-runtimes node ...` (sem o node o YouTube devolve 403).
