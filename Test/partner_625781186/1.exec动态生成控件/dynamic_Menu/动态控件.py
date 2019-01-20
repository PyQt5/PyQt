# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt5 import  QtGui, QtWidgets, QtCore, QtWinExtras
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from functools import partial
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
            self.pushButton.setContextMenuPolicy(Qt.CustomContextMenu)
            self.pushButton.customContextMenuRequested.connect(lambda:self.helpMenu(i))#右键请求,传入i实际上一直是4            
            self.pushButton.clicked.connect(self.pr)
            
#    法二
    def dynamic2(self):
        for i in range(5, 8):
            txt="""
self.pushButton_{i} = QtWidgets.QPushButton(self);
self.pushButton_{i}.setText("pushButton{i}");
self.pushButton_{i}.setObjectName("pushButton{i}");
self.verticalLayout.addWidget(self.pushButton_{i});

self.pushButton_{i}.setContextMenuPolicy(Qt.CustomContextMenu)
self.pushButton_{i}.customContextMenuRequested.connect(partial(self.helpMenu,i))#右键请求,用lambda会报错,partial需要import

self.pushButton_{i}.clicked.connect(self.pr)
                """.format(i=i)
            exec(txt)
        #只能法二可用的方式
        self.pushButton_5.clicked.connect(self.pr2)
        self.pushButton_6.clicked.connect(self.pr2)
        self.pushButton_7.clicked.connect(self.pr2)            
            

    def helpMenu(self, *type):       
        '''帮助按钮的右键菜单'''
        print(type)
        popMenu =QMenu()
        
        if type[0]==5 or self.sender().text()== 'pushButton0':
            popMenu.addAction(u'关于',self.pr)
            popMenu.addSeparator()
        
        elif type[0]==6 or self.sender().text()== 'pushButton1':
            popMenu.addAction(u'清理图片',self.pr)
            popMenu.addSeparator()
        
        elif type[0]==7 or self.sender().text()== 'pushButton2':
            gitMenu=QMenu('同步到Git', popMenu)
            
            self.pushAction=QAction(u'上传', self, triggered=lambda:self.pr)
            gitMenu.addAction(self.pushAction)
            
            self.pullAction=QAction(u'下载', self, triggered=lambda:self.pr)
            gitMenu.addAction(self.pullAction)
            
            gitMenu.addSeparator()
            gitMenu.addAction(u'配置仓库',lambda:self.pr)

            popMenu.addAction(gitMenu.menuAction())#!!
        popMenu.exec_(QCursor.pos())#鼠标位置
            
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
