#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年3月30日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: WindowNotify
@description: 右下角弹窗
"""
import webbrowser

try:
    from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QTimer, pyqtSignal
    from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout
except ImportError:
    from PySide2.QtCore import Qt, QPropertyAnimation, QPoint, QTimer, Signal as pyqtSignal
    from PySide2.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout

from Lib.UiNotify import Ui_NotifyForm  # @UnresolvedImport


class WindowNotify(QWidget, Ui_NotifyForm):
    SignalClosed = pyqtSignal()  # 弹窗关闭信号

    def __init__(self, title="", content="", timeout=5000, *args, **kwargs):
        super(WindowNotify, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setTitle(title).setContent(content)
        self._timeout = timeout
        self._init()

    def setTitle(self, title):
        if title:
            self.labelTitle.setText(title)
        return self

    def title(self):
        return self.labelTitle.text()

    def setContent(self, content):
        if content:
            self.labelContent.setText(content)
        return self

    def content(self):
        return self.labelContent.text()

    def setTimeout(self, timeout):
        if isinstance(timeout, int):
            self._timeout = timeout
        return self

    def timeout(self):
        return self._timeout

    def onView(self):
        print("onView")
        webbrowser.open_new_tab("http://alyl.vip")

    def onClose(self):
        # 点击关闭按钮时
        print("onClose")
        self.isShow = False
        QTimer.singleShot(100, self.closeAnimation)  # 启动弹回动画

    def _init(self):
        # 隐藏任务栏|去掉边框|顶层显示
        self.setWindowFlags(Qt.Tool | Qt.X11BypassWindowManagerHint |
                            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 关闭按钮事件
        self.buttonClose.clicked.connect(self.onClose)
        # 点击查看按钮
        self.buttonView.clicked.connect(self.onView)
        # 是否在显示标志
        self.isShow = True
        # 超时
        self._timeouted = False
        # 桌面
        self._desktop = QApplication.instance().desktop()
        # 窗口初始开始位置
        self._startPos = QPoint(
            self._desktop.screenGeometry().width() - self.width() - 5,
            self._desktop.screenGeometry().height()
        )
        # 窗口弹出结束位置
        self._endPos = QPoint(
            self._desktop.screenGeometry().width() - self.width() - 5,
            self._desktop.availableGeometry().height() - self.height() - 5
        )
        # 初始化位置到右下角
        self.move(self._startPos)

        # 动画
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.finished.connect(self.onAnimationEnd)
        self.animation.setDuration(1000)  # 1s

        # 弹回定时器
        self._timer = QTimer(self, timeout=self.closeAnimation)

    def show(self, title="", content="", timeout=5000):
        self._timer.stop()  # 停止定时器,防止第二个弹出窗弹出时之前的定时器出问题
        self.hide()  # 先隐藏
        self.move(self._startPos)  # 初始化位置到右下角
        super(WindowNotify, self).show()
        self.setTitle(title).setContent(content).setTimeout(timeout)
        return self

    def showAnimation(self):
        print("showAnimation isShow = True")
        # 显示动画
        self.isShow = True
        self.animation.stop()  # 先停止之前的动画,重新开始
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(self._endPos)
        self.animation.start()
        # 弹出5秒后,如果没有焦点则弹回去
        self._timer.start(self._timeout)

    #         QTimer.singleShot(self._timeout, self.closeAnimation)

    def closeAnimation(self):
        print("closeAnimation hasFocus", self.hasFocus())
        # 关闭动画
        if self.hasFocus():
            # 如果弹出后倒计时5秒后还有焦点存在则失去焦点后需要主动触发关闭
            self._timeouted = True
            return  # 如果有焦点则不关闭
        self.isShow = False
        self.animation.stop()
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(self._startPos)
        self.animation.start()

    def onAnimationEnd(self):
        # 动画结束
        print("onAnimationEnd isShow", self.isShow)
        if not self.isShow:
            print("onAnimationEnd close()")
            self.close()
            print("onAnimationEnd stop timer")
            self._timer.stop()
            print("onAnimationEnd close and emit signal")
            self.SignalClosed.emit()

    def enterEvent(self, event):
        super(WindowNotify, self).enterEvent(event)
        # 设置焦点(好像没啥用,不过鼠标点击一下后,该方法就有用了)
        print("enterEvent setFocus Qt.MouseFocusReason")
        self.setFocus(Qt.MouseFocusReason)

    def leaveEvent(self, event):
        super(WindowNotify, self).leaveEvent(event)
        # 取消焦点
        print("leaveEvent clearFocus")
        self.clearFocus()
        if self._timeouted:
            QTimer.singleShot(1000, self.closeAnimation)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    window = QWidget()
    notify = WindowNotify(parent=window)

    layout = QHBoxLayout(window)

    b1 = QPushButton(
        "弹窗1", window, clicked=lambda: notify.show(content=b1.text()).showAnimation())
    b2 = QPushButton(
        "弹窗2", window, clicked=lambda: notify.show(content=b2.text()).showAnimation())

    layout.addWidget(b1)
    layout.addWidget(b2)

    window.show()

    sys.exit(app.exec_())
