#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年1月17日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
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
app.setStyleSheet('''QDialogButtonBox {
    dialogbuttonbox-buttons-have-icons: 1;
    dialog-ok-icon: url(../icons/Ok.png);
    dialog-open-icon: url(../icons/Open.png);
    dialog-save-icon: url(../icons/Save.png);
    dialog-cancel-icon: url(../icons/Cancel.png);
}

QMessageBox {
    messagebox-critical-icon: url(../icons/Close.png);
}
''')
QMessageBox.critical(None, "提示critical", "消息",
                     QMessageBox.Ok |
                     QMessageBox.Open |
                     QMessageBox.Save |
                     QMessageBox.Cancel)
sys.exit()
