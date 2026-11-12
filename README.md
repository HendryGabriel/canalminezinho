# canalminezinho

Inteligência para fazer vídeos de **documentário de Minecraft** no estilo do canal TheLuics (@TheLuics, 165 mil inscritos), usando o Claude Code + o MCP do Minecraft.

Estudo feito em 12/11/2026: 12 vídeos longos (todos com transcrição lida), 7 longos e 3 Shorts baixados e medidos (cortes, volume, quadros), 113 Shorts listados, 12 thumbnails olhadas, análise de edição/som pelo Gemini e pesquisa das ferramentas e dos MCPs de Minecraft.

## Como usar
Abra o Claude Code nesta pasta. Na 1ª mensagem de cada conversa ele pergunta (menu em [guia/formatos-e-estilos.md](guia/formatos-e-estilos.md)):
1. **Formato:** 1 Documentário · 2 Machinima · 3 Animações complexas (Blender).
2. **Voz:** você grava · TTS do Gemini (Google AI Studio).
3. **Estilo** do formato (ex.: luta estilo anime, terror, comédia, novelinha, "e se...?").
4. **Tema:** você diz, ou ele traz 5 ideias.

Depois ele segue o guia do formato escolhido. O Claude usa Blender, ffmpeg, OBS, Minecraft + MCP e o Claude in Chrome neste PC.

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
| [guia/12-novelinha.md](guia/12-novelinha.md) | Formato 2 (Machinima): novelinha e histórias, itens da vida real, câmera de novela automática |
| [guia/13-vozes.md](guia/13-vozes.md) | Voz: gravar você mesmo ou TTS do Gemini (voz fixa por personagem) |
| [guia/14-estudo-reel-luta.md](guia/14-estudo-reel-luta.md) | Estudo quadro a quadro de um reel de luta estilo anime: cortes, quadros de impacto, efeitos e como fazer com personagens próprios |
| [skill/minecraft-documentario/SKILL.md](skill/minecraft-documentario/SKILL.md) | Skill do Claude Code que usa tudo isso |

## Pastas
- `analises/machinima/` — estudo de Aphmau, Maizen e Cash (machinima gringa) + síntese.
- `analises/gemini-gringos/` — análise de edição, som e música dos 6 canais gringos (Gemini; conferir "como é feito" nos quadros).
- `analises/animacao/` — estudo de Element Animation, Rainimator e Kamui Animation (animação 3D gringa) + síntese com o "look" no Blender.
- `analises/roteiros/` — análise de roteiro de cada vídeo do TheLuics + síntese.
- `analises/gemini/` — análise de edição, efeitos e música de cada vídeo (Gemini Pro).
- `analises/ferramentas-minecraft.md` — pesquisa completa dos MCPs, mods, Blender, Tripo, música.
- `dados/` — lista de vídeos e Shorts com views.
- `ferramentas/` — `alinhar_voz.py` (acha o tempo de cada frase na sua voz) + scripts do estudo (legenda → texto, medir cortes/volume, transcrever com Whisper, prompt do Gemini).
- `videos/NN_tema/` — cada vídeo: `fatos.md`, `roteiro.md`, `cenas.md`, `tempos.json` (áudio e vídeo ficam só no PC).

## O que NÃO está aqui
O repositório é público. Transcrições completas, vídeos, thumbnails e quadros do TheLuics ficam só no PC (`ESTUDOS/theluics/`), porque são obra dele.
