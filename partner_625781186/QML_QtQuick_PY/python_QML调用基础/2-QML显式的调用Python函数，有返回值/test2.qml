import QtQuick 2.0

Rectangle {
    id: root
    width: 320; height: 240
    color: "lightgray"
    Text {
        id: txt
        text: "Clicked me"
        font.pixelSize: 20
        anchors.centerIn: parent
    }
    Text {
        id: txt1
        text: "..."
        font.pixelSize: 20
    }
    MouseArea {
        id: mouse_area
        anchors.fill: parent  // 有效区域
        onClicked: {
            console.log("test...")  // 控制台打印信息
            txt1.text = con.returnValue(20) //QML显式的调用Python函数    
        }
    }
}