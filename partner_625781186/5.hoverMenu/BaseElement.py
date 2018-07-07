# -*- coding: utf-8 -*-
'''
description: 抽象类模块

Created on 2018年7月7日

email: 625781186@qq.com

'''
from PyQt5 import  QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import traceback, sip

class SingeleWidget(QWidget):
    '''
    菜单条的每个框。
    '''
    #1
    def __init__(self, parent=None):
        '''
        _hideFlag__Button：  0 表明没有显示弹窗；1表示显示了弹窗。
        '''
        super(SingeleWidget, self).__init__(parent)
        
        self._hideFlag__Button = 0
        self.m_menu = QWidget()
        self.setProperty("WID", "isTrue")
        self.setAttribute(Qt.WA_StyledBackground, True)
        print("W实例化")
#        self.setMaximumWidth(80)
    def _creatMenu(self, L_Name, parent):
        '''
        Main.py中被调用。把LX类实例化。
        '''
       # self.m_menu = L1(parent)
        print(L_Name, parent)
        self.m_menu = L_Name(parent)
        
    def enterEvent(self, e): 
        '''鼠标移入label后 ， _hideFlag__Button=1，表明显示了弹窗。'''         
        #设置菜单窗体的宽度
        self.m_menu.setMinimumWidth(self.width())
        self.m_menu.setMaximumWidth(self.width()) 
        
        #我靠！
        a0 = self.mapToGlobal( QPoint( self.parent().x() , self.height()) )
        
        self.m_menu.move(a0) 
        
        #设置table外容器的宽度
        if self.m_menu.tableWidget.rowCount()!=0:
            table = self.m_menu.tableWidget
            height = table.rowCount()*30
            table.parent().setMinimumHeight(height)
            table.parent().setMaximumHeight(height)  
#            table.setMinimumHeight(height)
#            table.setMaximumHeight(height)            
            self.m_menu.show() 

        #表明显示了弹窗      
        self._hideFlag__Button = 1        
        
    def leaveEvent(self, e):  
        '''
        离开时判断是否显示了窗体，80ms后发射到_jugement去检测。
        '''
        if self._hideFlag__Button==1: #显示了窗体
            QTimer.singleShot(80, self._jugement)

    def _jugement(self):
        '''
        离开上面窗体之后80ms, 1：进入旁边的菜单框；2：进入弹出的菜单。
        '''
        if self.m_menu._hideFlag__Menu!=1:
            self.m_menu.hide()
            self.m_menu.close()
            self._hideFlag__Button=0            
        else:
            pass


    
#========================================================
class BaseMenuWidget(QWidget):
    #2
    '''
    下拉菜单的基类。 被LX继承，父类在18L 实现。
    '''
    def __init__(self, parent=None):
        '''
        _hideFlag__Menu: 0时隐藏，1时显示；
        '''

        super(BaseMenuWidget, self).__init__(parent)
        #无边框，隐藏任务栏；
        self.setWindowFlags( Qt.FramelessWindowHint|Qt.Tool|Qt.Widget)   
        self.setupUi(self)
        self._hideFlag__Menu = 0
        print("L实例化") 
      
    def enterEvent(self, e):
        #表明进入了弹窗
        self._hideFlag__Menu=1
        
    def leaveEvent(self, e):
        self._hideFlag__Menu=0  
        self.hide()  
        for i in self.children():
            if isinstance(i, BaseTable):#判断对象是否是tablewiget, 是则隐藏选中item颜色
                i.clearSelection()

    def _showSomething(self, **kwgs):
        MW = self.parent()
        
        if MW.objectName()=="MainWindow":

                try:
#                    MW.Buttom_Vbox.setParent(None)#这是个严重的问题，如果用这个函数会造成78L无法成功
                    _parent=MW.Buttom_Vbox.parent()#获取下面窗体对象的指针
                    
                    # ! 目前的安排是离开当前页则释放对象 , 要求页面数据不需要保留才可以。
                    for obj in _parent.children():
                        print(obj)
                        sip.delete(obj)
                    
                    MW.Buttom_Vbox = QtWidgets.QVBoxLayout(_parent)
                    MW.Buttom_Vbox.setContentsMargins(0, 0, 0, 0)
                    MW.Buttom_Vbox.setSpacing(0)
                    MW.Buttom_Vbox.setObjectName("Buttom_Vbox")
         
                except:
                    showERROR()
            
#                elif msg==QMessageBox.No:
#                    pass
#        else:
#            showERROR()
    def _deleteSomething(self):
        pass
#====================================================
class BaseButton(QPushButton):
    #1
    '''
    主菜单的按钮的样式。
    '''
    def __init__(self, parent=None):

        super(BaseButton, self).__init__(parent)
        
#        self.setMinimumWidth(50)
#        self.setMaximumWidth(80)     

        self.setMaximumWidth(80)
        self.setMinimumHeight(self.width())#保证是个正方形
        self.setFocusPolicy(Qt.NoFocus)#无焦点，防止背景卡色
        self.setFlat(True)#无凸起阴影

        self.clicked.connect(self._todo)
        
        self.png = QLabel(self)
        print("B实例化")

    def _todo(self, *args, **kwgs):
        '''
        每个按钮要重新实现的功能函数。
        '''
        pass
    
    def _createLabel(self, path):
        '''
        path：主菜单图标的路径。
        '''
        self.png.resize(self.size())
        self.png_pixmap = QPixmap(path)
        self.png.setPixmap(self.png_pixmap)  
        self.png.setScaledContents(True)  
        pass
    def resizeEvent(self, e):
        self.setMinimumHeight(self.width()) 
        self.png.resize(self.size())
        
#==================================================        
class BaseTable(QTableWidget):
    #3
    '''
    下拉菜单中Table的样式。
    '''
    def __init__(self, parent=None):
        super(BaseTable, self).__init__(parent)

        self.horizontalHeader().setSectionResizeMode(3)#列宽设置

        self.horizontalHeader().setStretchLastSection(True); #充满列宽    
        
        self.verticalHeader().setSectionResizeMode(1)#行高设置          
        
        self.verticalHeader().setStretchLastSection(True); #充满行高  

        self.setEditTriggers(QAbstractItemView.NoEditTriggers);  #只读

        self.itemClicked.connect(self.parent()._showSomething)#Go 66L;
        
        #关闭滑动条
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        print("T实例化") 
        
def showERROR():    
    errmsg = traceback.format_exc()      
    QMessageBox.warning(QWidget(), '请确认', errmsg,
                        QMessageBox.Ok)
