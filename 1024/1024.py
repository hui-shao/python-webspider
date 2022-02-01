import getopt
import os
import platform
import re
import sys
import time
import traceback

import requests

# config
_use_quiet_mode = False
_use_utf8_res_encoding = True
_use_aria2 = False


def options():
    """用于处理传入参数"""
    help_info = '''
        -h [--help]                    显示此帮助信息
        -f [--filename] <filename>     将从该文件批量读入目标地址
        -q [--quiet]                   静默运行模式

        --disable-utf8                 禁用 "对获取的网页进行 utf-8 编码" (默认开启)
        --enable-aria2                 启用 "调用 aria2 进行下载 " (默认关闭)
    '''

    print("")
    global url_list, filename, _use_utf8_res_encoding, _use_aria2, _use_quiet_mode
    opts, args = getopt.getopt(sys.argv[1:], '-h-f:-q', ['help', 'filename=', 'quiet', 'disable-utf8', 'enable-aria2'])
    if len(opts) < 1:  # 若未接收到已经预设的命令行参数，则直接采用默认参数
        print("[*] 未检测到传入参数，采用默认配置\n")
        url_list.append(input("请输入网址(含http): "))
        return 0
    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            print("[+] Help info :\n" + help_info)
            exit(0)
        if opt_name in ('-f', '--filename'):
            filename = str(opt_value)
            print("[+] 从该文件读入目标地址: ", filename)
            continue
        if opt_name in ('-q', '--quiet'):
            _use_quiet_mode = True
            print("[+] 启用无交互静默模式")
            continue
        if opt_name == '--disable-utf8':
            _use_utf8_res_encoding = False
            print("[+] 禁用 '对获取的网页进行 utf-8 编码'")
            continue
        if opt_name == '--enable-aria2':
            _use_aria2 = True
            print("[+] 启用 '调用 aria2 进行下载'")
            continue
    print("")


def _requests(_method: str, _url: str, _data: dict = None, _param: dict = None, _ex_hea: dict = None):
    data = _data
    param = _param
    hea = {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (Ksubpage_html, like Gecko) Chrome/41.0.2272.118 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    retry_n = 0
    while retry_n < 5:
        try:
            if _ex_hea:
                hea.update(_ex_hea)
            if _method.upper() == 'GET':
                res = requests.get(_url, data=data, params=param, headers=hea, timeout=(12.05, 72))
            elif _method.upper() == 'POST':
                res = requests.post(_url, data=data, headers=hea, timeout=(12.05, 54))
            elif _method.upper() == 'PUT':
                res = requests.put(_url, data=data, headers=hea, timeout=(12.05, 54))
            elif _method.upper() == 'DELETE':
                res = requests.delete(_url, data=data, headers=hea, timeout=(12.05, 54))
            else:
                print('TypeError')
                return None
        except requests.exceptions.SSLError:
            print("SSL 错误, 2s后重试 -> SSLError: An SSL error occurred.")
            time.sleep(2)
        except requests.exceptions.ConnectTimeout:
            print(
                "建立连接超时, 5s后重试 -> ConnectTimeout: The request timed out while trying to connect to the remote server.")
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


def read_url_list(_filename: str) -> list:
    with open(f'./{filename}', 'r', encoding='utf-8') as f:
        url_arr = f.read().split("\n")
    return url_arr


class Spider:
    def __init__(self):
        self.title = ""
        self.res_text = ""
        self.dl_urls = []
        self.dl_urls_err = []

    def run(self, _url_list: list):
        for url in _url_list:
            if not self.get_info(url):
                continue
            self.text_handle()
            self.save_dl_urls()
            if not _use_quiet_mode:  # 非静默模式下, 询问是否下载
                if not co.ask("是否开始下载"):
                    return None
            co.console_clear()
            if _use_aria2:
                self.download_aria2()
            else:
                self.download_regular()
            self.save_dl_urls_err()
            self.clean_vars()
            self.clean_files()

    def get_info(self, _url: str) -> bool:
        if _url.__len__() < 5:
            return False
        res = _requests("get", _url)
        if not res:
            return False
        res.encoding = "utf-8" if _use_utf8_res_encoding else "gbk"
        title_arr = re.findall('<title>(.*?) .*?</title>', res.text)
        dl_urls = re.findall("ess-data='(.*?)'", res.text)
        self.title = title_arr[0] if title_arr else "null"
        self.dl_urls = dl_urls if dl_urls else []
        print(f"即将显示提取到的内容, 共 {len(self.dl_urls)} 个\n")
        time.sleep(1)
        for url in self.dl_urls:
            print(f"{url}")
        print(f"\n标题: {self.title}\n")
        return True

    def text_handle(self):
        if self.title.__len__() < 6:
            self.title = input("请输入标题:") if not _use_quiet_mode else time.strftime("%Y%m%d_%H%M%S")
        self.title = re.sub(r'[\\/:*?"<>|]', '_', self.title)

    def download_regular(self):
        print("\n================BEGIN================\n")
        if not os.path.exists("./" + self.title):
            os.mkdir("./" + self.title)
        print("目录已建立.\n")
        i = 0
        for url in self.dl_urls:
            suffix = url.split("/")[-1].split(".")[-1]
            suffix = re.sub(r'[\\/:*?"<>|]', '_', suffix)
            response = _requests("get", url)
            print(i, response)
            if response.status_code == 200:
                with open(f"./{self.title}/{str(i).zfill(3)}.{suffix}", "wb") as f:
                    f.write(response.content)
            else:
                self.dl_urls_err.append(url)
            i += 1
            time.sleep(1.2)
        print("\n=================END=================\n")

    def download_aria2(self):
        try:
            print("================BEGIN================")
            run_path = os.getcwd()
            os.system("aria2c -i %s/dl_urls.txt -d %s/%s" % (run_path, run_path, self.title))
        except Exception:
            print("ERROR!")
            time.sleep(3)

    def save_dl_urls(self):
        if self.dl_urls:
            with open("./dl_urls.txt", "w", encoding="utf-8") as f:
                for url in self.dl_urls:
                    f.write(f"{url}\n")

    def save_dl_urls_err(self):
        if self.dl_urls_err:
            with open("./dl_urls_err.txt", "a", encoding="utf-8") as f:
                f.write("\n")
                f.writelines(self.dl_urls_err)

    def clean_vars(self):
        self.title = ""
        self.res_text = ""
        self.dl_urls_err.clear()
        self.dl_urls.clear()

    @staticmethod
    def clean_files():
        if _use_quiet_mode:  # 静默模式下不执行删除文件
            return None
        if co.ask("是否删除 dl_urls.txt"):
            os.remove("./dl_urls.txt") if os.path.exists("./dl_urls.txt") else print("File Not Found")
        if co.ask("是否删除 dl_urls_err.txt"):
            os.remove("./dl_urls_err.txt") if os.path.exists("./dl_urls_err.txt") else print("File Not Found")


class ConsoleTools(object):
    def __init__(self):
        self.sysinfo = self._check_platform()

    @staticmethod
    def _check_platform():
        check_result = platform.system()
        if "indows" in check_result:
            return "W"
        elif "inux" in check_result:
            return "L"

    def console_clear(self):
        if self.sysinfo == "W":
            os.system("cls")
        elif self.sysinfo == "L":
            os.system("clear")

    @staticmethod
    def ask(_text) -> bool:
        inp = input(f"{_text} (y/n) : ")
        if inp in ("y", "Y"):
            return True
        elif inp in ("n", "N"):
            return False
        else:
            return False


if __name__ == '__main__':
    os.chdir(sys.path[0])
    url_list = []
    filename = ""
    try:
        options()
        if filename:  # 指定文件名时, 从文件读入目标地址
            url_list = read_url_list(filename)
        co = ConsoleTools()
        sp = Spider()
        sp.run(url_list)
    except KeyboardInterrupt:
        print("\n[#] 捕获 KeyboardInterrupt, 终止")
    print("\n[+] 程序运行完毕")
