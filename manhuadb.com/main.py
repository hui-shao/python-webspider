# -*- coding: UTF-8 -*-
# @Time    : 2020/10/5 10:59
# @Author  : Hui-Shao

import os
import re
import time
import base64
import traceback

import Tools
import requests

# Some vars
DirPath = "./Downloads/"  # 文件存储目录 注意以 / 结尾
URL = "https://www.manhuadb.com/manhua/10817"
SCKEY = ""  # 用于server酱消息推送，若不需要请保持现状
SaveImgUrl = True  # 是否保存相应章节的图片下载地址
Aria = False  # 是否使用aria下载


class Spider:
    def __init__(self):
        self.hea = {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
        }
        self.book_name = ""  # 整本书的名字
        self.chapter_info_arr = []  # 每个元素为tuple, 链接+标题
        self.chapter_url = ""  # 初始化 每个章节页面自身的url
        self.chapter_title = ""  # 初始化 每个章节页面自身的标题
        self.chapter_img_urls = []  # 初始化 存储每一章节中所有图片的url
        self.dirpath_sub = ""  # 初始化 存储图片的二级路径 实际上后续会被赋值为：DirPath + self.title
        self.err_list_total = []  # 记录错误链接（每完成一话会，并将错误写入文件后列表会清空）
        self.err_total_count = 0  # 记录错误总数

    def run(self):
        time_start = time.time()
        print("START...")
        # 以下 获取每一话的一些基本信息
        print("获取基本信息中...")
        print(URL)
        if not self.get_chapter_num(URL):
            print("获取章节信息失败，程序终止")
            exit()
        for a in self.chapter_info_arr:
            print("正在获取每一话内所有图片的下载地址...")
            self.chapter_url, self.chapter_title = "https://www.manhuadb.com" + a[0], a[1]
            print(f"当前进度: {self.chapter_title}  {self.chapter_url}")
            self.dirpath_sub = DirPath + self.book_name + "/" + self.chapter_title + "/"
            self.mkdir()  # 建立文件夹
            if "error" in self.get_chapter_imgurls():  # 检查返回值，如果获取必要信息环节出错,跳过此次循环
                print("获取信息失败，跳过此次循环")
                continue
            if SaveImgUrl:
                print("\n正在保存下载地址...")
                self.save_imgurl(self.chapter_img_urls)
            if Aria and SaveImgUrl:  # 判断是否使用aria下载
                print("已将下载指令传递至aria2 请自行检查")
                os.system(f"aria2c -i {self.dirpath_sub}url.txt -d {self.dirpath_sub}")
            else:
                print("下载开始...")
                count = 1
                for url in self.chapter_img_urls:
                    self.download(_url=url, _count=count)
                    if count % 15 == 0:
                        print("暂停一下...")
                        # time.sleep(3)  # debug only
                        time.sleep(10)
                    count += 1
                self.write_err_total()  # 每完成一话，将所有错误信息写入到 $DirPath 下的 Errors_total.txt 文件
            print("\n%s Finished.\nContinue after 5s..." % self.chapter_title)
            time.sleep(5)
            tool.console_clear()  # 清屏
            self.chapter_img_urls = []  # 每下载完成一话，清空链接列表
        # 以下 下载完成之后..
        total_time = time.time() - time_start
        print("\n\n====================\n")
        print("All Finished.\nTotal errors: %d\nTotal time： %.4f s" % (self.err_total_count, total_time))
        msgtool.send_wxmsg(SCKEY, "爬虫任务通知", "All Finished.\n\nTotal errors: %d\n\nTotal time： %.4f s\n" % (
            self.err_total_count, total_time))  # server酱消息推送
        input("Press ENTER to Exit..")

    def get_chapter_num(self, _url):
        """
        用于获取每一话的页面地址
        :param _url: 目标网页url
        :return: 若无异常返回True,否则false
        :var: self.chapter_info_arr 存储章节信息的数组
        :var: self.book_name 整本书的名字
        """
        hea = self.hea
        err_status = 0
        retry_n = 0
        while retry_n <= 3:
            if retry_n != 0:
                print("Retry: ", retry_n)
            try:
                res = requests.get(url=_url, headers=hea, timeout=30)
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
                print("Timeout")
                err_status = 1
                retry_n += 1
                print("10s后继续...")
                # time.sleep(5)  # debug only
                time.sleep(10)
            except Exception as err_info:
                print("Error\n", err_info)
                err_status = 2
                retry_n += 1
                print("15s后继续...")
                # time.sleep(5)  # debug only
                time.sleep(15)
            else:
                err_status = 0
                self.book_name = re.findall(r'<h1 class="comic-title">(.*?)</h1>', res.text)[0]
                self.chapter_info_arr = re.findall(r'<a class="fixed-a-es" href="(.*?)" title="(.*?)">', res.text)
                break
        if err_status == 1:
            self.err_list_total.append("网络连接错误|获取章节信息|链接|%s" % _url)
            return False
        elif err_status == 2:
            self.err_list_total.append("其他错误|获取章节信息|链接|%s" % _url)
            return False
        else:
            return True

    def get_chapter_imgurls(self):
        """
        用于获取xx话的所有图片下载地址
        :return: 若出现异常，返回error文本
        :var: self.chapter_img_urls
        """
        hea = self.hea
        res = ""
        err_status = 0
        retry_n = 0
        while retry_n <= 3:
            if retry_n != 0:
                print("Retry: ", retry_n)
            try:
                res = requests.get(url=self.chapter_url, headers=hea, timeout=15)
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
                print("Timeout")
                err_status = 1
                retry_n += 1
                print("10s后继续...")
                # time.sleep(5)  # debug only
                time.sleep(10)
            except Exception as err_info:
                print("Error\n", err_info)
                err_status = 1
                retry_n += 1
                print("15s后继续...")
                # time.sleep(5)  # debug only
                time.sleep(15)
            else:
                try:
                    result = re.findall(r"<script>var img_data = '(.*?)';</script>", res.text)[0]
                    img_urls_info = eval(base64.b64decode(result))
                    img_host_and_pre = re.findall(r'data-host="(.*?)".*?data-img_pre="(.*?)">', res.text)
                    for dict_n in img_urls_info:
                        self.chapter_img_urls.append(
                            img_host_and_pre[0][0] + img_host_and_pre[0][1] + dict_n["img"])  # 生成url数组
                except IndexError:
                    err_status = 2
                else:
                    err_status = 0
                break
        if err_status == 1:
            self.err_list_total.append("Request错误|请求图片地址|链接|%s" % res.url)  # 如果有错误，设置 img_url 包括 “error” 文本，用于后续检测
            return "Request.get_error"
        elif err_status == 2:
            self.err_list_total.append("正则匹配错误|请求图片地址|链接|%s" % res.url)
            return "Re.findall_error"
        else:
            return "success"

    def mkdir(self):
        """
        This function will make dirs to save files and set some vars about path
        You must run it before save_imgurl() and downlload()
        :return:
        """
        if not os.path.exists(DirPath):
            os.makedirs(DirPath)
        if not os.path.exists(self.dirpath_sub):
            os.makedirs(self.dirpath_sub)

    def download(self, _url, _count):
        if "error" in _url:
            return None
        start = time.time()
        hea = self.hea
        err_status = 0
        retry_n = 0
        while retry_n <= 3:
            if retry_n != 0:
                print("Retry: ", retry_n)
            try:
                pic = requests.get(_url, headers=hea, timeout=60)
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
                print("Image:%d Timeout!" % _count)
                err_status = 1
                retry_n += 1
                print("10s后继续...")
                # time.sleep(5)  # debug only
                time.sleep(10)
            except Exception:
                print("Image:%d Error!" % _count)
                err_status = 2
                retry_n += 1
                print("10s后继续...")
                # time.sleep(5)  # debug only
                time.sleep(10)
            else:
                err_status = 0
                pic_file = open(self.dirpath_sub + str(_count).zfill(3) + ".jpg", "wb")
                pic_file.write(pic.content)
                pic_file.close()
                end = time.time()
                print("Image:%d Finished.  Cost: %.4f s" % (_count, end - start))
                break
        if err_status != 0:
            errurl_file = open(self.dirpath_sub + "errors.txt", "a", encoding='utf-8')
            errurl_file.write("%d.jpg|%s" % (_count, _url) + "\n")
            errurl_file.close()
            self.err_list_total.append("%s|图片下载错误|%d.jpg|%s" % (self.chapter_title, _count, _url))
            return 1  # 返回值暂时还没有用...
        return 0

    def save_imgurl(self, _imgurls):
        """
        :param _imgurls: 接受一个下载地址列表，将其逐行写入文件
        :return: 无
        """
        imgurl_file = open(self.dirpath_sub + "url.txt", "w+", encoding='utf-8')
        for each in _imgurls:
            imgurl_file.write(each + "\n")
        imgurl_file.close()

    def write_err_total(self):
        count = len(self.err_list_total)
        if count > 0:
            errtotal_file = open(DirPath + "Errors_total.txt", "a", encoding="utf-8")
            for each in self.err_list_total:
                errtotal_file.write(each + "\n")
            errtotal_file.close()
            self.err_total_count += count  # 把当前错误数计入总数
            self.err_list_total = []  # 写入完成后清空错误列表
        else:
            pass


if __name__ == '__main__':
    try:
        tool = Tools.ConsoleTools()
        msgtool = Tools.MsgTools()
        spider = Spider()
        spider.run()
    except KeyboardInterrupt:
        print("\n\nRaised KeyboardInterruption.\nExit!")
    except Exception:
        traceback.print_exc()
