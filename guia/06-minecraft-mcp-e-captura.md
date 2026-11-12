# MCP do Minecraft e captura das imagens

Pesquisa completa (com links e alternativas): `analises/ferramentas-minecraft.md`.
**Nada disso está instalado ainda neste PC** (12/11/2026). Confira as versões no Modrinth antes de instalar.

## 1. Qual MCP usar
**Recomendado: `chapmanjw/minecraft-java-fabric-mcp-server`** (mod Fabric, MCP por HTTP dentro do próprio jogo).
- ~183 ferramentas: `command_execute` (qualquer /comando, inclusive WorldEdit), `entity_teleport`, hora, clima, gamerules, `block_fill_region`, `block_clone_region`, `structure_load_to_world`, `player_set_camera`, `view_capture` (print da visão do jogador para o Claude conferir o quadro).
- Versão-alvo: **Minecraft Java 1.21.11 + Fabric** (JDK 21).
- Em aberto: não está documentado se funciona no single player. Se não funcionar, rodar um servidor Fabric local com o mesmo mod.

Alternativas: `cuspymd/mcp-server-mod` (mais simples, só comandos de uma lista fixa, com screenshot), `yuniko-software/minecraft-mcp-server` (bot Mineflayer que entra como jogador, bom como "figurante"), MCPs por RCON (precisam de servidor dedicado).

## 2. Instalação (Windows 11)
1. Prism Launcher → nova instância **1.21.11 Fabric**.
2. Mods (Modrinth, versão 1.21.11): Fabric API, `fabric-api-mcp-server`, Sodium, Iris, Distant Horizons, Flashback, WorldEdit, Chunky, Camera Utils.
3. Shader: Complementary Reimagined (funciona com Distant Horizons).
4. Mundo criativo **com cheats**. Apertar **F3+P** (o jogo não pausa quando você vai para o terminal).
5. Testar: `curl http://127.0.0.1:8765/healthz`
6. No terminal, na pasta do projeto:
   ```
   claude mcp add --transport http minecraft-java http://localhost:8765/mcp
   ```
   (o endpoint do cliente, com o `view_capture`, tem outra porta: ver `docs/configuration.md` do projeto)
7. Reiniciar o Claude Code e conferir com `/mcp`.

Segurança: o MCP escuta só em 127.0.0.1. `command_execute` é admin: não abrir para a rede.

## 3. O que o MCP faz e o que é manual
| O Claude faz pelo MCP | Você faz à mão |
|---|---|
| Teleportar a câmera para cada plano (`/tp @s x y z yaw pitch`), modo espectador | Gravar no Flashback e montar a câmera em keyframes |
| Travar hora/clima (`/time set`, `/weather`, `/gamerule doDaylightCycle false`), `/tick freeze` | Ajustar shader, Distant Horizons e FOV |
| Construir cenário: `/fill`, `/clone`, `/place structure minecraft:mansion`, WorldEdit `//paste` | Construções artísticas finas (Axiom é visual) |
| Pré-gerar o mapa (`/chunky radius 5000`, `/chunky start`) | Exportar para Blender (Mineways) |
| Invocar mobs, villagers com nome, armor stands (`/summon`) | Animar personagens de esquete |
| Tirar print para você aprovar o enquadramento | Gerar modelo 3D no Tripo e converter (ObjToSchematic) |

**Nenhum MCP grava vídeo.** O MCP prepara a cena; o Flashback filma.

## 4. Receitas de cena (do estilo dele)
- **Construção isolada no vazio** (ranking de tamanhos): mundo superflat void → `/place structure minecraft:<nome> 0 64 0` → `/time set midnight` → shader com neblina → órbita no Flashback.
- **"Olha você do lado"**: `/summon armor_stand` com a skin/cabeça do personagem ao lado da construção; câmera baixa.
- **Paisagem épica**: mundo normal pré-gerado com Chunky, Distant Horizons a 256+ chunks, `/time set 12500` (fim de tarde), FOV 30-50, drone lento.
- **Simulação "dia X"**: mesmo ponto filmado em vários estados (construir a vila, depois destruir com `/fill ... air` e trocar blocos por sculk), timelapse no Flashback.
- **Esquete com villagers**: `/summon villager ~ ~ ~ {CustomName:'"Pai"',NoAI:1b}` (parados para posar), cenário construído por comando.
- **Mapa visto de cima**: render do mapa (Chunky renderer ou mapa do Distant Horizons) + círculos no editor.

## 5. Fluxo com o Claude
1. Roteiro pronto → o Claude faz a **lista de planos** (`planos.md`: nº, frase, tipo de imagem, cenário, coordenadas, hora, câmera).
2. Para cada plano de jogo: o Claude monta o cenário pelo MCP e manda o print (`view_capture`).
3. Você aprova → grava no Flashback (F1 esconde a interface) → exporta em 1080p/1440p 60 fps em `cenas/<nº>.mp4`.
4. Planos de estúdio/espaço: Blender (Mineways exporta a construção).
5. Montagem, texto e som (guias 03 e 05).

## 6. Música e sons do jogo
- Gameplay de Minecraft em vídeo monetizado é permitido pelas Diretrizes de Uso da Mojang.
- **A trilha oficial (C418, Lena Raine) tem Content ID.** Não usar. Usar trilha livre (YouTube Audio Library, Epidemic, Artlist, Pixabay).
- Sons do jogo (passos, portas, villager, caverna, Warden) estão em `%APPDATA%\.minecraft\assets\objects` (índice em `assets\indexes\<versão>.json`). Usar como efeito. Não usar as faixas de música dessa pasta.
