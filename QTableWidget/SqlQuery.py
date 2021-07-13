#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年5月15日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: SqlQuery
@description: 
"""

try:
    from PyQt5.QtCore import pyqtSlot
    from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
except ImportError:
    from PySide2.QtCore import Slot as pyqtSlot
    from PySide2.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import and_
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, Text

from Lib.mainui import Ui_Form

# engine = create_engine('mysql+mysqldb://root@localhost:3306/tourist?charset=utf8')
engine = create_engine('sqlite:///Data/data.sqlite3', echo=True)  # echo 表示开启命令显示
Base = declarative_base()


class Tourist(Base):
    __tablename__ = 'tourist'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    license = Column(Text)
    flightnumber = Column(Text)
    flightdate = Column(Text)
    seatnumber = Column(Text)
    boardingport = Column(Text)
    no = Column(Text)
    departurestation = Column(Text)
    destinationstation = Column(Text)


class Window(QWidget, Ui_Form):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # sql的拼接字段
        self.sql = {}
        # 数据库连接
        self.session = sessionmaker(bind=engine)()

    @pyqtSlot()
    def on_pushButtonQuery_clicked(self):
        """查询按钮"""
        self.applyName()
        self.applySeat()
        self.applyLicense()
        self.applyPort()
        if not self.sql:
            return QMessageBox.warning(self, '提示', '没有进行任何输入')
        # 清空数据
        self.tableWidget.clear()
        # 重新设置表头
        self.tableWidget.setHorizontalHeaderLabels(
            ['编号', '姓名', '证件号', '航班号', '航班日期', '座位号', '登机口', '序号', '出发地', '目的地'])
        # 根据选择的字段进行并列查询
        rets = self.session.query(Tourist).filter(
            and_(*(key == value for key, value in self.sql.items()))).all()
        if not rets:
            return QMessageBox.information(self, '提示', '未查询到结果')
        self.tableWidget.setRowCount(len(rets))
        # 根据查询结果添加到表格中
        for row, tourist in enumerate(rets):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(tourist.id)))
            self.tableWidget.setItem(
                row, 1, QTableWidgetItem(str(tourist.name)))
            self.tableWidget.setItem(
                row, 2, QTableWidgetItem(str(tourist.license)))
            self.tableWidget.setItem(
                row, 3, QTableWidgetItem(str(tourist.flightnumber)))
            self.tableWidget.setItem(
                row, 4, QTableWidgetItem(str(tourist.flightdate)))
            self.tableWidget.setItem(
                row, 5, QTableWidgetItem(str(tourist.seatnumber)))
            self.tableWidget.setItem(
                row, 6, QTableWidgetItem(str(tourist.boardingport)))
            self.tableWidget.setItem(row, 7, QTableWidgetItem(str(tourist.no)))
            self.tableWidget.setItem(
                row, 8, QTableWidgetItem(str(tourist.departurestation)))
            self.tableWidget.setItem(
                row, 9, QTableWidgetItem(str(tourist.destinationstation)))

    def applyName(self):
        """姓名"""
        if not self.checkBoxName.isChecked():
            if Tourist.name in self.sql:
                # 移除
                self.sql.pop(Tourist.name)
        # 更新或添加到字典里
        else:
            self.sql[Tourist.name] = self.lineEditName.text().strip()

    def applySeat(self):
        """座位号"""
        if not self.checkBoxSeat.isChecked():
            if Tourist.seatnumber in self.sql:
                # 移除
                self.sql.pop(Tourist.seatnumber)
        # 更新或添加到字典里
        else:
            self.sql[Tourist.seatnumber] = self.lineEditSeat.text().strip()

    def applyLicense(self):
        """证件号"""
        if not self.checkBoxLicense.isChecked():
            if Tourist.license in self.sql:
                # 移除
                self.sql.pop(Tourist.license)
        # 更新或添加到字典里
        else:
            self.sql[Tourist.license] = self.lineEditLicense.text().strip()

    def applyPort(self):
        """登机口"""
        if not self.checkBoxPort.isChecked():
            if Tourist.boardingport in self.sql:
                # 移除
                self.sql.pop(Tourist.boardingport)
        # 更新或添加到字典里
        else:
            self.sql[Tourist.boardingport] = self.lineEditPort.text().strip()


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
