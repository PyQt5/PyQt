# -*- coding: utf-8 -*-
'''
description: 要增加菜单栏时，在这里添加。<br>

Created on 2018年7月7日

email: 625781186@qq.com

BX: 主菜单按钮；<br>
LX：子菜单按钮-继承了UI类和 隐藏基类；<br>
'''

from BaseElement import *

from UStoreData1 import Ui_L1
from UCompetitiveProduct2 import Ui_L2 
from UMarketAnalysis3 import Ui_L3
from UThroughTrain4 import Ui_L4

#============================================= 店铺数据 =======================================
class B1( BaseButton):
    def __init__(self, parent=None):
        super(B1, self).__init__(parent)
        self._createLabel(":/static/store_data.png")        
    def _todo(self, *args, **kwgs):
        super(B1, self)._todo()

class L1( Ui_L1.Ui_Form, BaseMenuWidget):
    def __init__(self, parent=None):
        super(L1, self).__init__(parent)
    def _showSomething(self, item):
        super(L1, self)._showSomething()
        MW = self.parent()#是MainWindow
        if item.text()=="语音数据":
            print(1) #功能未实现

#============================================= 竞品分析 =======================================
class B2(BaseButton):
    def __init__(self, parent=None):
        super(B2, self).__init__(parent)
        self._createLabel(":/static/competitiveProductAnalysis.png")         
    def _todo(self, *args, **kwgs):
        super(B2, self)._todo()
        
class L2(Ui_L2.Ui_Form,  BaseMenuWidget):
    def __init__(self, parent=None):
        super(L2, self).__init__(parent)
    def _showSomething(self, item):
        super(L2, self)._showSomething()
        
        MW = self.parent()#是MainWindow
        if item.text()=="评价分析":
            print(1) #功能未实现
        elif item.text()=="SKU分析":

            from UCompetitiveProduct2 import SKU_Widget
            #切换窗体
            self.sku_Widget = SKU_Widget.SKU_Form(MW.Buttom_Vbox.parent())

            self.parent().Buttom_Vbox.addWidget(self.sku_Widget)

            
        elif item.text()=="流量分析":
            print(3) #功能未实现


#============================================= 市场分析 =======================================
class B3(BaseButton):
    def __init__(self, parent=None):
        super(B3, self).__init__(parent)
        self._createLabel(":/static/search.png")         
        
    def _todo(self, *args, **kwgs):
        super(B3, self)._todo()
        
class L3(Ui_L3.Ui_Form, BaseMenuWidget):
    def __init__(self, parent=None):
        super(L3, self).__init__(parent)
    def _showSomething(self, item):
        super(L3, self)._showSomething()
        MW = self.parent()#是MainWindow
        if item.text()=="类目趋势": 
            print(1)#功能未实现
        elif item.text()=="属性趋势":
            print(2)#功能未实现
        elif item.text()=="品牌分析":
            print(3)#功能未实现


#============================================= 直通车工具 =======================================
class B4(BaseButton):
    def __init__(self, parent=None):
        super(B4, self).__init__(parent)
        self._createLabel(":/static/throughTrain.png")         
    
    def _todo(self, *args, **kwgs):
        super(B4, self)._todo()
        
class L4(Ui_L4.Ui_Form,BaseMenuWidget):
    def __init__(self, parent=None):
        super(L4, self).__init__(parent)
    def _showSomething(self, item):
        super(L4, self)._showSomething()
        MW = self.parent()#是MainWindow
        
        if item.text()=="地域分析":
            from UThroughTrain4 import GeographicAnalysis_Widget         
            self.geo_Widget = GeographicAnalysis_Widget.GeographicAnalysis_Form(MW.Buttom_Vbox.parent())
            #切换窗体
            MW.Buttom_Vbox.addWidget(self.geo_Widget)
            
            self.geo_Widget.show()
        elif item.text()=="实时数据":
            print(2)#功能未实现
        elif item.text()=="标签工具":
            print(3)


#============================================= 智钻工具 =======================================
