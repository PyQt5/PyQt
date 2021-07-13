# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testTree.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(719, 544)
        self.treeWidget = QtWidgets.QTreeWidget(Form)
        self.treeWidget.setGeometry(QtCore.QRect(80, 80, 256, 192))
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Unchecked)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.treeWidget.headerItem().setText(0, _translate("Form", "测试"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("Form", "测试1"))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("Form", "子节点1"))
        self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("Form", "字节点2"))
        self.treeWidget.topLevelItem(0).child(2).setText(0, _translate("Form", "字节点3"))
        self.treeWidget.topLevelItem(0).child(3).setText(0, _translate("Form", "字节点4"))
        self.treeWidget.topLevelItem(0).child(4).setText(0, _translate("Form", "字节点5"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
