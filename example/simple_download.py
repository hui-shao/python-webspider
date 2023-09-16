import requests
import time
import random
import os
import sys
from urllib.parse import urlparse

err_url_list = []
path = "."
keep_raw_name = False


def get_filename_suffix(_url: str) -> []:
    temp1 = urlparse(_url).path
    filename_ = os.path.basename(temp1)
    suffix_ = os.path.splitext(temp1)[-1]
    return [filename_, suffix_]


def downloader(_url: str, _index: int, _path: str, _filename: str, _suffix: str) -> None:
    if not keep_raw_name:
        _filename = str(_index).zfill(5)
    hea = {
        "user-agent": "Mozilla/5.0 (Linux; Android 9; MI 6 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.85 Mobile Safari/537.36"
    }
    res = requests.get(url=_url, headers=hea)
    if res.status_code in (200, 206):
        with open("{}/{}{}".format(_path, _filename, _suffix), "wb") as file:
            file.write(res.content)
        print("[+] Success on {}".format(_index))
    else:
        err_url_list.append(_url)
        print("\n[!] Error on {}\n".format(_index))


if __name__ == '__main__':
    os.chdir(sys.path[0])
    with open("./urls.txt") as f:
        urls = list(map(lambda x: x.strip("\n"), f.readlines()))

    for i in range(0, len(urls)):
        url = urls[i]
        filename, suffix = get_filename_suffix(url)
        downloader(url, i, path, filename, suffix)
        # time.sleep(random.randint(3, 10))

    if err_url_list:
        with open("./err_url.txt", "w") as f:
            f.write("\n".join(err_url_list))
