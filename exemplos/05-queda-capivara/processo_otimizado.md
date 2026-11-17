# Processo de criação — o que deu errado na v1 e como fica daqui pra frente

## Problemas da v1 (medidos)
1. **Cenário achado, não construído.** Usei o mundo existente (vila taiga cercada de floresta nevada) e montei peças soltas. Resultado: o "campo de terra dura" era um quadrado no meio da floresta, e a floresta "longe, pro lado" estava em todo lugar. O visual contradizia a narração.
2. **Nenhuma checagem roteiro × imagem antes de gravar.** Eu conferia se cada take estava enquadrado, não se ele provava a frase.
3. **Exploração cara.** ~40 % do tempo foi procurar biomas, árvores com visada livre e ângulos de câmera em mundo natural (mapas de altura, raycasts, várias tomadas de teste).
4. **Retakes por bugs de ferramenta:** peças piscando (reenvio da mesma transformação), salto de peça ao mudar o deslocamento depois de montar, displays invisíveis além de ~160 blocos (raio de rastreio), summon falhando em chunk não carregado, gravação com 1 quadro.

## Pipeline novo (v2)
1. **Bíblia do cenário** (a bíblia do cenário): cada frase com afirmação sobre o lugar vira FATO visual + ELEMENTO + PLANO que prova. Proibições explícitas (ex.: nenhuma neve fora da floresta).
2. **Mapa-maquete construído do zero** (`set_queda.py`): uma área plana sobre o oceano (tela em branco), cada elemento posicionado conforme a história (Steve cai sobre o lago → vila ao lado → campo grande colado → floresta nevada única e distante). Todas as coordenadas em `SET`; os takes só leem `SET`.
3. **Naturalizar** depois de posicionar: colinas por ruído com máscara que preserva as features, mato/flores/manchas de terra, bosques verdes esparsos (verdes ≠ floresta nevada, então não confundem a história).
4. **Maquete de cima antes de gravar** (`set_queda.maquete()`): uma imagem do mapa inteiro; só grava depois que ela "conta a história" sozinha.
5. **Takes por script** (`takes2.py`), personagem Steve (`motor.Steve`: cabeça real player_head + corpo articulado), uma folha de contato por lote.
6. **Montagem por receita** (`montar_queda.py`) com legenda/voz já alinhadas; a voz só é gerada uma vez.

## Otimizações para os próximos
- Reaproveitar o **mapa-maquete** como template: lago/vila/campo/floresta/rodovia são parâmetros; um novo roteiro "queda/viagem" muda só `SET`.
- **Regra dos 160 blocos:** elementos que precisam aparecer em plano muito aberto (anel, linha, marcadores) devem ser blocos, não displays.
- Clareira de pouso já preparada no `set` (visada livre garantida) em vez de procurar ângulo em floresta natural.
- `Camera.criar` já teleporta e espera o chunk carregar; `posar` não reenvia transformação igual.
- Checar `nb_read_packets` de todos os takes antes de montar (gravação de 1 quadro).
- Comandos em lote por tile com `forceload` (funciona sem o jogador perto) e scripts retomáveis (arquivo de progresso).
