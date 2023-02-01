#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2023/02/01
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: InteractiveRun.py
@description:
"""

import os
import sys

try:
    import chardet
except ImportError:
    print('chardet not found')

try:
    from PyQt5.QtCore import QProcess
    from PyQt5.QtWidgets import (QApplication, QLineEdit, QPushButton,
                                 QTextBrowser, QVBoxLayout, QWidget)
except ImportError:
    from PySide2.QtCore import QProcess
    from PySide2.QtWidgets import (QApplication, QLineEdit, QPushButton,
                                   QTextBrowser, QVBoxLayout, QWidget)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)

        command = 'ping www.baidu.com'
        if sys.platform.startswith('win'):
            command = 'ping -n 5 www.baidu.com'
        elif sys.platform.startswith('darwin') or sys.platform.startswith(
                'linux'):
            command = 'ping -c 5 www.baidu.com'
        else:
            raise RuntimeError('Unsupported platform: %s' % sys.platform)

        self.cmdEdit = QLineEdit(command, self)
        layout.addWidget(self.cmdEdit)

        self.buttonRun = QPushButton('执行命令', self)
        layout.addWidget(self.buttonRun)
        self.buttonRun.clicked.connect(self.run_command)

        self.resultView = QTextBrowser(self)
        layout.addWidget(self.resultView)

        self._cmdProcess = None
        self._init()

    def closeEvent(self, event):
        if self._cmdProcess:
            self._cmdProcess.writeData('exit'.encode() + os.linesep.encode())
            self._cmdProcess.waitForFinished()
            if self._cmdProcess:
                self._cmdProcess.terminate()
        super(Window, self).closeEvent(event)

    def _init(self):
        if self._cmdProcess:
            return
        # 打开终端shell
        self._cmdProcess = QProcess(self)
        self._cmdProcess.setProgram(
            'cmd' if sys.platform.startswith('win') else 'bash')
        # 合并输出流和错误流，只从标准输出流读取数据
        self._cmdProcess.setProcessChannelMode(QProcess.MergedChannels)
        self._cmdProcess.started.connect(self.on_started)
        self._cmdProcess.finished.connect(self.on_finished)
        self._cmdProcess.errorOccurred.connect(self.on_error)
        self._cmdProcess.readyReadStandardOutput.connect(
            self.on_readyReadStandardOutput)
        self._cmdProcess.start()

    def run_command(self):
        self._init()
        command = self.cmdEdit.text().strip()
        if not command:
            return
        command = command.encode(sys.getdefaultencoding()) + os.linesep.encode(
            sys.getdefaultencoding())
        self._cmdProcess.writeData(command)

    def on_started(self):
        self.resultView.append('ping process started, pid: %s' %
                               self._cmdProcess.processId())

    def on_finished(self, exitCode, exitStatus):
        print('ping process finished, exitCode: %s, exitStatus: %s' %
              (exitCode, exitStatus))
        self._cmdProcess.kill()
        self._cmdProcess = None

    def on_error(self, error):
        self.resultView.append('ping process error: %s, message: %s' %
                               (error, self._cmdProcess.errorString()))
        self._cmdProcess.kill()
        self._cmdProcess = None

    def on_readyReadStandardOutput(self):
        # 读取已有结果
        result = self._cmdProcess.readAllStandardOutput().data()
        try:
            encoding = chardet.detect(result)
            self.resultView.append(result.decode(encoding['encoding']))
        except Exception:
            self.resultView.append(result.decode('utf-8', errors='ignore'))


if __name__ == '__main__':
    import cgitb

    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
