#!/usr/bin/env python3
import sys

from PySide import QtGui, QtWebKit
from zested.gui import MainWindow


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
