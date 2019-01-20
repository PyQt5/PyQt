%Module QtNinePatch
%Import QtCore/QtCoremod.sip
%Import QtGui/QtGuimod.sip

class QtNinePatch
{
%TypeHeaderCode
#include "../QtNinePatch.h"
%End

public:
    static QPixmap createPixmapFromNinePatchImage(const QImage &, int, int);

};