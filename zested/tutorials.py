# -*- coding: utf-8 -*-

import json
import os
from codecs import open
from markdown import Markdown
from markdown.extensions.zds import ZdsExtension
from zested.smileys import smileys

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


class Extract(object):
    '''
    An extract is the basic structure of a tutorial, an contains mardown text
    only.

    Attributes:
        - title: the extract title;
        - path: the mardown file path;
        - md: the mardown text;
        - html: the HTML version of the mardown text;
        - uptodate: a boolean encoding wether the file is uptodate with the
                    `md` content or not.
    '''

    def __init__(self, title, path):
        self.title = title
        self.path = path
        with open(self.path, encoding="utf8") as fd:
            self.md = fd.read()
        self.html = ""
        self.render()
        self.updodate = True

    def save(self):
        '''Save the mardown text to the corresponding file'''
        with open(path, "w", encoding="utf8") as fd:
            fd.write(self.md)
        self.uptodate = True

    def render(self):
        '''Render the markdown text to HTML'''
        converter = Markdown(**MARKDOWN_OPTIONS)
        self.html = converter.convert(self.md)

    def update(self, new_text):
        '''Set the markdown text to `new_text`'''
        self.md = new_text
        self.uptodate = False

    def navbar(self):
        '''Create the HTML navigation bar corresponding to this extract'''
        return '<a href="{link}">{title}</a>'.format(
                                                link=self.title,
                                                title=self.title)


class Section(object):
    '''
    A tutorial section contains extracts, and can have an introduction, a
    conclusion and some children, these children being extracts or sections.

    A full tutorial is represented by it's root Section.

    Attributes:
        - title: the section title;
        - path: the directory containing the section data;
        - introduction: the section introduction, if applicable
        - conclusion: tyhe section conclusion, if applicable
        - children: the section content.
    '''

    def __init__(self, title, path, intro=None, conclusion=None):
        self.title = title
        self.path = path
        self.introduction = intro
        self.conclusion = conclusion
        self.children = []

    def append(self, other):
        self.children.append(other)

    def navbar(self):
        '''Create the HTML navigation bar corresponding to this section'''
        res = '<ul>'
        if self.introduction:
            res += '<li>' + self.introduction.navbar() + '</li>'
        if self.children:
            for child in self.children:
                res += "<li>" + child.navbar() + "</li>"
        if self.conclusion:
            res += '<li>' + self.conclusion.navbar() + '</li>'
        res += '</ul>'
        return res


def load(path):
    '''
    Read a `manifest.json` file and create the corresponding tutorial object.
    '''
    with open(path, encoding="utf8") as fd:
        manifest = json.load(fd)

    ROOT_PATH = os.path.dirname(path)
    title = manifest["title"]
    introduction = Extract(
                    "Introduction — " + title,
                    os.path.join(ROOT_PATH, manifest["introduction"])
                    )
    conclusion = Extract(
                    "Conclusion — " + title,
                    os.path.join(ROOT_PATH, manifest["conclusion"])
                    )
    tutorial = Section(title, ROOT_PATH, introduction, conclusion)

    if manifest["type"] == "BIG":
        tutorial = _load_big_tuto(tutorial, manifest)
    elif manifest["type"] == "MINI":
        tutorial = _load_mini_tuto(tutorial, manifest)

    return tutorial


def _load_big_tuto(tutorial, manifest):
    for part in manifest["parts"]:
        title = part["title"]
        introduction = Extract(
                        "Introduction — " + title,
                        os.path.join(tutorial.path, part["introduction"])
                        )
        conclusion = Extract(
                        "Conclusion — " + title,
                        os.path.join(tutorial.path, part["conclusion"])
                        )
        tuto_part = Section(title,
                            os.path.join(
                                tutorial.path,
                                os.path.dirname(part["conclusion"])),
                            introduction,
                            conclusion)
        for chapter in part["chapters"]:
            title = chapter["title"]
            introduction = Extract(
                            "Introduction — " + title,
                            os.path.join(tutorial.path, part["introduction"])
                            )
            conclusion = Extract(
                            "Conclusion — " + title,
                            os.path.join(tutorial.path, part["conclusion"])
                            )
            tuto_chapter = Section(
                                title,
                                os.path.join(
                                    tutorial.path,
                                    os.path.dirname(chapter["introduction"])
                                ),
                                introduction,
                                conclusion)
            for extract in chapter["extracts"]:
                tuto_chapter.append(
                    Extract(extract["title"],
                            os.path.join(tutorial.path, extract["text"]))
                )
            tuto_part.append(tuto_chapter)
        tutorial.append(tuto_part)
    return tutorial


def _load_mini_tuto(tutorial, manifest):
    for extract in manifest["chapter"]["extracts"]:
        tutorial.append(
            Extract(
                extract["title"],
                os.path.join(tutorial.path, extract["text"])
            )
        )
    return tutorial
