#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年1月17日
@author: Irony."[讽刺]
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: warning
@description: 
'''

__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"

import sys

from PyQt5.QtWidgets import QApplication, QMessageBox


app = QApplication(sys.argv)
app.setStyleSheet('''
QPushButton[text="&No"] {
    background: red;
    qproperty-icon: url(../icons/No.png);
}
QPushButton[text="&No"]:hover {
    background: darkRed;
}

QPushButton[text="N&o to All"] {
    background: green;
    qproperty-icon: url(../icons/NoToAll.png);
}
QPushButton[text="N&o to All"]:hover {
    background: darkGreen;
}

QPushButton[text="Abort"] {
    background: blue;
    qproperty-icon: url(../icons/Abort.png);
}
QPushButton[text="Abort"]:hover {
    background: darkBlue;
}

QPushButton[text="Retry"] {
    background: cyan;
    qproperty-icon: url(../icons/Retry.png);
}
QPushButton[text="Retry"]:hover {
    background: darkCyan;
}

QPushButton[text="Ignore"] {
    background: magenta;
    qproperty-icon: url(../icons/Ignore.png);
}
QPushButton[text="Ignore"]:hover {
    background: darkMegenta;
}

QMessageBox {
    messagebox-warning-icon: url(../icons/No.png);
}

QMessageBox QPushButton {
    min-width: 95px;
    min-height: 30px;
    border-radius: 5px;
}

QMessageBox QLabel {
    color: red;
}
''')
QMessageBox.warning(None, "提示warning", "消息",
                    QMessageBox.No |
                    QMessageBox.NoToAll |
                    QMessageBox.Abort |
                    QMessageBox.Retry |
                    QMessageBox.Ignore)
sys.exit()
