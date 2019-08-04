import requests,re,sys,os,time

def Download():
    print("开始下载......")
    i = 1

    #逐行读取url.txt中的链接文本，
    urlfile = open("./url.txt","r")
    lines = urlfile.readlines()
    for line in lines:
        #重要！！下面这句使用了strip方法
        #目的是移除line开头和结尾的换行符、空格等
        #否则在requests.get里面会出现404错误
        line = line.strip()
        print("\n"+line)
        
        #用requests.get下载图片
        response = requests.get(line,headers = hea)
        #取response中二进制数据
        img = response.content
        print(response)
        
        for j in range(1,100):
            f = open("./"+str(i)+".jpg","wb")
        f.write(img)
        i += 1




def Getsource():

    inputurl = input('请输入网址(含http)：')
    html = requests.get(inputurl,headers = hea)

    #转为utf-8编码
    html.encoding = 'utf-8'

    #输出获取的源码
    print(html.text)

    #输出源码到文件
    data0=open("./source.html",'w+') 
    print(html.text,file=data0)
    data0.close()

    #延迟2秒后清屏
    time.sleep(2)
    os.system('clear')

    #此为正则表达式部分。(写在''里面)。找到规律，利用正则，内容就可以出来
    text = re.findall('src="(.*?)" ',html.text)

    #分组显示
    data1 = open("./url.txt","a")
    for each in text:
        print(each)
        #逐行写入保存到文本文件
        data1.write(each+"\n")
    data1.close




def Delurl():
    #删除文件
    str_s2 = "\n是否删除url.txt? (y/n)\n选择："
    while True:
        str_in2 = input(str_s2)
        if str_in2 in ('N', 'n'):
            break
        if str_in2 in ('Y', 'y'):
            os.remove("./url.txt")
            break







#设置hea，即useragent，让目标网站误以为本程序是浏览器，并非爬虫。
#从网站的Requests Header中获取。审查元素
hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}


#获取网页源码
Getsource()

#下载文件
str_s1 = "\n是否下载文件? (y/n)\n选择："
while True:
    str_in1 = input(str_s1)
    if str_in1 in ('N', 'n'):
        break
    if str_in1 in ('Y', 'y'):
        Download()
        break

#删除 url.txt
Delurl()
