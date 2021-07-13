#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/9/14
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: ColumnView
@description: 
"""

try:
    from PyQt5.QtWidgets import QApplication, QComboBox, QFileSystemModel, QHBoxLayout, QSpacerItem, \
        QSizePolicy
except ImportError:
    from PyQt5.QtWidgets import QApplication, QComboBox, QFileSystemModel, QHBoxLayout, QSpacerItem, \
        QSizePolicy


class PathComboBox(QComboBox):

    def __init__(self, *args, is_item=False, **kwargs):
        super(PathComboBox, self).__init__(*args, **kwargs)
        self.is_item = is_item
        if not self.is_item:
            self.setEditable(True)
            layout = QHBoxLayout(self)
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 23)
            layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        else:
            self.f_model = QFileSystemModel(self)
            self.f_model.setRootPath('')
            self.setModel(self.f_model)

    def addWidget(self, widget):
        self.layout().insertWidget(self.layout().count() - 1, widget)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = PathComboBox()
    w.show()
    w.addWidget(PathComboBox(w, is_item=True))
    sys.exit(app.exec_())
