# Ferramentas para vídeos cinematográficos de Minecraft (estilo TheLuics) + MCP no Claude Code

Pesquisa de 12/11/2026. Windows 11, Claude Code, nenhum MCP de Minecraft instalado ainda.
Versões mudam rápido: antes de instalar, confira no GitHub/Modrinth qual versão do jogo cada peça suporta.
**Versão-alvo sugerida: Java 1.21.11 + Fabric**, porque é a única que todas as peças abaixo suportam
(MCP chapmanjw, mcp-server-mod, Flashback, Mineflayer).

---

## 1. MCPs de Minecraft existentes

### 1.1 Comparação rápida

| MCP | Como conecta | Faz | Precisa | Bom para |
|---|---|---|---|---|
| **chapmanjw/minecraft-java-fabric-mcp-server** | Mod Fabric dentro do jogo, MCP HTTP nativo | ~183 ferramentas: `command_execute` (qualquer /comando), `entity_teleport`, `level_set_time`, `level_set_weather`, `level_set_game_rule`, `block_fill_region`, `block_clone_region`, `structure_load_to_world`, `player_set_camera` (/spectate), `view_capture` (print PNG da visão do jogador) | MC 1.21.11 (JDK 21) ou 26.x (JDK 25), Fabric Loader + Fabric API | **Montar cena, teleportar, comandos e conferir enquadramento por print. RECOMENDADO** |
| **cuspymd/mcp-server-mod** | Mod Fabric no cliente, HTTP `localhost:8080/mcp` | `execute_commands` (só lista fixa: fill, setblock, clone, summon, tp, give, gamemode, effect, enchant, weather, time, say), `get_player_info`, `get_blocks_in_area`, `take_screenshot` (com x/y/z/yaw/pitch) | MC 1.21.4 a 1.21.11 / 26.x, Fabric, mundo com cheats | Alternativa simples. **Não roda /gamerule nem WorldEdit** (fora da lista) |
| **yuniko-software/minecraft-mcp-server** | Bot Mineflayer entra no mundo como outro jogador | andar, voar, olhar, cavar, colocar bloco, inventário, chat (`send-chat`/`read-chat`), achar blocos/entidades | Node >= 20.10, mundo "Abrir para LAN" ou servidor; MC 1.21.11 | Bot "ator" na cena. **Sem ferramenta de comando**: comandos só via `send-chat "/tp ..."` se o bot for OP |
| **RCON** (Peterson047, MinecraftCodeFoundary/Hareidus, scotteratigan, deemkeen) | RCON do servidor dedicado (porta 25575) | `run_command` = qualquer comando de servidor; alguns leem log | Servidor dedicado (Paper/Fabric) com `enable-rcon=true`. **Não funciona em mundo single player** | Servidor local "de estúdio"; simples e estável |
| **amenti-labs/vibecraft** | Mod Fabric cliente + servidor Python (SSE) | constrói com /fill, /setblock ou WorldEdit | Python 3.10+ e uv, Java 21, compilar o mod; 1.20.1 a 1.21.4 | Construções grandes por texto (versão do jogo mais antiga) |
| **Mming-Lab/minecraft-bedrock-mcp-server** | WebSocket do Bedrock (`/connect localhost:8001/ws`) | jogador, agente, mundo, blocos, **câmera**, sistema | Node 16+, Bedrock/Education com cheats | Só se for gravar no Bedrock (não recomendado: sem Flashback/Iris/DH) |
| Construtores de schematic (joshbker Minecraft Builder, simonerecchia/minecraft-schematic-lab) | Offline, geram `.schem` | Claude desenha estrutura e exporta Sponge `.schem` | WorldEdit 7 para colar | Gerar construções e colar com `//paste` |

Links:
- https://github.com/chapmanjw/minecraft-java-fabric-mcp-server (lista completa: `docs/tools.md`) e https://modrinth.com/project/fabric-api-mcp-server
- https://modrinth.com/mod/mcp-server-mod (código: github.com/cuspymd/mcp-server-mod)
- https://github.com/yuniko-software/minecraft-mcp-server
- https://github.com/Peterson047/Minecraft-MCP-Server · https://github.com/MinecraftCodeFoundary/Minecraft-MCP-Server · https://glama.ai/mcp/servers/scotteratigan/minecraft-rcon-mcp
- https://github.com/amenti-labs/vibecraft
- https://glama.ai/mcp/servers/@Mming-Lab/minecraft-bedrock-mcp-server
- https://github.com/simonerecchia/minecraft-schematic-lab

### 1.2 Escolha: chapmanjw (mod Fabric) como principal

Por quê: roda dentro do próprio jogo (não precisa de servidor separado nem de bot), executa **qualquer** comando
(`/tp`, `/time set`, `/weather`, `/gamerule`, e comandos do WorldEdit se o mod WorldEdit estiver instalado),
e devolve **print da tela** (`view_capture`) para o Claude conferir o enquadramento antes de gravar.
Claude Code fala HTTP direto, sem proxy.

Instalação (Windows 11):
1. Instalar o Minecraft Java e abrir a 1.21.11 vanilla uma vez.
2. Instalar Fabric Loader para 1.21.11 (https://fabricmc.net/use/installer/) ou usar Prism Launcher (mais fácil para manter perfis de mods separados).
3. Baixar no Modrinth, versão 1.21.11: `fabric-api-mcp-server`, `Fabric API`. Colocar em `%APPDATA%\.minecraft\mods` (ou na pasta mods da instância do Prism).
4. Abrir o perfil Fabric, entrar num mundo criativo **com cheats ligados**. Apertar **F3+P** (desliga "pausar ao perder o foco", senão o jogo pausa quando você vai para o terminal).
5. Testar: `curl http://127.0.0.1:8765/healthz`
6. Adicionar ao Claude Code (na pasta do projeto):
   ```
   claude mcp add --transport http minecraft-java http://localhost:8765/mcp
   claude mcp add --transport http minecraft-java-client http://localhost:8766/mcp
   ```
   (o segundo é o endpoint do cliente, onde fica o `view_capture`; confira a porta/caminho em `docs/configuration.md`)
   Ou pelo plugin oficial: `/plugin marketplace add chapmanjw/minecraft-java-fabric-claude-plugin` e
   `/plugin install minecraft-java@minecraft-java-claude`.
7. Reiniciar o Claude Code e rodar `/mcp` para ver se conectou.

Segurança: por padrão escuta só em 127.0.0.1, limite de 60 req/min. `command_execute` passa por cima do limite de acesso,
então trate como "admin" (não exponha para a rede). **Não está documentado se funciona no single player** (servidor integrado);
se as ferramentas de mundo não responderem, rode um servidor Fabric local com o mesmo mod e entre nele.

### 1.3 Alternativas e configs prontas

**mcp-server-mod (cuspymd)** — mesma ideia, mais simples:
```
claude mcp add --transport http minecraft http://localhost:8080/mcp
```
(o Modrinth diz que Claude Code precisa de proxy, mas isso é antigo: o Claude Code aceita `--transport http`.)

**yuniko (bot Mineflayer)** — no Windows o `npx` precisa do `cmd /c`:
```
claude mcp add minecraft-bot -- cmd /c npx -y github:yuniko-software/minecraft-mcp-server --host localhost --port 25565 --username ClaudeBot
```
Ou no `.mcp.json` do projeto:
```json
{
  "mcpServers": {
    "minecraft-bot": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "github:yuniko-software/minecraft-mcp-server",
               "--host", "localhost", "--port", "25565", "--username", "ClaudeBot"]
    }
  }
}
```
Atenção: o bot entra sem conta Microsoft (modo offline). "Abrir para LAN" costuma exigir autenticação; se o bot for recusado,
use um servidor Paper local com `online-mode=false` em `server.properties`. A porta do LAN é aleatória: troque `25565` pela que o jogo mostrar.

**RCON (servidor dedicado local)** — `server.properties`:
```
enable-rcon=true
rcon.port=25575
rcon.password=troque_isto
online-mode=false
```
`.mcp.json` (MinecraftCodeFoundary, Python 3.11+, `pip install .` a partir do clone):
```json
{
  "mcpServers": {
    "minecraft-rcon": {
      "command": "minecraft-rcon-mcp",
      "env": { "RCON_HOST": "localhost", "RCON_PORT": "25575",
               "RCON_PASSWORD": "troque_isto", "SERVER_DIR": "C:/mc-server" }
    }
  }
}
```
Vantagem do RCON: o servidor fica rodando e o Claude prepara o mundo enquanto você grava pelo cliente.

### 1.4 Limites de qualquer MCP
- Nenhum MCP **grava vídeo** nem controla Flashback/Replay Mod. A câmera cinematográfica é manual (ou keyframes no Flashback).
- `view_capture`/`take_screenshot` servem para conferir enquadramento, não para filmar (sem shader de qualidade garantido, 1 quadro por chamada).
- Comandos gigantes (`/fill` acima de 32.768 blocos) falham: dividir ou usar WorldEdit.
- Chunks longe do jogador não existem até carregar: pré-gerar com o mod Chunky antes.

---

## 2. Como os criadores de documentário de Minecraft capturam as imagens

### 2.1 Pilha de mods (Fabric, 1.21.11)
| Ferramenta | Para quê | Link |
|---|---|---|
| **Flashback** (Moulberry) | Grava a sessão e depois você monta a câmera em keyframes (posição, FOV, tempo, timelapse) e exporta vídeo. Substituto moderno do Replay Mod | https://modrinth.com/mod/flashback |
| Replay Mod | O clássico (camera path, keyframes, render). Mais lento para atualizar versão | https://www.replaymod.com |
| **Iris + Sodium** | Shaders com bom FPS | https://modrinth.com/mod/iris |
| Shaders: Complementary Reimagined/Unbound, BSL, Bliss, Nostalgia | Visual "filme". Complementary e Bliss funcionam com Distant Horizons | modrinth.com/shaders |
| **Distant Horizons** | Renderiza centenas de chunks (horizonte gigante, essencial para vídeos de "escala") | https://modrinth.com/mod/distanthorizons |
| **Chunky** (pregenerator, mod de servidor) | `/chunky radius 5000` e `/chunky start` pré-geram o mundo. Não confundir com o Chunky renderer | https://modrinth.com/plugin/chunky |
| WorldEdit / **Axiom** | Construir e editar terreno rápido (Axiom é editor visual, só no cliente com permissão) | modrinth.com/plugin/worldedit · axiom.moulberry.com |
| Camera Utils / Freecam | Zoom suave, câmera livre, roll; Freecam para olhar sem mover o jogador | modrinth.com/mod/camera-utils · modrinth.com/mod/freecam |
| Modpacks prontos | "Cinematic Studio", "Cinemacraft" (Axiom, Flashback, WorldEdit, Camera Utils, DH) | modpackindex.com/modpack/135827/cinematic-studio |

Truques: **F1** esconde HUD; FOV baixo (30) achata e aumenta a sensação de tamanho, FOV alto (100+) exagera profundidade;
câmera bem baixa perto do chão faz bloco parecer prédio; `/gamerule doDaylightCycle false` trava a luz entre takes;
`/tick freeze` (1.20.3+) congela mobs/água; spectator (`/gamemode spectator`) atravessa blocos; escala comparada com
um personagem parado (`/summon armor_stand` ou o bot Mineflayer como "figurante").

### 2.2 Render fora do jogo (Blender/path tracing)
- **Mineways** (mineways.com) ou **jmc2obj** exportam um pedaço do mundo para OBJ/USD → Blender (Cycles/Eevee) para planos impossíveis no jogo (escala do universo, câmera macro, volumetria).
- **Chunky renderer** (chunky-dev.github.io): path tracer só de Minecraft, imagens fotorrealistas, lento e pesado em RAM; cheque suporte da versão do mundo.
- Shader path tracing no jogo (ex.: Camellia): parar a câmera e acumular amostras, bom para still.

### 2.3 Modelos 3D de IA (Tripo AI, patrocinador de um vídeo dele)
- Tripo gera modelo por texto/imagem, tem estilização **Voxel** e **Lego**, exporta GLB/OBJ/FBX/STL/USD (não exporta schematic).
- Para dentro do Minecraft: OBJ → **ObjToSchematic** (objtoschematic.com, v2 web) → `.schem` → `//schem load` + `//paste` (WorldEdit) ou `structure_load_to_world` pelo MCP.
- Para o Blender: importar o GLB direto na cena exportada pelo Mineways.

### 2.4 O que o MCP automatiza x o que é manual
| Automatiza pelo MCP (comandos) | Manual |
|---|---|
| Teleportar e orientar (`/tp @s x y z yaw pitch`), spectator | Gravar com Flashback/Replay Mod e montar keyframes |
| Hora, clima, gamerules, `/tick freeze`, efeitos (`night_vision`, `invisibility`) | Escolher/ajustar shader, Distant Horizons, FOV |
| Construir: `/fill`, `/clone`, `/place structure`, WorldEdit (`//pos1`, `//set`, `//paste`) | Axiom (é visual) |
| Pré-gerar mapa (`/chunky ...`), invocar mobs, armor stands | Exportar e montar no Blender/Mineways/Chunky renderer |
| Conferir enquadramento por print e listar coordenadas de cada plano | Gerar modelo no Tripo e converter no ObjToSchematic (site web) |
| Gerar `.schem` de estruturas (schematic-lab) | Edição final, música, narração |

Fluxo sugerido: Claude lê o roteiro → cria uma lista de planos com coordenadas → monta cada cenário por comando →
tira print para você aprovar → você grava no Flashback (F1, câmera em keyframes) → exporta.

---

## 3. O que é público sobre o fluxo do TheLuics

- Canal: https://www.youtube.com/@TheLuics (id UCXl-iYiOftKELkZTa4RQ34Q). A página do canal não carrega para robôs, então descrição e links não puderam ser lidos.
- Patreon: https://www.patreon.com/TheLuics — título "TheLuics | Youtuber de Minecraft", cerca de 1.670 membros, 22 posts (todos travados),
  plano a partir de **R$ 20/mês**, texto do "sobre": diz que é YouTuber de Minecraft e precisa de ajuda para continuar postando.
  **A página pública não mostra o curso**; nomes dos planos, benefícios e títulos de posts só aparecem para membros.
  O curso citado (efeitos, roteiro, quanto ganha) não foi achado em Hotmart/Kiwify nem em busca aberta.
- Redes: TikTok @the_luics (vídeos recentes sobre um servidor próprio, "MEU SERVIDOR PRECISA DE VOCÊS!") e @luics30, Instagram @the_luics.
- Nenhuma entrevista ou post público descrevendo mods/editor foi encontrado. Para descobrir a pilha dele sem entrar em conta:
  ler descrições e comentários fixados dos vídeos, e pedir ao Gemini que identifique shader/DH/Flashback pelos quadros (pasta `analises/gemini`).

---

## 4. Música e efeitos sonoros

- **Trilha oficial (C418, Lena Raine, Aaron Cherof, Kumi Tanioka) é protegida.** Há relatos de Content ID em faixas como "Mice on Venus",
  o que tira ou divide a monetização. Mesmo que o autor diga que não reclama, a editora/distribuidora pode reclamar.
  Uso curto e baixo no fundo reduz, mas não elimina o risco. Se vier reivindicação, o editor do YouTube remove a faixa.
- Alternativas seguras: **YouTube Audio Library** (grátis, no Studio), **Epidemic Sound** (assinatura, libera o canal),
  **Artlist** (licença vitalícia por música), Pixabay Music (grátis, conferir licença). Buscar por "ambient piano", "atmospheric",
  "dark ambient", "cinematic drone" para o clima calmo/misterioso do gênero.
- Sons do jogo: as Diretrizes de Uso da Mojang (https://www.minecraft.net/pt-br/usage-guidelines) liberam usar gameplay em vídeo monetizado.
  Na prática, criadores gravam o som ambiente no próprio Flashback/OBS ou extraem os `.ogg` de
  `%APPDATA%\.minecraft\assets\objects` (índice em `assets\indexes\<versão>.json`) para usar como efeito (cave sounds, portal, ender dragon).
  Sons de caverna e de ambiente são a "assinatura" de vídeos de anomalias e mistério; evite as faixas de música dessa pasta (mesmo risco da trilha).

---

## Setup recomendado (resumo)
1. Prism Launcher → instância **1.21.11 Fabric** com: Fabric API, `fabric-api-mcp-server`, Sodium, Iris, Distant Horizons, Flashback, WorldEdit (Fabric), Chunky, Camera Utils.
2. `claude mcp add --transport http minecraft-java http://localhost:8765/mcp` (+ endpoint cliente para prints).
3. Mundo criativo com cheats, F3+P, pré-gerar com Chunky, travar luz com gamerule.
4. Claude monta cada plano por comando e mostra print; você grava no Flashback e exporta.
5. Opcional: yuniko (bot figurante) e servidor Paper + RCON se quiser um mundo "estúdio" sempre ligado.
