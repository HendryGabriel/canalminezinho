"""Elenco articulado (block_display) e objetos 3D do short 'O Vaso Vazio'.
Todos os rigs herdam de motor.Pato / motor.Capivara e animam todas as partes no mesmo tick
via datapack queda:aplica (cada instancia usa tag propria: 'ping', 'rei', 'riv1', 'riv2', 'riv3')."""
import os, sys, math
import numpy as np
_FERR_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ferramentas', 'animacao-no-jogo'))
if os.path.isdir(_FERR_REPO) and _FERR_REPO not in sys.path:
    sys.path.insert(0, _FERR_REPO)
import motor as M
from motor import U, EPS, T, S, R, rx, ry, rz, D2, quat, C

# ==============================================================================
# UTILITARIOS DE MULTI-PERSONAGEM E MODELOS RICOS
# ==============================================================================

def posar_varios(pares, dur=6):
    """Atualiza varios personagens no MESMO comando queda:aplica (zero defasagem entre atores).
    pares: lista de tuplas (personagem, dict_kwargs_de_posar) ou apenas instancias de Pato."""
    itens = []
    for item in pares:
        if isinstance(item, tuple):
            p, kw = item
        else:
            p, kw = item, {}
        pose = kw.get('pose')
        ori = kw.get('ori')
        d = kw.get('dur', dur)
        juntas = kw.get('juntas')
        if pose:
            p.pose = pose
        if ori is not None:
            p.ori = ori
        if not hasattr(p, '_ult'):
            p._ult = {}
        for nome, m in p._mats(juntas=juntas).items():
            if p._ult.get(nome) == m:
                continue
            p._ult[nome] = m
            itens.append('{t:"%s_%s",d:%d,m:%s}' % (p.tag, nome, d, m))
    for i in range(0, len(itens), 110):
        lote = itens[i:i + 110]
        M.mc.cmd('data modify storage queda:p lista set value [' + ','.join(lote) + ']')
        M.mc.cmd('function queda:aplica')


class ModeloRico(M.Modelo):
    """Estende motor.Modelo aceitando pecas com rotacao local opcional:
      - 3 itens: (bloco, canto, tamanho) -> caixa alinhada aos eixos (identico a motor.Modelo)
      - 4 itens: (bloco, pivo_base, tamanho, (yaw, pitch, roll)) -> base centrada em pivo_base crescendo +y
      - 5 itens: (bloco, pivo, tamanho, (yaw, pitch, roll), canto_relativo)
    """
    def _nbt(self):
        Rb = R(*self.ori)
        out = {}
        for nome, spec in self.partes.items():
            if len(spec) == 3:
                blk, c, t_ = spec
                Mat = T(*self.off) @ Rb @ T(*c)
                q = quat(Rb[:3, :3])
            else:
                blk, piv, t_, rot = spec[:4]
                crel = spec[4] if len(spec) >= 5 else (-t_[0] / 2.0, 0.0, -t_[2] / 2.0)
                Rl = R(*rot)
                Mat = T(*self.off) @ Rb @ T(*piv) @ Rl @ T(*crel)
                q = quat((Rb @ Rl)[:3, :3])
            pq = self._q.get(nome)
            if pq is not None and sum(a * b for a, b in zip(q, pq)) < 0:
                q = tuple(-v for v in q)
            self._q[nome] = q
            out[nome] = ('{translation:[%.4ff,%.4ff,%.4ff],left_rotation:[%.5ff,%.5ff,%.5ff,%.5ff],'
                         'scale:[%.4ff,%.4ff,%.4ff],right_rotation:[0f,0f,0f,1f]}' % (*Mat[:3, 3], *q, *t_))
        return out


# ==============================================================================
# 1. PING CAPIVARA — Mascote do canal vestindo tunica vinho e dourada
# ==============================================================================

CB_PING = (0, 11 * U, 0)
FZC_PING = 7 * U

PARTES_PING = dict(M.CAPI)
# Ombros ligeiramente mais largos e adiantados (±6.8*U, 9.0*U, 1.5*U) e bracos mais longos (9.6*U)
# para que as patinhas alcancem a frente do focinho sem nunca entrar dentro da cabeca (largura ±6.5*U)!
PIV_BE_PING = (6.8 * U, 9.0 * U, 1.5 * U)
PIV_BD_PING = (-6.8 * U, 9.0 * U, 1.5 * U)
PARTES_PING.update({
    'braco_e':      (M.PELO,              PIV_BE_PING, (3.1 * U, 7.8 * U, 3.1 * U), (-1.55 * U, -7.8 * U, -1.55 * U), 'braco_e'),
    'mao_e':        (M.ESC,               PIV_BE_PING, (3.2 * U, 2.0 * U, 3.2 * U), (-1.6 * U, -9.6 * U, -1.6 * U), 'braco_e'),
    'braco_d':      (M.PELO,              PIV_BD_PING, (3.1 * U, 7.8 * U, 3.1 * U), (-1.55 * U, -7.8 * U, -1.55 * U), 'braco_d'),
    'mao_d':        (M.ESC,               PIV_BD_PING, (3.2 * U, 2.0 * U, 3.2 * U), (-1.6 * U, -9.6 * U, -1.6 * U), 'braco_d'),
    # Tunica oriental vinho (red_terracotta) com faixa e gola dourada (yellow_terracotta)
    'tunica':       ('red_terracotta',    (0, 0, 0), (10.5 * U, 9.4 * U, 8.5 * U), (-5.25 * U, 0.6 * U, -4.25 * U), 'tronco'),
    'tunica_barra': ('red_terracotta',    (0, 0, 0), (10.7 * U, 1.8 * U, 8.7 * U), (-5.35 * U, -0.5 * U, -4.35 * U), 'tronco'),
    'faixa_ouro':   ('yellow_terracotta', (0, 0, 0), (10.8 * U, 1.6 * U, 8.8 * U), (-5.4 * U, 2.8 * U, -4.4 * U), 'tronco'),
    'broche_ouro':  ('gold_block',        (0, 0, 0), (2.4 * U, 2.0 * U, 0.6 * U),  (-1.2 * U, 2.6 * U, 4.15 * U), 'tronco'),
    'gola_ouro':    ('yellow_terracotta', (0, 0, 0), (6.8 * U, 1.2 * U, 8.7 * U),  (-3.4 * U, 9.0 * U, -4.35 * U), 'tronco'),
    'lapela_e':     ('yellow_terracotta', (0, 0, 0), (1.3 * U, 5.2 * U, 0.4 * U),  (0.6 * U, 4.2 * U, 4.12 * U), 'tronco'),
    'lapela_d':     ('yellow_terracotta', (0, 0, 0), (1.3 * U, 5.2 * U, 0.4 * U),  (-1.9 * U, 4.2 * U, 4.12 * U), 'tronco'),
    'manga_e':      ('red_terracotta',    PIV_BE_PING, (3.5 * U, 3.8 * U, 3.5 * U), (-1.75 * U, -3.6 * U, -1.75 * U), 'braco_e'),
    'punho_e':      ('yellow_terracotta', PIV_BE_PING, (3.6 * U, 0.8 * U, 3.6 * U), (-1.8 * U, -4.0 * U, -1.8 * U), 'braco_e'),
    'manga_d':      ('red_terracotta',    PIV_BD_PING, (3.5 * U, 3.8 * U, 3.5 * U), (-1.75 * U, -3.6 * U, -1.75 * U), 'braco_d'),
    'punho_d':      ('yellow_terracotta', PIV_BD_PING, (3.6 * U, 0.8 * U, 3.6 * U), (-1.8 * U, -4.0 * U, -1.8 * U), 'braco_d'),
    # Cantos do sorriso e bochechas suaves (escalam com self.sorriso)
    'sorr_e':       ('black_concrete',    CB_PING, (1.1 * U, 0.9 * U, 0.02), (1.9 * U, 1.45 * U, FZC_PING + 3.4 * U - 0.005), 'cabeca'),
    'sorr_d':       ('black_concrete',    CB_PING, (1.1 * U, 0.9 * U, 0.02), (-3.0 * U, 1.45 * U, FZC_PING + 3.4 * U - 0.005), 'cabeca'),
    'boch_e':       ('pink_terracotta',   CB_PING, (1.8 * U, 1.0 * U, 0.02), (2.7 * U, 4.3 * U, FZC_PING + 2 * EPS - 0.01), 'cabeca'),
    'boch_d':       ('pink_terracotta',   CB_PING, (1.8 * U, 1.0 * U, 0.02), (-4.5 * U, 4.3 * U, FZC_PING + 2 * EPS - 0.01), 'cabeca'),
})

POSES_PING = dict(M.POSES_CAPI)
POSES_PING.update({
    'pe':            {'braco_e': (-12, 0, 8), 'braco_d': (-12, 0, -8)},
    'recebe':        {'braco_e': (-70, 0, -14), 'braco_d': (-70, 0, 14), 'cabeca': (6, 0, 0)},
    'segura_vaso':   {'braco_e': (-60, 0, -13), 'braco_d': (-60, 0, 13), 'cabeca': (2, 0, 0)},
    'agacha_planta': {'tronco': (14, 0, 0), 'perna_e': (-48, 0, 8), 'perna_d': (-48, 0, -8),
                      'braco_e': (-62, 0, -10), 'braco_d': (-66, 0, 10), 'cabeca': (10, 0, 0)},
    'rega':          {'braco_d': (-72, 0, -10), 'braco_e': (-34, 0, 8), 'cabeca': (8, -6, 0)},
    'apoia_rosto':   {'tronco': (8, 0, 0), 'braco_e': (-64, 0, -10), 'braco_d': (-64, 0, 10),
                      'cabeca': (8, 0, 5)},
    'triste_vaso':   {'braco_e': (-58, 0, -13), 'braco_d': (-58, 0, 13), 'cabeca': (12, 0, 0),
                      'perna_e': (0, 0, 2), 'perna_d': (0, 0, -2)},
    'anda1':         {'braco_e': (32, 0, 6), 'braco_d': (-32, 0, -6), 'perna_e': (-32, 0, 0), 'perna_d': (32, 0, 0)},
    'anda2':         {'braco_e': (-32, 0, 6), 'braco_d': (32, 0, -6), 'perna_e': (32, 0, 0), 'perna_d': (-32, 0, 0)},
    'anda_vaso1':    {'braco_e': (-60, 0, -13), 'braco_d': (-60, 0, 13), 'perna_e': (-28, 0, 0), 'perna_d': (28, 0, 0), 'cabeca': (4, 0, 0)},
    'anda_vaso2':    {'braco_e': (-60, 0, -13), 'braco_d': (-60, 0, 13), 'perna_e': (28, 0, 0), 'perna_d': (-28, 0, 0), 'cabeca': (4, 0, 0)},
    'vencedor':      {'braco_d': (-158, 0, -24), 'braco_e': (-52, 0, -12), 'cabeca': (-8, 0, 5)},
    'coroado':       {'braco_e': (-60, 0, -13), 'braco_d': (-60, 0, 13), 'cabeca': (-4, 0, 0)},
    'sentado_trono': {'perna_e': (-80, 0, 8), 'perna_d': (-80, 0, -8),
                      'braco_e': (-36, 0, 14), 'braco_d': (-36, 0, -14), 'cabeca': (-3, 0, 0)},
})


class PingCapivara(M.Capivara):
    PARTES = PARTES_PING
    POSES = POSES_PING
    CENTRO = 7 * U
    ALT_CHAO = 13.4 * U     # y do centro acima do piso para os pes tocarem o chao (escala 1.0)
    CABECA = M.Capivara.CABECA
    sorriso = 0.0

    def __init__(self, tag='ping', escala=1.0):
        super().__init__(tag, escala)
        self.partes = dict(PARTES_PING)
        self.poses = POSES_PING
        self.fechar = 0.25          # olhar doce e vivo padrao
        self.sorriso = 0.0

    def _rosto(self, nome, c, t):
        s = max(0.0, min(1.0, self.sorriso))
        if nome.startswith('sorr_'):
            if s < 0.05:
                return (c[0], c[1], c[2] - 0.03), (0.001, 0.001, 0.001)
            h = t[1] * (0.4 + 0.8 * s)
            return (c[0], c[1] + 0.15 * s * t[1], c[2]), (t[0] * (0.6 + 0.4 * s), h, t[2])
        if nome.startswith('boch_'):
            if s < 0.15:
                return (c[0], c[1], c[2] - 0.03), (0.001, 0.001, 0.001)
            k = (s - 0.15) / 0.85
            return c, (t[0] * k, t[1] * k, t[2])
        if nome == 'boca' and s > 0.05:
            w = t[0] * (1.0 + 0.35 * s)
            h = t[1] * (0.85 + 1.4 * self.boca_ab)
            dx = (w - t[0]) * 0.5
            dy = 0.25 * s * t[1] - 0.5 * self.boca_ab * t[1]
            return (c[0] - dx, c[1] + dy, c[2]), (w, h, t[2])
        if nome.startswith('sobr') and s > 0.1 and self.brava < 0.1:
            return (c[0], c[1] + 0.35 * s * t[1], c[2]), t
        return super()._rosto(nome, c, t)


# ==============================================================================
# HELPER DE ROSTO HUMANO (usado por Rei e Rival)
# ==============================================================================

CAB_H = (0, 12 * U, 0)
FZ_H = 4 * U


def _pxh(col, lin, w=1.0, h=1.0, dz=EPS):
    """Placa no rosto humano 8x8 em U: coluna 0 = esquerda de quem olha de frente."""
    x = 4 * U - (col + w) * U
    y = (8 - lin - h) * U
    return (x, y, FZ_H + dz - 0.01), (w * U, h * U, 0.012)


# ==============================================================================
# 2. REI — Idoso majestoso com Tunica Imperial, Barba Longa e Coroa Mianliu
# ==============================================================================

def _construir_partes_rei():
    PELE = 'white_terracotta'
    TUN = 'cyan_terracotta'
    TUN2 = 'gray_concrete'
    OURO = 'gold_block'
    AM = 'yellow_concrete'
    BCO = 'white_concrete'
    PRATA = 'light_gray_concrete'

    p = {
        # Tronco e tunica imperial longa com bordados dourados
        'tronco':        (TUN,  (0, 0, 0), (8.6 * U, 12 * U, 4.8 * U),   (-4.3 * U, 0, -2.4 * U), 'tronco'),
        'tunica_saia':   (TUN,  (0, 0, 0), (9.2 * U, 4.4 * U, 5.2 * U),  (-4.6 * U, -4.0 * U, -2.6 * U), 'tronco'),
        'painel_frente': (TUN2, (0, 0, 0), (4.2 * U, 15.2 * U, 0.35 * U), (-2.1 * U, -3.8 * U, 2.35 * U), 'tronco'),
        'bordado_v':     (AM,   (0, 0, 0), (1.4 * U, 12.0 * U, 0.4 * U), (-0.7 * U, -3.2 * U, 2.52 * U), 'tronco'),
        'cinto_ouro':    (OURO, (0, 0, 0), (9.4 * U, 1.6 * U, 5.4 * U),  (-4.7 * U, 2.6 * U, -2.7 * U), 'tronco'),
        'fivela_jade':   ('emerald_block', (0, 0, 0), (2.0 * U, 1.8 * U, 0.5 * U), (-1.0 * U, 2.5 * U, 2.55 * U), 'tronco'),
        'gola_ouro':     (OURO, (0, 0, 0), (6.4 * U, 1.3 * U, 5.2 * U),  (-3.2 * U, 10.8 * U, -2.6 * U), 'tronco'),
        'lapela_e':      (OURO, (0, 0, 0), (1.2 * U, 7.0 * U, 0.4 * U),  (0.8 * U, 4.2 * U, 2.38 * U), 'tronco'),
        'lapela_d':      (OURO, (0, 0, 0), (1.2 * U, 7.0 * U, 0.4 * U),  (-2.0 * U, 4.2 * U, 2.38 * U), 'tronco'),
        'ombr_e':        (OURO, (0, 0, 0), (2.2 * U, 0.9 * U, 5.2 * U),  (3.6 * U, 11.2 * U, -2.6 * U), 'tronco'),
        'ombr_d':        (OURO, (0, 0, 0), (2.2 * U, 0.9 * U, 5.2 * U),  (-5.8 * U, 11.2 * U, -2.6 * U), 'tronco'),

        # Bracos com mangas largas imperiais
        'manga_alta_e':  (TUN,  (6.2 * U, 10.2 * U, 0), (4.4 * U, 5.5 * U, 4.6 * U), (-2.2 * U, -4.5 * U, -2.3 * U), 'braco_e'),
        'manga_larga_e': (TUN2, (6.2 * U, 10.2 * U, 0), (4.8 * U, 4.6 * U, 5.4 * U), (-2.4 * U, -8.8 * U, -2.7 * U), 'braco_e'),
        'punho_ouro_e':  (OURO, (6.2 * U, 10.2 * U, 0), (4.9 * U, 0.9 * U, 5.5 * U), (-2.45 * U, -8.9 * U, -2.75 * U), 'braco_e'),
        'mao_e':         (PELE, (6.2 * U, 10.2 * U, 0), (3.4 * U, 2.2 * U, 3.4 * U), (-1.7 * U, -10.6 * U, -1.7 * U), 'braco_e'),

        'manga_alta_d':  (TUN,  (-6.2 * U, 10.2 * U, 0), (4.4 * U, 5.5 * U, 4.6 * U), (-2.2 * U, -4.5 * U, -2.3 * U), 'braco_d'),
        'manga_larga_d': (TUN2, (-6.2 * U, 10.2 * U, 0), (4.8 * U, 4.6 * U, 5.4 * U), (-2.4 * U, -8.8 * U, -2.7 * U), 'braco_d'),
        'punho_ouro_d':  (OURO, (-6.2 * U, 10.2 * U, 0), (4.9 * U, 0.9 * U, 5.5 * U), (-2.45 * U, -8.9 * U, -2.75 * U), 'braco_d'),
        'mao_d':         (PELE, (-6.2 * U, 10.2 * U, 0), (3.4 * U, 2.2 * U, 3.4 * U), (-1.7 * U, -10.6 * U, -1.7 * U), 'braco_d'),

        # Pernas cobertas pela tunica longa + canelas articuladas (para sentar com joelho 90°) + botas imperiais
        'perna_e':       (TUN2, (2.2 * U, 0, 0),  (4.3 * U, 9.6 * U, 4.5 * U),  (-2.15 * U, -9.6 * U, -2.25 * U), 'perna_e'),
        'canela_e':      (TUN2, (2.2 * U, 0, 0),  (0.1 * U, 0.1 * U, 0.1 * U),  (-0.05 * U, -5.0 * U, -0.05 * U), 'perna_e'),
        'barra_perna_e': (OURO, (2.2 * U, 0, 0),  (4.4 * U, 0.9 * U, 4.6 * U),  (-2.2 * U, -9.8 * U, -2.3 * U), 'perna_e'),
        'pe_e':          ('black_concrete', (2.2 * U, 0, 0), (4.2 * U, 2.2 * U, 4.8 * U), (-2.1 * U, -12.0 * U, -2.1 * U), 'perna_e'),

        'perna_d':       (TUN2, (-2.2 * U, 0, 0), (4.3 * U, 9.6 * U, 4.5 * U),  (-2.15 * U, -9.6 * U, -2.25 * U), 'perna_d'),
        'canela_d':      (TUN2, (-2.2 * U, 0, 0), (0.1 * U, 0.1 * U, 0.1 * U),  (-0.05 * U, -5.0 * U, -0.05 * U), 'perna_d'),
        'barra_perna_d': (OURO, (-2.2 * U, 0, 0), (4.4 * U, 0.9 * U, 4.6 * U),  (-2.2 * U, -9.8 * U, -2.3 * U), 'perna_d'),
        'pe_d':          ('black_concrete', (-2.2 * U, 0, 0), (4.2 * U, 2.2 * U, 4.8 * U), (-2.1 * U, -12.0 * U, -2.1 * U), 'perna_d'),

        # Cabeca e cabelos brancos
        'cabeca':        (PELE,  CAB_H, (8 * U, 8 * U, 8 * U),       (-4 * U, 0, -4 * U), 'cabeca'),
        'cabelo_topo':   (PRATA, CAB_H, (8.3 * U, 1.8 * U, 8.3 * U), (-4.15 * U, 6.4 * U, -4.15 * U), 'cabeca'),
        'cabelo_nuca':   (BCO,   CAB_H, (8.3 * U, 7.2 * U, 0.5 * U), (-4.15 * U, 0.8 * U, -4.35 * U), 'cabeca'),
        'cabelo_lat_e':  (BCO,   CAB_H, (0.4 * U, 5.5 * U, 5.5 * U), (3.95 * U, 2.0 * U, -3.5 * U), 'cabeca'),
        'cabelo_lat_d':  (BCO,   CAB_H, (0.4 * U, 5.5 * U, 5.5 * U), (-4.35 * U, 2.0 * U, -3.5 * U), 'cabeca'),

        # Bigode e barba branca longa em 3 camadas descendo na frente do peito
        'bigode_c':      (BCO, CAB_H, (4.8 * U, 0.9 * U, 0.5 * U), (-2.4 * U, 1.85 * U, FZ_H), 'cabeca'),
        'bigode_e':      (BCO, CAB_H, (1.1 * U, 1.8 * U, 0.45 * U), (1.6 * U, 0.6 * U, FZ_H), 'cabeca'),
        'bigode_d':      (BCO, CAB_H, (1.1 * U, 1.8 * U, 0.45 * U), (-2.7 * U, 0.6 * U, FZ_H), 'cabeca'),
        'barba_1':       (BCO, CAB_H, (5.6 * U, 2.6 * U, 1.2 * U), (-2.8 * U, -1.8 * U, FZ_H - 0.5 * U), 'cabeca'),
        'barba_2':       (BCO, CAB_H, (4.6 * U, 3.0 * U, 0.9 * U), (-2.3 * U, -4.5 * U, FZ_H - 0.3 * U), 'cabeca'),
        'barba_3':       (BCO, CAB_H, (3.2 * U, 2.8 * U, 0.7 * U), (-1.6 * U, -7.0 * U, FZ_H - 0.2 * U), 'cabeca'),
    }

    # Rosto detalhado
    for nome, blk, ct in [
        ('olho_bco_e', BCO,              _pxh(1.0, 4.0, 1.0, 1.0)),
        ('olho_e',     'black_concrete', _pxh(2.0, 4.0, 1.0, 1.0)),
        ('olho_d',     'black_concrete', _pxh(5.0, 4.0, 1.0, 1.0)),
        ('olho_bco_d', BCO,              _pxh(6.0, 4.0, 1.0, 1.0)),
        ('brilho_e',   BCO,              _pxh(1.9, 3.9, 0.35, 0.35, dz=2 * EPS)),
        ('brilho_d',   BCO,              _pxh(4.9, 3.9, 0.35, 0.35, dz=2 * EPS)),
        ('nariz',      'light_gray_terracotta', _pxh(3.2, 4.6, 1.6, 1.1, dz=2 * EPS)),
        ('boca',       'black_concrete', _pxh(3.0, 6.2, 2.0, 0.7, dz=3 * EPS)),
        ('sorr_e',     'black_concrete', _pxh(2.3, 5.9, 0.7, 0.6, dz=3 * EPS)),
        ('sorr_d',     'black_concrete', _pxh(5.0, 5.9, 0.7, 0.6, dz=3 * EPS)),
        ('palp_e',     PELE,             _pxh(0.95, 3.95, 2.1, 1.1, dz=3 * EPS)),
        ('palp_d',     PELE,             _pxh(4.95, 3.95, 2.1, 1.1, dz=3 * EPS)),
        # Sobrancelhas brancas compridas de sabio
        ('sobr_e',     BCO,              _pxh(0.4, 2.85, 2.8, 0.85, dz=4 * EPS)),
        ('sobr_d',     BCO,              _pxh(4.8, 2.85, 2.8, 0.85, dz=4 * EPS)),
    ]:
        c, t = ct
        p[nome] = (blk, CAB_H, t, c, 'cabeca')

    # Coroa Imperial Mianliu (todas as pecas prefixadas com 'coroa_' para liga/desliga limpo)
    p['coroa_aro']    = (OURO, CAB_H, (8.6 * U, 1.1 * U, 8.6 * U),  (-4.3 * U, 7.6 * U, -4.3 * U), 'cabeca')
    p['coroa_base']   = ('black_concrete', CAB_H, (6.4 * U, 2.4 * U, 6.4 * U), (-3.2 * U, 8.5 * U, -3.2 * U), 'cabeca')
    p['coroa_jade']   = ('emerald_block',  CAB_H, (1.4 * U, 1.2 * U, 0.5 * U), (-0.7 * U, 8.9 * U, 3.0 * U), 'cabeca')
    p['coroa_pino']   = (OURO, CAB_H, (9.8 * U, 0.45 * U, 0.45 * U), (-4.9 * U, 9.5 * U, -0.22 * U), 'cabeca')
    p['coroa_tabua']  = ('black_concrete', CAB_H, (8.8 * U, 0.65 * U, 12.2 * U), (-4.4 * U, 10.8 * U, -6.1 * U), 'cabeca')
    p['coroa_friso']  = (OURO, CAB_H, (9.0 * U, 0.28 * U, 12.4 * U), (-4.5 * U, 11.45 * U, -6.2 * U), 'cabeca')

    # Fileiras de contas pendentes (Liu) na frente (+z) e atras (-z)
    xs_contas = [-3.4 * U, -1.7 * U, 0.0, 1.7 * U, 3.4 * U]
    for idx, xk in enumerate(xs_contas):
        for lado, zk in (('f', 5.85 * U), ('t', -6.05 * U)):
            p[f'coroa_cnt1_{lado}{idx}'] = (OURO, CAB_H, (0.38 * U, 0.75 * U, 0.38 * U), (xk - 0.19 * U, 10.0 * U, zk), 'cabeca')
            p[f'coroa_cnt2_{lado}{idx}'] = (BCO,  CAB_H, (0.36 * U, 0.85 * U, 0.36 * U), (xk - 0.18 * U, 9.05 * U, zk), 'cabeca')
            p[f'coroa_cnt3_{lado}{idx}'] = (OURO, CAB_H, (0.38 * U, 0.75 * U, 0.38 * U), (xk - 0.19 * U, 8.2 * U, zk), 'cabeca')

    return p


PARTES_REI = _construir_partes_rei()

POSES_REI = dict(M.POSES_STEVE)
POSES_REI.update({
    'pe':           {'braco_e': (0, 0, 4), 'braco_d': (0, 0, -4)},
    'entrega':      {'braco_d': (-78, 0, 12), 'braco_e': (10, 0, 6), 'cabeca': (10, 0, 0)},
    'sentado':      {'perna_e': (-90, 0, 4), 'perna_d': (-90, 0, -4),
                     'braco_d': (-44, 0, -10), 'braco_e': (-44, 0, 10), 'cabeca': (6, 0, 0)},
    'maos_costas':  {'braco_e': (30, 0, -28), 'braco_d': (30, 0, 28), 'cabeca': (8, 0, 0)},
    'anda1':        {'braco_e': (22, 0, 4), 'braco_d': (-22, 0, -4), 'perna_e': (-24, 0, 0), 'perna_d': (24, 0, 0)},
    'anda2':        {'braco_e': (-22, 0, 4), 'braco_d': (22, 0, -4), 'perna_e': (24, 0, 0), 'perna_d': (-24, 0, 0)},
    'anda_costas1': {'braco_e': (30, 0, -28), 'braco_d': (30, 0, 28), 'perna_e': (-20, 0, 0), 'perna_d': (20, 0, 0), 'cabeca': (8, 0, 0)},
    'anda_costas2': {'braco_e': (30, 0, -28), 'braco_d': (30, 0, 28), 'perna_e': (20, 0, 0), 'perna_d': (-20, 0, 0), 'cabeca': (8, 0, 0)},
    'anuncia':      {'braco_e': (-142, 0, 20), 'braco_d': (14, 0, -8), 'cabeca': (-4, -10, 0)},
    'hashi':        {'braco_d': (-74, 0, 16), 'braco_e': (-56, 0, -16), 'cabeca': (20, 0, 0)},
    'coroando':     {'braco_e': (-118, 0, -16), 'braco_d': (-118, 0, 16), 'cabeca': (12, 0, 0)},
    'ombro':        {'braco_e': (-54, 0, 14), 'braco_d': (16, 0, -8), 'cabeca': (10, -10, 0)},
})


class Rei(M.Pato):
    PARTES = PARTES_REI
    POSES = POSES_REI
    CENTRO = 6 * U
    ALT_CHAO = 18 * U * 1.18   # 1.2744m na escala padrao 1.18 para as botas tocarem exatamente o piso!
    CABECA = (0, 10 * U, 2 * U)
    sorriso = 0.0

    def __init__(self, tag='rei', escala=1.18, com_coroa=True):
        super().__init__(tag, escala)
        self.ALT_CHAO = 18 * U * escala
        self.partes = dict(PARTES_REI)
        self.poses = POSES_REI
        self.com_coroa = com_coroa
        self.sorriso = 0.0

    def set_coroa(self, ativo, dur=1):
        """Liga ou desliga a Coroa Imperial ao vivo no mesmo tick."""
        self.com_coroa = bool(ativo)
        if hasattr(self, '_ult') and self._ult:
            self.posar(dur=dur)

    def _rosto(self, nome, c, t):
        s = max(0.0, min(1.0, self.sorriso))
        if nome.startswith('coroa_') and not self.com_coroa:
            return c, (0.0, 0.0, 0.0)
        if self.pose == 'sentado':
            # Joelho dobrado em 90 graus reais sobre o assento (y=71.50) com botas pousadas no tapete (y=71.00)!
            if nome == 'tunica_saia':
                return (-4.6 * U, -1.6 * U, -2.6 * U), (9.2 * U, 2.0 * U, 5.2 * U)
            if nome == 'painel_frente':
                return (-2.1 * U, -1.5 * U, 2.35 * U), (4.2 * U, 12.9 * U, 0.35 * U)
            if nome == 'bordado_v':
                return (-0.7 * U, -1.2 * U, 2.52 * U), (1.4 * U, 10.0 * U, 0.4 * U)
            if nome in ('perna_e', 'perna_d'):
                return (-2.15 * U, -8.8 * U, -2.0 * U), (4.3 * U, 8.8 * U, 4.1 * U)
            if nome in ('canela_e', 'canela_d'):
                return (-2.1 * U, -9.2 * U, -7.8 * U), (4.2 * U, 3.8 * U, 6.2 * U)
            if nome in ('barra_perna_e', 'barra_perna_d'):
                return (-2.2 * U, -9.3 * U, -7.9 * U), (4.4 * U, 4.0 * U, 0.9 * U)
            if nome in ('pe_e', 'pe_d'):
                return (-2.1 * U, -10.1 * U, -9.25 * U), (4.2 * U, 4.8 * U, 1.9 * U)
        if nome.startswith('sorr_'):
            if s < 0.05:
                return (c[0], c[1], c[2] - 0.03), (0.001, 0.001, 0.001)
            return (c[0], c[1] + 0.2 * s * t[1], c[2]), (t[0] * (0.6 + 0.4 * s), t[1] * (0.5 + 0.7 * s), t[2])
        if nome == 'boca' and s > 0.05:
            w = t[0] * (1.0 + 0.35 * s)
            dx = (w - t[0]) * 0.5
            return (c[0] - dx, c[1] + 0.2 * s * t[1], c[2]), (w, t[1] * (0.85 + 1.2 * self.boca_ab), t[2])
        if nome.startswith('sobr') and s > 0.1 and self.brava < 0.1:
            return (c[0], c[1] + 0.35 * s * t[1], c[2]), t
        return super()._rosto(nome, c, t)


# ==============================================================================
# 3. RIVAL — Jovem concorrente articulado com coque tradicional e tunica colorida
# ==============================================================================

def _construir_partes_rival(cor='green_terracotta'):
    PELE = 'white_terracotta'
    CAB = 'black_concrete'
    FAIXA = 'yellow_terracotta'
    CALCA = 'gray_concrete'

    p = {
        'tronco':       (cor,   (0, 0, 0), (8.2 * U, 12 * U, 4.2 * U),   (-4.1 * U, 0, -2.1 * U), 'tronco'),
        'tunica_barra': (cor,   (0, 0, 0), (8.5 * U, 2.4 * U, 4.5 * U),  (-4.25 * U, -2.0 * U, -2.25 * U), 'tronco'),
        'faixa':        (FAIXA, (0, 0, 0), (8.6 * U, 1.5 * U, 4.6 * U),  (-4.3 * U, 2.8 * U, -2.3 * U), 'tronco'),
        'gola_e':       ('light_gray_terracotta', (0, 0, 0), (1.1 * U, 5.5 * U, 0.35 * U), (0.5 * U, 6.2 * U, 1.95 * U), 'tronco'),
        'gola_d':       ('light_gray_terracotta', (0, 0, 0), (1.1 * U, 5.5 * U, 0.35 * U), (-1.6 * U, 6.2 * U, 1.95 * U), 'tronco'),

        'manga_e':      (cor,  (6 * U, 10 * U, 0), (4.2 * U, 5.0 * U, 4.2 * U), (-2.1 * U, -4.0 * U, -2.1 * U), 'braco_e'),
        'braco_e':      (PELE, (6 * U, 10 * U, 0), (3.6 * U, 6.2 * U, 3.6 * U), (-1.8 * U, -10.0 * U, -1.8 * U), 'braco_e'),
        'manga_d':      (cor,  (-6 * U, 10 * U, 0), (4.2 * U, 5.0 * U, 4.2 * U), (-2.1 * U, -4.0 * U, -2.1 * U), 'braco_d'),
        'braco_d':      (PELE, (-6 * U, 10 * U, 0), (3.6 * U, 6.2 * U, 3.6 * U), (-1.8 * U, -10.0 * U, -1.8 * U), 'braco_d'),

        'perna_e':      (CALCA, (2 * U, 0, 0),  (4.0 * U, 10 * U, 4.0 * U), (-2 * U, -10 * U, -2 * U), 'perna_e'),
        'pe_e':         (CAB,   (2 * U, 0, 0),  (4.1 * U, 2 * U, 4.4 * U),  (-2.05 * U, -12 * U, -2.05 * U), 'perna_e'),
        'perna_d':      (CALCA, (-2 * U, 0, 0), (4.0 * U, 10 * U, 4.0 * U), (-2 * U, -10 * U, -2 * U), 'perna_d'),
        'pe_d':         (CAB,   (-2 * U, 0, 0), (4.1 * U, 2 * U, 4.4 * U),  (-2.05 * U, -12 * U, -2.05 * U), 'perna_d'),

        # Cabeca, cabelo preto e coque tradicional oriental bem visivel de frente e de costas
        'cabeca':       (PELE, CAB_H, (8 * U, 8 * U, 8 * U),       (-4 * U, 0, -4 * U), 'cabeca'),
        'cabelo_topo':  (CAB,  CAB_H, (8.4 * U, 2.2 * U, 8.4 * U), (-4.2 * U, 6.0 * U, -4.2 * U), 'cabeca'),
        'cabelo_nuca':  (CAB,  CAB_H, (8.4 * U, 6.8 * U, 0.6 * U), (-4.2 * U, 1.2 * U, -4.4 * U), 'cabeca'),
        'cabelo_lat_e': (CAB,  CAB_H, (0.45 * U, 5.2 * U, 6.8 * U), (3.95 * U, 2.6 * U, -4.1 * U), 'cabeca'),
        'cabelo_lat_d': (CAB,  CAB_H, (0.45 * U, 5.2 * U, 6.8 * U), (-4.4 * U, 2.6 * U, -4.1 * U), 'cabeca'),
        'coque_base':   (FAIXA, CAB_H, (3.4 * U, 0.8 * U, 3.4 * U), (-1.7 * U, 8.1 * U, -2.2 * U), 'cabeca'),
        'coque':        (CAB,  CAB_H, (3.2 * U, 2.4 * U, 3.2 * U), (-1.6 * U, 8.7 * U, -2.1 * U), 'cabeca'),
        'grampo_coque': ('gold_block', CAB_H, (4.8 * U, 0.35 * U, 0.35 * U), (-2.4 * U, 9.6 * U, -0.6 * U), 'cabeca'),
    }

    for nome, blk, ct in [
        ('cab_franja_e', CAB, _pxh(0.0, 2.0, 1.2, 1.4)),
        ('cab_franja_d', CAB, _pxh(6.8, 2.0, 1.2, 1.4)),
        ('olho_bco_e', 'white_concrete', _pxh(1.0, 4.0, 1.0, 1.0)),
        ('olho_e',     CAB,              _pxh(2.0, 4.0, 1.0, 1.0)),
        ('olho_d',     CAB,              _pxh(5.0, 4.0, 1.0, 1.0)),
        ('olho_bco_d', 'white_concrete', _pxh(6.0, 4.0, 1.0, 1.0)),
        ('brilho_e',   'white_concrete', _pxh(1.9, 3.9, 0.35, 0.35, dz=2 * EPS)),
        ('brilho_d',   'white_concrete', _pxh(4.9, 3.9, 0.35, 0.35, dz=2 * EPS)),
        ('nariz',      'light_gray_terracotta', _pxh(3.3, 4.9, 1.4, 0.9, dz=2 * EPS)),
        ('boca',       'black_concrete', _pxh(3.0, 6.2, 2.0, 0.8, dz=2 * EPS)),
        ('sorr_e',     'black_concrete', _pxh(2.3, 5.9, 0.7, 0.6, dz=2 * EPS)),
        ('sorr_d',     'black_concrete', _pxh(5.0, 5.9, 0.7, 0.6, dz=2 * EPS)),
        ('palp_e',     PELE,             _pxh(0.95, 3.95, 2.1, 1.1, dz=3 * EPS)),
        ('palp_d',     PELE,             _pxh(4.95, 3.95, 2.1, 1.1, dz=3 * EPS)),
        ('sobr_e',     CAB,              _pxh(0.9, 3.0, 2.2, 0.75, dz=3 * EPS)),
        ('sobr_d',     CAB,              _pxh(4.9, 3.0, 2.2, 0.75, dz=3 * EPS)),
    ]:
        c, t = ct
        p[nome] = (blk, CAB_H, t, c, 'cabeca')

    return p


POSES_RIVAL = dict(M.POSES_STEVE)
POSES_RIVAL.update({
    'pe':           {'braco_e': (0, 0, 5), 'braco_d': (0, 0, -5)},
    'recebe':       {'braco_e': (-75, 0, -25), 'braco_d': (-75, 0, 25), 'cabeca': (8, 0, 0)},
    'segura_vaso':  {'braco_e': (-68, 0, -22), 'braco_d': (-68, 0, 22), 'cabeca': (0, 0, 0)},
    'orgulhoso':    {'tronco': (-6, 0, 0), 'cabeca': (-14, 0, 4),
                     'braco_e': (-72, 0, -22), 'braco_d': (-72, 0, 22),
                     'perna_e': (4, 0, 4), 'perna_d': (4, 0, -4)},
    'chocado':      {'braco_e': (-35, 0, 62), 'braco_d': (-35, 0, -62), 'cabeca': (-8, 0, 0),
                     'perna_e': (0, 0, 7), 'perna_d': (0, 0, -7)},
    # Mao direita exatamente atras da nuca/coque (z negativo) cocando envergonhado
    'coca_cabeca1': {'braco_d': (146, 0, 30), 'braco_e': (8, 0, 6), 'cabeca': (16, -6, 6)},
    'coca_cabeca2': {'braco_d': (158, 0, 36), 'braco_e': (8, 0, 6), 'cabeca': (19, -2, 4)},
    'anda1':        {'braco_e': (28, 0, 5), 'braco_d': (-28, 0, -5), 'perna_e': (-28, 0, 0), 'perna_d': (28, 0, 0)},
    'anda2':        {'braco_e': (-28, 0, 5), 'braco_d': (28, 0, -5), 'perna_e': (28, 0, 0), 'perna_d': (-28, 0, 0)},
})


class Rival(M.Pato):
    POSES = POSES_RIVAL
    CENTRO = 6 * U
    ALT_CHAO = 18 * U
    CABECA = (0, 10 * U, 2 * U)
    sorriso = 0.0

    def __init__(self, tag='riv1', cor='green_terracotta', escala=1.0):
        self.cor = cor
        self.PARTES = _construir_partes_rival(cor)
        super().__init__(tag, escala)
        self.poses = POSES_RIVAL
        self.sorriso = 0.0

    def _rosto(self, nome, c, t):
        s = max(0.0, min(1.0, self.sorriso))
        if nome.startswith('sorr_'):
            if s < 0.05:
                return (c[0], c[1], c[2] - 0.03), (0.001, 0.001, 0.001)
            return (c[0], c[1] + 0.2 * s * t[1], c[2]), (t[0] * (0.6 + 0.4 * s), t[1] * (0.5 + 0.7 * s), t[2])
        if nome == 'boca' and s > 0.05:
            w = t[0] * (1.0 + 0.35 * s)
            dx = (w - t[0]) * 0.5
            return (c[0] - dx, c[1] + 0.2 * s * t[1], c[2]), (w, t[1] * (0.85 + 1.4 * self.boca_ab), t[2])
        return super()._rosto(nome, c, t)


# ==============================================================================
# 4. MODELOS 3D DETALHADOS (motor.Modelo / ModeloRico)
# ==============================================================================

PALETAS_FLORES = {
    'flor_rosa': ('magenta_concrete', 'pink_concrete', 'yellow_concrete', 'gold_block'),
    'flor_ouro': ('red_concrete', 'orange_concrete', 'yellow_concrete', 'shroomlight'),
    'flor_azul': ('purple_concrete', 'light_blue_concrete', 'cyan_concrete', 'yellow_concrete'),
}


def criar_vaso(tag='vaso', tipo='vazio'):
    """Vaso de ceramica oriental (y=0 na base, ~0.35m de altura do vaso).
    tipo: 'vazio' | 'semente' | 'flor_rosa' | 'flor_ouro' | 'flor_azul'"""
    p = {
        # Base e corpo arredondado em ceramica
        'pe':         ('brown_terracotta', (-0.13, 0.00, -0.13), (0.26, 0.04, 0.26)),
        'corpo_b':    ('terracotta',       (-0.16, 0.04, -0.16), (0.32, 0.10, 0.32)),
        'corpo_b45':  ('terracotta',       (0.0, 0.04, 0.0),     (0.30, 0.10, 0.30), (45, 0, 0)),
        'corpo_m':    ('terracotta',       (-0.185, 0.13, -0.185), (0.37, 0.13, 0.37)),
        'corpo_m45':  ('terracotta',       (0.0, 0.13, 0.0),     (0.35, 0.13, 0.35), (45, 0, 0)),
        'pescoco':    ('brown_terracotta', (-0.16, 0.26, -0.16), (0.32, 0.04, 0.32)),
        # Borda larga superior em tijolo/ceramica com cavidade real para a terra
        'borda_n':    ('bricks',           (-0.21, 0.29, -0.21), (0.42, 0.06, 0.06)),
        'borda_s':    ('bricks',           (-0.21, 0.29,  0.15), (0.42, 0.06, 0.06)),
        'borda_l':    ('bricks',           ( 0.15, 0.29, -0.15), (0.06, 0.06, 0.30)),
        'borda_o':    ('bricks',           (-0.21, 0.29, -0.15), (0.06, 0.06, 0.30)),
        'anel_ouro':  ('yellow_terracotta', (-0.195, 0.20, -0.195), (0.39, 0.025, 0.39)),
        # Terra escura e fertil dentro do vaso
        'terra_base': ('mud',              (-0.155, 0.27, -0.155), (0.31, 0.055, 0.31)),
        'terra_gr1':  ('rooted_dirt',      (-0.10, 0.315, -0.09),  (0.09, 0.02, 0.08)),
        'terra_gr2':  ('rooted_dirt',      ( 0.02, 0.315,  0.02),  (0.08, 0.02, 0.09)),
        'terra_gr3':  ('mud',              (-0.04, 0.318, -0.02),  (0.10, 0.018, 0.09)),
    }

    if tipo == 'semente':
        p['semente_casca'] = ('lime_terracotta', (0.0, 0.328, 0.0), (0.075, 0.055, 0.095), (15, 10, 0))
        p['semente_ponta'] = ('lime_concrete',   (0.0, 0.365, 0.01), (0.045, 0.03, 0.055), (15, -12, 0))

    elif tipo in PALETAS_FLORES:
        c_ext, c_int, c_mio, c_luz = PALETAS_FLORES[tipo]
        # Caule verde robusto e ligeiramente sinuoso subindo ate ~0.92m
        p['caule_1'] = ('green_concrete', (0.0, 0.32, 0.0),   (0.065, 0.22, 0.065), (0, 4, -3))
        p['caule_2'] = ('green_concrete', (0.01, 0.52, 0.01), (0.060, 0.22, 0.060), (0, -5, 4))
        p['caule_3'] = ('lime_concrete',  (-0.01, 0.72, 0.0), (0.052, 0.20, 0.052), (0, 6, 0))

        # 6 folhas largas e vibrantes abrindo radialmente
        for i, ang_y in enumerate((0, 60, 120, 180, 240, 300)):
            alt = 0.42 if i % 2 == 0 else 0.58
            cor_f = 'lime_concrete' if i % 2 == 0 else 'green_concrete'
            comp = 0.28 if i % 2 == 0 else 0.24
            p[f'folha_{i}'] = (cor_f, (0.0, alt, 0.0), (0.11, comp, 0.03), (ang_y, 58, 0))

        # Grande corola principal no topo (8 petalas externas + 6 internas + miolo luminoso)
        topo = (0.0, 0.90, 0.02)
        for i in range(8):
            ay = i * 45
            p[f'pet_ext_{i}'] = (c_ext, topo, (0.13, 0.25, 0.035), (ay, 64, 0))
        for i in range(6):
            ay = i * 60 + 22
            p[f'pet_int_{i}'] = (c_int, (0.0, 0.92, 0.02), (0.11, 0.19, 0.035), (ay, 42, 0))
        p['miolo_base'] = (c_mio, (-0.08, 0.89, -0.06), (0.16, 0.09, 0.16))
        p['miolo_luz']  = (c_luz, (-0.05, 0.96, -0.03), (0.10, 0.05, 0.10))

        # 2 flores/botoes laterais exuberantes para encher a silhueta
        for j, (bx, by, bz, yaw_b) in enumerate(((-0.17, 0.68, 0.06, 75), (0.17, 0.74, -0.04, -75))):
            p[f'ramo_b{j}'] = ('green_concrete', (0.0, by - 0.12, 0.0), (0.04, 0.20, 0.04), (yaw_b, 48, 0))
            for k in range(5):
                p[f'b{j}_pet_{k}'] = (c_int if k % 2 == 0 else c_ext, (bx, by, bz), (0.08, 0.14, 0.03), (k * 72, 52, 0))
            p[f'b{j}_mio'] = (c_mio, (bx - 0.045, by, bz - 0.045), (0.09, 0.06, 0.09))

    elif tipo != 'vazio':
        raise ValueError(f"Tipo de vaso desconhecido: {tipo!r}")

    return ModeloRico(p, tag)


def criar_regador(tag='regador'):
    """Regador metalico com alca arqueada e bico longo inclinado para frente (+z)."""
    p = {
        'fundo':      ('iron_block',          (-0.13, 0.00, -0.13), (0.26, 0.03, 0.26)),
        'corpo':      ('light_gray_concrete', (-0.13, 0.03, -0.13), (0.26, 0.25, 0.26)),
        'corpo_45':   ('light_gray_concrete', (0.0, 0.03, 0.0),     (0.24, 0.25, 0.24), (45, 0, 0)),
        'faixa_m':    ('iron_block',          (-0.138, 0.14, -0.138), (0.276, 0.035, 0.276)),
        'borda_sup':  ('iron_block',          (-0.138, 0.26, -0.138), (0.276, 0.03, 0.276)),
        'meia_tampa': ('iron_block',          (-0.13, 0.285, 0.0),  (0.26, 0.015, 0.13)),
        'agua_int':   ('light_blue_concrete', (-0.11, 0.23, -0.11), (0.22, 0.02, 0.22)),
        # Alca superior e traseira
        'alca_tras':  ('iron_block',          (-0.025, 0.08, -0.21), (0.05, 0.22, 0.035)),
        'alca_tras_b':('iron_block',          (-0.025, 0.08, -0.21), (0.05, 0.035, 0.09)),
        'alca_topo':  ('iron_block',          (-0.025, 0.28, -0.21), (0.05, 0.11, 0.035)),
        'alca_arco':  ('iron_block',          (-0.025, 0.36, -0.21), (0.05, 0.035, 0.31)),
        'alca_frente':('iron_block',          (-0.025, 0.28,  0.07), (0.05, 0.09, 0.035)),
        # Bico inclinado saindo da frente inferior (+z) e crivo dourado/ferro na ponta
        'bico':       ('iron_block',          (0.0, 0.08, 0.11),    (0.065, 0.32, 0.065), (0, 48, 0)),
        'crivo':      ('gold_block',          (0.0, 0.285, 0.335),  (0.12, 0.04, 0.12),   (0, 48, 0)),
        'crivo_furos':('gray_concrete',       (0.0, 0.312, 0.365),  (0.09, 0.012, 0.09),  (0, 48, 0)),
    }
    return ModeloRico(p, tag)


def criar_panela_fervendo(tag='panela'):
    """Caldeirao/panela real com parede translucida mostrando agua quente, bolhas e 6 sementes."""
    p = {
        # Braseiro / pes de ferro escuro na base
        'pe_1':        ('polished_blackstone', (-0.36, 0.00, -0.36), (0.12, 0.12, 0.12)),
        'pe_2':        ('polished_blackstone', ( 0.24, 0.00, -0.36), (0.12, 0.12, 0.12)),
        'pe_3':        ('polished_blackstone', (-0.36, 0.00,  0.24), (0.12, 0.12, 0.12)),
        'pe_4':        ('polished_blackstone', ( 0.24, 0.00,  0.24), (0.12, 0.12, 0.12)),
        'brasas':      ('magma_block',         (-0.28, 0.02, -0.28), (0.56, 0.07, 0.56)),
        'chama_1':     ('shroomlight',         (-0.16, 0.07, -0.16), (0.32, 0.04, 0.32)),

        # Fundo metalico da panela e aro superior de cobre/ferro
        'fundo':       ('gray_concrete',       (-0.42, 0.11, -0.42), (0.84, 0.06, 0.84)),
        'aro_base':    ('cut_copper',          (-0.44, 0.14, -0.44), (0.88, 0.05, 0.88)),
        # Paredes translucidas permitindo ver claramente a agua e as 6 sementes
        'vidro_frente':('light_blue_stained_glass', (-0.42, 0.19,  0.37), (0.84, 0.36, 0.05)),
        'vidro_tras':  ('light_blue_stained_glass', (-0.42, 0.19, -0.42), (0.84, 0.36, 0.05)),
        'vidro_esq':   ('light_blue_stained_glass', (-0.42, 0.19, -0.37), (0.05, 0.36, 0.74)),
        'vidro_dir':   ('light_blue_stained_glass', ( 0.37, 0.19, -0.37), (0.05, 0.36, 0.74)),
        # Volume de agua quente interna
        'agua_corpo':  ('light_blue_stained_glass', (-0.37, 0.18, -0.37), (0.74, 0.31, 0.74)),
        'agua_topo':   ('white_stained_glass',      (-0.37, 0.48, -0.37), (0.74, 0.03, 0.74)),

        # Aro nobre de cobre e ferro + alcas laterais
        'aro_sup_n':   ('copper_block', (-0.46, 0.54, -0.46), (0.92, 0.07, 0.09)),
        'aro_sup_s':   ('copper_block', (-0.46, 0.54,  0.37), (0.92, 0.07, 0.09)),
        'aro_sup_o':   ('copper_block', (-0.46, 0.54, -0.37), (0.09, 0.07, 0.74)),
        'aro_sup_l':   ('copper_block', ( 0.37, 0.54, -0.37), (0.09, 0.07, 0.74)),
        'alca_esq':    ('iron_block',   (-0.55, 0.48, -0.14), (0.09, 0.10, 0.28)),
        'alca_dir':    ('iron_block',   ( 0.46, 0.48, -0.14), (0.09, 0.10, 0.28)),
    }

    # 6 sementes cozinhando la dentro em alturas e angulos variados
    sementes_pos = [
        (-0.20, 0.26,  0.14, (20, 15, 10),  'brown_terracotta'),
        ( 0.18, 0.34,  0.16, (-35, 22, -8), 'lime_terracotta'),
        (-0.04, 0.39,  0.02, (50, -18, 15), 'brown_terracotta'),
        ( 0.21, 0.24, -0.15, (10, 30, -20), 'brown_terracotta'),
        (-0.22, 0.36, -0.16, (-25, -14, 25),'lime_terracotta'),
        ( 0.03, 0.28, -0.20, (65, 12, 5),   'brown_terracotta'),
    ]
    for i, (sx, sy, sz, srot, scor) in enumerate(sementes_pos):
        p[f'semente_{i}'] = (scor, (sx, sy, sz), (0.10, 0.075, 0.12), srot)

    # Bolhas de fervura subindo na agua
    bolhas = [
        (-0.14, 0.44,  0.18, 0.055), (0.12, 0.46,  0.08, 0.065),
        (-0.02, 0.50, -0.08, 0.070), (0.22, 0.42, -0.06, 0.050),
        (-0.24, 0.48, -0.04, 0.060), (0.06, 0.36,  0.22, 0.045),
        (-0.10, 0.53,  0.06, 0.080), (0.16, 0.52, -0.16, 0.075),
    ]
    for i, (bx, by, bz, bs) in enumerate(bolhas):
        blk = 'white_concrete' if i % 2 == 0 else 'white_stained_glass'
        p[f'bolha_{i}'] = (blk, (bx - bs / 2, by, bz - bs / 2), (bs, bs, bs))

    return ModeloRico(p, tag)


def criar_semente_hashi(tag='sem_hashi', cozida=False):
    """Macro-close: dois palitinhos de bambu pincando uma semente grande (viva ou cozida/rachada)."""
    if not cozida:
        p = {
            # Semente viva, verde-clara e saudavel no centro (0, 0, 0)
            'sem_corpo':  ('lime_terracotta', (0.0, -0.13, 0.0), (0.22, 0.26, 0.19), (0, 0, 0)),
            'sem_bojo':   ('lime_terracotta', (0.0, -0.10, 0.0), (0.25, 0.20, 0.21), (35, 0, 0)),
            'sem_topo':   ('lime_concrete',   (0.0,  0.10, 0.0), (0.14, 0.07, 0.13), (0, 8, 0)),
            'sem_germe':  ('yellow_terracotta', (-0.035, 0.15, -0.03), (0.07, 0.04, 0.06)),
            'sem_brilho': ('white_concrete',  (0.05, 0.02, 0.095), (0.035, 0.06, 0.015)),
        }
    else:
        p = {
            # Semente cozida escura rachada ao meio mostrando interior escuro/morto
            'metade_esq': ('brown_terracotta', (-0.015, -0.13, 0.0), (0.115, 0.26, 0.19), (0, 0, 7)),
            'metade_dir': ('brown_terracotta', ( 0.015, -0.13, 0.0), (0.115, 0.26, 0.19), (0, 0, -7)),
            'casca_tras': ('mud',              (-0.10, -0.11, -0.10), (0.20, 0.22, 0.08)),
            'miolo_coz':  ('moss_block',       (-0.045, -0.10, -0.07), (0.09, 0.21, 0.16)),
            'fenda_esc':  ('black_terracotta', (-0.018, -0.11, -0.08), (0.036, 0.23, 0.185)),
            'topo_murch': ('mud',              (-0.06, 0.10, -0.05),  (0.12, 0.05, 0.10)),
            # Fiapos sutis de vapor saindo da semente quente
            'vapor_1':    ('white_stained_glass', (-0.03, 0.20, -0.02), (0.05, 0.09, 0.05)),
            'vapor_2':    ('white_stained_glass', ( 0.02, 0.31,  0.00), (0.06, 0.08, 0.06)),
        }

    # Dois hashis longos de bambu claro vindo da direita/cima e pincando a semente nas laterais
    p['hashi_sup']   = ('birch_planks',      (-0.11, -0.02, 0.0), (0.038, 0.78, 0.038), (0, 0, -72))
    p['hashi_inf']   = ('stripped_oak_wood', (-0.11, -0.06, 0.0), (0.038, 0.78, 0.038), (0, 0, -82))
    p['ponta_sup']   = ('stripped_oak_wood', (-0.17, -0.01, -0.018), (0.07, 0.032, 0.036))
    p['ponta_inf']   = ('birch_planks',      (-0.17, -0.065, -0.018), (0.07, 0.032, 0.036))

    return ModeloRico(p, tag)


def criar_coroa_imperial(tag='coroa_solta'):
    """Grande Coroa Imperial (Mianliu) dourada com contas pendentes para coroar a Capivara Ping."""
    OURO = 'gold_block'
    PRETO = 'black_concrete'
    PEROLA = 'white_concrete'

    p = {
        # Aro dourado dimensionado para a cabeca da Capivara (largura ~0.82, prof ~0.76)
        'aro_base':    (OURO,  (-0.41, 0.00, -0.38), (0.82, 0.08, 0.76)),
        'aro_friso':   ('yellow_concrete', (-0.42, 0.02, -0.39), (0.84, 0.035, 0.78)),
        'jade_frontal':('emerald_block',   (-0.07, 0.015, 0.36), (0.14, 0.09, 0.04)),
        'rubi_central':('red_concrete',    (-0.035, 0.035, 0.385), (0.07, 0.05, 0.03)),
        # Cupula imperial preta elevada para acomodar a laranjinha da Capivara sem atravessar!
        'cupula':      (PRETO, (-0.31, 0.08, -0.29), (0.62, 0.21, 0.58)),
        'cinta_ouro':  (OURO,  (-0.32, 0.16, -0.30), (0.64, 0.04, 0.60)),
        'grampo_real': (OURO,  (-0.48, 0.18, -0.025), (0.96, 0.04, 0.05)),
        # Tabua superior Mian preta com moldura dourada
        'tabua_mian':  (PRETO, (-0.42, 0.29, -0.50), (0.84, 0.05, 1.00)),
        'moldura_ouro':(OURO,  (-0.435, 0.335, -0.515), (0.87, 0.025, 1.03)),
        'pinaculo':    (OURO,  (-0.06, 0.36, -0.06), (0.12, 0.05, 0.12)),
    }

    # 7 cordoes imperiais de perolas e ouro na frente (+z) e 7 atras (-z), terminando acima das sobrancelhas
    xs = [-0.33, -0.22, -0.11, 0.0, 0.11, 0.22, 0.33]
    for i, xk in enumerate(xs):
        for lado, zk in (('f', 0.475), ('t', -0.505)):
            p[f'fio_a_{lado}{i}'] = (OURO,   (xk - 0.016, 0.225, zk), (0.032, 0.060, 0.032))
            p[f'fio_b_{lado}{i}'] = (PEROLA, (xk - 0.015, 0.155, zk), (0.030, 0.065, 0.030))
            p[f'fio_c_{lado}{i}'] = (OURO,   (xk - 0.016, 0.090, zk), (0.032, 0.060, 0.032))
            p[f'fio_d_{lado}{i}'] = (PEROLA, (xk - 0.014, 0.030, zk), (0.028, 0.055, 0.028))

    return ModeloRico(p, tag)
