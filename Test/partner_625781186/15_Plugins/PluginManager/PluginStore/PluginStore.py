# -*- coding: utf-8 -*-

"""
插件仓库管理界面.
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
    def __init__(self, manager,  parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(PluginStore, self).__init__(parent)
        self.setupUi(self)
        
        self.manager = manager
        self.__mw    = parent
        self.model = manager.model
        self.index = manager.index
        
        header     = manager.header
        jsonPlugin = manager.jsonPlugin
        activeInfo = manager.pluginsInfo

        self.__initUI(header , jsonPlugin , activeInfo)
        
    def __initUI(self , header , jsonPlugin , activeInfo):
        #加载或者卸载插件
        self.model.RE_UN_LoadSignal.connect(self.re_un_load)
        self.model.AutoStartSignal.connect(self.allow_un_start)
        
        # == 设置 tableView 一些参数 ==
        self.tableView.setModel(self.model)
        self.tableView.setRootIndex(self.index);
        #只读
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers); 
        #充满列宽    
        self.tableView.horizontalHeader().setStretchLastSection(True); 
        for col in [0, 3, 4, 5]:
            self.tableView.resizeColumnToContents(col)
        #最小化两列
        self.tableView.horizontalHeader().resizeSection(1, 0)
        self.tableView.horizontalHeader().resizeSection(2, 0)
        
        #列宽设置
        # self.tableView.horizontalHeader().setSectionResizeMode(2)
        #行高设置      
        self.tableView.verticalHeader().setSectionResizeMode(2)    
          
        #进入item时候显示全名
        self.tableView.setMouseTracking(True); 
        self.tableView.entered.connect(lambda index : 
                                            self.setToolTip(index.data()) 
                                            if index.column()!=1 else 0)              
        #右键请求 弹出菜单
        self.tableView.customContextMenuRequested.connect(
                                            self.myListWidgetContext)
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu) 
        
    def myListWidgetContext(self):
        popMenu = QMenu()

        popMenu.addAction(u'重载模块',lambda:self.re_un_load(1))
        popMenu.addAction(u'卸载模块',lambda:self.re_un_load(2))
#        popMenu.addAction(u'替换对象',lambda:self.re_un_load(3))
#        popMenu.addAction(u'删除文件',lambda:self.del_Item(1))

        popMenu.exec_(QCursor.pos())#鼠标位置
        
    def re_un_load(self, type=1):
        """
        加载/重载和卸载插件.
        """
        # 复选框重载和卸载
        if isinstance(type , tuple):
            mod = type[0]
            index = type[1]
            # == 没什么用 为了刷新界面 == #
            self.__mw.activateWindow()
            self.manager.dia.tableView.activateWindow()                
            self.manager.dia.tableView.setCurrentIndex(index)
            # == 没什么用 为了刷新界面 == #
            
            if self.manager.pluginsInfo["StartModule"][mod]["active"]:
                msg = QMessageBox.information(self, 
                                            "确认", "即将卸载插件.", 
                                            QMessageBox.Yes|
                                            QMessageBox.No, QMessageBox.Yes)
                if msg==QMessageBox.Yes:
                    self.manager.unload(mod)
            else:
                self.manager.reload(mod) 

        # 右键菜单重载和卸载 , 默认的是选行的第0列
        else:
            for index in self.tableView.selectionModel().selectedRows():     
                mod = index.data()[:-3]
                
                if   type==1:
                    self.manager.reload(mod)
                elif type==2:
                    self.manager.unload(mod)

    def del_Item(self):
        #TODO:
        pass
        
    def allow_un_start(self, mod):
        """
        允许/禁止 插件的自启动.
        """
        if self.manager.jsonPlugin[mod]["Allow"]:
            msg = QMessageBox.information(self, 
                                        "确认", "即将禁止插件自启.", 
                                        QMessageBox.Yes|
                                        QMessageBox.No, QMessageBox.Yes)

            # 取消打勾 , 即取消自启插件
            if msg==QMessageBox.Yes:
                mfunc_AKrCVJson([mod, "Allow"], False)
                self.manager.jsonPlugin[mod]["Allow"] = False
        else:
            # 转变为打勾 , 即自启插件
            QMessageBox.information(self, "允许", "已允许插件自启.")
            mfunc_AKrCVJson([mod, "Allow"], True)
            self.manager.jsonPlugin[mod]["Allow"] = True

