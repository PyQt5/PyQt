#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年5月7日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: 自动更新.test
@description: 
"""
import sys

sys.path.append("mylibs")
import os
from time import sleep
from zipfile import ZipFile


def update():
    # 更新
    from mylibs import testlibs  # @UnresolvedImport
    v1 = testlibs.version()  # 获取本地模块版本
    v2 = "0.0.2"  # 模拟新版本（也可以从网络中检测）
    if v1 != v2:  # 需要更新
        print("发现新版本：0.0.2")
        # 模拟从网络中下载更新包并解压（也可以包含图片等其它文件）
        with ZipFile("mylibs2.zip", "r") as zf:
            zf.extractall(os.path.dirname(sys.executable))  # 解压到当前目录
        return 1
    return 0


def main():
    from mylibs import testlibs  # @UnresolvedImport
    testlibs.test()
    print("当前版本：", testlibs.version())
    if update():
        print("更新完毕，即将重启")
        import platform
        if platform.system() == "Windows":
            import ctypes
            ctypes.windll.user32.MessageBoxW(
                0, "更新完毕，关闭对话框即将重启", "提示", 0x0000030)
        sleep(0.5)
        os.startfile(sys.executable)  # 重启
        sys.exit()  # 退出本身


if __name__ == "__main__":
    main()
    input("press any key exit")
