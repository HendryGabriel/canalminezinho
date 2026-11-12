# canalminezinho — instruções para o Claude

Este repositório guarda o método para fazer vídeos de Minecraft com o Claude Code + o MCP do Minecraft.

## Primeira mensagem de cada conversa nova (obrigatório, 1 vez por conversa)
Antes de qualquer trabalho de vídeo, mostre o menu de `guia/formatos-e-estilos.md` em 2 passos (ferramenta AskUserQuestion).
Não pergunte de novo na mesma conversa. Não pergunte o que o usuário já respondeu na própria mensagem.

**Passo 1 (1 AskUserQuestion, 2 perguntas):**
1. **Formato:** 1 Documentário · 2 Machinima · 3 Animações complexas.
2. **Voz:** Eu gravo · TTS do Gemini (Google AI Studio).

**Passo 2 (1 AskUserQuestion, 2 perguntas):**
3. **Estilo:** as opções do formato escolhido (tabela do guia `formatos-e-estilos.md` §3; mostre as 3 mais fortes, o resto cabe em "Outro").
4. **Tema:** "Tenho um tema" (o usuário escreve) · "Me dá ideias" (o Claude traz 5 ideias no formato e estilo, como no §4).

Grave as respostas em `videos/NN_tema/projeto.md`. Se a conversa continuar um vídeo que já tem `projeto.md`, leia o arquivo e confirme em 1 linha em vez de perguntar.

## Arquivos de trabalho
- No começo de todo projeto: ler `aprendizados.md` (o que já funcionou e o que quebrou).
- Copiar os modelos de `modelos/` para `videos/NN_tema/` e preencher. Ver o exemplo do formato em `exemplos/` antes de escrever.
- Seguir `checklists.md` em cada etapa. No fim do vídeo: escrever em `aprendizados.md`.
- Música, sons, skins, rigs e mapas: só de `biblioteca/` (licença conferida) e com créditos na descrição.
- Scripts: `ferramentas/alinhar_voz.py` (voz → tempos), `ferramentas/minecraft/` (datapack de cenas, OBS), `ferramentas/edicao/` (montagem, efeitos, lip sync, thumbs), `ferramentas/blender/` (looks, efeitos, montar cena).

## Ferramentas
O Claude pode usar Blender (por script), ffmpeg, OBS, Minecraft + MCP, Python e o Claude in Chrome (Gemini, AI Studio, sites de mods). Instalar programa/mod, aceitar termos ou comprar: só com o OK do usuário.

## Regras de todo projeto
- A ideia vem primeiro. Formato 1: nota 8/10 no filtro do guia 00. Formatos 2 e 3: premissa, quem quer o quê, conflito, virada e final, com ficha de personagens (guia 12 §1).
- `roteiro.md` = só fala, com tom e pausa por frase (e quem fala). Câmera, cenário, NPCs, expressões e objetos vão só no `cenas.md` (guia 09).
- O usuário só escolhe a ideia e (se escolheu "eu gravo") grava a voz. O Claude faz o resto nos tempos da fala (guia 08).
- Para cenas do jogo use o MCP do Minecraft (guia 06). Movimento e câmera rodam num datapack; o MCP dá a ordem e tira print. Plano B de câmera: Flashback (manual).
- Não copie o TheLuics nem outros canais: nada de skins, personagens, nomes de série, bordões, roteiros ou thumbnails deles. Copie o método, não a obra.
- Machinima e animações complexas (qualquer estilo, inclusive luta estilo anime): só personagens, nomes, poderes e histórias próprios. Não recriar cenas, personagens, falas, música ou dublagem de anime/filme/série (guia 10 §6, guia 11 §5).
- Blender 5.2 está instalado (`C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`, roda com `-b -P script.py`).
- Não use a trilha oficial do Minecraft (C418/Lena Raine): tem Content ID.
- Confira todo fato do jogo na Minecraft Wiki antes de narrar.
- Voz de IA → marcar "conteúdo alterado/sintético = Sim" no YouTube Studio.
- Repositório público: nunca suba vídeo, áudio, transcrição ou imagem de outros criadores, nem dados pessoais (e-mail, contas).
