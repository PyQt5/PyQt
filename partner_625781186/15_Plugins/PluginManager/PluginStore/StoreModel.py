#!/usr/bin/env python
"""
tableview的模型.
"""
from PyQt5 import  QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

PluginFileCol = 0
h1 = 1
h2 = 2
MTime = 3
CTime = 4
AutoStartCol  = 5

class FileModel(QFileSystemModel):
    """
    继承QFileSystemModel.
    """
    RE_UN_LoadSignal = pyqtSignal(object)
    AutoStartSignal  = pyqtSignal(object)
    
    def __init__(self , manager=None , *a, **kw):
        super(FileModel,self).__init__(*a,**kw )
        self.manager = manager
   
    def columnCount(self, index):
        """
        添加了两列
        """
        return 6
        
    def headerData(self, section, Orientation, role=Qt.DisplayRole):
        if Orientation==1:
            if   section == PluginFileCol:
                return "文件名"                 
#            elif section == h1:
#                return "Si"            
#            elif section == h2:
#                return "Ty"            
            elif section == MTime:
                return "修改时间"            
            elif section == CTime:
                return "创建时间"
            elif section == AutoStartCol:
                return "允许自启动"

        return super(FileModel,self).headerData(section, Orientation, role)
    
# ===== 如何让model/view界面出现复选框 =====
    def flags(self, index):
        """
        flag描述了view中数据项的状态信息
        """
        column = index.column()
        
        if  column==PluginFileCol:
            
        # 首先获取超类的flags返回值
            flag = super(FileModel, self).flags(index)

        # 或运算，将ItemIsEditable（可编辑）标志叠加上去
            return flag | Qt.ItemIsEnabled   \
                        | Qt.ItemIsUserCheckable\
                        | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled \
                 | Qt.ItemIsSelectable\
                 | Qt.ItemIsUserCheckable
                 
    def data(self,  index , role = Qt.DisplayRole):
        """
        根据值来显示界面信息.
        """
        if not index.isValid() :
            # 亦或者当前的索引值不在合理范围，即小于等于0，超出总行数
            return QVariant()  # 返回一个QVariant，相当与空条目
            
        column = index.column()
        # 复选框角色
        if role == Qt.CheckStateRole: 

            if column == PluginFileCol:
                mod = index.data()[:-3]
                return (Qt.Checked 
                    if self.manager.pluginsInfo["StartModule"][mod]["active"]
                    else Qt.Unchecked)
            elif column == AutoStartCol:
                
                mod = self.index(index.row(), PluginFileCol,
                                self.manager.index).data()[:-3]
             
                return (Qt.Checked 
                    if self.manager.jsonPlugin[mod]["Allow"]
                    else Qt.Unchecked)
        # 文本角色
        if role == Qt.DisplayRole:
            if  column == CTime:
                mod = self.index(index.row(), PluginFileCol,
                                self.manager.index).data()[:-3]    
                return self.manager.jsonPlugin[mod]["CreateTime"]
            elif column == AutoStartCol:
                mod = self.index(index.row(), PluginFileCol,
                                self.manager.index).data()[:-3]    
                return str(self.manager.jsonPlugin[mod]["Allow"] )
        return super(FileModel,self).data(index , role)
        
    def setData(self, index, value, role = Qt.DisplayRole):
        """
        数据驱动界面 , 发射信号修改数据即可.
        """
        if not index.isValid() :
            # 亦或者当前的索引值不在合理范围，即小于等于0，超出总行数
            return QVariant() 

        if role == Qt.CheckStateRole:
            mod = self.index(index.row(), PluginFileCol,
                            self.manager.index).data()[:-3]  
                            
            if   index.column() == PluginFileCol: 
                self.RE_UN_LoadSignal.emit((mod, index))
            elif index.column() == AutoStartCol: 
                self.AutoStartSignal.emit(mod)
                
        return super(FileModel,self).setData(index , value, role)         

# ===== 如何让model/view界面出现复选框 =====
