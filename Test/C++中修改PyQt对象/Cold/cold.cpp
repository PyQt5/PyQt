#include "cold.h"

void cold(QImage &src, int delta)
{
    int rows = src.height();
    int cols = src.width();
    for (int i = 0; i < rows; i++)
    {
        QRgb *line = (QRgb *)src.scanLine(i);
        for (int j = 0; j < cols; j++)
        {
            int r = qRed(line[j]);
            int g = qGreen(line[j]);
            int b = qBlue(line[j]) + delta;
            b = qBound(0, b, 255);
            src.setPixel(j, i, qRgb(r, g, b));
        }
    }
}
