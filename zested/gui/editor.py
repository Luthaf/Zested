import os
import urllib.request
import time

from PySide import QtGui, QtUiTools, QtCore

from zested import UI_DIR, CSS_DIR
from zested.render import MarkdownRenderThread
from zested.highlight import MarkdownHighlighter
from zested.gui.messages import SaveModifiedMessage

RENDER_INTERVAL = 500

class ZestedEditorTab(QtGui.QTabWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.tabCloseRequested.connect(self.remove_tab)
        self.can_render = True
        self.delayed_rendering = False
        self._read_css()

    def _read_css(self):
        with open(os.path.join(CSS_DIR, "main.css"), encoding="utf8") as fd:
            self.css = fd.read()
        with open(os.path.join(CSS_DIR, "pygments.css"), encoding="utf8") as fd:
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
        Load an extract and fill a tab with it, or set the extract tab active
        if it is aleready loaded.
        '''
        # Container directories
        if os.path.isdir(extract.path):
            return None

        # Check if the tab already exists
        all_tabs = self.findChildren(QtGui.QWidget, "editor_tab")
        for tab in all_tabs:
            if tab.filepath == extract.path:
                self.setCurrentWidget(tab)
                return None

        tab = self.new_tab(extract.path, extract.title)
        self.current_editor.textChanged.connect(self.update_preview)

        with open(extract.path, encoding="utf8") as fd:
            self.current_editor.setPlainText(fd.read())

        self.current_editor.textChanged.connect(self.warning_updated)

    def new_tab(self, path, title=""):
        '''
        Create a new empty tab
        '''
        ui_filename = os.path.join(UI_DIR, "editor_tab.ui")
        loader = QtUiTools.QUiLoader()
        tab = loader.load(ui_filename, self)

        tab.filepath = path
        tab.updated = False

        self.addTab(tab, title)
        self.setCurrentWidget(tab)

        document = tab.findChild(QtGui.QPlainTextEdit).document()
        tab.highlighter = MarkdownHighlighter(document)

        return tab

    def remove_tab(self, index):
        '''
        Remove the tab at the index `index`
        '''
        tab = self.widget(index)
        if tab is None:
            return None

        if tab.updated:
            message = SaveModifiedMessage()
            ret = message.exec_()
            if ret == message.Save:
                current = self.tabBar().currentIndex()
                self.setCurrentWidget(tab)
                self.save_current_tab()
                if current > index:
                    self.setCurrentWidget(self.widget(current - 1))
                else:
                    self.setCurrentWidget(self.widget(current))
            elif ret == message.Discard:
                pass
            elif ret == message.Cancel:
                return "Canceled"
            else:
                return None

        self.removeTab(index)
        tab.deleteLater()

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
        with open(self.current_tab.filepath, "w", encoding="utf8") as fd:
            fd.write(text)
        if self.current_tab.updated:
            self._flip_updated()

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

    def warning_updated(self):
        '''
        Add a little star if the content of the tab changed, and switch the
        current_tab.updated attribute to True
        '''
        if not self.current_tab.updated:
            self._flip_updated()

    def _flip_updated(self):
        '''
        Flip the updated state: tab attribute and tab title
        '''
        tab_bar = self.tabBar()
        index = tab_bar.currentIndex()

        if not self.current_tab.updated:
            # Add star
            tab_bar.setTabText(index, tab_bar.tabText(index) + "*")
        else:
            # Remove star
            tab_bar.setTabText(index, tab_bar.tabText(index)[:-1])
        # Flip attribute
        self.current_tab.updated = not self.current_tab.updated


class ZestedTextEditor(QtGui.QTextBrowser):

    def loadResource(self, type, name):
        zds_domain = "http://zestedesavoir.com"
        if type == QtGui.QTextDocument.ImageResource:
            image_url = name.toString()
            if image_url.startswith("http"):
                local_path = self._download_image(image_url)
            elif image_url.startswith("/") and not os.path.isfile(image_url):
                # relatives URL
                local_path = self._download_image(zds_domain + image_url)
            else:
                local_path = name.toLocalFile()
            return QtGui.QImage(local_path)
        return super().loadResource(type, name)

    def _download_image(self, image_url):
        '''
        Download a network image to a local temporary directory.

        If the file already exists and is less old than 24h, reuse-it
        '''
        image_path = os.path.join(*image_url.split("/")[3:])
        tmpdir = QtCore.QDir.tempPath()

        filepath = os.path.join(tmpdir,
                                "zested" + time.strftime("%d-%m-%y"),
                                image_path)

        if os.path.isfile(filepath):
            return filepath

        filedir = os.path.dirname(filepath)
        os.makedirs(filedir, exist_ok=True)

        image = open(filepath, "wb")

        image_on_network = urllib.request.urlopen(image_url)
        while True:
            buf = image_on_network.read(65536)
            if len(buf) == 0:
                break
            image.write(buf)

        image.close()
        image_on_network.close()

        return filepath
