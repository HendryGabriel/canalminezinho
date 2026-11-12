# Edição: imagem, câmera, texto e ritmo

Base: 7 vídeos longos + 3 Shorts baixados em 480p e medidos com `ferramentas/medir_video.py` (detecção de corte do ffmpeg, limiar 0.3) + grades de quadros + análise do Gemini (`analises/gemini/`).
Os quadros ficam só no PC (`ESTUDOS/theluics/frames/`), porque o repositório é público.

## 1. Números medidos
| Vídeo | Duração | Cortes | Plano médio | Mediana | Volume |
|---|---|---|---|---|---|
| A verdadeira escala | 20,4 min | 199 | 6,1 s | 2,4 s | -20,1 LUFS |
| Nunca teve jogador | 29,2 min | 440 | 4,0 s | 2,0 s | -16,7 LUFS |
| Fábrica de todos os blocos | 25,9 min | 302 | 5,1 s | 2,5 s | -15,5 LUFS |
| 100% do Minecraft | 27,6 min | 219 | 7,5 s | 4,0 s | -21,0 LUFS |
| Mundo impossível | 24,9 min | 291 | 5,1 s | 3,3 s | -16,8 LUFS |
| Farm de redstone (vlog) | 17,4 min | 241 | 4,3 s | 2,3 s | -15,7 LUFS |
| Trailer planeta | 1,8 min | 20 | 5,1 s | 3,0 s | -15,3 LUFS |
| Shorts (3) | 1,8-2,3 min | 12-53 | 2,5-8 s | 2,0-3,7 s | -15 LUFS |

O detector não pega fusões e câmeras lentas contínuas, então o número real de planos é um pouco maior.

Leitura:
- **Metade dos planos dura 2-4 s.** Planos longos (10-20 s) só nas pausas com música e nos voos cinematográficos.
- **Abertura mais rápida:** 21-22 cortes no 1º minuto (1 a cada ~3 s).
- O ritmo sobe nas listas/rankings e nos clímax (escala: 50 cortes no minuto 19, a montagem final de mundos).
- Volume final entre -21 e -15 LUFS. Para nós: **-14 LUFS** (padrão do YouTube).

## 2. Os 6 tipos de imagem (o "visual TheLuics")
1. **Cinematic no jogo com shader**: paisagem com neblina, luz de fim de tarde, câmera de drone lenta (dolly/órbita). Shader parecido com Complementary/BSL. Horizonte longe (Distant Horizons).
2. **Estúdio 3D cinza** (Blender): fundo liso cinza-claro com **papel quadriculado** e sombra suave. Blocos e construções do jogo isolados, réguas de medida, círculos, texto 3D. É o cenário das explicações e contas.
3. **Construção isolada no vazio escuro**: a estrutura (mansão, bastion, iglu) sozinha num vazio azul-escuro com neblina. Dá para fazer no jogo: mundo void + `/place structure` + noite + shader.
4. **Espaço**: planetas feitos de blocos, galáxia de partículas, o mapa do Minecraft como cubo/placa ao lado da Terra e do Sol. Blender.
5. **Mapa visto de cima**: mapa do mundo (render top-down) com círculos verde/vermelho animados ("ZONA CINZA").
6. **Cenas de esquete**: personagens (villagers, Steve Bo, a skin dele, amarela de óculos) em cenários construídos (bar, igreja, laboratório, cidade realista). Com animação de personagem (Blender ou mod de animação).

Extras: fotos reais recortadas dentro da cena 3D (Coliseu, Basílica, Louvre), tela do menu do Minecraft como janela flutuando no estúdio, gravação de tela de app (patrocínio).

## 3. Câmera
- Drone lento para frente (dolly in) e órbita ao redor da construção.
- Câmera baixa ao lado do personagem para mostrar escala ("olha você do lado").
- Whip pan/slide rápido para revelar o próximo planeta/construção maior.
- Zoom brusco no rosto do villager como piada.
- Match cut: do modelo 3D no estúdio para o mesmo ângulo dentro do jogo.

## 4. Texto na tela
- **Não usa legenda corrida.** Só palavra-chave e número (1 a 4 palavras): "ZONA CINZA", "10.000 m", "Volume:", "60.000.000", "GIGAN..." (digitando).
- Fonte sem serifa grossa (tipo Montserrat/Poppins Black), branca, com contorno escuro ou sombra dura. Às vezes texto 3D dentro do estúdio.
- Texto aparece com **pop** (escala 50%→100% com bounce) ou **digitando**, no tempo exato da palavra falada.
- Às vezes uma frase pequena cinza em minúsculas, tipo legenda de nota ("tivesse dentro de paris", "ilustrativo", "exagero").
- **Contador** grande em fonte mono/pixel: "DIA: 3.711", "ANO: 101.413" no meio-baixo da tela.
- Números gigantes sobem como cronômetro (contagem rápida).
- Setas brancas curvas, réguas com medida (1 m, 58 m), círculos.
- Piada escondida no texto (seed "EU ODEIO MINECRAFT..." / "DEIXA O SEU LIKE").

## 5. Transições
- 90% corte seco.
- Fade para preto antes de capítulo e para entrar em clima de medo.
- Whip/slide com motion blur nas comparações.
- Match cut entre estúdio e jogo.

## 6. Humor na edição
- Música para de repente (corte de vinil) na quebra da piada.
- Silêncio desconfortável olhando um erro de propósito (a skin "realista" feia).
- Zoom rápido em rosto.
- Música clichê (acordeão francês em Paris).

## 7. Receita de montagem (DaVinci Resolve, grátis)
1. Narração na timeline (corte as respirações nas partes rápidas; deixe as pausas marcadas no roteiro).
2. Para cada frase, 1 plano. Planos de 2-4 s; 10-20 s só nas pausas.
3. Ordem de prioridade da imagem: estúdio 3D nas contas; cinematic nas emoções; mapa/espaço na escala; esquete no humor.
4. Textos com pop/digitando só nas palavras-chave e números.
5. Contadores e réguas: Fusion (no Resolve) ou Remotion (já usado no outro canal, ver skill `canal-dark/references/motion.md`).
6. Exportar 1080p ou 1440p, 60 fps (o canal dele sobe em 60 fps; 1440p dá mais bitrate no YouTube).

## 8. O que dá para automatizar aqui no PC
- Montagem por script com ffmpeg (já temos no canal Zé Cinza: zoom, cortes, mix -14 LUFS).
- Motion graphics (texto pop, contador, régua, círculo) com Remotion.
- Render de estúdio 3D com Blender em linha de comando (`blender -b cena.blend -P script.py`) — Blender ainda **não está instalado** neste PC.
- Cenas do jogo: o MCP do Minecraft monta o cenário; a gravação com câmera é no Flashback (ver `guia/06-minecraft-mcp-e-captura.md`).
