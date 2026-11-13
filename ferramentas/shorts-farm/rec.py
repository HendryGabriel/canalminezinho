"""Helpers de gravacao: inicia/paraliza gravar.py em subprocesso."""
import subprocess, os, sys, time, json
D = os.path.dirname(os.path.abspath(__file__))
PY = os.environ.get('GRAVAR_PYTHON', sys.executable)  # python com numpy + flexaudio
ENV = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV')}


class Rec:
    def __init__(self, base, maxs=300):
        self.base = base
        os.makedirs(os.path.dirname(base), exist_ok=True)
        self.events = []
        self.p = subprocess.Popen([PY, os.path.join(D, 'gravar.py'), base, str(maxs)], cwd=D,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=ENV)
        time.sleep(1.5)

    def ev(self, name):
        self.events.append((name, time.time()))

    def stop(self):
        open(self.base + '.stop', 'w').close()
        out = self.p.communicate(timeout=60)[0]
        json.dump(self.events, open(self.base + '_events.json', 'w'))
        try: os.remove(self.base + '.stop')
        except OSError: pass
        return out
