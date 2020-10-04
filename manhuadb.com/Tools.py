# -*- coding: UTF-8 -*-
# @Time    : 2020/8/8 17:05
# @Author  : Hui-Shao

import json
import os
import platform
import time

import requests


class ConsoleTools(object):
    def __init__(self):
        pass

    @staticmethod
    def check_platform():
        check_result = platform.system()
        if "indows" in check_result:
            return "W"
        elif "inux" in check_result:
            return "L"

    def console_clear(self):
        sysinfo = self.check_platform()
        if sysinfo == "W":
            os.system("cls")
            return
        elif sysinfo == "L":
            os.system("clear")
            return
        os.system("cls")


class MsgTools:
    def __init__(self):
        pass

    @staticmethod
    def send_wxmsg(_sckey, _title="Title", _text=""):
        """
        用于微信消息推送 服务基于 Server酱
        :param _sckey: 推送用的key（必填）
        :param _title: 标题（必填） 最长256字节
        :param _text: 正文（选填） 最长64K 支持MarkDown  如需换行请使用两个连续的换行符
        :return:
        """
        if len(_sckey) <= 5:
            return 1
        url_postmsg = "https://sc.ftqq.com/%s.send" % _sckey
        _text = _text + "\n\n" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data = {
            "text": "%s" % _title,
            "desp": "%s" % _text
        }
        try:
            res = requests.post(url=url_postmsg, data=data)
            msg_back = json.loads(res.text)
            if msg_back["errmsg"] == "success":
                print("[Server酱] 消息推送成功！")
            else:
                print("[Server酱] 消息推送可能失败 返回值：%s" % (msg_back["errmsg"]))
        except Exception as err_info:
            print("消息发送错误\n", err_info)
