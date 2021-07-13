#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年8月7日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: QtRemoteObjects.SyncUi.WindowSlave
@description: 备窗口
"""
from PyQt5.QtCore import QUrl
from PyQt5.QtRemoteObjects import QRemoteObjectNode, QRemoteObjectReplica
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QCheckBox, \
    QProgressBar, QMessageBox


class WindowSlave(QWidget):

    def __init__(self, *args, **kwargs):
        super(WindowSlave, self).__init__(*args, **kwargs)
        self.setupUi()
        # 加入Master节点
        node = QRemoteObjectNode(parent=self)
        node.connectToNode(QUrl('local:WindowMaster'))
        # 获取WindowMaster对象
        self.windowMaster = node.acquireDynamic('WindowMaster')
        # 初始化成功后才能去绑定信号等
        self.windowMaster.initialized.connect(self.onInitialized)
        # 状态改变 https://doc.qt.io/qt-5/qremoteobjectreplica.html#State-enum
        self.windowMaster.stateChanged.connect(self.onStateChanged)

    def setupUi(self):
        self.setWindowTitle('WindowSlave')
        self.resize(300, 400)
        layout = QVBoxLayout(self)
        # 输入框(双向同步)
        self.lineEdit = QLineEdit(self)
        # 勾选框(双向同步)
        self.checkBox = QCheckBox('来勾我啊', self)
        # 进度条(Master更新Slave)
        self.progressBar = QProgressBar(self)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.checkBox)
        layout.addWidget(self.progressBar)

    def onStateChanged(self, newState, oldState):
        if newState == QRemoteObjectReplica.Suspect:
            QMessageBox.critical(self, '错误', '连接丢失')

    def onInitialized(self):
        # Master和Slave输入框绑定
        self.windowMaster.editValueChanged.connect(self.lineEdit.setText)
        self.lineEdit.textChanged.connect(self.windowMaster.updateEdit)

        # Master和Slave勾选框绑定
        self.windowMaster.checkToggled.connect(self.checkBox.setChecked)
        self.checkBox.toggled.connect(self.windowMaster.updateCheck)

        # Master进度条同步到Slave
        self.windowMaster.progressValueChanged.connect(
            self.progressBar.setValue)

        print('绑定信号槽完成')


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = WindowSlave()
    w.show()
    sys.exit(app.exec_())
