# Cenas — TÍTULO
Mundo de gravação: · Versão: · Look (formato 3): humor | épico | kids | toon

### C001 — F001–F002 (+ pausa)
tipo: jogo | estudio3d | espaco | mapa | texto | blender
mundo:
local: x y z · dimensão · hora (/time set N) · clima · tick congelado: sim/não
cenário:
  - comando ou estrutura
elenco:
  - NOME: tipo (Easy NPC / mannequin / villager / rig Blender), skin, posição, pose, olhando para
ações (tempo a partir do início da 1ª frase da cena):
  +0,0  NOME emote: wave
  F002 início  NOME anda até x y z (1,5 s)
planos:                       # formato 2: vários ângulos da mesma cena
  F001  plano geral, estático
  F002  close de NOME, sobre o ombro de OUTRO
câmera:
  movimento: estática | dolly in/out | travelling | drone | órbita | revelação | câmera baixa
  de: x y z · yaw · pitch   →   para: x y z · yaw · pitch
  duração: (até o fim de F00N / da pausa)
efeitos (pós): impacto | flash | tingido | tremida | linhas | aberração  @ F00N início +0,2 s
texto na tela: "TEXTO" (pop) em F00N
som: efeito @ momento · música: estilo (sobe/desce)
