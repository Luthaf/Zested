import os

from PySide import QtCore, QtGui, QtUiTools

from zested.gui.loader import UiLoader
from zested.gui import ZestedTextEditor

from zested import IMG_DIR, UI_DIR
from zested.tutorial import tutorial_from_manifest, render_tutorial

from zested import ressources


APP_STATES = {
    "home": "home.ui",
    "editor": "editor.ui"
}

CUSTOM_WIDGETS = [ZestedTextEditor]

CONNECTIONS = {
    "actionOuvrir": "load_tutorial",
    "actionFermer": "close_tab",
    "actionEnregistrer": "save_tab",
}

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super().__init__()

        # Load main ui
        loader = UiLoader(self)
        loader.load_ui("main.ui")

        self.connect_actions()

        # Set windows informations
        self.setWindowIcon(QtGui.QIcon(os.path.join(IMG_DIR, 'clem.png')))
        self.setWindowTitle("ZestEd")

        # Load default state
        self.change_state("home")

        # Set tutorial tree view width
        tutorial = self.findChild(QtGui.QWidget, "tutorial")
        rect = tutorial.frameRect()
        rect.setWidth(350)
        tutorial.setFrameRect(rect)

        self.showMaximized()
        self.raise_()

    def connect_actions(self):
        for action_name, slot in CONNECTIONS.items():
            action = self.findChild(QtGui.QAction, action_name)
            action.triggered.connect(getattr(self, slot))

    def change_state(self, state):
        self.state = state
        content = self.findChild(QtGui.QWidget, "content")
        layout = content.layout()

        # Remove old widgets in content
        for i in range(layout.count()):
            b = layout.takeAt(i)
            b.widget().deleteLater()

        ui_filename = os.path.join(UI_DIR, APP_STATES[state])
        loader = QtUiTools.QUiLoader()

        for widget in CUSTOM_WIDGETS:
            loader.registerCustomWidget(widget)

        new_state = loader.load(ui_filename, content)
        content.layout().addWidget(new_state)

    def load_tutorial(self):
        # Get filepath. Should be a manifest.json file
        home_dir = os.getenv('USERPROFILE') or os.getenv('HOME')
        path, _ = QtGui.QFileDialog.getOpenFileName(self, 'Ouvir un tutoriel (fichier manifest.json)', home_dir)
        tutorial_widget = self.findChild(QtGui.QWidget, "tutorial")
        # Create the tutorial instance
        self.tutorial = tutorial_from_manifest(path)
        # Render the tutorial instance
        render_tutorial(self.tutorial, tutorial_widget, self.open_extract)

        self.setWindowTitle("ZestEd — " + self.tutorial.title)

    def open_extract(self, extract):
        if self.state != "editor":
            self.change_state("editor")

        editor = self.findChild(ZestedTextEditor)
        editor.load_extract(extract)

    def close_tab(self):
        editor = self.findChild(ZestedTextEditor)
        editor.remove_current_tab()

    def save_tab(self):
        editor = self.findChild(ZestedTextEditor)
        editor.save_current_tab()

