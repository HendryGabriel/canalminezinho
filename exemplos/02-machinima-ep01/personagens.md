# Personagens (formatos 2 e 3) — série "Pastelaria da Vó"

Todos originais do canal: nomes, skins, bordões e história. Skins feitas à mão no Blockbench (modo Skin, 64×64), a partir de arte conceito (`biblioteca/README.md` §4).
Elenco no jogo: **Easy NPC** + **Emotecraft x Easy NPC** (guia 09). Plano B se o emote não tocar no NPC humanoide: **mannequin** (Java 1.21.9+) com a skin no `profile` + expressão "sem mod" (tabela do guia 09).
Nomes dos emotes abaixo = nomes genéricos do guia 09; na instalação o Claude troca pelos nomes reais do Emotecraft (só emotes genéricos: nada de dança de jogo/TikTok).
Vozes de TTS: sugestão para ouvir no AI Studio (ouvir 2–3 opções no EP. 1, anotar a escolhida aqui e **nunca mais trocar**).

## TOCO
- quem é (idade, papel): 12 anos, protagonista e **câmera do episódio** (1ª pessoa). Chegou na vila pequeno e calado; a Vó Cida "adotou" ele no balcão. Hoje é o que tem as ideias (quase sempre ruins, sempre corajosas).
- quer: salvar a pastelaria da Vó e provar que dá conta.
- medo: decepcionar a Vó; voltar a ficar sozinho no banco da praça.
- mania / bordão próprio: **"Dá ruim, mas dá certo!"** (antes de toda ideia arriscada; 1 a 3 vezes por episódio, e sempre no CTA). Fala com quem assiste ("e você vai contar junto").
- cor-assinatura: **laranja** (#F2811D).
- skin / modelo: `skins/toco.png` · moletom laranja com capuz e bolso canguru, bermuda jeans, tênis branco, cabelo castanho espetado, avental branco com mancha de óleo (fantasia do EP. 1: "pasteleiro"). Skin própria, feita em 12/11 no Blockbench. Na 1ª pessoa só aparece o braço laranja; nos planos de novela entra o **TOCO-dublê** (Easy NPC com a mesma skin).
- voz:
  - eu gravo: sua voz normal, um pouco mais aguda e rápida, sorrindo; frases curtas, energia de "vamos!". Na edição: +2 semitons.
  - TTS: voz `Puck` · estilo: `Brazilian Portuguese 12-year-old boy, energetic and optimistic, fast talker, smiling voice, brave but a little clumsy, short punchy sentences.`
- expressões principais (só nos planos de novela; na 1ª pessoa o "rosto" é a mão/HUD):
  - feliz / ideia → `emote: cheer` (ou `clap`) + partícula `happy_villager`
  - ideia arriscada ("Dá ruim...") → `emote: point` para a frente + pulinho
  - susto → `emote: shock` + recua 1 bloco
  - triste → `emote: sad` (cabeça baixa) · sentado no banco = pose sentado do Easy NPC
  - bravo → `emote: angry` + `angry_villager`
  - falando → `emote: talk`

## NINA
- quem é (idade, papel): 12 anos, melhor amiga do Toco, a "contadora" da turma. Responsável, irônica, mas com coração mole.
- quer: que a conta feche. Sempre.
- medo: errar uma conta (e, no fundo, errar com um amigo).
- mania / bordão próprio: **"Pela minha conta..."** antes de todo número. Anota tudo no **caderninho** (é a prova no clímax).
- cor-assinatura: **verde-água** (#2EC4B6).
- skin / modelo: `skins/nina.png` · jaqueta verde-água, camiseta branca, calça cinza, óculos redondos pretos, duas tranças pretas, lápis atrás da orelha. Item na mão: `book` com `item_model` "vila:caderno" (pacote de textura do canal). Skin própria, feita em 12/11.
- voz:
  - eu gravo: firme, rápida nas contas, seca nas ironias (cara séria, sem rir). Na edição: +3 semitons.
  - TTS: voz `Leda` · estilo: `Brazilian Portuguese 12-year-old girl, smart and precise, fast when counting numbers, dry deadpan sarcasm, warm underneath.`
- expressões principais:
  - conta / explica → `emote: think` (mão no queixo) e depois `emote: point` para o placar
  - ironia → `emote: shrug` (ou cabeça inclinada `Pose.Head`)
  - comemora número → `emote: clap` + `happy_villager`
  - susto → `emote: shock`
  - triste / culpa → `emote: sad`
  - mistério / pista → agachada (pose do Easy NPC) olhando o baú

## GUGA
- quem é (idade, papel): 11 anos, o amigo comilão e engraçado; parece bobo, mas é o mais leal (e o que salva o dia com o "pastel de emergência").
- quer: comer. E, de verdade, ser levado a sério.
- medo: ser acusado/ignorado pelos amigos; ficar sem pastel.
- mania / bordão próprio: sempre com **comida na mão**; transforma qualquer coisa em comida ("pastel de desculpas", "pastel de emergência"). Diz "Ops." antes de cada desastre.
- cor-assinatura: **amarelo-mostarda** (#E3B23C) — a cor da massa do pastel.
- skin / modelo: `skins/guga.png` · camiseta amarelo-mostarda com um pastel desenhado, boné vermelho virado para trás, bermuda marrom, bochechas rosadas, farelo (pixels bege) na roupa. Item na mão: pastel (`item_model` "vila:pastel"). Skin própria, feita em 12/11.
- voz:
  - eu gravo: grave e arrastada, meio "de boca cheia", ri no meio das falas; grita fino nos sustos. Na edição: +1 semitom.
  - TTS: voz `Fenrir` · estilo: `Brazilian Portuguese 11-year-old boy, goofy and relaxed, slightly slow and chewy, sudden high-pitched yelps when scared, very sincere when sad.`
- expressões principais:
  - comendo → `emote: eat` (se não existir: mão à boca em loop com `talk`) + som `entity.generic.eat`
  - susto → `emote: shock` + pulo + som `entity.player.hurt`
  - empolgado / poção de velocidade → `emote: cheer` + efeito `speed` e partícula `cloud` nos pés
  - triste (acusado) → `emote: sad`, anda devagar para o banco, senta
  - "Ops." → `emote: shrug` + cabeça baixa

## VÓ CIDA
- quem é (idade, papel): 78 anos, dona da pastelaria da praça. Dá fiado para todo mundo, por isso nunca juntou dinheiro. Sábia e com humor seco.
- quer: manter a pastelaria aberta, que para ela é "feita de gente".
- medo: a praça sem a pastelaria; os meninos brigarem.
- mania / bordão próprio: **"Nada de pressa"** (e depois "Sem pressa, mas sem moleza!"). Chama todo mundo de "meu filho / minha filha".
- cor-assinatura: **roxo-lilás** (#9B5DE5).
- skin / modelo: `skins/vo_cida.png` · vestido lilás, avental florido branco e rosa, xale roxo, coque branco, óculos de aro dourado. Item: bengala (`stick` com `item_model` "vila:bengala"). Fica sentada (pose sentada do Easy NPC) na cadeira de balanço (Macaw's Furniture) quase o episódio todo: "joelho de pedra". Skin própria, feita em 12/11.
- voz:
  - eu gravo: devagar, voz mais "para dentro", um pouco trêmula, carinhosa; nas piadas, seca. Na edição: −1 semitom + leve tremolo.
  - TTS: voz `Sulafat` · estilo: `Brazilian Portuguese grandmother in her late seventies, slow and warm, slightly shaky voice, gentle humor, dry and wise one-liners.`
- expressões principais:
  - ensinando → `emote: talk` + `emote: point` para a mesa
  - bronca carinhosa → `emote: angry` curto (1 s) + cabeça inclinada
  - triste → `emote: sad`, olha para o chão
  - história emocional → `emote: talk` bem lento; partícula `heart` no fim (F148)
  - comemora → `emote: clap` sentada

## LORENA
- quem é (idade, papel): 13 anos, a rica da vila, dona da Torre Dourada. Rival, esnobe e engraçada; no fundo também se sente sozinha (o ouro dela é "de uma vida inteira").
- quer: a praça inteira para o "Estacionamento Dourado" (de carrinhos de mina).
- medo: perder o ouro; admitir que gosta de alguma coisa simples (como pastel).
- mania / bordão próprio: **"Tchauzinho."** (e "Tchauzinho, pobrinhos."). Tem ciúme do bordão: "O tchauzinho é meu!". Tudo dela é de ouro.
- cor-assinatura: **dourado** (#FFC300).
- skin / modelo: `skins/lorena.png` · jaqueta dourada brilhante, saia branca, botas douradas, cabelo loiro liso com tiara/coroa de pixels, óculos escuros na cabeça. Item: `golden_pickaxe` (clímax). Skin própria, feita em 12/11.
- voz:
  - eu gravo: nasal e arrastada no "tchauzinho", fala de cima para baixo; no espanto, grita e perde a pose. Na edição: +2 semitons.
  - TTS: voz `Despina` · estilo: `Brazilian Portuguese 13-year-old rich girl, snobbish and dramatic, drawls on 'tchauzinho', loses her composure when shocked, softer when sad.`
- expressões principais:
  - esnobe / "tchauzinho" → `emote: wave` com um braço só, de costas para os outros
  - bravo → `emote: angry` + `angry_villager`
  - espanto (cofre vazio) → `emote: shock` + recua
  - triste → `emote: sad` (F171)
  - comendo o pastel → `emote: eat` + `heart` pequeno (ela gostou e não quer admitir)

## Figurantes (mobs genéricos do Minecraft, sem voz)
- **DUQUESA, a raposa ladra** — raposa vermelha (`fox`, `Type:"red"`), nome dado no fim pela Vó. Esmeralda na boca (`weapon.mainhand`). Sons do jogo: `entity.fox.ambient` = o "ié-ié", `entity.fox.sleep`, `entity.fox.eat`. Vira caixa da pastelaria no fim.
- **O CREEPER** — creeper sem nome, `NoAI` (só se mexe por `/tp`). Explode a placa (B1), compra pastel com pólvora (B3); a pólvora vira os fogos do final.
- **ZUMBI DE CAPACETE** — `zombie` com `iron_helmet`, paga com cenoura, gosta de pastel queimado.
- **ALDEÕES** — fila de 10 (profissões: ferreiro/weaponsmith, pescador/fisherman, bibliotecária/librarian, padeiro = farmer, bruxa = `witch`), 1 aldeãozinho (`Age:-24000`). Com **Fresh Animations** piscam e mexem a sobrancelha sozinhos. Sons `entity.villager.yes / no / trade`.
- **SEU MORDOMO** (sem nome na fala) — aldeão `nitwit` de terno (pacote de textura opcional) dormindo em pé na Torre (`NoAI`, partícula de "zzz" = `text_display` "z z z").
