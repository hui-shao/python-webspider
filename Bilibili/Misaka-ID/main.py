import requests
import json
import time
import random

if __name__ == "__main__":
    start = time.time()
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
    f = open("./lists.txt", "w+", encoding="utf-8")
    for i in range(1, 2000):
        par = {
            "nickName": "御坂" + str(i) + "号"
        }
        try:
            res = requests.get(url=url, params=par, headers=hea, timeout=5)
        except KeyboardInterrupt:
            print("Cancled")
            break
        except requests.exceptions.ConnectTimeout:
            print("timeout", i)
            timeout.append(i)
            continue
        except Exception as err:
            print("Error！ %d\n" % i, err)
            errs.append(i)
            continue
        else:
            result = json.loads(res.text)
            if result["code"] == 0:
                print("available", i)
                lst_available.append(i)
            else:
                print("unavailable", i)
                lst_unavailable.append(i)
        a = str(lst_available)
        f.seek(0)
        f.write("Available: " + str(lst_available) + "\nUnavailable: " + str(lst_unavailable) + "\nTimeout: " + str(
            timeout) + "\nError: " + str(errs))
        f.write("\n\nAvailable_count = %d\nUnavailable_count = %d" % (len(lst_available), len(lst_unavailable)))
        if i % 500 == 0:
            f.flush()
        if i % 100 == 0:
            time.sleep(random.randint(10, 30))
        else:
            time.sleep(random.random())
    f.close()
    end = time.time()
    print("\n\nFinished.  Total time:", end - start)
