# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\pyPro\hoverMenu\UThroughTrain4\GeographicAnalysis_Widget.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(528, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.analyzed_csv_label = QtWidgets.QLabel(Form)
        self.analyzed_csv_label.setObjectName("analyzed_csv_label")
        self.horizontalLayout.addWidget(self.analyzed_csv_label)
        self.choose_file = QtWidgets.QPushButton(Form)
        self.choose_file.setObjectName("choose_file")
        self.horizontalLayout.addWidget(self.choose_file)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.start_analysis = QtWidgets.QPushButton(Form)
        self.start_analysis.setObjectName("start_analysis")
        self.horizontalLayout.addWidget(self.start_analysis)
        self.clear_data = QtWidgets.QPushButton(Form)
        self.clear_data.setObjectName("clear_data")
        self.horizontalLayout.addWidget(self.clear_data)
        self.download_excel = QtWidgets.QPushButton(Form)
        self.download_excel.setObjectName("download_excel")
        self.horizontalLayout.addWidget(self.download_excel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.analyzed_csv = QtWidgets.QLabel(Form)
        self.analyzed_csv.setObjectName("analyzed_csv")
        self.horizontalLayout_2.addWidget(self.analyzed_csv)
        self.file_name = QtWidgets.QLineEdit(Form)
        self.file_name.setObjectName("file_name")
        self.horizontalLayout_2.addWidget(self.file_name)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.geographicAnalysis_table = QtWidgets.QTableWidget(Form)
        self.geographicAnalysis_table.setObjectName("geographicAnalysis_table")
        self.geographicAnalysis_table.setColumnCount(6)
        self.geographicAnalysis_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.geographicAnalysis_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.geographicAnalysis_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.geographicAnalysis_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.geographicAnalysis_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.geographicAnalysis_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.geographicAnalysis_table.setHorizontalHeaderItem(5, item)
        self.verticalLayout.addWidget(self.geographicAnalysis_table)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.analyzed_csv_label.setText(_translate("Form", "选择待分析的数据表(*.csv)："))
        self.choose_file.setText(_translate("Form", "选择文件"))
        self.start_analysis.setText(_translate("Form", "开始分析"))
        self.clear_data.setText(_translate("Form", "数据清理"))
        self.download_excel.setText(_translate("Form", "导出Excel"))
        self.analyzed_csv.setText(_translate("Form", "当前文件："))
        item = self.geographicAnalysis_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "省份"))
        item = self.geographicAnalysis_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "城市"))
        item = self.geographicAnalysis_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "订单数（市）"))
        item = self.geographicAnalysis_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "百分比（市）"))
        item = self.geographicAnalysis_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "订单数（省）"))
        item = self.geographicAnalysis_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "百分比（省）"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

