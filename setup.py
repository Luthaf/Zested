"""
This is a setup.py script for freezing the app
    py2app is used on OsX
    py2exe is used on Windows
"""
import sys
import os
from setuptools import setup

from zested import __version__

with open("Requirements.txt") as fd:
    requirements = [r.strip() for r in fd.readlines()]

entry_point = "main.py"

options = {
    'name': "ZestEd",
    'author': "Luthaf",
    'author_email': "luthaf@luthaf.fr",
    'license': "MIT",
    'version': __version__,

    'install_requires': requirements,

    'packages': ["zested"],
    'data_files': ["assets"],
}

py2app_options = {
    'argv_emulation': True,
    'includes': ["PySide.QtXml"],
    'packages': ["xml", "markdown"],
    'iconfile': "assets/img/clem.icns",
}

if sys.platform == 'darwin':
     options.update(dict(
         setup_requires=['py2app'],
         install_requires=None,
         app=[entry_point],
         options={"py2app": py2app_options},
     ))
elif sys.platform == 'win32':
    pass
#     options.update(dict(
#         setup_requires=['py2exe'],
#         app=[entry_point],
#     ))


setup(**options)
