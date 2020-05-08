import websocket
from roominfo import roomInfo
from util import *
import _thread
import zlib
import time
import threading
import ctypes
import inspect
from PyQt5.QtWidgets import (QListWidget, QApplication, QListWidgetItem)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QObject
import json

class runForeverThread(threading.Thread):
    def __init__(self, wss: websocket.WebSocketApp):
        threading.Thread.__init__(self)
        self.wss = wss
        self.runThread = None
        self.heartBeat = None

    def run(self) -> None:
        self.wss.run_forever()

class heartBeatThread(threading.Thread):
    def __init__(self, wss: websocket.WebSocketApp):
        threading.Thread.__init__(self)
        self.wss = wss

    def run(self) -> None:
        payload = 'hello'
        payload_byte = bytearray(payload, 'ascii')

        length = len(payload_byte) + 16
        length_byte = length.to_bytes(4, 'big')

        header_length_byte = int(16).to_bytes(2, 'big')
        datapack_protocol_ver_byte = int(1).to_bytes(2, 'big')
        kind_of_datapack_byte = int(2).to_bytes(4, 'big')
        const_one_byte = int(1).to_bytes(4, 'big')
        final = length_byte + header_length_byte + datapack_protocol_ver_byte + kind_of_datapack_byte + const_one_byte + payload_byte
        while 1:
            try:
                self.wss.send(final)
            except Exception as e:
                print('connecting...')
                time.sleep(5)
            else:
                print('heart')
                time.sleep(20)

class danmuWebsocket(QObject):
    """
    websocket类，用于构造连接到b站直播间ws服务器的过程以及保持连接,同时获取服务器发送的弹幕信息
    """

    realtimeRenQi = pyqtSignal(str)
    realtimeFans = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.room = roomInfo('0')
        self.wss = None
        self.danmuContent = None
        self.isConnected = False

    def __init__(self, roomId: str):
        """
        构造函数，使用房间id构造ws连接
        :param roomId: 房间直接id
        """
        super().__init__()
        self.room = roomInfo(roomId)
        self.wss = None
        self.isConnected = False

    def __init__(self, roomId: str, danmuContent: QListWidget):
        """
        构造函数，使用房间id构造ws连接，同时传入弹幕鸡主窗口中弹幕显示Widget
        :param roomId: 房间直接id
        :param danmuContent: 主窗口中显示弹幕的QListWidget
        """
        super().__init__()
        self.room = roomInfo(roomId)
        self.wss = None
        self.danmuContent = danmuContent
        self.isConnected = False

    def getRoomId(self):
        return self.room.getRoomId()

    def getToken(self):
        return self.room.get_token()

    def handleMsg(self, message):
        """
        处理从弹幕服务器发来的弹幕信息，由on_message()方法调用
        :param message: 接收到的信息
        """
        message = message[16:]
        try:
            message = zlib.decompress(message)
        except Exception as e:
            if message == b'{"code":0}':
                self.danmuContent.addItem(QListWidgetItem(QIcon('img/notice.png'), '已连接到直播间。'))
                QApplication.processEvents()
                self.isConnected = True
            else:
                print(message)
                try:
                    temp = json.loads(message)
                except Exception as e:
                    self.sendRenQiToMainWindow(str(int().from_bytes(message, 'big', signed=False)))
                else:
                    if temp['cmd'] == 'ROOM_REAL_TIME_MESSAGE_UPDATE':
                        self.sendFansToMainWindow(str(temp['data']['fans']))

            # pass
        else:
            t = convertSourceDanmuToList(message)
            for l in t:
                if l['cmd'] == 'SEND_GIFT':
                    timestr = time.strftime("[%H:%M:%S] ", time.localtime(l['data']['timestamp']))
                    # print(timestr + l['data']['uname'] + ' 赠送 ' + l['data']['giftName'] + ' x' + str(l['data']['num']))
                    self.danmuContent.addItem(QListWidgetItem(QIcon('img/gift.png'), timestr + l['data']['uname'] + ' 赠送 ' + l['data']['giftName'] + ' x' + str(l['data']['num'])))
                elif l['cmd'] == 'DANMU_MSG':
                    timestr = time.strftime("[%H:%M:%S] ", time.localtime(l['info'][9]['ts']))
                    # print(timestr + l['info'][2][1] + ':' + l['info'][1])
                    self.danmuContent.addItem(QListWidgetItem(QIcon('img/message.png'), timestr + l['info'][2][1] + ':' + l['info'][1]))
            self.danmuContent.setCurrentRow(self.danmuContent.count() - 1)
            QApplication.processEvents()

    def on_error(self, error):
        self.isConnected = False
        self.stopThread(self.heartBeat.ident)
        self.danmuContent.addItem(QListWidgetItem(QIcon('img/error.png'), '出现错误：' + error))
        QApplication.processEvents()
        print(error)

    def on_message(self, message):
        _thread.start_new_thread(self.handleMsg, (message,))

    def on_open(self):
        print("opening...")
        self.danmuContent.addItem(QListWidgetItem(QIcon('img/notice.png'), '正在连接......'))
        QApplication.processEvents()
        self.wss.send(generateAuthPack(self.room))

    def __del__(self):
        if self.isConnected == True:
            self.isConnected == False
            self.wss.close()
            self.stopThread(self.heartBeat.ident)

    def stopWss(self):
        if self.isConnected == True:
            self.danmuContent.addItem(QListWidgetItem(QIcon('img/notice.png'), '连接已断开。'))
            QApplication.processEvents()
            self.isConnected == False
            self.wss.close()
            self.stopThread(self.heartBeat.ident)

    def stopThread(self, tid):
        """
        停止一个由Threading创建的线程
        :param tid: Thread的id，可由thread.ident获得
        :return: 0: 线程不存在
        """
        tid = ctypes.c_long(tid)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(SystemExit))
        if res == 0:
            return
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def startWss(self):
        self.wss = websocket.WebSocketApp('wss://broadcastlv.chat.bilibili.com/sub',
                                     on_message=self.on_message,
                                     on_error=self.on_error,
                                     on_open=self.on_open)
        self.runThread = runForeverThread(self.wss)
        self.heartBeat = heartBeatThread(self.wss)
        self.runThread.start()
        self.heartBeat.start()

    def getConnectionState(self):
        return self.isConnected

    def sendRenQiToMainWindow(self, RenQi):
        self.realtimeRenQi.emit(str(RenQi))

    def sendFansToMainWindow(self, Fans):
        self.realtimeFans.emit(Fans)

