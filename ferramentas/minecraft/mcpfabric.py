"""Cliente do MCPFabric (mod 0.10+, ponte HTTP do proprio jogo). Config: env MCPFABRIC_CONFIG ou a instancia canal-26-3 do CurseForge.
Ponte em 127.0.0.1:25599 (POST /rpc, Bearer token). Uso: import mcpfabric as mcf; mcf.cmd('time set day'); mcf.rpc('info.status')"""
import json, os, time, urllib.request, urllib.error

CFG = os.environ.get('MCPFABRIC_CONFIG', os.path.join(os.path.expanduser('~'), 'curseforge', 'minecraft', 'Instances', 'canal-26-3', 'config', 'mcpfabric.config.json'))
_tok = [None]


def _token():
    if not _tok[0]:
        _tok[0] = json.load(open(CFG, encoding='utf-8'))['token']
    return _tok[0]


def rpc(method, params=None, t=30):
    body = json.dumps({'method': method, 'params': params or {}}).encode()
    r = urllib.request.Request('http://127.0.0.1:25599/rpc', body, {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + _token()})
    for tent in range(5):
        try:
            d = json.loads(urllib.request.urlopen(r, timeout=t).read().decode())
            if not d.get('ok'):
                raise RuntimeError('%s: %s' % (method, d.get('error')))
            return d.get('result')
        except urllib.error.HTTPError as e:
            if e.code == 429 and tent < 4:
                time.sleep(0.5); continue
            raise


def cmd(c, t=30):
    """roda um comando (sem a barra) como operador; devolve o texto de retorno"""
    return rpc('command.run', {'command': c}, t)


c = cmd
