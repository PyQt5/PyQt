#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年3月1日
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: EmbedWindow
@description: 嵌入外部窗口
"""

__Author__ = 'By: Irony\nQQ: 892768447\nEmail: 892768447@qq.com'
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0

from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget,\
    QLabel
import win32con
import win32gui


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        layout = QVBoxLayout(self)

        self.myhwnd = int(self.winId())  # 自己的句柄

        layout.addWidget(QPushButton('获取所有可用、可视窗口', self,
                                     clicked=self._getWindowList, maximumHeight=30))
        layout.addWidget(
            QLabel('双击列表中的项目则进行嵌入目标窗口到下方\n格式为：句柄|父句柄|标题|类名', self, maximumHeight=30))
        self.windowList = QListWidget(
            self, itemDoubleClicked=self.onItemDoubleClicked, maximumHeight=200)
        layout.addWidget(self.windowList)

    def closeEvent(self, event):
        """窗口关闭"""
        if self.layout().count() == 4:
            self.restore()
        super(Window, self).closeEvent(event)

    def _getWindowList(self):
        """清空原来的列表"""
        self.windowList.clear()
        win32gui.EnumWindows(self._enumWindows, None)

    def onItemDoubleClicked(self, item):
        """列表双击选择事件"""
        # 先移除掉item
        self.windowList.takeItem(self.windowList.indexFromItem(item).row())
        hwnd, phwnd, _, _ = item.text().split('|')
        # 开始嵌入

        if self.layout().count() == 4:
            # 如果数量等于4说明之前已经嵌入了一个窗口，现在需要把它释放出来
            self.restore()
        hwnd, phwnd = int(hwnd), int(phwnd)
        # 嵌入之前的属性
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        print('save', hwnd, style, exstyle)

        widget = QWidget.createWindowContainer(QWindow.fromWinId(hwnd))
        widget.hwnd = hwnd  # 窗口句柄
        widget.phwnd = phwnd  # 父窗口句柄
        widget.style = style  # 窗口样式
        widget.exstyle = exstyle  # 窗口额外样式
        self.layout().addWidget(widget)

    def restore(self):
        """归还窗口"""
        # 有bug，归还后窗口没有了WS_VISIBLE样式，不可见
        widget = self.layout().itemAt(3).widget()
        print('restore', widget.hwnd, widget.style, widget.exstyle)
        win32gui.SetParent(widget.hwnd, widget.phwnd)  # 让它返回它的父窗口
        win32gui.SetWindowLong(
            widget.hwnd, win32con.GWL_STYLE, widget.style | win32con.WS_VISIBLE)  # 恢复样式
        win32gui.SetWindowLong(
            widget.hwnd, win32con.GWL_EXSTYLE, widget.exstyle)  # 恢复样式
        win32gui.ShowWindow(
            widget.hwnd, win32con.SW_SHOW)  # 显示窗口
        widget.close()
        self.layout().removeWidget(widget)  # 从布局中移出
        widget.deleteLater()

    def _enumWindows(self, hwnd, _):
        """遍历回调函数"""
        if hwnd == self.myhwnd:
            return  # 防止自己嵌入自己
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            phwnd = win32gui.GetParent(hwnd)
            title = win32gui.GetWindowText(hwnd)
            name = win32gui.GetClassName(hwnd)
            self.windowList.addItem(
                '{0}|{1}|\t标题：{2}\t|\t类名：{3}'.format(hwnd, phwnd, title, name))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
