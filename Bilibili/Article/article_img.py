import requests
import re
import sys
import os
import time


def Download():
    print("开始下载......")
    i = 1
    # 建立以时间命名的目录
    #
    # ----获取系统时间 年 月 日
    ymd = time.strftime("%Y%m%d", time.localtime(time.time()))
    # ---- 获取系统时间 小时 分钟 秒。 输出：120043
    hms = time.strftime("%H%M%S", time.localtime(time.time()))
    #
    path = str(ymd)+"_"+str(hms)
    os.mkdir("./"+path)
    print("目录已建立："+path)
    #
    # 逐行读取url.txt中的链接文本，
    urlfile = open("./url.txt", "r")
    lines = urlfile.readlines()
    for line in lines:
        # 重要！！下面这句使用了strip方法
        # 目的是移除line开头和结尾的换行符、空格等
        # 否则在requests.get里面会出现404错误
        line = line.strip()
        print("\n\n"+line)
        # 使用try对下载部分进行异常处理
        try:
            # 用requests.get下载图片
            # 设置timeout防止卡住，第一个是连接时间，第二个是读取时间
            response = requests.get(line, headers=hea, timeout=(12, 60))
            # 取response中二进制数据
            img = response.content
            print(response)
            #
            for j in range(1, 100):
                f = open("./"+path+"/"+str(i)+".png", "wb")
                f.write(img)
                f.close
        # try中的语句如果出现异常，则执行except里面的代码
        except:
            # 输出出错的链接到errors.txt,并提示
            data2 = open("./errors.txt", "a", encoding='utf-8')
            data2.write(line+"\n")
            data2.close
            print("!!!出现错误!!!\n出错链接已保存至errors.txt")
            # 使用continue跳过本次出错的循环
            continue
        i += 1


def Getsource():
    inputurl = input('请输入网址(含http)：')
    html = requests.get(inputurl, headers=hea, timeout=(72, 120))
    #
    # 转为utf-8编码
    html.encoding = 'utf-8'
    #
    # 输出获取的源码
    print("即将显示网页源码\n")
    time.sleep(2)
    print(html.text)
    #
    # 输出源码到文件
    data0 = open("./source.html", 'w+', encoding='utf-8')
    print(html.text, file=data0)
    data0.close()
    #
    # 延迟2秒后清屏
    time.sleep(2)
    # os.system('clear') #for Unix
    os.system('cls')  # for Windows
    #
    
    # PART 1 此为 正则表达式 部分。(写在''里面)。找到规律，利用正则，内容就可以出来 ps.注意表达式里的空格。
    text = re.findall('meta itemprop="image" content="(.*?)"', html.text)
    #
    # 输出正则提取结果至文件
    data1 = open("./url.txt", "a", encoding='utf-8')
    for each in text:
        print(each)
        # 逐行写入保存到文本文件
        data1.write(each+"\n")

    # PART 2 此为 正则表达式 部分。(写在''里面)。找到规律，利用正则，内容就可以出来 ps.注意表达式里的空格。
    text = re.findall('img data-src="(.*?)" width="', html.text)
    #
    # 输出正则提取结果至文件
    data1 = open("./url.txt", "a", encoding='utf-8')
    for each in text:
        print("http:"+each)
        # 逐行写入保存到文本文件
        data1.write("http:"+each+"\n")

def Delfiles():
    while True:
        # 删除文件
        print("\n####文件删除选项####\n")
        print("1.删除 url.txt\n2.删除 errors.txt\n3.删除两者\n4.保留两者")
        str_s2 = "\n\n选择："
        str_in2 = input(str_s2)
        if str_in2 in ('1'):
            os.remove("./url.txt")
            break
        if str_in2 in ('2'):
            os.remove("./errors.txt")
            break
        if str_in2 in ('3'):
            os.remove("./url.txt")
            os.remove("./errors.txt")
            break
        if str_in2 in ('4'):
            break


#
#
# ==================================
# ===============main===============
# ==================================
#
#
# 设置hea，即useragent，让目标网站误以为本程序是浏览器，并非爬虫。
# 从网站的Requests Header中获取。审查元素
hea = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}


# 获取网页源码
Getsource()
#
# 下载文件
str_s1 = "\n是否下载文件? (y/n)\n选择："
while True:
    str_in1 = input(str_s1)
    if str_in1 in ('N', 'n'):
        break
    if str_in1 in ('Y', 'y'):
        Download()
        break
#
print("\n*****运行完毕~*****")
#
# 删除文件？
Delfiles()
