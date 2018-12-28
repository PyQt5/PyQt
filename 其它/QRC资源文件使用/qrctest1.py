#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年05月01日
@author: Irony."[讽刺]
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: qrctest1
@description: 
'''

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

import res_rc  # @UnusedImport @UnresolvedImport


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class ImageView(QLabel):

    def __init__(self, *args, **kwargs):
        super(ImageView, self).__init__(*args, **kwargs)
        self.resize(800, 600)

        # 从资源文件res_rc.py中加载
        # 转换命令pyrcc5 res.qrc -o res_rc.py
        # 这种方式是从通过pyrcc5转换res.qrc为res_rc.py文件，可以直接import加载
        # 此时可以通过路径:/images/head.jpg来访问
        self.setPixmap(QPixmap(":/images/head.jpg"))


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(res_rc.qCleanupResources)  # 退出时要清理资源
    w = ImageView()
    w.show()
    sys.exit(app.exec_())
