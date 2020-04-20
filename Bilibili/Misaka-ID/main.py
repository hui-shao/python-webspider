import requests
import json
import time
import random
import sys
import getopt

# 一些默认的参数
sckey = ""  # 用于 servre酱 消息推送，若不需要，无需修改保持现状
prefix = "御坂"
suffix = "号"
zfill_n = 0
chk_range = "1,20001"  # 闭区间
filename_out = "lists.txt"
# 以下一般无需修改
url = "https://passport.bilibili.com/web/generic/check/nickname"
hea = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/80.0.3987.132 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"
}
help_info = '''
    -r [--range]       编号检测范围(闭区间,英文逗号分隔) 
                           例如: --range=1,200    表示从 1 检测到 200
    -p [--prefix]      名称前缀
    -s [--suffix]      名称后缀
    -z [--zfill]       将编号补齐的位数
                           例如: --zfill=5        会将 1 补齐为 00001
    -k [--key]         用于 "server酱" 推送的sckey (push token)
    -f [--filename]    用于设置保存结果的文件名 默认为 lists.txt
'''


def options():
    """用于处理传入参数"""
    print("")
    global chk_range, prefix, suffix, zfill_n, sckey, filename_out
    opts, args = getopt.getopt(sys.argv[1:], '-h-r:-p:-s:-z:-k:-f:',
                               ['help', 'range=', 'prefix=', 'suffix=', 'zfill=', 'key=', 'filename='])
    if len(opts) < 1:  # 若未接收到已经预设的命令行参数，则直接采用默认参数
        print("[*] 未检测到传入参数，采用默认格式，如 御坂2233号\n")
        return 0
    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            print("[+] Help info :\n" + help_info)
            exit()
        if opt_name in ('-r', '--range'):
            print("[+] 范围: ", opt_value)
            chk_range = str(opt_value)
            continue
        if opt_name in ('-p', '--prefix'):
            print("[+] 前缀: ", opt_value)
            prefix = str(opt_value)
            continue
        if opt_name in ('-s', '--suffix'):
            print("[+] 后缀: ", opt_value)
            suffix = str(opt_value)
            continue
        if opt_name in ('-z', '--zfill'):
            print("[+] 补齐位数: ", opt_value)
            zfill_n = int(opt_value)
            continue
        if opt_name in ('-k', '--key'):
            sckey = str(opt_value)
            print("[+] Sckey: ", sckey[:12] + "*" * (len(sckey) - 6 - 12) + sckey[(len(sckey) - 6):])
            continue
        if opt_name in ('-f', '--filename'):
            filename_out = str(opt_value)
            print("[+] 输出文件名: ", filename_out)
            continue
    print("")


def send_wxmsg(_sckey, _title="misaka", _context="正文"):
    url_postmsg = "https://sc.ftqq.com/%s.send" % _sckey
    _context = _context + "\n\n" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    data = {
        "text": "%s" % _title,
        "desp": "%s" % _context
    }
    try:
        res = requests.post(url=url_postmsg, data=data)
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
                break
            elif result["code"] == 2001 or result["code"] == 40014:
                print(i, "unavailable")
                lst_unavailable.append(i)
                break
            else:
                print(i, "unknown")
                error_status = 3
                retry_n += 1
                time.sleep(3)
    # 以下--循环(异常重试)结束后 对错误状态进行判断 并写入列表
    if error_status == 1:
        timeout.append(i)
    elif error_status == 2:
        errs.append(i)
    elif error_status == 3:
        lst_unknown.append(i)
    if (i % 20 == 0) or (i + 1 == i_end):
        # 每检测20个写一次文件
        write_result()


def write_result():
    f.seek(0)
    f.write("Available: " + str(lst_available) + "\nUnavailable: " + str(lst_unavailable) + "\nTimeout: " + str(
        timeout) + "\nError: " + str(errs) + "\nUnknown: " + str(
        lst_unknown) + "\n\nAvailable_count = %d\nUnavailable_count = %d\n" % (
                len(lst_available), len(lst_unavailable)))
    f.flush()


def sleep():
    if i == 0:
        return 0
    if i % 100 == 0:
        sleep_time_1 = random.randint(5, 15)
        print("\n达到整百，随机暂停 %d s\n" % sleep_time_1)
        time.sleep(sleep_time_1)
    elif i % 10 == 0:
        time.sleep(random.uniform(0.2, 0.6))  # 取0.2-0.7之间的随机float
    else:
        time.sleep(0.02)


def loop(_start_n, _end_n):
    global i, par
    for i in range(_start_n, _end_n):
        par = {"nickName": "%s" % (prefix + str(i) + suffix)}  # request.get 参数
        check()
        sleep()


def loop_zfill(_start_n, _end_n):
    global i, par
    for i in range(_start_n, _end_n):
        par = {"nickName": "%s" % (prefix + str(i).zfill(zfill_n) + suffix)}  # request.get 参数
        check()
        sleep()


if __name__ == "__main__":
    # Some vars
    start_time = time.time()
    options()
    i = 1  # 初始化检测编号
    lst_available = []
    lst_unavailable = []
    lst_unknown = []
    timeout = []
    errs = []
    par = {}
    chk_range = chk_range.split(",")
    i_start = int(chk_range[0])
    i_end = int(chk_range[1]) + 1
    # run
    f = open("./" + filename_out, "w+", encoding="utf-8")
    try:
        if zfill_n == 0:  # 判断是否补齐0位，并进入for循环
            loop(i_start, i_end)
        else:
            loop_zfill(i_start, i_end)
    except KeyboardInterrupt:
        print("\nRaised Control-C.  Cancled!\n")
    except Exception as err_info_1:
        print("\nError!\n", err_info_1)
    else:
        total_time = time.time() - start_time
        print("\n\nFinished\nTotal time: %f s\n" % total_time)
        if not sckey == "":
            print("Server酱推送中...")
            send_wxmsg(_sckey=sckey, _title="Misaka-ID", _context="Finished.\n\nTotal time: %f s" % total_time)
    f.write("\n\nType: " + prefix + r"%d" + suffix + "  --zfill=%d\n" % zfill_n)
    f.close()
