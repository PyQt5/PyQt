#!/usr/bin/env python
# encoding: utf-8
"""
Created on 2017年4月21日
@author: weike32
@site: https://pyqt.site ,https://github.com/weike32
@email: 394967319@qq.com
@file: CopyContent
@description: 查阅了很多博客，如果有异，可以联系作者邮箱。本Demo仅作学习参考用，保有后续相关权益。
"""
import sys

try:
    from PyQt5 import QtWidgets
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PySide2 import QtWidgets
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *


class MyTable(QTableWidget):
    def __init__(self, parent=None):
        super(MyTable, self).__init__(parent)
        self.setWindowTitle("我是一个表格")
        self.setWindowIcon(QIcon("male.png"))
        self.resize(920, 240)
        self.setColumnCount(6)
        self.setRowCount(2)
        # 设置表格有两行五列。
        self.setColumnWidth(0, 200)
        self.setColumnWidth(4, 200)
        self.setRowHeight(0, 100)
        # 设置第一行高度为100px，第一列宽度为200px。

        self.table()

    def table(self):
        self.setItem(0, 0, QTableWidgetItem("你的名字"))
        self.setItem(0, 1, QTableWidgetItem("性别"))
        self.setItem(0, 2, QTableWidgetItem("出生日期"))
        self.setItem(0, 3, QTableWidgetItem("职业"))
        self.setItem(0, 4, QTableWidgetItem("收入"))
        self.setItem(0, 5, QTableWidgetItem("进度条"))
        # 添加表格的文字内容.
        self.setHorizontalHeaderLabels(["第一行", "第二行", "第三行", "第四行", "第五行", "第六行"])
        self.setVerticalHeaderLabels(["第一列", "第二列"])
        # 设置表头
        lbp = QLabel()
        lbp.setPixmap(QPixmap("youPicture.png"))
        self.setCellWidget(1, 1, lbp)
        # 在表中添加一张图片
        twi = QTableWidgetItem("Graph")
        twi.setFont(QFont("Times", 10, ))
        self.setItem(1, 0, twi)

        # 添加一个自己设置了大小和类型的文字。
        dte = QDateTimeEdit()
        dte.setDateTime(QDateTime.currentDateTime())
        dte.setDisplayFormat("yyyy/MM/dd")
        dte.setCalendarPopup(True)
        self.setCellWidget(1, 2, dte)
        # 添加一个弹出的日期选择，设置默认值为当前日期,显示格式为年月日。
        cbw = QComboBox()
        cbw.addItem("医生")
        cbw.addItem("老师")
        cbw.addItem("律师")
        self.setCellWidget(1, 3, cbw)
        # 添加了一个下拉选择框
        sb = QSpinBox()
        sb.setRange(1000, 10000)
        sb.setValue(5000)  # 设置最开始显示的数字
        sb.setDisplayIntegerBase(10)  # 这个是显示数字的进制，默认是十进制。
        sb.setSuffix("元")  # 设置后辍
        sb.setPrefix("RMB: ")  # 设置前辍
        sb.setSingleStep(100)
        self.setCellWidget(1, 4, sb)
        # 添加一个进度条

        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.setCellWidget(1, 5, self.progressBar)
        self.step = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        # 信号连接到槽
        self.timer.timeout.connect(self.onTimerOut)
        self.count = 0

    def onTimerOut(self):  # 重写timerEvent
        self.count += 1
        if self.count >= 100:  # value >= 100时，停止计时器
            self.timer.stop()
            print("结束")
            # self.progressBar.setValue(self.step)
        else:
            print(self.count)
            self.progressBar.setValue(self.count)
            # return
            # self.step += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myTable = MyTable()
    myTable.show()
    app.exit(app.exec_())
