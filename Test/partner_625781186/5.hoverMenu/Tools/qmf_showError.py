
"""
Created on 2018-09-09

description: 错误提示窗模块

author: 625781186@qq.com

site: https://github.com/625781186
"""


from PyQt5 import  QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import traceback

def w_showERROR(widget=None): 
    
    errmsg = traceback.format_exc()      
#    QMessageBox.warning(QWidget(), '请确认', errmsg,
#                        QMessageBox.Ok)
    msg  = QErrorMessage(widget)
    msg.setModal(True)
    msg.showMessage(errmsg)
    
def f_showERROR(func, *args, **kwargs):
    def _doWhat(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            import sys
            app =QApplication(sys.argv)            
            errmsg = traceback.format_exc()    
            print(errmsg)
            gitMsg=QMessageBox()

            gitMsg.setWindowTitle("错误")	

            gitMsg.setText(errmsg)
            gitMsg.setDetailedText(errmsg)
            gitMsg.setStandardButtons(QMessageBox.Ok)
            gitMsg.buttons()[-1].click()
                   
            gitMsg.exec_()	
            
            sys.exit(app.exec_())  
            return
            
    return _doWhat    
