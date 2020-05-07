import sys

from danmuWebsocket import danmuWebsocket
from mainWindow import mainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    # dws = danmuWebsocket('5050')
    # dws.startWss()
    app = QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec_())


