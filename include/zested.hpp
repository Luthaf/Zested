/* Zested, an offline editor for Zeste de Savoir
Copyright (C) 2015-2016 Luthaf - Licence MIT */
#ifndef ZESTED_ZESTED_HPP
#define ZESTED_ZESTED_HPP

#include <QWidget>

struct ZestedError: public std::runtime_error {
    ZestedError(std::string err): std::runtime_error(err) {}
};

//! Main window for the Zested application
class Zested: public QWidget {
public:
    Zested();
    ~Zested();

    //! Dynamically load the ui `file`
    void switch_ui(const std::string& file);
private:
    const std::string DATAROOT;
};

#endif
