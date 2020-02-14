import requests
import json
import re
import time
import os
import platform


def get_book_info(_shelfId):
    '''
    用于获取“一个书架”上面的每本书的信息，返回书本名称和书本id
    '''
    url_1 = "https://mp.codeup.cn/book/shelf.htm"
    param_1 = {"id": "%s" % (_shelfId), "mallId": "263"}
    headers_1 = {
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://mp.codeup.cn/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1; OPPO R9tm Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043128 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D PA QQ/7.0.0.3135 NetType/4G WebP/0.3.0 Pixel/1080"
    }
    try:
        response_1 = requests.get(url_1, headers=headers_1, params=param_1, timeout=(72, 120))
    except requests.exceptions.ConnectionError:
        print("网络连接错误")
    _name_s = re.findall(r'<div class="book-list-item-name">(.*?)</div>', response_1.text)
    _name_s.remove("'+v.bookName+'")
    _book_id_s = re.findall(r'<div class="book vis" ebook-id="(\d*?)"  onclick', response_1.text)
    return _name_s, _book_id_s


def get_img_lists(_book_id, _shelf_id):
    url_2 = "https://biz.bookln.cn/ebookpageservices/queryAllPageByEbookId.do"
    data_2 = {"ebookId": "%s" % (_book_id)}
    headers_2 = {
        "content-length": "118",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "origin": "http://mp.codeup.cn",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded",
        "referer": "http://mp.codeup.cn/book/sample.htm?id=%s&shelfId=%s&mallId=263" % (_book_id, _shelf_id),
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    try:
        response_2 = requests.post(url_2, headers=headers_2, data=data_2, timeout=(72, 120))
    except requests.exceptions.ConnectionError:
        print("网络连接错误")
    _img_list = []
    _pageNo_list = []
    dic = json.loads(response_2.text)
    num = len(dic["data"]["data"])
    for i in range(0, num):
        img_single = dic["data"]["data"][i]["imgurl"]
        _img_list.append(img_single)
        pageNo_single = dic["data"]["data"][i]["pageNo"]
        _pageNo_list.append(pageNo_single)
    return _img_list, _pageNo_list


def download_directly(_download_url, _dirname, _file_num):
    '''
    使用requests库下载文件，支持自动保存错误链接
    :_dirname 保存文件的目录
    :_file_num 保存的文件名
    '''
    print(_download_url)
    try:
        response = requests.get(_download_url, headers=download_hea, timeout=(72, 120))
        img = response.content
        print(response)
        print(str(_file_num))
        with open("./"+_dirname+"/"+str(_file_num)+".jpg", "wb") as f_1:
            f_1.write(img)
    except Exception:
        # 输出出错的链接到errors.txt,并提示
        f_2 = open("./"+_dirname+"/errors.txt", "a", encoding='utf-8')
        f_2.write(_download_url+"\n")
        f_2.close
        print("ERROR!\n出错链接已保存至errors.txt")
        time.sleep(3)


def download_aria():
    pass


def clean():
    '''
    用于控制台清屏
    '''
    if sys_type == "Windows":
        os.system("cls")
    elif sys_type == "Linux":
        os.system("clear")


def define_vars():
    '''
    定义一些全局变量
    '''
    # 以下变量主要被用于 __main__
    global shelf_ids
    shelf_ids = ["2528", "2529", "2530", "2531", "2558", "2559", "2571", "2572", "2573"]
    # 以下变量主要被用于 clean()
    global sys_type
    sys_type = platform.system()
    # 以下变量主要被用于 download_directly()
    global download_hea
    download_hea = {
        "sec-fetch-dest": "image",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36",
        "accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }


if __name__ == "__main__":
    define_vars()  # 初始化一下变量
    for shelf_id in shelf_ids:
        # 获取书本名称和书本id
        r_1 = get_book_info(shelf_id)
        name_s = r_1[0]
        book_id_s = r_1[1]
        flag_1 = 0  # book_id_s 列表中的序号
        for name in name_s:
            print("当前书本："+name)
            book_id = book_id_s[flag_1]
            print("该书本id："+book_id)
            # 获取对应的一本书的每一页的下载地址（列表）
            print("开始获取下载地址……")
            r_2 = get_img_lists(_book_id=book_id, _shelf_id=shelf_id)
            print("OK.")
            img_list = r_2[0]
            pageNo_list = r_2[1]
            print("================开始下载================")
            # 建立目录
            if not os.path.exists("./"+name):
                os.mkdir("./"+name)
            print("目录已建立")
            flag_2 = 0  # pageNo_list 列表中的序号
            for img_url in img_list:
                pageNo = pageNo_list[flag_2]
                download_directly(_download_url=img_url, _dirname=name, _file_num=pageNo)
                time.sleep(1)
                flag_2 = flag_2 + 1
            print("=================下载完成=================\n")
            flag_1 = flag_1 + 1
        input("按任意键继续下一本书>>>")
        clean()
