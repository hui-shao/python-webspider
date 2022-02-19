import requests
import os
import sys
import time

path_s = "downloads"
suffix = "mp3"
start_n = 8
stop_n = 1000  # 开区间
zfill_n = 3
base_url = "https://appcourse.sflep.com/1631af1315be413d99cfa06e75969278/media/1/sen_3u1_p2_txta_"
hea = {
    "user-agent": "Mozilla/5.0 (Linux; Android 9; MI 6 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.85 Mobile Safari/537.36"
}

if __name__ == '__main__':
    os.chdir(sys.path[0])
    n_404 = 0
    err_list = []
    for i in range(start_n, stop_n, 1):
        i_s = str(i).zfill(zfill_n)
        url = f"{base_url}{i_s}.{suffix}"
        try:
            res = requests.get(url=url, headers=hea, params=str(round(time.time() * 1000)))
            if res.status_code == 206 or res.status_code == 200:
                print(f"Current: {i_s}.{suffix}")
                if not os.path.exists(f"./{path_s}"):
                    os.mkdir(f"./{path_s}")
                with open(f"./{path_s}/{i_s}.{suffix}", "wb") as f:
                    f.write(res.content)
                n_404 = 0
            elif res.status_code == 404:
                n_404 += 1
                if n_404 >= 5:
                    print("Finished")
                    break
                else:
                    print(f"404 On {i_s}.{suffix}")
                    err_list.append(f"{i_s}.{suffix}")
                    continue
        except requests.exceptions.RequestException:
            print(f"网络连接错误 {i_s}.{suffix}")
            err_list.append(f"{i_s}.{suffix}")
