#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019/10/4
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: MagneticOfSun
@description: 
"""

#############################################################################
##
## Copyright (C) 2014 Riverbank Computing Limited.
## Copyright (C) 2014 Digia Plc
## All rights reserved.
## For any questions to Digia, please use contact form at http://qt.digia.com
##
## This file is part of the QtDataVisualization module.
##
## Licensees holding valid Qt Enterprise licenses may use this file in
## accordance with the Qt Enterprise License Agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and Digia.
##
## If you have questions regarding the use of this file, please use
## contact form at http://qt.digia.com
##
#############################################################################


import math

from PyQt5.QtCore import QFileInfo, QObject, QSize, Qt, QTimer, QLocale
from PyQt5.QtDataVisualization import (Q3DCamera, Q3DScatter, Q3DTheme,
                                       QAbstract3DGraph, QAbstract3DSeries, QScatter3DSeries,
                                       QScatterDataItem)
from PyQt5.QtGui import QColor, QLinearGradient, QQuaternion, QVector3D
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
                             QSlider, QSizePolicy, QVBoxLayout, QWidget)

country = QLocale.system().country()
if country in (QLocale.China, QLocale.HongKong, QLocale.Taiwan):
    Tr = {
        'Item rotations example - Magnetic field of the sun': '项目旋转示例-太阳磁场',
        'Toggle animation': '开启/关闭 动画',
        'Toggle Sun': '显示/隐藏 太阳',
        'Field Lines (1 - 128):': '磁场线条数(1 - 128)：',
        'Arrows per line (8 - 32):': '箭头数(8 - 32)：'
    }
else:
    Tr = {}


class ScatterDataModifier(QObject):
    verticalRange = 8.0
    horizontalRange = verticalRange
    ellipse_a = horizontalRange / 3.0
    ellipse_b = verticalRange
    doublePi = math.pi * 2.0
    radiansToDegrees = 360.0 / doublePi
    animationFrames = 30.0  # 动画帧数

    def __init__(self, scatter):
        super(ScatterDataModifier, self).__init__()

        mesh_dir = QFileInfo(__file__).absolutePath() + '/Data/mesh'

        self.m_graph = scatter  # Q3DScatter 对象实例
        self.m_rotationTimer = QTimer()
        self.m_fieldLines = 12  # 初始磁场线数量
        self.m_arrowsPerLine = 16  # 初始箭头数
        self.m_magneticField = QScatter3DSeries()  # 磁场线三维散点图
        self.m_sun = QScatter3DSeries()  # 太阳三维散点图
        self.m_angleOffset = 0.0  # 角度偏移
        self.m_angleStep = self.doublePi / self.m_arrowsPerLine / self.animationFrames

        # 设置阴影质量
        self.m_graph.setShadowQuality(QAbstract3DGraph.ShadowQualityNone)
        # 设置当前场景中的激活的相机预设值
        self.m_graph.scene().activeCamera().setCameraPreset(
            Q3DCamera.CameraPresetFront)

        # Magnetic field lines use custom narrow arrow.
        # 磁力线使用自定义窄箭头。
        self.m_magneticField.setItemSize(0.2)
        self.m_magneticField.setMesh(QAbstract3DSeries.MeshUserDefined)
        self.m_magneticField.setUserDefinedMesh(mesh_dir + '/narrowarrow.obj')
        # 设置渐变颜色
        fieldGradient = QLinearGradient(0, 0, 16, 1024)
        fieldGradient.setColorAt(0.0, Qt.black)
        fieldGradient.setColorAt(1.0, Qt.white)
        self.m_magneticField.setBaseGradient(fieldGradient)
        self.m_magneticField.setColorStyle(Q3DTheme.ColorStyleRangeGradient)

        # For 'sun' we use a custom large sphere.
        # 使用一个自定义的球体代表太阳
        self.m_sun.setItemSize(0.2)
        self.m_sun.setName("Sun")
        self.m_sun.setItemLabelFormat("@seriesName")
        self.m_sun.setMesh(QAbstract3DSeries.MeshUserDefined)
        self.m_sun.setUserDefinedMesh(mesh_dir + '/largesphere.obj')
        self.m_sun.setBaseColor(QColor(0xff, 0xbb, 0x00))
        self.m_sun.dataProxy().addItem(QScatterDataItem(QVector3D()))

        self.m_graph.addSeries(self.m_magneticField)
        self.m_graph.addSeries(self.m_sun)

        # Configure the axes according to the data.
        # 设置x轴的范围值
        self.m_graph.axisX().setRange(-self.horizontalRange,
                                      self.horizontalRange)
        # 设置y轴的范围值
        self.m_graph.axisY().setRange(-self.verticalRange, self.verticalRange)
        # 设置z轴的范围值
        self.m_graph.axisZ().setRange(-self.horizontalRange,
                                      self.horizontalRange)
        # x和z轴上的段数
        # 这表明绘制了多少标签。要绘制的网格线的数量使用公式计算：segments * subsegments + 1。预设默认值为5。该值不能低于1。
        self.m_graph.axisX().setSegmentCount(self.horizontalRange)
        self.m_graph.axisZ().setSegmentCount(self.horizontalRange)

        self.m_rotationTimer.timeout.connect(self.triggerRotation)

        self.toggleRotation()
        self.generateData()

    def generateData(self):
        # 生成模拟数据
        magneticFieldArray = []

        for i in range(self.m_fieldLines):
            horizontalAngle = (self.doublePi * i) / self.m_fieldLines
            xCenter = self.ellipse_a * math.cos(horizontalAngle)
            zCenter = self.ellipse_a * math.sin(horizontalAngle)

            # Rotate - arrow is always tangential to the origin.
            # 旋转-箭头始终与原点相切。
            yRotation = QQuaternion.fromAxisAndAngle(0.0, 1.0, 0.0,
                                                     horizontalAngle * self.radiansToDegrees)

            for j in range(self.m_arrowsPerLine):
                # Calculate the point on the ellipse centered on the origin and
                # 计算椭圆上以原点为中心的点
                # parallel to the x-axis.
                # 平行于X轴。
                verticalAngle = ((self.doublePi * j) / self.m_arrowsPerLine) + self.m_angleOffset
                xUnrotated = self.ellipse_a * math.cos(verticalAngle)
                y = self.ellipse_b * math.sin(verticalAngle)

                # Rotate the ellipse around the y-axis.
                # 围绕Y轴旋转椭圆。
                xRotated = xUnrotated * math.cos(horizontalAngle)
                zRotated = xUnrotated * math.sin(horizontalAngle)

                # Add the offset.
                # 添加偏移量。
                x = xCenter + xRotated
                z = zCenter + zRotated

                zRotation = QQuaternion.fromAxisAndAngle(0.0, 0.0, 1.0,
                                                         verticalAngle * self.radiansToDegrees)
                totalRotation = yRotation * zRotation

                itm = QScatterDataItem(QVector3D(x, y, z), totalRotation)
                magneticFieldArray.append(itm)

        if self.m_graph.selectedSeries() is self.m_magneticField:
            self.m_graph.clearSelection()

        self.m_magneticField.dataProxy().resetArray(magneticFieldArray)

    def setFieldLines(self, lines):
        self.m_fieldLines = lines
        self.generateData()

    def setArrowsPerLine(self, arrows):
        self.m_arrowsPerLine = arrows
        self.m_angleOffset = 0.0
        self.m_angleStep = self.doublePi / self.m_arrowsPerLine / self.animationFrames
        self.generateData()

    def triggerRotation(self):
        self.m_angleOffset += self.m_angleStep
        self.generateData()

    def toggleSun(self):
        self.m_sun.setVisible(not self.m_graph.seriesList()[1].isVisible())

    def toggleRotation(self):
        if self.m_rotationTimer.isActive():
            self.m_rotationTimer.stop()
        else:
            self.m_rotationTimer.start(15)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    graph = Q3DScatter()
    container = QWidget.createWindowContainer(graph)

    screenSize = graph.screen().size()
    container.setMinimumSize(
        QSize(screenSize.width() / 2, screenSize.height() / 1.5))
    container.setMaximumSize(screenSize)
    container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    container.setFocusPolicy(Qt.StrongFocus)

    widget = QWidget()
    hLayout = QHBoxLayout(widget)
    vLayout = QVBoxLayout()
    hLayout.addWidget(container, 1)
    hLayout.addLayout(vLayout)

    widget.setWindowTitle(Tr.get("Item rotations example - Magnetic field of the sun",
                                 "Item rotations example - Magnetic field of the sun"))

    toggleRotationButton = QPushButton(Tr.get("Toggle animation", "Toggle animation"))
    toggleSunButton = QPushButton(Tr.get("Toggle Sun", "Toggle Sun"))

    fieldLinesSlider = QSlider(Qt.Horizontal)
    fieldLinesSlider.setTickInterval(1)
    fieldLinesSlider.setMinimum(1)
    fieldLinesSlider.setValue(12)
    fieldLinesSlider.setMaximum(128)

    arrowsSlider = QSlider(Qt.Horizontal)
    arrowsSlider.setTickInterval(1)
    arrowsSlider.setMinimum(8)
    arrowsSlider.setValue(16)
    arrowsSlider.setMaximum(32)

    vLayout.addWidget(toggleRotationButton)
    vLayout.addWidget(toggleSunButton)
    vLayout.addWidget(QLabel(Tr.get("Field Lines (1 - 128):", "Field Lines (1 - 128):")))
    vLayout.addWidget(fieldLinesSlider)
    vLayout.addWidget(QLabel(Tr.get("Arrows per line (8 - 32):", "Arrows per line (8 - 32):")))
    vLayout.addWidget(arrowsSlider, 1, Qt.AlignTop)

    modifier = ScatterDataModifier(graph)

    toggleRotationButton.clicked.connect(modifier.toggleRotation)
    toggleSunButton.clicked.connect(modifier.toggleSun)
    fieldLinesSlider.valueChanged.connect(modifier.setFieldLines)
    arrowsSlider.valueChanged.connect(modifier.setArrowsPerLine)

    widget.show()
    sys.exit(app.exec_())
