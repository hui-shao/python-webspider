import requests
import platform
import os
import sys
import json

har_filepath = "./welearn.sflep.com.har"
download_path = "./har_downloads"
suffix = "mp3"
merge = True


def check_dir() -> None:
    os.chdir(sys.path[0])
    if not os.path.exists(download_path):
        os.mkdir(download_path)


def read_har_file() -> dict:
    with open(har_filepath, "r", encoding="utf-8") as file:
        har_text_raw = file.read()
    if har_text_raw:
        har_text_dict = json.loads(har_text_raw)
        return har_text_dict
    else:
        return {}


def generate_url_list(_har_text_dict: dict) -> list:
    entries_list = _har_text_dict.get("log").get("entries")
    ori_target_url_list = []
    for i in range(0, len(entries_list)):
        per_dict = entries_list[i]
        per_url = str(per_dict.get("request").get("url"))
        if per_url.endswith(".{}".format(suffix)):
            ori_target_url_list.append(per_url)
    final_target_url_list = list(set(ori_target_url_list))  # 利用集合进行元素去重
    final_target_url_list.sort(key=ori_target_url_list.index)  # 按照原列表顺序排序
    return final_target_url_list


def downloader(_url: str, _index: int, _path: str, _suffix: str) -> None:
    hea = {
        "user-agent": "Mozilla/5.0 (Linux; Android 9; MI 6 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.85 Mobile Safari/537.36"
    }
    res = requests.get(url=_url, headers=hea)
    if res.status_code in (200, 206):
        with open("{}/{}.{}".format(_path, str(_index).zfill(5), _suffix), "wb") as file:
            file.write(res.content)
        print("[+] Success on {}".format(_index))
    else:
        err_url_list.append(_url)
        print("\n[!] Error on {}\n".format(_index))


def write_err_list() -> None:
    if not err_url_list:  # 如果 err_url_list 为空 直接返回 不进行读写
        return None
    with open("{}/error_list.txt".format(download_path), "w", encoding="utf-8") as file:
        for err_url in err_url_list:
            file.writelines(err_url)


def merge_file() -> None:
    os.chdir(sys.path[0] + "/{}".format(download_path))
    os_type = platform.system()
    if os_type == "Windows":
        os.system("copy /b *.{} merged.{}".format(suffix, suffix))
    elif os_type == "Linux":
        os.system("cat *.{} > merged.{}".format(suffix, suffix))
    else:
        pass


def run():
    check_dir()
    har_text_dict = read_har_file()
    url_list = generate_url_list(har_text_dict)
    for i in range(0, len(url_list)):
        downloader(url_list[i], i, download_path, suffix)
    write_err_list()
    if merge:
        merge_file()


if __name__ == '__main__':
    err_url_list = []  # 用于记录出错的链接
    run()
