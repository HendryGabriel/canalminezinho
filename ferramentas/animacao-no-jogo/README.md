# ferramentas/animacao-no-jogo — personagem animado + cenário por script + câmera lisa

Método: `guia/16-animacao-personagem-no-jogo.md`. Exemplo: `exemplos/05-queda-capivara/`.
Testado em nov/2026: Windows 11, Minecraft Java 26.3 Fabric, ponte **MCP Fabric**, Distant Horizons.

## Configuração (variáveis de ambiente)
| Variável | Para que |
|---|---|
| `ANIM_PROJETO` | pasta do vídeo (`brutos/`, `tmp/`, `final/`, `audio/`, `roteiro/`, `checkpoints/`, `overlays/`, `fontes/usar/`). Padrão: pasta atual |
| `MC_JOGADOR` | seu nick (padrão `@p`) |
| `MC_OPTIONS` | `options.txt` da instância |
| `ANIM_MUSICA` | trilha (padrão `<projeto>/audio/musica.mp3`) |

Instale o datapack: copie `datapack_queda/` para `saves/<mundo>/datapacks/queda` e rode `/reload`.
Ele traz `queda:tick` (velocidade da câmera/objetos por tick) e `queda:aplica` (todas as partes do personagem no mesmo tick).

## Scripts
| Script | Faz |
|---|---|
| `motor.py` | matemática (quatérnios), personagens (`Pato`, `Steve`, `Capivara`), `Camera` (rig), destroços, bola de fogo, `Modelo` (carro) |
| `set_queda.py` | constrói o cenário a partir de `SET` (base, vila, lago, campo, floresta, rodovia, nuvens), `naturalizar`, `decorar`, `maquete` |
| `moldura.py` | costa irregular + serra atrás da floresta (esconde o fim do mapa) |
| `cenarios.py` | `checkpoint()` / `restaurar()` de áreas |
| `takes3.py` | `Vel` (velocidade no servidor), `Trajeto` (segmentos interpolados), `rodar()`, planos de pouso |
| `v5.py` | **versão final**: função `queda()` genérica + os 47 planos e a lista `ORDEM` (tempos das palavras) |
| `abertura.py` | avião por dentro (corredor), corrida, salto e explosão |
| `takes.py`, `takes2.py` | versões anteriores (reaproveitadas por `v5.py`) |
| `estudio.py`, `rec.py`, `gravar.py` | preparar o cliente, captura contínua por sessão |
| `montar_v5.py` (+ `montar_queda.py`) | montagem: cor, linhas de velocidade, legenda de 1 palavra, altitude, whoosh, −12 LUFS |
| `linhas_v5.py` | overlays de velocidade (vertical e radial) |
| `travadas.py`, `passo_img.py` | medem quadros repetidos e regularidade do movimento |
| `pouso.py`, `mapa.py`, `ver_mapa.py`, `shot.py` | visada livre de câmera, heightmap, prints |

Uso típico: `python set_queda.py base vila lago campo floresta rodovia nuvens limpar_arvores naturalizar decorar` →
`python moldura.py costa serra arvores_serra verdejar arvores_serra2` → `python v5.py nuvens` → `python v5.py todos` → `python montar_v5.py`.
