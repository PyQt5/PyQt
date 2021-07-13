#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2021年06月23日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: TabCornerStyle
@description: 
"""

try:
    from PyQt5.QtCore import QRect
    from PyQt5.QtWidgets import QProxyStyle, QStyle
except ImportError:
    from PySide2.QtCore import QRect
    from PySide2.QtWidgets import QProxyStyle, QStyle


class TabCornerStyle(QProxyStyle):

    def subElementRect(self, element, option, widget):
        try:
            rect = super(TabCornerStyle, self).subElementRect(element, option, widget)
            if element == QStyle.SE_TabWidgetRightCorner and rect.isValid():
                # 标签tab的矩形范围
                tab_rect = self.subElementRect(QStyle.SE_TabWidgetTabBar, option, widget)
                # 内容面板的矩形范围
                panel_rect = self.subElementRect(QStyle.SE_TabWidgetTabPane, option, widget)
                ext_height = 2 * self.pixelMetric(QStyle.PM_TabBarBaseHeight, option, widget)
                # 修正过后填充的矩形范围
                cor_rect = QRect(tab_rect.x() + tab_rect.width() + ext_height, tab_rect.y() + ext_height,
                                 panel_rect.width() - tab_rect.width() - 2 * ext_height,
                                 tab_rect.height() - 2 * ext_height)
                return cor_rect
            return rect
        except Exception as e:
            print(e)
            return QRect()
