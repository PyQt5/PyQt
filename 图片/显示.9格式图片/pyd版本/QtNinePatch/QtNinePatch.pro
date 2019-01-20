#-------------------------------------------------
#
# Project created by QtCreator 2018-10-25T14:12:10
#
#-------------------------------------------------

QT       += core axcontainer gui

#greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = QtNinePatch
TEMPLATE = lib
CONFIG += release
CONFIG += warn_off exceptions_off hide_symbols

#CONFIG += staticlib
#CONFIG += dll static release

DESTDIR = build
DLLDESTDIR = build

DEFINES += QTNINEPATCHLIB_LIBRARY

SOURCES += QtNinePatch.cpp

HEADERS += QtNinePatch.h

unix {
    target.path = /usr/lib
    INSTALLS += target
}

DEFINES += _XKEYCHECK_H

INCLUDEPATH += .
INCLUDEPATH += $$[QT_INSTALL_HEADERS]

LIBS += -L$$[QT_INSTALL_LIBS]
