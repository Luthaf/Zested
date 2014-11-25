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

entry_point = "ZestEd.py"

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
    'packages': ["xml", "markdown", "pygments"],
    'iconfile': "assets/img/clem.icns",
}

py2exe_options = {
    'includes': ["PySide.QtXml"],
    'packages': ["xml", "markdown", "pygments"],
    'dist_dir': os.path.join(os.path.dirname(__file__), "dist", "windows"),
    'excludes': ['_ssl'],
    'bundle_files': 3, # Should be keeped, needed by PySide
}

if sys.platform == 'darwin':
     options.update(dict(
         setup_requires=['py2app'],
         install_requires=None,
         app=[entry_point],
         options={"py2app": py2app_options},
     ))
elif sys.platform == 'win32':
    import py2exe
    import glob

    if not os.path.exists(py2exe_options['dist_dir']):
        if not os.path.exists("dist"):
            os.mkdir("dist")
        os.mkdir(py2exe_options['dist_dir'])

    py2exe_data_files = [
        ("assets\\" + i, glob.glob("assets\\" + i + "\\*")) for i in ["css", "img", "ui", "smileys"]
    ]

    options.update(dict(
         setup_requires=['py2exe'],
         install_requires=None,
         windows=[{
            "script": entry_point,
            "icon_resources": [(1, os.path.join("assets", "img", "clem.ico"))]
         }],
         zipfile="zested.zip",
         data_files=py2exe_data_files,
         options={"py2exe": py2exe_options},
     ))


setup(**options)
