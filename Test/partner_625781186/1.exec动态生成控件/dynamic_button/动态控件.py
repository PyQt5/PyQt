# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt5 import  QtGui, QtWidgets, QtCore, QtWinExtras
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Ui_动态控件 import Ui_Dialog


class Dialog(QDialog, Ui_Dialog):

    def __init__(self, parent=None):

        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.dynamic1()
        self.dynamic2()
  
#    法一
    def dynamic1(self):
        for i in range(5):
            self.pushButton = QtWidgets.QPushButton(self)
            self.pushButton.setText("pushButton%d"%i)
            self.pushButton.setObjectName("pushButton%d"%i)
            self.verticalLayout.addWidget(self.pushButton)
            self.pushButton.clicked.connect(self.pr)
#    法二
    def dynamic2(self):
        for i in range(4):
            txt="""
self.pushButton_{i} = QtWidgets.QPushButton(self);
self.pushButton_{i}.setText("pushButton{i}");
self.pushButton_{i}.setObjectName("pushButton{i}");
self.verticalLayout.addWidget(self.pushButton_{i});
self.pushButton_{i}.clicked.connect(self.pr)
                """.format(i=i)
            exec(txt)
        #只能法二可用的方式
        self.pushButton_1.clicked.connect(self.pr2)
        self.pushButton_2.clicked.connect(self.pr2)
        self.pushButton_3.clicked.connect(self.pr2)

    def pr(self):
        '''法一和法二都可用的调用
        if self.sender().objectName=='XXX':
            self.pr2()
        '''
        print(self.sender().text())
        print(self.sender().objectName())
        print(self.pushButton.text())
        
    def pr2(self):
        print(2)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Dialog()
    ui.show()
    sys.exit(app.exec_())
