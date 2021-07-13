"""
Created on 2018年1月30日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: CalendarQssStyle
@description: 日历美化样式
"""
import sys

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QTextCharFormat, QBrush, QColor
    from PyQt5.QtWidgets import QApplication, QCalendarWidget
except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QTextCharFormat, QBrush, QColor
    from PySide2.QtWidgets import QApplication, QCalendarWidget

StyleSheet = """
/*顶部导航区域*/
#qt_calendar_navigationbar {
    background-color: rgb(0, 188, 212);
    min-height: 100px;
}


/*上一个月按钮和下一个月按钮(从源码里找到的objectName)*/
#qt_calendar_prevmonth, #qt_calendar_nextmonth {
    border: none; /*去掉边框*/
    margin-top: 64px;
    color: white;
    min-width: 36px;
    max-width: 36px;
    min-height: 36px;
    max-height: 36px;
    border-radius: 18px; /*看来近似椭圆*/
    font-weight: bold; /*字体加粗*/
    qproperty-icon: none; /*去掉默认的方向键图片，当然也可以自定义*/
    background-color: transparent;/*背景颜色透明*/
}
#qt_calendar_prevmonth {
    qproperty-text: "<"; /*修改按钮的文字*/
}
#qt_calendar_nextmonth {
    qproperty-text: ">";
}
#qt_calendar_prevmonth:hover, #qt_calendar_nextmonth:hover {
    background-color: rgba(225, 225, 225, 100);
}
#qt_calendar_prevmonth:pressed, #qt_calendar_nextmonth:pressed {
    background-color: rgba(235, 235, 235, 100);
}


/*年,月控件*/
#qt_calendar_yearbutton, #qt_calendar_monthbutton {
    color: white;
    margin: 18px;
    min-width: 60px;
    border-radius: 30px;
}
#qt_calendar_yearbutton:hover, #qt_calendar_monthbutton:hover {
    background-color: rgba(225, 225, 225, 100);
}
#qt_calendar_yearbutton:pressed, #qt_calendar_monthbutton:pressed {
    background-color: rgba(235, 235, 235, 100);
}


/*年份输入框*/
#qt_calendar_yearedit {
    min-width: 50px;
    color: white;
    background: transparent;/*让输入框背景透明*/
}
#qt_calendar_yearedit::up-button { /*往上的按钮*/
    width: 20px;
    subcontrol-position: right;/*移动到右边*/
}
#qt_calendar_yearedit::down-button { /*往下的按钮*/
    width: 20px;
    subcontrol-position: left; /*移动到左边去*/
}


/*月份选择菜单*/
CalendarWidget QToolButton QMenu {
     background-color: white;
}
CalendarWidget QToolButton QMenu::item {
    padding: 10px;
}
CalendarWidget QToolButton QMenu::item:selected:enabled {
    background-color: rgb(230, 230, 230);
}
CalendarWidget QToolButton::menu-indicator {
    /*image: none;去掉月份选择下面的小箭头*/
    subcontrol-position: right center;/*右边居中*/
}


/*下方的日历表格*/
#qt_calendar_calendarview {
    outline: 0px;/*去掉选中后的虚线框*/
    selection-background-color: rgb(0, 188, 212); /*选中背景颜色*/
}
"""


class CalendarWidget(QCalendarWidget):

    def __init__(self, *args, **kwargs):
        super(CalendarWidget, self).__init__(*args, **kwargs)
        # 隐藏左边的序号
        self.setVerticalHeaderFormat(self.NoVerticalHeader)

        # 修改周六周日颜色

        fmtGreen = QTextCharFormat()
        fmtGreen.setForeground(QBrush(Qt.green))
        self.setWeekdayTextFormat(Qt.Saturday, fmtGreen)

        fmtOrange = QTextCharFormat()
        fmtOrange.setForeground(QBrush(QColor(252, 140, 28)))
        self.setWeekdayTextFormat(Qt.Sunday, fmtOrange)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    w = CalendarWidget()
    w.show()
    sys.exit(app.exec_())
