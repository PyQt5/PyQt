# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Administrator\Desktop\untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

"""
Created on $date$ <br>
description: 自定义combobox, 添加按钮图标  <br>
author: 东love方 <br>

"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import myRes_rc


try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

def _fromUtf8(text):
    return text

class ComboBoxWidget(QWidget):
    """
    listWidget中的单个item.
    """
    itemOpSignal = pyqtSignal(QListWidgetItem)

    def __init__(self, text, listwidgetItem):
        super().__init__()
        self.text = text
        self.listwidgetItem = listwidgetItem
        self.initUi()

    def initUi(self):
        self.horizontalLayout = QHBoxLayout(self)
        self.file_btn = QPushButton(QIcon(":/newPrefix/file.png"), self.text, self)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.file_btn.setSizePolicy(sizePolicy)
        qss = '''QPushButton 
{
    background-color: transparent;
    border: none;
}

QPushButton:hover {
    background:transparent;
    }'''
        self.file_btn.setStyleSheet(qss)
        self.bt_close = QToolButton(self)
        self.bt_close.setIcon(QIcon(":/newPrefix/if_Delete_1493279.png"))
        self.bt_close.setAutoRaise(True)
        self.bt_close.setToolTip("Delete")
        self.bt_close.clicked.connect(lambda: self.itemOpSignal.emit(self.listwidgetItem))

        self.horizontalLayout.addWidget(self.bt_close)
        self.horizontalLayout.addWidget(self.file_btn)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        


class ListQCombobox(QComboBox):

    def __init__(self, *args):
        super(ListQCombobox, self).__init__(*args)
        self.listw = QListWidget(self)
        self.setModel(self.listw.model())
        self.setView(self.listw)
        self.activated.connect(self.setTopText)
        qss = '''QComboBox QAbstractItemView::item {
                    height: 25px;
                }

                QListView::item:hover {
                    background: #BDD7FD;
                }'''
        self.setStyleSheet(qss)

    def refreshInputs(self, list_inputs):
        self.clear()
        # 循环实例化添加item
        for num, path in enumerate(list_inputs):
            listwitem = QListWidgetItem(self.listw)
            listwitem.setToolTip(path)
            itemWidget = ComboBoxWidget(os.path.basename(path), listwitem)
            itemWidget.itemOpSignal.connect(self.removeCombo)
            # 背景颜色
            if num % 2 == 0:
                listwitem.setBackground(QColor(255, 255, 255))
            else:
                listwitem.setBackground(QColor(237, 243, 254))
            listwitem.setSizeHint(itemWidget.sizeHint())
            self.listw.addItem(listwitem)
            self.listw.setItemWidget(listwitem, itemWidget)
        self.setTopText()

    def setTopText(self):
        list_text = self.fetchListsText()
        if len(list_text) > 1:
            topText = "%d input files"%len(list_text)
        elif len(list_text) == 1:
            topText = os.path.basename(list_text[0])
        else:
            topText = "No input files"
        self.setEditText(topText)

    def refreshBackColors(self):
        for row in range(self.view().count()):
            if row % 2 == 0:
                self.view().item(row).setBackground(QColor(255, 255, 255))
            else:
                self.view().item(row).setBackground(QColor(237, 243, 254))

    def removeCombo(self, listwidgetItem):
        view = self.view()
        index = view.indexFromItem(listwidgetItem)
        view.takeItem(index.row())
        self.refreshBackColors()
        self.setTopText()

    def fetchListsText(self):
        return [self.view().item(row).toolTip() for row in range(self.view().count())]

    def fetchCurrentText(self):
        if self.view().count():
            return self.view().item(0).toolTip()
        else:
            return ""

    def count(self):
        return self.view().count()


class Ui_Dialog(QDialog):

    def __init__(self, parent=None):
        super(Ui_Dialog, self).__init__(parent)
        self.setupUi()
        list_new_inputs = [r"../0.jpg",
                           r"../00.jpg",
                           r"../2.jpg",
                           r"../3.jpg"]
        self.comboBox_4.refreshInputs(list_new_inputs)

    def setupUi(self):
        self.resize(366, 173)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.comboBox_4 = ListQCombobox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_4.sizePolicy().hasHeightForWidth())
        self.comboBox_4.setSizePolicy(sizePolicy)
        self.comboBox_4.setAcceptDrops(True)
        self.comboBox_4.setEditable(True)
        self.comboBox_4.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_4.setObjectName(_fromUtf8("comboBox_4"))
        self.gridLayout.addWidget(self.comboBox_4, 0, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setMinimumSize(QtCore.QSize(30, 26))
        self.pushButton_3.setMaximumSize(QtCore.QSize(30, 26))
        self.pushButton_3.setStyleSheet(_fromUtf8(""))
        self.pushButton_3.setText(_fromUtf8(""))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 0, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 3)
        self.pushButton.clicked.connect(lambda: print(self.comboBox_4.view().width()))

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_4.setText(_translate("Dialog", "text:", None))
        self.pushButton.setText(_translate("Dialog", "Get combobox width", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = Ui_Dialog()
    dialog.show()
    sys.exit(app.exec_())

