class WigglyWidget : QWidget
{
%TypeHeaderCode
#include "wigglywidget.h"
%End

public:
    WigglyWidget(QWidget *parent /TransferThis/ = 0);

public slots:
    void setText(const QString &newText);

protected:
    virtual void paintEvent(QPaintEvent *);
    virtual void timerEvent(QTimerEvent *);
};
