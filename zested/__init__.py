from os import path
import sys

if hasattr(sys, "frozen") and sys.frozen == "macosx_app":
    DATA_DIR = path.abspath(path.join(path.dirname(__file__), "..", "..", "..", "assets"))
elif hasattr(sys, "frozen") and sys.platform == "win32":
    DATA_DIR = path.join(path.dirname(sys.executable), "assets")
else:
    DATA_DIR = path.abspath(path.join(path.dirname(__file__), "assets"))

# Define base dir variables
UI_DIR = path.join(DATA_DIR, "ui")
IMG_DIR = path.join(DATA_DIR, "img")
CSS_DIR = path.join(DATA_DIR, "css")
SMILEY_DIR = path.join(DATA_DIR, "smileys")
DICT_DIR = path.join(DATA_DIR, "dict")
TRANS_DIR = path.join(DATA_DIR, "translations")

__version__ = "0.3"
