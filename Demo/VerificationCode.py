#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017年4月5日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: widgets.WidgetCode
@description: 
"""
import string
from random import sample

try:
    from PyQt5.QtCore import Qt, qrand, QPointF, QPoint, QBasicTimer
    from PyQt5.QtGui import QPainter, QBrush, QPen, QPalette, QFontMetrics, QFontDatabase
    from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QHBoxLayout, QLineEdit
except ImportError:
    from PySide2.QtCore import Qt, qrand, QPointF, QPoint, QBasicTimer
    from PySide2.QtGui import QPainter, QBrush, QPen, QPalette, QFontMetrics, QFontDatabase
    from PySide2.QtWidgets import QLabel, QApplication, QWidget, QHBoxLayout, QLineEdit

DEF_NOISYPOINTCOUNT = 60  # 噪点数量
COLORLIST = ("black", "gray", "red", "green", "blue", "magenta")
TCOLORLIST = (Qt.black, Qt.gray, Qt.red, Qt.green, Qt.blue, Qt.magenta)
QTCOLORLIST = (Qt.darkGray, Qt.darkRed, Qt.darkGreen, Qt.darkBlue, Qt.darkMagenta)
HTML = "<html><body>{html}</body></html>"
FONT = "<font color=\"{color}\">{word}</font>"
WORDS = list(string.ascii_letters + string.digits)
SINETABLE = (0, 38, 71, 92, 100, 92, 71, 38, 0, -38, -71, -92, -100, -92, -71, -38)


class WidgetCode(QLabel):

    def __init__(self, *args, **kwargs):
        super(WidgetCode, self).__init__(*args, **kwargs)
        self._sensitive = False  # 是否大小写敏感
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setBackgroundRole(QPalette.Midlight)
        self.setAutoFillBackground(True)
        # 字体
        newFont = self.font()
        newFont.setPointSize(16)
        newFont.setFamily("Kristen ITC")
        newFont.setBold(True)
        self.setFont(newFont)
        self.reset()
        # 定时器
        self.step = 0
        self.timer = QBasicTimer()
        self.timer.start(60, self)

    def reset(self):
        self._code = "".join(sample(WORDS, 4))  # 随机4个字符
        self.setText(self._code)

    def check(self, code):
        return self._code == str(code) if self._sensitive else self._code.lower() == str(code).lower()

    def setSensitive(self, sensitive):
        self._sensitive = sensitive

    #     def setText(self, text):
    #         text = text if (text and len(text) == 4) else "".join(sample(WORDS, 4))  # 随机4个字符
    #         self._code = str(text)
    #         html = "".join([FONT.format(color=COLORLIST[qrand() % 6], word=t) for t in text])
    #         super(WidgetCode, self).setText(HTML.format(html=html))

    def mouseReleaseEvent(self, event):
        super(WidgetCode, self).mouseReleaseEvent(event)
        self.reset()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.step += 1
            return self.update()
        return super(WidgetCode, self).timerEvent(event)

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
            painter.setPen(QPen(QTCOLORLIST[qrand() % 5], 1, Qt.SolidLine))
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
        # super(WidgetCode, self).paintEvent(event)  # 绘制文字
        # 绘制跳动文字
        metrics = QFontMetrics(self.font())
        x = (self.width() - metrics.width(self.text())) / 2
        y = (self.height() + metrics.ascent() - metrics.descent()) / 2
        for i, ch in enumerate(self.text()):
            index = (self.step + i) % 16
            painter.setPen(TCOLORLIST[qrand() % 6])
            painter.drawText(x, y - ((SINETABLE[index] * metrics.height()) / 400), ch)
            x += metrics.width(ch)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName("Validate Code")
    QFontDatabase.addApplicationFont("Data/itckrist.ttf")
    w = QWidget()
    layout = QHBoxLayout(w)

    cwidget = WidgetCode(w, minimumHeight=35, minimumWidth=80)
    layout.addWidget(cwidget)
    lineEdit = QLineEdit(w, maxLength=4, placeholderText="请输入验证码并按回车验证",
                         returnPressed=lambda: print(cwidget.check(lineEdit.text())))
    layout.addWidget(lineEdit)
    w.show()
    sys.exit(app.exec_())
