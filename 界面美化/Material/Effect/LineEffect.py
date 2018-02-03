#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年2月3日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: LineEffect
@description: 
'''
from PyQt5.QtCore import QTimer, QLine
from PyQt5.QtGui import QPen


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class LineEffect:

    def __init__(self, *args, **kwargs):
        self._lSetp = 0
        self._lSp = 20
        self._lInDraw = False    # 获取焦点绘制状态
        self._lOutDraw = False    # 失去焦点绘制状态
        self._lEnabled = True
        self._lTimer = QTimer(
            self, interval=20, timeout=self._updateLineEffect)    # 计时器

    def _focusInEvent(self, event):
        if not self._lEnabled:
            return
        self._lTimer.stop()
        self._lInDraw = True
        self._lOutDraw = False
        self._lSetp = 0
        self._lTimer.start()
        self.update()

    def _focusOutEvent(self, event):
        if not self._lEnabled:
            return
        self._lTimer.stop()
        self._lInDraw = False
        self._lOutDraw = True
        self._lSetp = 0
        self._lTimer.start()
        self.update()

    def _paintEvent(self, painter):
        if not self._lEnabled:
            return
        pen = QPen(self.lineColor)
        pen.setWidth(self.borderWidth)
        painter.setPen(pen)
        cx, setp = self.width() / 2, self.width() / self._lSp
        if self.hasFocus():
            if self._lInDraw:
                painter.drawLines(
                    QLine(
                        cx, self.height(), cx + setp * self._lSetp, self.height()),
                    QLine(
                        cx, self.height(), cx - setp * self._lSetp, self.height()),
                )
            else:
                painter.drawLine(0, self.height(), self.width(), self.height())
        else:
            if self._lOutDraw:
                painter.drawLines(
                    QLine(cx + setp * (self._lSp - self._lSetp),
                          self.height(), cx, self.height()),
                    QLine(cx - setp * (self._lSp - self._lSetp),
                          self.height(), cx, self.height()),
                )

    def _updateLineEffect(self):
        if self._lSetp < self._lSp:
            self._lSetp += 1
            self.repaint()
            if self._lSetp == self._lSp:
                self._lSetp = 0
                self._lTimer.stop()
                if self._lInDraw:
                    self._lInDraw = False
                if self._lOutDraw:
                    self._lOutDraw = False
                    self.repaint()

    def _setEnabled(self, enable):
        self._lEnabled = enable

    def _setDisabled(self, enable):
        self._lEnabled = not enable
