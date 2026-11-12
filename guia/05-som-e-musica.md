# Efeitos sonoros, música e mixagem

Base: análise do Gemini Pro com minutagem (`analises/gemini/`), deixas de som da legenda automática ([música], [risadas], [canto], [grito]) e medição de volume com ffmpeg.
O Gemini às vezes erra o segundo exato ou chuta o nome do som. Use como mapa, não como verdade absoluta.

## 1. Regra de ouro
**Se algo aparece ou se move na tela, faz som.** O Gemini contou 30-40 efeitos marcados por vídeo só nos primeiros minutos; na prática, 1 efeito a cada 3-5 s.

## 2. Dicionário de efeitos (o que ele usa em cada situação)
| Situação | Efeito |
|---|---|
| Texto aparece (pop) | pop curto / whoosh suave |
| Palavra digitando | máquina de escrever / teclado rápido |
| Número revelado | "ka-ching" (caixa registradora), ding |
| Número gigante subindo | tique de contador digital acelerado |
| Revelação de escala (Terra, monumento, título) | **boom grave / sub drop** com reverb |
| Câmera voando / troca de cena | whoosh longo, whoosh reverso |
| Gráfico (círculo, régua, seta) | beep de interface, sonar, risco de giz |
| Janela/menu do jogo | clique de mouse, clique duplo |
| Quebra de piada | **disco arranhando (record scratch)** + música corta seco |
| Susto/terror | horror stinger, batimento cardíaco, grito |
| Tempo passando | clique de câmera, relógio tiquetaqueando |
| Ação cartoon | "pow", boing, splat |
| Coisa do jogo na tela | **som original do Minecraft** (villager "hrmm", passos, madeira quebrando, portal, água na lava, Warden, Ender Dragon) |

Sons do jogo: extrair de `%APPDATA%\.minecraft\assets\objects` (índice em `assets\indexes\<versão>.json`). Efeitos genéricos: biblioteca própria (o usuário já tem `ESTUDOS/biblioteca-sfx/`), Pixabay, YouTube Audio Library, Epidemic.

## 3. Música
- **Troca a música a cada bloco do roteiro** (a cada 1-3 min), sempre combinando com a emoção da cena. Exemplo do vídeo "Nunca teve jogador":
  - mistério investigativo (abertura) → eletrônica de tutorial (aula técnica) → coral épico tipo chefão (piada do exército) → ukulele feliz irônico (vila alegre) → synthwave anos 80 (cena de DeLorean) → synth melancólico (bar) → música de assalto (o plano) → orquestral épica crescente (passagem do tempo, para seco no Big Bang) → drone sombrio (apocalipse) → cântico de igreja (villagers fanáticos) → silêncio + batimento (porão) → piano e violoncelo tristes (fim dos villagers) → lo-fi cômico ("comercial") → relógio rítmico (Endermen) → orquestra de guerra (Nether) → rumor de terror (Warden) → piano reflexivo subindo (lição final).
- Na "Verdadeira escala": riser de mistério → piano calmo nas contas → acordeão francês (piada de Paris) → synth investigativo (seeds) → orquestral épica que cresce a cada planeta → coral sombrio (monumento) → metais tensos (bastion) → orquestra infernal (Nether) → dark ambient (ancient city) → piano + cordas no final.
- **Música corta seco** para marcar piada ou susto. Silêncio total é uma ferramenta (piada da skin feia, descida ao porão).
- **Final sempre em piano/cordas emotivo**, subindo de volume na última frase.
- Padrão que se repete nos 5 vídeos analisados: **lo-fi/piano calmo nas contas** (relaxa para a matemática), **marimba/pizzicato cômico** nas piadas (estilo Kevin MacLeod, que tem licença CC BY em incompetech.com: dá para usar com crédito), **orquestral épica crescente** nas escalas, **drone escuro** no medo, **silêncio total** antes da piada final ou no clímax.
- No Short também: 4-5 trocas de música em 2 min, cada troca separada por 1 s de silêncio com disco arranhando.

## 4. Voz
- Voz real dele, gravada perto do microfone, com compressão forte e graves reforçados (voz de "documentário/rádio").
- Partes rápidas: respiros cortados (jump cut no áudio). Final: pausas longas de propósito.
- Ele faz todas as vozes das esquetes, mudando o tom: criança (pitch para cima), pai na igreja (reverb), robô cansado (abafado, graves). Villager francês com sotaque.

## 5. Mixagem (números)
- Medido: trechos só de música ficam em ~-23 LUFS e trechos com fala em ~-20,6 LUFS no mesmo vídeo → **nas pausas a música sobe quase até o nível da voz**.
- Durante a fala: música ~15-20 dB abaixo da voz (ducking).
- Nas pausas dramáticas e no final: música sobe para perto da voz (-5 dB).
- Master: o canal dele sai entre -21 e -15 LUFS. Para nós: **-14 LUFS integrado, pico -1 dBTP**.
- 3 trilhas separadas: VOZ, MÚSICA, SFX.

## 6. Direitos
- Não usar a trilha oficial do Minecraft (C418, Lena Raine, Aaron Cherof): tem Content ID.
- Ele usa músicas com letra em inglês em alguns trechos (synthwave cantado). Para nós: só trilha com licença (YouTube Audio Library, Epidemic, Artlist, Pixabay).

## 7. Receita rápida (ffmpeg)
```
# ducking da música pela voz + master -14 LUFS
ffmpeg -i voz.wav -i musica.wav -i sfx.wav -filter_complex \
"[1][0]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[m];\
[0][m][2]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1:LRA=11" mix.wav
```
Nas pausas do roteiro, suba a música à mão (keyframe de volume) ou corte a música em blocos e use `volume` por trecho.
