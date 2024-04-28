#ifndef WIGGLYWIDGET_H
#define WIGGLYWIDGET_H

#include <QBasicTimer>
#include <QWidget>

#ifdef Q_OS_WIN
#include <QtCore/qglobal.h>

#if defined(WIGGLYWIDGET_LIBRARY)
#define WIGGLYWIDGET_EXPORT Q_DECL_EXPORT
#else
#define WIGGLYWIDGET_EXPORT
#endif
#endif

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

#endif // WIGGLYWIDGET_H
