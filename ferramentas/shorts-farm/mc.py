"""Cliente minimo da ponte MCP Fabric (JSON-RPC em /rpc). Le o token do bridge.json; nunca imprime."""
import json, urllib.request, os, base64, sys

_D = os.path.expanduser(r'~/.mcpfabric/bridge.json')
_id = 0


def call(method, params=None, timeout=30):
    global _id
    _id += 1
    b = json.load(open(_D))
    body = json.dumps({"jsonrpc": "2.0", "id": _id, "method": method, "params": params or {}}).encode()
    req = urllib.request.Request(b['url'] + '/rpc', data=body, method='POST',
                                 headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + b['token']})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=timeout))
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode(errors='replace')}
    if 'error' in r:
        return {"error": r['error']}
    return r.get('result')


def cmd(c):
    return call('command.run', {'command': c.lstrip('/')})


def shot(path, **kw):
    r = call('vision.screenshot', kw, timeout=60)
    if isinstance(r, dict):
        for k, v in r.items():
            if isinstance(v, str) and len(v) > 1000:
                open(path, 'wb').write(base64.b64decode(v.split(',')[-1]))
                return {kk: vv for kk, vv in r.items() if kk != k}
    return r


if __name__ == '__main__':
    print(json.dumps(call(sys.argv[1], json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}), indent=1, ensure_ascii=False)[:6000])
