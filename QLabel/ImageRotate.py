#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年11月19日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: 
@description: 
"""

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPixmap, QPainter, QImage
    from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, \
        QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QApplication
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QPixmap, QPainter, QImage
    from PySide2.QtWidgets import QWidget, QLabel, QPushButton, \
        QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QApplication


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.imageLabel = QLabel(self)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.imageLabel)
        clayout = QHBoxLayout()
        layout.addItem(clayout)
        clayout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        clayout.addWidget(QPushButton('水平翻转', self, clicked=self.doHorFilp))
        clayout.addWidget(QPushButton('垂直翻转', self, clicked=self.doVerFilp))
        clayout.addWidget(QPushButton(
            '顺时针45度', self, clicked=self.doClockwise))
        clayout.addWidget(QPushButton(
            '逆时针45度', self, clicked=self.doAnticlockwise))
        clayout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 原始图片
        self.srcImage = QImage('Data/fg.png')
        self.imageLabel.setPixmap(QPixmap.fromImage(self.srcImage))

    def doHorFilp(self):
        # 水平翻转
        self.srcImage = self.srcImage.mirrored(True, False)
        self.imageLabel.setPixmap(QPixmap.fromImage(self.srcImage))

    def doVerFilp(self):
        # 垂直翻转
        self.srcImage = self.srcImage.mirrored(False, True)
        self.imageLabel.setPixmap(QPixmap.fromImage(self.srcImage))

    def doClockwise(self):
        # 顺时针45度
        image = QImage(self.srcImage.size(),
                       QImage.Format_ARGB32_Premultiplied)
        painter = QPainter()
        painter.begin(image)
        # 以图片中心为原点
        hw = self.srcImage.width() / 2
        hh = self.srcImage.height() / 2
        painter.translate(hw, hh)
        painter.rotate(45)  # 旋转45度
        painter.drawImage(-hw, -hh, self.srcImage)  # 把图片绘制上去
        painter.end()
        self.srcImage = image  # 替换
        self.imageLabel.setPixmap(QPixmap.fromImage(self.srcImage))

    #         # 下面这个旋转方法针对90度的倍数,否则图片会变大
    #         trans = QTransform()
    #         trans.rotate(90)
    #         self.srcImage = self.srcImage.transformed(
    #             trans, Qt.SmoothTransformation)
    #         self.imageLabel.setPixmap(QPixmap.fromImage(self.srcImage))

    def doAnticlockwise(self):
        # 逆时针45度
        image = QImage(self.srcImage.size(),
                       QImage.Format_ARGB32_Premultiplied)
        painter = QPainter()
        painter.begin(image)
        # 以图片中心为原点
        hw = self.srcImage.width() / 2
        hh = self.srcImage.height() / 2
        painter.translate(hw, hh)
        painter.rotate(-45)  # 旋转-45度
        painter.drawImage(-hw, -hh, self.srcImage)  # 把图片绘制上去
        painter.end()
        self.srcImage = image  # 替换
        self.imageLabel.setPixmap(QPixmap.fromImage(self.srcImage))


#         # 下面这个旋转方法针对90度的倍数,否则图片会变大
#         trans = QTransform()
#         trans.rotate(90)
#         self.srcImage = self.srcImage.transformed(
#             trans, Qt.SmoothTransformation)
#         self.imageLabel.setPixmap(QPixmap.fromImage(self.srcImage))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
