import requests
import re
import os
import time


def Getsource_rootpage():
    rootpage_url = input('请输入网址(含http)：')
    rootpage_subpage_html = requests.get(rootpage_url, headers=hea, timeout=(72, 120))
    rootpage_subpage_html.encoding = 'utf-8'
    # print("即将显示网页源码\n")
    # time.sleep(2)
    # print(rootpage_subpage_html.text)
    data0 = open("./source_1024.html", 'w+', encoding='utf-8')
    print(rootpage_subpage_html.text, file=data0)
    data0.close()
    time.sleep(2)
    os.system('clear')  # for linux
    text = re.findall("ess-data='(.*?)'", rootpage_subpage_html.text)
    get_title = re.findall('<title>(.*?) .*?</title>',rootpage_subpage_html.text)
    #get_title = re.findall(r'<title>(.*?\d{1,3}P.*?\]) ', rootpage_subpage_html.text)
    #
    print("即将显示提取到的内容\n")
    print("共"+str(len(text))+"个")
    time.sleep(2)
    #
    data1 = open("./url.txt", "w+", encoding='utf-8')
    for each in text:
        print(each)
        data1.write(each+"\n")
    data1.close
    return get_title


def DownloadIMG(download_url):
    try:
        print("================BEGIN================")
        print(download_url)
        response = requests.get(download_url, headers=hea, timeout=(72, 120))
        img = response.content
        print(response)
        print(str(i))
        print("=================END=================\n")
        #
        f = open("./"+title+"/"+str(i)+".jpg", "wb")
        f.write(img)
        f.close
    except Exception:
        # 输出出错的链接到errors.txt,并提示
        data2 = open("./errors.txt", "a", encoding='utf-8')
        data2.write(download_url+"\n")
        data2.close
        print("ERROR!\n出错链接已保存至errors.txt")
        time.sleep(3)


def Delfiles():
    while True:
        # 删除文件
        print("\n####文件删除选项####\n")
        print("1.删除 url.txt\n2.删除 errors.txt\n3.删除html\n99.全部清空\n0.退出")
        str_s2 = "\n\n选择："
        str_in2 = input(str_s2)
        if str_in2 in ('1'):
            if os.path.exists("./url.txt") is True:
                os.remove("./url.txt")
            else:
                print("文件不存在")
                time.sleep(2)
        if str_in2 in ('2'):
            if os.path.exists("./errors.txt") is True:
                os.remove("./errors.txt")
            else:
                print("文件不存在")
                time.sleep(2)
        if str_in2 in ('3'):
            if os.path.exists("./source_1024.html") is True:
                os.remove("./source_1024.html")
            else:
                print("文件不存在")
                time.sleep(2)
        if str_in2 in ('99'):
            os.system("rm ./*.txt")
            os.system("rm ./*.html")
        if str_in2 in ('0'):
            break


'''
==================================
===============main===============
==================================
'''
# global variables
hea = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (Ksubpage_html, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
title_list = Getsource_rootpage()
title = ",".join(title_list)
# title = title.encode('utf-8')
if len(title) <5:
    title = input("输入标题: ")
print("\n标题：")
print(title)
i = 1
while True:
    str_in1 = input("是否下载(y/n)：")
    if str_in1 in ('y'):
        # PART.GETSOURCE-子网页subpage
        print("\n开始下载……")
        if not os.path.exists("./"+title):
            os.mkdir("./"+title)
        print("目录已建立")
        urlfile = open("./url.txt", "r")
        lines = urlfile.readlines()
        urlfile.close()
        for imgurl in lines:
            imgurl = imgurl.strip()
            DownloadIMG(imgurl)
            time.sleep(1.5)
            i = i+1
        break
    if str_in1 in ('n'):
        print("下载取消")
        break


# 删除文件
Delfiles()
