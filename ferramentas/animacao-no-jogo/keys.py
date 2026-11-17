"""Envia teclas para a janela do Minecraft via PostMessage (sem roubar o foco)."""
import ctypes, time, sys
from ctypes import wintypes
u = ctypes.windll.user32
WM_KEYDOWN, WM_KEYUP = 0x100, 0x101
VK = {'F1': (0x70, 0x3B), 'F3': (0x72, 0x3D), 'P': (0x50, 0x19), 'ESC': (0x1B, 0x01), 'F2': (0x71, 0x3C), 'F5': (0x74, 0x3F)}


def hwnd():
    res = []
    @ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    def cb(h, l):
        n = u.GetWindowTextLengthW(h)
        if n:
            b = ctypes.create_unicode_buffer(n + 1); u.GetWindowTextW(h, b, n + 1)
            if b.value.startswith('Minecraft') and u.IsWindowVisible(h):
                res.append(h)
        return True
    u.EnumWindows(cb, 0)
    return res[0]


def down(k, h=None):
    h = h or hwnd(); vk, sc = VK[k]
    u.PostMessageW(h, WM_KEYDOWN, vk, 1 | (sc << 16))


def up(k, h=None):
    h = h or hwnd(); vk, sc = VK[k]
    u.PostMessageW(h, WM_KEYUP, vk, 1 | (sc << 16) | (1 << 30) | (1 << 31))


def tap(k, h=None):
    down(k, h); time.sleep(0.08); up(k, h)


def combo(a, b):
    h = hwnd(); down(a, h); time.sleep(0.1); tap(b, h); time.sleep(0.1); up(a, h)


def set_client(w, hgt, x=None, y=None):
    """Redimensiona a janela para area cliente w x hgt."""
    h = hwnd()
    class R(ctypes.Structure): _fields_ = [('l', ctypes.c_long), ('t', ctypes.c_long), ('r', ctypes.c_long), ('b', ctypes.c_long)]
    wr, cr = R(), R()
    u.GetWindowRect(h, ctypes.byref(wr)); u.GetClientRect(h, ctypes.byref(cr))
    bw = (wr.r - wr.l) - cr.r; bh = (wr.b - wr.t) - cr.b
    x = wr.l if x is None else x; y = wr.t if y is None else y
    SWP_NOZORDER, SWP_NOACTIVATE = 0x4, 0x10
    u.SetWindowPos(h, 0, x, y, w + bw, hgt + bh, SWP_NOZORDER | SWP_NOACTIVATE)
    u.GetClientRect(h, ctypes.byref(cr))
    return cr.r, cr.b


if __name__ == '__main__':
    if sys.argv[1] == 'combo': combo(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'tap': tap(sys.argv[2])
    elif sys.argv[1] == 'size': print(set_client(int(sys.argv[2]), int(sys.argv[3]), *(int(a) for a in sys.argv[4:6])))
