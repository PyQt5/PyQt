#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年1月26日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: CustomIcon
@description: 
"""

import sys

try:
    from PyQt5.QtCore import QFileInfo
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QFileSystemModel, QFileIconProvider, QApplication, \
        QTreeView
except ImportError:
    from PySide2.QtCore import QFileInfo
    from PySide2.QtGui import QIcon
    from PySide2.QtWidgets import QFileSystemModel, QFileIconProvider, QApplication, \
        QTreeView


class FileIconProvider(QFileIconProvider):
    """图标提供类"""

    def __init__(self, *args, **kwargs):
        super(FileIconProvider, self).__init__(*args, **kwargs)
        self.DirIcon = QIcon("Data/icons/folder.png")
        self.TxtIcon = QIcon("Data/icons/file.png")

    def icon(self, type_info):
        '''
        :param fileInfo: 参考http://doc.qt.io/qt-5/qfileinfo.html
        '''
        if isinstance(type_info, QFileInfo):
            # 如果type_info是QFileInfo类型则用getInfoIcon来返回图标
            return self.getInfoIcon(type_info)
        # 如果type_info是QFileIconProvider自身的IconType枚举类型则执行下面的方法
        # 这里只能自定义通用的几种类型，参考http://doc.qt.io/qt-5/qfileiconprovider.html#IconType-enum
        '''
        QFileIconProvider::Computer     0
        QFileIconProvider::Desktop      1
        QFileIconProvider::Trashcan     2
        QFileIconProvider::Network      3
        QFileIconProvider::Drive        4
        QFileIconProvider::Folder       5
        QFileIconProvider::File         6
        '''
        if type_info == QFileIconProvider.Folder:
            # 如果是文件夹
            return self.DirIcon
        return super(FileIconProvider, self).icon(type_info)

    def getInfoIcon(self, type_info):
        if type_info.isDir():  # 文件夹
            return self.DirIcon
        if type_info.isFile() and type_info.suffix() == "txt":  # 文件并且是txt
            return self.TxtIcon
        return super(FileIconProvider, self).icon(type_info)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    model = QFileSystemModel()
    model.setIconProvider(FileIconProvider())  # 设置为自定义的图标提供类
    model.setRootPath("")
    tree = QTreeView()
    tree.setModel(model)

    tree.setAnimated(False)
    tree.setIndentation(20)
    tree.setSortingEnabled(True)

    tree.setWindowTitle("Dir View")
    tree.resize(640, 480)
    tree.show()

    sys.exit(app.exec_())
