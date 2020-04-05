# -*- coding: UTF-8 -*-
import json


class Base64:
    def __init__(self):
        self._keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

    @staticmethod
    def fromCharCode(n):
        """仿照js的字符转换"""
        return chr(n % 256)

    def decode(self, _input):
        output = ""
        i = 0
        # _input = re.sub("[^A-Za-z0-9\+\/\=]", "", _input)
        while i < len(_input):
            enc1 = self._keyStr.index(_input[i])
            i += 1
            enc2 = self._keyStr.index(_input[i])
            i += 1
            enc3 = self._keyStr.index(_input[i])
            i += 1
            enc4 = self._keyStr.index(_input[i])
            i += 1
            chr1 = (enc1 << 2) | (enc2 >> 4)
            chr2 = ((enc2 & 15) << 4) | (enc3 >> 2)
            chr3 = ((enc3 & 3) << 6) | enc4
            output = output + self.fromCharCode(chr1)
            if enc3 != 64:
                output = output + self.fromCharCode(chr2)
            if enc4 != 64:
                output = output + self.fromCharCode(chr3)
        return output


def run(_input_keys):
    # km5_img_url = "WyIxfGh0dHA6XC9cL2Rpbmd5dWUud3MuMTI2Lm5ldFwvMjAyMFwvMDQwMVwvMTY1OWNjNTFqMDBxODJycTgwMDMwYzAwMGhzMDBwb20uanBnIiwiMnxodHRwOlwvXC9kaW5neXVlLndzLjEyNi5uZXRcLzIwMjBcLzA0MDFcLzYwYTIzODM1ajAwcTgycnE4MDAzcWMwMDBoczAwcG9tLmpwZyIsIjN8aHR0cDpcL1wvZGluZ3l1ZS53cy4xMjYubmV0XC8yMDIwXC8wNDAxXC8wZjU0M2E3N2owMHE4MnJxOTAwM3JjMDAwaHMwMHBvbS5qcGciLCI0fGh0dHA6XC9cL2Rpbmd5dWUud3MuMTI2Lm5ldFwvMjAyMFwvMDQwMVwvYmExMzM1Y2JqMDBxODJycTkwMDMzYzAwMGhzMDBwb20uanBnIiwiNXxodHRwOlwvXC9kaW5neXVlLndzLjEyNi5uZXRcLzIwMjBcLzA0MDFcLzc1NGZmM2YxajAwcTgycnE5MDAzaGMwMDBoczAwcG9tLmpwZyIsIjZ8aHR0cDpcL1wvZGluZ3l1ZS53cy4xMjYubmV0XC8yMDIwXC8wNDAxXC8zNWJkNzg4NWowMHE4MnJxOTAwM21jMDAwaHMwMHBvbS5qcGciLCI3fGh0dHA6XC9cL2Rpbmd5dWUud3MuMTI2Lm5ldFwvMjAyMFwvMDQwMVwvMzQ2YjJmMjBqMDBxODJycTgwMDN0YzAwMGhzMDBwb20uanBnIiwiOHxodHRwOlwvXC9kaW5neXVlLndzLjEyNi5uZXRcLzIwMjBcLzA0MDFcLzRmZDBjNjM0ajAwcTgycnE5MDAzNWMwMDBoczAwcG9tLmpwZyIsIjl8aHR0cDpcL1wvZGluZ3l1ZS53cy4xMjYubmV0XC8yMDIwXC8wNDAxXC9hYWNhMGI0NGowMHE4MnJxODAwM2djMDAwaHMwMHBvbS5qcGciLCIxMHxodHRwOlwvXC9kaW5neXVlLndzLjEyNi5uZXRcLzIwMjBcLzA0MDFcLzU3MDE4ZGE2ajAwcTgycnE5MDAzN2MwMDBoczAwcG9tLmpwZyIsIjExfGh0dHA6XC9cL2Rpbmd5dWUud3MuMTI2Lm5ldFwvMjAyMFwvMDQwMVwvOTdlODNjZThqMDBxODJycTgwMDM2YzAwMGhzMDBwb20uanBnIiwiMTJ8aHR0cDpcL1wvZGluZ3l1ZS53cy4xMjYubmV0XC8yMDIwXC8wNDAxXC9kNDBmNjM5YmowMHE4MnJxOTAwMnRjMDAwaHMwMHBvbS5qcGciXQ=="
    url_list = []
    base64 = Base64()
    bbba = base64.decode(_input_keys)
    num_uel_arr = json.loads(bbba)  # 转换生成list
    for url in num_uel_arr:
        url = url.split("|")[-1]
        if not "http:" in url:
            url = "http:" + url
        url_list.append(url)
    return url_list
