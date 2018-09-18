# -*- coding: utf-8 -*-

"""
Module implementing PluginStore.
"""

"""
Created on 2018-09-18 <br>
description: $description$ <br>
author: 625781186@qq.com <br>
site: https://github.com/625781186 <br>
更多经典例子:https://github.com/892768447/PyQt <br>
课件: https://github.com/625781186/WoHowLearn_PyQt5 <br>
视频教程: https://space.bilibili.com/1863103/#/ <br>
"""

from PyQt5 import  QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtWidgets import QDialog
try:
    from Ui_PluginStore import Ui_Dialog
except:
    from .Ui_PluginStore import Ui_Dialog
    
from Tools.pmf_myjson import *

class PluginStore(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, header , existPlugin , parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(PluginStore, self).__init__(parent)
        self.setupUi(self)
        
        self.existPlugin = existPlugin
        
        self.tableWidget.setColumnCount(len(header))
        self.tableWidget.setHorizontalHeaderLabels(header)

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers); #只读
                
        self.tableWidget.horizontalHeader().setSectionResizeMode(3)#列宽设置
        
        self.tableWidget.horizontalHeader().setStretchLastSection(True); #充满列宽    
        
        self.tableWidget.verticalHeader().setSectionResizeMode(2)#行高设置          
        
#        self.tableWidget.verticalHeader().setStretchLastSection(True); #充满行高  

        for  row, key in enumerate(existPlugin):
            
            self.tableWidget.insertRow(row)
            for col, head in enumerate(header):
                if   col==0:
                    # 设置插件名称
                    self.tableWidget.setItem(row , col ,QTableWidgetItem(key))
                elif col==1:
                    item = QTableWidgetItem(head)
                    # 读取json中 "Allow" 设置勾选
                    item.setCheckState(Qt.Checked 
                                        if existPlugin[key][head]==True 
                                        else Qt.Unchecked)
                                        
                    self.tableWidget.setItem(row , col ,item)
                else:
                    self.tableWidget.setItem(row , col ,
                        QTableWidgetItem(existPlugin[key][head]))
                        
        self.tableWidget.cellChanged.connect(self.handleItemClicked) 
        
        self.tableWidget.setMouseTracking(True); 
        self.tableWidget.itemEntered.connect(lambda item : item.setToolTip(item.text()) 
                                            if item.column()!=1 else 0)          
        
    def handleItemClicked(self, row ,col):
        print(row ,col)
        if col==1:
            item = self.tableWidget.item(row, 0 ) 
            key =  item.text() 
            item = self.tableWidget.item(row, 1 ) 
            print(item.text())
            print(self.existPlugin[key]["Allow"])
            # 转变为打勾 , 即注册插件
            if item.checkState() == Qt.Checked:
                
                QMessageBox.information(self, "注册插件", "注册成功.")
                mfunc_writeJson([key, "Allow"], True)
                
            # 取消注册插件
            elif item.checkState() == Qt.Unchecked:
                QMessageBox.information(self, "取消插件", "取消成功.")
                mfunc_writeJson([key, "Allow"], False)
    
    def delRow(self):
        #TODO:
        pass
        
    
