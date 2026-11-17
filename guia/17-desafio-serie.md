# Formato 4 — Desafio / Série (encenado)

Vídeo longo de desafio ("Skyblock mas...", "100 dias", sobrevivência com regra) **roteirizado e filmado por comando**.
O usuário só narra. O Claude escreve o roteiro, monta o mapa, filma as cenas pelo MCP/datapack e edita.

## 0. Regra de honestidade (obrigatória)
Não é survival jogado de verdade. Então:
- Uma frase leve na abertura do vídeo ("tudo aqui é encenado, eu escrevo, o personagem sofre").
- Descrição: "Vídeo roteirizado e gravado com comandos".
- YouTube Studio: marcar "conteúdo alterado/sintético = Sim" quando houver voz de IA.
- Nada de título ou thumb que diga "sobrevivi de verdade". O personagem é quem sobrevive.

## 1. Por que esse formato funciona (dados de 12/11/2026)
Vídeos longos de desafio com mais de 500 mil views nos últimos 3 meses: "100 dias" e hardcore (1 a 4 h), drama de SMP, "mundo para dormir", tutorial de construção.
Em comum: **regra simples, contador, ameaça que cresce, final claro**.

## 2. Molde de 10–12 min (1 episódio)
| % do tempo | Bloco | O que fazer |
|---|---|---|
| 0–5% | Gancho + regra | Mostrar o final ("no dia 30...") e a regra em 2 frases. Aviso de encenado. |
| 5–12% | O cenário | Ilha/mundo, o que o personagem tem, o que está em jogo, contador na tela |
| 12–85% | Escada de dias | 4 a 6 blocos de dias. Cada bloco: mob/problema novo → solução → perda (contador cai) → pausa |
| 85–95% | Clímax | O mob final. Um plano que usa o que foi plantado nos blocos anteriores |
| 95–100% | Lição + pergunta | 1 linha emocional, pergunta para os comentários, despedida curta |

## 3. Regras de roteiro do formato
1. **Plantar e colher:** tudo o que parece inútil no começo (areia, pólvora, poção) vira solução no clímax. O público sente a recompensa.
2. **Escada que só piora:** cada mob/problema é pior que o anterior. Nunca repetir o mesmo tipo de ameaça duas vezes seguidas.
3. **Contador de perda:** número simples na tela (blocos da ilha, vidas, comida). Cai a cada baque.
4. **Re-gancho a cada 1–2 min:** "mas o próximo é pior", "só que tem um problema".
5. **Dias que passam rápido:** blocos de dias sem graça viram uma frase ("passam os dias 21 a 23").
6. **Pausas de cena de 10–15 s** depois de cada revelação (música + imagem, sem fala).
7. **Final em 1 linha:** a lição do personagem, não do narrador.
8. Narrador sabe mais que o personagem ("ele ainda não sabe para quê. Eu sei.").
9. Fatos do jogo conferidos na Minecraft Wiki antes de narrar (`fatos.md`).

## 4. Como o Claude filma (sem jogar)
1. Mapa do desafio por comando (`mapa/`): `/fill` em lote, `forceload`, ver `videos/01_luta-ceu-quebrado/mapa/README.md`.
2. Personagem: mannequin ou Easy NPC com skin própria; mobs por `/summon`.
3. Cada cena do `cenas.md` vira uma função de datapack (`ferramentas/minecraft/datapack.py`) com ações no tempo da voz.
4. O MCP dá a ordem e tira print; OBS grava; câmera pelo rig do datapack (plano B: Flashback).
5. Contador de dias/blocos entra como texto na montagem (`montar.py`, `textos[]`, estilo `fixo`).

## 5. Checklist do episódio
- [ ] A regra cabe em 2 frases?
- [ ] O final aparece como gancho nos primeiros 30 s?
- [ ] Algo plantado nos primeiros 3 min volta no clímax?
- [ ] O contador cai em todo bloco?
- [ ] Cada bloco é pior que o anterior?
- [ ] Aviso de "encenado" na abertura e na descrição?
- [ ] Pergunta para os comentários antes da despedida?
- [ ] Fatos do jogo conferidos (`fatos.md`)?
- [ ] 130–145 palavras por minuto?
