# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\QGroup_432987409\WoHowLearn\0.M_I_pyqt\partner_625781186\CodeTip\ui\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(486, 313)
        MainWindow.setStyleSheet("QListView::item:alternate {\n"
"   \n"
"    background-color: rgb(85, 255, 255);\n"
"}")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.l3 = QtWidgets.QLineEdit(self.centralWidget)
        self.l3.setObjectName("l3")
        self.verticalLayout.addWidget(self.l3, 6, 0, 1, 1)
        self.l1 = QtWidgets.QLineEdit(self.centralWidget)
        self.l1.setObjectName("l1")
        self.verticalLayout.addWidget(self.l1, 4, 0, 1, 1)
        self.l2 = QtWidgets.QLineEdit(self.centralWidget)
        self.l2.setObjectName("l2")
        self.verticalLayout.addWidget(self.l2, 5, 0, 1, 1)
        self.pre_btn = QtWidgets.QPushButton(self.centralWidget)
        self.pre_btn.setObjectName("pre_btn")
        self.verticalLayout.addWidget(self.pre_btn, 1, 0, 1, 1)
        self.tableView = QtWidgets.QTableView(self.centralWidget)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView, 0, 0, 1, 1)
        self.next_btn = QtWidgets.QPushButton(self.centralWidget)
        self.next_btn.setObjectName("next_btn")
        self.verticalLayout.addWidget(self.next_btn, 2, 0, 1, 1)
        self.listView = QtWidgets.QListView(self.centralWidget)
        self.listView.setObjectName("listView")
        self.verticalLayout.addWidget(self.listView, 0, 1, 1, 1)
        self.sub_btn = QtWidgets.QPushButton(self.centralWidget)
        self.sub_btn.setObjectName("sub_btn")
        self.verticalLayout.addWidget(self.sub_btn, 3, 0, 1, 1)
        self.l4 = QtWidgets.QLineEdit(self.centralWidget)
        self.l4.setObjectName("l4")
        self.verticalLayout.addWidget(self.l4, 7, 0, 1, 1)
        self.l5 = QtWidgets.QLineEdit(self.centralWidget)
        self.l5.setObjectName("l5")
        self.verticalLayout.addWidget(self.l5, 8, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.saveaction = QtWidgets.QAction(MainWindow)
        self.saveaction.setObjectName("saveaction")
        self.action12 = QtWidgets.QAction(MainWindow)
        self.action12.setObjectName("action12")
        self.actionas = QtWidgets.QAction(MainWindow)
        self.actionas.setObjectName("actionas")
        self.actiondz = QtWidgets.QAction(MainWindow)
        self.actiondz.setObjectName("actiondz")
        self.actiongc = QtWidgets.QAction(MainWindow)
        self.actiongc.setObjectName("actiongc")
        self.actiondb = QtWidgets.QAction(MainWindow)
        self.actiondb.setObjectName("actiondb")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pre_btn.setText(_translate("MainWindow", "上一条"))
        self.next_btn.setText(_translate("MainWindow", "下一条"))
        self.sub_btn.setText(_translate("MainWindow", "提交"))
        self.saveaction.setText(_translate("MainWindow", "保存"))
        self.saveaction.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.action12.setText(_translate("MainWindow", "查看帮助文档"))
        self.actionas.setText(_translate("MainWindow", "关于"))
        self.actiondz.setText(_translate("MainWindow", "dz"))
        self.actiongc.setText(_translate("MainWindow", "gc"))
        self.actiondb.setText(_translate("MainWindow", "db"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

