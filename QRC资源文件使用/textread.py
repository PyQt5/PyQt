#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QFile, QIODevice, QTextStream, QTextCodec
from PyQt5.QtWidgets import QTextBrowser

import res_rc  # @UnresolvedImport @UnusedImport


# Created on 2018年5月1日
# author: Irony
# site: https://pyqt5.com, https://github.com/892768447
# email: 892768447@qq.com
# file: QRC资源文件使用.textread
# description:
__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class TextBrowser(QTextBrowser):

    def __init__(self, *args, **kwargs):
        super(TextBrowser, self).__init__(*args, **kwargs)
        self.setText(self.readText(':/README.md'))

    def readText(self, path):
        file = QFile(path)
        if not file.open(QIODevice.ReadOnly):
            return ''
        stream = QTextStream(file)
        # 下面这句设置编码根据文件的编码自行确定
        stream.setCodec(QTextCodec.codecForName('UTF-8'))
        data = stream.readAll()
        file.close()
        del stream
        return data


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(res_rc.qCleanupResources)  # 退出时要清理资源
    w = TextBrowser()
    w.show()
    sys.exit(app.exec_())
