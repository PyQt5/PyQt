#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget

from Lib.SettingUi import Ui_Setting  # @UnresolvedImport


# Created on 2018年3月28日
# author: Irony
# site: https://pyqt5.com , https://github.com/892768447
# email: 892768447@qq.com
# file: QQSettingPanel
# description:

__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


class Window(QWidget, Ui_Setting):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.resize(700, 435)
        self._blockSignals = False

        # 绑定滚动条和左侧item事件
        self.scrollArea.verticalScrollBar().valueChanged.connect(
            self.onValueChanged)
        self.listWidget.itemClicked.connect(self.onItemClicked)

    def onValueChanged(self, value):
        """滚动条"""
        if self._blockSignals:
            # 防止item点击时改变滚动条会触发这里
            return
        for i in range(8):  # 因为这里右侧有8个widget
            widget = getattr(self, 'widget_%d' % i, None)
            # widget不为空且在可视范围内
            if widget and not widget.visibleRegion().isEmpty():
                self.listWidget.setCurrentRow(i)  # 设置item的选中
                return

    def onItemClicked(self, item):
        """左侧item"""
        row = self.listWidget.row(item)  # 获取点击的item的索引
        # 由于右侧的widget是按照命名widget_0 widget_1这样比较规范的方法,可以通过getattr找到
        widget = getattr(self, 'widget_%d' % row, None)
        if not widget:
            return
        # 定位右侧位置并滚动
        self._blockSignals = True
        self.scrollArea.verticalScrollBar().setSliderPosition(widget.pos().y())
        self._blockSignals = False


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(open("Data/style.qss", "rb").read().decode("utf-8"))
    w = Window()
    w.show()
    sys.exit(app.exec_())
