---
name: minecraft-animacao-no-jogo
description: Produz shorts de animação com personagem DENTRO do Minecraft Java (sem Blender) no formato viral "e se você...?" (queda livre, viagem, sobrevivência) - cenário construído a partir do roteiro, personagem de block_display com rosto animado, câmera lisa por velocidade no servidor, ~1 corte por palavra, legenda de 1 palavra, cor e master de short viral. Use quando o usuário pedir animação/história com personagem gravada no jogo, recriar um short animado de Minecraft, mascote do canal no jogo, ou reclamar de câmera travada / personagem flutuando / cenário que não bate com a narração.
---

# Animação com personagem dentro do jogo

Fonte: repositório `canalminezinho` (github.com/HendryGabriel/canalminezinho) — `guia/16-animacao-personagem-no-jogo.md` (método completo),
`ferramentas/animacao-no-jogo/` (scripts + datapack) e `exemplos/05-queda-capivara/` (versões e feedbacks).

## Ordem de trabalho
1. **Bíblia do cenário**: cada frase que afirma algo sobre o lugar → fato visual → elemento → plano. Mostre ao usuário antes de construir.
2. **Cenário por script** sobre oceano aplainado (`set_queda.py`, coordenadas só em `SET`), depois `naturalizar` + `decorar` + `moldura.py` (costa e serra escondem o fim do mapa). Foto de cima (`maquete`) que conte a história sozinha.
3. **Personagem próprio** com 1 detalhe de marca (ex.: `motor.Capivara`, laranja na cabeça). Rosto animável (`fechar`, `boca_ab`, `brava`).
4. **Lista de planos** com os tempos das palavras da narração (~1 plano por segundo), personagem em TODO plano (lugares em 3/4 com o rosto olhando o lugar), câmera a 2–4 blocos, closes nas emoções.
5. **Gravar** numa captura contínua (`v5.py todos`), Distant Horizons com poucos threads durante a gravação.
6. **Montar** (`montar_v5.py`): cor (+40 % saturação, contraste, vinheta), linhas de velocidade, 1 palavra de legenda branca, dados numa caixinha, whoosh nos cortes, −12 LUFS.
7. **Conferir** (guia 16 §6): folha 2 qps, `travadas.py` < 3 %, frase × imagem, continuidade nos cortes de ação.

## Armadilhas que já custaram retrabalho
- Câmera: nunca `tp` por tick do Python; use `Vel` (datapack `queda:tick`). `teleport_duration` não suaviza o jogador montado.
- Personagem: todas as partes no mesmo tick (`queda:aplica`); transformação decomposta em quatérnio; nunca reenviar a mesma.
- Personagem preso à câmera parece parado em ação: solte-o e faça cair mais rápido que a câmera. Coisas demoradas (explosão) em thread.
- `fill` longe da câmera exige `forceload`. Quedas continuam até dentro da neve/água; o plano seguinte começa no impacto.
- Câmera olhando pra cima abaixo de y≈190 mostra a base cinza das nuvens vanilla; nuvens de bloco só brancas e longe dos closes.
- Marcadores do mapa visto de cima: blocos reais (displays somem além de ~160 blocos) ou desenho na legenda ASS, fora da faixa da legenda.
- Recriar vídeo de outro criador serve para estudo; para publicar, tema e roteiro próprios (regra do repo).
