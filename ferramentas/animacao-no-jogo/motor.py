import os as _os
PROJ = _os.environ.get('ANIM_PROJETO', _os.getcwd())
"""Motor de cena do short 'Queda': pato montado com block_display (rig), destrocos com fisica, camera.
Tudo vanilla 26.3 por comando pela ponte mcpfabric."""
import math, time, threading, random
import numpy as np
import mc

PL = _os.environ.get('MC_JOGADOR', '@p')


def C(c):
    r = mc.cmd(c)
    if isinstance(r, dict) and not r.get('success', True):
        print('FALHOU', c[:160], '->', r.get('output') or r.get('error'))
    return r


# ---------------- matematica ----------------
def rx(a):
    c, s = math.cos(a), math.sin(a); return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]])


def ry(a):
    c, s = math.cos(a), math.sin(a); return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]])


def rz(a):
    c, s = math.cos(a), math.sin(a); return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


def T(x, y, z):
    m = np.eye(4); m[:3, 3] = [x, y, z]; return m


def S(x, y, z):
    return np.diag([x, y, z, 1.0])


def R(yaw=0, pitch=0, roll=0):
    """yaw em torno de Y (graus, sentido do Minecraft: 0=sul/+z, 90=oeste), pitch inclina a frente pra baixo, roll"""
    return ry(math.radians(-yaw)) @ rx(math.radians(pitch)) @ rz(math.radians(roll))


def mat_nbt(m):
    return '[' + ','.join(f'{v:.4f}f' for v in m.flatten()) + ']'


# ---------------- pato ----------------
D2 = math.radians
# parte: (bloco, pivo no corpo, tamanho, canto da caixa relativo ao pivo, junta)
PARTES = {
    'tronco': ('yellow_concrete', (0, 0.0, 0), (0.56, 0.62, 0.36), (-0.28, 0, -0.18), 'tronco'),
    'cabeca': ('yellow_concrete', (0, 0.62, 0), (0.56, 0.52, 0.5), (-0.28, 0, -0.25), 'cabeca'),
    'bico': ('orange_concrete', (0, 0.62, 0), (0.3, 0.13, 0.2), (-0.15, 0.12, 0.24), 'cabeca'),
    'olho_e': ('black_concrete', (0, 0.62, 0), (0.08, 0.12, 0.02), (0.1, 0.27, 0.245), 'cabeca'),
    'olho_d': ('black_concrete', (0, 0.62, 0), (0.08, 0.12, 0.02), (-0.18, 0.27, 0.245), 'cabeca'),
    'gorro1': ('red_wool', (0, 0.62, 0), (0.58, 0.07, 0.52), (-0.29, 0.5, -0.26), 'cabeca'),
    'gorro2': ('orange_wool', (0, 0.62, 0), (0.58, 0.07, 0.52), (-0.29, 0.57, -0.26), 'cabeca'),
    'gorro3': ('lime_wool', (0, 0.62, 0), (0.54, 0.07, 0.48), (-0.27, 0.64, -0.24), 'cabeca'),
    'gorro4': ('light_blue_wool', (0, 0.62, 0), (0.48, 0.06, 0.42), (-0.24, 0.71, -0.21), 'cabeca'),
    'gorro5': ('purple_wool', (0, 0.62, 0), (0.36, 0.06, 0.3), (-0.18, 0.77, -0.15), 'cabeca'),
    'braco_e': ('yellow_concrete', (0.28, 0.56, 0), (0.17, 0.5, 0.17), (0, -0.5, -0.085), 'braco_e'),
    'mao_e': ('orange_concrete', (0.28, 0.56, 0), (0.17, 0.12, 0.17), (0, -0.62, -0.085), 'braco_e'),
    'braco_d': ('yellow_concrete', (-0.28, 0.56, 0), (0.17, 0.5, 0.17), (-0.17, -0.5, -0.085), 'braco_d'),
    'mao_d': ('orange_concrete', (-0.28, 0.56, 0), (0.17, 0.12, 0.17), (-0.17, -0.62, -0.085), 'braco_d'),
    'perna_e': ('orange_concrete', (0.14, 0.02, 0), (0.2, 0.52, 0.2), (-0.1, -0.52, -0.1), 'perna_e'),
    'perna_d': ('orange_concrete', (-0.14, 0.02, 0), (0.2, 0.52, 0.2), (-0.1, -0.52, -0.1), 'perna_d'),
    'pe_e': ('orange_concrete', (0.14, 0.02, 0), (0.24, 0.08, 0.36), (-0.12, -0.6, -0.12), 'perna_e'),
    'pe_d': ('orange_concrete', (-0.14, 0.02, 0), (0.24, 0.08, 0.36), (-0.12, -0.6, -0.12), 'perna_d'),
}
# pose: rotacoes das juntas (graus, eixos x,y,z locais). x>0 gira a frente pra baixo (braco pra frente = x negativo)
POSES = {
    'pe': {},
    'estrela': {'braco_e': (0, 0, 115), 'braco_d': (0, 0, -115), 'perna_e': (0, 0, 28), 'perna_d': (0, 0, -28), 'cabeca': (-25, 0, 0)},
    'estrela2': {'braco_e': (-10, 0, 95), 'braco_d': (-10, 0, -95), 'perna_e': (15, 0, 35), 'perna_d': (15, 0, -35), 'cabeca': (-30, 0, 0)},
    'mergulho': {'braco_e': (180, 0, 10), 'braco_d': (180, 0, -10), 'perna_e': (0, 0, 4), 'perna_d': (0, 0, -4)},
    'planador': {'braco_e': (0, 0, 30), 'braco_d': (0, 0, -30), 'perna_e': (0, 0, 6), 'perna_d': (0, 0, -6), 'cabeca': (-35, 0, 0)},
    'desmaio': {'braco_e': (-40, 0, 70), 'braco_d': (30, 0, -120), 'perna_e': (-30, 0, 20), 'perna_d': (20, 0, -10), 'cabeca': (35, 0, 20)},
    'pouso': {'braco_e': (-150, 0, -25), 'braco_d': (-150, 0, 25), 'perna_e': (-50, 0, 8), 'perna_d': (-50, 0, -8), 'cabeca': (20, 0, 0)},
    'encolhido': {'braco_e': (-160, 0, -40), 'braco_d': (-160, 0, 40), 'perna_e': (-80, 0, 5), 'perna_d': (-80, 0, -5), 'cabeca': (30, 0, 0)},
    'bracos_cima': {'braco_e': (0, 0, 150), 'braco_d': (0, 0, -150), 'cabeca': (-20, 0, 0)},
}


class Pato:
    PARTES = None; POSES = None; CENTRO = 0.4
    fechar = 0.0      # 0 = olhos abertos, 1 = fechados
    boca_ab = 0.0     # 0 = fechada, 1 = aberta (grito)
    brava = 0.0       # sobrancelhas descem (careta contra o vento)

    def _rosto(self, nome, c, t):
        f = 1.0 if self.olhos_fechados else self.fechar
        H = t[1]                                        # altura original da placa
        if nome.startswith('olho') and f > 0.85:      # olho fechado = linha escura
            return (c[0], c[1] + 0.4 * H, c[2]), (t[0], 0.22 * H, t[2])
        if nome.startswith('brilho') and f > 0.5:
            return c, (0.001, 0.001, t[2])
        if nome.startswith('palp'):
            h = max(0.002, f * H)                       # palpebra desce do topo do olho
            return (c[0], c[1] + H - h, c[2]), (t[0], h, t[2])
        if nome.startswith('sobr'):
            h = max(0.002, (0.25 + 0.75 * self.brava) * H)
            return (c[0], c[1] - 0.5 * self.brava * H + (H - h), c[2]), (t[0], h, t[2])
        if nome == 'boca':
            h = H * (0.35 + 1.65 * self.boca_ab)
            return (c[0], c[1] + H * 0.5 - h * 0.5 - 0.6 * self.boca_ab * H, c[2]), (t[0], h, t[2])
        return c, t

    def __init__(self, tag='pato', escala=1.0):
        self.tag = tag; self.k = escala
        self.partes = self.PARTES or PARTES; self.poses = self.POSES or POSES
        self.pos = (0, 0, 0); self.ori = (0, 0, 0); self.pose = 'pe'; self.juntas = {}
        self.olhos_fechados = False
        self.off = (0, 0, 0)   # deslocamento quando montado na camera
        self.montado = False
        self._q = {}

    def _mats(self, ori=None, pose=None, juntas=None):
        """devolve {parte: nbt da transformacao decomposta} (translacao + rotacao em quaternio + escala)"""
        ori = ori or self.ori
        J = dict(self.poses[pose or self.pose]); J.update(juntas or {})
        k = self.k
        Rb = R(*ori)
        base = T(*self.off) @ S(k, k, k) @ Rb @ T(0, -self.CENTRO, 0)
        out = {}
        for nome, (blk, piv, tam, canto, junta) in self.partes.items():
            jr = J.get(junta, (0, 0, 0))
            Rj = rx(D2(jr[0])) @ ry(D2(jr[1])) @ rz(D2(jr[2]))
            c, t_ = canto, tam
            if self.partes is PARTES:
                if self.olhos_fechados and nome.startswith('olho'):
                    c = (canto[0] - 0.02, canto[1] + 0.04, canto[2]); t_ = (tam[0] + 0.04, 0.03, tam[2])
            else:
                c, t_ = self._rosto(nome, c, t_)
            M = base @ T(*piv) @ Rj @ T(*c)
            if blk == 'HEAD':   # item_display: modelo centrado, 0.5 de lado, rosto para -z
                q = quat((Rb @ Rj @ ry(math.pi))[:3, :3]); t_ = tuple(v / 0.5 for v in t_)
            else:
                q = quat((Rb @ Rj)[:3, :3])
            pq = self._q.get(nome)
            if pq is not None and sum(a * b for a, b in zip(q, pq)) < 0:
                q = tuple(-v for v in q)
            self._q[nome] = q
            sc = (k * t_[0], k * t_[1], k * t_[2])
            out[nome] = ('{translation:[%.4ff,%.4ff,%.4ff],left_rotation:[%.5ff,%.5ff,%.5ff,%.5ff],scale:[%.4ff,%.4ff,%.4ff],'
                         'right_rotation:[0f,0f,0f,1f]}' % (*M[:3, 3], *q, *sc))
        return out

    def criar(self, x, y, z, ori=(0, 0, 0), pose='pe', tdur=2, off=(0, 0, 0)):
        self.pos, self.ori, self.pose, self.off = (x, y, z), ori, pose, off
        self._q = {}
        C(f'kill @e[tag={self.tag}]')
        self._ult = self._mats()
        for nome, m in self._ult.items():
            blk = self.partes[nome][0]
            if blk == 'HEAD':
                C('summon item_display %.3f %.3f %.3f {Tags:["%s","%s_%s"],teleport_duration:%d,view_range:4f,'
                  'brightness:{sky:15,block:15},item:{id:"minecraft:player_head",count:1,components:{"minecraft:profile":'
                  '{texture:"entity/player/wide/steve"}}},transformation:%s}' % (x, y, z, self.tag, self.tag, nome, tdur, m))
                continue
            C('summon block_display %.3f %.3f %.3f {Tags:["%s","%s_%s"],teleport_duration:%d,view_range:4f,'
              'brightness:{sky:15,block:15},block_state:"minecraft:%s",transformation:%s}'
              % (x, y, z, self.tag, self.tag, nome, tdur, blk, m))

    def montar(self, off=None):
        """prende as partes no rig da camera: pato e camera se movem juntos sem tremer.
        Use criar(..., off=...) para ja nascer com o deslocamento (mudar off depois causa salto de parte)."""
        if off is not None and tuple(off) != tuple(self.off):
            self.off = off; self.posar(dur=1)
        self.montado = True
        C(f'execute as @e[tag={self.tag}] run ride @s mount @e[tag=camrig,limit=1]')

    def desmontar(self):
        self.montado = False
        C(f'execute as @e[tag={self.tag}] run ride @s dismount')

    def mover(self, x, y, z):
        self.pos = (x, y, z)
        C(f'tp @e[tag={self.tag}] {x:.3f} {y:.3f} {z:.3f}')

    def posar(self, pose=None, ori=None, dur=6, juntas=None):
        if pose: self.pose = pose
        if ori is not None: self.ori = ori
        if not hasattr(self, '_ult'): self._ult = {}
        itens = []
        for nome, m in self._mats(juntas=juntas).items():
            if self._ult.get(nome) == m:
                continue   # reenviar a mesma transformacao faz a parte piscar no cliente
            self._ult[nome] = m
            itens.append('{t:"%s_%s",d:%d,m:%s}' % (self.tag, nome, dur, m))
        if itens:   # todas as partes no MESMO tick (datapack queda:aplica): rosto nao atrasa em relacao a cabeca
            mc.cmd('data modify storage queda:p lista set value [' + ','.join(itens) + ']')
            mc.cmd('function queda:aplica')

    def remover(self):
        C(f'kill @e[tag={self.tag}]')


# ---------------- destrocos ----------------
def destrocos(cx, cy, cz, blocos, n=20, vel=0.6, vy=0.4, tam=(0.3, 1.0), tag='deb', espalhar=0.8, giro=True,
              brilho=False, gravidade=True):
    """cria n pedacos em volta de (cx,cy,cz) com velocidade aleatoria. Carregador = armor_stand pequeno invisivel
    (tem fisica e colide); o pedaco e um block_display passageiro, girado."""
    ids = []
    for i in range(n):
        b = random.choice(blocos); s = random.uniform(*tam)
        a = random.uniform(0, 2 * math.pi); h = random.uniform(0.3, 1.0)
        mx, mz = math.cos(a) * vel * h, math.sin(a) * vel * h
        my = vy * random.uniform(0.5, 1.3)
        px, py, pz = cx + random.uniform(-espalhar, espalhar), cy + random.uniform(-espalhar, espalhar) * 0.6, cz + random.uniform(-espalhar, espalhar)
        m = R(random.uniform(0, 360), random.uniform(-80, 80), random.uniform(-80, 80)) @ T(-s / 2, -s / 2, -s / 2) @ S(s, s, s)
        g = i % 4
        br = 'brightness:{sky:15,block:15},' if brilho else ''
        C('summon armor_stand %.2f %.2f %.2f {Tags:["%s","%s_c"],Invisible:1b,Small:1b,NoGravity:%db,Silent:1b,Invulnerable:1b,'
          'Motion:[%.3f,%.3f,%.3f],Passengers:[{id:"minecraft:block_display",Tags:["%s","%s_d","%s_g%d"],%s'
          'block_state:"minecraft:%s",transformation:%s}]}'
          % (px, py, pz, tag, tag, 0 if gravidade else 1, mx, my, mz, tag, tag, tag, g, br, b, mat_nbt(m)))
    if giro:
        threading.Thread(target=_girar, args=(tag,), daemon=True).start()


def _girar(tag, passos=4, dt=0.45):
    # cada passo: nova orientacao aleatoria por pedaco, interpolada (o cliente suaviza)
    time.sleep(0.06)
    for p in range(passos):
        # gira grupos inteiros (mesma rotacao aplicada a cada grupo, mas com escala/posicao propria):
        for g in range(4):
            yaw, pit, rol = random.uniform(0, 360), random.uniform(-90, 90), random.uniform(-90, 90)
            q = euler_quat(yaw, pit, rol)
            C('execute as @e[tag=%s_g%d] run data merge entity @s {start_interpolation:0,interpolation_duration:%d,'
              'transformation:{left_rotation:[%.4ff,%.4ff,%.4ff,%.4ff]}}' % (tag, g, int(dt * 20) + 1, *q))
        time.sleep(dt)


def quat(m):
    tr = m[0, 0] + m[1, 1] + m[2, 2]
    if tr > 0:
        S_ = math.sqrt(tr + 1.0) * 2; w = 0.25 * S_
        x = (m[2, 1] - m[1, 2]) / S_; y = (m[0, 2] - m[2, 0]) / S_; z = (m[1, 0] - m[0, 1]) / S_
    elif m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
        S_ = math.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2; w = (m[2, 1] - m[1, 2]) / S_
        x = 0.25 * S_; y = (m[0, 1] + m[1, 0]) / S_; z = (m[0, 2] + m[2, 0]) / S_
    elif m[1, 1] > m[2, 2]:
        S_ = math.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2; w = (m[0, 2] - m[2, 0]) / S_
        x = (m[0, 1] + m[1, 0]) / S_; y = 0.25 * S_; z = (m[1, 2] + m[2, 1]) / S_
    else:
        S_ = math.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2; w = (m[1, 0] - m[0, 1]) / S_
        x = (m[0, 2] + m[2, 0]) / S_; y = (m[1, 2] + m[2, 1]) / S_; z = 0.25 * S_
    return (x, y, z, w)


def euler_quat(yaw, pitch, roll):
    return quat(R(yaw, pitch, roll)[:3, :3])


def _old_euler_quat(yaw, pitch, roll):
    m = R(yaw, pitch, roll)[:3, :3]
    w = math.sqrt(max(0, 1 + m[0, 0] + m[1, 1] + m[2, 2])) / 2
    if w < 1e-4:
        return (1.0, 0.0, 0.0, 0.0)
    x = (m[2, 1] - m[1, 2]) / (4 * w); y = (m[0, 2] - m[2, 0]) / (4 * w); z = (m[1, 0] - m[0, 1]) / (4 * w)
    return (x, y, z, w)


def limpar(tag='deb'):
    C(f'kill @e[tag={tag}]')


def bola_fogo(x, y, z, r=3.0, tag='fogo', dur=14):
    """esfera de cubos laranja/amarelos brilhantes que cresce e some"""
    for i in range(14):
        b = random.choice(['orange_concrete', 'yellow_concrete', 'orange_concrete', 'red_concrete', 'shroomlight'])
        a, e = random.uniform(0, 2 * math.pi), random.uniform(-1, 1)
        d = random.uniform(0, r * 0.5)
        px, py, pz = x + d * math.cos(a) * math.sqrt(1 - e * e), y + d * e, z + d * math.sin(a) * math.sqrt(1 - e * e)
        s0 = 0.2
        m = R(random.uniform(0, 360), random.uniform(-60, 60), 0) @ T(-s0 / 2, -s0 / 2, -s0 / 2) @ S(s0, s0, s0)
        C('summon block_display %.2f %.2f %.2f {Tags:["%s","%s_%d"],brightness:{sky:15,block:15},'
          'block_state:"minecraft:%s",transformation:%s}' % (px, py, pz, tag, tag, i, b, mat_nbt(m)))
    time.sleep(0.1)
    for i in range(14):
        s = random.uniform(r * 0.6, r * 1.1)
        m = R(random.uniform(0, 360), random.uniform(-60, 60), random.uniform(-40, 40)) @ T(-s / 2, -s / 2, -s / 2) @ S(s, s, s)
        C('data merge entity @e[tag=%s_%d,limit=1] {start_interpolation:0,interpolation_duration:%d,transformation:%s}'
          % (tag, i, dur // 2, mat_nbt(m)))

    def sumir():
        time.sleep(dur / 40)
        for i in range(14):
            s = 0.05
            m = T(-s / 2, -s / 2, -s / 2) @ S(s, s, s)
            C('data merge entity @e[tag=%s_%d,limit=1] {start_interpolation:0,interpolation_duration:%d,transformation:%s}'
              % (tag, i, dur, mat_nbt(m)))
        time.sleep(dur / 20 + 0.2)
        C(f'kill @e[tag={tag}]')
    threading.Thread(target=sumir, daemon=True).start()


# ---------------- camera (jogador montado num display que se move com teleport_duration) ----------------
CAM = 'camrig'
EYE = 1.02


class Camera:
    def __init__(self, tdur=2):
        self.tdur = tdur

    def criar(self, x, y, z, yaw, pitch):
        C(f'ride {PL} dismount')
        C(f'tp {PL} {x:.2f} {y:.2f} {z:.2f}')   # carrega os chunks antes de criar o rig (summon longe falha)
        time.sleep(1.2)
        C(f'kill @e[tag={CAM}]')
        C('summon block_display %.3f %.3f %.3f {Tags:["%s"],teleport_duration:%d,block_state:{Name:"minecraft:air"}}'
          % (x, y - EYE, z, CAM, self.tdur))
        time.sleep(0.15)
        C(f'gamemode creative {PL}')
        C(f'ride {PL} mount @e[tag={CAM},limit=1]')
        self.olhar(yaw, pitch)

    def mover(self, x, y, z):
        C(f'tp @e[tag={CAM},limit=1] {x:.3f} {y - EYE:.3f} {z:.3f}')

    def olhar(self, yaw, pitch):
        mc.call('control.look', {'yaw': yaw, 'pitch': pitch})

    def fim(self):
        C(f'ride {PL} dismount'); C(f'kill @e[tag={CAM}]')


def yp(c, t):
    dx, dy, dz = t[0] - c[0], t[1] - c[1], t[2] - c[2]
    yaw = math.degrees(math.atan2(-dx, dz))
    pitch = -math.degrees(math.atan2(dy, math.hypot(dx, dz)))
    return yaw, pitch


class Relogio:
    """laço a 20 Hz: fn(t) chamada a cada tick ate dur"""
    def __init__(self, dur, fn, hz=20):
        t0 = time.time(); k = 0
        while True:
            t = time.time() - t0
            if t > dur: break
            fn(t)
            k += 1
            dl = t0 + k / hz - time.time()
            if dl > 0: time.sleep(dl)


# ---------------- modelo rigido (carro, aviao, marcadores) ----------------
class Modelo:
    """partes = {nome: (bloco, canto, tamanho)} em coordenadas locais; frente = +z"""
    def __init__(self, partes, tag):
        self.partes = partes; self.tag = tag; self.off = (0, 0, 0); self.ori = (0, 0, 0); self._q = {}

    def _nbt(self):
        Rb = R(*self.ori); out = {}
        for nome, (blk, c, t_) in self.partes.items():
            M = T(*self.off) @ Rb @ T(*c)
            q = quat(Rb[:3, :3]); pq = self._q.get(nome)
            if pq is not None and sum(a * b for a, b in zip(q, pq)) < 0:
                q = tuple(-v for v in q)
            self._q[nome] = q
            out[nome] = ('{translation:[%.4ff,%.4ff,%.4ff],left_rotation:[%.5ff,%.5ff,%.5ff,%.5ff],scale:[%.4ff,%.4ff,%.4ff],'
                         'right_rotation:[0f,0f,0f,1f]}' % (*M[:3, 3], *q, *t_))
        return out

    def criar(self, x, y, z, ori=(0, 0, 0), off=(0, 0, 0), tdur=2, brilho=True):
        self.ori, self.off = ori, off; self._q = {}
        C(f'kill @e[tag={self.tag}]')
        br = 'brightness:{sky:15,block:15},' if brilho else ''
        for nome, m in self._nbt().items():
            C('summon block_display %.3f %.3f %.3f {Tags:["%s","%s_%s"],teleport_duration:%d,view_range:8f,%s'
              'block_state:"minecraft:%s",transformation:%s}' % (x, y, z, self.tag, self.tag, nome, tdur, br, self.partes[nome][0], m))

    def montar(self):
        C(f'execute as @e[tag={self.tag}] run ride @s mount @e[tag=camrig,limit=1]')

    def posar(self, ori=None, off=None, dur=4):
        if ori is not None: self.ori = ori
        if off is not None: self.off = off
        for nome, m in self._nbt().items():
            C('data merge entity @e[tag=%s_%s,limit=1] {start_interpolation:0,interpolation_duration:%d,transformation:%s}'
              % (self.tag, nome, dur, m))

    def mover(self, x, y, z):
        C(f'tp @e[tag={self.tag}] {x:.3f} {y:.3f} {z:.3f}')

    def remover(self):
        C(f'kill @e[tag={self.tag}]')


CARRO = {
    'corpo': ('red_concrete', (-0.9, 0.3, -2.0), (1.8, 0.65, 4.0)),
    'capo': ('red_concrete', (-0.85, 0.95, -1.1), (1.7, 0.08, 2.2)),
    'vidro': ('light_blue_stained_glass', (-0.8, 0.95, -1.0), (1.6, 0.55, 1.9)),
    'teto': ('red_concrete', (-0.82, 1.5, -1.0), (1.64, 0.1, 1.9)),
    'r1': ('black_concrete', (0.8, 0.0, 1.0), (0.25, 0.6, 0.6)),
    'r2': ('black_concrete', (-1.05, 0.0, 1.0), (0.25, 0.6, 0.6)),
    'r3': ('black_concrete', (0.8, 0.0, -1.6), (0.25, 0.6, 0.6)),
    'r4': ('black_concrete', (-1.05, 0.0, -1.6), (0.25, 0.6, 0.6)),
    'farol1': ('yellow_concrete', (0.45, 0.55, 2.0), (0.35, 0.2, 0.05)),
    'farol2': ('yellow_concrete', (-0.8, 0.55, 2.0), (0.35, 0.2, 0.05)),
}


def snd(som, x, y, z, vol=1.0, pitch=1.0):
    C(f'playsound {som} master @a {x:.1f} {y:.1f} {z:.1f} {vol} {pitch}')


def snd_cam(som, vol=1.0, pitch=1.0):
    C(f'execute at {PL} run playsound {som} master @a ~ ~ ~ {vol} {pitch}')


# ---------------- Steve ----------------
U = 0.06  # 1 pixel da skin
PELE = 'white_terracotta'
STEVE = {
    # nome: (bloco, pivo, tamanho, canto relativo ao pivo, junta)   origem = quadril (meio da cintura)
    'tronco': ('cyan_concrete', (0, 0, 0), (8 * U, 12 * U, 4 * U), (-4 * U, 0, -2 * U), 'tronco'),
    'manga_e': ('cyan_concrete', (6 * U, 10 * U, 0), (4 * U, 4 * U, 4 * U), (-2 * U, -2 * U, -2 * U), 'braco_e'),
    'braco_e': (PELE, (6 * U, 10 * U, 0), (3.9 * U, 8 * U, 3.9 * U), (-1.95 * U, -10 * U, -1.95 * U), 'braco_e'),
    'manga_d': ('cyan_concrete', (-6 * U, 10 * U, 0), (4 * U, 4 * U, 4 * U), (-2 * U, -2 * U, -2 * U), 'braco_d'),
    'braco_d': (PELE, (-6 * U, 10 * U, 0), (3.9 * U, 8 * U, 3.9 * U), (-1.95 * U, -10 * U, -1.95 * U), 'braco_d'),
    'perna_e': ('blue_concrete', (2 * U, 0, 0), (4 * U, 10 * U, 4 * U), (-2 * U, -10 * U, -2 * U), 'perna_e'),
    'pe_e': ('gray_concrete', (2 * U, 0, 0), (4.05 * U, 2 * U, 4.05 * U), (-2.02 * U, -12 * U, -2.02 * U), 'perna_e'),
    'perna_d': ('blue_concrete', (-2 * U, 0, 0), (4 * U, 10 * U, 4 * U), (-2 * U, -10 * U, -2 * U), 'perna_d'),
    'pe_d': ('gray_concrete', (-2 * U, 0, 0), (4.05 * U, 2 * U, 4.05 * U), (-2.02 * U, -12 * U, -2.02 * U), 'perna_d'),
}
POSES_STEVE = dict(POSES)
POSES_STEVE.update({
    'estrela': {'braco_e': (0, 0, 120), 'braco_d': (0, 0, -120), 'perna_e': (0, 0, 25), 'perna_d': (0, 0, -25), 'cabeca': (-30, 0, 0)},
    'estrela2': {'braco_e': (-15, 0, 100), 'braco_d': (-15, 0, -100), 'perna_e': (20, 0, 30), 'perna_d': (20, 0, -30), 'cabeca': (-35, 0, 0)},
    'pouso': {'braco_e': (-170, 0, -20), 'braco_d': (-170, 0, 20), 'perna_e': (-45, 0, 6), 'perna_d': (-45, 0, -6), 'cabeca': (15, 0, 0)},
    'joelhos': {'braco_e': (-170, 0, -20), 'braco_d': (-170, 0, 20), 'perna_e': (-75, 0, 6), 'perna_d': (-75, 0, -6), 'cabeca': (15, 0, 0)},
    'encolhido': {'braco_e': (-150, 0, -35), 'braco_d': (-150, 0, 35), 'perna_e': (-85, 0, 5), 'perna_d': (-85, 0, -5), 'cabeca': (35, 0, 0)},
    'bracos_cima': {'braco_e': (0, 0, 155), 'braco_d': (0, 0, -155), 'cabeca': (-15, 0, 0)},
    'andar1': {'braco_e': (30, 0, 0), 'braco_d': (-30, 0, 0), 'perna_e': (-30, 0, 0), 'perna_d': (30, 0, 0)},
})


class Steve(Pato):
    PARTES = STEVE; POSES = POSES_STEVE; CENTRO = 6 * U

    def __init__(self, tag='steve', escala=1.0):
        super().__init__(tag, escala)


# ---- cabeca do Steve em blocos (rosto animavel: piscar, fechar olhos, boca abrir) ----
CAB = (0, 12 * U, 0)
PELE_R = 'white_terracotta'; CABELO = 'brown_concrete'
FZ = 4 * U          # frente da cabeca (+z)
EPS = 0.004


def _px(col, lin, w=1, h=1, dz=EPS):
    """placa no rosto: coluna/linha do pixel (0..7, linha 0 = topo); visto de frente a coluna 0 fica a esquerda"""
    x = 4 * U - (col + w) * U
    y = (8 - lin - h) * U
    return (x, y, FZ + dz - 0.01), (w * U, h * U, 0.01)


def _add(nome, bloco, ct):
    c, t = ct
    STEVE[nome] = (bloco, CAB, t, c, 'cabeca')


STEVE['cabeca'] = (PELE_R, CAB, (8 * U, 8 * U, 8 * U), (-4 * U, 0, -4 * U), 'cabeca')
STEVE['cabelo_topo'] = (CABELO, CAB, (8.3 * U, 2.15 * U, 8.3 * U), (-4.15 * U, 6 * U, -4.15 * U), 'cabeca')
STEVE['cabelo_nuca'] = (CABELO, CAB, (8.3 * U, 6.5 * U, 0.3 * U), (-4.15 * U, 1.5 * U, -4.15 * U), 'cabeca')
_add('cab_e', CABELO, _px(0, 2)); _add('cab_d', CABELO, _px(7, 2))
_add('olho_bco_e', 'white_concrete', _px(1, 4)); _add('olho_e', 'blue_concrete', _px(2, 4))
_add('olho_d', 'blue_concrete', _px(5, 4)); _add('olho_bco_d', 'white_concrete', _px(6, 4))
_add('nariz', 'brown_terracotta', _px(3, 5, 2))
_add('barba', CABELO, _px(2, 6, 4))
_add('boca', 'black_concrete', _px(3, 6, 2, 1, dz=2 * EPS))
_add('palp_e', PELE_R, _px(1, 4, 2, 1, dz=3 * EPS))
_add('palp_d', PELE_R, _px(5, 4, 2, 1, dz=3 * EPS))
_add('sobr_e', CABELO, _px(1, 3, 2, 1, dz=3 * EPS))
_add('sobr_d', CABELO, _px(5, 3, 2, 1, dz=3 * EPS))


# ---------------- Capivara (personagem do canal) ----------------
PELO, ESC, FOC = 'brown_concrete_powder', 'brown_terracotta', 'brown_concrete_powder'
CB = (0, 11 * U, 0)          # pivo da cabeca (topo do corpo)
FZC = 7 * U                  # frente do rosto (z)


def _pc(x0, y0, w, h, dz=EPS):
    """placa no rosto: x0,y0 = canto inferior esquerdo visto de frente (em U, x positivo = direita de quem olha)"""
    return (-(x0 + w) * U, y0 * U, FZC + dz - 0.01), (w * U, h * U, 0.01)


CAPI = {
    'tronco': (PELO, (0, 0, 0), (10 * U, 11 * U, 8 * U), (-5 * U, 0, -4 * U), 'tronco'),
    'cabeca': (PELO, CB, (13 * U, 10 * U, 12 * U), (-6.5 * U, 0, -5 * U), 'cabeca'),
    'focinho': (FOC, CB, (11 * U, 5.4 * U, 3.4 * U), (-5.5 * U, 0, FZC - 0.01), 'cabeca'),
    'nariz': (ESC, CB, (8 * U, 2.2 * U, 0.3 * U), (-4 * U, 3 * U, FZC + 3.4 * U - 0.012), 'cabeca'),
    'narina_e': ('black_concrete', CB, (1.2 * U, 1 * U, 0.02), (1.2 * U, 3.6 * U, FZC + 3.7 * U - 0.008), 'cabeca'),
    'narina_d': ('black_concrete', CB, (1.2 * U, 1 * U, 0.02), (-2.4 * U, 3.6 * U, FZC + 3.7 * U - 0.008), 'cabeca'),
    'orelha_e': (ESC, CB, (2.4 * U, 2.2 * U, 1.4 * U), (4 * U, 9.6 * U, -3.5 * U), 'cabeca'),
    'orelha_d': (ESC, CB, (2.4 * U, 2.2 * U, 1.4 * U), (-6.4 * U, 9.6 * U, -3.5 * U), 'cabeca'),
    'laranja': ('orange_concrete', CB, (4.6 * U, 4.2 * U, 4.6 * U), (-2.3 * U, 10 * U, -1.8 * U), 'cabeca'),
    'folha': ('lime_concrete', CB, (1.6 * U, 0.8 * U, 2.6 * U), (-0.4 * U, 14.2 * U, -0.9 * U), 'cabeca'),
    'braco_e': (PELO, (6 * U, 9.5 * U, 0), (3.2 * U, 7 * U, 3.2 * U), (-1.6 * U, -7 * U, -1.6 * U), 'braco_e'),
    'mao_e': (ESC, (6 * U, 9.5 * U, 0), (3.3 * U, 1.8 * U, 3.3 * U), (-1.65 * U, -8.6 * U, -1.65 * U), 'braco_e'),
    'braco_d': (PELO, (-6 * U, 9.5 * U, 0), (3.2 * U, 7 * U, 3.2 * U), (-1.6 * U, -7 * U, -1.6 * U), 'braco_d'),
    'mao_d': (ESC, (-6 * U, 9.5 * U, 0), (3.3 * U, 1.8 * U, 3.3 * U), (-1.65 * U, -8.6 * U, -1.65 * U), 'braco_d'),
    'perna_e': (PELO, (2.6 * U, 0.5 * U, 0), (4 * U, 5.5 * U, 4 * U), (-2 * U, -5.5 * U, -2 * U), 'perna_e'),
    'pe_e': (ESC, (2.6 * U, 0.5 * U, 0), (4.2 * U, 1.6 * U, 5.5 * U), (-2.1 * U, -6.9 * U, -2 * U), 'perna_e'),
    'perna_d': (PELO, (-2.6 * U, 0.5 * U, 0), (4 * U, 5.5 * U, 4 * U), (-2 * U, -5.5 * U, -2 * U), 'perna_d'),
    'pe_d': (ESC, (-2.6 * U, 0.5 * U, 0), (4.2 * U, 1.6 * U, 5.5 * U), (-2.1 * U, -6.9 * U, -2 * U), 'perna_d'),
}


def _addc(nome, bloco, ct):
    c, t = ct
    CAPI[nome] = (bloco, CB, t, c, 'cabeca')


_addc('olho_e', 'black_concrete', _pc(-5.2, 5.6, 2.4, 2.6))
_addc('olho_d', 'black_concrete', _pc(2.8, 5.6, 2.4, 2.6))
_addc('brilho_e', 'white_concrete', _pc(-3.9, 7.1, 0.9, 0.9, dz=2 * EPS))
_addc('brilho_d', 'white_concrete', _pc(4.1, 7.1, 0.9, 0.9, dz=2 * EPS))
_addc('palp_e', PELO, _pc(-5.3, 5.5, 2.6, 2.8, dz=3 * EPS))
_addc('palp_d', PELO, _pc(2.7, 5.5, 2.6, 2.8, dz=3 * EPS))
_addc('sobr_e', ESC, _pc(-5.4, 8.4, 2.8, 0.7, dz=3 * EPS))
_addc('sobr_d', ESC, _pc(2.6, 8.4, 2.8, 0.7, dz=3 * EPS))
CAPI['boca'] = ('black_concrete', CB, (4 * U, 0.9 * U, 0.02), (-2 * U, 0.9 * U, FZC + 3.4 * U - 0.006), 'cabeca')

POSES_CAPI = dict(POSES_STEVE)
POSES_CAPI.update({
    'corre1': {'braco_e': (70, 0, 10), 'braco_d': (-70, 0, -10), 'perna_e': (-60, 0, 0), 'perna_d': (55, 0, 0), 'cabeca': (-8, 0, 0)},
    'corre2': {'braco_e': (-70, 0, 10), 'braco_d': (70, 0, -10), 'perna_e': (55, 0, 0), 'perna_d': (-60, 0, 0), 'cabeca': (-8, 0, 0)},
    'salto': {'braco_e': (150, 0, 40), 'braco_d': (150, 0, -40), 'perna_e': (-40, 0, 10), 'perna_d': (30, 0, -10), 'cabeca': (-25, 0, 0)},
    'ouvidos': {'braco_e': (-20, 0, 150), 'braco_d': (-20, 0, -150), 'perna_e': (0, 0, 20), 'perna_d': (0, 0, -20), 'cabeca': (5, 0, 0)},
    'feliz': {'braco_e': (0, 0, 140), 'braco_d': (0, 0, -140), 'cabeca': (-10, 0, 8)},
})


class Capivara(Pato):
    PARTES = CAPI; POSES = POSES_CAPI; CENTRO = 7 * U
    CABECA = (0, 12 * U + 4.5 * U - 7 * U, 2 * U)     # ponto do rosto (para mirar closes)

    def __init__(self, tag='steve', escala=1.0):
        super().__init__(tag, escala)
        self.fechar = 0.45          # olhar sonolento padrao
