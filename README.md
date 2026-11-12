# canalminezinho

Inteligência para fazer vídeos de **documentário de Minecraft** no estilo do canal TheLuics (@TheLuics, 165 mil inscritos), usando o Claude Code + o MCP do Minecraft.

Estudo feito em 12/11/2026: 12 vídeos longos (todos com transcrição lida), 7 longos e 3 Shorts baixados e medidos (cortes, volume, quadros), 113 Shorts listados, 12 thumbnails olhadas, análise de edição/som pelo Gemini e pesquisa das ferramentas e dos MCPs de Minecraft.

## Comece aqui
| Arquivo | O que tem |
|---|---|
| [guia/00-ideias.md](guia/00-ideias.md) | **1º passo:** como achar uma ideia boa, filtro de 10 pontos, banco de ideias |
| [guia/01-o-canal.md](guia/01-o-canal.md) | Números do canal, as 2 fases, por que funciona |
| [guia/02-roteiro.md](guia/02-roteiro.md) | Regras, molde por % do tempo, fórmulas de abertura, humor, checklist |
| [guia/03-edicao-visual.md](guia/03-edicao-visual.md) | Ritmo medido, os 6 tipos de imagem, câmera, texto, transições |
| [guia/04-thumbnails-e-titulos.md](guia/04-thumbnails-e-titulos.md) | Receita da thumb e fórmulas de título |
| [guia/05-som-e-musica.md](guia/05-som-e-musica.md) | Efeitos sonoros, música, mixagem |
| [guia/06-minecraft-mcp-e-captura.md](guia/06-minecraft-mcp-e-captura.md) | Qual MCP instalar, como, e como gravar as cenas |
| [guia/07-shorts.md](guia/07-shorts.md) | Shorts |
| [guia/08-fluxo-de-producao.md](guia/08-fluxo-de-producao.md) | Passo a passo: você grava a voz, o Claude faz o resto |
| [guia/09-roteiro-e-cenas.md](guia/09-roteiro-e-cenas.md) | Roteiro com tom e pausa + arquivo de cenas (câmera, NPCs, expressões) para o MCP |
| [guia/10-machinima.md](guia/10-machinima.md) | Cenas de filme: 3 níveis, planos, regras de cinema, diálogo, lip sync, direitos |
| [guia/11-minecraft-para-blender.md](guia/11-minecraft-para-blender.md) | Mundo e personagens do Minecraft no Blender, efeitos (aura, raio, explosão), Dragon Mine Z, portar mods antigos com IA |
| [skill/minecraft-documentario/SKILL.md](skill/minecraft-documentario/SKILL.md) | Skill do Claude Code que usa tudo isso |

## Pastas
- `analises/roteiros/` — análise de roteiro de cada vídeo + síntese.
- `analises/gemini/` — análise de edição, efeitos e música de cada vídeo (Gemini Pro).
- `analises/ferramentas-minecraft.md` — pesquisa completa dos MCPs, mods, Blender, Tripo, música.
- `dados/` — lista de vídeos e Shorts com views.
- `ferramentas/` — `alinhar_voz.py` (acha o tempo de cada frase na sua voz) + scripts do estudo (legenda → texto, medir cortes/volume, transcrever com Whisper, prompt do Gemini).
- `videos/NN_tema/` — cada vídeo: `fatos.md`, `roteiro.md`, `cenas.md`, `tempos.json` (áudio e vídeo ficam só no PC).

## O que NÃO está aqui
O repositório é público. Transcrições completas, vídeos, thumbnails e quadros do TheLuics ficam só no PC (`ESTUDOS/theluics/`), porque são obra dele.
