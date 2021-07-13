#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年10月18日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: ImageSlipped
@description: 
"""

try:
    from PyQt5.QtGui import QPixmap, QPainter
    from PyQt5.QtWidgets import QWidget, QApplication
except ImportError:
    from PySide2.QtGui import QPixmap, QPainter
    from PySide2.QtWidgets import QWidget, QApplication


class SlippedImgWidget(QWidget):

    def __init__(self, bg, fg, *args, **kwargs):
        super(SlippedImgWidget, self).__init__(*args, **kwargs)
        # 开启鼠标跟踪
        self.setMouseTracking(True)
        # 背景
        self.bgPixmap = QPixmap(bg)
        # 前景
        self.pePixmap = QPixmap(fg)
        # 最小尺寸(背景右边和下方隐藏10个像素)
        size = self.bgPixmap.size()
        self.setMinimumSize(size.width() - 10, size.height() - 10)
        self.setMaximumSize(size.width() - 10, size.height() - 10)
        # 分成10份用于鼠标移动判断
        self.stepX = size.width() / 10
        self.stepY = size.height() / 10
        # 偏移量
        self._offsets = [-4, -4, -4, -4]  # 背景(-4,-4),前景(-4,-4)

    def mouseMoveEvent(self, event):
        super(SlippedImgWidget, self).mouseMoveEvent(event)
        pos = event.pos()

        # 偏移量
        offsetX = 5 - int(pos.x() / self.stepX)
        offsetY = 5 - int(pos.y() / self.stepY)
        self._offsets[0] = offsetX
        self._offsets[1] = offsetY
        self._offsets[2] = offsetX
        self._offsets[3] = offsetY
        # 刷新
        self.update()

    def paintEvent(self, event):
        super(SlippedImgWidget, self).paintEvent(event)
        # 绘制图形
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 左上角偏移5个像素画背景图片
        painter.drawPixmap(
            -5 + self._offsets[0],
            -5 + self._offsets[1], self.bgPixmap)
        # 右下角偏移5个像素画前景图片
        painter.drawPixmap(
            self.width() - self.pePixmap.width() + 5 - self._offsets[2],
            self.height() - self.pePixmap.height() + 5 - self._offsets[3],
            self.pePixmap
        )


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = SlippedImgWidget('Data/bg1.jpg', 'Data/fg1.png')
    w.show()
    sys.exit(app.exec_())
