/* Zested, an offline editor for Zeste de Savoir
Copyright (C) 2015-2016 Luthaf - Licence MIT */

#ifndef ZESTED_PYTHON_HPP
#define ZESTED_PYTHON_HPP

#include <string>

struct PythonError: public std::runtime_error {
    PythonError(std::string err): std::runtime_error(err) {}
};

//! Initialize all Python-related state. `libpath` is the path to
//! PYTHONHOME, the standard python library being at `PYTHONHOME/lib/python2.7`.
//! `name` is the name of the main program (`argv[0]`).
void init_python(const char* libpath, const char* name);

//! Call a python `function` in the `module` with `arg` as argument.
//! This will throw a `PythonError` in case of Python exception.
std::string call_python(const std::string& module, const std::string& function, const std::string& arg);

//! Terminate python interpreter.
void finish_python();

#endif
