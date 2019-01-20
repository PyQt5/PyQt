
# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
from PyQt5 import  QtGui, QtWidgets, QtCore, QtQml
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtQuickWidgets import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import QQuickView

from Ui_py_qml import Ui_MainWindow
import qml_rc

class Dialog(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super(Dialog, self).__init__(parent)
        self.setupUi(self)
#        self.mywidget() #法一

#        self.myview()#法二

        self.myengine()
        
#        self.pushButton.clicked.connect(self.pr)
        
    def mywidget(self):
        self.m_quickWidget=QQuickWidget();
        self.m_quickWidget.setResizeMode(QQuickWidget.SizeRootObjectToView) ;
        self.m_quickWidget.setSource(QUrl("py_mqltest.qml"));
        self.verticalLayout.addWidget(self.m_quickWidget)
    def myview(self):
        path = 'py_mqltest.qml'   # 加载的QML文件
        self.view = QQuickView()
        self.view.setSource(QUrl(path))
        self.container = QWidget.createWindowContainer(self.view);        
        self.verticalLayout.addWidget(self.container)  
        
    def myengine(self):    
        self.engine = QQmlApplicationEngine(QUrl("qrc:/py_mqltest.qml")) ;
        print(self.engine.rootObjects(),"==",self.engine.rootObjects())
        self.qmlWindow = self.engine.rootObjects()[0]

        self.container = QWidget.createWindowContainer(self.qmlWindow);
        self.verticalLayout.addWidget(self.container)

        self.verticalLayout.addWidget(QPushButton('pushButton0'))  
        self.verticalLayout.addWidget(QPushButton('pushButton2'))
  
    def pr(self):
        print("123")
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    # engine = QQmlApplicationEngine(QUrl("py_mqltest.qml")) ;
    # qmlWindow = engine.rootObjects()[0]
    # container = QWidget.createWindowContainer(qmlWindow);  
    # widget = QWidget();
    # grid = QGridLayout(widget);    
    # grid.addWidget(container,0,0);
    # widget.show();
    
    Dialog = Dialog()

    Dialog.show()

    sys.exit(app.exec_())
