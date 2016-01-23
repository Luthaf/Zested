/* Zested, an offline editor for Zeste de Savoir
Copyright (C) 2015-2016 Luthaf - Licence MIT */
#include <QApplication>
#include "zested.hpp"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    Zested zested;
    zested.show();

    return app.exec();
}
