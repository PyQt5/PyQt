import QtQuick 2.8
import QtQuick.Window 2.2
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.0

Rectangle {
    id: rectangle
    visible: true
    width: 300
    height: 300

    color: "#0e0c0c"
    clip: false

    GridLayout {
        anchors.leftMargin: 0
        anchors.topMargin: 0
        anchors.rightMargin: 107
        anchors.bottomMargin: 0
        anchors.fill: parent
        rows: 3
        columns: 2

        Slider {
            id: slider
            Layout.columnSpan: 2
            value: 0.5
        }

        Switch {
            id: switch1
            text: qsTr("Switch")
            Layout.columnSpan: 2
        }

        ProgressBar {
            id: progressBar
            Layout.columnSpan: 2
            value: 0.5
        }

        RadioButton {
            id: radioButton
            text: qsTr("Radio Button")
            checked: true
        }
    }

    Rectangle {
        id: rectangle1
        x: 183
        y: -86
        width: 200
        height: 100
        color: "#514e4e"
        anchors.right: parent.right
        anchors.rightMargin: -80
        anchors.bottom: parent.top
        anchors.bottomMargin: 0
        rotation: 45
    }
}
