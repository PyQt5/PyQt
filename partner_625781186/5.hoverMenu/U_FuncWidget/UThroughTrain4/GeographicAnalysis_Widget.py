# -*- coding: utf-8 -*-

"""
Module implementing GeographicAnalysis_Form.
"""

from PyQt5 import  QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .Ui_GeographicAnalysis_Widget import Ui_Form


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
        
        self.geographicAnalysis_table.horizontalHeader().setSectionResizeMode(1)#列宽设置

        self.geographicAnalysis_table.horizontalHeader().setStretchLastSection(True); #充满列宽    
        
        self.geographicAnalysis_table.verticalHeader().setSectionResizeMode(1)#行高设置          
        
        self.geographicAnalysis_table.verticalHeader().setStretchLastSection(True); #充满行高  

        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = GeographicAnalysis_Form()

    ui.show()
    sys.exit(app.exec_())
