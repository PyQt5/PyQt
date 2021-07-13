#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年2月2日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: QtQuick.FlatStyle
@description: 
"""
import os
import sys

try:
    from PyQt5.QtCore import QCoreApplication, Qt, QUrl
    from PyQt5.QtQml import QQmlApplicationEngine
    from PyQt5.QtWidgets import QApplication, QMessageBox
except ImportError:
    from PySide2.QtCore import QCoreApplication, Qt, QUrl
    from PySide2.QtQml import QQmlApplicationEngine
    from PySide2.QtWidgets import QApplication, QMessageBox

if __name__ == '__main__':
    try:
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    except:
        pass

    os.chdir('FlatStyle')

    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.objectCreated.connect(
        lambda obj, _: (
            QMessageBox.critical(None, '错误', '运行失败，可能是当前PyQt版本不支持'), engine.quit) if not obj else 0)
    engine.addImportPath('imports')
    engine.load(QUrl('flatstyle.qml'))

    sys.exit(app.exec_())
