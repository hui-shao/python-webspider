import json
import os
import re
import sys
import traceback
import time
import random

import requests


class Spider:
    def __init__(self):
        self.json_filename = ""
        self.save_path = "downloads"
        self.json = {}
        self.err_list_total = []  # 记录错误

    def run(self):
        print("START...")

        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)

        self.json_filename = sys.argv[1] if len(sys.argv) > 1 else input("输入当前目录下json文件名：")
        print("获取基本信息中...\n")
        text_in = open(self.json_filename, "r", encoding="utf-8").read()
        self.json = json.loads(text_in)

        datas = self.json.get("info").get("Datas")
        i = 1
        for item in datas:
            print(i)
            sound_name = item.get("soundstr")
            sound_name = self.clean_file_name(sound_name)
            sound_intro = item.get("intro")
            sound_intro = self.clean_html(sound_intro)
            sound_url = item.get("soundurl")
            cover_url = item.get("front_cover")
            self.download(sound_name, sound_intro, sound_url, cover_url)
            i += 1
            sleep_time = random.randint(5, 30)
            print(f"\n\nWait {sleep_time}s\n\n")
            time.sleep(sleep_time)
        self.err_url_output()
        input("Press ENTER to Exit..")

    @staticmethod
    def clean_file_name(filename: str):  # 文件名合法化 用作路径
        invalid_chars = r'[\\\/:*?"<>|]'
        replace_char = '-'
        return re.sub(invalid_chars, replace_char, filename)

    @staticmethod
    def clean_html(html):  # 利用nltk的clean_html()函数将html文件解析为text文件
        # First we remove inline JavaScript/CSS:
        cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
        # Then we remove html comments. This has to be done before removing regular
        # tags since comments can contain '>' characters.
        cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
        # Next we can remove the remaining tags:
        cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
        # Finally, we deal with whitespace
        cleaned = re.sub(r"&nbsp;", " ", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned.strip()

    def download(self, _name: str, _intro: str, _s_url: str, _c_url: str) -> None:
        print(f"Current:\n{_name}\n{_intro}\n{_s_url}\n{_c_url}\n")
        if not os.path.exists(f"{self.save_path}/{_name}"):
            os.mkdir(f"{self.save_path}/{_name}")

        open(f"{self.save_path}/{_name}/intro.txt", "w", encoding="utf-8").write(_name + "\n\n" + _intro)

        res1 = self._requests("get", _s_url)
        suffix1 = os.path.splitext(_s_url)[1]
        if res1 is not None and res1.status_code == 200:
            open(f"{self.save_path}/{_name}/audio{suffix1}", "wb").write(res1.content)
        else:
            self.err_list_total.append(_s_url)
        print(f"Sound Resp: {res1}")

        res2 = self._requests("get", _c_url)
        suffix2 = os.path.splitext(_c_url)[1]
        if res2 is not None and res1.status_code == 200:
            open(f"{self.save_path}/{_name}/cover{suffix2}", "wb").write(res2.content)
        else:
            self.err_list_total.append(_c_url)
        print(f"Cover Resp: {res1}")

    def err_url_output(self):
        print(f"\n\nError_List: {len(self.err_list_total)}\n{self.err_list_total}")
        open(f"{self.save_path}/err_list.txt", "w").writelines(list(map(lambda x: (x + "\n"), self.err_list_total)))

    @staticmethod
    def _requests(_method: str, _url: str, _data: dict = None, _param: dict = None, _ex_hea: dict = None):
        hea = {
            "User-Agent": "MissEvanApp/5.7.5 (Android;11;Xiaomi M2102K1AC mars)"
        }

        retry_n = 0
        while retry_n < 5:
            try:
                if _ex_hea:
                    hea.update(_ex_hea)
                if _method.upper() == 'GET':
                    res = requests.get(_url, data=_data, params=_param, headers=hea, timeout=(12.05, 72))
                elif _method.upper() == 'POST':
                    res = requests.post(_url, data=_data, headers=hea, timeout=(12.05, 54))
                elif _method.upper() == 'PUT':
                    res = requests.put(_url, data=_data, headers=hea, timeout=(12.05, 54))
                elif _method.upper() == 'DELETE':
                    res = requests.delete(_url, data=_data, headers=hea, timeout=(12.05, 54))
                else:
                    print('TypeError')
                    return None
            except requests.exceptions.SSLError:
                print("SSL 错误, 2s后重试 -> SSLError: An SSL error occurred.")
                time.sleep(2)
            except requests.exceptions.ConnectTimeout:
                print(
                    "建立连接超时, 5s后重试 -> ConnectTimeout: The request timed out while trying to connect to the remote "
                    "server.")
                time.sleep(5)
            except requests.exceptions.ReadTimeout:
                print(
                    "读取数据超时, 3s后重试 -> ReadTimeout: The server did not send any data in the allotted amount of time.")
                time.sleep(3)
            except requests.exceptions.ConnectionError:
                print(f"{traceback.format_exc(3)}")
                print("\n建立连接错误, 5s后重试")
                time.sleep(5)
            except requests.exceptions.RequestException:
                print(f"{traceback.format_exc(3)}")
                print("\n其他网络连接错误, 5s后重试")
                time.sleep(5)
            except KeyboardInterrupt:
                print("\n捕获到 KeyboardInterrupt, 退出")
                return None
            else:
                return res
            retry_n += 1
            continue
        print("\n达到最大重试次数, 退出")
        return None


if __name__ == '__main__':
    os.chdir(sys.path[0])
    try:
        spider = Spider()
        spider.run()
    except KeyboardInterrupt:
        print("\n\nRaised KeyboardInterruption.\nExit!")
    except Exception:
        traceback.print_exc()
