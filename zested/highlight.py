from PySide import QtGui, QtCore

import os
import re
import hunspell

from zested import DICT_DIR

SpellChecker = hunspell.HunSpell(os.path.join(DICT_DIR, "fr.dic"),
                                 os.path.join(DICT_DIR, "fr.aff"))

class SpellCheckFormat(QtGui.QTextCharFormat):
    '''
    Highligth spell checking error
    '''
    def __init__(self):
        super().__init__()
        self.setUnderlineColor("red")
        self.setUnderlineStyle(self.WaveUnderline)


class MarkdownHighlighter(QtGui.QSyntaxHighlighter):

    def highlightBlock(self, text):
        spellcheck_format = SpellCheckFormat()

        for word in re.finditer("\w+", text):
            if not SpellChecker.spell(word.group()):
                self.setFormat(word.start(),
                               word.end()-word.start(),
                               spellcheck_format)
