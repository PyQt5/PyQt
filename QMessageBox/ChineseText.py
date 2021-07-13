#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月10日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: ChineseText
@description: 修改消息对话框文字汉化
"""
import sys

try:
    from PyQt5.QtWidgets import QApplication, QMessageBox
except ImportError:
    from PySide2.QtWidgets import QApplication, QMessageBox

TextStyle = """
QMessageBox QPushButton[text="OK"] {
    qproperty-text: "好的";
}
QMessageBox QPushButton[text="Open"] {
    qproperty-text: "打开";
}
QMessageBox QPushButton[text="Save"] {
    qproperty-text: "保存";
}
QMessageBox QPushButton[text="Cancel"] {
    qproperty-text: "取消";
}
QMessageBox QPushButton[text="Close"] {
    qproperty-text: "关闭";
}
QMessageBox QPushButton[text="Discard"] {
    qproperty-text: "不保存";
}
QMessageBox QPushButton[text="Don't Save"] {
    qproperty-text: "不保存";
}
QMessageBox QPushButton[text="Apply"] {
    qproperty-text: "应用";
}
QMessageBox QPushButton[text="Reset"] {
    qproperty-text: "重置";
}
QMessageBox QPushButton[text="Restore Defaults"] {
    qproperty-text: "恢复默认";
}
QMessageBox QPushButton[text="Help"] {
    qproperty-text: "帮助";
}
QMessageBox QPushButton[text="Save All"] {
    qproperty-text: "保存全部";
}
QMessageBox QPushButton[text="&Yes"] {
    qproperty-text: "是";
}
QMessageBox QPushButton[text="Yes to &All"] {
    qproperty-text: "全部都是";
}
QMessageBox QPushButton[text="&No"] {
    qproperty-text: "不";
}
QMessageBox QPushButton[text="N&o to All"] {
    qproperty-text: "全部都不";
}
QMessageBox QPushButton[text="Abort"] {
    qproperty-text: "终止";
}
QMessageBox QPushButton[text="Retry"] {
    qproperty-text: "重试";
}
QMessageBox QPushButton[text="Ignore"] {
    qproperty-text: "忽略";
}
"""

app = QApplication(sys.argv)

# 通过QSS样式的方式设置按钮文字
app.setStyleSheet(TextStyle)

# 由于年代久远，Qt5的翻译功能没有更新，还是用的旧的结构导致无法翻译
# 这里不使用（需要修改ts源码重新编译成qm）
# translator = QTranslator()
# print(translator.load(QLocale(), 'qt', '_', QLibraryInfo.location(
#     QLibraryInfo.TranslationsPath)))
# app.installTranslator(translator)

QMessageBox.information(
    None, 'information', '消息',
    QMessageBox.Ok |
    QMessageBox.Open |
    QMessageBox.Save |
    QMessageBox.Cancel |
    QMessageBox.Close |
    QMessageBox.Discard |
    QMessageBox.Apply |
    QMessageBox.Reset |
    QMessageBox.RestoreDefaults |
    QMessageBox.Help |
    QMessageBox.SaveAll |
    QMessageBox.Yes |
    QMessageBox.YesToAll |
    QMessageBox.No |
    QMessageBox.NoToAll |
    QMessageBox.Abort |
    QMessageBox.Retry |
    QMessageBox.Ignore
)
sys.exit()
