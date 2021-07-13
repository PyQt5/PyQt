#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年5月15日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: QssQSlider
@description: 通过QSS美化QSlider
"""

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider

StyleSheet = """
QWidget {
    background: gray;
}

/*横向*/
QSlider:horizontal {
    min-height: 60px;
}
QSlider::groove:horizontal {
    height: 1px;
    background: white; 
}
QSlider::handle:horizontal {
    width: 30px;
    margin-top: -15px;
    margin-bottom: -15px;
    border-radius: 15px;
    background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.6 rgba(210, 210, 210, 255), stop:0.7 rgba(210, 210, 210, 100));
}
QSlider::handle:horizontal:hover {
    background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.6 rgba(255, 255, 255, 255), stop:0.7 rgba(255, 255, 255, 100));
}

/*竖向*/
QSlider:vertical {
    min-width: 60px;
}
QSlider::groove:vertical {
    width: 1px;
    background: white; 
}
QSlider::handle:vertical {
    height: 30px;
    margin-left: -15px;
    margin-right: -15px;
    border-radius: 15px;
    background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.6 rgba(210, 210, 210, 255), stop:0.7 rgba(210, 210, 210, 100));
}
QSlider::handle:vertical:hover {
    background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.6 rgba(255, 255, 255, 255), stop:0.7 rgba(255, 255, 255, 100));
}
"""


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        layout = QVBoxLayout(self)
        layout.addWidget(QSlider(Qt.Vertical, self))
        layout.addWidget(QSlider(Qt.Horizontal, self))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    w = Window()
    w.show()
    sys.exit(app.exec_())
