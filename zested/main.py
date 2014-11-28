#!/usr/bin/env python3
import sys

from PySide import QtGui, QtCore
from zested.gui import MainWindow
from zested import TRANS_DIR

def main():
    app = QtGui.QApplication(sys.argv)
    QtCore.QCoreApplication.setOrganizationName("Zested")
    QtCore.QCoreApplication.setApplicationName("ZestEd")
    translator = QtCore.QTranslator()
    translator.load("qt_fr", TRANS_DIR)
    app.installTranslator(translator)
    main_window = MainWindow()
    sys.exit(app.exec_())
