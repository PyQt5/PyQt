#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年4月19日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: FramelessDialog
@description: 无边框圆角对话框 
"""

try:
    from PyQt5.QtCore import Qt, QSize, QTimer
    from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, \
        QGraphicsDropShadowEffect, QPushButton, QGridLayout, QSpacerItem, \
        QSizePolicy, QApplication
except ImportError:
    from PySide2.QtCore import Qt, QSize, QTimer
    from PySide2.QtWidgets import QDialog, QVBoxLayout, QWidget, \
        QGraphicsDropShadowEffect, QPushButton, QGridLayout, QSpacerItem, \
        QSizePolicy, QApplication

Stylesheet = """
#Custom_Widget {
    background: white;
    border-radius: 10px;
}

#closeButton {
    min-width: 36px;
    min-height: 36px;
    font-family: "Webdings";
    qproperty-text: "r";
    border-radius: 10px;
}
#closeButton:hover {
    color: white;
    background: red;
}
"""


class Dialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.setObjectName('Custom_Dialog')
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet(Stylesheet)
        self.initUi()
        # 添加阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)

    def initUi(self):
        layout = QVBoxLayout(self)
        # 重点： 这个widget作为背景和圆角
        self.widget = QWidget(self)
        self.widget.setObjectName('Custom_Widget')
        layout.addWidget(self.widget)

        # 在widget中添加ui
        layout = QGridLayout(self.widget)
        layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 0)
        layout.addWidget(QPushButton(
            'r', self, clicked=self.accept, objectName='closeButton'), 0, 1)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum,
                                   QSizePolicy.Expanding), 1, 0)

    def sizeHint(self):
        return QSize(600, 400)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Dialog()
    w.exec_()
    QTimer.singleShot(200, app.quit)
    sys.exit(app.exec_())
