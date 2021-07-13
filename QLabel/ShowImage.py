#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年12月23日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: ShowImage
@description: 
"""
import sys

try:
    from PyQt5.QtCore import QResource
    from PyQt5.QtGui import QPixmap, QMovie
    from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QLabel
except ImportError:
    from PySide2.QtCore import QResource
    from PySide2.QtGui import QPixmap, QMovie
    from PySide2.QtWidgets import QWidget, QApplication, QHBoxLayout, QLabel

from Lib.xpmres import image_head  # @UnresolvedImport


class ImageView(QWidget):

    def __init__(self, *args, **kwargs):
        super(ImageView, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        layout = QHBoxLayout(self)

        # 从文件加载图片
        layout.addWidget(QLabel(self, pixmap=QPixmap("Data/head.jpg")))

        # QResource 参考 http://doc.qt.io/qt-5/resources.html

        # 从资源文件中加载1  from py file
        # 转换命令pyrcc5 res.qrc -o res_rc.py
        # 这种方式是从通过pyrcc5转换res.qrc为res_rc.py文件，可以直接import加载
        # 此时可以通过路径:/images/head.jpg来访问
        layout.addWidget(QLabel(self, pixmap=QPixmap(":/images/head.jpg")))

        # 从二进制资源文件res.rcc中加载
        # 转换命令tools/rcc.exe -binary res2.qrc -o res.rcc
        # 这里把资源前缀修改下(/myfile),见res2.qrc文件
        # 此时需要注册
        QResource.registerResource("Data/res.rcc")
        # 注意前缀
        layout.addWidget(
            QLabel(self, pixmap=QPixmap(":/myfile/images/head.jpg")))

        # 从xpm数组中加载
        # 通过工具tools/Image2XPM.exe来转换
        # 这里把转换的xpm数组直接放到py文件中当做一个变量
        # 见xpmres.py中的image_head
        layout.addWidget(QLabel(self, pixmap=QPixmap(image_head)))

        # 加载gif图片
        movie = QMovie("Data/loading.gif")
        label = QLabel(self)
        label.setMovie(movie)
        layout.addWidget(label)
        movie.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ImageView()
    w.show()
    sys.exit(app.exec_())
