#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2022/02/25
@author: Irony
@site: https://pyqt.site, https://github.com/PyQt5
@email: 892768447@qq.com
@file: ColourfulProgress.py
@description:
"""

try:
    from PyQt5.QtCore import QLineF, QRect, QRectF, Qt
    from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen, QTransform
    from PyQt5.QtWidgets import (QApplication, QGridLayout, QProgressBar,
                                 QSlider, QStyleOptionProgressBar, QWidget)
except ImportError:
    from PySide2.QtCore import QRect, Qt, QRectF, QLineF
    from PySide2.QtGui import QColor, QPainter, QPen, QTransform, QPainterPath
    from PySide2.QtWidgets import (QApplication, QProgressBar,
                                   QStyleOptionProgressBar, QWidget, QSlider,
                                   QGridLayout)

from Lib.QStyleAnimation import QProgressStyleAnimation


class ColourfulProgress(QProgressBar):

    def __init__(self, *args, **kwargs):
        self._color = kwargs.pop('color', QColor(43, 194, 83))
        self._fps = kwargs.pop('fps', 60)
        self._lineWidth = kwargs.pop('lineWidth', 50)  # 线条宽度
        self._radius = kwargs.pop('radius', None)  # None为自动计算圆角
        self._animation = None
        super(ColourfulProgress, self).__init__(*args, **kwargs)
        self.setColor(self._color)
        self.setFps(self._fps)
        self.setLineWidth(self._lineWidth)
        self.setRadius(self._radius)

    def setColor(self, color):
        """
        :type color: QColor
        :param color: 颜色
        """
        self._color = QColor(color) if isinstance(
            color, (QColor, Qt.GlobalColor)) else QColor(43, 194, 83)

    def setFps(self, fps):
        """
        :type fps: int
        :param fps: 帧率
        """
        self._fps = max(int(fps), 1) if isinstance(fps, (int, float)) else 60

    def setLineWidth(self, width):
        """
        :type width: int
        :param width: 线条宽度
        """
        self._lineWidth = max(int(width), 0) if isinstance(width,
                                                           (int, float)) else 50

    def setRadius(self, radius):
        """
        :type radius: int
        :param radius: 半径
        """
        self._radius = max(int(radius), 1) if isinstance(radius,
                                                         (int, float)) else None

    def paintEvent(self, _):
        """
        重写绘制事件，参考 qfusionstyle.cpp 中的 CE_ProgressBarContents 绘制方法
        """
        option = QStyleOptionProgressBar()
        self.initStyleOption(option)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(0.5, 0.5)

        vertical = option.orientation == Qt.Vertical  # 是否垂直
        inverted = option.invertedAppearance  # 是否反转
        # 是否显示动画
        indeterminate = (option.minimum == option.maximum) or (
            option.minimum < option.progress < option.maximum)
        rect = option.rect

        if vertical:
            rect = QRect(rect.left(), rect.top(), rect.height(),
                         rect.width())  # 翻转宽度和高度
            m = QTransform.fromTranslate(rect.height(), 0)
            m.rotate(90.0)
            painter.setTransform(m, True)

        maxWidth = rect.width()
        progress = max(option.progress, option.minimum)
        totalSteps = max(1, option.maximum - option.minimum)
        progressSteps = progress - option.minimum
        progressBarWidth = int(progressSteps * maxWidth / totalSteps)
        width = progressBarWidth  # 已进行的进度宽度
        radius = max(1, (min(width,
                             self.width() if vertical else self.height()) //
                         4) if self._radius is None else self._radius)

        reverse = (not vertical and
                   option.direction == Qt.RightToLeft) or vertical
        if inverted:
            reverse = not reverse

        # 绘制范围
        path = QPainterPath()
        if not reverse:
            progressBar = QRectF(rect.left(), rect.top(), width, rect.height())
        else:
            progressBar = QRectF(rect.right() - width, rect.top(), width,
                                 rect.height())

        # 切割范围
        path.addRoundedRect(progressBar, radius, radius)
        painter.setClipPath(path)

        # 绘制背景颜色
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._color)
        painter.drawRoundedRect(progressBar, radius, radius)

        if not indeterminate:
            if self._animation:
                self._animation.stop()
                self._animation = None
        else:
            # 叠加颜色覆盖后出现类似线条间隔的效果
            color = self._color.lighter(320)
            color.setAlpha(80)
            painter.setPen(QPen(color, self._lineWidth))

            if self._animation:
                if self._animation.state() == QProgressStyleAnimation.Stopped:
                    # FIXME: 最小化后动画会停止
                    self._animation.start()
                step = int(self._animation.animationStep() % self._lineWidth)
            else:
                step = 0
                self._animation = QProgressStyleAnimation(self._fps, self)
                self._animation.start()

            # 动画斜线绘制
            startX = int(progressBar.left() - rect.height() - self._lineWidth)
            endX = int(rect.right() + self._lineWidth)

            if (not inverted and not vertical) or (inverted and vertical):
                lines = [
                    QLineF(x + step, progressBar.bottom(),
                           x + rect.height() + step, progressBar.top())
                    for x in range(startX, endX, self._lineWidth)
                ]
            else:
                lines = [
                    QLineF(x - step, progressBar.bottom(),
                           x + rect.height() - step, progressBar.top())
                    for x in range(startX, endX, self._lineWidth)
                ]
            painter.drawLines(lines)


if __name__ == '__main__':
    import cgitb
    import sys

    cgitb.enable(format='text')
    app = QApplication(sys.argv)

    w = QWidget()
    layout = QGridLayout(w)

    w1 = ColourfulProgress(color=QColor('#85c440'))
    w1.setMinimumWidth(300)
    w1.setMaximumWidth(300)
    w1.setRange(0, 100)
    layout.addWidget(w1, 0, 0, 1, 1)

    w2 = ColourfulProgress(color=QColor('#f2b63c'))
    w2.setMinimumWidth(300)
    w2.setMaximumWidth(300)
    w2.setInvertedAppearance(True)
    w2.setRange(0, 100)
    layout.addWidget(w2, 1, 0, 1, 1)

    w3 = ColourfulProgress(color=QColor('#db3a27'))
    w3.setMinimumHeight(300)
    w3.setMaximumHeight(300)
    w3.setOrientation(Qt.Vertical)
    w3.setRange(0, 100)
    layout.addWidget(w3, 0, 1, 2, 1)

    w4 = ColourfulProgress(color=QColor('#5aaadb'))
    w4.setMinimumHeight(300)
    w4.setMaximumHeight(300)
    w4.setInvertedAppearance(True)
    w4.setOrientation(Qt.Vertical)
    w4.setRange(0, 100)
    layout.addWidget(w4, 0, 2, 2, 1)

    slider = QSlider(Qt.Horizontal)
    slider.setRange(0, 100)
    slider.valueChanged.connect(w1.setValue)
    slider.valueChanged.connect(w2.setValue)
    slider.valueChanged.connect(w3.setValue)
    slider.valueChanged.connect(w4.setValue)
    slider.setValue(50)
    layout.addWidget(slider, 2, 0, 1, 3)

    w.show()

    sys.exit(app.exec_())
