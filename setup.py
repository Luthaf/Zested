"""
This is a setup.py script for freezing the app
    py2app is used on OsX
    py2exe is used on Windows
"""
import sys
import os

from setuptools import setup, find_packages
from zested import __version__

options = {
    'name': "Zested",
    'author': "Luthaf",
    'author_email': "luthaf@luthaf.fr",
    'license': "MIT",
    'version': __version__,

    'install_requires': ["PySide", "pygments", "markdown"],
    'dependency_links': ['http://github.com/Luthaf/Python-ZMarkdown/archive/master-zds.zip#egg=markdown'],

    'packages': find_packages(),
    'include_package_data': True,

    'entry_points': {
        'gui_scripts': [
            "zested = zested.main:main",
        ],
    },
}

py2app_options = {
    'argv_emulation': True,
    'includes': ["PySide.QtXml"],
    'packages': ["xml", "markdown", "pygments"],
    'iconfile': "zested/assets/img/clem.icns",
}

py2exe_options = {
    'includes': ["PySide.QtXml"],
    'packages': ["xml", "markdown", "pygments"],
    'dist_dir': os.path.join(os.path.dirname(__file__), "dist", "windows"),
    'excludes': ['_ssl'],
    'bundle_files': 3, # Should be keeped, needed by PySide
}

if sys.argv[1] == "py2app":
     options.update(dict(
         setup_requires=['py2app'],
         install_requires=None,
         data_files=["zested/assets"],
         include_package_data=False,
         app=["Zested.py"],
         options={"py2app": py2app_options},
     ))

elif sys.argv[1] == "py2exe":
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
         windows=[{
            "script": "Zested.py",
            "icon_resources": [(1, os.path.join("assets", "assets", "img", "clem.ico"))]
         }],
         zipfile="zested.zip",
         install_requires=None,
         include_package_data=False,
         data_files=py2exe_data_files,
         options={"py2exe": py2exe_options},
     ))


setup(**options)
