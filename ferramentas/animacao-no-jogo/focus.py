"""Foco temporario na janela do Minecraft + SendInput (teclas reais)."""
import ctypes, time
from ctypes import wintypes
import keys
u = ctypes.windll.user32

class KI(ctypes.Structure):
    _fields_ = [('wVk', wintypes.WORD), ('wScan', wintypes.WORD), ('dwFlags', wintypes.DWORD), ('time', wintypes.DWORD), ('dwExtraInfo', ctypes.c_size_t)]
class MI(ctypes.Structure):
    _fields_ = [('dx', ctypes.c_long), ('dy', ctypes.c_long), ('mouseData', wintypes.DWORD), ('dwFlags', wintypes.DWORD), ('time', wintypes.DWORD), ('dwExtraInfo', ctypes.c_size_t)]
class U(ctypes.Union):
    _fields_ = [('ki', KI), ('mi', MI)]
class INP(ctypes.Structure):
    _fields_ = [('type', wintypes.DWORD), ('u', U)]


def key(sc, upflag=False):
    i = INP(); i.type = 1; i.u.ki = KI(0, sc, 0x0008 | (0x0002 if upflag else 0), 0, 0)
    u.SendInput(1, ctypes.byref(i), ctypes.sizeof(INP))


def focus():
    h = keys.hwnd(); prev = u.GetForegroundWindow()
    key(0x38); key(0x38, True)  # alt tap libera SetForegroundWindow
    u.ShowWindow(h, 9); u.SetForegroundWindow(h)
    time.sleep(0.4)
    return prev, u.GetForegroundWindow() == h


def restore(prev):
    key(0x38); key(0x38, True); u.SetForegroundWindow(prev)
