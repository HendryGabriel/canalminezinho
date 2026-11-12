# Cenas — A VOVÓ FICOU PEQUENININHA!?
Mundo de gravação: fazenda_nena (Minecraft, montado pelo MCP) → Mineways 14.02 → `fazenda_nena.blend` · Versão: Blender 5.2 + MCprep 3.6.3 · Look (formato 3): kids

## 0. Montagem fixa (fazer 1 vez; vira o cenário fixo da série)
### Cenário no Minecraft (MCP, mundo plano, `/time set 1000`, `/weather clear`)
| Lugar | Coordenadas | Blocos |
|---|---|---|
| Casa da Vovó | 0 64 0 → 12 70 10, porta em 6 64 0 (frente para −Z) | paredes `birch_planks` + `stripped_oak_log`, telhado `brick_stairs`, janelas `glass_pane` com `flower_box` (vaso) |
| Cozinha | dentro, 1 64 1 → 6 67 6 | `brewing_stand` na mesa em 2 65 3 (mesa = `oak_planks` + `oak_slab`), `cauldron` = pia, prateleira com `potion` e `book`, cadeira em 4 64 3 (`oak_stairs`) |
| Varanda | 1 64 −1 → 11 64 −3 | `oak_planks`, cerquinha `oak_fence`, cadeira de balanço (Blockbench) em 3 64 −2 |
| Galinheiro | 16 64 −10 → 20 66 −6 | cerca `spruce_fence`, 3 `hay_block` = ninhos, telhadinho `spruce_slab` |
| Jardim | 0 64 −14 → 14 64 −5 | `sunflower`, `peony`, `rose_bush`, `lilac` (2 blocos de altura = "árvores" para a Vovó pequena), 6 `flower_pot` com `poppy`/`dandelion`, poste `oak_fence` em 9 64 −12 |
| Pasto | −22 64 −32 → −4 64 −16 | grama, cerca `oak_fence` (o trecho −12 64 −32 → −8 64 −32 exporta **separado**: é o que quebra), cocho com `hay_block` |
| Beira da floresta | z < −33 | `dark_oak` grande (`/place feature minecraft:dark_oak` ×12), tronco caído `oak_log[axis=x]` em −13 64 −31 → −10 64 −31 |
| Quarto da memória | 40 64 0 → 46 68 6 (separado, longe) | `light_blue_wool` no chão, berço = `spruce_fence` + `white_wool`, janela grande, `lantern` na mesinha |

### Mineways → Blender
1. Mineways: `fazenda_nena` → área −25 60 −45 até 25 75 12 → Export for Rendering → **OBJ**, "export separate objects" ligado → `fazenda_dia.obj`. Área 38 62 −2 até 48 70 8 → `quarto_memoria.obj`.
2. Blender: MCprep → World Imports → Prep Materials (pixel nítido, **Closest**). Separar como objetos soltos: o trecho da cerca que quebra, os 6 vasos, o `brewing_stand`, a chaleira.
3. Props do Blockbench (glTF): frasco de poção grande (vidro + líquido rosa com emissão 0,5), livro aberto (página `livro_pagina.png`: desenho de vaca + balde + seta + vovó grande, sem texto), bandeja com bolo, balde e balde de leite, ovo, pena, peixinho, trigo, lanterna, chaleira cromada, berço.
4. Personagens: ver `personagens.md` (rigs MCprep + rosto por sequência de imagens).

### Looks (todos partem de `looks.aplicar_look("kids")`: Eevee, AgX Punchy, saturação 1,2, sol 4,5, f/4, motion blur 0,5, 30 fps)
| Nome | Trocas | Cenas |
|---|---|---|
| kids-dia | padrão | C001–C009, C015 (parte) |
| kids-tarde | `sol=3.0, sol_cor=(1.0,0.62,0.35), sol_altura=10, ceu=(1.0,0.55,0.35)` | C010 |
| kids-noite | `sol=0.4, sol_cor=(0.5,0.6,1.0), sol_altura=25, ceu=(0.05,0.07,0.18), ceu_forca=0.5` + luz pontual quente na lanterna/janela | C011–C012, C014–C016, C017 |
| kids-memória | kids-noite + `vinheta_branca=0.8, sat=0.85, glare=0.6, fstop=2.8` + luz quente forte na lanterna | C013 |
Câmera padrão: **24 mm**, perto do rosto, um pouco de baixo (estilo kids do estudo); 18 mm nos planos gerais exagerados; 35–50 mm só em closes de emoção. Plano médio de 2,4–2,9 s.
**Escala:** 1 bloco = 1 m. Vovó grande ≈ 1,8 m; Vovó pequenininha = escala 0,25 (≈ 0,45 m). Nos planos dela a câmera desce para **0,3 m do chão** (câmera baixa: o mundo vira gigante).

### Efeitos usados (`ferramentas/blender/efeitos.py`)
- prontos: `icone("!?")`, `icone("!")`, `icone("?")`, `icone("coracao")`, `coracoes()`, `tremida_camera()`, `flash()`; look com `vinheta_branca` e `aberracao`.
- **novos (adicionar em `efeitos.py`, 1 função cada, ~20 linhas):** `fumaca_puf(pos, ini, cor)` (esfera de fumaça rosa: 30 cubinhos com emissão fraca, crescem e somem em 12 quadros), `espiral_pocao(pos, ini, fim, cor)` (partículas com campo de força *Vortex*, igual à partícula de poção do jogo), `notas(pos, ini, fim, tamanho)` (notas musicais de pixel subindo: sai do assobio), `estrelinhas(pos, ini, fim)` (3 estrelas girando em volta da cabeça), `lagrimas(rig, ini, fim)` (2 jatos de cubinhos azuis saindo dos olhos), `splash(pos, ini, cor)` (coroa de gotas brancas + respingos).

### Som e música (`biblioteca/README.md`)
Mix: grunhidos 100% · efeitos 70% · música 40–60% (sem fala, a música conta a história; **sobe nos momentos quietos e tristes, desce na correria**, como no estudo do Kamui). Volume final −14 LUFS.
Motivo de 4 notas (sol-mi-sol-dó): assobio gravado por você + versão **caixinha de música** sintetizada pelo Claude (Python, notas puras com decaimento) → original, sem licença para conferir.

---

### C001 — F001–F002
tipo: blender
mundo: fazenda_dia.obj
local: varanda e pasto ao fundo · manhã (kids-dia) · céu limpo · quadros f1–165
cenário:
  - varanda, cadeira de balanço, pasto e Mimosa ao fundo
elenco:
  - VOVÓ NENA: rig, escala 1, em pé na beira da varanda (3, −3, 0), olhando para o pasto
  - MIMOSA: rig vaca, no pasto (−12, −24, 0) → anda até a varanda
ações (quadro):
  f1–20  VOVÓ põe 2 dedos na boca (braço direito sobe)
  f20–90  VOVÓ assobia (corpo inclina 5° para trás no "fiii") · `notas()` saindo da boca f22–90
  f60  MIMOSA levanta a cabeça (orelhas mexem), começa a trotar f70
  f91–140  MIMOSA trota até a varanda (trote: 4 passos por s, pulinho no fim)
  f140–165  VOVÓ tira trigo do bolso do avental e dá para ela; `coracoes()` na Mimosa f145–165
planos:
  f1–45  grande plano geral da fazenda, 18 mm, drone descendo devagar até a varanda
  f46–90  plano médio da Vovó assobiando, 28 mm, de lado
  f91–125  plano geral do pasto: a Mimosa trotando em direção à câmera, 24 mm, câmera baixa
  f126–165  plano médio Vovó + Mimosa (2 personagens), 24 mm
câmera:
  movimento: drone descendo (f1–45) · estática · estática baixa · dolly in curto
  de: (8, −20, 12) · olhando (3, −3, 1)   →   para: (6, −9, 3) · olhando (3, −3, 1.5)
  duração: f1–45
rostos:
  VOVÓ f1–19 = 2 · f20–90 = 11 · f91–165 = 2 (pisca f150)
  MIMOSA f1–90 = 1 · f91–165 = 2 · f145–165 = 4
efeitos (pós): nenhum
texto na tela: nenhum (episódio sem texto)
som: passarinhos, galo distante · assobio forte (voz) · trote · "muu" feliz · música: **ukulele alegre** (YouTube Audio Library, `happy ukulele`, sem atribuição) entra em f1

### C002 — F003–F005 (+ pausa 0,5 s)
tipo: blender
mundo: fazenda_dia.obj (cozinha)
local: cozinha · manhã, sol entrando pela janela · quadros f166–390
cenário:
  - mesa com `brewing_stand` (objeto separado), frasco grande no suporte, potinhos (açúcar, pétala, pó brilhante = glowstone dust do MCprep)
elenco:
  - BIBO: rig criança, de óculos de proteção nos olhos, em pé num banquinho na frente da mesa
  - VOVÓ NENA: entra pela porta da varanda com a bandeja de bolo
ações (quadro):
  f166–200  BIBO joga açúcar (pitada: braço sobe e desce) · `espiral_pocao()` branca curta
  f200–235  joga a pétala · líquido do frasco fica rosa (cor do material animada)
  f235–270  joga o pó brilhante · frasco borbulha (`espiral_pocao()` rosa f240–375)
  f271–330  VOVÓ entra (andar, 6 passos) e se inclina sobre o frasco (peito −25°)
  f331–360  frasco treme (Noise na rotação, força 3°) · tampa pula f345 (sobe 0,3 m e gira)
  f350–375  BIBO e VOVÓ olham o frasco e depois se olham (cabeças viram 0,3 s) · `icone("!?")` nos dois f352–390
  f376–390  pausa: tudo parado (hold) · só o frasco brilhando mais (emissão 0,5 → 3)
planos:
  f166–235  close das mãos do Bibo e do frasco (plano detalhe), 35 mm, f/2.8
  f236–270  primeiro plano do Bibo, língua de fora, 24 mm, de baixo
  f271–330  plano médio: a Vovó entrando ao fundo, o Bibo de costas na frente (profundidade)
  f331–360  plano detalhe do frasco tremendo, 50 mm
  f361–390  plano médio dos dois com o frasco no meio (2 shot), dolly in lento
câmera:
  movimento: estática nos detalhes · dolly in no fim
  de: (2, 1.2, 1.4) · olhando (2, 3, 1.1)   →   para: (2, 1.8, 1.35) · olhando (2, 3, 1.1)
  duração: f361–390
rostos:
  BIBO f166–330 = 9 (concentrado, língua de fora: variante do 9 com língua) · f331–360 = 1 · f361–390 = 6
  VOVÓ f271–330 = 2 · f331–390 = 6
efeitos (pós): leve glare no frasco
texto na tela: nenhum
som: "plim" de cada ingrediente · borbulhas crescendo · tampa "pop" · "hã?" dos dois · música: ukulele continua e **para seco** em f376 (silêncio da pausa)

### C003 — F006–F008
tipo: blender
mundo: fazenda_dia.obj (cozinha)
local: cozinha · quadros f391–600
cenário:
  - cardigã lilás separado (objeto do Blockbench com a mesma textura), na cadeira em 4 64 3
elenco:
  - VOVÓ NENA: troca de escala em f400 (1 → 0,25 em 4 quadros, escondido pela fumaça) e aparece sentada debaixo do cardigã
  - BIBO
ações (quadro):
  f391  `flash()` 2 quadros + `fumaca_puf()` rosa grande na Vovó (f391–430)
  f392–400  BIBO cai do banquinho para trás (sentado no chão)
  f436–480  fumaça abre devagar: só o cardigã na cadeira
  f480–525  o cardigã mexe (2 "ondas" no tecido via shape key) e a Vovó pequenininha sai por baixo, tossindo
  f526–565  close do Bibo
  f566–600  close da Vovó pequenininha olhando as mãos (vira as palmas 2 vezes)
planos:
  f391–435  plano médio da cozinha, 24 mm: o PUF (câmera tremendo)
  f436–525  plano médio da cadeira com o cardigã, 28 mm, dolly in muito lento
  f526–565  primeiro plano do Bibo, 24 mm, câmera baixa
  f566–600  primeiro plano da Vovó pequenininha, **câmera a 0,3 m da mesa/cadeira**, 24 mm (ela parece normal; o cardigã gigante atrás mostra a escala)
câmera:
  movimento: tremida (f391–410) · dolly in
  de: (4, 1.3, 1.0) · olhando (4, 3, 0.6)   →   para: (4, 1.7, 0.9) · olhando (4, 3, 0.6)
  duração: f436–525
rostos:
  BIBO f391–525 = 6 · f526–565 = 6 (pisca 2 vezes rápido f545–556)
  VOVÓ f480–525 = 9 · f526–565 = 6 · f566–600 = 6
efeitos (pós): **aberração cromática + blur radial** f391–399 (impacto) · `tremida_camera(forca=0.12)` f391–410
texto na tela: nenhum
som: PUF fofo + "plim" · tosse fininha · "UÉ?!" do Bibo em f526 · "piu?" da Vovó em f580 · música: 1 nota de xilofone descendo (Pixabay, `cartoon fall`) em f480

### C004 — F009–F011
tipo: blender
mundo: fazenda_dia.obj (cozinha)
local: mesa da cozinha · quadros f601–870
cenário:
  - chaleira cromada na mesa (material metálico; ligar **raytracing** do Eevee só neste plano para o reflexo)
elenco:
  - VOVÓ NENA (0,25) em cima da mesa · BIBO de joelhos ao lado da mesa (cabeça na altura dela) · PAÇOCA na janela (6, 0.2, 1.6)
ações (quadro):
  f601–705  VOVÓ pula 3 vezes (pulinhos de 0,1 m), dedo em riste balançando (braço direito, 6 balanços) · `icone("veia")` (veia de raiva grande) f610–700
  f706–740  BIBO junta as mãos (pose "desculpa"), cabeça inclinada
  f741–760  VOVÓ cruza os braços, vira o rosto
  f760–795  VOVÓ vê o reflexo na chaleira (ela pequena e esticada no metal) e cai na risada (corpo balança)
  f796–870  PAÇOCA na janela: pupilas crescem (rosto 1 → 2 em f810), rabo balança (rotação senoidal, 2 Hz)
planos:
  f601–660  primeiro plano da Vovó brava, câmera a 0,3 m, 24 mm, contra-plongée leve (ela "grande" na bronca)
  f661–705  plano médio por cima do ombro do Bibo: ela pequena dando bronca na mesa (piada da escala)
  f706–740  primeiro plano do Bibo, 28 mm
  f741–795  plano detalhe do reflexo na chaleira (50 mm) → ela rindo
  f796–835  plano médio da janela com o Paçoca, 35 mm
  f836–870  plano detalhe dos olhos do Paçoca (50 mm), dolly in rápido
câmera:
  movimento: dolly in rápido nos olhos do gato
  de: (6, −1.2, 1.7) · olhando (6, 0.2, 1.75)   →   para: (6, −0.4, 1.72) · olhando (6, 0.2, 1.75)
  duração: f836–870
rostos:
  VOVÓ f601–740 = 7 · f741–760 = 7 · f761–795 = 3
  BIBO f601–705 = 12 · f706–740 = 4
  PAÇOCA f796–809 = 1 · f810–870 = 2
efeitos (pós): nenhum
texto na tela: nenhum
som: "mm-mmm-mm!" fininho (+7 semitons) · "uuhh..." · "hi-hi-hi-hi!" fininho · "tchiiing" de caçador (Pixabay, `sparkle sting`) no olho do gato · música: **pizzicato cômico** (Kevin MacLeod, "Fluffing a Duck", CC BY 4.0) entra em f601

### C005 — F012–F013
tipo: blender
mundo: fazenda_dia.obj (cozinha → porta)
local: cozinha · quadros f871–1095
cenário:
  - livro de poções aberto na mesa (prop do Blockbench) com a página `livro_pagina.png`
elenco:
  - BIBO · VOVÓ NENA (0,25)
ações (quadro):
  f871–930  BIBO folheia o livro (3 páginas viram, 0,4 s cada)
  f931–970  para na página da vaca: o dedo aponta vaca → balde → seta → vovó grande
  f971–1005  BIBO levanta a cabeça: ideia (`icone("!")` f975–1005)
  f1006–1040  BIBO pega o balde na pia e a Vovó com a outra mão, põe no ombro (ela senta)
  f1041–1095  BIBO corre para a porta (corrida 6 passos/s), a Vovó segurando o cabelo dele
planos:
  f871–930  plano médio do Bibo com o livro, 24 mm
  f931–970  plano detalhe da página (50 mm, de cima), o dedo andando pelo desenho
  f971–1005  primeiro plano do Bibo, dolly in rápido
  f1006–1095  plano geral da cozinha: os dois saindo pela porta, 18 mm
câmera:
  movimento: dolly in rápido (ideia)
  de: (2.5, 1.0, 1.3) · olhando (2.5, 3, 1.2)   →   para: (2.5, 1.9, 1.25) · olhando (2.5, 3, 1.2)
  duração: f971–1005
rostos:
  BIBO f871–970 = 1 · f971–1095 = 2
  VOVÓ f1006–1095 = 6 → 2 em f1060
efeitos (pós): nenhum
texto na tela: nenhum (o livro é só desenho)
som: páginas virando · "ahá!" em f975 · "hup-hup!" · passos de criança correndo · música continua

### C006 — F014–F017
tipo: blender
mundo: fazenda_dia.obj (varanda)
local: varanda, pasto ao fundo · quadros f1096–1530
cenário:
  - igual ao C001; uma galinha ciscando na varanda
elenco:
  - BIBO na beira da varanda · VOVÓ (0,25) no ombro dele · MIMOSA longe no pasto, pastando · GALINHA no chão perto do Bibo
ações (quadro):
  f1096–1150  VOVÓ põe 2 dedos na boca
  f1150–1215  VOVÓ assobia: `notas(tamanho=0.15)` minúsculas f1150–1215 · MIMOSA não levanta a cabeça
  f1216–1270  BIBO enche as bochechas, bico · f1271–1300 sai "pft": `icone()` gota de cuspe voa na Vovó
  f1300–1320  VOVÓ limpa o rosto com a manga
  f1321–1380  BIBO põe os dedos na boca, sopra: "prrrr" (corpo treme)
  f1381–1440  GALINHA vira a cabeça devagar para ele (ofendida)
  f1441–1500  VOVÓ ri, balança, escorrega do ombro (f1500–1530 cai para fora do quadro)
planos:
  f1096–1150  plano médio Bibo + Vovó no ombro, 28 mm
  f1151–1180  primeiro plano da Vovó assobiando, 35 mm
  f1181–1215  grande plano geral do pasto, 18 mm: a Mimosa pastando, nada acontece (as notinhas somem antes de chegar)
  f1216–1320  primeiro plano dos dois (2 shot apertado), 24 mm
  f1321–1380  primeiro plano do Bibo soprando
  f1381–1440  primeiro plano da galinha, 35 mm, câmera baixa (reação)
  f1441–1530  plano médio: a Vovó rindo e caindo do ombro
câmera:
  movimento: estática (o humor está no corte)
  de: (5, −5.5, 1.4) · olhando (5, −3, 1.3)   →   para: igual
  duração: —
rostos:
  VOVÓ f1096–1150 = 2 · f1151–1215 = 11 · f1271–1320 = 14 · f1441–1500 = 3 · f1501–1530 = 6
  BIBO f1216–1270 = 11 · f1271–1320 = 15 · f1321–1380 = 9 · f1381–1440 = 1 · f1441–1530 = 6
  GALINHA f1381–1440 = 2 (ofendida)
efeitos (pós): nenhum
texto na tela: nenhum
som: assobio fininho · "ffff... pft!" · "éca!" · "prrrrr" · cacarejo ofendido · "hi-hi-hi... ai!" · música baixa de propósito no assobio fininho (f1150–1215) e volta

### C007 — F018–F021
tipo: blender
mundo: fazenda_dia.obj (galinheiro)
local: galinheiro · quadros f1531–1935
cenário:
  - ninho de feno (`hay_block` cortado + palha solta do Blockbench); 1 ovo
elenco:
  - VOVÓ (0,25) · GALINHA · BIBO
ações (quadro):
  f1531–1560  VOVÓ cai no ninho (arco + squash de 2 quadros ao tocar)
  f1561–1605  VOVÓ senta, tonta (`estrelinhas()` f1565–1600)
  f1606–1660  GALINHA chega e senta em cima (fofa, olho fechado de satisfação); só o coque aparece
  f1661–1710  coque mexe; braços da Vovó saem pelos lados batendo
  f1711–1790  BIBO puxa a galinha (3 puxões; a galinha estica como borracha: escala Y 1 → 1,3)
  f1791–1800  PLOC: a galinha sai voando para trás, o ovo pula, a Vovó vem grudada no ovo
  f1801–1845  VOVÓ desgruda do ovo; pena espetada no coque (prop pena)
  f1846–1900  VOVÓ cospe uma pena (pena voa)
  f1901–1935  BIBO segura o riso, bochechas vermelhas
planos:
  f1531–1560  plano geral do galinheiro, 18 mm, a Vovó caindo do alto do quadro
  f1561–1605  primeiro plano dela tonta, câmera no chão (0,2 m)
  f1606–1710  plano médio da galinha sentada nela (só o coque!), 28 mm — **plano-chave da thumb B**
  f1711–1790  plano médio do Bibo puxando, 24 mm
  f1791–1845  câmera lenta 50% (renderizar a 60 quadros e esticar) no PLOC, 35 mm
  f1846–1900  primeiro plano da Vovó cuspindo a pena
  f1901–1935  primeiro plano do Bibo segurando o riso
câmera:
  movimento: estática + câmera lenta no PLOC
  de: (18, −11.5, 0.6) · olhando (18, −8, 0.4)   →   para: igual
  duração: f1606–1790
rostos:
  VOVÓ f1531–1605 = 6 · f1801–1845 = 7 · f1846–1900 = 9
  GALINHA f1606–1710 = 2 (satisfeita, olho fechado)
  BIBO f1711–1790 = 9 · f1791–1845 = 6 · f1901–1935 = 15
efeitos (pós): squash/stretch na galinha (escala) · penas voando (8 props de pena com física simples) no PLOC
texto na tela: nenhum
som: "fofs" · "mmmf! mmmf!" abafado · cacarejo contente · "nnnnhh... UH!" · PLOC (Pixabay `cartoon pop`) · "ptu!" · "mmf-hmf"

### C008 — F022–F026
tipo: blender
mundo: fazenda_dia.obj (jardim)
local: jardim de flores altas · quadros f1936–2505
cenário:
  - flores de 2 blocos (girassol, peônia, roseira, lilás) = "floresta" para a Vovó · 6 vasos (objetos separados) · poste de cerca em 9 64 −12
elenco:
  - VOVÓ (0,25) · PAÇOCA · BIBO · balde
ações (quadro):
  f1936–1980  sombra do Paçoca cobre a Vovó (luz: o gato entra entre o sol e ela)
  f1981–2025  VOVÓ olha para cima devagar · `icone("!?", cor vermelha)` f1990–2025 · PAÇOCA sorri (boca do gato: textura)
  f2026–2205  perseguição: caminho em S entre as flores (curva de caminho, Follow Path) · VOVÓ corre 8 passos/s, PAÇOCA salta em arcos de 0,4 m · BIBO entra correndo f2100
  f2206–2250  VOVÓ pula dentro do vaso (some) · f2251–2310 PAÇOCA enfia a cara no vaso (o vaso balança)
  f2311–2345  BIBO mergulha, escorrega (escorregão: corpo horizontal 0,5 s) · balde voa em arco
  f2346–2415  balde encaixa na cabeça do Paçoca (f2360) · PAÇOCA sai do vaso cego
  f2416–2480  PAÇOCA anda de lado, às cegas, bate no poste (f2470)
  f2481–2505  PAÇOCA tonto (`estrelinhas()`)
planos:
  f1936–1980  primeiro plano da Vovó, câmera no chão, a sombra chegando
  f1981–2025  contra-plongée do Paçoca (do ponto de vista dela), 18 mm: o gato GIGANTE
  f2026–2085  travelling baixo (0,25 m) acompanhando a Vovó entre as flores, 18 mm, motion blur
  f2086–2145  plano geral do jardim (de cima, 24 mm): os três em fila correndo
  f2146–2205  travelling baixo de novo, o gato entrando no quadro atrás dela
  f2206–2310  plano médio do vaso: a cara do gato entrando, o vaso balançando
  f2311–2415  plano geral: o Bibo escorregando e o balde voando (câmera lenta 50% do f2340 ao f2360)
  f2416–2505  plano médio do Paçoca de balde batendo no poste
câmera:
  movimento: travelling baixo (perseguição)
  de: (2, −8, 0.25) · olhando (4, −8, 0.2)   →   para: (10, −11, 0.25) · olhando (12, −11, 0.2)
  duração: f2026–2085 e f2146–2205 (dois trechos)
rostos:
  VOVÓ f1936–1980 = 1 · f1981–2205 = 6 (pisca não) · f2206–2310 = 12
  PAÇOCA f1936–2310 = 2 · f2481–2505 = 5
  BIBO f2100–2310 = 9 · f2311–2415 = 6
efeitos (pós): linhas de velocidade leves na perseguição · `tremida_camera()` 4 quadros no PLONC do balde e no BOING
texto na tela: nenhum
som: "iiih!" · "ai-ai-ai-ai!" · "nã-nã-nã!" · patinhas · "toc" no vaso · "uooo... uf!" · PLONC de balde · BOING + miado abafado · música: **perseguição cômica** (Kevin MacLeod, "Run Amok", CC BY 4.0 — conferir no incompetech) f2026–2505, mais alta (sem grunhido importante)

### C009 — F027–F029
tipo: blender
mundo: fazenda_dia.obj (jardim → caminho do pasto)
local: jardim · quadros f2506–3000
elenco:
  - VOVÓ (0,25) · PAÇOCA · BIBO com o balde
ações (quadro):
  f2506–2560  BIBO tira o balde da cabeça do Paçoca · VOVÓ sai do vaso
  f2561–2655  VOVÓ tira o peixinho do bolso do avental (o bolso "brilha" 4 quadros), estende · PAÇOCA cheira
  f2656–2720  PAÇOCA come (mastiga 3 vezes), deita de lado · `coracoes()` f2670–2790 · ronrona (corpo sobe/desce)
  f2721–2790  VOVÓ sobe nas costas dele
  f2791–2850  PAÇOCA levanta com ela; VOVÓ aponta para o pasto (braço esticado, pose de general)
  f2851–3000  "cavalaria": PAÇOCA corre com a Vovó, BIBO atrás; câmera lenta 60% f2880–2960
planos:
  f2506–2560  plano médio dos três
  f2561–2655  primeiro plano da Vovó com o peixinho (câmera baixa) → plano detalhe do bolso
  f2656–2720  primeiro plano do Paçoca ronronando, 35 mm
  f2721–2790  plano médio: ela subindo no gato
  f2791–2850  **contra-plongée** heroico: Vovó montada apontando, sol atrás (lens flare leve), 18 mm
  f2851–3000  travelling lateral baixo, os dois passando pelas flores; o Bibo correndo atrás
câmera:
  movimento: travelling lateral
  de: (4, −13, 0.5) · olhando (4, −10, 0.4)   →   para: (−4, −16, 0.5) · olhando (−4, −13, 0.4)
  duração: f2851–3000
rostos:
  VOVÓ f2561–2655 = 2 · f2721–2790 = 3 · f2791–3000 = 13
  PAÇOCA f2561–2655 = 1 · f2656–2790 = 3 · f2791–3000 = 2
  BIBO f2851–3000 = 3
efeitos (pós): glare do sol no contra-plongée · poeira nas patas
texto na tela: nenhum
som: "psss-psss-psss" · mastigada · ronronar · "iiiiiá!" fininho · "uhuuu!" · música: **marcha heroica de brincadeira** (Audio Library `heroic march` / `epic comedy`) f2791–3000

### C010 — F030–F032
tipo: blender
mundo: fazenda_dia.obj (pasto)
local: pasto · fim de tarde (kids-tarde) · quadros f3001–3360
cenário:
  - trecho da cerca que quebra (objeto separado, 4 blocos), cocho com feno
elenco:
  - MIMOSA pastando no meio do pasto · BIBO com o balde · PAÇOCA com a VOVÓ montada, atrás do Bibo
ações (quadro):
  f3001–3135  BIBO anda na ponta dos pés (passos lentos, braços abertos), dedo na boca "shhh" f3050
  f3136–3165  PAÇOCA mia (boca abre)
  f3166–3225  MIMOSA levanta a cabeça, vê o gato, pula para trás · `icone("!?")` f3170–3225
  f3226–3300  MIMOSA dispara (galope 6 passos/s) na direção da cerca
  f3300–3315  cerca quebra: 4 blocos voam (keyframes + rotação)
  f3316–3360  MIMOSA some entre as árvores escuras · BIBO estende o braço
planos:
  f3001–3070  grande plano geral do pasto ao pôr do sol, 18 mm, silhuetas
  f3071–3135  plano médio do Bibo na ponta dos pés, 24 mm
  f3136–3165  primeiro plano do Paçoca miando (35 mm)
  f3166–3225  primeiro plano da Mimosa assustada, 28 mm
  f3226–3315  plano geral: a Mimosa correndo e quebrando a cerca
  f3316–3360  plano por cima do ombro do Bibo: a floresta engolindo a vaca
câmera:
  movimento: estática + pan seguindo a vaca (f3226–3315)
  de: (−6, −20, 1.5) · olhando (−10, −28, 1)   →   para: (−6, −20, 1.5) · olhando (−10, −33, 1.2)
  duração: f3226–3315
rostos:
  BIBO f3001–3165 = 13 · f3166–3360 = 6
  MIMOSA f3001–3165 = 1 · f3166–3360 = 3
  PAÇOCA f3136–3165 = 1 · VOVÓ f3166–3360 = 6
efeitos (pós): `tremida_camera()` f3300–3310
texto na tela: nenhum
som: grilos começando · "shhh..." · miado · "MUU?!" · cascos · madeira quebrando · "nããão!" · música: corta a marcha em f3136; **tensão leve** (Audio Library `suspense kids`/`tension pizzicato`)

### C011 — F033–F035
tipo: blender
mundo: fazenda_dia.obj (beira da floresta)
local: beira da floresta escura · o sol se põe (kids-tarde → kids-noite em f3361–3540, animar a força e a cor do sol) · quadros f3361–3870
cenário:
  - tronco caído; folhas de carvalho-escuro; neblina **bem leve** só dentro da floresta (volume local, densidade 0,02, para o escuro ter profundidade)
elenco:
  - BIBO · VOVÓ (0,25) montada no PAÇOCA · ZUMBI: só silhueta escura entre as árvores (−12, −38, 0), sem rosto visível
ações (quadro):
  f3361–3450  BIBO corre até a beira e freia (derrapa)
  f3451–3540  a luz cai (sol some) · gemido de zumbi · BIBO congela, ombros sobem
  f3541–3600  BIBO dá um passo para trás, tremendo (Noise leve no corpo)
  f3600–3660  o balde escorrega da mão e cai (rola 1 m)
  f3661–3760  BIBO senta no tronco, abraça os joelhos
  f3761–3870  BIBO chora (`lagrimas()` f3770–3870) · VOVÓ desce do gato e olha para ele
planos:
  f3361–3450  plano geral por trás do Bibo: ele pequeno diante das árvores enormes, 18 mm (plongée leve)
  f3451–3540  primeiro plano do Bibo, a luz sumindo no rosto, 35 mm
  f3541–3600  ponto de vista do Bibo: a floresta escura, a silhueta do zumbi mexendo 1 vez
  f3601–3660  plano detalhe do balde caindo
  f3661–3760  plano médio do Bibo sentando no tronco, 28 mm
  f3761–3870  primeiro plano do Bibo chorando, depois a Vovó entrando no quadro embaixo
câmera:
  movimento: dolly in muito lento no choro
  de: (−11.5, −29.3, 0.9) · olhando (−11.5, −31, 0.85)   →   para: (−11.5, −29.8, 0.88) · olhando (−11.5, −31, 0.85)
  duração: f3761–3870
rostos:
  BIBO f3361–3450 = 13 · f3451–3660 = 12 · f3661–3760 = 4 · f3761–3870 = 5
  VOVÓ f3761–3870 = 4
efeitos (pós): saturação cai 20% de f3451 a f3870
texto na tela: nenhum
som: vento nas folhas · gemido de zumbi distante (sons do Minecraft) · "uh... uh-uh..." · "clang" · "uééé" + fungada · música: some em f3451 (só ambiente) e entra **piano triste** baixinho em f3761 (Scott Buckley, faixa calma de piano, CC BY 4.0)

### C012 — F036–F037
tipo: blender
mundo: fazenda_dia.obj (tronco)
local: tronco, noite (kids-noite), lua · quadros f3871–4125
elenco:
  - BIBO sentado · VOVÓ (0,25)
ações (quadro):
  f3871–3930  VOVÓ escala o joelho do Bibo (esforço, 2 tentativas)
  f3931–4020  VOVÓ dá 3 tapinhas na mão dele, olha para ele
  f4021–4125  VOVÓ assobia baixinho · `notas(tamanho=0.12)` lentas e brancas
planos:
  f3871–3930  plano médio de lado, 28 mm
  f3931–4020  plano detalhe: a mãozinha dela na mão dele (50 mm, f/2.8)
  f4021–4125  primeiro plano dela assobiando, com o rosto do Bibo desfocado ao fundo (rack focus do rosto dela para o dele em f4090)
câmera:
  movimento: rack focus (foco muda de distância)
  de: foco em 0,35 m (Vovó)   →   para: foco em 0,9 m (Bibo)
  duração: f4090–4125
rostos:
  VOVÓ f3871–3930 = 9 · f3931–4020 = 2 · f4021–4125 = 11
  BIBO f3871–4089 = 5 · f4090–4125 = 4
efeitos (pós): nenhum
texto na tela: nenhum
som: "shh-shh-shh" fininho · assobio fininho baixinho · piano para em f4021; a **caixinha de música** com as 4 notas começa por baixo do assobio e emenda na memória

### C013 — F038 (memória)
tipo: blender
mundo: quarto_memoria.obj
local: quarto do Bibo bebê, noite de trovão (kids-memória) · chuva na janela · quadros f4126–4485
cenário:
  - berço, janela grande com chuva (plano com textura de chuva animada), relâmpago = luz azul 3 quadros em f4160 e f4300
  - lanterna na mesinha (luz pontual quente, 40 W, liga em f4200)
elenco:
  - BIBO BEBÊ (escala 0,5, cabeça 1,3×) no berço · VOVÓ NENA grande (escala 1), de camisola lilás
ações (quadro):
  f4126–4200  BIBO BEBÊ chora em pé no berço, segurando a grade · relâmpago f4160
  f4200–4250  VOVÓ entra, acende a lanterna (o quarto fica dourado)
  f4250–4340  VOVÓ senta ao lado e assobia · `notas()` douradas · relâmpago f4300 (o bebê nem liga)
  f4341–4400  BIBO BEBÊ para de chorar, ri, bate palminhas
  f4401–4450  BIBO BEBÊ faz bico e tenta assobiar: sai cuspe (gotinha)
  f4451–4485  os dois riem; fade branco para voltar
planos:
  f4126–4200  plano médio do berço, 24 mm, luz azul da janela
  f4201–4250  plano geral do quarto acendendo, 18 mm
  f4251–4340  plano médio da Vovó assobiando, o bebê olhando para ela (2 shot), 28 mm
  f4341–4400  primeiro plano do bebê rindo, 35 mm
  f4401–4485  plano médio dos dois rindo, dolly out lento → branco
câmera:
  movimento: dolly out lento
  de: (43, 2.2, 1.2) · olhando (43, 4, 1.0)   →   para: (43, 1.2, 1.4) · olhando (43, 4, 1.0)
  duração: f4401–4485
rostos:
  BIBO BEBÊ f4126–4250 = 5 · f4251–4340 = 6 · f4341–4400 = 3 · f4401–4450 = 11 · f4451–4485 = 3
  VOVÓ f4200–4250 = 2 · f4251–4340 = 11 · f4341–4485 = 3
efeitos (pós): **vinheta branca borrada** em toda a cena (look kids-memória) · desfoque leve nas bordas · grão leve · entrada e saída com fade branco de 10 quadros (f4126–4135, f4476–4485)
texto na tela: nenhum
som: chuva e trovão abafados (como se fossem lembrança: passa-baixa 2 kHz) · "uéé... hihi! pft!" do bebê · assobio normal · **caixinha de música com as 4 notas** (sintetizada) alta: é o momento mais quieto, a música manda

### C014 — F039–F040 (+ pausa 1 s)
tipo: blender
mundo: fazenda_dia.obj (tronco)
local: tronco, noite (kids-noite) · quadros f4486–4725
elenco:
  - BIBO · VOVÓ (0,25) no joelho dele · PAÇOCA deitado ao lado
ações (quadro):
  f4486–4540  BIBO olha para a Vovó, enxuga as lágrimas com a manga (braço passa no rosto 2 vezes)
  f4541–4605  BIBO levanta, firme
  f4606–4695  BIBO respira fundo (peito sobe, ombros sobem), enche as bochechas, faz bico
  f4696–4725  pausa: tudo parado, só a respiração dele
planos:
  f4486–4540  primeiro plano do Bibo, 35 mm (rosto ainda molhado)
  f4541–4605  contra-plongée do Bibo de pé contra a lua (18 mm) — pequeno herói
  f4606–4725  primeiro plano frontal do Bibo, dolly in bem lento até o bico (50 mm)
câmera:
  movimento: dolly in
  de: (−11.5, −29.2, 1.0) · olhando (−11.5, −31, 1.05)   →   para: (−11.5, −30.1, 1.03) · olhando (−11.5, −31, 1.05)
  duração: f4606–4725
rostos:
  BIBO f4486–4540 = 4 · f4541–4605 = 13 · f4606–4725 = 11
  VOVÓ f4486–4725 = 2
efeitos (pós): nenhum
texto na tela: nenhum
som: fungada decidida · respiração · caixinha de música termina em f4540 · **silêncio total** f4696–4725 (só um grilo)

### C015 — F041–F043
tipo: blender
mundo: fazenda_dia.obj (beira da floresta)
local: beira da floresta, noite clara de lua (kids-noite, um pouco mais de luz) · quadros f4726–5100
elenco:
  - BIBO · VOVÓ (0,25) · PAÇOCA · MIMOSA sai da floresta · ZUMBI foge
ações (quadro):
  f4726–4845  BIBO assobia forte · `notas(tamanho=0.35)` coloridas (as 4 cores da família) saindo em arco · VOVÓ põe as mãos no rosto
  f4846–4900  silêncio: as árvores paradas
  f4901–4950  MIMOSA sai trotando da floresta · `coracoes()` f4930–4995
  f4951–4995  ao fundo, o ZUMBI sai correndo para o outro lado, braços para cima (gag)
  f4996–5060  BIBO tira leite (balde embaixo da Mimosa, braços alternando)
  f5061–5100  balde cheio (líquido branco sobe: objeto escala Z)
planos:
  f4726–4790  primeiro plano do Bibo assobiando, 35 mm, notinhas saindo
  f4791–4845  primeiro plano da Vovó, olhos de coração (reação), câmera baixa
  f4846–4900  grande plano geral da floresta escura, parada (espera)
  f4901–4995  plano geral: a Mimosa saindo das árvores; o zumbi fugindo bem pequeno no fundo
  f4996–5100  plano médio do Bibo tirando leite, 24 mm
câmera:
  movimento: estática + revelação lenta (sobe 0,5 m) na saída da Mimosa
  de: (−11, −28, 0.6) · olhando (−11, −36, 1.2)   →   para: (−11, −28, 1.1) · olhando (−11, −36, 1.0)
  duração: f4901–4995
rostos:
  BIBO f4726–4845 = 11 · f4846–4900 = 6 · f4901–5100 = 2
  VOVÓ f4791–4845 = 8 · f4846–4900 = 6 · f4901–5100 = 3
  MIMOSA f4901–5100 = 2
efeitos (pós): glare leve nas notas
texto na tela: nenhum
som: assobio forte (a melhor tomada!) · "ôôô!" · 1 s de silêncio · "MUU!" · "uaaah?!" do zumbi fugindo (Minecraft, pitch +3) · leite no balde · música: **orquestra calorosa** entra no "MUU!" (Scott Buckley, faixa esperançosa, CC BY 4.0, ou Audio Library `hopeful orchestral`), com o motivo das 4 notas tocado por um instrumento se der

### C016 — F044–F046
tipo: blender
mundo: fazenda_dia.obj (beira da floresta)
local: igual · quadros f5101–5430
cenário:
  - balde de leite cheio (objeto separado, líquido com shape key de onda)
elenco:
  - VOVÓ: escala 0,25 → **1** dentro do balde (f5206–5215, escondido pelo splash) · BIBO · MIMOSA · PAÇOCA
ações (quadro):
  f5101–5170  VOVÓ se inclina na borda do balde para beber
  f5171–5205  escorrega (pernas para cima) e cai dentro: `splash()` branco f5195
  f5206–5250  o balde treme; a Vovó cresce e sai dele, encharcada, **com o balde na cabeça**
  f5251–5295  VOVÓ tira o balde, ri
  f5296–5380  abraço apertado (Bibo pula no colo dela) · `coracoes(qtd=5)` f5300–5430
  f5381–5430  MIMOSA lambe os dois (língua = prop rosa) · PAÇOCA se esfrega nas pernas
planos:
  f5101–5170  plano detalhe: a Vovó pequena na borda do balde, câmera na altura do leite, 35 mm
  f5171–5205  plano médio: ela caindo (câmera lenta 50% de f5185 a f5200)
  f5206–5250  plano médio do balde: ela crescendo para fora (o balde sobe junto na cabeça), 24 mm
  f5251–5295  primeiro plano da Vovó com o rosto molhado de leite (gotinhas)
  f5296–5430  plano médio do abraço → dolly out para plano geral com a Mimosa e o Paçoca, lua atrás
câmera:
  movimento: dolly out
  de: (−11, −29.5, 1.3) · olhando (−11, −31, 1.1)   →   para: (−11, −26.5, 2.0) · olhando (−11, −31, 1.0)
  duração: f5296–5430
rostos:
  VOVÓ f5101–5170 = 2 · f5171–5205 = 6 · f5206–5250 = 6 · f5251–5295 = 3 · f5296–5430 = 8
  BIBO f5171–5250 = 6 · f5251–5430 = 3
  MIMOSA f5381–5430 = 4
efeitos (pós): `splash()` + `flash()` suave (branco 2 quadros) no crescimento · gotas de leite caindo do cabelo
texto na tela: nenhum
som: "iiih—" fininho · SPLASH de leite · "ahá!" (a voz **volta ao normal** no meio da palavra: corte de +7 para 0 semitom) · "ha-ha-ha!" · "slurp" · música no máximo e alegre

### C017 — F047–F049
tipo: blender
mundo: fazenda_dia.obj (cozinha)
local: cozinha à noite, luz quente da lâmpada (kids-noite + luz interna) · quadros f5431–5820
cenário:
  - frasco rosa caído na mesa, pingando no chão (gota animada a cada 15 quadros, poça rosa com emissão 0,3)
elenco:
  - PAÇOCA: escala 1 → **0,25** em f5551–5556 (escondido pela fumacinha) · GALINHA (entrou pela porta aberta) · BIBO e VOVÓ (normal, de pijama/camisola) na porta
ações (quadro):
  f5431–5490  PAÇOCA entra, cheira a poça
  f5491–5550  PAÇOCA lambe (3 lambidas) · `icone("?")` f5520–5550
  f5551–5565  `fumaca_puf()` rosa pequeno
  f5566–5610  a fumaça abre: PAÇOCA pequenininho, olhando as patas
  f5611–5680  a GALINHA olha para ele (cabeça inclina), dá um passo
  f5681–5770  a GALINHA persegue o PAÇOCA pela cozinha (volta em círculo em volta da mesa)
  f5771–5820  BIBO e VOVÓ na porta riem, se abraçam de lado
planos:
  f5431–5550  plano médio do gato e da poça, câmera baixa, 28 mm
  f5551–5610  plano médio: o puf e o gatinho (câmera desce para 0,2 m)
  f5611–5680  contra-plongée da galinha GIGANTE (ponto de vista do gatinho), 18 mm — espelho do plano do gato na C008
  f5681–5770  plano geral da cozinha de cima (24 mm): a perseguição em círculo
  f5771–5820  plano médio dos dois rindo na porta
câmera:
  movimento: estática (geral) · contra-plongée
  de: (3.5, 3.5, 0.15) · olhando (3.8, 2.5, 0.5)   →   para: igual
  duração: f5611–5680
rostos:
  PAÇOCA f5431–5550 = 1 · f5566–5610 = 6 · f5611–5770 = 6
  BIBO f5771–5820 = 3 · VOVÓ f5771–5820 = 3
efeitos (pós): aberração cromática curta (4 quadros) no puf · linhas de velocidade na perseguição
texto na tela: nenhum
som: "lep, lep, lep" · puf pequenininho · miado fininho (+7 semitons) · cacarejo bravo · risada dos dois · música: pizzicato cômico (o mesmo da C004) volta curtinho

### C018 — F050 (tela final)
tipo: blender
mundo: fazenda_dia.obj (quintal)
local: quintal, dia (kids-dia) · quadros f5821–6270 (15 s)
cenário:
  - quintal simples, céu azul; metade direita da tela livre (para os 2 vídeos e o botão)
elenco:
  - PAÇOCA (0,25) montado na GALINHA, dando voltas (loop de 4 s, 3,75 voltas) · VOVÓ e BIBO pequenos ao fundo, acenando
ações (quadro):
  f5821–6270  loop: galinha andando em círculo com o gatinho em cima (caminho circular de 1,5 m) · f6150–6270 VOVÓ assobia (`notas()`)
planos:
  f5821–6270  plano geral fixo, 24 mm, tudo do lado esquerdo da tela
câmera:
  movimento: estática
  de: (8, −16, 1.2) · olhando (6, −12, 0.5)   →   para: igual
  duração: 15 s
rostos:
  PAÇOCA = 4 (amor: gostou do passeio) · VOVÓ = 2 · BIBO = 2
efeitos (pós): botão de inscrever animado (próprio) · moldura para os 2 vídeos da tela final
texto na tela: nenhum (o YouTube põe os vídeos)
som: **tema da série**: ukulele (o mesmo da C001) + assobio forte das 4 notas no fim (f6150)
