from PySide import QtGui

import os
import re

HAVE_HUNSPELL = False
try:
    import hunspell
    HAVE_HUNSPELL = True
except ImportError:
    pass

from zested import DICT_DIR

if HAVE_HUNSPELL:
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

        if HAVE_HUNSPELL:
            for word in re.finditer("\w+", text):
                if not SpellChecker.spell(word.group()):
                    self.setFormat(word.start(),
                                   word.end()-word.start(),
                                   spellcheck_format)
