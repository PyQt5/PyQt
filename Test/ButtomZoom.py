#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年10月30日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: ButtomZoom
@description: 
"""
try:
    from PyQt5.QtCore import QPropertyAnimation, QRect
    from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy
except ImportError:
    from PySide2.QtCore import QPropertyAnimation, QRect
    from PySide2.QtWidgets import QApplication, QPushButton, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy


class ZoomButton(QPushButton):

    def __init__(self, *args, **kwargs):
        super(ZoomButton, self).__init__(*args, **kwargs)
        self._animation = QPropertyAnimation(
            self, b'geometry', self, duration=200)

    def updatePos(self):
        # 记录自己的固定的geometry值
        self._geometry = self.geometry()
        self._rect = QRect(
            self._geometry.x() - 6,
            self._geometry.y() - 2,
            self._geometry.width() + 12,
            self._geometry.height() + 4
        )

    def showEvent(self, event):
        super(ZoomButton, self).showEvent(event)
        self.updatePos()

    def enterEvent(self, event):
        super(ZoomButton, self).enterEvent(event)
        self._animation.stop()  # 停止动画
        # 修改动画的开始值
        self._animation.setStartValue(self._geometry)
        # 修改动画的终止值
        self._animation.setEndValue(self._rect)
        self._animation.start()

    def leaveEvent(self, event):
        super(ZoomButton, self).leaveEvent(event)
        self._animation.stop()  # 停止动画
        # 修改动画的开始值
        self._animation.setStartValue(self._rect)
        # 修改动画的终止值
        self._animation.setEndValue(self._geometry)
        self._animation.start()

    def mousePressEvent(self, event):
        self._animation.stop()  # 停止动画
        # 修改动画的开始值
        self._animation.setStartValue(self._rect)
        # 修改动画的终止值
        self._animation.setEndValue(self._geometry)
        self._animation.start()
        super(ZoomButton, self).mousePressEvent(event)


class Window(QWidget):
    # 测试窗口

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        # 1. 加入布局中
        layout = QHBoxLayout(self)
        layout.addSpacerItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.button1 = ZoomButton('按钮1', self)
        layout.addWidget(self.button1)
        layout.addSpacerItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        # 2. 不在布局中
        self.button2 = ZoomButton('按钮2', self)

    # 以下两个方法需要重写

    def showEvent(self, event):
        super(Window, self).showEvent(event)
        # 更新按钮的位置
        self.button1.updatePos()
        # 针对不在控件中的按钮
        self.button2.move(self.width() - self.button2.width() - 15,
                          self.height() - self.button2.height() - 10)
        self.button2.updatePos()

    def resizeEvent(self, event):
        super(Window, self).resizeEvent(event)
        # 更新按钮的位置
        self.button1.updatePos()
        # 针对不在控件中的按钮
        self.button2.move(self.width() - self.button2.width() - 15,
                          self.height() - self.button2.height() - 10)
        self.button2.updatePos()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyleSheet("""QPushButton {
    border: none;
    font-weight: bold;
    font-size: 16px;
    border-radius: 18px;
    min-width: 180px;
    min-height: 40px;
    background-color: white;
    }""")
    w = Window()
    w.show()
    sys.exit(app.exec_())
