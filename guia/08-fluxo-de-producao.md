# Fluxo de produção de 1 vídeo

Divisão do trabalho:
- **Você:** aprova a ideia, grava e edita a sua voz.
- **Claude:** todo o resto, guiado pelo tempo da sua fala.

Cada vídeo fica em `videos/NN_tema/` (o áudio e os vídeos não sobem para o GitHub, por causa do `.gitignore`).

## 0. Ferramentas (instalar 1 vez)
- Minecraft Java 1.21.11 Fabric + mods + MCP do Minecraft (guia 06).
- OBS Studio (já instalado neste PC) com o WebSocket ligado: Ferramentas → Configurações do servidor WebSocket → Ativar, porta 4455.
- Blender (para estúdio 3D e espaço; ainda não instalado).
- Trilha livre e sons do jogo (guia 05).

## 1. Ideia — Claude propõe, você escolhe
- O Claude traz 5 a 10 ideias com a nota do filtro (guia 00), o título, a thumb em 3 palavras, a escada de degraus e a virada.
- Você escolhe 1. Só ideia com nota 8 ou mais.
- O Claude confere os números na Minecraft Wiki e salva em `fatos.md` (cada número com o link).

## 2. Roteiro e cenas — Claude escreve
- `roteiro.md`: frases F001..., cada uma com tom e pausa (guia 09 §1). Molde e checklist no guia 02.
- `cenas.md`: uma ficha por cena com cenário, elenco, ações, expressões e câmera (guia 09 §3).
- Você lê o roteiro e pede ajustes. As cenas você não precisa ler.

## 3. Voz — você
- Grava lendo o `roteiro.md`, edita (corta erro e respiro, limpa ruído) e salva `voz.wav` na pasta do vídeo.
- Nas `[pausa de cena N s]` deixe só 2 s: o Claude estica.
- Avise: "voz pronta do vídeo NN".

## 4. O resto — Claude, automático
1. `ferramentas/alinhar_voz.py` → `tempos.json` (início e fim de cada frase). Frase marcada "CONFERIR" = o Claude ouve e acerta à mão.
2. Ajusta a duração de cada cena aos tempos da sua fala.
3. Gera o datapack das cenas (cenário, elenco, ações e câmera em ticks).
4. Para cada cena: monta pelo MCP → print para conferir → OBS grava → `/function` da cena → para.
5. Estúdio 3D e espaço no Blender.
6. Monta o vídeo nos tempos da voz: planos de 2–4 s, textos pop, contadores, efeito em toda revelação, música por bloco que sobe nas pausas, master -14 LUFS (guias 03 e 05).
7. Faz 3 thumbs (A/B/C), título, descrição com capítulos e 2 Shorts (guias 04 e 07).
8. Você assiste e aprova. Depois sobe no YouTube.

## Onde pode precisar de você
- Cena com câmera tremida no rig por comando → gravar aquela cena no Flashback (manual).
- Erro do MCP ou do jogo que trava → reabrir o jogo.
- Frase marcada "CONFERIR" que o Claude não consiga resolver.

## Começo recomendado
O 1º vídeo deve ser de **medir** ou **ranking** (guia 00): estruturas e blocos do jogo, poucos personagens, câmera simples. Esquetes com muitos NPCs ficam para depois que o rig de câmera e o OBS estiverem testados.
