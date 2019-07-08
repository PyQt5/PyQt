#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月8日
@author: Irony
@site: https://pyqt5.com https://github.com/PyQt5
@email: 892768447@qq.com
@file: ScreenShotPage
@description: 网页整体截图
"""
import cgitb
import os
import sys

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton,\
    QMessageBox


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019"
__Version__ = "Version 1.0"


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(600, 400)
        layout = QVBoxLayout(self)
        self.webView = QWebView()
        layout.addWidget(self.webView)
        layout.addWidget(QPushButton('截图', self, clicked=self.onScreenShot))
        self.webView.load(QUrl("https://pyqt5.com"))

    def onScreenShot(self):
        page = self.webView.page()
        frame = page.mainFrame()
        size = frame.contentsSize()
        image = QImage(size, QImage.Format_ARGB32_Premultiplied)
        image.fill(Qt.transparent)

        painter = QPainter()
        painter.begin(image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        # 记录旧大小
        oldSize = page.viewportSize()
        # *****重点就是这里******
        page.setViewportSize(size)
        frame.render(painter)
        painter.end()
        image.save('Data/ScreenShotPage.png', 'png')

        # 截图完成后需要还原,否则界面不响应鼠标等
        page.setViewportSize(oldSize)

        os.startfile(os.path.abspath('Data/ScreenShotPage.png'))
        QMessageBox.information(self, '提示', '截图完成')


if __name__ == "__main__":
    sys.excepthook = cgitb.enable(1, None, 5, '')
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
