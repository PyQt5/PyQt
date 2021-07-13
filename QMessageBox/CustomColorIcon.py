#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年1月17日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: CustomBtnIcon
@description: 
"""

import sys

try:
    from PyQt5.QtWidgets import QApplication, QMessageBox
except ImportError:
    from PySide2.QtWidgets import QApplication, QMessageBox

app = QApplication(sys.argv)
app.setStyleSheet('''QDialogButtonBox {
    dialogbuttonbox-buttons-have-icons: 1;
    dialog-ok-icon: url(Data/icons/Ok.png);
    dialog-open-icon: url(Data/icons/Open.png);
    dialog-save-icon: url(Data/icons/Save.png);
    dialog-cancel-icon: url(Data/icons/Cancel.png);
}

#qt_msgbox_label {
    color: red;
    background: green;
}

#qt_msgboxex_icon_label {
    background: red;
}

QMessageBox {
    background: black;
    messagebox-information-icon: url(Data/icons/Close.png);
}

QMessageBox QPushButton {
    padding: 2px;
    border-radius: 5px;
    background: white;
}

QMessageBox QPushButton:hover {
    background: darkCyan;
}

QMessageBox QPushButton[text="Reset"] {
    background: red;
}

QMessageBox QPushButton[text="Apply"] {
    background: cyan;
    qproperty-icon: url(Data/icons/Apply.png);
}
''')
QMessageBox.information(None, "information", "消息",
                        QMessageBox.Apply |
                        QMessageBox.Cancel |
                        QMessageBox.Close |
                        QMessageBox.Discard |
                        QMessageBox.Help |
                        QMessageBox.No |
                        QMessageBox.Ok |
                        QMessageBox.Open |
                        QMessageBox.Reset |
                        QMessageBox.Save |
                        QMessageBox.Yes)
sys.exit()
