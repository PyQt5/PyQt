#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Created on 2018年4月30日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: Test
@description:
"""

try:
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QApplication
except ImportError:
    from PySide2.QtGui import QIcon
    from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QApplication

from Lib.FramelessWindow import FramelessWindow  # @UnresolvedImport


class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QPushButton('按钮', self))
        layout.addWidget(QTextEdit(self))


# 样式
StyleSheet = """
/*标题栏*/
TitleBar {
    background-color: rgb(54, 157, 180);
}

/*最小化最大化关闭按钮通用默认背景*/
#buttonMinimum,#buttonMaximum,#buttonClose {
    border: none;
    background-color: rgb(54, 157, 180);
}

/*悬停*/
#buttonMinimum:hover,#buttonMaximum:hover {
    background-color: rgb(48, 141, 162);
}
#buttonClose:hover {
    color: white;
    background-color: rgb(232, 17, 35);
}

/*鼠标按下不放*/
#buttonMinimum:pressed,#buttonMaximum:pressed {
    background-color: rgb(44, 125, 144);
}
#buttonClose:pressed {
    color: white;
    background-color: rgb(161, 73, 92);
}
"""

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    w = FramelessWindow()
    w.setWindowTitle('测试标题栏')
    w.setWindowIcon(QIcon('Data/Qt.ico'))
    w.setWidget(MainWindow(w))  # 把自己的窗口添加进来
    w.show()
    sys.exit(app.exec_())
