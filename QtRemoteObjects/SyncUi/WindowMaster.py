#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年8月7日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: QtRemoteObjects.SyncUi.WindowMaster
@description: 主窗口
"""
from PyQt5.QtCore import QUrl, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtRemoteObjects import QRemoteObjectHost
from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QCheckBox, \
    QProgressBar


class WindowMaster(QWidget):
    # 输入框内容变化信号
    editValueChanged = pyqtSignal(str)
    # 勾选框变化信号
    checkToggled = pyqtSignal(bool)
    # 进度条变化信号
    progressValueChanged = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super(WindowMaster, self).__init__(*args, **kwargs)
        self.setupUi()

        # 开启节点
        host = QRemoteObjectHost(QUrl('local:WindowMaster'), parent=self)
        host.enableRemoting(self, 'WindowMaster')
        print('开启节点完成')

        # 定时器更新进度条
        self._value = 0
        self.utimer = QTimer(self, timeout=self.updateProgress)
        self.utimer.start(200)

    def setupUi(self):
        self.setWindowTitle('WindowMaster')
        self.resize(300, 400)
        layout = QVBoxLayout(self)
        # 输入框(双向同步)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.textChanged.connect(self.editValueChanged.emit)
        # 勾选框(双向同步)
        self.checkBox = QCheckBox('来勾我啊', self)
        self.checkBox.toggled.connect(self.checkToggled.emit)
        # 进度条(Master更新Slave)
        self.progressBar = QProgressBar(self)
        self.progressBar.valueChanged.connect(self.progressValueChanged.emit)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.checkBox)
        layout.addWidget(self.progressBar)

    def updateProgress(self):
        self._value += 1
        if self._value > 100:
            self._value = 0
        self.progressBar.setValue(self._value)

    @pyqtSlot(str)
    def updateEdit(self, text):
        """更新输入框内容的槽函数
        :param text:
        """
        self.lineEdit.setText(text)

    @pyqtSlot(bool)
    def updateCheck(self, checked):
        """更新勾选框的槽函数
        :param checked:
        """
        self.checkBox.setChecked(checked)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = WindowMaster()
    w.show()
    sys.exit(app.exec_())
