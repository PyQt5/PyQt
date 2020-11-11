#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/11/12
@author: Irony
@site: https://github.com/892768447
@email: 892768447@qq.com
@file: ImageView
@description: 图片查看控件，支持移动、放大、缩小
"""

__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2020 Irony'
__Version__ = 1.0

import os

from PyQt5.QtCore import QPoint, QPointF, Qt
from PyQt5.QtGui import QPainter, QColor, QImage, QPixmap
from PyQt5.QtWidgets import QWidget


class ImageView(QWidget):
    """图片查看控件"""

    def __init__(self, image, *args, **kwargs):
        super(ImageView, self).__init__(*args, **kwargs)
        self.setCursor(Qt.OpenHandCursor)
        self._image = None
        self._pos = QPoint(0, 0)  # 移动图片偏移
        self._p_pos = None  # 鼠标按下点
        self._scale = 1  # 缩放
        self._max_scale = 20  # 最大放大级别
        self._background = kwargs.pop('background', None)
        self.setPixmap(image)

    def setMaxScale(self, scale):
        """设置最大放大级别，默认为20
        :param scale: 最大缩放
        :type scale: int
        """
        self._max_scale = scale

    def setBackground(self, color):
        """设置背景颜色
        :param color: 背景颜色
        :type color: QColor or str
        """
        if isinstance(color, QColor):
            self._background = color
        elif isinstance(color, str):
            color = QColor(color)
            if color.isValid():
                self._background = color
        else:
            return
        self.update()

    def setPixmap(self, image):
        """加载图片
        :param image: 图片或者图片路径
        :type image: QPixmap or QImage or str
        """
        if isinstance(image, QPixmap):
            self._image = image
        elif isinstance(image, QImage):
            self._image = QPixmap.fromImage(image)
        elif isinstance(image, str) and os.path.isfile(image):
            self._image = QPixmap(image)
        else:
            return
        self._pos = QPoint(0, 0)
        self._p_pos = None
        self.update()

    def mousePressEvent(self, event):
        """鼠标按下修改鼠标样式以及记录初始移动点"""
        super(ImageView, self).mousePressEvent(event)
        self.setCursor(Qt.ClosedHandCursor)
        if event.button() == Qt.LeftButton:
            self._p_pos = event.pos()

    def mouseReleaseEvent(self, event):
        """鼠标释放修改鼠标样式"""
        super(ImageView, self).mouseReleaseEvent(event)
        self.setCursor(Qt.OpenHandCursor)
        self._p_pos = None

    def mouseMoveEvent(self, event):
        """鼠标移动图片"""
        super(ImageView, self).mouseMoveEvent(event)
        if event.buttons() == Qt.LeftButton and self._p_pos:
            offset = event.pos() - self._p_pos
            self._p_pos += offset
            self._pos += offset
            self.update()

    def wheelEvent(self, event):
        super(ImageView, self).wheelEvent(event)
        step = 0.4 if self._scale > 1.1 else 0.1
        if event.angleDelta().y() > 0:
            # 放大
            self._scale += step
            self._scale = min(self._scale, self._max_scale)
        else:
            # 缩小
            self._scale -= step
            self._scale = max(self._scale, 0.1)
        self.update()

    def paintEvent(self, event):
        super(ImageView, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        if self._background:
            painter.fillRect(self.rect(), self._background)
        if not self._image or self._image.isNull():
            return
        # 变换坐标中心为窗口中点
        painter.translate(self.width() / 2, self.height() / 2)
        # 缩放
        painter.scale(self._scale, self._scale)
        painter.drawPixmap(QPointF(-self._image.width() / 2 + self._pos.x(), -self._image.height() / 2 + self._pos.y()),
                           self._image)


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = ImageView('ScreenShot/CallVirtualKeyboard2.png')
    w.show()
    sys.exit(app.exec_())
