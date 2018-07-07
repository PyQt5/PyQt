import QtQuick 2.0

Rectangle {
    width: 320; height: 240
    color: "lightblue"
    Text {
        id: txt
        text: "Clicked me"
        font.pixelSize: 20
        anchors.centerIn: parent
    }
    MouseArea {
        id: mouse_area
        anchors.fill: parent  // 有效区域
        onClicked: {
           con.outputString("Hello, Python3") //QML显式的调用Python函数   
        }
    }
}