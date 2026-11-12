# Vozes: gravar você mesmo ou TTS do Gemini

Escolha no começo do projeto (o Claude pergunta na 1ª mensagem de cada conversa nova). Vale para todos os formatos.

| | Eu gravo | TTS do Gemini (Google AI Studio) |
|---|---|---|
| Qualidade | a mais natural, emoção de verdade | boa, sotaque pt-BR certo, lê números e R$ |
| Personagens | você faz todas as vozes (muda o jeito; o Claude ajusta tom/eco por personagem) | 1 voz fixa por personagem |
| Trabalho seu | gravar e editar | nenhum (só aprovar) |
| Tempo das falas | `alinhar_voz.py` acha cada frase | o Claude já sabe (gera por bloco e alinha igual) |
| Limite | — | ~45 gerações ("Runs") por conta Google por dia |
| YouTube Studio | normal | marcar **conteúdo alterado/sintético = Sim** |

## 1. Eu gravo
1. Microfone perto da boca (2 palmos), quarto com cortina/cama (menos eco), celular no modo avião.
2. Programa: Audacity ou Reaper (grátis/barato). 48 kHz.
3. Leia o `roteiro.md`: cada frase com o tom e a pausa marcados (guia 09 §1). Errou → repita a frase inteira.
4. Edite: corte erros e respiros, redução de ruído leve. Nas `[pausa de cena N s]` deixe só 2 s.
5. Salve `videos/NN_tema/voz.wav` e avise o Claude.
6. Vários personagens: grave todas as falas na ordem, mudando a voz. O Claude separa por personagem pelo roteiro e pode mudar o tom (pitch), pôr eco ou "voz de rádio".

## 2. TTS do Gemini (Google AI Studio)
O Claude usa o Chrome (Claude in Chrome) em `aistudio.google.com/u/N/generate-speech`, com a conta Google que o usuário escolher.

### Voz fixa por personagem (`personagens.md`)
Cada personagem (e o narrador) tem 1 voz do AI Studio + 1 texto de estilo, **sempre iguais** em todos os vídeos:
```
## NARRADOR
voz: <nome da voz no AI Studio>
estilo: Brazilian Portuguese documentary narrator, curious and warm male voice, clear, medium pace, short pause after every number.

## LIA
voz: <nome da voz>
estilo: Brazilian Portuguese teenage girl, fast and curious, bright, a bit nervous.
```
Escolha as vozes ouvindo 2–3 opções no 1º vídeo e anote. Não troque depois (o público reconhece o personagem pela voz).

### Como o Claude gera
1. Junta as falas por personagem e por bloco (até ~140 palavras por Run).
2. Diálogo de 2 personagens: o AI Studio aceita **2 falantes no mesmo Run** (Speaker 1 e Speaker 2, cada um com sua voz); com 3 ou mais, gera separado e junta.
3. O tom de cada frase (`[irônico · devagar]`) vai para o estilo ou para uma instrução curta antes da fala.
4. Baixa cada áudio, confere a velocidade (100–140 palavras/min) e junta com as pausas do roteiro.
5. Roda `alinhar_voz.py` para ter `tempos.json`, igual à voz gravada.

### Cuidados (aprendidos no outro canal)
- ~45 Runs por conta por dia; a cota volta no dia seguinte. Conte os Runs antes de começar um episódio.
- Na 1ª vez, o Chrome pode bloquear vários downloads do site: o usuário clica no ícone de download bloqueado → "Sempre permitir" → recarrega a aba.
- Um dialog novo volta para a voz padrão e o estilo vazio: conferir voz e estilo antes de cada Run.
- Pausar o player antes de baixar. Um clique real no botão Download.
- Se aparecer "Quota limit reached" ou oferta de plano pago: parar e perguntar ao usuário (nunca comprar nada).
- Página nova pedindo aceite de termos: só o usuário aceita.
