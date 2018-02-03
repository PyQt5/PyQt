#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年2月3日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: TestLineEdit
@description: 
'''
import sys
sys.path.insert(0, "../../")
print(sys.path)

from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel

from Material.Utils import Colors  # @UnresolvedImport
from Material.Widget.LineEdit import LineEdit  # @UnresolvedImport


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QGridLayout(self)
        colors = Colors.alls()
        for row, key in enumerate(colors):
            layout.addWidget(QLabel(key, self), row, 0, 1, 1)
            for column, value in enumerate(colors.get(key)):
                line = LineEdit(value._name, self)
                line.lineColor = value
#                 line.setEnabled(randrange(0, 2))
                layout.addWidget(line, row, column + 1, 1, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("LineEdit")
    app.setApplicationName("LineEdit")
    w = Window()
    w.show()
    sys.exit(app.exec_())
