#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年11月5日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: ClickJumpSlider
@description: 
"""

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QApplication, QSlider, QStyleOptionSlider, QStyle, QWidget, QFormLayout, \
        QLabel
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QApplication, QSlider, QStyleOptionSlider, QStyle, QWidget, QFormLayout, \
        QLabel


class ClickJumpSlider(QSlider):

    def mousePressEvent(self, event):
        # 获取上面的拉动块位置
        option = QStyleOptionSlider()
        self.initStyleOption(option)
        rect = self.style().subControlRect(
            QStyle.CC_Slider, option, QStyle.SC_SliderHandle, self)
        if rect.contains(event.pos()):
            # 如果鼠标点击的位置在滑块上则交给Qt自行处理
            super(ClickJumpSlider, self).mousePressEvent(event)
            return
        if self.orientation() == Qt.Horizontal:
            # 横向，要考虑invertedAppearance是否反向显示的问题
            self.setValue(self.style().sliderValueFromPosition(
                self.minimum(), self.maximum(),
                event.x() if not self.invertedAppearance() else (self.width(
                ) - event.x()), self.width()))
        else:
            # 纵向
            self.setValue(self.style().sliderValueFromPosition(
                self.minimum(), self.maximum(),
                (self.height() - event.y()) if not self.invertedAppearance(
                ) else event.y(), self.height()))


class DemoWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(DemoWindow, self).__init__(*args, **kwargs)
        self.resize(600, 600)
        layout = QFormLayout(self)

        self.label1 = QLabel('0', self)
        self.slider1 = ClickJumpSlider(Qt.Horizontal)
        self.slider1.valueChanged.connect(lambda v: self.label1.setText(str(v)))
        layout.addRow(self.label1, self.slider1)

        # 横向-反向显示
        self.label2 = QLabel('0', self)
        self.slider2 = ClickJumpSlider(Qt.Horizontal, invertedAppearance=True)
        self.slider2.valueChanged.connect(lambda v: self.label2.setText(str(v)))
        layout.addRow(self.label2, self.slider2)

        self.label3 = QLabel('0', self)
        self.slider3 = ClickJumpSlider(Qt.Vertical, minimumHeight=200)
        self.slider3.valueChanged.connect(lambda v: self.label3.setText(str(v)))
        layout.addRow(self.label3, self.slider3)

        # 纵向反向显示
        self.label4 = QLabel('0', self)
        self.slider4 = ClickJumpSlider(Qt.Vertical, invertedAppearance=True, minimumHeight=200)
        self.slider4.valueChanged.connect(lambda v: self.label4.setText(str(v)))
        layout.addRow(self.label4, self.slider4)


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(format='text')

    app = QApplication(sys.argv)
    w = DemoWindow()
    w.show()
    sys.exit(app.exec_())
