# -*- coding: utf-8 -*-

"""
主函数.

description: pyqt5悬浮下拉菜单

Created on 2018年7月7日

Author: 人间白头

email: 625781186@qq.com
"""

import sys 

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from U_FuncWidget.Menu import *
from Ui_Main import Ui_MainWindow

from Tools.CommonHelper import CommonHelper #读取CSS用
from Tools.qmf_showError import w_showERROR #弹窗报错


class MainWindow(Ui_MainWindow, QMainWindow):
    """
    主窗口.
    """

    def __init__(self, parent=None):
        """
        
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        
#        用于存储界面是否需要删除,
#        目前只支持9个菜单按钮。
        self.Wid_Obj={
        "b1":{}, "b2":{}, "b3":{}, "b4":{},  "b5":{}, 
        "b6":{}, "b7":{}, "b8":{}, "b9":{}, 
        }
        
        self.__initUI()
        
    def __initUI(self):
        '''
        一些无法在基础元素累中初始化的参数。
        '''
        
        # 有用判断最长的label的长度
        label_width = 0

        self.label_list = []
        
        # 从上部分窗体的子对象中循环选取出self.WX
        for WX in self.topWidget.children():
            # 判断是不是WX窗体
            name = WX.objectName()[0] 
            if name =="W" and isinstance(WX, SingeleWidget):
                num  = WX.objectName()[1]
                # 从全局中取 LX类
                LX   = globals()["L%s"%num]
                del WX.m_menu
                WX.m_menu = LX(self)  
                
                label = WX.findChild(QLabel)
                self.label_list.append(label)

                # 判断文字最长的label
                if label_width < len(label.text()):
                    label_width = len(label.text())

        # 用空格填充label,  使其宽度统一
        for label in self.label_list:
            
            length = label_width - len(label.text())
            size = length
            text = label.text()
            
            if length%2:
                text = ' '+ text +' '
            text = ' '*size+ text +' '*size
            label.setText(text)
        
        self.readCSS(self)
        
        self.DEFAULT = {}
        self.animation = QPropertyAnimation(self.topWidget, b'maximumHeight' )
        self.toggleButton.clicked.connect(self.start_animation)
        
    def readCSS(self, obj):
        '''
        用于设置样式，SingeleWidget类中也需要用到。
        '''
        styleFile = './Tools/style.css'
        qssStyle = CommonHelper.readQss( styleFile )  
        obj.setStyleSheet( qssStyle )  

    def start_animation(self, checked):
        
        CurrentHeight = self.topWidget.height()
        if self.DEFAULT == {}:
            self.DEFAULT["len"] = CurrentHeight
        if CurrentHeight == 0:
            direction = QAbstractAnimation.Backward
            self.toggleButton.setText("↑")
        else:
            direction = QAbstractAnimation.Forward
            self.toggleButton.setText("↓")
        self.animation.setDirection(direction)
        self.animation.setDuration(150)
        self.animation.setStartValue(self.DEFAULT["len"])
        self.animation.setEndValue(0)
        self.animation.start()  
        
#    def enterEvent(self, e):
#        '''自定义标题栏需要重置光标。'''
#        self.setCursor(Qt.ArrowCursor)

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)

    ui = MainWindow()
    
#    import qdarkstyle
#    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())     
    
    ui.show()
    
    sys.exit(app.exec_())
