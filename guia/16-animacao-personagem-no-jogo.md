# 16 — Animação com personagem dentro do jogo (estilo "e se você...?")

Método testado em nov/2026 recriando um short viral de queda livre (personagem caindo de um avião, procurando onde pousar).
Tudo é feito no Minecraft Java 26.3 (Fabric + ponte MCP), sem Blender: personagem de `block_display`, cenário construído por script,
câmera por comando, montagem e legenda por código. Ferramentas: `ferramentas/animacao-no-jogo/`. Exemplo: `exemplos/05-queda-capivara/`.

## 1. O que faz um vídeo desses viralizar (comparação com o original de 15 mi de views)
Medido lado a lado (quadros nos mesmos segundos, cortes, cor, volume):

| Item | Original | Nossa 1ª versão | Regra |
|---|---|---|---|
| Personagem nos planos de lugar | em quase todo quadro | sumia (vista de cima vazia) | **personagem em TODO plano**, olhando o lugar (3/4, rosto visível) |
| Ritmo | ~1 plano por segundo | 1 a cada 2 s | **corte a cada palavra-chave** (~1 s), alternando perto / de baixo / de cima / lado |
| Distância | personagem grande no quadro | pequeno | câmera a 2–4 blocos; closes no rosto nas emoções |
| Altura | nuvens passando perto | poucas e longe | camadas de nuvens de blocos atravessadas (sem a câmera passar por dentro) |
| Cor | saturada, "brinquedo" | acinzentada | `eq=saturation=1.4:contrast=1.08`, vibrance, vinheta leve |
| Texto | 1 palavra branca pequena | blocos de 3 palavras + rótulos | **1 palavra por vez**, branca; dados (altitude) numa caixinha discreta |
| Personagem | mascote com acessório de marca | Steve genérico | personagem próprio com 1 detalhe memorável (ex.: capivara com laranja na cabeça) |
| Volume | −11,9 LUFS | −14 | master **−12 LUFS**, whoosh em cada corte |

Acabamento é condição necessária, não garantia: tema próprio e formato fixo pesam tanto quanto.

## 2. Cenário: construa a partir do roteiro (não procure no mundo)
- Monte a **bíblia do cenário**: cada frase que afirma algo sobre o lugar vira um FATO visual + o ELEMENTO + o PLANO que prova.
  Ex.: "a floresta fica longe, pro lado" = única mancha de neve do mapa, no outro extremo, a ~190 blocos do lago.
- Construa sobre uma área de **oceano aplainada** (tela em branco). Todas as coordenadas num dicionário `SET`; os takes só leem `SET`.
- Depois de posicionar: **naturalizar** (colinas por ruído com máscara que preserva as features), mato, flores, bosques verdes esparsos.
  O usuário rejeitou terreno plano e artificial.
- **Esconda o fim do mapa**: costa irregular (praia) nas laterais e uma serra verde atrás do elemento final (`moldura.py`).
- Tire **uma foto de cima** antes de gravar: se ela não conta a história sozinha, não grave.
- Comandos de cenário longe da câmera: sempre `forceload add/remove` antes (sem isso o `fill` falha com "not loaded" e sobra lixo de takes antigos).

## 3. Personagem de block_display
- Rig com juntas (tronco, cabeça, braços, pernas) em `motor.py` (`Pato` genérico, `Steve`, `Capivara`). Rosto em placas finas: pálpebras, brilho no olho, sobrancelhas e boca animáveis (`fechar`, `boca_ab`, `brava`).
- Mande a transformação **decomposta** (translation + left_rotation em quatérnio + scale), nunca a matriz; nunca reenvie a mesma transformação (a peça pisca).
- **Todas as partes no mesmo tick**: `posar()` monta uma lista em `storage queda:p` e chama `function queda:aplica` (datapack). Mandar parte por parte faz o rosto "descolar" da cabeça.
- Animação suave: nada de ruído aleatório por tick; oscilação senoidal a cada 6 ticks com `interpolation_duration` 7.

## 4. Câmera lisa
- A câmera é o jogador montado num `block_display` (rig). O cliente segue a posição do *servidor* do veículo: `teleport_duration` **não** suaviza o passageiro, e um `tp` por tick vindo do Python treme com o jitter da rede.
- Solução: **velocidade no servidor** — datapack com `$tp @s ~$(vx) ~$(vy) ~$(vz)` todo tick, lendo `storage queda:cam` (classe `Vel`). Mede-se com `travadas.py`: de 12,5 % de quadros repetidos para ~2 %.
- Planos sem rotação de câmera, velocidade constante, sem câmera lenta/acelerada na montagem.
- Personagem **preso** à câmera parece parado no ar em planos de ação: deixe-o solto caindo mais rápido que a câmera (`Trajeto`, displays com `teleport_duration` definido no `summon` ou ~0,1 s antes do `tp`).
- Nunca rode coisa demorada (explosão com dezenas de `summon`) dentro do laço de 20 Hz: use thread, senão o personagem para e "flutua".
- Mire calculando: `ang(alvo − câmera)`; nos closes, mire o ponto do rosto; câmera olhando para cima abaixo de y≈190 pega a parte de baixo cinza das nuvens vanilla.
- Quedas no chão: a trajetória continua até dentro da neve (nunca para em cima); o plano seguinte começa já no impacto.

## 5. Gravação e montagem
- Uma captura contínua por lote (`estudio.sessao_inicio/fim`); cada plano vira evento e a montagem recorta (`fonte()`). Iniciar o `gfxcapture` a cada take ficou instável.
- Cada plano grava 1,2 s de sobra; a montagem pula os quadros parados do começo (`inicio_mov`) e entra no 1º evento de ação + 0,35 s.
- Lista de planos única (`ORDEM` em `v5.py` → `roteiro/planos_v5.json`) com os tempos das palavras da narração.
- Distant Horizons recalcula LOD depois de grandes `fill` e come vários núcleos: baixe `numberOfThreads` só durante a gravação.

## 6. Checklist de conferência (antes de entregar)
- [ ] folha 2 qps do vídeo inteiro: personagem em todo plano, nada dentro de bloco, sem nuvem escura dominando
- [ ] `travadas.py`: quadros repetidos < 3 %, sem congelamento > 3 quadros fora de planos parados de propósito
- [ ] cada frase do roteiro × imagem (bíblia do cenário)
- [ ] marcador/linha do mapa fora da faixa da legenda
- [ ] continuidade nos cortes de ação (queda → impacto → buraco)
- [ ] `ebur128` ≈ −12 LUFS, duração = narração
