#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年3月24日
@author: Irony
@site: https://github.com/892768447
@email: 892768447@qq.com
@file: SimpleImagePs
@description: 图片查看
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMainWindow, QToolBar
from SimpleImageView import SimpleImageView  # @UnresolvedImport


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # 获取可用主屏桌面大小
        screenRect = QApplication.instance().desktop().availableGeometry()
        # 设置为桌面的2/3大
        self.resize(
            int(screenRect.width() * 2 / 3), int(screenRect.height() * 2 / 3))
        # 初始化中心控件
        self._imageView = SimpleImageView(self)
        self.setCentralWidget(self._imageView)
        # 初始化菜单栏
        self._initMenuBar()
        # 初始化工具条
        self._initToolBar()

    def _initMenuBar(self):
        """菜单栏"""
        menuBar = self.menuBar()
        menu = menuBar.addMenu('文件')
        menu.addAction('打开', self._imageView.loadImage)
        menu.addAction('关闭')
        menu.addAction('退出')

    def _initToolBar(self):
        """工具条"""
        toolBar = QToolBar('工具栏', self)
        self.addToolBar(Qt.LeftToolBarArea, toolBar)
        toolBar.addAction('灰度', self._imageView._greyScale)
        toolBar.addAction('亮度')
        toolBar.addAction('暖色调')
        toolBar.addAction('冷色调')
        toolBar.addAction('饱和度')
        toolBar.addAction('模糊')
        toolBar.addAction('锐化', self._ruihua)

    def _ruihua(self):
        # 得到按钮的大概位置
        print(self.mapFromGlobal(QCursor.pos()))


if __name__ == '__main__':
    import sys
    import os
    print('pid:', os.getpid())
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setApplicationDisplayName('简单图片处理')
    app.setApplicationName('简单图片处理')
    app.setApplicationVersion('1.0')
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
