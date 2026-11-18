# Exemplo 06 — "O Vaso Vazio" (Capivara Ping & O Rei)

Short vertical narrativo de **65,9 s** (`47 planos`, `1080×1920`, `30 fps`, `-12 LUFS`) produzido 100% dentro do Minecraft Java via MCP Fabric (sem Blender), adaptando o conto clássico "O Vaso Vazio" com a mascote do canal (**Capivara Ping**).

> Manual e skill completos: [`../../skill/vaso-vazio-shorts-3d/SKILL.md`](../../skill/vaso-vazio-shorts-3d/SKILL.md)

## Destaques técnicos deste modelo
- **Fidelidade à referência + extensão >60s para monetização:** 43 planos cobrindo toda a narrativa original + 4 planos de epílogo (`P44..P47`: Ping no trono, distribuição de sementes verdadeiras e reino florescendo) totalizando `65,91 s`.
- **Modelos 3D ricos (`elenco.py` — `ModeloRico`):** suporte a rotações locais `(yaw, pitch, roll)` por peça, arredondamento octogonal (`0° + 45°`) para vasos e regador, flores abertas radialmente, panela translúcida com água/sementes/bolhas, coroa imperial Mianliu sob medida para a cabeça e laranja da Capivara, e semente cozida rachada nos hashis para super-close macro.
- **Proporções e geometria anti-clipping:**
  - `PingCapivara` (`escala=1.0`, `ALT_CHAO = 13.4*U`), `Rival` (`escala=1.0`, `ALT_CHAO = 18*U`), `Rei` (`escala=1.18`, `ALT_CHAO = 18*U*1.18`).
  - Ombros da Capivara abertos em `(±6.8*U, 9.0*U, +1.5*U)` e vaso a `0.56 m` à frente (`y_piso + 0.46 m`); pose `'sentado'` com joelhos dobrados em `90°` sobre a almofada do trono (`y=71.50`) e botas no tapete (`y=71.00`).
- **Cenário 360° sem fim de mapa (`set_vaso.py`):** ilha sobre o oceano, praias senoidais, serras 360° revestidas com `grass_block` + `moss_block` e bosques de cerejeiras, relevo com máscara protetora, Palácio Imperial iluminado (`light[level=15]`), Câmara da Caldeira, Lago Koi e Casa do Ping com janela real vazada.
- **Captura determinística 30 fps (`takes_vaso.py`):** captura direta do framebuffer OpenGL (`vision.screenshot` keep-alive) com `/tick rate 3.4` + velocidade no servidor (`Vel`) + pré-roll de `0.06 s` (`0%` de quadros repetidos) + mixagem exata dos `.ogg` oficiais do jogo (`render_audio_plano`).
- **Edição (`montar_vaso.py`):** grade quente vibrante, legenda `.ass` `Monocraft` de 1 palavra com micro-pop, whoosh nos cortes, sidechain ducking e master `-12 LUFS`.
