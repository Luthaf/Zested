"""
This is a setup.py script for freezing the app
    py2app is used on OsX
    py2exe is used on Windows
"""
import sys

min_version = (3, 2)
if sys.version_info <= min_version:
    print("Please use Python >= 3.2 for this package.")
    sys.exit(1)

from setuptools import setup, find_packages
from zested import __version__

options = {
    'name': "Zested",
    'author': "Luthaf",
    'author_email': "luthaf@luthaf.fr",
    'license': "MIT",
    'version': __version__,

    'install_requires': ["PySide", "pygments", "markdown"],
    'dependency_links': [
        'https://github.com/zestedesavoir/Python-ZMarkdown/archive\
        /master-zds.zip#egg=markdown'
    ],

    'packages': find_packages(),
    'include_package_data': True,

    'entry_points': {
        'gui_scripts': [
            "zested = zested.main:main",
        ],
    },
}

setup(**options)
