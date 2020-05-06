import websocket
from roominfo import roomInfo
from util import *
import _thread
import zlib
import time

class danmuWebsocket:
    def __init__(self):
        self.room = roomInfo('0')
        self.wss = None

    def __init__(self, roomId: str):
        self.room = roomInfo(roomId)
        self.wss = None

    def getRoomId(self):
        return self.room.getRoomId()

    def getToken(self):
        return self.room.get_token()

    def handleMsg(self, message):
        message = message[16:]
        try:
            message = zlib.decompress(message)
        except Exception as e:
            print(message)
        else:
            t = convertSourceDanmuToList(message)
            for l in t:
                if l['cmd'] == 'SEND_GIFT':
                    timestr = time.strftime("[%H:%M:%S] ", time.localtime(l['data']['timestamp']))
                    print(timestr + l['data']['uname'] + ' 赠送 ' + l['data']['giftName'] + ' x' + str(l['data']['num']))
                elif l['cmd'] == 'DANMU_MSG':
                    timestr = time.strftime("[%H:%M:%S] ", time.localtime(l['info'][9]['ts']))
                    print(timestr + l['info'][2][1] + ':' + l['info'][1])

    def on_error(self, error):
        print(error)

    def on_message(self, message):
        _thread.start_new_thread(self.handleMsg, (message,))

    def on_open(self):
        print("opening...")
        self.wss.send(generateAuthPack(self.room))

    def heartBeat(self, wss):
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
                wss.send(final)
            except Exception as e:
                print('connecting...')
                time.sleep(5)
            else:
                print('heart')
                time.sleep(20)

    def startWss(self):
        self.wss = websocket.WebSocketApp('wss://broadcastlv.chat.bilibili.com/sub',
                                     on_message=self.on_message,
                                     on_error=self.on_error,
                                     on_open=self.on_open)
        _thread.start_new_thread(self.heartBeat, (self.wss,))
        self.wss.run_forever()


