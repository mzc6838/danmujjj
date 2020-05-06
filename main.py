from danmuWebsocket import danmuWebsocket

if __name__ == '__main__':
    dws = danmuWebsocket('5050')
    dws.startWss()

