#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bottle
from bottle import route, template, static_file
import os

from zested import tutorials

ROOT_DIR = os.path.dirname(__file__)
bottle.TEMPLATE_PATH = [os.path.join(ROOT_DIR, "templates")]


@route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root=os.path.join(ROOT_DIR, "static"))


@route('/')
def index():
    # return template('index', name="bottle")
    p = "/Volumes/Aldith/Documents/Enseignement/Fortran/archive/manifest.json"
    tutorial = tutorials.load(p)
    extract = tutorial.children[0].children[0].children[0]
    return template('editor', tutorial=tutorial, extract=extract)

if __name__ == "__main__":
    bottle.run(host='localhost', port=5000)
