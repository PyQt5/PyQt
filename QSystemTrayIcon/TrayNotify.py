#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2021年12月09日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: TrayNotify
@description: 托盘闪烁
"""

try:
    from PyQt5.QtCore import QTimer
    from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QPushButton,
                                 QStyle, QSystemTrayIcon, QWidget)
except ImportError:
    from PySide2.QtCore import QTimer
    from PySide2.QtWidgets import (QApplication, QHBoxLayout, QPushButton,
                                   QStyle, QSystemTrayIcon, QWidget)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.addWidget(QPushButton('开始闪烁', self, clicked=self.start_flash))
        layout.addWidget(QPushButton('停止闪烁', self, clicked=self.stop_flash))
        # 创建托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(
            QStyle.SP_ComputerIcon))
        self.tray_icon.show()
        # 图标闪烁定时器
        self.tray_visible = True
        self.flash_timer = QTimer(self, timeout=self.flash_icon)

    def closeEvent(self, event):
        self.stop_flash()
        self.tray_icon.hide()
        super(Window, self).closeEvent(event)

    def start_flash(self):
        """开始闪烁"""
        if not self.flash_timer.isActive():
            self.flash_timer.start(500)

    def stop_flash(self):
        """停止闪烁后需要显示图标"""
        if self.flash_timer.isActive():
            self.flash_timer.stop()
            self.tray_icon.setIcon(self.style().standardIcon(
                QStyle.SP_ComputerIcon))

    def flash_icon(self):
        """根据当前图标是否可见切换图标"""
        if self.tray_visible:
            self.tray_icon.setIcon(self.style().standardIcon(
                QStyle.SP_TrashIcon))
        else:
            self.tray_icon.setIcon(self.style().standardIcon(
                QStyle.SP_ComputerIcon))
        self.tray_visible = not self.tray_visible


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
