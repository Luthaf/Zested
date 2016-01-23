from PySide import QtCore, QtUiTools
import os

from zested import UI_DIR


class UiLoader(QtUiTools.QUiLoader):

    def __init__(self, baseinstance):
        super().__init__()
        self.baseinstance = baseinstance

    def createWidget(self, class_name, parent=None, name=''):
        if parent is None and self.baseinstance:
            # supposed to create the top-level widget, return the base instance
            # instead
            return self.baseinstance
        else:
            # create a new widget for child widgets
            widget = super(UiLoader, self).createWidget(
                class_name,
                parent,
                name
            )
            if self.baseinstance:
                # set an attribute for the new child widget on the base
                # instance, just like PyQt4.uic.loadUi does.
                setattr(self.baseinstance, name, widget)
            return widget

    def load_ui(self, path):
        filename = os.path.join(UI_DIR, path)
        widget = self.load(filename)
        QtCore.QMetaObject.connectSlotsByName(widget)
        return widget
