from PyQt5.QtWidgets import (QWidget, QLineEdit, QPushButton, QLabel, QListWidget, QApplication)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QStringListModel
from danmuWebsocket import danmuWebsocket


class mainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.confirm_btn = QPushButton('连接', self)
        self.disconnect_btn = QPushButton('断开', self)

        self.roomInfo_Label = QLabel('房间链接：https://live.bilibili.com/', self)
        self.realtimeRenQi_Label = QLabel('当前人气值：', self)
        self.realtimeRenQiNum_Label = QLabel('0', self)
        self.fans_Label = QLabel('当前粉丝数：', self)
        self.fansNum_Label = QLabel('0', self)

        self.roomid_LE = QLineEdit(self)

        self.danmuContent_listW = QListWidget(self)
        self.danmu_Model = QStringListModel(self)

        self.dmws = None

        self.init()

    def init(self):
        self.setWindowTitle('dmj')
        self.setGeometry(300, 300, 600, 380)

        self.roomInfo_Label.setGeometry(20, 30, 280, 30)
        self.roomInfo_Label.setFont(QFont('等线', 14))
        self.realtimeRenQi_Label.setGeometry(20, 330, 100, 30)
        self.realtimeRenQi_Label.setFont(QFont('等线', 14))
        self.realtimeRenQiNum_Label.setGeometry(130, 330, 440, 30)
        self.realtimeRenQiNum_Label.setFont(QFont('等线', 14))
        self.fans_Label.setGeometry(310, 330, 110, 30)
        self.fans_Label.setFont(QFont('等线', 14))
        self.fansNum_Label.setGeometry(420, 330, 120, 30)
        self.fansNum_Label.setFont(QFont('等线', 14))

        self.roomid_LE.setGeometry(300, 30, 90, 30)
        self.roomid_LE.setFont(QFont('等线', 14))

        self.danmuContent_listW.setGeometry(20, 80, 560, 250)
        self.danmuContent_listW.setFont(QFont('等线', 12))
        self.danmuContent_listW.setCurrentRow(self.danmuContent_listW.count() - 1)

        self.confirm_btn.setGeometry(410, 30, 75, 30)
        self.confirm_btn.setFont(QFont('等线', 12))
        self.confirm_btn.clicked.connect(self.startWss)

        self.disconnect_btn.setGeometry(500, 30, 75, 30)
        self.disconnect_btn.setFont(QFont('等线', 12))
        self.disconnect_btn.clicked.connect(self.closeWss)
        self.disconnect_btn.setEnabled(False)

        self.show()

    def closeEvent(self, QCloseEvent):
        if self.dmws is not None:
            if self.dmws.getConnectionState():
                print('closing...')
                self.dmws.stopWss()
                self.dmws.__del__()

    def startWss(self):
        self.confirm_btn.setEnabled(False)
        self.disconnect_btn.setEnabled(True)
        self.roomid_LE.setEnabled(False)
        self.dmws = danmuWebsocket(self.roomid_LE.text(), self.danmuContent_listW)
        self.dmws.startWss()
        self.dmws.realtimeRenQi.connect(self.updateRealtimeRenQi)
        self.dmws.realtimeFans.connect(self.updateFansNum)

    def closeWss(self):
        self.confirm_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.roomid_LE.setEnabled(True)
        self.dmws.stopWss()

    def updateRealtimeRenQi(self, renqi):
        self.realtimeRenQiNum_Label.setText(renqi)

    def updateFansNum(self, fans):
        self.fansNum_Label.setText(fans)
