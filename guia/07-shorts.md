# Shorts

Base: lista dos 113 Shorts com views (`dados/shorts.csv`) + 3 Shorts baixados, medidos e transcritos com Whisper (1,2 mi, 857 mil, 791 mil).

## 0. Método principal: Short estilo DonJone (estudo de 13/11/2026)
Canal brasileiro com 2,3 mi inscritos, 1.175 Shorts e **~1 mi de views por Short** (mediana). Estudo completo: `analises/shorts-donjone.md`.

### Molde de 1 Short (50–60 s, ~200 palavras)
| Tempo | O que acontece |
|---|---|
| 0,0–0,7 s | mascote do canal anda até a câmera, câmera entra em close no rosto |
| 0,0–3 s | **1ª frase = afirmação forte** contra o senso comum ou pergunta ("No Minecraft, o ouro é melhor que o diamante") + a prova visual na tela |
| 3–8 s | antecipa a objeção ("e eu não tô falando isso só porque...") |
| 8–40 s | **prova em cadeia**: 3–5 fatos do jogo ligados por "e", "mas", "isso porque", cada um com um número concreto |
| 40–50 s | virada ("mas tem um truque que quase ninguém sabe") |
| 50–56 s | **fecha no fato mais forte**, em 1 frase. Sem "se inscreve", sem despedida |
| últimos 2–6 s | imagem final sem fala (a fala acaba antes do vídeo) |

### Regras
- Fala **rápida**: 200–245 palavras/min (com a voz gravada, ler com energia; com TTS, estilo "fast and excited").
- **Uma imagem para cada ideia**, trocando a cada 1–2 s, mostrando **literalmente** o que a fala diz. O Claude monta por comando: item num bloco no meio de um lago, estrutura com `/place`, vila, tela de crafting com zoom, mobs "atuando".
- Shader suave, céu limpo; 1ª pessoa com HUD ou 3ª pessoa com o mascote.
- **Legenda**: 1–2 palavras por vez, minúsculas, letra grossa arredondada, branca com contorno escuro, pequena (~6% da largura), um pouco abaixo do centro.
- **Título**: 1–4 palavras com ponto final ("Eles são humanos.", "Profissionais."). Palavras fortes: melhor, errado, segredo, vida real.
- Volume −11 a −14 LUFS.
- **Loop:** a última frase termina na palavra que abre a primeira ("...feitas a partir do **ouro**." → "No Minecraft, o **ouro**..."). O vídeo acaba seco nessa palavra e o YouTube reinicia sem emenda: mais gente assiste de novo.
- **Som:** 1 música de fundo só, leve (lo-fi/arcade), contínua, ~10–15% do volume da voz, sem trocar. **Pop** em cada legenda, **whoosh** em cada corte, **som do próprio jogo** em cada ação (comer, quebrar, villager, poção, XP). Voz com todas as respirações cortadas e compressão forte. Exceção: Short de **teoria/lore/medo** usa trilha de suspense e **corta a música para silêncio** no momento arrepiante (ex.: a "voz" do mob), depois volta épica.
- **Mascote próprio** com 1 detalhe marcante (cor, acessório). Não copiar o capacete de diamante dele nem a skin.
- **Volume de produção**: vários Shorts por semana; o mesmo cenário serve para vários.

### 5 tipos que funcionam
1. Afirmação contra o senso comum ("X é melhor que diamante").
2. Teoria/lore ("os Endermen são humanos").
3. Mecânica escondida ("o que acontece se o seu cachorro morrer").
4. Dicas de profissional ("você tá minerando errado").
5. Vida real / história ("item do Minecraft na vida real", "o item mais antigo").

## 1. O que funciona (estudo do TheLuics)
| Short | Views | Tipo |
|---|---|---|
| IS THERE ANYONE IN YOUR MINECRAFT WORLD? (seeds) | 1,2 mi | curiosidade com conta, tirado do longo "A verdadeira escala" |
| The best XP farm in Minecraft | 910 mil | tutorial de farm |
| O THE END ERA PRA SER COMPLETAMENTE DIFERENTE | 857 mil | curiosidade de história do jogo |
| this youtuber thinks minecraft is small... poor guy | 791 mil | escala, título de meme |
| The best sand farm | 590 mil | tutorial de farm |
| the player NEVER APPEARED IN MINECRAFT | 542 mil | resumo do longo "Nunca teve jogador" |
| E SE VOCÊ QUISESSE QUEBRAR O MUNDO INTEIRO? | 529 mil | resumo do longo "100%" |

- Os temas dos longos de sucesso viram Shorts (e vice-versa): seed, escala, sem jogador, 100%, Far Lands (em 3 partes).
- Duração: **1 a 2 min** (Short pode ter até 3 min). Não são de 30 s.
- Título em inglês na maioria + `#minecraft #minecraftjava #minecraftbedrock #mcpe`.

## 2. Roteiro do Short
1. **1ª frase = afirmação chocante ou pergunta**, sem introdução: "Alguém pode estar jogando agora no seu mundo do Minecraft. Deixa eu explicar." / "O Minecraft é gigantesco. E não, isso não é um exagero." / "Você sabia que o End era pra ser assim?"
2. "Deixa eu explicar" e vai direto para a regra do jogo.
3. Conta passo a passo com 1 número grande e 1 comparação real (584 bilhões de anos = 42x a idade do universo; 210 mundos empilhados = 1 folha de papel).
4. Virada: "Mas isso não é 100% verdade" / "Mas não é bem assim."
5. Final com piada ou alfinetada: "...então o seu amigo que disse que tem a mesma seed do [youtuber] tá mentindo." / "Parabéns, o End."
6. Short-trailer: termina chamando o longo ("Sejam bem-vindos ao segundo episódio de Anomalias do Minecraft").

## 3. Edição do Short
- Vertical 9:16. Mesmos visuais do longo: estúdio 3D branco, multidões de personagens (Blender, array), cinematic com shader.
- Planos de 2-4 s; o Short de curiosidade do End teve 53 cortes em 2,3 min (1 a cada 2,5 s).
- Texto: só palavra-chave ou número no meio da tela ("NO SEU MUNDO.", "18", "584,5", "BUG", "8 FPS"). Sem legenda corrida.
- Volume -15 LUFS (para nós, -14).
