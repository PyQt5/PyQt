# -*- coding: utf-8 -*-
'''
description: 抽象类模块

Created on 2018年7月7日

Author: 人间白头

email: 625781186@qq.com

'''
import  sip ,  functools

from PyQt5 import  QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Tools.qmf_showError import f_showERROR, w_showERROR
from Tools.CommonHelper import CommonHelper


SHOWMENU  = {"yes":True , "no":False , "setShow":True , "setHide":False }
ENTERMENU = {"yes":True , "no":False }

class SingeleWidget(QWidget):
    '''
    菜单栏的每个框。
    '''
    #1
    
    Button_hideFlag = SHOWMENU["setHide"]

    def __init__(self, parent=None):
        '''
        Button_hideFlag：  0 表明没有显示弹窗；1表示显示了弹窗。
        '''
        super(SingeleWidget, self).__init__(parent)
        
        # 很重要 ,  否则样式背景无效!
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        # 这个m_menu没有用， 有用的是main.py中生成的m_menu
        self.m_menu = QWidget()
        
        # 用来测试qss的 ,  可以注释掉
        self.setProperty("WID", "isTrue")
        
    def enterEvent(self, e): 

        #设置菜单窗体的宽度
        self.m_menu.setMinimumWidth(self.width())
        self.m_menu.setMaximumWidth(self.width()) 
        
        #我靠！ 把菜单窗体对齐到按钮框 
        menu_Pos = self.mapToGlobal(
                        QPoint( self.parent().x() , 
                                self.parent().height() ) 
                        )
        
        self.m_menu.move(menu_Pos) 
        
        self.m_menu.show()

        #表明显示了弹窗      
        self.Button_hideFlag = SHOWMENU["setShow"]
        
    def leaveEvent(self, e):  
        '''
        离开时判断是否显示了窗体，80ms后发射到_jugement去检测。
        '''
        if self.Button_hideFlag is SHOWMENU["yes"]: #显示了窗体
            QTimer.singleShot(80, self._jugement)

    def _jugement(self):
        '''
        离开上面窗体之后80ms, 1：进入旁边的菜单框；2：进入弹出的菜单。
        '''
        if self.m_menu.Menu_hideFlag is ENTERMENU["no"]:
            self.m_menu.hide()
            self.m_menu.close()
            self.Button_hideFlag = SHOWMENU["setHide"]

#==================================================
class BaseMenuWidget(QTableWidget):
    #2
    '''
    下拉菜单。
    '''
    m_currentRow = None
    m_currentCol = None
    
    Menu_hideFlag = ENTERMENU["no"]
    
    def __init__(self, parent=None):
        '''
        Menu_hideFlag: 0时隐藏，1时显示；
        '''

        super(BaseMenuWidget, self).__init__(parent)

        self.__initUI()
        
    def __initUI(self):
        
        #无边框，隐藏任务栏；
        self.setWindowFlags( Qt.FramelessWindowHint|Qt.Tool|Qt.Widget) 
        #列宽设置
        self.horizontalHeader().setSectionResizeMode(3)
        #充满列宽
        self.horizontalHeader().setStretchLastSection(True) 
        #行高模式
        self.verticalHeader().setSectionResizeMode(1) 
        #充满行高  
        self.verticalHeader().setStretchLastSection(True) 
        #只读
        self.setEditTriggers(QAbstractItemView.NoEditTriggers) 
        
        # 隐藏表头
        self.horizontalHeader().setVisible(False);
        self.verticalHeader().setVisible(False);        
        
        # 关闭滑动条
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        self.setColumnCount(1);
        self._setHeight()
        
        # 不知道为啥main.py中的下拉菜单样式要重新赋予一次
        self.parent().readCSS(self)
    
    def _setHeight(self):
            height = self.rowCount()*40
            self.setMinimumHeight(height)
            self.setMaximumHeight(height)        

    def enterEvent(self, e):
        #表明进入了弹窗
        self.Menu_hideFlag = ENTERMENU["yes"]
        
    def leaveEvent(self, e):
        #表名离开了弹窗
        self.Menu_hideFlag = ENTERMENU["no"]
        self.hide() 
        
        #取消点击的按钮
        if self.m_currentRow is not None:
            self.clearSelection()        
            self.cellWidget(self.m_currentRow, 
                            self.m_currentCol).setCheckable(False)
                        
    def _addAction(self, text, MyWidget=None, func=None,  *args, **kwags):
        '''
        obj : QPushButton对象；
        text：obj的字；
        func：obj点击链接的信号；
        MyWidget:想要显示的窗体对象；
        '''
        self.insertRow(self.rowCount())
        self._setHeight()
        row = self.rowCount()-1
        col = self.columnCount()-1  
        
        obj = QPushButton(text)
        obj.setProperty("M_Action", "isTrue")
        obj.setFlat(True)        
        obj.setCheckable(True);
        obj.setAutoExclusive(True);
        
        #老子真聪明，哈哈
        #按钮默认连接changeTab函数
        if func == None :
            func = self.changeTab 
        obj.clicked.connect(lambda: setattr(self , "m_currentRow" , row))
        obj.clicked.connect(lambda: setattr(self , "m_currentCol" , col))
        
        obj.clicked.connect(functools.partial(
                                        func, 
                                        text, 
                                        MyWidget, 
                                        *args, 
                                        **kwags)
                            )
            
        self.setCellWidget(row, col , obj);
        
    def _findParent(self, currentObj):
        '''
        递归找父窗口。
        '''

        if currentObj.parent().objectName()=="MainWindow":
            return currentObj.parent()
            
        #这里有返回值，返回倒数第二次的 
        return self._findParent(currentObj.parent())
        
    def changeTab(self, text, MyWidget, *args, **kwags):
        #返回的MainWindow
        mw = self._findParent(self) 
        
        #save:是否保留窗体；id：在mw.Wid_Obj 二级字典的键值；
        if "save" in kwags and "id" in kwags:
            save, id = kwags["save"],  kwags["id"]
            #B1类-b1; B2类-b2;
            _key = "b"+ self.__class__.__name__[-1]
#            print(_key)
            childrens = mw.bottomWidget.children()[1:]
            if childrens!=[]:
                for obj in childrens:
                    # 隐藏所有对象 
                    obj.setVisible(False)
                    # 如果没有不可删除的属性，就删掉
                    if  not hasattr(obj, "SAVE"):
                        sip.delete(obj)
                        del obj
                    
            #如果为"s", 即对象不删除，保存到字典中；
            if save=="s":
                if MyWidget is not None:
                    #第一次点击到时候判断是否存在二级字典中；
                    if id in mw.Wid_Obj[_key].keys():
                        print("存在wid_obj:", mw.Wid_Obj[_key][id])
                        print("EXIT?:",mw.Wid_Obj[_key][id].SAVE )
                        mw.Wid_Obj[_key][id].setVisible(True)
                    else:
                    #不存在则创建;
                        print("saving..")
                        obj_Widget = MyWidget()
                        #动态添加不删除标志
                        obj_Widget.SAVE = True
                        #存对象
                        mw.Wid_Obj[_key][id] = obj_Widget
                        #加到布局
                        mw.Bottom_Vbox.addWidget(obj_Widget)
    
            elif save=="d":
                obj_Widget = MyWidget(mw)
                mw.Bottom_Vbox.addWidget(obj_Widget) 

        print(mw.Wid_Obj) 
        
#==================================================
class BaseButton(QPushButton):
    #1
    '''
    菜单栏的按钮的样式。
    '''
    def __init__(self, parent=None):

        super(BaseButton, self).__init__(parent)
        
        self.setMinimumWidth(70)
        self.setMaximumWidth(88)     
        self.setMinimumHeight(self.width()) #保证是个正方形

        self.setFocusPolicy(Qt.NoFocus) #无焦点，防止背景卡色
        self.setFlat(True) #无凸起阴影

        self.clicked.connect(self._todo)
        
        self.png = QLabel(self)
        
    def _createLabel(self, path):
        '''
        path：主菜单图标的路径。
        '''
        self.png.resize(self.size())
        self.png_pixmap = QPixmap(path)
        self.png.setPixmap(self.png_pixmap)  
        self.png.setScaledContents(True)  
        pass        

    def _todo(self, *args, **kwgs):
        '''
        每个按钮要重新实现的功能函数。
        '''
        pass
        
    def resizeEvent(self, e):
        self.setMinimumHeight(self.width()) 
        self.png.resize(self.size())
        
