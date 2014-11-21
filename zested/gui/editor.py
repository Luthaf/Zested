import os

from markdown import Markdown
from markdown.extensions.zds import ZdsExtension

from PySide import QtGui, QtUiTools, QtCore

from zested import UI_DIR, CSS_DIR
from zested.gui.smileys import smileys

ZDS_EXTENSION_CONFIG = {
    "inline": False,
    "emoticons": smileys
}

RENDER_INTERVAL = 500

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
        self.can_render = True
        self.delayed_rendering = False

        with open(os.path.join(CSS_DIR, "main.css")) as fd:
            self.css = fd.read()

        with open(os.path.join(CSS_DIR, "pygments.css")) as fd:
            self.css += fd.read()

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
        '''
        Create a new tab, and set it's content to the extract file
        content.
        '''
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
        '''
        Remove the tab at the index `index`
        '''
        widget = self.widget(index)
        self.removeTab(index)
        widget.deleteLater()

    def remove_current_tab(self):
        '''
        Remove the current tab
        '''
        index = self.tabBar().currentIndex()
        self.remove_tab(index)

    def save_current_tab(self):
        '''
        Save the current tab's editor content to the associated file
        '''
        text = self.current_editor.toPlainText()
        with open(self.current_tab.filepath, "w") as fd:
            fd.write(text)

    def update_preview(self):
        '''
        Main logic to update preview: if possible, a new thread is started.
        Then, we wait for the thread to finish, and terminate it if it's take
        too long.
        '''
        if self.can_render:
            self._switch_can_render()
            QtCore.QTimer.singleShot(RENDER_INTERVAL, self._switch_can_render)
        else:
            self._delay_rendering()
            return None

        self.render_thread = MarkdownRenderThread(
                                self.current_editor.toPlainText(),
                                self.css
                                )
        self.render_thread.start()
        self.render_thread.done.connect(self.render_preview)

        self.render_thread.wait(3/4*RENDER_INTERVAL)
        #TODO: log this
        self.render_thread.terminate()

    def _switch_can_render(self):
        '''
        Flip the self.can_render attribute.
        '''
        self.can_render = not self.can_render

    def render_preview(self):
        '''
        Effectively update the preview panel.
        '''
        vscroll_bar = self.current_viewer.verticalScrollBar()
        hscroll_bar = self.current_viewer.horizontalScrollBar()
        vscroll = vscroll_bar.value()
        hscroll = hscroll_bar.value()
        self.current_viewer.setText(self.render_thread.html)
        vscroll_bar.setValue(vscroll)
        hscroll_bar.setValue(hscroll)

        self.delayed_rendering = False

    def _delay_rendering(self):
        '''
        Delay markdown rendering if there is no already delayed rendering
        '''
        if not self.delayed_rendering:
            QtCore.QTimer.singleShot(2*RENDER_INTERVAL, self.update_preview)
            self.delayed_rendering = True

class MarkdownRenderThread(QtCore.QThread):
    done = QtCore.Signal()

    def __init__(self, text, css):
        QtCore.QThread.__init__(self)
        self.text = text
        self.css = css

    def run(self):
        self.html = '<style type="text/css">'
        self.html += self.css
        self.html += '</style>'

        self.html += md.convert(self.text)
        self.done.emit()
