#include "QtNinePatch.h"

struct Part {
    bool stretchable;
    int pos;
    int len;
    Part()
        : stretchable(false)
        , pos(0)
        , len(0)
    {
    }
    Part(int pos, int len, bool stretchable)
        : stretchable(stretchable)
        , pos(pos)
        , len(len)
    {
    }
};

static inline bool isStretchableMarker(QRgb pixel)
{
    return (qAlpha(pixel) >> 7) & 1;
}

static QPixmap resize9patch(QImage const &image, int dw, int dh)
{
    int sw = image.width();
    int sh = image.height();
    if (sw > 2 && sh > 2 && dw > 0 && dh > 0) {
        QPixmap pixmap(dw, dh);
        pixmap.fill(Qt::transparent);
        QPainter pr(&pixmap);
        pr.setRenderHint(QPainter::SmoothPixmapTransform);

        std::vector<Part> horz;
        std::vector<Part> vert;
        int horz_stretch = 0;
        int vert_stretch = 0;
        {
            int pos;
            QRgb last;
            QRgb next;
            pos = 0;
            last = image.pixel(1, 0);
            for (int x = 1; x < sw - 1; x++) {
                next = image.pixel(x + 1, 0);
                if (isStretchableMarker(last) != isStretchableMarker(next) || x == sw - 2) {
                    bool stretchable = isStretchableMarker(last);
                    int len = x - pos;
                    horz.push_back(Part(pos, len, stretchable));
                    if (stretchable) horz_stretch += len;
                    last = next;
                    pos = x;
                }
            }
            pos = 0;
            last = image.pixel(0, 1);
            for (int y = 1; y < sh - 1; y++) {
                next = image.pixel(0, y + 1);
                if (isStretchableMarker(last) != isStretchableMarker(next) || y == sh - 2) {
                    bool stretchable = isStretchableMarker(last);
                    int len = y - pos;
                    vert.push_back(Part(pos, len, stretchable));
                    if (stretchable) vert_stretch += len;
                    last = next;
                    pos = y;
                }
            }
        }
        double horz_mul = 0;
        double vert_mul = 0;
        if (horz_stretch > 0) horz_mul = (double)(dw - (sw - 2 - horz_stretch)) / horz_stretch;
        if (vert_stretch > 0) vert_mul = (double)(dh - (sh - 2 - vert_stretch)) / vert_stretch;
        int dy0 = 0;
        int dy1 = 0;
        double vstretch = 0;
        for (int i = 0; i < (int)vert.size(); i++) {
            int sy0 = vert[i].pos;
            int sy1 = vert[i].pos + vert[i].len;
            if (i + 1 == (int)vert.size()) {
                dy1 = dh;
            } else if (vert[i].stretchable) {
                vstretch += (double)vert[i].len * vert_mul;
                double s = floor(vstretch);
                vstretch -= s;
                dy1 += (int)s;
            } else {
                dy1 += vert[i].len;
            }
            int dx0 = 0;
            int dx1 = 0;
            double hstretch = 0;
            for (int j = 0; j < (int)horz.size(); j++) {
                int sx0 = horz[j].pos;
                int sx1 = horz[j].pos + horz[j].len;
                if (j + 1 == (int)horz.size()) {
                    dx1 = dw;
                } else if (horz[j].stretchable) {
                    hstretch += (double)horz[j].len * horz_mul;
                    double s = floor(hstretch);
                    hstretch -= s;
                    dx1 += (int)s;
                } else {
                    dx1 += horz[j].len;
                }
                pr.drawImage(QRect(dx0, dy0, dx1 - dx0, dy1 - dy0), image, QRect(sx0 + 1, sy0 + 1, sx1 - sx0, sy1 - sy0));
                dx0 = dx1;
            }
            dy0 = dy1;
        }

        return pixmap;
    }
    return QPixmap();
}

QPixmap QtNinePatch::createPixmapFromNinePatchImage(const QImage &image, int dw, int dh)
{
    int w = dw;
    int h = dh;
    if (w < image.width() || h < image.height()) { // shrink
        if (w < image.width()) w = image.width();
        if (h < image.height()) h = image.height();
        QPixmap pm1 = resize9patch(image, w, h);
        if (pm1.isNull()) return QPixmap();
        QPixmap pm2(dw, dh);
        pm2.fill(Qt::transparent);
        QPainter pr(&pm2);
        pr.setRenderHint(QPainter::SmoothPixmapTransform);
        pr.drawPixmap(0, 0, dw, dh, pm1, 0, 0, w, h);
        return pm2;
    } else {
        return resize9patch(image, w, h);
    }
}
