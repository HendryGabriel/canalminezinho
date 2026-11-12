"""Liga e desliga a gravação do OBS pelo WebSocket (protocolo v5), só com a biblioteca padrão do Python.

Antes (1 vez): OBS → Ferramentas → Configurações do servidor WebSocket → Ativar, porta 4455.
Se tiver senha, ponha em OBS_SENHA (variável de ambiente) ou no argumento --senha.

Uso:
  python -X utf8 obs.py status
  python -X utf8 obs.py gravar        # começa a gravar e mostra a hora exata
  python -X utf8 obs.py parar         # para e mostra o arquivo salvo
Teste: python -X utf8 obs.py --teste  (confere a conta da senha, sem OBS)

No fluxo: obs.py gravar → MCP roda /function cenas:cNNN/start → espera a duração → obs.py parar.
A diferença entre a hora do "gravar" e a do /function é o corte do começo na montagem.
ponytail: cliente WebSocket mínimo (sem extensões, mensagens < 64 KB); trocar por obsws-python se precisar de mais.
"""
import base64, hashlib, json, os, socket, struct, sys, time


def auth(senha, salt, challenge):
    segredo = base64.b64encode(hashlib.sha256((senha + salt).encode()).digest()).decode()
    return base64.b64encode(hashlib.sha256((segredo + challenge).encode()).digest()).decode()


class OBS:
    def __init__(self, host='127.0.0.1', porta=4455, senha=''):
        self.s = socket.create_connection((host, porta), timeout=5)
        chave = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall((f'GET / HTTP/1.1\r\nHost: {host}:{porta}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n'
                        f'Sec-WebSocket-Key: {chave}\r\nSec-WebSocket-Version: 13\r\n'
                        'Sec-WebSocket-Protocol: obswebsocket.json\r\n\r\n').encode())
        resp = b''
        while b'\r\n\r\n' not in resp:
            resp += self.s.recv(1024)
        if b' 101 ' not in resp.split(b'\r\n')[0]:
            raise RuntimeError('OBS recusou a conexão: ' + resp.split(b'\r\n')[0].decode())
        hello = self._ler()['d']
        ident = {'rpcVersion': 1}
        if 'authentication' in hello:
            a = hello['authentication']
            ident['authentication'] = auth(senha, a['salt'], a['challenge'])
        self._enviar({'op': 1, 'd': ident})
        if self._ler().get('op') != 2:
            raise RuntimeError('OBS não aceitou a identificação (senha errada?)')

    def _enviar(self, obj):
        dados = json.dumps(obj).encode()
        mask = os.urandom(4)
        n = len(dados)
        cab = struct.pack('!BB', 0x81, 0x80 | n) if n < 126 else struct.pack('!BBH', 0x81, 0x80 | 126, n)
        self.s.sendall(cab + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(dados)))

    def _rx(self, n):
        buf = b''
        while len(buf) < n:
            parte = self.s.recv(n - len(buf))
            if not parte:
                raise RuntimeError('conexão fechada pelo OBS')
            buf += parte
        return buf

    def _ler(self):
        while True:
            b1, b2 = self._rx(2)
            n = b2 & 0x7F
            if n == 126: n = struct.unpack('!H', self._rx(2))[0]
            elif n == 127: n = struct.unpack('!Q', self._rx(8))[0]
            dados = self._rx(n)
            if b1 & 0x0F == 1:          # só quadros de texto
                return json.loads(dados)

    def pedir(self, tipo, dados=None):
        rid = str(time.time())
        self._enviar({'op': 6, 'd': {'requestType': tipo, 'requestId': rid, 'requestData': dados or {}}})
        while True:
            m = self._ler()
            if m.get('op') == 7 and m['d'].get('requestId') == rid:
                st = m['d']['requestStatus']
                if not st.get('result'):
                    raise RuntimeError(f"{tipo} falhou: {st.get('comment', st.get('code'))}")
                return m['d'].get('responseData', {})


def teste():
    # caso feito à mão: muda se a fórmula mudar (sha256 → base64 → +challenge → sha256 → base64)
    a = auth('senha', 'sal', 'desafio')
    s1 = base64.b64encode(hashlib.sha256(b'senhasal').digest()).decode()
    assert a == base64.b64encode(hashlib.sha256((s1 + 'desafio').encode()).digest()).decode()
    assert len(base64.b64decode(a)) == 32
    print('teste OK (a conexão real só dá para testar com o OBS aberto e o WebSocket ligado)')


if __name__ == '__main__':
    args = sys.argv[1:]
    if args == ['--teste']:
        teste(); sys.exit()
    senha = args[args.index('--senha') + 1] if '--senha' in args else os.environ.get('OBS_SENHA', '')
    obs = OBS(senha=senha)
    cmd = args[0] if args else 'status'
    if cmd == 'gravar':
        obs.pedir('StartRecord'); print('gravando desde', f'{time.time():.3f}')
    elif cmd == 'parar':
        print('salvo em', obs.pedir('StopRecord').get('outputPath'), 'às', f'{time.time():.3f}')
    else:
        print(obs.pedir('GetRecordStatus'))
