from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QRectF, Qt, QUrl
from PyQt5.QtGui import QColor, QGuiApplication, QPainter, QPen
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtQuick import QQuickPaintedItem, QQuickView


class PieChart(QQuickPaintedItem):

    chartCleared = pyqtSignal()  # 定义信号

    @pyqtProperty(str)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @pyqtProperty(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = QColor(color)

    def __init__(self, parent=None):
        super(PieChart, self).__init__(parent)

        self._name = ''
        self._color = QColor()

    def paint(self, painter):
        painter.setPen(QPen(self._color, 2))
        painter.setRenderHints(QPainter.Antialiasing, True)

        rect = QRectF(0, 0, self.width(), self.height()).adjusted(1, 1, -1, -1)
        painter.drawPie(rect, 90 * 16, 290 * 16)

    @pyqtSlot()
    def clearChart(self):
        self.color = QColor(Qt.transparent)
        self.update()

        self.chartCleared.emit()  # 发射信号


if __name__ == '__main__':
    import os
    import sys

    app = QGuiApplication(sys.argv)

    qmlRegisterType(PieChart, "Charts", 1, 0, "PieChart")

    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.setSource(
        QUrl.fromLocalFile(
            os.path.join(os.path.dirname(__file__), 'test5.qml')))
    view.show()

    sys.exit(app.exec_())
