#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年1月17日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: question
@description: 
'''

__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"

import sys

from PyQt5.QtWidgets import QApplication, QMessageBox


app = QApplication(sys.argv)
app.setStyleSheet('''
QPushButton[text="Restore Defaults"] {
    background: red;
    qproperty-icon: url(../icons/RestoreDefaults.png);
}
QPushButton[text="Restore Defaults"]:hover {
    background: darkRed;
}

QPushButton[text="Help"] {
    background: green;
    qproperty-icon: url(../icons/Help.png);
}
QPushButton[text="Help"]:hover {
    background: darkGreen;
}

QPushButton[text="Save All"] {
    background: blue;
    qproperty-icon: url(../icons/SaveAll.png);
}
QPushButton[text="Save All"]:hover {
    background: darkBlue;
}

QPushButton[text="&Yes"] {
    background: cyan;
    qproperty-icon: url(../icons/Yes.png);
}
QPushButton[text="&Yes"]:hover {
    background: darkCyan;
}

QPushButton[text="Yes to &All"] {
    background: magenta;
    qproperty-icon: url(../icons/YesToAll.png);
}
QPushButton[text="Yes to &All"]:hover {
    background: darkMegenta;
}

QMessageBox {
    messagebox-question-icon: url(../icons/Close.png);
}

QMessageBox QPushButton {
    min-width: 95px;
    min-height: 30px;
    border-radius: 5px;
}
''')
QMessageBox.question(None, "提示question", "消息",
                     QMessageBox.RestoreDefaults |
                     QMessageBox.Help |
                     QMessageBox.SaveAll |
                     QMessageBox.Yes |
                     QMessageBox.YesToAll)
sys.exit()
