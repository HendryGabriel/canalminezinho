---
name: vaso-vazio-shorts-3d
description: Pipeline completo e definitivo para criar Shorts/TikToks narrativos virais (>60s) 100% dentro do Minecraft Java (via MCP Fabric, sem Blender) no padrão de excelência do vídeo "O Vaso Vazio" — engenharia reversa fiel à referência, adaptação com a mascote Capivara Ping, cenários arquitetônicos 360° construídos por script sem colisão, modelos 3D esculpidos com ModeloRico e proporções anatômicas anti-clipping, captura determinística 30 fps com /tick rate 3.4 (0% de quadros repetidos), síntese exata de SFX (.ogg) e edição viral (grade quente, legenda Monocraft 1 palavra com micro-pop, whoosh e master -12 LUFS).
---

# Skill & Manual Completo — Shorts Narrativos 3D no Minecraft (Modelo "O Vaso Vazio")

Este documento reúne **todo o conhecimento técnico, artístico e de engenharia** consolidado na produção do vídeo **"O Vaso Vazio"** (`65,9 s`, `47 planos`, `1080×1920` a `30 fps`), projetado para que qualquer agente de IA em outro computador consiga assumir o projeto após um `git pull` e produzir novos vídeos mantendo **exatamente o mesmo nível de fidelidade à referência, qualidade de modelos 3D, proporções anatômicas, fluidez de câmera e acabamento de edição**.

---

## 0. Mapa Rápido no Repositório (`canalminezinho`)

Ao clonar ou atualizar este repositório (`https://github.com/HendryGabriel/canalminezinho.git`), consulte imediatamente:

| Caminho no Repositório | Papel no Pipeline |
|---|---|
| `skill/vaso-vazio-shorts-3d/SKILL.md` | **Este documento mestre** (processo ponta a ponta, regras de proporção, anti-clipping, captura e edição). |
| `exemplos/06-vaso-vazio/biblia_cenario.md` | Exemplo real de Bíblia do Cenário (`Frase → Fato visual obrigatório → Elemento em SET → Planos`). |
| `exemplos/06-vaso-vazio/planos.json` | Decupagem completa dos 47 planos (`t0`, `t1`, `frase_trecho`, `descricao_visual`) cobrindo `65,91 s`. |
| `exemplos/06-vaso-vazio/config_vaso.py` | Dicionário único `SET` de coordenadas e cotas de piso compartilhado por todos os scripts. |
| `exemplos/06-vaso-vazio/elenco.py` | Rigs articulados (`PingCapivara`, `Rei`, `Rival`), sincronizador multi-ator (`posar_varios`) e `ModeloRico` (vasos octogonais, flores radiais, regador, panela translúcida fervendo, hashis macro, coroa imperial). |
| `exemplos/06-vaso-vazio/set_vaso.py` | Construtor retomável do mapa-estúdio: ilha sobre oceano, praias senoidais, serras 360° sem listras de terra, naturalização com máscara protetora, Palácio Imperial, Câmara da Caldeira, Jardim Koi e Casa com janela real. |
| `exemplos/06-vaso-vazio/takes_vaso.py` | Gravador determinístico de `30 fps` via framebuffer OpenGL (`vision.screenshot` + `/tick rate 3.4` + pré-roll de velocidade) + renderizador exato de efeitos sonoros `.ogg` do Minecraft. |
| `exemplos/06-vaso-vazio/montar_vaso.py` | Pipeline de pós-produção FFmpeg: color grading quente, legenda `.ass` `Monocraft` de 1 palavra com micro-pop, whoosh procedural nos cortes, sidechain ducking e master `-12 LUFS`. |
| `ferramentas/animacao-no-jogo/` | Motor base (`motor.py`, `mc.py`, `takes3.py` com classe `Vel`), `datapack_queda/` e utilitários (`ajustar_tempos.py` em `ferramentas/shorts-farm/`). |
| `aprendizados.md` | Histórico vivo de bugs resolvidos e regras permanentes — **ler antes de começar e atualizar ao terminar cada vídeo**. |

---

## 1. Pré-requisitos de Ambiente no Computador de Produção

Antes de iniciar a gravação no outro computador, confira o ambiente:

1. **Minecraft Java Edition (1.21.4+ / 26.x) com Fabric + Mod MCP Fabric**:
   - O cliente precisa estar aberto em um mundo local (preferencialmente oceano amplo ou superflat oceânico) com o mod **MCP Fabric** ativo, expondo `~/.mcpfabric/bridge.json` (`url` + `token` para chamadas JSON-RPC em `/rpc`: `command.run`, `vision.screenshot`, `control.look`, `screen.close`).
   - **Janela em proporção vertical `9:16`** (ex.: `540×960`, `720×1280` ou `1080×1920`), FOV cinematográfico (`55–70`), HUD oculto ou limpo (`F1` / invisibilidade sem nametag), nuvens vanilla desligadas ou acima do teto das cenas.
   - Se usar **Distant Horizons**, reduza `numberOfThreads` durante a gravação para não competir por CPU/GPU após grandes comandos `fill`.
2. **Datapack `queda` instalado no mundo ativo**:
   - Copie `ferramentas/animacao-no-jogo/datapack_queda/` para `<pasta_da_instancia>/saves/<mundo>/datapacks/queda/` e rode `/reload`.
   - Ele fornece duas funções vitais no servidor:
     - `queda:tick`: move o rig da câmera (`@e[tag=voa_cam]`) todo tick no servidor com `$tp @s ~$(vx) ~$(vy) ~$(vz)` lendo `storage queda:cam` (elimina 100% da tremedeira de rede).
     - `queda:aplica`: aplica recursivamente num **único tick** todas as transformações de `storage queda:p lista` (`$data merge entity ...`), impedindo que olhos, pálpebras, boca ou chapéu/coroa atrasem em relação à cabeça.
3. **Ferramentas locais no Sistema**:
   - **Python 3.10+** com `numpy` e `openai-whisper` (ou `faster-whisper`).
   - **FFmpeg + FFprobe** no `PATH` (com suporte a `libx264`, `libass`/`subtitles`, `loudnorm`, `sidechaincompress`).
   - **Fonte `Monocraft.ttf`** em `<projeto>/fontes/usar/` (ou `biblioteca/`).
   - **Voz TTS**: acesso ao **Google AI Studio** (`aistudio.google.com/generate-speech`, voz padrão **Rami** em PT-BR via Chrome com remote debugging ou API Gemini TTS).
4. **Variáveis de ambiente suportadas pelos scripts**:
   - `ANIM_PROJETO`: caminho da pasta de trabalho do vídeo atual (ex.: `D:\minecraft\novo_video`, fora do repo público para não versionar `.mp4`/`.wav` pesados).
   - `MC_JOGADOR`: nick do jogador na sessão (padrão `@p`).
   - `MC_ASSETS_DIR` (opcional): pasta `assets` do launcher (auto-detectada em `%APPDATA%\ModrinthApp\meta\assets` ou `%APPDATA%\.minecraft\assets`).

---

## 2. Os 5 Pilares de Qualidade do Modelo "O Vaso Vazio"

O sucesso de **"O Vaso Vazio"** vem da combinação rigorosa de cinco pilares que **nunca devem ser simplificados**:

1. **Fidelidade Cirúrgica à Referência + Protagonista Próprio**:
   - Todo beat narrativo, intenção de câmera, contraste visual (ex.: plantas gigantes coloridas dos rivais vs. vaso pequeno vazio de Ping; close da semente cozida nos hashis; coroação emocionante) e curva dramática da referência são preservados, mas reencenados com identidade própria no Minecraft tendo a **Capivara Ping** (com laranja e folha na cabeça + traje temático da história) como protagonista.
2. **Duração ≥ 60 Segundos (Meta: `61 s – 68 s`) para Monetização no TikTok**:
   - Se o vídeo de referência tiver menos de 60 segundos (ex.: `45–58 s`), **nunca estique os planos deixando o vídeo lento**. Mantenha o ritmo ágil (`~1,2–1,5 s` por plano) e escreva um **epílogo orgânico de 3 a 5 planos** (ex.: em *Vaso Vazio*, P44–P47 mostraram Ping no trono distribuindo sementes verdadeiras e o reino florescendo, levando o vídeo de `58,5 s` para `65,9 s`).
3. **Modelos 3D Ricos (`ModeloRico`) e Proporções Anatômicas Anti-Clipping**:
   - Nada de blocos brutos sem forma ou personagens genéricos atravessando móveis. Objetos usam geometria octogonal (`0° + 45°`), pétalas radiais, vidro translúcido e macro-props dedicados; personagens têm escalas hierárquicas (`Ping 1.0`, `Rivais 1.0`, `Rei 1.18`), rostos animados em placas milimétricas e offsets matemáticos que impedem braços de entrarem na cabeça ou pés de afundarem no piso.
4. **Cenário 360° Construído para a Câmera**:
   - Nenhum cenário "procurado no mapa vanilla". Tudo nasce de `SET` sobre uma ilha cercada por praias orgânicas e um anel 360° de serras verdes arborizadas (escondendo o fim de chunk), iluminação interna `level=15` uniforme e marcenaria projetada para zero colisão nos closes.
5. **Captura Determinística 30 FPS + Edição e Sound Design Cinematográficos**:
   - Zero engasgos (`0%` de quadros repetidos) graças à captura por framebuffer com `/tick rate 3.4` + pré-roll de câmera, efeitos sonoros `.ogg` cravados no milissegundo da ação, cor vibrante e quente, legenda de 1 palavra com micro-pop e mix `-12 LUFS` com whoosh e sidechain ducking.

---

## 3. Passo a Passo Completo de Criação (Do Link ao MP4 Final)

> **Dica de Velocidade (Execução Paralela):** Não trabalhe de forma puramente sequencial esperando cada etapa lenta terminar. Assim que a **Bíblia do Cenário** e o `config_<video>.py` (`SET`) estiverem definidos (Etapa 1), dispare **em paralelo** (via subagentes ou tarefas simultâneas):
> - **Frente A:** Geração do TTS, alinhamento Whisper + `ajustar_tempos.py` e fechamento dos timestamps em `planos.json`;
> - **Frente B:** Construção do cenário no Minecraft (`set_<video>.py`);
> - **Frente C:** Modelagem dos personagens e objetos 3D (`elenco.py`).

### Etapa 1 — Engenharia Reversa da Referência, Roteiro (>60s) e Bíblia do Cenário

1. **Estudo Quadro a Quadro da Referência**:
   - Ao receber um link de referência (YouTube Shorts, TikTok, Reels), baixe-o temporariamente fora do repositório público, extraia o áudio/transcrição e gere uma folha de quadros (`1–2 fps`) para mapear:
     - **Abertura (0–3 s)**: qual imagem + primeira frase prendem a atenção imediatamente?
     - **Decupagem completa**: ângulo de cada plano (plongée, contra-plongée, perfil, 3/4, OTS, super-close macro), quem está em cena, que objeto segura, qual expressão facial faz e onde corta.
     - **Vídeos SEM FALA (Mudos)**: quando a referência não tiver narração, decupe a história em **beats visuais de `0,9–1,6 s`**, prestando atenção redobrada às **micro-expressões faciais** (`fechar`, `boca_ab`, `brava`, `sorriso`), silhueta clara das ações e **efeitos sonoros pontuais** em cada movimento/reação (pois o SFX + música carregam 100% do ritmo!).
2. **Roteiro Adaptado (`roteiro/narracao.txt`)**:
   - Escreva frases curtas, diretas, faladas, sem gordura, adaptando o protagonista para **Ping** (a Capivara mascote do canal).
   - Confira a contagem de palavras: para passar de **60 segundos** com narração natural (~2,3 a 2,6 palavras/s), mire em **145 a 165 palavras** (ou adicione o epílogo narrativo ao final).
   - **Regra de Direitos Autorais (`CLAUDE.md`)**: nunca suba vídeo/áudio de terceiros no GitHub; crie sempre adaptação própria com nossos rigs, cenários e texto em PT-BR.
3. **Bíblia do Cenário (`roteiro/biblia_cenario.md`) + `config_<video>.py`**:
   - Antes de colocar 1 bloco no jogo, monte a tabela `Frase/Beat → Fato visual obrigatório → Elemento em SET → Planos` (veja `exemplos/06-vaso-vazio/biblia_cenario.md`).
   - Se a frase diz *"ficou vigiando pela janela"*, o cenário **precisa** ter uma janela real vazada (`air`), um peitoril sólido onde o vaso apoia, um banquinho interno na altura certa para Ping não bater no muro e interior iluminado/decorado atrás dele!
   - Centralize **todas** as coordenadas e alturas em `config_<video>.py` (`SET`, `Y`, `YP`, `YJ`). Nenhum outro arquivo chuta coordenadas fora de `SET`.

---

### Etapa 2 — Voz (TTS), Alinhamento Palavra a Palavra e `planos.json`

1. **Geração da Narração (`audio/narracao.wav`)**:
   - Gere a locução em PT-BR no **Google AI Studio** (`Generate Speech`) usando a voz **Rami** com instrução de contador de histórias envolvente, quente e expressivo, e converta para WAV PCM `48000 Hz`:
     ```bash
     ffmpeg -y -i audio/narracao.mp3 -ar 48000 -ac 1 audio/narracao.wav
     ```
   - *(Se precisar estender um vídeo já gravado para >60s: gere apenas `epilogo.wav` com a mesma voz Rami e concatene com pequeno respiro de `0.25 s` ao final de `narracao.wav`, preservando intactos os timestamps de P01..PN anteriores!)*
2. **Transcrição Word-Level + Correção Pós-Pausa (`pal_aj.json`)**:
   - Extraia os timestamps por palavra com Whisper (`word_timestamps=True` → `audio/pal.json` no formato `[[t0, t1, "palavra"], ...]`).
   - **OBRIGATÓRIO:** rode `ajustar_tempos.py` logo em seguida:
     ```bash
     python ferramentas/shorts-farm/ajustar_tempos.py audio/narracao.wav audio/pal.json audio/pal_aj.json -32 0.08
     ```
   - *Por quê?* O Whisper sempre adianta `0,1–0,3 s` a primeira palavra depois de uma pausa respiratória; `ajustar_tempos.py` cruza com `silencedetect` do FFmpeg e crava o início exato da voz.
3. **Montagem de `roteiro/planos.json`**:
   - Quebre a história em **~42 a 50 planos** (`~1,0 s a 1,8 s` por plano), cortando exatamente no início das palavras-chave de `pal_aj.json` (`t0` do plano seguinte = `t1` do plano anterior, sem buracos pretos).
   - Cada item de `planos.json` define `nome` (`P01..P47`), `t0`, `t1`, `take`, `frase_trecho` e `descricao_visual`.

---

### Etapa 3 — Construção do Cenário Cinematográfico (`set_<video>.py`)

Use `exemplos/06-vaso-vazio/set_vaso.py` como template base. Siga estas regras arquitetônicas:

1. **Conexão Rápida, Divisão de `fill` e Checkpoints**:
   - Use conexão `http.client.HTTPConnection` **keep-alive** direto na ponte `~/.mcpfabric/bridge.json` (10× mais rápido que abrir processo por comando).
   - Na função wrapper `C(cmd)`, divida recursivamente ao meio qualquer `fill` com `> 32.000` blocos e qualquer `fillbiome` com `> 20.000` blocos (evita erro de limite do Minecraft).
   - Sempre chame `forceload add` antes de editar áreas distantes da câmera e `forceload remove` ao terminar o tile. Salve cada etapa concluída em `checkpoints/set_feito.txt` para que o script seja 100% retomável.
2. **Ilha sobre o Oceano + Horizonte 360° Fechado (Zero Fim de Mapa)**:
   - Construa uma base limpa (`canvas` ~`260×280` blocos em `Y=64`, bioma `minecraft:flower_forest` para grama verde-viva e água azul-turquesa).
   - Desenhe **praias orgânicas** nos 4 lados moduladas por soma de senóides (`onda()`).
   - Levante um **anel 360° de serras ao Norte/Sul e colinas a Leste/Oeste** (`serra()` + `verdejar_serras()`):
     - **Truque anti-listra marrom:** nas encostas íngremes, preencha os 4 blocos do topo com `grass_block` e aplique `moss_block` nas encostas visíveis (verde nas 6 faces do bloco — elimina aquelas escadinhas marrons de terra feias ao fundo!).
     - Plante centenas de árvores variadas (`cherry`, `oak`, `spruce`, `birch`) garantindo `grass_block` embaixo e `air` acima antes de `place feature`.
   - Rode `naturalizar()` aplicando colinas suaves por ruído multiplicadas por uma **máscara protetora suave (`mascara_ilha(x, z)`)** que vale `0.0` sobre todas as construções, praças e caminhos, subindo suavemente até `1.0` a 20 blocos de distância.
3. **Arquitetura Pensada para Câmera e Zero Colisão**:
   - **Pé-direito e amplitude:** salões internos devem ter pelo menos `10–12` blocos de altura livre e colunas afastadas do eixo central (ex.: 31 blocos livres de vão) para travellings e contra-plongées nunca baterem em pilastras ou lustres.
   - **Iluminação 15 Uniforme ("Luz de Estúdio"):** combine janelas/painéis treliçados (`oak_fence` + `birch_planks` + `shroomlight` pelo lado externo) com uma **grade 3D invisível de `light[level=15]`** (`fill x y z x y z light[level=15] replace air` a cada 3–4 blocos) em todos os interiores. Nenhum close fica escuro ou acinzentado.
   - **Marcenaria Anti-Clipping:**
     - **Tronos e cadeiras:** use `slab[type=bottom]` (`altura +0.50 m`) livre na frente (sem escada invertida ou bloco cheio trancando a frente da canela), permitindo dobrar o joelho a `90°` com os pés no piso.
     - **Bancadas e Janelas para a Capivara:** como Ping tem `0,80 m` de altura nas pernas/tronco, coloque um **banquinho baixo (`spruce_slab[type=bottom]`, `+0.50 m`)** recuado a `~1,1–1,3 m` atrás da mesa ou peitoril da janela. Assim as patinhas alcançam o vaso por cima do tampo sem a barriga ou o focinho entrarem na parede!
     - **Fumaça em closes:** `campfire` gera fumaça marrom grande que tapa closes macro. Nos planos fechados (ex.: panela fervendo), troque temporariamente o `campfire` por `magma_block` + partículas controladas (`bubble_pop`, `splash`) e restaure no `finally`.
4. **Fotos de Verificação (`fotos()`)**:
   - Antes de gravar qualquer plano, gere screenshots dos pontos-chave (`vista_palacio_ext.png`, `vista_salao_trono.png`, `vista_jardim_casa.png`, `vista_janela.png`, `vista_cozinha.png`) e inspecione visualmente com `read_file` para validar enquadramento, iluminação e horizonte.

---

### Etapa 4 — Modelos 3D (`ModeloRico`), Rigs Articulados e Regras de Proporção (`elenco.py`)

Toda a geometria de personagens e objetos usa a unidade base **`U = 0.06 m`** (equivalente a 1 pixel da skin clássica do Minecraft). Isso mantém todas as texturas, espessuras de roupa, olhos e acessórios em harmonia visual perfeita.

#### 4.1 Hierarquia de Proporções e Escalas entre Atores
| Tipo de Ator | Classe Base (`elenco.py`) | `escala` | `ALT_CHAO` (centro → piso) | Dimensões Principais | Quando Usar |
|---|---|---|---|---|---|
| **Mascote Protagonista (Ping)** | `PingCapivara(M.Capivara)` | `1.0` | `13.4 * U` (`0.804 m`) | Tronco `10×11×8 U`, Cabeça `13×10×12 U`, Focinho até `+0.62 m`, Laranja + Folha no topo | Protagonista carismático em todos os vídeos; contraste visual ótimo ao lado de humanos mais altos. |
| **Humanos / Jovens / Coadjuvantes** | `Rival(M.Pato)` | `1.0` | `18.0 * U` (`1.080 m`) | Tronco `8.2×12×4.2 U`, Cabeça `8×8×8 U`, Braços `10 U`, Pernas `12 U` | Coadjuvantes, rivais, aldeões estilizados, amigos (diferencie por cor da túnica e penteado/chapéu 3D). |
| **Autoridade / Rei / Mentor / Vilão** | `Rei(M.Pato)` | `1.18` | `18.0 * U * escala` (`1.2744 m`) | Tronco imperial `8.6×12×4.8 U` + saia longa, mangas largas, barba em 3 camadas | Personagens imponentes ou mais velhos/altos em cena. |

> **REGRA CRÍTICA DE ESCALA (`ALT_CHAO`):** Sempre que criar um personagem com `escala != 1.0`, calcule **`self.ALT_CHAO = ALT_CHAO_BASE * escala`** (ex.: `18 * U * 1.18 = 1.2744 m`) e posicione-o em `y = Y_SUPERFICIE_PISO + ator.ALT_CHAO` (onde `Y_SUPERFICIE_PISO = bloco_y + 1.0`, ex.: piso no bloco `y=68` → superfície exata `YS = 69.0`). Sem multiplicar por `escala`, os pés afundam no chão!

#### 4.2 Geometria Anti-Clipping (Anatomia da Capivara, Assentos e Objetos Segurados)
Estes números foram calibrados e validados no *Vaso Vazio* para eliminar 100% de interpenetrações:
1. **Ombros e Braços da Capivara Ping:**
   - A cabeça da Capivara é larga (`13*U` → `±6.5*U` = `±0.39 m`) e o focinho avança até `+0.62 m`.
   - Com ombros padrão (`±6.0*U`), levantar os braços fazia os braços sumirem dentro das bochechas/cabeça!
   - **Solução obrigatória (já em `PingCapivara`):** pivôs dos ombros abertos e adiantados em **`(±6.8 * U, 9.0 * U, +1.5 * U)`** com braços+mãos somando `9.6 * U`, abdução leve nas poses frontais (`braco_e: (-60, 0, -13)`, `braco_d: (-60, 0, +13)`) e **pitch da cabeça limitado a `≤ 15°`** quando segura objetos.
2. **Distância Exata de Objetos Segurados nas Mãos:**
   - **Na Capivara (`PingCapivara`):** posicione o vaso/objeto a **`0.56 m` à frente** do centro de Ping na direção de `ori` (`dx = -sin(rad)*0.56`, `dz = cos(rad)*0.56`) e na altura **`Y_PISO + 0.46 m`**.
   - **Em Humanos (`Rival`):** posicione o vaso/objeto a **`0.48 m` à frente** e na altura **`Y_PISO + 0.80 m`**.
3. **Anatomia Sentada Real (Joelho Dobrado em `90°` sem entrar no Trono):**
   - Apenas girar `perna_e/d` em `-90°` num bloco único faz a coxa atravessar o assento ou flutuar longe da cadeira.
   - Em `Rei._rosto()` (quando `self.pose == 'sentado'`), a perna se divide dinamicamente em **coxa horizontal** sobre a almofada (`y=71.50`) e **`canela_e/d` + `pe_e/d` verticais** descendo a `90°` na frente do assento até tocar o tapete (`y=71.00`), encurtando também `tunica_saia` para não rasgar o banco!
4. **Acessórios de Cabeça sob Medida:**
   - A Capivara tem a laranjinha (`y = 10..14.2*U`) e a folha (`y = 14.2..15*U`) no topo da cabeça. Qualquer chapéu/capacete/coroa feito para ela (como `criar_coroa_imperial`) precisa ter aro `0.82×0.76 m` e **cúpula oca/elevada (`0.21 m`)** para acomodar a laranja sem atravessar, além de cordões pendentes parando acima da linha das sobrancelhas.
   - Se um ator entrega um acessório que vestia (ex.: Rei tira a própria coroa para coroar Ping), use `rei = Rei('rei', com_coroa=False)` ou `rei.set_coroa(False)` (escala `(0,0,0)` nas peças `coroa_*`).

#### 4.3 Expressões Faciais Vivas em Placas Finas (`EPS = 0.004 m`)
Todo personagem possui placas faciais escalonadas em `z` por múltiplos de `EPS = 0.004 m` (zero *z-fighting*) controladas por 4 variáveis contínuas (`0.0` a `1.0`):
- `fechar`: desce as pálpebras (`palp_e/d`), esconde o brilho especular (`brilho_e/d`) acima de `0.5` e afina o olho em linha acima de `0.85` (use para piscadas naturais de `3 ticks` e olhares tristes/serenos).
- `boca_ab`: abre a boca verticalmente (choque, fala solene, comemoração).
- `brava`: inclina/abaixa as sobrancelhas (seriedade, esforço, determinação).
- `sorriso`: faz brotar os cantos curvados do sorriso (`sorr_e/d`), alarga e ergue levemente a boca, arqueia as sobrancelhas e faz aparecer bochechas rosadas (`boch_e/d` na Capivara).

#### 4.4 Modelagem de Objetos 3D Esculpidos (`ModeloRico`)
A classe `ModeloRico` (em `elenco.py`) estende `motor.Modelo` permitindo peças com **rotação local `(yaw, pitch, roll)` em torno de qualquer pivô**:
- `(bloco, canto, tamanho)` → caixa ortogonal rápida;
- `(bloco, pivo_base, tamanho, (yaw, pitch, roll))` → peça inclinada/girada crescendo a partir de `pivo_base`;
- `(bloco, pivo, tamanho, (yaw, pitch, roll), canto_relativo)` → controle total de pivô + offset.

**Técnicas de escultura 3D para manter o padrão "Vaso Vazio":**
- **Cilindros / Vasos / Regadores Redondos:** sobreponha duas caixas concêntricas na mesma faixa de altura, uma a `0°` e outra girada a `(45, 0, 0)` (ligeiramente menor para casar as quinas) + borda superior oca em 4 barras formando cavidade real com `mud`/`rooted_dirt` dentro!
- **Plantas e Corolas Orgânicas:** caules em 3 segmentos com leve inclinação alternada (`pitch +4°, -5°, +6°`), folhas abrindo radialmente a cada `60°` (`pitch=58°`) e flores com `8` pétalas externas (`pitch=64°`), `6` internas (`pitch=42°`) e miolo luminoso (`gold_block`/`shroomlight`).
- **Líquidos e Recipientes Translúcidos:** use `light_blue_stained_glass` + `white_stained_glass` nas paredes/superfície para que a câmera veja os objetos submersos (ex.: as 6 sementes cozinhando e bolhas 3D dentro do caldeirão).
- **Modelos Dedicados de Super-Close (Macro):** quando a referência tiver um plano detalhe extremo (ex.: semente rachada ao meio segurada por hashis soltando vapor), construa uma função dedicada (`criar_semente_hashi`) em escala generosa e rica em micro-detalhes em vez de dar zoom exagerado num cubinho minúsculo.

#### 4.5 Atualização Atômica no Mesmo Tick (`posar` e `posar_varios`)
- Toda entidade `block_display` nasce com `brightness:{sky:15,block:15}` e transformação **decomposta** (`translation`, `left_rotation` em quatérnio garantindo `dot(q, q_anterior) >= 0` para nunca dar giro fantasma de 360°, e `scale`).
- `posar()` guarda a string da última transformação em `self._ult[nome]` e **nunca reenvia peça que não mudou** (reenviar a mesma transformação no Minecraft faz a peça piscar!).
- Quando houver 2 ou mais atores animando no mesmo tick (ex.: os 3 rivais chocados ou coçando a cabeça juntos), chame **`posar_varios([(riv1, {...}), (riv2, {...}), (riv3, {...})], dur=5)`** para empacotar tudo numa única chamada a `function queda:aplica`.

---

### Etapa 5 — Direção de Cena, Captura Determinística 30 FPS e SFX In-Game (`takes_<video>.py`)

Use `exemplos/06-vaso-vazio/takes_vaso.py` como arquitetura padrão de gravação:

1. **Por que Captura Determinística com `/tick rate 3.4`?**:
   - Gravação de tela em tempo real a `20 ticks/s` sofre com engasgos de janela, GC da JVM ou jitter do Python.
   - Reduzindo o relógio do servidor para **`/tick rate 3.4`** (`K_SLOW = 20.0 / 3.4 ≈ 5.88×` mais calmo no tempo real), o laço de captura solicita exatamente `n_frames = round(dur * 30)` screenshots via RPC keep-alive (`vision.screenshot`) espaçados por `DT_WALL = K_SLOW / 30` (`~0,196 s` reais por frame) e envia direto por `stdin` (`image2pipe`) ao FFmpeg já escalando em `1080×1920` Lanczos e aplicando o color grading!
   - **Resultado:** `30 fps` matematicamente perfeitos, **0% de quadros repetidos** e funcionamento confiável mesmo sem foco de janela ou em sessão isolada.
2. **Câmera Lisa (`Vel`) + Pré-Roll de `0.06 s` (Zero Quadro Parado no Corte)**:
   - A câmera é o jogador invisível montado num `block_display` (`camrig`) movido todo tick no servidor pela classe `Vel` (`datapack queda:tick`).
   - Recue a posição inicial da câmera em `cpos_pre = cpos - v_cam * 0.06`, ative `tc.tick(0.0)` sob `/tick rate 3.4` e aguarde `time.sleep(0.06 * K_SLOW)` **antes** de capturar o quadro `f = 0`. Assim o veículo já está em velocidade cruzeiro no primeiro frame e todo corte entra em movimento!
   - Para caminhadas de atores e trajetória de objetos (sementes caindo, coroa descendo), use `TrajetoJogo(seletor, fn_pos_em_t_jogo, passo=0.15)` (calcula `teleport_duration` automaticamente em ticks de jogo).
3. **Gramática de Enquadramento Vertical (`9:16`)**:
   - **Personagem grande e em `3/4`:** câmera a `1,8 m – 3,8 m` nos planos médios e `1,1 m – 2,1 m` nos closes; use `ori_para(pos_ator, cpos, offset_yaw=±15..25°)` para nunca chapar o focinho de frente nem esconder o rosto de costas.
   - **Zona segura da legenda:** em `1080×1920`, a legenda fica na faixa inferior-média (`MarginV=700`, `y ≈ 1150–1240 px`); mantenha rostos e objetos cruciais no terço central/superior (`mirar_ponto(cpos, alvo)`).
   - **Partículas vivas sincronizadas:** em cenas de água, terra, magia, florada ou vitória, dispare partículas (`splash`, `falling_water`, `block{block_state:"minecraft:rooted_dirt"}`, `bubble_pop`, `cherry_leaves`, `end_rod`) nos ticks certos do plano.
4. **Áudio In-Game Sintetizado Direto dos `.ogg` Oficiais (`render_audio_plano`)**:
   - Como a captura visual roda em slow-motion determinístico (`/tick rate 3.4`), não gravamos o áudio da placa de som. Em vez disso, cada chamada `snd_cam('evento.minecraft', vol, pitch)` dentro de `fn_inicio` ou `fn_tick` registra o timestamp exato `_T_ATUAL` do plano (`0.000 s .. dur`).
   - Ao fim do plano, `render_audio_plano()` resolve o evento no `minecraft/sounds.json` oficial dos assets locais, aplica `pitch` (`asetrate=48000*pitch,aresample=48000`) e `adelay` em milissegundos no FFmpeg e gera `tmp/seg/aXX.wav` cristalino, sem ruído de fundo e cravado no frame exato de cada passo, gota d'água, plantio ou acorde de ametista!

---

### Etapa 6 — Auditoria Visual Obrigatória Antes do Render Final

**REGRA INEGOCIÁVEL:** Nunca entregue o vídeo final sem auditar todos os planos gravados (`tmp/seg/v00.mp4 .. vNN.mp4`)!

1. Gere folhas de contato (ou extraia 2–3 frames por plano: início, meio e fim) e inspecione visualmente com `read_file` procurando:
   - Braço ou pata entrando na cabeça/focinho/tronco;
   - Personagem afundando no piso, flutuando ou entrando dentro de trono/mesa/parede;
   - Rosto cortado pela borda do quadro ou coberto por fumaça/folha de árvore/pilar;
   - Fundo mostrando vazio de chunk ou terra marrom crua.
2. Qualquer plano com defeito é corrigido em `takes_<video>.py` (ou `elenco.py`) e regravado isoladamente em poucos segundos:
   ```bash
   python takes_vaso.py P05 P12 --refazer
   ```
3. *(Opcional — Integração com VideoHub)*: se o projeto VideoHub estiver disponível na máquina (`D:\minecraft\videohub`), o vídeo pode ser aberto na timeline interativa para coleta de notas pontuais por timestamp.

---

### Etapa 7 — Edição, Color Grading, Legenda e Masterização (`montar_<video>.py`)

Com `v00.mp4..vNN.mp4` e `a00.wav..aNN.wav` aprovados, rode `python montar_vaso.py --so-final` (ou completo se vier de sessão bruta `.mkv`). Os parâmetros exatos do modelo **"O Vaso Vazio"** são:

1. **Color Grading Quente e Vibrante ("Brinquedo Cinematográfico")**:
   ```text
   eq=saturation=1.38:contrast=1.08:gamma=0.98,vibrance=intensity=0.28,colorbalance=rs=0.02:gs=0.01:rh=0.03,vignette=angle=0.38
   ```
2. **Legenda Viral `.ass` de 1 Palavra (`Monocraft`) com Micro-Pop**:
   - Fonte `Monocraft`, tamanho `66`, Negrito (`-1`), cor primária branca `&H00FFFFFF`, contorno preto grosso `Outline=4`, sombra `Shadow=3`, `Alignment=2`, `MarginV=700` (em `PlayResX: 1080`, `PlayResY: 1920`).
   - Cada palavra de `pal_aj.json` entra sozinha (sem pontuação pendurada) com animação elástica rápida de `70 ms`:
     ```ass
     {\fscx88\fscy88\t(0,70,\fscx100\fscy100)}palavra
     ```
   - *(Em vídeos 100% mudos/sem narração, omita o filtro de legenda para deixar a imagem limpa como na referência).*
3. **Whoosh Procedural Suave nos Cortes + Mixagem de 4 Canais a `-12 LUFS`**:
   - `whoosh()` gera ruído filtrado curto (`0.26 s`, amplitude `0.16`) centrado em cada corte (`t0` de `P02..PN`).
   - Mixagem FFmpeg de 4 pistas:
     - **Narração:** `volume=1.0` (também enviada como chave `[sc]` do compressor sidechain);
     - **SFX do Jogo (`jogo.wav`):** `volume=0.55`;
     - **Música de Fundo (`biblioteca/`):** `volume=0.24` + `sidechaincompress=threshold=0.03:ratio=5:attack=20:release=300` (abaixa suavemente quando a voz fala e sobe nas pausas/epílogo) + `afade=t=out:d=1.8` no encerramento;
     - **Whoosh (`whoosh.wav`):** `volume=0.75`.
   - **Masterização final:** `loudnorm=I=-12:TP=-1.0:LRA=9`, vídeo `libx264 -crf 17 -preset medium -pix_fmt yuv420p -r 30`, áudio `aac -b:a 192k -ar 48000 -movflags +faststart`.

---

## 4. Checklist Final de Entrega (Conferir Todo Vídeo)

- [ ] **Duração total ≥ 60,0 s** (ideal `61–68 s` para monetização no TikTok) mantendo cortes dinâmicos (`~1,0–1,6 s/plano`).
- [ ] **Fidelidade à referência**: todos os beats narrativos, contrastes visuais, ângulos-chave e clímax emocional estão presentes e claros.
- [ ] **Zero clipping anatômico ou de cenário**: braços da Capivara fora do focinho, pés tocando exatamente o piso (`ALT_CHAO * escala`), poses sentadas com joelhos em `90°`, objetos segurados nas distâncias exatas (`0.56 m` Ping / `0.48 m` humanos).
- [ ] **Fluidez 30 fps**: `0%` de engasgos nos travellings, sem quadro estático morto no início dos cortes.
- [ ] **Áudio e Legenda**: palavras sincronizadas pós-pausa (`ajustar_tempos.py`), SFX `.ogg` encaixados nas ações visuais, música com ducking sem brigar com a voz e loudness integrado em **`-12 LUFS`** (`ebur128`).
- [ ] **Higiene de Repositório Público**: vídeos/áudios brutos e referências de terceiros mantidos apenas na pasta de trabalho fora do Git; código novo e aprendizados registrados em `aprendizados.md`.
