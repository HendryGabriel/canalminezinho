# Personagens (formatos 2 e 3) — série "Bibo e Vovó Nena"

Todos originais do canal (nomes, visuais, história). Episódios **sem fala**: a personagem tem de ser entendida só pela silhueta, pela cor e pelo rosto.
Rig: **MCprep** (rig de jogador "Fancy Feet" com cotovelo e joelho + Skin Swap) ou **R-G Simple Minecraft Rig** (MIT) — os dois estão em `biblioteca/README.md` §3, com crédito. Partes extras (coque, óculos, avental) modeladas no **Blockbench** e presas no osso da cabeça/corpo. Skins próprias, 64×64, desenhadas à mão.
Mobs (gato, vaca, galinha, zumbi): **MCprep Mob Spawner** com textura do jogo (mob genérico do Minecraft) + troca de olhos por textura.

## Rosto por troca de textura (vale para todos os humanos)
Como funciona no Blender: o rig usa a skin inteira como textura. Cada expressão é **uma cópia da skin com só os pixels do rosto (8×8 da frente da cabeça, camada de dentro) trocados**. As cópias viram uma sequência de imagens (`rostos/bibo/bibo_0001.png` … `_0015.png`). No material, o nó **Image Texture** fica em modo *Image Sequence* (Frames = 1) e o **Offset** é ligado por driver a uma propriedade `rosto` (número inteiro) no osso da cabeça: `offset = rosto - 1`. Animar o rosto = pôr keyframes **constantes** em `rosto`. Piscar: o script põe `rosto = 10` por 3 quadros a cada 3–5 s (aleatório) quando o rosto está em 1 ou 2.
Os óculos da Vovó e a franja do Bibo ficam na camada de fora (overlay) e **não mudam**.

| Nº | Expressão | Olhos (2 px de largura cada, linha 4 e 5 do rosto) | Boca (linhas 6–7) | Extra |
|---|---|---|---|---|
| 1 | neutro | quadrado 2×2 escuro com 1 px branco de brilho no canto | 2 px escuros retos | — |
| 2 | feliz | arco "^ ^" (3 px em V invertido) | sorriso: 4 px curvados para cima | bochecha rosa 1 px |
| 3 | rindo | "> <" fechados | boca aberta 4×2 vermelho-escuro com 2 px de língua rosa | bochecha rosa 2 px |
| 4 | triste | 2×2 caídos para fora, sobrancelha "/ \" 2 px | curva para baixo 4 px | — |
| 5 | chorando | fechados "– –" | aberta 4×2 tremida | **lágrimas**: 2 colunas azul-claro (#7FD3FF) do olho até o queixo |
| 6 | surpreso | 2×3 grandes, brilho branco 2 px | "O" 2×2 escuro | sobrancelha alta 1 px acima |
| 7 | bravo | 2×2 com sobrancelha "\ /" grossa preta por cima | reta 4 px com 1 px de dente branco | **veia** vermelha "#" 3×3 no canto da testa + bochecha vermelha |
| 8 | amor | **corações** rosa (#FF4F8B) 3×3 | sorriso 4 px | bochecha rosa 2 px |
| 9 | esforço | "> <" | dentes cerrados 4×1 branco com borda | gota de suor azul 1×2 na testa |
| 10 | piscando | linha 2×1 | igual à expressão de antes (usar 1 ou 2) | — |
| 11 | assobio | 2×2 meio fechados (1 px) | bico "o" 1×1 escuro no meio | bochechas cheias rosa 2 px |
| 12 | medo | 1×1 pequenos (pupila encolhida) com branco em volta | zigue-zague 4 px | gota de suor + rosto 1 tom mais pálido |
| 13 | decidido | 2×2 com sobrancelha reta baixa | linha firme 3 px, canto levantado | — |
| 14 | nojo | um olho fechado "–", outro 2×2 | língua para fora 2×1 rosa | tom esverdeado nas bochechas |
| 15 | segurando o riso | "^ ^" apertados | lábios fechados 2 px tremidos | bochechas cheias **vermelhas** 2×2 |

Ícones que saem da cabeça (não fazem parte da textura; vêm de `ferramentas/blender/efeitos.py` → `icone()` / `coracoes()`): corações, "!?", "!", "?", estrelinhas de tontura, veia de raiva grande, gota de suor grande, notas musicais.

## BIBO
- quem é (idade, papel): 7 anos, neto da Vovó Nena, protagonista. Curioso, cientista de brincadeira, um pouco medroso do escuro. Ainda não sabe assobiar.
- quer: desfazer o que fez (devolver o tamanho da Vovó) e, no fundo, ser corajoso como ela.
- medo: escuro e barulho de monstro à noite.
- mania / bordão próprio: (sem fala) **língua de fora quando se concentra**; **óculos de proteção** na testa (desce para os olhos quando vai "fazer ciência"). Tenta assobiar e só sai cuspe — até o fim.
- cor-assinatura: **azul-turquesa** (#1FB5C7).
- skin / modelo: `skins/bibo.png` (própria, 12/11) · rig MCprep jogador com proporção de criança: corpo 0,8× e **cabeça 1,15×** (o "fofo" do estilo kids). Macacão jeans azul-turquesa sobre camiseta amarela-clara, tênis vermelhos, cabelo castanho-escuro com franja de 1 px na camada de fora, bochechas sempre um pouco rosadas. Extra no Blockbench: óculos de proteção (aro laranja, lente azul transparente) presos no osso da cabeça, com 2 poses (testa / olhos).
  - Versão **bebê** (só na memória, F038): mesmo rig, escala 0,5, cabeça 1,3×, macacãozinho branco, chupeta não.
- voz: (eu gravo) grunhidos de criança: "hã?", "uau", "ahá", "uéé" (choro), risada aguda curta; gravar normal e subir **+3 semitons** na edição. Assobio de verdade (F041): gravar o assobio forte das 4 notas. (TTS: não usar; grunhido de TTS soa falso.)
- expressões principais: feliz `2` · rindo `3` · triste `4` · chorando `5` (F035) · surpreso `6` (F008) · medo `12` (F033–F034) · decidido `13` (F039) · esforço `9` (F020) · assobio `11` (F015, F041) · segurando o riso `15` (F021) · amor `8` (F046).

## VOVÓ NENA
- quem é (idade, papel): 72 anos, avó do Bibo, dona da fazendinha. Brava por 3 segundos e depois ri de tudo. Sabe chamar qualquer bicho com o assobio de 4 notas.
- quer: (pequenininha) voltar ao tamanho normal sem perder a pose — e cuidar do Bibo mesmo do tamanho de uma caneca.
- medo: o Bibo triste.
- mania / bordão próprio: **o assobio sol-mi-sol-dó**; **bolso mágico do avental** (sempre sai um petisco: trigo para a vaca em F002, peixinho para o gato em F027). Dedo em riste quando dá bronca.
- cor-assinatura: **lilás** (#B07CE8).
- skin / modelo: `skins/vovo_nena.png` (própria, 12/11) · rig MCprep jogador com **braços finos** (modelo "slim"), postura um pouco curvada (osso do peito −8°). Cardigã lilás, vestido rosa-claro com bolinhas brancas, avental creme com bolso grande na frente, sapatilha marrom. Extras no Blockbench: **coque branco** (cubo 4×3×4 no topo de trás da cabeça) e **óculos redondos dourados** (aro de 1 px na camada de fora).
  - **Pequenininha:** o mesmo rig com **escala 0,25** (≈ 45 cm: cabe num vaso de flor e monta no gato). O cardigã fica para trás (objeto separado, escala 1, na cadeira).
  - **Grande na memória (F038):** igual, com luz quente e sem o avental (camisola lilás).
- voz: (eu gravo) risadinha "hi-hi-hi" de vó, "hmpf!", "ôô?", "ai-ai-ai"; voz normal **−1 semitom**. Pequenininha: **a mesma gravação +7 semitons** (fica de passarinho; é parte da piada). Quando volta ao tamanho (F045), a voz volta ao normal no meio do "ahá!". Assobio: forte (F001, F050), fininho (F014, F037 = +7 semitons), normal (F038).
- expressões principais: feliz `2` · rindo `3` (F010, F017) · bravo `7` (F009) · surpreso `6` (F007, F022) · nojo `14` (F015) · esforço `9` (F021, cuspindo a pena) · triste `4` (F035) · amor `8` (F041 orgulho, F046) · assobio `11`.

## PAÇOCA
- quem é (idade, papel): o gato da casa, gordinho e curioso. Começa vendo a Vovó como brinquedo, vira o "cavalo" dela.
- quer: caçar a coisa pequena que corre (depois: peixinho e carinho).
- medo: balde (depois da F025, sempre que vê um balde, recua).
- mania / bordão próprio: rabo balançando antes de pular; ronrona alto quando ganha petisco.
- cor-assinatura: **laranja-caramelo** (#E8892B) com **coleira azul-turquesa** (igual ao Bibo: é o gato dele).
- skin / modelo: MCprep Mob Spawner → gato com a textura do gato **ruivo** do jogo (variante "red"), coleira pintada em turquesa com 1 px de sininho dourado. Olhos por troca de textura (mesmo truque dos humanos, só os pixels dos olhos):
  `1` normal · `2` caçador (pupila enorme preta, quase o olho todo) · `3` ronronando (olhos fechados "^ ^") · `4` amor (corações) · `5` tonto (espiral 3×3) · `6` assustado (pupila 1 px).
  **Pequenininho** (piada final): escala 0,25.
- voz: miados e ronronar (gravar ou Freesound CC0 `cat meow`, `cat purr`); miado fininho = +7 semitons.
- expressões principais: caçador `2` (F011, F022) · tonto `5` + estrelinhas (F026) · ronronando `3` + corações (F028) · assustado `6` (F049).

## MIMOSA
- quem é (idade, papel): a vaca da fazenda. Atende ao assobio da Vovó; foge com medo do gato.
- quer: trigo e paz.
- medo: gato (a piada: uma vaca enorme com medo de um gato).
- mania / bordão próprio: **flor vermelha (papoula) presa na orelha**; sino de pescoço.
- cor-assinatura: **vermelho-papoula** (#E63946) na flor.
- skin / modelo: MCprep Mob Spawner → vaca do jogo (variante comum) + `poppy` (item do MCprep) presa no osso da cabeça + sino (`bell` do MCprep, escala 0,3) no pescoço. Olhos: `1` normal · `2` feliz (^ ^) · `3` assustada (olhos grandes com branco) · `4` amor.
- voz: "muu" do jogo (sons do Minecraft) — feliz (pitch +2), assustado ("MUU?!" curto).
- expressões principais: feliz `2` + corações (F002, F042) · assustada `3` + "!?" (F031) · amor `4` (F046, lambendo).

## Figurantes (mobs genéricos)
- **GALINHA** — MCprep chicken branca. Choca a Vovó (F019) e, no fim, persegue o Paçoca pequenininho (F049). Olhar "ofendido" = cabeça inclinada 20° + olho meio fechado (troca de textura `2`).
- **ZUMBI** — MCprep zombie, só a silhueta na floresta (F033) e o plano dele fugindo do gato (F042). Nunca assusta de verdade: é piada.
