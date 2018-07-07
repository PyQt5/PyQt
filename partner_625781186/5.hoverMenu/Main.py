# -*- coding: utf-8 -*-

"""
主函数.

description: pyqt5悬浮下拉菜单

Created on 2018年7月7日

email: 625781186@qq.com
"""


from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Menu import *
from Ui_Main import Ui_MainWindow
#读取CSS用
from CommonHelper import CommonHelper

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.showMaximized()
        # W1->TestWidget 生成，然后B->，然后L->tablewidget
        for i in range(1,10):
            try:
                txt='''self.W{x}._creatMenu(L{x}, self);
'''.format(x=i)

                exec(txt)
            except:
                continue
                
    def enterEvent(self, e):
        '''自定义标题栏需要重置光标。'''
        self.setCursor(Qt.ArrowCursor)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    ui = MainWindow()
    styleFile = './style.css'
    qssStyle = CommonHelper.readQss( styleFile )  
    ui.setStyleSheet( qssStyle )     
    ui.show()   

    sys.exit(app.exec_())
