#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2018年2月3日
@author: Irony."[讽刺]
@site: http://alyl.vip, http://orzorz.vip, https://coding.net/u/892768447, https://github.com/892768447
@email: 892768447@qq.com
@file: LineEdit
@description: 
'''
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QLineEdit, QFrame

from Effect.LineEffect import LineEffect  # @UnresolvedImport
from Utils.MaterialProperty import MaterialProperty  # @UnresolvedImport


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class LineEdit(QLineEdit, MaterialProperty, LineEffect):

    def __init__(self, *args, **kwargs):
        super(LineEdit, self).__init__(*args, **kwargs)
        self.borderWidth = 4
        LineEffect.__init__(self)
        # 去掉边框
        self.setFrame(QFrame.NoFrame)

    def paintEvent(self, event):
        super(LineEdit, self).paintEvent(event)
        painter = QPainter(self)
        pen = QPen(self.lineHintColor)
        pen.setWidth(self.borderWidth)
        painter.setPen(pen)  # draw bottom line(画底部横线)
        #painter.drawLine(self.rect().bottomLeft(), self.rect().bottomRight())
        painter.drawLine(0, self.height(), self.width(), self.height())
        if not self.isEnabled() or self.isReadOnly():
            return
        LineEffect._paintEvent(self, painter)

    def focusInEvent(self, event):
        super(LineEdit, self).focusInEvent(event)
        LineEffect._focusInEvent(self, event)

    def focusOutEvent(self, event):
        super(LineEdit, self).focusOutEvent(event)
        LineEffect._focusOutEvent(self, event)

    def setReadOnly(self, only):
        super(LineEdit, self).setReadOnly(only)
        LineEffect._setEnabled(self, False)

    def setEnabled(self, enable):
        super(LineEdit, self).setEnabled(enable)
        LineEffect._setEnabled(self, enable)

    def setDisabled(self, enable):
        super(LineEdit, self).setDisabled(enable)
        LineEffect._setDisabled(self, enable)
