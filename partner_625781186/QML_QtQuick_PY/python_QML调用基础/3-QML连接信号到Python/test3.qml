import QtQuick 2.0
 
Rectangle {
    id: root
    width: 320; height: 240
    color: "lightgray"
    signal sendClicked(string str) // 定义信号
 
    Text {
        id: txt
        text: "Clicked me"
        font.pixelSize: 20
        anchors.centerIn: parent
    }
    MouseArea {
        id: mouse_area
        anchors.fill: parent  //有效区域
        onClicked: {
            root.sendClicked("Hello, Python3")//发射信号到Python        
        }
    }
}