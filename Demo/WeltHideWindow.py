#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年3月1日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: WeltHideWindow
@description: 简单的窗口贴边隐藏
"""

import os
import platform
from subprocess import getoutput

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (
        QApplication,
        QGridLayout,
        QMessageBox,
        QPushButton,
        QSizePolicy,
        QSpacerItem,
        QWidget,
    )
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import (
        QApplication,
        QGridLayout,
        QMessageBox,
        QPushButton,
        QSizePolicy,
        QSpacerItem,
        QWidget,
    )


def IsSupport():
    """判断是否支持"""
    if platform.system() == "Linux":
        name = os.environ.get("XDG_SESSION_DESKTOP", "") + os.environ.get(
            "XDG_CURRENT_DESKTOP", ""
        )
        if name.lower().find("gnome") != -1:
            print("gnome desktop")
            return False

        wid = getoutput("xprop -root _NET_SUPPORTING_WM_CHECK").split(" # ")[-1]
        print("wid:", wid)
        if wid:
            name = getoutput("xprop -id %s _NET_WM_NAME" % wid)
            print("name:", name)
            if name.lower().find("gnome") != -1:
                print("gnome desktop")
                return False

    return True


class WeltHideWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(WeltHideWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.resize(400, 300)
        self._width = QApplication.desktop().availableGeometry(self).width()
        layout = QGridLayout(self)
        layout.addItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 0
        )
        self.closeBtn = QPushButton("X", self)
        layout.addWidget(self.closeBtn, 0, 1)
        layout.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 1, 0
        )
        self.closeBtn.clicked.connect(self.close)
        self.closeBtn.setMinimumSize(24, 24)
        self.closeBtn.setMaximumSize(24, 24)

    def mousePressEvent(self, event):
        """鼠标按下事件，需要记录下坐标self._pos 和 是否可移动self._canMove"""
        super(WeltHideWindow, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._pos = event.globalPos() - self.pos()
            # 当窗口最大化或者全屏时不可移动
            self._canMove = not self.isMaximized() or not self.isFullScreen()

    def mouseMoveEvent(self, event):
        """鼠标移动事件，动态调整窗口位置"""
        super(WeltHideWindow, self).mouseMoveEvent(event)
        if event.buttons() == Qt.LeftButton and self._canMove:
            self.move(event.globalPos() - self._pos)

    def mouseReleaseEvent(self, event):
        """鼠标弹起事件，这个时候需要判断窗口的左边是否符合贴到左边，顶部，右边一半"""
        super(WeltHideWindow, self).mouseReleaseEvent(event)
        self._canMove = False
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        if x < 0:
            # 隐藏到左边
            return self.move(1 - self.width(), y)
        if y < 0:
            # 隐藏到顶部
            return self.move(x, 1 - self.height())
        if x > self._width - self.width() / 2:  # 窗口进入右边一半距离
            # 隐藏到右边
            return self.move(self._width - 1, y)

    def enterEvent(self, event):
        """鼠标进入窗口事件，用于弹出显示窗口"""
        super(WeltHideWindow, self).enterEvent(event)
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        if x < 0:
            return self.move(0, y)
        if y < 0:
            return self.move(x, 0)
        if x > self._width - self.width() / 2:
            return self.move(self._width - self.width(), y)

    def leaveEvent(self, event):
        """鼠标离开事件，如果原先窗口已经隐藏，并暂时显示，此时离开后需要再次隐藏"""
        super(WeltHideWindow, self).leaveEvent(event)
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        if x == 0:
            return self.move(1 - self.width(), y)
        if y == 0:
            return self.move(x, 1 - self.height())
        if x == self._width - self.width():
            return self.move(self._width - 1, y)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    if not IsSupport():
        QMessageBox.warning(
            None,
            "Warning",
            "当前桌面不支持此功能",
        )
        app.quit()
    else:
        w = WeltHideWindow()
        w.show()
        sys.exit(app.exec_())
