#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年1月17日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
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
app.setStyleSheet('''QDialogButtonBox {
    dialogbuttonbox-buttons-have-icons: 1;
    dialog-close-icon: url(../icons/Close.png);
    dialog-discard-icon: url(../icons/Discard.png);
    dialog-apply-icon: url(../icons/Apply.png);
    dialog-reset-icon: url(../icons/Reset.png);
}

QMessageBox {
    messagebox-information-icon: url(../icons/Ok.png);
}
''')
QMessageBox.information(None, "提示information", "消息",
                        QMessageBox.Close |
                        QMessageBox.Discard |
                        QMessageBox.Apply |
                        QMessageBox.Reset)
sys.exit()
