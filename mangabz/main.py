# -*- coding: UTF-8 -*-
import os
import re
import sys
import time

import Tools
import requests

# Some vars
SaveImgUrl = True
DirPath = "./Downloads/"  # 文件存储目录 注意以 / 结尾
URL = "http://www.mangabz.com/m"
START_N = 21715
END_N = 21720
SCKEY = ""  # 用于server酱消息推送，若不需要请保持现状
Aria = False


class Spider:
    def __init__(self):
        self.hea = {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
        }
        self.err_list_total = []  # 记录错误链接（每完成一话会，并将错误写入文件后列表会清空）
        self.err_total_count = 0  # 记录错误总数
        self.url = URL
        self.dirpath = DirPath  # 初始化 存储图片的一级路径
        self.dirpath_sub = ""  # 初始化 存储图片的二级路径 实际上后续会被赋值为：self.dirpath + self.title
        self.url_a = ""  # 拼接后的url 如 "http://www.mangabz.com/m21715"
        self.title = ""
        self.mid = ""
        self.cid = ""
        self.img_total = 0

    def run(self):
        imgurl_list = []
        time_start = time.time()
        print("START...")
        # 以下 获取每一话的一些基本信息
        for i in range(START_N, END_N + 1):  # 每一话的网页地址
            self.url_a = self.url + "%d/" % i  # 拼接后的url
            print("获取基本信息中...")
            print(self.url_a)
            getinfo_result = spider.get_info(self.url_a, i)
            if getinfo_result == 1:  # 检查返回值，如果获取必要信息环节出错,跳过此次循环
                print("获取信息失败，跳过此次循环")
                continue
            # 以下 获取一话内所有图片的下载地址，并生成列表
            print("获取所有图片下载地址中...")
            for page_n in range(1, self.img_total + 1):
                sys.stdout.write("\r第 %d 张，共 %d 张" % (page_n, self.img_total))
                sys.stdout.flush()
                imgurl = self.get_imgurl(self.url_a, self.cid, self.mid, self.img_total, page_n)
                imgurl_list.append(imgurl)
            # 以下 逐行保存图片下载地址列表为 txt
            if SaveImgUrl:
                print("\n将下载地址保存至 url.txt 中...")
                self.save_imgurl(imgurl_list)
            # 以下 遍历“图片下载地址”列表，开始下载
            print("下载开始...")
            count = 1
            for imgurl in imgurl_list:
                if "error" in imgurl:
                    count += 1
                    continue
                else:
                    self.download(imgurl, count)
                if count % 10 == 0:
                    print("暂停一下...")
                    # time.sleep(3)  # debug only
                    time.sleep(10)
                count += 1
            imgurl_list = []  # 下载完一话以后清空一下列表
            self.write_err_total()  # 每完成一话，将所有错误信息写入到 $DirPath 下的 Errors_total.txt 文件
            print("\n%s Finished.\nContinue after 5s..." % self.title)
            time.sleep(5)
            tool.console_clear()  # 清屏
        # 以下 下载完成之后..
        total_time = time.time() - time_start
        print("\n\n====================\n")
        print("All Finished.\nTotal errors: %d\nTotal time： %.4f s" % (self.err_total_count, total_time))
        msgtool.send_wxmsg(SCKEY, "爬虫任务通知", "All Finished.\n\nTotal errors: %d\n\nTotal time： %.4f s\n" % (
            self.err_total_count, total_time))  # server酱消息推送
        input("Press ENTER to Exit..")

    def get_info(self, _url, _count):
        """
        用于获取标题和一些关于漫画的信息，比如页数
        :param _count: 序号
        :param _url: 目标网页url
        :return: 若无异常，返回一个列表, 若出现异常，返回 1
        """
        hea = self.hea
        cookie = {"mangabz_lang": "2"}
        err_status = 0
        retry_n = 0
        while retry_n <= 3:
            if retry_n != 0:
                print("Retry: ", retry_n)
            try:
                res = requests.get(url=_url, headers=hea, cookies=cookie, timeout=30)
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
                self.title = re.findall(r'MANGABZ_CTITLE = "(.*?)";', res.text)[0]
                self.title = re.sub("^.*? ", "", self.title)  # 移除重复的漫画名
                self.title = "%d_" % _count + self.title  # 在目录名前加序号便于排序与区分
                self.mid = re.findall(r'MANGABZ_MID=(\d*?);', res.text)[0]
                self.cid = re.findall(r'MANGABZ_CID=(\d*?);', res.text)[0]
                self.img_total = int(re.findall(r'MANGABZ_IMAGE_COUNT=(\d*?);', res.text)[0])
                break
        if err_status == 1:
            self.err_list_total.append("网络连接错误|请求漫画信息|链接|%s" % _url)
            return 1
        elif err_status == 2:
            self.err_list_total.append("其他错误|请求漫画信息|链接|%s" % _url)
            return 1
        else:
            self.dirpath_sub = self.dirpath + self.title + "/"  # 设置 存储图片的二级路径
            self.mkdir()  # 创建文件夹
            return 0

    def get_imgurl(self, _url, _cid, _mid, _img_total, _page_n):
        """
        用于获取指定的xx话的图片下载地址
        :param _page_n: 页码数
        :param _mid:
        :param _img_total:总页数
        :param _cid:
        :param _url: 目标网页的url
        :return: 若无异常，返回img_url, 若出现异常，返回 1
        """
        url = _url + "chapterimage.ashx"
        hea = self.hea
        hea["Referer"] = "%s" % _url
        pars = {
            "cid": "%s" % _cid,
            "page": "%d" % _page_n,
            "key": "",
            "_cid": "%s" % _cid,
            "_mid": "%s" % _mid,
            "_dt": "%s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        }
        res = ""
        img_url = "Unchanged_error"  # 若该变量的值未被更改，即可认为出错
        err_status = 0
        retry_n = 0
        while retry_n <= 3:
            if retry_n != 0:
                print("Retry: ", retry_n)
            try:
                res = requests.get(url=url, params=pars, headers=hea, timeout=15)
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
                if _page_n < _img_total:
                    result = re.findall(r"dm5imagefun\|(.*?)\|\d+\|(.*?)\|\|function", res.text)
                else:
                    result = re.findall(r"pix\|(.*?)\|dm5imagefun\|(.*?)\|", res.text)
                try:
                    key = result[0][0]  # 异常处理，判断正则是否返回结果
                    img_name = result[0][1]
                except IndexError:
                    err_status = 2
                else:
                    err_status = 0
                    img_url = "http://image.mangabz.com/1/%s/%s/%s.jpg?cid=%s&key=%s&uk=" % (
                        _mid, _cid, img_name, _cid, key)
                break
        if err_status == 1:
            self.err_list_total.append("Request错误|请求图片地址|链接|%s" % res.url)  # 如果有错误，设置 img_url 包括 “error” 文本，用于后续检测
            img_url = "Request.get_error"
        elif err_status == 2:
            self.err_list_total.append("正则匹配错误|请求图片地址|链接|%s" % res.url)
            img_url = "Re.findall_error"
        return img_url

    def mkdir(self):
        """
        This function will make dirs to save files and set some vars about path
        You must run it before save_imgurl() and downlload()
        :return:
        """
        if not os.path.exists(self.dirpath):
            os.mkdir(self.dirpath)
        if not os.path.exists(self.dirpath_sub):
            os.mkdir(self.dirpath_sub)

    def download(self, _url, _count):
        hea = self.hea
        hea["Referer"] = self.url_a
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
                start = time.time()
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
            self.err_list_total.append("%s|图片下载错误|%d.jpg|%s" % (self.title, _count, _url))
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
            errtotal_file = open(self.dirpath + "Errors_total.txt", "a", encoding="utf-8")
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
    except Exception as error_info:
        print("\n\nERROR!\n", error_info)
