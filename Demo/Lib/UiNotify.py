# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notify.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except ImportError:
    from PySide2 import QtCore, QtGui, QtWidgets


class Ui_NotifyForm(object):
    def setupUi(self, NotifyForm):
        NotifyForm.setObjectName("NotifyForm")
        NotifyForm.resize(300, 200)
        NotifyForm.setStyleSheet("QWidget#widgetTitle {\n"
                                 "    background-color: rgb(76, 169, 106);\n"
                                 "}\n"
                                 "QWidget#widgetBottom {\n"
                                 "    border-top-style: solid;\n"
                                 "    border-top-width: 2px;\n"
                                 "    border-top-color: rgb(185, 218, 201);\n"
                                 "}\n"
                                 "QLabel#labelTitle {\n"
                                 "    color: rgb(255, 255, 255);\n"
                                 "}\n"
                                 "QLabel#labelContent {\n"
                                 "    padding: 5px;\n"
                                 "}\n"
                                 "QPushButton {\n"
                                 "    border: none;\n"
                                 "    background: transparent;\n"
                                 "}\n"
                                 "QPushButton#buttonClose {\n"
                                 "    font-family: \"webdings\";\n"
                                 "    color: rgb(255, 255, 255);\n"
                                 "}\n"
                                 "QPushButton#buttonClose:hover {\n"
                                 "    background-color: rgb(212, 64, 39);\n"
                                 "}\n"
                                 "QPushButton#buttonView {\n"
                                 "    color: rgb(255, 255, 255);\n"
                                 "    border-radius: 5px;\n"
                                 "    border: solid 1px rgb(76, 169, 106);\n"
                                 "    background-color: rgb(76, 169, 106);\n"
                                 "}\n"
                                 "QPushButton#buttonView:hover {\n"
                                 "    color: rgb(0, 0, 0);\n"
                                 "}")
        self.verticalLayout = QtWidgets.QVBoxLayout(NotifyForm)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widgetTitle = QtWidgets.QWidget(NotifyForm)
        self.widgetTitle.setMinimumSize(QtCore.QSize(0, 26))
        self.widgetTitle.setObjectName("widgetTitle")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widgetTitle)
        self.horizontalLayout_3.setContentsMargins(10, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelTitle = QtWidgets.QLabel(self.widgetTitle)
        self.labelTitle.setText("")
        self.labelTitle.setObjectName("labelTitle")
        self.horizontalLayout_3.addWidget(self.labelTitle)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.buttonClose = QtWidgets.QPushButton(self.widgetTitle)
        self.buttonClose.setMinimumSize(QtCore.QSize(26, 26))
        self.buttonClose.setMaximumSize(QtCore.QSize(26, 26))
        self.buttonClose.setObjectName("buttonClose")
        self.horizontalLayout_3.addWidget(self.buttonClose)
        self.verticalLayout.addWidget(self.widgetTitle)
        self.labelContent = QtWidgets.QLabel(NotifyForm)
        self.labelContent.setText("")
        self.labelContent.setWordWrap(True)
        self.labelContent.setObjectName("labelContent")
        self.verticalLayout.addWidget(self.labelContent)
        self.widgetBottom = QtWidgets.QWidget(NotifyForm)
        self.widgetBottom.setObjectName("widgetBottom")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widgetBottom)
        self.horizontalLayout.setContentsMargins(0, 5, 5, 5)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(170, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.buttonView = QtWidgets.QPushButton(self.widgetBottom)
        self.buttonView.setMinimumSize(QtCore.QSize(75, 25))
        self.buttonView.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonView.setObjectName("buttonView")
        self.horizontalLayout.addWidget(self.buttonView)
        self.verticalLayout.addWidget(self.widgetBottom)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(NotifyForm)
        QtCore.QMetaObject.connectSlotsByName(NotifyForm)

    def retranslateUi(self, NotifyForm):
        _translate = QtCore.QCoreApplication.translate
        NotifyForm.setWindowTitle(_translate("NotifyForm", "消息提示"))
        self.buttonClose.setText(_translate("NotifyForm", "r"))
        self.buttonView.setText(_translate("NotifyForm", "查 看"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    NotifyForm = QtWidgets.QWidget()
    ui = Ui_NotifyForm()
    ui.setupUi(NotifyForm)
    NotifyForm.show()
    sys.exit(app.exec_())
