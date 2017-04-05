#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年4月5日
@author: Irony."[讽刺]
@site: alyl.vip, orzorz.vip, irony.coding.me , irony.iask.in , mzone.iask.in
@email: 892768447@qq.com
@file: widgets.WidgetCode
@description: 
'''
from random import sample
import string

from PyQt5.QtCore import Qt, qrand, QPointF, QPoint
from PyQt5.QtGui import QPainter, QBrush, QFont, QPen, QFontDatabase
from PyQt5.QtWidgets import QLabel, QLineEdit


__version__ = "0.0.1"

DEF_NOISYPOINTCOUNT = 60  # 噪点数量
COLORLIST = ("black", "gray", "red", "green", "blue", "cyan", "magenta")
QTCOLORLIST = (Qt.darkGray, Qt.darkRed, Qt.darkGreen, Qt.darkBlue, Qt.darkCyan, Qt.darkMagenta)
HTML = "<html><body>{html}</body></html>"
FONT = "<font color=\"{color}\">{word}</font>"
WORDS = list(string.ascii_letters + string.digits)

class WidgetCode(QLabel):
    
    def __init__(self, *args, **kwargs):
        super(WidgetCode, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setFont(QFont("Jokerman", 16))
        self.reset()
        
    def reset(self):
        self._code = "".join(sample(WORDS, 4))  # 随机4个字符
        self.setText(self._code)
    
    def check(self, code):
        # 校验
        print("check", self._code.lower(), str(code).lower())
        return self._code.lower() == str(code).lower()
    
    def setText(self, text=""):
        self._code = text
        html = "".join([FONT.format(color=COLORLIST[qrand() % 7], word=t) for t in text])
        super(WidgetCode, self).setText(HTML.format(html=html))
    
    def mouseReleaseEvent(self, event):
        super(WidgetCode, self).mouseReleaseEvent(event)
        self.reset()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 背景白色
        painter.fillRect(event.rect(), QBrush(Qt.white))
        # 绘制边缘虚线框
        painter.setPen(Qt.DashLine)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(self.rect())
        # 随机画条线
        for _ in range(3):
            painter.setPen(QPen(QTCOLORLIST[qrand() % 6], 1, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawLine(QPoint(0, qrand() % self.height()),
                             QPoint(self.width(), qrand() % self.height()))
            painter.drawLine(QPoint(qrand() % self.width(), 0),
                             QPoint(qrand() % self.width(), self.height()))
        # 绘制噪点
        painter.setPen(Qt.DotLine)
        painter.setBrush(Qt.NoBrush)
        for _ in range(self.width()):  # 绘制噪点
            painter.drawPoint(QPointF(qrand() % self.width(), qrand() % self.height()))
        super(WidgetCode, self).paintEvent(event)  # 绘制文字

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout
    app = QApplication(sys.argv)
    app.setApplicationName("Validate Code")
    QFontDatabase.addApplicationFont("Jokerman.ttf")
    w = QWidget()
    layout = QHBoxLayout(w)
    
    cwidget = WidgetCode(w, minimumHeight=48, minimumWidth=100)
    layout.addWidget(cwidget)
    lineEdit = QLineEdit(w, maxLength=4, placeholderText="请输入验证码并按回车验证",
            returnPressed=lambda:print(cwidget.check(lineEdit.text())))
    layout.addWidget(lineEdit)
    w.show()
    sys.exit(app.exec_())
