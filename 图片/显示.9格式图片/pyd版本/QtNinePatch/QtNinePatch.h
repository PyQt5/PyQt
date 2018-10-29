#ifndef QTNINEPATCH_H
#define QTNINEPATCH_H

#include <QtCore/qglobal.h>

#if defined(QTNINEPATCHLIB_LIBRARY)
#  define QTNINEPATCHLIBSHARED_EXPORT Q_DECL_EXPORT
#else
#  define QTNINEPATCHLIBSHARED_EXPORT Q_DECL_IMPORT
#endif

#include <QImage>
#include <QPixmap>
#include <QPainter>
#include <vector>

class QtNinePatch;

class QTNINEPATCHLIBSHARED_EXPORT QtNinePatch
{

public:
    static QPixmap createPixmapFromNinePatchImage(const QImage &, int, int);
};

#endif // QTNINEPATCH_H
