import json
import os

from PySide import QtGui


class TutorialPart:
    '''
    A Tutorial is a recursive structure of TutorialPart.
    '''

    def __init__(self, title, path, have_intro=False, have_conclu=False):
        self.title = title
        self.path = path
        self.have_introduction = have_intro
        self.have_conclusion = have_conclu
        self.children = []

    def __str__(self):
        return self.title

    def append(self, other):
        self.children.append(other)

    @property
    def conclusion(self):
        if self.have_conclusion:
            return os.path.join(self.path, "conclusion.md")
        else:
            return None

    @property
    def introduction(self):
        if self.have_introduction:
            return os.path.join(self.path, "introduction.md")
        else:
            return None


def tutorial_from_manifest(path):
    with open(path, encoding="utf8") as fd:
        manifest = json.load(fd)

    base_path = os.path.dirname(path)
    tutorial = TutorialPart(manifest["title"], base_path, True, True)

    if manifest["type"] == "BIG":
        tutorial = load_big_tuto(tutorial, manifest)
    elif manifest["type"] == "MINI":
        tutorial = load_mini_tuto(tutorial, manifest)

    return tutorial


def load_big_tuto(tutorial, manifest):
    for part in manifest["parts"]:
        tuto_part = TutorialPart(
            part["title"], os.path.join(
                tutorial.path,
                os.path.dirname(part["introduction"])),
            True, True)
        for chapter in part["chapters"]:
            tuto_chapter = TutorialPart(
                chapter["title"], os.path.join(
                    tutorial.path,
                    os.path.dirname(chapter["introduction"])),
                True, True)
            for extract in chapter["extracts"]:
                tuto_chapter.append(TutorialPart(
                    extract["title"], os.path.join(
                        tutorial.path,
                        extract["text"])))
            tuto_part.append(tuto_chapter)
        tutorial.append(tuto_part)
    return tutorial


def load_mini_tuto(tutorial, manifest):
    for extract in manifest["chapter"]["extracts"]:
        tutorial.append(
            TutorialPart(
                extract["title"],
                os.path.join(tutorial.path, extract["text"])
            )
        )
    return tutorial


def render_tutorial(tutorial, widget, callback):
    '''
    Render a tutorial class to the tree view widget

    The callback function is called when an item is double clicked
    '''
    content = widget.findChild(QtGui.QWidget, "tutorial_content")
    content.clear()
    create_tutorial_tree_view(content.invisibleRootItem(), tutorial, root=True)

    title = widget.findChild(QtGui.QWidget, "tutorial_title")
    MAX_TUTO_TITLE_LENGHT = 32

    content.itemDoubleClicked.connect(callback)

    if len(tutorial.title) > MAX_TUTO_TITLE_LENGHT:
        title.setText(tutorial.title[:MAX_TUTO_TITLE_LENGHT] + "…")
    else:
        title.setText(tutorial.title)


class TutorialItem(QtGui.QTreeWidgetItem):
    '''
    A TutorialItem hold the tutorial item file path and title
    '''

    def __init__(self, path, title):
        super().__init__()
        self.path = path
        self.title = title


def create_tutorial_tree_view(widget, section, root=False):
    '''
    Recusive function to render the tutorial class
    '''

    if not root:
        child = TutorialItem(section.path, section.title)
        widget.addChild(child)
        child.setText(0, str(section))

    root_widget = child if not root else widget

    if section.introduction is not None:
        child = TutorialItem(
            section.introduction,
            "Introduction — " + section.title
        )
        root_widget.addChild(child)
        child.setText(0, "Introduction")

    for child_section in section.children:
        create_tutorial_tree_view(root_widget, child_section)

    if section.conclusion is not None:
        child = TutorialItem(
            section.conclusion,
            "Conclusion — " + section.title
        )
        root_widget.addChild(child)
        child.setText(0, "Conclusion")
