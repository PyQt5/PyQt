#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年1月29日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: NormalStyle
@description: 
"""

import sys

try:
    from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QApplication
except ImportError:
    from PySide2.QtWidgets import QWidget, QHBoxLayout, QPushButton, QApplication

StyleSheet = """
/*这里是通用设置，所有按钮都有效，不过后面的可以覆盖这个*/
QPushButton {
    border: none; /*去掉边框*/
}

/*
QPushButton#xxx
或者
#xx
都表示通过设置的objectName来指定
*/
QPushButton#RedButton {
    background-color: #f44336; /*背景颜色*/
}
#RedButton:hover {
    background-color: #e57373; /*鼠标悬停时背景颜色*/
}
/*注意pressed一定要放在hover的后面，否则没有效果*/
#RedButton:pressed {
    background-color: #ffcdd2; /*鼠标按下不放时背景颜色*/
}

#GreenButton {
    background-color: #4caf50;
    border-radius: 5px; /*圆角*/
}
#GreenButton:hover {
    background-color: #81c784;
}
#GreenButton:pressed {
    background-color: #c8e6c9;
}

#BlueButton {
    background-color: #2196f3;
    /*限制最小最大尺寸*/
    min-width: 96px;
    max-width: 96px;
    min-height: 96px;
    max-height: 96px;
    border-radius: 48px; /*圆形*/
}
#BlueButton:hover {
    background-color: #64b5f6;
}
#BlueButton:pressed {
    background-color: #bbdefb;
}

#OrangeButton {
    max-height: 48px;
    border-top-right-radius: 20px; /*右上角圆角*/
    border-bottom-left-radius: 20px; /*左下角圆角*/
    background-color: #ff9800;
}
#OrangeButton:hover {
    background-color: #ffb74d;
}
#OrangeButton:pressed {
    background-color: #ffe0b2;
}

/*根据文字内容来区分按钮,同理还可以根据其它属性来区分*/
QPushButton[text="purple button"] {
    color: white; /*文字颜色*/
    background-color: #9c27b0;
}
"""


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.addWidget(QPushButton("red button", self,
                                     objectName="RedButton", minimumHeight=48))
        layout.addWidget(QPushButton("green button", self,
                                     objectName="GreenButton", minimumHeight=48))
        layout.addWidget(QPushButton("blue button", self,
                                     objectName="BlueButton", minimumHeight=48))
        layout.addWidget(QPushButton("orange button", self,
                                     objectName="OrangeButton", minimumHeight=48))
        layout.addWidget(QPushButton("purple button", self,
                                     objectName="PurpleButton", minimumHeight=48))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    w = Window()
    w.show()
    sys.exit(app.exec_())
