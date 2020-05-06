import json
from roominfo import roomInfo

def s2bin(s: str) -> str:
    """
    用于将字符串转为二进制
    :param s: 传入的字符串
    :return: 转换为二进制的0/1字符串
    """
    tmp = []
    tmpp = ''
    for c in s:
        tmpp = str(bin(ord(c)).replace('0b', ''))
        while len(tmpp) != 8:
            tmpp = '0' + tmpp
        tmp.append(tmpp)

    str_bin = ''.join(tmp)
    return str_bin


def bin2hex(s: str) -> str:
    """
    将二进制转换为十六进制
    :param s: 二进制字符串
    :return: 十六进制字符串
    """
    temp = ''
    result = ''
    for c in s:
        temp += c
        if len(temp) == 4:
            result += str(hex(int(temp, 2))[2:])
            temp = ''
    if temp is not '':
        result += str(hex(int(temp, 2))[2:])
    return result


def convertSourceDanmuToList(message: bytearray) -> list:
    """
    发现当有大量弹幕数据涌入时，b站会将多条弹幕信息合并在一个数据包中
    该方法用于将多条弹幕数据从一个数据包中解析出来
    :param message: 原始数据包
    :return: 经过拆分并被json解码过的弹幕json信息list
    """
    msgList = []
    while len(message):
        length_temp = int().from_bytes(message[:4], byteorder='big', signed=True)
        message_temp = message[:length_temp]
        message = message[length_temp:]
        msgList.append(json.loads(message_temp[16:]))
    return msgList


def generateAuthPack(dmj: roomInfo) -> bytes:
    """
    构造首次连接时的认证包
    :param room_id: 房间号
    :return: 构造出的认证包
    """
    payload = '{"uid":0,"roomid":' \
              + dmj.room_id \
              + ',"protover":2,"platform":"web","clientver":"1.11.0","type":2,"key":"' \
              + dmj.get_token() \
              + '"}'
    payload_byte = bytearray(payload, 'ascii')

    length = len(payload_byte) + 16
    length_byte = length.to_bytes(4, 'big')

    header_length_byte = int(16).to_bytes(2, 'big')

    datapack_protocol_ver_byte = int(2).to_bytes(2, 'big')

    kind_of_datapack_byte = int(7).to_bytes(4, 'big')

    const_one_byte = int(1).to_bytes(4, 'big')

    return length_byte + header_length_byte + datapack_protocol_ver_byte + kind_of_datapack_byte + const_one_byte + payload_byte
