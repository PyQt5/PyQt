#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年1月17日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
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
app.setStyleSheet('''QDialogButtonBox {
    dialogbuttonbox-buttons-have-icons: 1;
    dialog-no-icon: url(../icons/No.png);
    dialog-abort-icon: url(../icons/Abort.png);
    dialog-retry-icon: url(../icons/Retry.png);
    dialog-ignore-icon: url(../icons/Ignore.png);
}

QMessageBox {
    messagebox-warning-icon: url(../icons/Ok.png);
}
''')
QMessageBox.warning(None, "提示warning", "消息",
                    QMessageBox.No |
                    QMessageBox.NoToAll |
                    QMessageBox.Abort |
                    QMessageBox.Retry |
                    QMessageBox.Ignore)
sys.exit()
