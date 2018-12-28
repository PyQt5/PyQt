#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年1月17日
@author: Irony."[讽刺]
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: critical
@description: 
'''

__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"

import sys

from PyQt5.QtWidgets import QApplication, QMessageBox


app = QApplication(sys.argv)
app.setStyleSheet('''
QPushButton[text="OK"] {
    background: red;
    qproperty-icon: url(../icons/Ok.png);
}
QPushButton[text="OK"]:hover {
    background: darkRed;
}

QPushButton[text="Open"] {
    background: green;
    qproperty-icon: url(../icons/Open.png);
}
QPushButton[text="Open"]:hover {
    background: darkGreen;
}

QPushButton[text="Save"] {
    background: blue;
    qproperty-icon: url(../icons/Save.png);
}
QPushButton[text="Save"]:hover {
    background: darkBlue;
}

QPushButton[text="Cancel"] {
    background: cyan;
    qproperty-icon: url(../icons/Cancel.png);
}
QPushButton[text="Cancel"]:hover {
    background: darkCyan;
}

QMessageBox {
    messagebox-critical-icon: url(../icons/Close.png);
}

QMessageBox QPushButton {
    min-width: 95px;
    min-height: 30px;
    border-radius: 5px;
}
''')
QMessageBox.critical(None, "提示critical", "消息",
                     QMessageBox.Ok |
                     QMessageBox.Open |
                     QMessageBox.Save |
                     QMessageBox.Cancel)
sys.exit()
