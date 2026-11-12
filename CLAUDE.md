# canalminezinho — instruções para o Claude

Este repositório guarda o método para fazer vídeos de Minecraft com o Claude Code + o MCP do Minecraft.

## Primeira mensagem de cada conversa nova (obrigatório, 1 vez por conversa)
Antes de qualquer trabalho de vídeo, pergunte as 2 coisas abaixo **numa só pergunta** (ferramenta AskUserQuestion, 2 perguntas juntas).
Não pergunte de novo na mesma conversa. Não pergunte o que o usuário já respondeu na própria mensagem.

1. **Formato do projeto**
   - **A — Documentário de Minecraft** (estilo TheLuics: escala, "e se", "é possível", 20–30 min) → guias 00–09.
   - **B — Novelinha / machinima de histórias** (personagens, itens da vida real, câmera de novela, episódios) → guias 12, 09, 10.
   - **C — Luta estilo anime no Blender** (personagens próprios, aura, raios, explosões) → guias 10, 11.
   - **D — Só Shorts** → guia 07 + o guia do formato do tema.
2. **Voz**
   - **Eu gravo** a minha voz (o usuário grava e edita; o Claude alinha com `ferramentas/alinhar_voz.py`).
   - **TTS do Gemini** no Google AI Studio (o Claude gera pelo Chrome; voz fixa por personagem) → guia 13.

Grave as respostas em `videos/NN_tema/projeto.md` (formato, voz, data). Se a conversa continuar um vídeo que já tem `projeto.md`, leia o arquivo e confirme em 1 linha em vez de perguntar.

## Regras de todo projeto
- A ideia vem primeiro e precisa de nota 8/10 no filtro do guia 00 (formato B: ficha de personagens e história do guia 12 §1).
- `roteiro.md` = só fala, com tom e pausa por frase (e quem fala). Câmera, cenário, NPCs, expressões e objetos vão só no `cenas.md` (guia 09).
- O usuário só escolhe a ideia e (se escolheu "eu gravo") grava a voz. O Claude faz o resto nos tempos da fala (guia 08).
- Para cenas do jogo use o MCP do Minecraft (guia 06). Movimento e câmera rodam num datapack; o MCP dá a ordem e tira print. Plano B de câmera: Flashback (manual).
- Não copie o TheLuics nem outros canais: nada de skins, personagens, nomes de série, bordões, roteiros ou thumbnails deles. Copie o método, não a obra.
- Machinima, novelinha e luta estilo anime: só personagens, nomes, poderes e histórias próprios. Não recriar cenas, personagens, falas, música ou dublagem de anime/filme/série (guia 10 §6, guia 11 §5).
- Blender 5.2 está instalado (`C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`, roda com `-b -P script.py`).
- Não use a trilha oficial do Minecraft (C418/Lena Raine): tem Content ID.
- Confira todo fato do jogo na Minecraft Wiki antes de narrar.
- Voz de IA → marcar "conteúdo alterado/sintético = Sim" no YouTube Studio.
- Repositório público: nunca suba vídeo, áudio, transcrição ou imagem de outros criadores, nem dados pessoais (e-mail, contas).
