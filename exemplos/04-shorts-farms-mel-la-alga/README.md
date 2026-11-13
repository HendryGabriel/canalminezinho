# Exemplo 04 — 3 shorts de farm com história (mel, lã, alga)

Feitos em 12–13/11/2026 seguindo `guia/15-shorts-farm-com-historia.md` com os scripts de `ferramentas/shorts-farm/`.
~60–66 s cada, 1080×1920 60 fps, voz TTS "Davi Andrei" (DarkPlanner), fonte Monocraft, trilhas Mixkit. Não publicados.
Os vídeos e as gravações brutas ficam só no PC (o repositório não guarda mídia).

Ideia de origem: as farms do vídeo "I Automated my Minecraft World in 24 Hours" (vybz), achado na caçada de outliers; molde de roteiro do short da Nixie "Existe um número que organiza o seu baú". A 1ª versão (tutorial puro) teve a edição aprovada e o roteiro rejeitado; esta é a versão com história.

## Roteiros (texto exato da narração)

### Mel — "Os golens pararam" (66 s)
Ele tinha seis golens de cobre organizando os baús da base. Era só jogar tudo no baú de cobre, e eles separavam: pedra com pedra, ferro com ferro. Um dia, ele voltou da mina e o depósito era um caos. Itens misturados, baús lotados, e os golens… parados. Tinham virado estátua. Golem de cobre oxida com o tempo, e quando fica todo verde, congela. Ele raspou cada um com o machado até voltar a cor de cobre, e eles voltaram a andar. Mas ele sabia: em alguns dias, iam congelar de novo. A única coisa que segura o cobre é cera, e cera vem de favo. Então ele achou uma colmeia, pegou a tesoura… e o enxame inteiro foi pra cima dele. Se ele não podia chegar perto, alguma coisa ia colher por ele. Colmeia cheia tem cinco níveis de mel, e um comparador lê esse número. Ele esticou o fio por cinco blocos: com quatro, o sinal morre no caminho. Com cinco, chega num ejetor com tesoura. Mas passaram dias, e a colmeia não enchia. Não tinha uma flor por perto. Ele plantou um jardim, e as abelhas começaram a voltar cheias de pólen. Na primeira colheita, três favos caíram no chão… e sumiram. Então um funil embaixo passou a mandar tudo pra um baú de cobre. Ele encerou os seis golens. E agora são eles que carregam, todo dia, a cera que impede eles de parar.

### Lã — "A obra de mil blocos" (61 s)
Ele queria a própria cara gigante na parede da base. Mil blocos de lã, dezesseis cores. Ele tosou todas as ovelhas da região e voltou com quarenta lãs. Faltavam novecentas e sessenta. Ovelha só dá lã de novo depois de comer grama. E a grama que ela come vira terra. Então ele prendeu uma ovelha em cima de um bloco de grama, cercada de vidro. Um observador vigia esse bloco: quando ela come, ele liga um ejetor com tesoura. Mas a lã caía em cima da grama e ficava presa lá dentro. Funil não puxa através de bloco… mas carrinho com funil puxa. Ele colocou um embaixo da grama, e a lã começou a descer pro baú. Mas na manhã seguinte, nada. A grama tinha virado terra, e terra não alimenta ovelha. Então ele cercou com grama: ela se espalha sozinha e cobre a terra de novo. Uma ovelha tingida dá lã colorida pra sempre, então ele fez uma de cada cor. Faltou o marrom: corante marrom só sai de cacau, e cacau só nasce na selva. Ele atravessou o mapa e voltou. Dezesseis ovelhas, dezesseis cores. Duas semanas depois, a obra estava pronta. E na primeira tempestade, um raio caiu bem nela. Lã pega fogo. Ele assistiu metade do rosto queimar… sorriu, e foi buscar mais lã.

### Alga — "A estufa de vidro" (63 s)
Ele estava construindo uma estufa de vidro. Dois mil blocos de areia pra derreter. Cada carvão derrete oito, então ele precisava de duzentos e cinquenta. Tinha doze. Passou três dias na mina e voltou com vinte. Até que lembrou: um bloco de alga seca derrete vinte. E alga cresce sozinha, embaixo d'água. Então ele montou um tubo de vidro com água e plantou uma muda. Um observador vigia a alga: quando ela cresce, um pistão corta tudo menos a base. Mas a alga cortada boiava e ficava presa no topo. Uma correnteza leva ela até um funil. Mas alga crua não queima. Então um defumador seca cada uma em cinco segundos. E pra virar combustível, um crafter junta nove num bloco. Ele foi dormir feliz. E acordou com o funil entupido e nenhum bloco. O crafter disparava antes de juntar nove, e travava. Então ele usou um comparador: ele conta os espaços cheios do crafter, e o sinal perde um a cada bloco de fio. Com nove blocos de fio, oito itens não chegam. Nove chegam, e sai um bloco. Cada bloco seca vinte algas, que viram dois blocos. A máquina se paga sozinha, e ainda sobra. Uma semana depois, a estufa estava pronta. E o carvão da mina? Virou tocha.

## Tomadas
**História** (`hist.py` / `hist2.py`, pasta `brutos/hist/`):

| Vídeo | Tomada | O que acontece |
|---|---|---|
| Mel | `m_s1` depósito | 6 golens de cobre separando itens; Steve joga itens no baú de cobre |
| Mel | `m_s2` caos | golens viraram estátua, itens no chão; Steve entra |
| Mel | `m_s3` oxida | close: golem passa de cobre → exposto → desgastado → oxidado → estátua |
| Mel | `m_s4` raspa | Steve raspa a estátua com machado até o golem voltar a andar |
| Mel | `m_s5` golens | golens trabalhando (plano geral) |
| Mel | `m_s7` abelhas | Steve tesoura o ninho, enxame ataca, ele foge |
| Mel | `m_funil26` | funil embaixo da colmeia + baú de cobre pega os favos |
| Mel | `m_s9` cera | Steve encera um golem (partícula `wax_on`) |
| Mel | `m_s10` final | órbita do depósito com golens carregando favos |
| Lã | `l_s1` parede | Steve com lã na frente da parede vazia, câmera sobe |
| Lã | `l_s2` tosa | tosa 3 ovelhas na mão |
| Lã | `l_s3` sem marrom | o rosto aparece linha por linha com buracos no marrom |
| Lã | `l_s4` cacau | árvore da selva, Steve colhe cacau |
| Lã | `l_s5` completa | os buracos marrons se completam |
| Lã | `l_s6` raio / `l_s7` fogo / `l_s8` sai | tempestade, raio na parede, fogo real (acelerado), Steve vai embora |
| Alga | `a_s1` estufa | estufa de vidro pela metade + monte de areia |
| Alga | `a_s2` fornalha | fornalha acesa, Steve com carvão |
| Alga | `a_s3` mina | Steve andando num túnel de mina |
| Alga | `a_s4` lagoa | lagoa com alga |
| Alga | `a_s5` noite | noite → manhã sobre a farm |
| Alga | `a_s7` / `a_s8` | estufa pronta; tochas acendendo em volta ao entardecer |

**Técnicas** (`shoot_*.py`, pastas `brutos/mel`, `brutos/la`, `brutos/alga`): montagem peça por peça e funcionamento real (comparador 0–5, ejetor colhendo, carrinho-funil puxando lã, grama se espalhando, pistão cortando alga, defumador, crafter com comparador).

## Planos de montagem
`planos/mel.json`, `planos/la.json`, `planos/alga.json` — formato explicado no guia 15 §5. `lote_tts.txt` = os 3 textos num lote só de TTS.

## Créditos de trilha (Mixkit, licença gratuita)
Mel: "Owies Ukulele" (Michael Ramir C., id 1072) · Lã: "Keep Smiling" (Ahjay Stelino, id 15) · Alga: "Little Bells" (Diego Nava, id 506).
