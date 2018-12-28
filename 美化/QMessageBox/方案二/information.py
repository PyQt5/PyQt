#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年1月17日
@author: Irony."[讽刺]
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: information
@description: 
'''

__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"

import sys

from PyQt5.QtWidgets import QApplication, QMessageBox


app = QApplication(sys.argv)
app.setStyleSheet('''
QPushButton[text="Close"] {
    background: red;
    qproperty-icon: url(../icons/Close.png);
}
QPushButton[text="Close"]:hover {
    background: darkRed;
}

QPushButton[text="Discard"] {
    background: green;
    qproperty-icon: url(../icons/Discard.png);
}
QPushButton[text="Discard"]:hover {
    background: darkGreen;
}

QPushButton[text="Apply"] {
    background: blue;
    qproperty-icon: url(../icons/Apply.png);
}
QPushButton[text="Apply"]:hover {
    background: darkBlue;
}

QPushButton[text="Reset"] {
    background: cyan;
    qproperty-icon: url(../icons/Reset.png);
}
QPushButton[text="Reset"]:hover {
    background: darkCyan;
}

QMessageBox {
    messagebox-information-icon: url(../icons/Close.png);
}

QMessageBox QPushButton {
    min-width: 95px;
    min-height: 30px;
    border-radius: 5px;
}
''')
QMessageBox.information(None, "提示information", "消息",
                        QMessageBox.Close |
                        QMessageBox.Discard |
                        QMessageBox.Apply |
                        QMessageBox.Reset)
sys.exit()
