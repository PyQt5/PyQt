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

import QtQuick 2.8
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.0
import Theme 1.0

Item {
    id: form

    width: 320
    height: 480
    property alias slider: slider
    property alias checkBoxUnderline: checkBoxUnderline
    property alias checkBoxBold: checkBoxBold
    property alias sizeSwitch: sizeSwitch
    property alias button: button

    Slider {
        id: slider
        width: 297
        height: 38
        stepSize: 1
        to: 18
        from: 10
        value: 14
        anchors.topMargin: Theme.baseSize
        anchors.top: gridLayout.bottom
        anchors.right: gridLayout.right
        anchors.left: gridLayout.left
        handle: Rectangle {
            id: sliderHandle
            x: slider.leftPadding + slider.visualPosition * (slider.availableWidth - width)
            y: slider.topPadding + slider.availableHeight / 2 - height / 2
            implicitWidth: 26
            implicitHeight: 26
            radius: 13
            color: slider.pressed ? Theme.mainColorDarker : Theme.mainColor
            border.color: Theme.gray
        }
    }

    GridLayout {
        id: gridLayout
        anchors.top: parent.top
        anchors.topMargin: 64

        anchors.horizontalCenter: parent.horizontalCenter
        columnSpacing: Theme.baseSize * 0.5
        rowSpacing: Theme.baseSize * 0.5
        rows: 4
        columns: 2

        Label {
            text: qsTr("Toggle Size")
            font: Theme.font
        }

        Switch {
            id: sizeSwitch
            Layout.fillWidth: true
        }

        CheckBox {
            id: checkBoxBold
            text: qsTr("Bold")
            checked: true
            Layout.fillWidth: true
        }

        CheckBox {
            id: checkBoxUnderline
            text: qsTr("Underline")
            Layout.fillWidth: true
        }

        Rectangle {
            id: rectangle
            color: Theme.mainColor
            Layout.fillWidth: true
            Layout.columnSpan: 2
            Layout.preferredHeight: 38
            Layout.preferredWidth: 297
        }

        Label {
            id: label
            text: qsTr("Customization")
            font: Theme.font
        }

        Button {
            id: button
            text: qsTr("Change Color")
            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
        }
    }
}
