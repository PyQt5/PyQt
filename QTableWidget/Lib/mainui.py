# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

try:
    from PyQt5 import QtCore, QtWidgets
except ImportError:
    from PySide2 import QtCore, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 362)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.checkBoxName = QtWidgets.QCheckBox(Form)
        self.checkBoxName.setObjectName("checkBoxName")
        self.gridLayout.addWidget(self.checkBoxName, 0, 0, 1, 1)
        self.checkBoxSeat = QtWidgets.QCheckBox(Form)
        self.checkBoxSeat.setObjectName("checkBoxSeat")
        self.gridLayout.addWidget(self.checkBoxSeat, 0, 2, 1, 1)
        self.lineEditName = QtWidgets.QLineEdit(Form)
        self.lineEditName.setObjectName("lineEditName")
        self.gridLayout.addWidget(self.lineEditName, 0, 1, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        self.gridLayout.addWidget(self.tableWidget, 3, 0, 1, 4)
        self.lineEditSeat = QtWidgets.QLineEdit(Form)
        self.lineEditSeat.setObjectName("lineEditSeat")
        self.gridLayout.addWidget(self.lineEditSeat, 0, 3, 1, 1)
        self.lineEditPort = QtWidgets.QLineEdit(Form)
        self.lineEditPort.setObjectName("lineEditPort")
        self.gridLayout.addWidget(self.lineEditPort, 1, 3, 1, 1)
        self.checkBoxPort = QtWidgets.QCheckBox(Form)
        self.checkBoxPort.setObjectName("checkBoxPort")
        self.gridLayout.addWidget(self.checkBoxPort, 1, 2, 1, 1)
        self.checkBoxLicense = QtWidgets.QCheckBox(Form)
        self.checkBoxLicense.setObjectName("checkBoxLicense")
        self.gridLayout.addWidget(self.checkBoxLicense, 1, 0, 1, 1)
        self.lineEditLicense = QtWidgets.QLineEdit(Form)
        self.lineEditLicense.setObjectName("lineEditLicense")
        self.gridLayout.addWidget(self.lineEditLicense, 1, 1, 1, 1)
        self.pushButtonQuery = QtWidgets.QPushButton(Form)
        self.pushButtonQuery.setObjectName("pushButtonQuery")
        self.gridLayout.addWidget(self.pushButtonQuery, 2, 0, 1, 4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.checkBoxName.setText(_translate("Form", "姓名"))
        self.checkBoxSeat.setText(_translate("Form", "座位号"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "编号"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "姓名"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "证件号"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "航班号"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "航班日期"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "座位号"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "登机口"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Form", "序号"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("Form", "出发地"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("Form", "目的地"))
        self.checkBoxPort.setText(_translate("Form", "登机口"))
        self.checkBoxLicense.setText(_translate("Form", "证件号"))
        self.pushButtonQuery.setText(_translate("Form", "查询"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
