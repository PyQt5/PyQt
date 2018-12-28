#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年05月01日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: qrctest2
@description: 
'''


from PyQt5.QtCore import QResource
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class ImageView(QLabel):

    def __init__(self, *args, **kwargs):
        super(ImageView, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        self.setPixmap(QPixmap(":/images/head.jpg"))


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    # 从二进制资源文件res.data中加载
    # 转换命令cd tools
    # rcc.exe -binary ../res.qrc -o ../res.data
    # 此时需要注册
    QResource.registerResource("res.data")
    app.aboutToQuit.connect(lambda: QResource.unregisterResource("res.data"))
    w = ImageView()
    w.show()
    sys.exit(app.exec_())
