# ferramentas/blender — cenas de Minecraft por script

Kit pequeno para o formato 3 (animações no Blender). Monta cada plano a partir de uma lista em JSON
e renderiza sozinho, sem abrir o Blender. Testado no **Blender 5.2.3 LTS** (Windows 11).

| Arquivo | O que faz |
|---|---|
| `looks.py` | `aplicar_look("humor" / "epico" / "kids" / "toon")`: motor, cor (AgX), céu, névoa, sol e luz de borda, DOF, motion blur, compositor (glare, saturação, aberração cromática, vinheta escura ou branca, letterbox), fps. Também `toon_material`, `contorno`, `animacao_em_dois`, `mat_pixel`. |
| `efeitos.py` | aura, raio, bola_energia, anel_choque, flash, linhas_velocidade, buraco_negro, explosao, icone (coração, "!?"), coracoes, tremida_camera. |
| `boneco.py` | boneco de blocos próprio (Tito) para testes: cabeça, corpo, braços e pernas com pivô. `criar`, `posar`, `andar`, `mover`. |
| `montar_cena.py` | lê o JSON e monta + renderiza cada plano (PNG e, se tiver ffmpeg, MP4). |
| `folha_contato.py` | (fora do Blender, Pillow) junta quadros de cada plano numa imagem só, para conferir. |
| `teste_shots.json` | 7 planos pequenos que usam todos os looks e todos os efeitos. |

## Como usar

```
"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P montar_cena.py -- planos.json
"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P montar_cena.py -- planos.json 03_raio 05_fim
python folha_contato.py "PASTA_DE_SAIDA"
```
O segundo comando renderiza só os planos com esses nomes. O tempo de render por quadro vai para `tempos.txt` na pasta de saída.

**Renders ficam fora do repositório** (ex.: `..\canalminezinho-testes\blender\`). Não aponte `saida` para dentro do repo.

## Formato do JSON

```json
{
  "padrao": { "resolucao": [1920, 1080], "saida": "C:/.../render", "video": true },
  "planos": [
    {
      "nome": "01_encontro",
      "look": "kids",
      "look_extra": { "vinheta_branca": 0.6, "aberracao": 0.03 },
      "motor": "EEVEE",
      "fps": 30,
      "frames": [1, 72],
      "passo": 2,
      "salvar_blend": false,
      "cenario": [
        { "tipo": "chao", "tamanho": 30, "cor": [0.33, 0.58, 0.22] },
        { "tipo": "bloco", "pos": [2, 4, 0.5], "cor": [0.5, 0.5, 0.5] },
        { "tipo": "obj", "obj": "C:/mundos/vila.obj", "pos": [0, 0, 0], "escala": 1, "rot_z": 0, "mcprep": true }
      ],
      "personagens": [
        { "nome": "Tito", "pos": [-2, 0, 0], "rot_z": 90, "cores": { "camisa": [0.2, 0.6, 0.3] },
          "andar": [1, 48, 8, 35],
          "mover": { "para": [0, 0, 0], "frames": [1, 48] },
          "poses": [ { "frame": 50, "braco_d": [-90, 0, 0], "cabeca": [0, 0, 20] } ] },
        { "nome": "Vila", "obj": "C:/skins/meu_personagem.obj", "pos": [3, 0, 0] }
      ],
      "camera": { "de": [0, -7, 2], "para": [0, -5, 1.8], "alvo": [0, 0, 1.2], "alvo_para": [1, 0, 1.2],
                  "lente": 35, "fstop": 2.8 },
      "efeitos": [
        { "tipo": "aura", "pos": [-2, 0, 0], "frames": [1, 48], "cor": [1, 0.8, 0.2] },
        { "tipo": "icone", "icone": "!?", "pos": [3, 0, 2.6], "frames": [50, 70] },
        { "tipo": "tremida_camera", "frames": [52, 58], "forca": 0.12 }
      ]
    }
  ]
}
```

- Tudo de `padrao` vale para todos os planos (o plano pode trocar). `saida` = pasta; cada plano vira `saida/NOME/0001.png…` e `saida/NOME.mp4`.
- `look_extra` troca qualquer valor da tabela `LOOKS` em `looks.py` (ex.: `nevoa`, `glare`, `fstop`, `amostras`, `letterbox`, `vinheta`).
- `motor` (`EEVEE` ou `CYCLES`) e `fps` passam por cima do look.
- Posições em metros. Câmera olha mais ou menos para **+Y**; o boneco olha para **-Y** (`rot_z: 90` = olha para +X).
- Boneco: partes `cabeca`, `braco_d`, `braco_e`, `perna_d`, `perna_e`, rotação em graus. `braco_d: [-90, 0, 0]` = braço para frente. `andar: [ini, fim, passo, angulo]` (os dois últimos são opcionais).
- No look `toon`, o `montar_cena` aplica sozinho: material toon em tudo, contorno em tudo menos o chão, animação em dois nos bonecos (`passo`, padrão 2). A câmera continua suave.
- Efeitos: `tipo` = nome da função em `efeitos.py`, `frames` = `[ini, fim]`, o resto são os parâmetros dela.

| Efeito | Parâmetros (além de `frames`) |
|---|---|
| `aura` | `pos` (pé do personagem), `cor`, `altura` |
| `raio` | `de`, `para`, `cor`, `grossura` |
| `bola_energia` | `pos`, `cor`, `raio` |
| `anel_choque` | `pos`, `cor`, `raio`, `normal` (para onde o anel "olha") — use 6–8 quadros |
| `flash` | `pos`, `forca` — use 1–3 quadros |
| `linhas_velocidade` | `pos`, `forma` (`radial` ou `paralelo`), `eixo` (direção da corrida), `cor`, `qtd` |
| `buraco_negro` | `pos`, `raio`, `cor` |
| `explosao` | `pos` (no chão), `cor`, `tamanho`, `detritos` — já inclui flash e anel |
| `icone` | `icone` (`coracao`, `!?`, `!`, `?`), `pos`, `cor`, `tamanho` — sempre de frente para a câmera |
| `coracoes` | `pos`, `qtd` |
| `tremida_camera` | `forca` (metros, 0,05–0,2) |

## Usar no Python do Blender (sem JSON)

```python
import sys; sys.path.insert(0, r"...\ferramentas\blender")
import looks, efeitos, boneco
looks.aplicar_look("epico")
boneco.criar("Tito", (0, 0, 0))
efeitos.raio((0, -0.4, 1.4), (6, -0.4, 1.4), 10, 30)
```

## O que foi testado (12/11/2026)

`teste_shots.json`, 480×270, Eevee (o plano 07 em Cycles), todos renderizados sem erro e conferidos na folha de contato:
4 looks, 11 efeitos, boneco andando/posando, toon + contorno + animação em dois, textura de pixel Closest, MP4 pelo ffmpeg.
Tempo por quadro (480×270, este PC): Eevee 0,13–0,27 s · Cycles 16 amostras 1,6 s.
Em 1080p conte ~10–20× isso.

## O que NÃO foi testado / limites

- **MCprep** (`"mcprep": true`): não está instalado. O código só chama `bpy.ops.mcprep.prep_materials()` se o MCprep existir; nunca rodou.
- **Mundo real do Mineways** (OBJ grande com texturas): não testado. A importação usa `bpy.ops.wm.obj_import` e põe toda textura em Closest. Mundos grandes podem passar da caixa de névoa (`nevoa_tam`, padrão 120 m).
- **Névoa** é uma caixa com volume, não o World: no Blender 5.2 o volume no World deixou o quadro todo preto (Eevee e Cycles).
- A **explosão** é simples (esfera de fogo com ruído + blocos em arco). No look humor (AgX) o fogo fica alaranjado claro, não vermelho vivo. Fogo de verdade = Mantaflow ou sprite.
- Rim light, sol e câmera seguem a convenção "câmera olha para +Y"; câmera de costas para isso deixa o rim na frente.
- Resolução 1080p e planos longos não foram medidos. Partículas são recalculadas a cada render (sem cache salvo).
- Boneco é só para teste; personagens dos vídeos = rig próprio (MCprep/Blockbench) importado por `obj`.
