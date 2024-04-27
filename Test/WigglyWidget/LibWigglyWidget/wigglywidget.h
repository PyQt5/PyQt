#ifndef WIGGLYWIDGET_H
#define WIGGLYWIDGET_H

#include <QBasicTimer>
#include <QWidget>

#include "WigglyWidget_global.h"

class WIGGLYWIDGET_EXPORT WigglyWidget : public QWidget {
  Q_OBJECT

 public:
  WigglyWidget(QWidget *parent = nullptr);

 public slots:
  void setText(const QString &newText);

 protected:
  virtual void paintEvent(QPaintEvent *event) override;
  virtual void timerEvent(QTimerEvent *event) override;

 private:
  QBasicTimer timer;
  QString text;
  int step;
};

#endif  // WIGGLYWIDGET_H
