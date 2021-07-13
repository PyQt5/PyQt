#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年5月27日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: FoldWidget
@description: 自定义item折叠控件仿QTreeWidget
"""

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QPushButton, QFormLayout, \
    QLineEdit, QListWidget, QListWidgetItem, QCheckBox


class CustomWidget(QWidget):

    def __init__(self, item, *args, **kwargs):
        super(CustomWidget, self).__init__(*args, **kwargs)
        self.oldSize = None
        self.item = item
        layout = QFormLayout(self)
        layout.addRow('我是label', QLineEdit(self))
        layout.addRow('点击', QCheckBox(
            '隐藏下面的按钮', self, toggled=self.hideChild))
        self.button = QPushButton('我是被隐藏的', self)
        layout.addRow(self.button)

    def hideChild(self, v):
        self.button.setVisible(not v)
        # 这里很重要 当隐藏内部子控件时 需要重新计算高度
        self.adjustSize()

    def resizeEvent(self, event):
        # 解决item的高度问题
        super(CustomWidget, self).resizeEvent(event)
        self.item.setSizeHint(QSize(self.minimumWidth(), self.height()))


class CustomButton(QPushButton):
    # 按钮作为开关

    def __init__(self, item, *args, **kwargs):
        super(CustomButton, self).__init__(*args, **kwargs)
        self.item = item
        self.setCheckable(True)  # 设置可选中

    def resizeEvent(self, event):
        # 解决item的高度问题
        super(CustomButton, self).resizeEvent(event)
        self.item.setSizeHint(QSize(self.minimumWidth(), self.height()))


class Window(QListWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        for _ in range(3):
            # 开关
            item = QListWidgetItem(self)
            btn = CustomButton(item, '折叠', self, objectName='testBtn')
            self.setItemWidget(item, btn)

            # 被折叠控件
            item = QListWidgetItem(self)
            # 通过按钮的选中来隐藏下面的item
            btn.toggled.connect(item.setHidden)
            self.setItemWidget(item, CustomWidget(item, self))


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    # 通过qss改变按钮的高度
    app.setStyleSheet('#testBtn{min-height:40px;}')
    w = Window()
    w.show()
    sys.exit(app.exec_())
