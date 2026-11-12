# Novelinha / machinima de histórias (formato 2 — Machinima)

Histórias entre personagens, em episódios, com itens da vida real (móveis, celular, TV, carro) e personagens que se mexem e fazem gestos. O jeito das séries de roleplay de Minecraft que fizeram sucesso no Brasil, com câmera de cinema/novela.
A IA monta o cenário, posiciona o elenco, filma de vários ângulos e corta no tempo das falas.

Regra de direitos: personagens, nomes, histórias e skins **próprios**. Não recriar séries, personagens ou bordões de outros canais.

## 0. O que os maiores canais gringos fazem (estudo de 12/11/2026)
Estudo completo: `analises/machinima/sintese.md` (+ `aphmau.md`, `maizen.md`, `cash.md`).

| | Aphmau (25 mi inscr.) | Maizen (18 mi) | Cash (12 mi) |
|---|---|---|---|
| Estilo | novela romântica | desenho dublado com roteiro | gincana com números |
| Views (mediana) | ~1 mi | ~2 mi | ~1,4 mi |
| Duração | ~21 min | ~24 min | ~19 min |
| Fala | ~170 pal/min, elenco ao vivo | ~120 pal/min, um fala por vez | ~220 pal/min |
| Legenda | só frase-chave | completa, cor por personagem | quase nada |
| Música | rara | o tempo todo | baixa |

O que os 3 fazem igual:
1. **Gravam no jogo, em primeira pessoa** do protagonista, com a barra do jogo na tela. Sem shader pesado, sem câmera de cinema. A sensação é "estou jogando com você".
2. **Elenco fixo** com cor ou visual fácil de reconhecer + **uma fantasia nova por vídeo** (lobisomem, rei dragão, bebê, família adotiva).
3. **Mapa e mods feitos para o roteiro:** celular, poderes, lojas com preço, contadores, transformações.
4. **Gancho no meio da ação** (0–40 s), premissa em 1 frase até 1:30, sem "olá".
5. 7–9 blocos de 1,5–3 min que crescem, viradas perto de 60% e 80%, **final feliz + piada**, CTA de 10 s sempre igual.
6. Público de 6–14 anos, mas **nenhum marcado "para crianças"**: tudo leve (morte vira piada, sem sangue).

**Decisão para o nosso formato 2:** a base é a deles (primeira pessoa no jogo, elenco fixo, mapa e regras feitos para o roteiro, episódio de ~20 min). A câmera de novela com vários ângulos (§4) entra **por cima**, nos momentos fortes: abertura do lugar, revelações, reações, clímax. É o nosso diferencial, sem perder a cara de "jogando junto".

### Molde de episódio (20 min)
| % | Em 20 min | Bloco |
|---|---|---|
| 0–3% | 0:00–0:35 | gancho no perigo ou na piada |
| 3–8% | 0:35–1:35 | premissa + regra ou número + o que está em jogo |
| 8–25% | 1:35–5:00 | 1ª tentativa, dá certo pela metade |
| 25–45% | 5:00–9:00 | escala + 1º racha no grupo |
| 45–60% | 9:00–12:00 | virada do meio (disfarce, plano descoberto) |
| 60–80% | 12:00–16:00 | maior desafio + momento emocional rápido |
| 80–92% | 16:00–18:30 | clímax visual (chefão, explosão, onda) |
| 92–98% | 18:30–19:40 | resolução + piada |
| 98–100% | 19:40–20:00 | CTA fixo de 10 s |
Um acontecimento novo a cada 60–90 s; troca de lugar a cada 2–3 min (= capítulos).

### Mecânicas do jogo que o Claude faz por comando (sem mod)
Placar (`/scoreboard`), timer (`/bossbar`), "UPGRADE!" (`/title`), avisos (`tellraw`), loja com preço (`text_display` + `/trigger`), onda/tsunami subindo (`/fill` de água agendado), explosões (TNT por comando), gigante/bebê (`/attribute ... scale`), celular e objetos (modelos próprios no pacote de textura).

### Títulos e thumbs
- Títulos: até 7 palavras, CAIXA ALTA na palavra de emoção, "!" ou ".." no fim. Fórmulas: "Fui ADOTADO por [família estranha] no Minecraft!", "Virei o REI [de X] no Minecraft..", "[NOOB] vs [PRO]: ...", "De POBRE a RICO: ...", "[Base X] vs [Desastre Y]!", "Nós [verbo] TODOS os [X]..". Mais 9 em `analises/machinima/sintese.md` §5.
- Thumb: render 3D com rosto expressivo (Blender), protagonista no centro, 1 ameaça ou desejo grande ao lado, tela dividida para comparar (POBRE/RICO), quase sem texto, cores fortes.

## 1. Formato do episódio
| Item | Valor |
|---|---|
| Duração | 6–12 min por episódio (Shorts: 1 cena de 45–60 s) |
| Elenco | 2–5 personagens fixos + figurantes |
| Estrutura | gancho (0–20 s) → situação → problema → complicação → virada → **gancho final "continua..."** |
| Ritmo | 1 piada ou reviravolta a cada 30–60 s |
| Série | o mesmo cenário (casa, escola, cidade) e o mesmo elenco em todo episódio |

### Fórmulas de história que funcionam
- "Meu primeiro dia de..." (emprego, escola, cidade nova)
- Vizinho chato / colega de quarto
- Segredo descoberto (celular esquecido, carta, câmera)
- Mistério na casa/cidade (barulho à noite, objeto sumido)
- Rivalidade com reviravolta (o vilão tinha razão)
- Família: pai rígido, irmão bagunceiro, avó que sabe de tudo
- Romance de novela (com ciúme, triângulo, casamento interrompido)

### Ficha de personagem (`personagens.md`)
```
## LIA
- quem é: 17 anos, nova na cidade, curiosa, fala rápido
- quer: descobrir quem mora na casa abandonada
- medo: ficar sozinha
- mania: tira foto de tudo com o celular
- skin: skins/lia.png · voz: (eu gravo: aguda e rápida) ou (TTS: voz + estilo do guia 13)
```
Toda cena precisa de alguém querendo algo e alguém (ou algo) no caminho.

## 2. Roteiro do episódio
Mesmo formato do guia 09/10 (`F001 [personagem: NOME · tom · velocidade] fala` + pausa), com:
- **Narrador opcional** (`[narrador · ...]`) para abrir, passar o tempo ("Três dias depois...") e fechar.
- Falas curtas (até ~15 palavras). Conversa é ping-pong.
- Marcar **[reação: NOME]** quando alguém precisa ser mostrado ouvindo (o Claude põe o close).
- Fim de episódio: frase de suspense + `[CONTINUA]`.

## 3. Cenário com itens da vida real
Duas pilhas. Escolha 1 no começo da série e não troque.

| | Pilha A (padrão) | Pilha B (mais itens) |
|---|---|---|
| Versão | a mesma do MCP (Fabric 1.21.11 / 26.x) | Fabric 1.21.1 |
| MCP | `chapmanjw` direto no jogo | MCP por **RCON** num servidor Fabric 1.21.1 local (o `chapmanjw` não roda na 1.21.1) |
| Móveis | Macaw's Furniture (acompanha as versões novas) | Handcrafted, Another Furniture, MrCrayfish's Refurbished (TV e computador que funcionam) |
| Celular, TV, notebook, carro | **objetos próprios** (abaixo) | mods: Modern Phone, PIPphone (+CarLib), PixelReel (TV), MC-Device (notebook, telefone), New Misc Items |
| Personagens e gestos | Easy NPC + Emotecraft x Easy NPC (guia 09) | Easy NPC + Emotecraft + Serious Player Animations |
| Rostos vivos | Fresh Animations + EMF + ETF | igual |

Versões vistas em 12/11/2026: confira cada uma no Modrinth/CurseForge antes de instalar. Mod útil que só existe na versão antiga: ver "portar mods" (guia 11 §5b).

### Objetos próprios (funciona em qualquer versão, sem mod)
Celular, TV, notebook, copo, mochila, carro parado: o Claude faz o modelo em Blockbench (é um arquivo JSON de caixinhas) dentro de um **pacote de textura** do canal e mostra no mundo com `item_display` (objeto parado) ou na mão do personagem (`item replace ... weapon.mainhand`). Tela de celular/TV com imagem trocada por textura = dá para "mostrar a mensagem" na tela.

### O Claude monta o cenário
1. Lê `cenas.md` (lugar, hora, clima, móveis, objetos, elenco).
2. Constrói por comando: paredes e chão (`/fill`), móveis (`/setblock` com os blocos do mod), objetos (`/summon item_display`), luz (lâmpadas, luz do dia por `/time`).
3. Guarda cada cenário pronto como estrutura (`/place template` / Structure Block) para os próximos episódios: **cenário fixo da série** (casa, escola, praça).
4. Manda print de cada ângulo para você aprovar antes de gravar.

## 4. Câmera de novela (cobertura automática)
Como a cena é feita por comandos (datapack), ela **se repete igual** quantas vezes precisar. O Claude grava a mesma cena 3 ou mais vezes, cada uma de um ângulo:
1. **Master:** plano geral com todos (sempre gravado).
2. **Close de cada personagem** que fala (sobre o ombro do outro).
3. **Extras:** plano detalhe (o celular, a carta), contra-plongée no vilão, plano aberto de estabelecimento da casa/cidade.

Depois corta automaticamente pelas regras:
| Momento | Plano |
|---|---|
| começo da cena | estabelecimento (fachada/cidade) 2–3 s → master |
| fala normal | close de quem fala (sobre o ombro do outro) |
| fala forte / revelação | close de quem ouve logo depois (reação) |
| frase dramática | close com aproximação lenta (dolly in) + música de tensão |
| ação (alguém entra, corre, cai) | master ou plano geral |
| 4+ falas seguidas no mesmo close | volta 1 vez para o master |
| objeto importante | plano detalhe |
| fim do episódio | close no rosto + corte seco para preto + "continua..." |

Regra dos 180° e campo/contracampo valem sempre (guia 10 §2).

## 5. Som de novela
- Trilha por clima: leve/cômica no dia a dia, tensão nos segredos, romântica, triste; **trilha de suspense curta** no gancho final.
- Efeitos: porta, passos, notificação de celular, campainha, carro, risada/"ahn?" cômico, vinil arranhando na quebra de piada.
- Ambiente sempre ligado (rua, chuva, casa à noite).
- Vozes: cada personagem com um jeito fixo (guia 13). Mix: voz em cima, música baixa, -14 LUFS.

## 6. Thumb e título
- Thumb: 2 personagens em close com expressão forte (susto, raiva, choro) + 1 objeto da história (celular com mensagem, carta) + 2–4 palavras.
- Título: situação + curiosidade. Ex.: "DESCOBRI O SEGREDO DO MEU VIZINHO NO MINECRAFT", "MEU PRIMEIRO DIA NA ESCOLA NOVA (EP. 1)".
- Playlist da série e "EP. N" no título.

## 7. Público
Novelinha de Minecraft costuma atrair crianças. No YouTube Studio, marque com cuidado se o vídeo é "conteúdo para crianças" (regra do YouTube; muda comentários e anúncios). Nada de violência pesada, palavrão ou tema adulto.
