from markdown import Markdown
from markdown.extensions.zds import ZdsExtension
from zested.smileys import smileys

from PySide import QtCore

ZDS_EXTENSION_CONFIG = {
    "inline": False,
    "emoticons": smileys
}

MARKDOWN_OPTIONS = {
    "extensions": [ZdsExtension(ZDS_EXTENSION_CONFIG)],
    "safe_mode": 'escape',
    "inline": False,
    "enable_attributes": False,
    "smart_emphasis": True,
    "lazy_ol": True,
}


class MarkdownRenderThread(QtCore.QThread):
    done = QtCore.Signal()

    def __init__(self, text, css):
        QtCore.QThread.__init__(self)
        self.text = text
        self.css = css

    def run(self):
        md = Markdown(**MARKDOWN_OPTIONS)

        self.html = '<style type="text/css">'
        self.html += self.css
        self.html += '</style>'

        self.html += md.convert(self.text)
        self.done.emit()
