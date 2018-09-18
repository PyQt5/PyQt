# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

"""
Created on 2018-09-16 <br>
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

from PyQt5.QtWidgets import QMainWindow

try:
    from Ui_main import Ui_MainWindow
except:
    from .Ui_main import Ui_MainWindow


from PluginManager.PluginManager import PluginManager

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pluginManager = PluginManager(self)  #初始化插件管理器
        
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))

#    自定义CSS样式
#    from BasePack.CommonHelper import CommonHelper
#    styleFile = 'BasePack/style.css'
#    qssStyle = CommonHelper.readQss( styleFile )  
#    framelessWindow.setStyleSheet( qssStyle )   

#    If you want to use this style, please pip install qdarkstyle.
#    import qdarkstyle
#    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    
    ui = MainWindow()

    ui.show()
    sys.exit(app.exec_())        
    
