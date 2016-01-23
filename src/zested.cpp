/* Zested, an offline editor for Zeste de Savoir
Copyright (C) 2015-2016 Luthaf - Licence MIT */
#include <QApplication>
#include <QFile>
#include <QUiLoader>

#include "zested.hpp"
#include "pycall.hpp"

Zested::Zested(): QWidget(nullptr),
                  DATAROOT((QCoreApplication::applicationDirPath() + "/" + RESOURCES_PATH).toStdString()) {
    init_python(DATAROOT.c_str(), "zested");
    switch_ui(":/ui/home.ui");
}

Zested::~Zested() {
    finish_python();
}

void Zested::switch_ui(const std::string& path) {
    QFile file(QString(path.c_str()));
    file.open(QFile::ReadOnly);
    QUiLoader loader;
    QWidget *new_ui = loader.load(&file, this);
    if (new_ui == nullptr) {
        throw ZestedError("Could not load ui file at: " + path);
    }
    new_ui->show();
}
