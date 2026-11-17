"""Personagem deitado (mannequin com pose:"sleeping", Minecraft 1.21.9+/26.x) no lugar certo.

Medido no jogo (26.3, vista de cima, 16/11/2026):
- A POSICAO da entidade e a dos PES. O corpo gira em torno dos pes e se estende ~1,8 x escala
  (atributo minecraft:scale) na direcao da cabeca. Largura ~0,6 x escala, altura deitado ~0,6 x escala.
- Direcao da cabeca pelo yaw (Rotation[0]):  0 -> -x (oeste)   90 -> +z (sul)   180 -> +x (leste)   270 -> -z (norte).
- Fica de barriga para cima (rosto para o ceu).
- So mover em Y durante a animacao (tp ... yaw 0): deslocar em X/Z gira o corpo e o tira do lugar;
  essa rotacao do corpo nao volta com tp -> recriar (kill + summon) antes de cada tomada.
- A LUZ do personagem vem do bloco onde ficam os PES: bloco solido ali = personagem preto (e sufoca).
  Nao coloque bloco na celula dos pes; use Invulnerable:1b (o /damage em entidade invulneravel da erro
  e o erro aborta a funcao inteira, inclusive o schedule da camera).
- Camera olhando para +z (sul): +x (leste) aparece a ESQUERDA da tela.

Uso: pes = deitado.pes(cabeca_x, y, cabeca_z, 'leste', escala=1.2)
     cmds = deitado.cmds(cabeca_x, y, cabeca_z, 'leste', escala=1.2, tag='hero')
cabeca_x/z = ponto onde deve ficar o TOPO da cabeca (deixe ~0,2 de folga da parede)."""
DIR = {'oeste': (0, -1, 0), 'sul': (90, 0, 1), 'leste': (180, 1, 0), 'norte': (270, 0, -1)}
COMPR = 1.8   # comprimento do corpo deitado em escala 1


def pes(cx, y, cz, direcao, escala=1.0):
    yaw, dx, dz = DIR[direcao]
    L = COMPR * escala
    return cx - dx * L, y, cz - dz * L, yaw


def cmds(cx, y, cz, direcao, escala=1.0, tag='hero', extra=''):
    x, y, z, yaw = pes(cx, y, cz, direcao, escala)
    return ['summon mannequin %.3f %.3f %.3f {Tags:["%s"],NoGravity:1b,Rotation:[%df,0f],pose:"sleeping"%s}' % (x, y, z, tag, yaw, extra),
            'attribute @e[tag=%s,limit=1] minecraft:scale base set %s' % (tag, escala)]
