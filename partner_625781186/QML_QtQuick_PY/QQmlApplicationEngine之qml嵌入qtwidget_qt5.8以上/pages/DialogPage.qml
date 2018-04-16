/****************************************************************************
**
** Copyright (C) 2017 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the examples of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** BSD License Usage
** Alternatively, you may use this file under the terms of the BSD license
** as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/

import QtQuick 2.6
import QtQuick.Layouts 1.0
import QtQuick.Controls 2.1

ScrollablePage {
    id: page

    readonly property int buttonWidth: Math.max(button.implicitWidth, Math.min(button.implicitWidth * 2, page.availableWidth / 3))

    Column {
        spacing: 40
        width: parent.width

        Label {
            width: parent.width
            wrapMode: Label.Wrap
            horizontalAlignment: Qt.AlignHCenter
            text: "Dialog is a popup that is mostly used for short-term tasks "
                + "and brief communications with the user."
        }

        Button {
            text: "Message"
            anchors.horizontalCenter: parent.horizontalCenter
            width: buttonWidth
            onClicked: messageDialog.open()

            Dialog {
                id: messageDialog

                x: (parent.width - width) / 2
                y: (parent.height - height) / 2

                title: "Message"

                Label {
                    text: "Lorem ipsum dolor sit amet..."
                }
            }
        }

        Button {
            id: button
            text: "Confirmation"
            anchors.horizontalCenter: parent.horizontalCenter
            width: buttonWidth
            onClicked: confirmationDialog.open()

            Dialog {
                id: confirmationDialog

                x: (parent.width - width) / 2
                y: (parent.height - height) / 2
                parent: ApplicationWindow.overlay

                modal: true
                title: "Confirmation"
                standardButtons: Dialog.Yes | Dialog.No

                Column {
                    spacing: 20
                    anchors.fill: parent
                    Label {
                        text: "The document has been modified.\nDo you want to save your changes?"
                    }
                    CheckBox {
                        text: "Do not ask again"
                        anchors.right: parent.right
                    }
                }
            }
        }

        Button {
            text: "Content"
            anchors.horizontalCenter: parent.horizontalCenter
            width: buttonWidth
            onClicked: contentDialog.open()

            Dialog {
                id: contentDialog

                x: (parent.width - width) / 2
                y: (parent.height - height) / 2
                width: Math.min(page.width, page.height) / 3 * 2
                contentHeight: logo.height * 2
                parent: ApplicationWindow.overlay

                modal: true
                title: "Content"
                standardButtons: Dialog.Close

                Flickable {
                    id: flickable
                    clip: true
                    anchors.fill: parent
                    contentHeight: column.height

                    Column {
                        id: column
                        spacing: 20
                        width: parent.width

                        Image {
                            id: logo
                            width: parent.width / 2
                            anchors.horizontalCenter: parent.horizontalCenter
                            fillMode: Image.PreserveAspectFit
                            source: "../images/qt-logo.png"
                        }

                        Label {
                            width: parent.width
                            text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc finibus "
                                + "in est quis laoreet. Interdum et malesuada fames ac ante ipsum primis "
                                + "in faucibus. Curabitur eget justo sollicitudin enim faucibus bibendum. "
                                + "Suspendisse potenti. Vestibulum cursus consequat mauris id sollicitudin. "
                                + "Duis facilisis hendrerit consectetur. Curabitur sapien tortor, efficitur "
                                + "id auctor nec, efficitur et nisl. Ut venenatis eros in nunc placerat, "
                                + "eu aliquam enim suscipit."
                            wrapMode: Label.Wrap
                        }
                    }

                    ScrollIndicator.vertical: ScrollIndicator {
                        parent: contentDialog.contentItem
                        anchors.top: flickable.top
                        anchors.bottom: flickable.bottom
                        anchors.right: parent.right
                        anchors.rightMargin: -contentDialog.rightPadding + 1
                    }
                }
            }
        }

        Button {
            text: "Input"
            anchors.horizontalCenter: parent.horizontalCenter
            width: buttonWidth
            onClicked: inputDialog.open()

            Dialog {
                id: inputDialog

                x: (parent.width - width) / 2
                y: (parent.height - height) / 2
                parent: ApplicationWindow.overlay

                focus: true
                modal: true
                title: "Input"
                standardButtons: Dialog.Ok | Dialog.Cancel

                ColumnLayout {
                    spacing: 20
                    anchors.fill: parent
                    Label {
                        elide: Label.ElideRight
                        text: "Please enter the credentials:"
                        Layout.fillWidth: true
                    }
                    TextField {
                        focus: true
                        placeholderText: "Username"
                        Layout.fillWidth: true
                    }
                    TextField {
                        placeholderText: "Password"
                        echoMode: TextField.PasswordEchoOnEdit
                        Layout.fillWidth: true
                    }
                }
            }
        }
    }
}
