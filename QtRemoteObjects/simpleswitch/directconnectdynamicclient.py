#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2018 Riverbank Computing Limited
## Copyright (C) 2017 Ford Motor Company
##
## This file is part of the PyQt examples.
##
## $QT_BEGIN_LICENSE:BSD$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## BSD License Usage
## Alternatively, you may use this file under the terms of the BSD license
## as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of The Qt Company Ltd nor the names of its
##     contributors may be used to endorse or promote products derived
##     from this software without specific prior written permission.
##
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


import sys

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QCoreApplication, QObject, QUrl
from PyQt5.QtRemoteObjects import QRemoteObjectNode


class DynamicClient(QObject):

    # This signal is connected with server_slot() slot of the source object and
    # echoes back the switch state received from the source.
    echoSwitchState = pyqtSignal(bool)

    def __init__(self, replica, parent=None):
        super().__init__(parent)

        self._replica = replica
        self._clientSwitchState = False

        replica.initialized.connect(self.initConnection)

    @pyqtSlot(bool)
    def recSwitchState(self, value):
        self._clientSwitchState = self._replica.property('currState')

        print("Received source state", value, self._clientSwitchState)

        # Emit the signal to echo the received state back to the server.
        self.echoSwitchState.emit(self._clientSwitchState)

    @pyqtSlot()
    def initConnection(self):
        # Connect the replica source signal currStateChanged() with the
        # client's recSwitchState() slot to receive the source's current state.
        self._replica.currStateChanged.connect(self.recSwitchState)

        # Connect the client's echoSwitchState() signal with replica's
        # server_slot() to echo back the received state.
        self.echoSwitchState.connect(self._replica.server_slot)


if __name__ == '__main__':

    app = QCoreApplication(sys.argv)

    # Create the remote object node.
    repNode = QRemoteObjectNode()

    # Connect with the remote host node.
    repNode.connectToNode(QUrl('local:replica'))

    # Acquire a replica of the source from the host node.
    replica = repNode.acquireDynamic('SimpleSwitch')

    # Create the client switch object and pass the replica to it.
    rswitch = DynamicClient(replica)

    sys.exit(app.exec_())
