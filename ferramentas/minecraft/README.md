# Ferramentas do jogo (datapack de cenas + OBS)

| Script | Faz | Testado |
|---|---|---|
| `datapack.py` | JSON da cena → datapack com câmera (rig suave) e ações no tempo certo | teste próprio OK (`--teste`); **no jogo ainda não** |
| `obs.py` | começa/para a gravação do OBS pelo WebSocket (só Python padrão) | conta da senha OK (`--teste`); **conexão real ainda não** (OBS fechado) |

## Fluxo de 1 cena
1. O Claude lê a ficha da cena no `cenas.md` e os tempos em `tempos.json` e escreve `cenas_json/c004.json` (formato no topo do `datapack.py`).
2. `python -X utf8 datapack.py cenas_json/c004.json "<pasta do mundo>"` → pelo MCP: `/reload`.
3. Pelo MCP: monta o cenário fixo (se não estiver no `setup`) e tira print (`view_capture`).
4. `python -X utf8 obs.py gravar` → MCP: `/function cenas:c004/start` → espera a duração → `python -X utf8 obs.py parar`.
5. O arquivo do OBS vai para `videos/NN_tema/cenas/c004.mp4`; o começo é cortado pela diferença de hora mostrada.

## Primeiro teste no jogo (checklist)
- [ ] `pack_format` certo para a versão (Minecraft Wiki → "Data pack format"); passe `--pack-format N`.
- [ ] `/ride @p mount` funciona no `text_display`? Se não, trocar o rig por `armor_stand` invisível com `NoGravity`.
- [ ] `ajuste_y`: o olho fica na altura certa? Ajuste até o print bater com a posição pedida.
- [ ] A câmera fica suave? Se tremer: gravar a 30 fps, subir `teleport_duration`, ou usar o Flashback nessa cena.
- [ ] F1 apertado (sem interface) e F3+P (o jogo não pausa) antes de gravar.
- [ ] OBS: WebSocket ligado (porta 4455), saída em MP4/MKV 1080p 60 fps.
Anote o que deu certo em `aprendizados.md`.
