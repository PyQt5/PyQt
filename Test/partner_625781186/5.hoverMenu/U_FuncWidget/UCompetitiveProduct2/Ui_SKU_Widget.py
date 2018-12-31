# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\QGroup_432987409\WoHowLearn\0.M_I_pyqt\partner_625781186\5.hoverMenu\U_FuncWidget\UCompetitiveProduct2\SKU_Widget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(578, 340)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.product_links = QtWidgets.QLabel(Form)
        self.product_links.setObjectName("product_links")
        self.horizontalLayout.addWidget(self.product_links)
        self.product_links_textarea = QtWidgets.QLineEdit(Form)
        self.product_links_textarea.setObjectName("product_links_textarea")
        self.horizontalLayout.addWidget(self.product_links_textarea)
        self.start_collecting = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_collecting.sizePolicy().hasHeightForWidth())
        self.start_collecting.setSizePolicy(sizePolicy)
        self.start_collecting.setObjectName("start_collecting")
        self.horizontalLayout.addWidget(self.start_collecting)
        self.clear = QtWidgets.QPushButton(Form)
        self.clear.setObjectName("clear")
        self.horizontalLayout.addWidget(self.clear)
        self.export_data = QtWidgets.QPushButton(Form)
        self.export_data.setObjectName("export_data")
        self.horizontalLayout.addWidget(self.export_data)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.productHeader = QtWidgets.QTableWidget(self.splitter)
        self.productHeader.setObjectName("productHeader")
        self.productHeader.setColumnCount(2)
        self.productHeader.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.productHeader.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.productHeader.setHorizontalHeaderItem(1, item)
        self.productCountHeader = QtWidgets.QTableWidget(self.splitter)
        self.productCountHeader.setObjectName("productCountHeader")
        self.productCountHeader.setColumnCount(2)
        self.productCountHeader.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.productCountHeader.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.productCountHeader.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.splitter)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.product_links.setText(_translate("Form", "宝贝链接："))
        self.start_collecting.setText(_translate("Form", "开始采集"))
        self.clear.setText(_translate("Form", "清空"))
        self.export_data.setText(_translate("Form", "导出数据"))
        item = self.productHeader.horizontalHeaderItem(0)
        item.setText(_translate("Form", "序号"))
        item = self.productHeader.horizontalHeaderItem(1)
        item.setText(_translate("Form", "SKU"))
        item = self.productCountHeader.horizontalHeaderItem(0)
        item.setText(_translate("Form", "序号"))
        item = self.productCountHeader.horizontalHeaderItem(1)
        item.setText(_translate("Form", "数量"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

