#!/usr/bin/env python3
import sys

from PySide import QtGui, QtCore
from zested.gui import MainWindow


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    QtCore.QCoreApplication.setOrganizationName("Zested")
    QtCore.QCoreApplication.setApplicationName("ZestEd")
    main_window = MainWindow()
    sys.exit(app.exec_())
