#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年5月29日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: LeftTabWidget
@description:
"""

from random import randint

try:
    from PyQt5.QtCore import Qt, QSize
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QStackedWidget, QHBoxLayout, \
        QListWidgetItem, QLabel
except ImportError:
    from PySide2.QtCore import Qt, QSize
    from PySide2.QtGui import QIcon
    from PySide2.QtWidgets import QApplication, QWidget, QListWidget, QStackedWidget, QHBoxLayout, \
        QListWidgetItem, QLabel


class LeftTabWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(LeftTabWidget, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        # 左右布局(左边一个QListWidget + 右边QStackedWidget)
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        # 左侧列表
        self.listWidget = QListWidget(self)
        layout.addWidget(self.listWidget)
        # 右侧层叠窗口
        self.stackedWidget = QStackedWidget(self)
        layout.addWidget(self.stackedWidget)
        self.initUi()

    def initUi(self):
        # 初始化界面
        # 通过QListWidget的当前item变化来切换QStackedWidget中的序号
        self.listWidget.currentRowChanged.connect(
            self.stackedWidget.setCurrentIndex)
        # 去掉边框
        self.listWidget.setFrameShape(QListWidget.NoFrame)
        # 隐藏滚动条
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 这里就用一般的文本配合图标模式了(也可以直接用Icon模式,setViewMode)
        for i in range(20):
            item = QListWidgetItem(
                QIcon('Data/0%d.ico' % randint(1, 8)), str('选 项 %s' % i), self.listWidget)
            # 设置item的默认宽高(这里只有高度比较有用)
            item.setSizeHint(QSize(16777215, 60))
            # 文字居中
            item.setTextAlignment(Qt.AlignCenter)

        # 再模拟20个右侧的页面(就不和上面一起循环放了)
        for i in range(20):
            label = QLabel('我是页面 %d' % i, self)
            label.setAlignment(Qt.AlignCenter)
            # 设置label的背景颜色(这里随机)
            # 这里加了一个margin边距(方便区分QStackedWidget和QLabel的颜色)
            label.setStyleSheet('background: rgb(%d, %d, %d);margin: 50px;' % (
                randint(0, 255), randint(0, 255), randint(0, 255)))
            self.stackedWidget.addWidget(label)


# 美化样式表
Stylesheet = """
/*去掉item虚线边框*/
QListWidget, QListView, QTreeWidget, QTreeView {
    outline: 0px;
}
/*设置左侧选项的最小最大宽度,文字颜色和背景颜色*/
QListWidget {
    min-width: 120px;
    max-width: 120px;
    color: white;
    background: black;
}
/*被选中时的背景颜色和左边框颜色*/
QListWidget::item:selected {
    background: rgb(52, 52, 52);
    border-left: 2px solid rgb(9, 187, 7);
}
/*鼠标悬停颜色*/
HistoryPanel::item:hover {
    background: rgb(52, 52, 52);
}

/*右侧的层叠窗口的背景颜色*/
QStackedWidget {
    background: rgb(30, 30, 30);
}
/*模拟的页面*/
QLabel {
    color: white;
}
"""

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyleSheet(Stylesheet)
    w = LeftTabWidget()
    w.show()
    sys.exit(app.exec_())
