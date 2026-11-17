# Exemplo 05 — "Queda sem paraquedas" com a capivara

Short vertical de 64,6 s recriando o formato de um vídeo viral de queda livre (personagem cai de um avião, procura onde pousar, plana até uma floresta nevada e sobrevive).
O roteiro foi traduzido de um vídeo de outro criador, por isso **não** está neste repositório (regra do repo); só o método, a lista de planos e a bíblia do cenário.

## Versões e o que cada feedback ensinou
| Versão | Feedback do usuário | Correção |
|---|---|---|
| v1 | cenário não batia com a narração (campo de terra = quadradinho dentro da floresta) | cenário construído pelo roteiro sobre o oceano |
| v2 | terreno parecia plano/artificial | naturalizar + decorar |
| v3 | personagem escondido atrás da legenda; queria rosto animado | mirar calculado; rosto em blocos |
| v4 | câmera travada; pausa depois do corte; fim do mapa aparecendo | velocidade no servidor (datapack), cortes no início do movimento, costa + serra |
| abertura | começo pouco engajante | corrida no corredor do avião, salto, explosão |
| v5 | "falta algo para viralizar" | crítica comparativa (guia 16 §1) → capivara, 47 planos, cor, legenda de 1 palavra, whoosh, −12 LUFS |
| v6 | rosto atrasado, "por trás" estranho, mapa em cima da legenda, buraco antes do pouso | partes no mesmo tick, 3/4, linha do mapa fora da legenda, forceload |
| v7 | capivara flutuando na explosão; parando em cima da neve | explosão em thread, personagem solto; queda até dentro da neve |
| v8 | lago mostrava um telhado | câmera do outro lado do lago |

## Arquivos
- A bíblia do cenário (frase → fato visual → elemento → plano) fica fora do repo porque cita o roteiro de terceiro; o formato está no guia 16 §2.
- `planos_v5.json` — os 47 planos (tempo de saída, take, linhas de velocidade).
- `processo_otimizado.md` — análise do processo e otimizações.
