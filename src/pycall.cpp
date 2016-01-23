/* Zested, an offline editor for Zeste de Savoir
Copyright (C) 2015-2016 Luthaf - Licence MIT */
#include <cassert>

#include <boost/python.hpp>
namespace py = boost::python;
#include <Python.h>

#include "pycall.hpp"

//! Python main module
static py::object __main__ = py::object();
//! Python main module global variables
static py::object __globals__ = py::object();
//! Parse and get traceback for a Python exception
static std::string python_exception();

void init_python(const char* libpath, const char* name) {
    assert(!Py_IsInitialized());
    Py_SetPythonHome(const_cast<char*>(libpath));
    Py_SetProgramName(const_cast<char*>(name));
    Py_Initialize();

    __main__ = py::import("__main__");
    __globals__ = __main__.attr("__dict__");
}

void finish_python() {
    Py_Finalize();
}

std::string call_python(const std::string& module, const std::string& function, const std::string& arg) {
    try {
        auto mod = py::import(py::str(module));
        auto func = mod.attr(py::str(function));
        auto res = func(arg);
        return py::extract<std::string>(res);
    } catch (const py::error_already_set&) {
        throw PythonError(python_exception());
    }
}

std::string python_exception() {
    PyObject *type_ptr = nullptr, *value_ptr = nullptr, *traceback_ptr = nullptr;
    PyErr_Fetch(&type_ptr, &value_ptr, &traceback_ptr);
    auto ret = std::string("Unfetchable Python error");

    if(type_ptr != nullptr){
        auto h_type = py::handle<>(type_ptr);
        py::extract<std::string> e_type_pstr{py::str(h_type)};
        if(e_type_pstr.check()) {
            ret = e_type_pstr();
        } else {
            ret = "Unknown exception type";
        }
    }

    if(value_ptr != nullptr){
        auto h_val = py::handle<>(value_ptr);
        py::extract<std::string> returned{py::str(h_val)};
        if(returned.check()) {
            ret +=  ": " + returned();
        } else {
            ret += ": Unparseable Python error: ";
        }
    }

    if(traceback_ptr != nullptr){
        auto h_tb = py::handle<>(traceback_ptr);
        py::object tb(py::import("traceback"));
        py::object fmt_tb(tb.attr("format_tb"));
        py::object tb_list(fmt_tb(h_tb));
        py::object tb_str(py::str("\n").join(tb_list));
        py::extract<std::string> returned(tb_str);
        if(returned.check()) {
            ret += ": " + returned();
        } else {
            ret += ": Unparseable Python traceback";
        }
    }
    return ret;
}
