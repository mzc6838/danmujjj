import json
import requests
import websocket

class roomInfo:
    def __init__(self):
        super(self)
        self.room_id = '0'

    def __init__(self, room_id: str):
        self.room_id = room_id

    def getRoomId(self):
        return self.room_id

    def get_token(self):
        if self.room_id != 0:
            req_link = 'https://api.live.bilibili.com/room/v1/Danmu/getConf?room_id=' + self.room_id + '&platform=pc&player=web'
            return json.loads(requests.get(req_link).text)['data']['token']
