# -*- coding: UTF-8 -*-
# @Time    : 2021/8/2 14:08
# @Author  : Hui-Shao

import requests
import json


class WxPusherTool:
    @staticmethod
    def send_wxmsg(_appToken, _type, _content, _summary="", _uids=None, _topicIds=None, _origin_url=""):
        """
        Args:
            _appToken: (str) "AT_xxx"
            _type: (int) 内容类型 1 表示文字  2 表示html(只发送body标签内部的数据即可，不包括body标签) 3 表示markdown
            _content: (str) 正文内容
            _summary: (str)消息摘要，显示在微信聊天页面或者模版消息卡片上，限制长度100，可以不传，不传默认截取content前面的内容。
            _uids: (list-str) 发送目标的UID，是一个数组。注意uids和topicIds可以同时填写，也可以只填写一个。"UID_xxxx"
            _topicIds: (list-str) 发送目标的topicId，是一个数组，也就是群发，使用uids单发的时候， 可以不传。
            _origin_url: (str) 原文链接(可选)
        """
        if _uids is None:
            _uids = []
        if len(_appToken) <= 5:
            return 1
        url_postmsg = "https://wxpusher.zjiecode.com/api/send/message"
        hea = {
            "Content-Type": "application/json"
        }
        data = {
            "appToken": str(_appToken),
            "content": str(_content),
            "summary": str(_summary),
            "contentType": int(_type),
            "topicIds": _topicIds,
            "uids": _uids,
            "url": _origin_url
        }
        try:
            res = requests.post(url=url_postmsg, json=data, headers=hea)  # 注: 不可用 data=data
            msg_back = json.loads(res.text)
            if msg_back["success"]:
                print("[WxPusher] 消息推送成功！")
            else:
                print("[WxPusher] 消息推送可能失败 返回值：%s" % (msg_back["msg"]))
        except Exception as err_info:
            print("消息发送错误\n", err_info)
