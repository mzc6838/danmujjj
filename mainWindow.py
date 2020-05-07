import _thread
from PyQt5.QtWidgets import (QWidget, QTextEdit, QPushButton, QLabel, QListWidget, QListWidgetItem)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QStringListModel
from danmuWebsocket import danmuWebsocket
import time


class mainWindow(QWidget):

    isConnect = False

    def __init__(self):
        super().__init__()

        self.confirm_btn = QPushButton('连接', self)
        self.disconnect_btn = QPushButton('断开', self)

        self.roomInfo_Label = QLabel('房间链接：https://live.bilibili.com/', self)

        self.roomid_textE = QTextEdit(self)

        self.danmuContent_listW = QListWidget(self)
        self.danmu_Model = QStringListModel(self)

        self.wss = None

        self.init()

    def init(self):
        self.setWindowTitle('dmj')
        self.setGeometry(300, 300, 600, 350)

        self.roomInfo_Label.setGeometry(20, 30, 280, 30)
        self.roomInfo_Label.setFont(QFont('等线', 14))

        self.roomid_textE.setGeometry(300, 30, 90, 30)

        self.danmuContent_listW.setGeometry(20, 80, 560, 250)
        self.danmuContent_listW.setFont(QFont('等线', 12))
        self.danmuContent_listW.setCurrentRow(self.danmuContent_listW.count() - 1)

        self.confirm_btn.setGeometry(410, 30, 75, 30)
        self.confirm_btn.setFont(QFont('等线', 12))
        self.confirm_btn.clicked.connect(self.startWss)

        self.disconnect_btn.setGeometry(500, 30, 75, 30)
        self.disconnect_btn.setFont(QFont('等线', 12))
        self.disconnect_btn.clicked.connect(self.closeWss)

        self.show()

    def closeEvent(self, QCloseEvent):
        self.dmws.stopWss()
        self.dmws.__del__()

    def startWss(self):
        self.confirm_btn.setEnabled(False)
        self.disconnect_btn.setEnabled(True)
        self.dmws = danmuWebsocket(self.roomid_textE.toPlainText(), self.danmuContent_listW)
        self.dmws.startWss()

    def closeWss(self):
        self.confirm_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.dmws.stopWss()