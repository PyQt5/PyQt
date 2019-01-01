#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年3月30日
@author: Irony."[讽刺]
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: AwesomeFont
@description: 
'''

__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2017 Irony.\"[讽刺]"
__Version__ = "Version 1.0"

import sys

from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout,\
    QScrollArea, QPushButton

from Lib.FontAwesome import FontAwesomes  # @UnresolvedImport


class ScrollArea(QScrollArea):

    def __init__(self):
        super(ScrollArea, self).__init__()
        self.setWindowTitle("FontAwesome Fonts")
        self.window = QWidget(self)
        self.setWidget(self.window)

        layout = QGridLayout(self.window)
        fonts = list(FontAwesomes.alls().items())  # 786个 131*6
        print(fonts)

        for row in range(131):
            for col in range(6):
                #         print(row, col, row * 6 + col)
                layout.addWidget(QPushButton(
                    ": ".join(fonts[row * 6 + col]),
                    self.window,
                    minimumHeight=33,
                    font=QFont("FontAwesome", 14)),
                    row, col, 1, 1)
        
        self.showMaximized()

    def resizeEvent(self, event):
        super(ScrollArea, self).resizeEvent(event)
        self.window.resize(self.width(), self.height() * 4)


app = QApplication(sys.argv)
app.setStyleSheet("""QPushButton:hover {
    color: green;
}
QPushButton:pressed {
    color: red;
}
""")

QFontDatabase.addApplicationFont(
    "Data/Fonts/fontawesome-webfont.ttf")

window = ScrollArea()

window.show()
sys.exit(app.exec_())
