# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graphAnalysis.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class graph_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1024, 768)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setContentsMargins(20, 20, 20, 20)
        self.gridLayout_3.setSpacing(20)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_7 = QtWidgets.QPushButton(Form)
        self.pushButton_7.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_3.addWidget(self.pushButton_7, 2, 2, 1, 2)
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 4)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_3.addWidget(self.tabWidget, 1, 1, 1, 4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_7.setText(_translate("Form", "分析"))
        self.label.setText(_translate("Form", "图形分析"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "折线图"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Tab 2"))
