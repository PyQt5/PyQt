# -*- coding: utf-8 -*-

"""
Module implementing Form.
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

from PyQt5.QtWidgets import QWidget
try:
    from Ui_PluginPage1 import Ui_Form
except:
    from Plugins.page1.Ui_PluginPage1 import Ui_Form
# Start-Of-Header
name = "Jedi Code Completion Plug-in"
author = "Detlev Offenbach <detlev@die-offenbachs.de>"
autoactivate = True
deactivateable = True
version = "2.3.1"
className = "Form"
packageName = "CompletionJedi"
shortDescription = "Provide completions and calltips using Jedi"
longDescription = (
    """This plug-in provides code completions and calltips"""
    """ using the Jedi package."""
)
needsRestart = False
pyqtApi = 2
python2Compatible = True
# End-Of-Header
Testdata = 2
class Form(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Form, self).__init__(parent)
        self.setupUi(self)
        
    @pyqtSlot()
    def on_pushButton_clicked(self):

        print(Testdata)
        pass        
    @pyqtSlot()
    def on_pushButton_2_clicked(self):

        print(className)
        pass        
    @pyqtSlot()
    def on_pushButton_3_clicked(self):

        print(className)
        pass        

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
    
    ui = Form()

    ui.show()
    sys.exit(app.exec_())        
