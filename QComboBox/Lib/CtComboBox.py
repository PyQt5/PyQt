#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2022/09/04
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: CtComboBox.py
@description: 文字居中对齐
"""

try:
    from PyQt5.QtCore import QRect, Qt
    from PyQt5.QtGui import QIcon, QPalette
    from PyQt5.QtWidgets import QComboBox, QProxyStyle
except ImportError:
    from PySide2.QtCore import QRect, Qt
    from PySide2.QtGui import QIcon, QPalette
    from PySide2.QtWidgets import QComboBox, QProxyStyle


class ComboBoxStyle(QProxyStyle):

    def drawControl(self, element, option, painter, widget=None):
        if element == QProxyStyle.CE_ComboBoxLabel:
            # https://github.com/qt/qtbase/blob/5.15.2/src/widgets/styles/qcommonstyle.cpp#L2200
            editRect = self.subControlRect(QProxyStyle.CC_ComboBox, option,
                                           QProxyStyle.SC_ComboBoxEditField,
                                           widget)
            painter.save()
            painter.setClipRect(editRect)
            if not option.currentIcon.isNull():
                # 绘制图标
                mode = QIcon.Normal if (
                    option.state &
                    QProxyStyle.State_Enabled) else QIcon.Disabled
                pixmap = option.currentIcon.pixmap(
                    widget.window().windowHandle() if widget else None,
                    option.iconSize, mode)
                iconRect = QRect(editRect)
                iconRect.setWidth(option.iconSize.width() + 4)
                iconRect = self.alignedRect(option.direction,
                                            Qt.AlignLeft | Qt.AlignVCenter,
                                            iconRect.size(), editRect)
                if option.editable:
                    painter.fillRect(iconRect,
                                     option.palette.brush(QPalette.Base))
                self.drawItemPixmap(painter, iconRect, Qt.AlignCenter, pixmap)

                if option.direction == Qt.RightToLeft:
                    editRect.translate(-4 - option.iconSize.width(), 0)
                else:
                    editRect.translate(option.iconSize.width() + 4, 0)
            if option.currentText and not option.editable:
                # 考虑右边箭头位置
                arrowRect = self.subControlRect(QProxyStyle.CC_ComboBox, option,
                                                QProxyStyle.SC_ComboBoxArrow,
                                                widget)
                editRect.setWidth(editRect.width() + arrowRect.width())
                # 绘制居中文字
                self.drawItemText(
                    painter, editRect.adjusted(1, 0, -1, 0),
                    self.visualAlignment(option.direction, Qt.AlignCenter),
                    option.palette, option.state & QProxyStyle.State_Enabled,
                    option.currentText)
            painter.restore()
            return
        super(ComboBoxStyle, self).drawControl(element, option, painter, widget)


class CtComboBox(QComboBox):

    def __init__(self, *args, **kwargs):
        super(CtComboBox, self).__init__(*args, **kwargs)
        # 绑定每个元素添加信号，用于设置文本居中
        self.model().rowsInserted.connect(self._onRowsInserted)
        self.setStyle(ComboBoxStyle())

    def _onRowsInserted(self, index, first, last):
        if first < 0:
            return
        for i in range(first, last + 1):
            self.view().model().item(i).setTextAlignment(Qt.AlignCenter)
