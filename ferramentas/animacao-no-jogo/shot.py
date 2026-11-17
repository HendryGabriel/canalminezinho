import mc, base64, sys
def shot(path):
    r = mc.call('vision.screenshot', {})
    open(path, 'wb').write(base64.b64decode(r['base64']))
    return path
if __name__ == '__main__':
    print(shot(sys.argv[1]))
