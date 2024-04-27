#include <QApplication>

#include "wigglywidget.h"

int main(int argc, char *argv[]) {
  QApplication a(argc, argv);
  WigglyWidget w;
  w.setText("pyqt.site");
  w.show();
  return a.exec();
}
