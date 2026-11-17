import os as _os
PROJ = _os.environ.get('ANIM_PROJETO', _os.getcwd())
"""Helpers de gravacao: inicia/paraliza gravar.py em subprocesso."""
import subprocess, os, time, json
D = _os.path.dirname(_os.path.abspath(__file__))
ENV = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV')}


class Rec:
    def __init__(self, base, maxs=300):
        self.base = base
        os.makedirs(os.path.dirname(base), exist_ok=True)
        self.events = []
        for tent in range(4):
            self.p = subprocess.Popen([D + r'\.venv\Scripts\python.exe', D + r'\gravar.py', base, str(maxs)], cwd=D,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=ENV)
            tam = 0
            for _ in range(50):          # ate 25 s: o mkv so cresce quando o 1o cluster e gravado
                time.sleep(0.5)
                try:
                    tam = os.path.getsize(base + '.mkv')
                except OSError:
                    tam = 0
                if tam > 5000 or self.p.poll() is not None:
                    break
            if tam > 5000:
                break
            # captura travada (gfxcapture entregou 1 quadro): reinicia
            open(base + '.stop', 'w').close()
            try:
                self.p.communicate(timeout=20)
            except subprocess.TimeoutExpired:
                self.p.kill()
            try: os.remove(base + '.stop')
            except OSError: pass
            print('captura travada, tentando de novo', tent + 1, flush=True)
            time.sleep(3)
        else:
            raise RuntimeError('captura nao iniciou')

    def ev(self, name):
        self.events.append((name, time.time()))

    def stop(self):
        open(self.base + '.stop', 'w').close()
        try:
            out = self.p.communicate(timeout=60)[0]
        except subprocess.TimeoutExpired:
            self.p.kill(); out = 'TIMEOUT'
            subprocess.run('taskkill /F /IM ffmpeg.exe', shell=True, capture_output=True)
        json.dump(self.events, open(self.base + '_events.json', 'w'))
        try: os.remove(self.base + '.stop')
        except OSError: pass
        return out
