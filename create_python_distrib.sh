#!/bin/bash

case $(uname -s) in
        Darwin)
            echo "MacOSX"
            ;;
        Linux)
            echo "Linux"
            ;;
        *)
            echo "Unknwown OS"
            exit 1
esac
exit

CONDA=$(pwd)/bin/conda
$CONDA install -y conda
$CONDA remove -y conda-env markdown tk yaml

rm -rf conda-meta envs pkgs share ssl include
find . -name "*.a" -delete
cd bin
rm -f 2to3 conda easy_install markdown_py pydoc python2 python2.7-config tclsh8.5 activate conda-env easy_install-2.7 openssl python2-config smtpd.py wheel c_rehash deactivate idle pip python-config python2.7 sqlite3 wish8.5

