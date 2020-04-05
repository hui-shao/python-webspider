# -*- coding: UTF-8 -*-
import os
import platform


class ConsoleTool(object):
    def __init__(self):
        pass

    @staticmethod
    def check_platform():
        check_result = platform.system()
        if "indows" in check_result:
            return "W"
        elif "inux" in check_result:
            return "L"

    def console_clear(self):
        sysinfo = self.check_platform()
        if sysinfo == "W":
            os.system("cls")
            return
        elif sysinfo == "L":
            os.system("clear")
            return
        os.system("cls")
