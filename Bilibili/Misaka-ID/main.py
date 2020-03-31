import requests
import json
import time
import random


def send_wxmsg(_sckey, _title="misaka", _context="正文"):
    url = "https://sc.ftqq.com/%s.send" % (_sckey)
    _context = _context + "\n\n" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    data = {
        "text": "%s" % (_title),
        "desp": "%s" % (_context)
    }
    try:
        res = requests.post(url=url, data=data)
        msg_back = json.loads(res.text)
        if msg_back["errmsg"] == "success":
            print("消息推送成功！")
        else:
            print("发送可能失败 返回值：%s" % (msg_back["errmsg"]))
    except Exception:
        print("消息发送错误")


def check():
    retry_n = 0
    error_status = 0
    while retry_n <= 3:
        if retry_n != 0:
            print("\nRetry:%d times:%d  :" % (i, retry_n))
        try:
            res = requests.get(url=url, params=par, headers=hea, timeout=10)
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
            print(i, "timeout")
            error_status = 1
            retry_n += 1
            time.sleep(2)
        except Exception as err_info:
            print("%d Error！\n" % i, err_info)
            error_status = 2
            retry_n += 1
            time.sleep(5)
        else:
            error_status = 0
            result = json.loads(res.text)
            if result["code"] == 0:
                print(i, "available")
                lst_available.append(i)
            else:
                print(i, "unavailable")
                lst_unavailable.append(i)
            break
    if error_status == 1:
        timeout.append(i)
    elif error_status == 2:
        errs.append(i)
    if i % 20 == 0:
        # 每检测20个写一次文件
        f.seek(0)
        f.write("Available: " + str(lst_available) + "\nUnavailable: " + str(lst_unavailable) + "\nTimeout: " + str(timeout) + "\nError: " + str(errs) + "\n\nAvailable_count = %d\nUnavailable_count = %d\n" % (len(lst_available), len(lst_unavailable)))
        f.flush()


def sleep():
    if i % 100 == 0:
        sleep_time_1 = random.randint(5, 15)
        print("\n达到整百，随机暂停 %d s\n" % sleep_time_1)
        time.sleep(sleep_time_1)
    elif i % 10 == 0:
        time.sleep(random.uniform(0.2, 0.6))  # 取0.2-0.7之间的随机float
    else:
        time.sleep(0.02)


def loop():
    global i, par
    for i in range(1, 20002):
        par = {"nickName": "御坂" + str(i) + "号"}  # request.get 参数
        check()
        sleep()


if __name__ == "__main__":
    # Some vars
    sckey = ""  # 用于 servre酱 消息推送，若不需要，无需修改保持现状
    start_time = time.time()
    lst_available = []
    lst_unavailable = []
    timeout = []
    errs = []
    url = "https://passport.bilibili.com/web/generic/check/nickname"
    hea = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/80.0.3987.132 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    par = {"nickName": "御坂1号"}
    i = 1
    # run
    f = open("./lists.txt", "w+", encoding="utf-8")
    try:
        loop()  # 进入 for 循环
    except KeyboardInterrupt:
        print("\nRaised Control-C.  Cancled!\n")
    except Exception as err_info_1:
        print("\nError!\n", err_info_1)
    else:
        total_time = time.time() - start_time
        print("\n\nFinished\nTotal time: %f\n" % total_time)
        if not sckey == "":
            send_wxmsg(_sckey=sckey, _title="Misaka-ID", _context="Finished.\n\nTotal time: %f" % total_time)
    f.close()
