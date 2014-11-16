import os

from markdown import Markdown
from markdown.extensions.zds import ZdsExtension

from PySide import QtGui, QtUiTools

from zested import UI_DIR, CSS_DIR
from zested.gui.smileys import smileys

ZDS_EXTENSION_CONFIG = {
    "inline": False,
    "emoticons": smileys
}

md = Markdown(extensions=[ZdsExtension(ZDS_EXTENSION_CONFIG)],
              safe_mode = 'escape',
              inline = False,
              enable_attributes = False,
              smart_emphasis = True,
              lazy_ol = True,
)

class ZestedTextEditor(QtGui.QTabWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.tabCloseRequested.connect(self.remove_tab)

    @property
    def current_tab(self):
        return self.widget(self.tabBar().currentIndex())

    @property
    def current_editor(self):
        return self.current_tab.findChild(QtGui.QWidget, "text_editor")

    @property
    def current_viewer(self):
        return self.current_tab.findChild(QtGui.QWidget, "viewer")

    def load_extract(self, extract):
        if os.path.isdir(extract.path):
            return None

        tab = self.new_tab(extract.path, extract.title)
        self.current_editor.textChanged.connect(self.update_preview)

        with open(extract.path) as fd:
            self.current_editor.setPlainText(fd.read())

    def new_tab(self, path, title=""):
        '''
        Create an empty new tab
        '''
        ui_filename = os.path.join(UI_DIR, "editor_tab.ui")
        loader = QtUiTools.QUiLoader()
        tab = loader.load(ui_filename, self)

        tab.filepath = path

        self.addTab(tab, title)
        self.setCurrentWidget(tab)
        return tab

    def remove_tab(self, index):
        widget = self.widget(index)
        self.removeTab(index)
        widget.deleteLater()

    def remove_current_tab(self):
        index = self.tabBar().currentIndex()
        self.remove_tab(index)

    def save_current_tab(self):
        text = self.current_editor.toPlainText()
        with open(self.current_tab.filepath, "w") as fd:
            fd.write(text)

    def update_preview(self):
        html = md.convert(self.current_editor.toPlainText())
        self.current_viewer.setText(html)

