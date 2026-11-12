# Do Minecraft para o Blender (cenário, personagens, efeitos)

Pesquisa de 12/11/2026. Neste PC: **Blender 5.2.3 LTS** instalado e roda por script (`blender -b`). Nenhum add-on de Minecraft instalado ainda.

## 1. Ferramentas
| Ferramenta | Para que | Versão / compatível | Link |
|---|---|---|---|
| **Mineways 14.02** | exporta um pedaço do mundo (blocos + texturas) para OBJ ou USD | Minecraft Java até **26.3** · Windows | realtimerendering.com/erich/minecraft/public/mineways |
| jmc2obj 128 | mesma função, alternativa | Minecraft até 1.21.9 (mais antigo) | github.com/jmc2obj/j-mc-2-obj |
| **MCprep 3.6.3** | add-on do Blender: importa o mundo com materiais certos, spawner de mobs, itens e blocos, rigs, clima com geometry nodes | Blender 2.83 a **5.2** · recursos até Minecraft 26.2 | github.com/Moo-Ack-Productions/MCprep |
| MiBlend 0.8 (beta) | alternativa nova ao MCprep (mundo, PBR procedural, neblina) | Blender 4.2 a 5.3 · Mineways só parcial | github.com/Aspirata/MiBlend |
| Blockbench | modelar personagens e objetos no estilo Minecraft; exporta para Blender (glTF/OBJ) e para o jogo | — | blockbench.net |

Escolha padrão: **Mineways (USD ou OBJ) + MCprep**.

## 2. Passo a passo: cenário
1. No jogo, construa ou ache o cenário (pode ser montado pelo MCP).
2. Mineways: abra o mundo → selecione a área → File → Export for Rendering → OBJ (ou USD). Marque "export separate objects" se quiser mexer em blocos sozinhos.
3. Blender: MCprep → World Imports → importar o OBJ → **Prep Materials** (texturas nítidas, transparência, brilho de lava/tocha).
4. Luz: céu (MCprep World Tools ou HDRI) + sol forte de um lado.
5. Clima e ar: neblina volumétrica, poeira, chuva/neve (MCprep weather).
6. Render: Eevee para teste, Cycles para o final.

Dica: blocos que vão quebrar na cena precisam ser objetos separados (export separado ou "separate by loose parts").

## 3. Passo a passo: personagens
- **Rig de jogador do MCprep** + skin própria (Skin Swap) → anima no Blender (pose, andar, soco, voo).
- Personagem especial (roupa, cabelo, acessório): modela no Blockbench → exporta glTF → rig no Blender.
- Mobs e villagers: Mob Spawner do MCprep.
- Rosto: troca de textura do rosto por quadro (olhos/boca) ou formas no modelo; a boca segue o lip sync do guia 10 §5.
- **Mods não vêm junto:** o Mineways só conhece blocos normais do Minecraft. Blocos e personagens de mods (ex.: Dragon Mine Z) não exportam com textura. No Blender, refaça-os no Blockbench ou como efeito.

## 4. Efeitos (o que deixa a cena "muito bem ambientada")
| Efeito | Como fazer no Blender |
|---|---|
| aura de energia | malha em volta do corpo com shader de emissão + ruído animado + partículas subindo; glare/bloom no compositor |
| raio de energia | cilindro/curva com emissão forte, núcleo branco e borda colorida; luz pontual andando junto; tremida da câmera |
| choque de 2 raios | 2 raios + esfera de luz no meio pulsando + faíscas (partículas) + onda de choque |
| explosão | simulação de fogo e fumaça (Quick Smoke/Mantaflow) ou sprites; flash de luz de 2–3 quadros |
| cratera / blocos voando | quebrar blocos (Cell Fracture ou blocos soltos) + física de corpo rígido |
| onda de choque | anel com emissão crescendo + distorção + poeira levantando |
| velocidade | linhas de velocidade (partículas esticadas) + motion blur + FOV abrindo |
| voo no céu | câmera seguindo + nuvens volumétricas + linhas de vento |
| transformação | luz por baixo, aura crescendo, raios elétricos (curvas com emissão piscando), blocos do chão subindo |
| impacto de soco | 2 quadros de flash, câmera tremendo, anel de poeira, pausa de 3–4 quadros (hit stop) |

Sempre: neblina e poeira no ar, luz colorida vinda do efeito, câmera com tremida leve nos impactos, compositor com glare e correção de cor.

## 5. Dragon Mine Z (avaliação)
- Mod de Dragon Ball para Minecraft. Versão mais nova achada: **2.1.3 (jul/2026), só Forge 1.20.1**. Não há versão Fabric nem 26.x.
- Consequências:
  - Precisa de **outra instância** (Forge 1.20.1), separada da instância de gravação (Fabric 1.21.11/26.x).
  - O MCP recomendado (`chapmanjw`) e o Flashback são só Fabric: **não rodam junto com o Dragon Mine Z**. No Forge seria MCP por RCON (servidor dedicado) e gravação com OBS.
  - Aura, golpes e transformações do mod **não exportam para o Blender**.
- **Direitos:** o mod usa personagens e transformações de Dragon Ball (obra protegida). Recriar cenas do anime, com nomes, visuais, falas, música ou dublagem, pode levar reivindicação ou derrubada e tirar a monetização.

**Recomendação:** fazer uma **série própria de luta estilo anime** no Blender: personagens próprios (skins e nomes seus), poderes próprios (cor, nome e forma da aura e dos golpes) e história própria, usando os elementos do gênero (treino, transformação, aura, raio de energia, luta no céu, cratera). Fica mais bonito que o mod, fica tudo no seu controle e o canal fica seguro.
Se mesmo assim quiser usar o Dragon Mine Z, use só para referência ou testes, não para vídeo monetizado.

## 6. O que o Claude automatiza no Blender
O Blender roda por script: `"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b cena.blend -P script.py`.
O Claude consegue:
- importar o OBJ do Mineways e preparar os materiais (operadores do MCprep por Python);
- montar câmera, luz, neblina e céu pelo `cenas.md` (os mesmos planos do guia 10);
- criar os efeitos da tabela acima a partir de modelos prontos (`efeitos.blend`, feito 1 vez);
- posicionar personagens e poses simples, e gerar os keyframes da boca pelo áudio;
- renderizar cada plano e montar no tempo da voz.
Fica com você (ou com um animador): a atuação de luta quadro a quadro.

## 7. Instalar (quando for usar)
1. Baixar Mineways 14.02 (site acima) e extrair numa pasta.
2. Baixar o .zip do MCprep 3.6.3 (GitHub Releases) → Blender → Edit → Preferences → Add-ons → Install from Disk.
3. Testar: exportar 1 casa do Minecraft, importar, Prep Materials, render Eevee.
