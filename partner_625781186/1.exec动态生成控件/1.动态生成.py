
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@resource:none
@description: 1. exec()执行动态生成控件 //关闭程序时把model类型保存到ini文件中,打开时生成model对象.
@Created on 2018年3月17日
@email: 625781186@qq.com
'''

from PyQt5 import  QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtSql import *
import re


from Ui_getModel import Ui_Dialog


class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.setting=QSettings('./setting.ini', QSettings.IniFormat)
        self.getModel()
        self.tableView.setModel(self.qmodel)
        
        print('1:', self.tableView.model())
    def closeEvent(self, e):
        text=re.split('\.| ', str(self.tableView.model()))
        if text != ['None']:
            i=[i for i, x in enumerate(text) if x.find('Model')!=-1]
#            print(text[i[-1]])
            self.setting.setValue("Model/model",text[i[-1]]+'()');#设置key和value，也就是参数和值  
    def getModel(self):
        if(self.setting.contains("Model/model")):   #此节点是否存在该数据
            model = self.setting.value("Model/model")
            exec('''self.qmodel=%s'''%(model))#python exec()执行字符串命令
            print('2:', self.qmodel)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    ui = Dialog()

    ui.show()
    sys.exit(app.exec_())