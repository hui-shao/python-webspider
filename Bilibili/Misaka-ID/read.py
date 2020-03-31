import re
import ast
import traceback
import sys


def run():
    # 从文件中读取
    try:
        f = open("./lists.txt", "r", encoding="utf-8")
        lines = f.readlines()
        f.close()
    except FileNotFoundError:
        print("list.txt 不存在！")
        sys.exit()
    except Exception:
        print("ERROR!\n", traceback.format_exc())
        sys.exit()
    # 字符操作
    avai = lines[0].strip("\n")
    unavai = lines[1].strip("\n")
    avai = re.sub(r"^.{9}: ", "", avai)
    unavai = re.sub(r"^.{11}: ", "", unavai)
    # 把列表形式的字符串转为列表
    try:
        available = ast.literal_eval(avai)
        unavailable = ast.literal_eval(unavai)
    except Exception:
        print("ERROR!\n", traceback.format_exc())
        sys.exit()
    else:
        # 计数
        print("已注册数：", len(unavailable))
        print("未注册数：", len(available))
    return unavailable, available


if __name__ == "__main__":
    run()
