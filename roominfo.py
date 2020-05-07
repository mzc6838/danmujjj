import json
import requests


class roomInfo:
    """
    房间信息类
    用于存储房间id以及其成员函数get_token用于获取发起ws请求时所需要的token值
    """
    def __init__(self, room_id: str):
        """
        构造函数传入房间id字符串，这个字符串为直接id而不是间接房间id
        :param room_id:
        """
        self.room_id = room_id

    def getRoomId(self):
        return self.room_id

    def get_token(self):
        if self.room_id != 0:
            req_link = 'https://api.live.bilibili.com/room/v1/Danmu/getConf?room_id=' + self.room_id + '&platform=pc&player=web'
            return json.loads(requests.get(req_link).text)['data']['token']
