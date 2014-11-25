import os

from PySide import QtCore, QtGui, QtUiTools

from zested.gui.loader import UiLoader
from zested.gui import ZestedTextEditor, ZestedEditorTab

from zested import IMG_DIR, UI_DIR
from zested.tutorial import tutorial_from_manifest, render_tutorial

from zested import ressources


APP_STATES = {
    "home": {
        "file": "home.ui",
        "connections": [
            ("openTutorial.clicked", "_load_recent_tutorial"),
        ],
    },
    "editor": {
        "file": "editor.ui",
    },
}

CUSTOM_WIDGETS = [ZestedEditorTab, ZestedTextEditor]

ACTIONS_CONNECTIONS = {
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
        self.setWindowTitle("ZestEd")

        self.connect_actions()

        # Load default state
        self.change_state("home")

        self._get_recent_files_list()

        self.showMaximized()
        # Set tutorial tree view width
        splitter = self.findChild(QtGui.QWidget, "splitter")
        splitter.setSizes([150, sum(splitter.sizes()) - 150])

        self.raise_()

    def connect_actions(self):
        for action_name, slot in ACTIONS_CONNECTIONS.items():
            action = self.findChild(QtGui.QAction, action_name)
            action.triggered.connect(getattr(self, slot))

    def change_state(self, state):
        state_data = APP_STATES[state]
        self.state = state
        content = self.findChild(QtGui.QWidget, "content")
        layout = content.layout()

        # Remove old widgets in content
        for i in range(layout.count()):
            b = layout.takeAt(i)
            b.widget().deleteLater()

        ui_filename = os.path.join(UI_DIR, state_data["file"])
        loader = QtUiTools.QUiLoader()

        for widget in CUSTOM_WIDGETS:
            loader.registerCustomWidget(widget)

        new_state = loader.load(ui_filename, content)
        content.layout().addWidget(new_state)

        for signal, slot in state_data.get("connections", []):
            signal_widget_name, signal_function = signal.split(".")
            signal_widget = self.findChild(QtGui.QWidget, signal_widget_name)
            getattr(signal_widget, signal_function).connect(getattr(self, slot))

    def load_tutorial(self):
        # Get filepath. Should be a manifest.json file
        home_dir = os.getenv('USERPROFILE') or os.getenv('HOME')
        path, _ = QtGui.QFileDialog.getOpenFileName(self,
                    'Ouvir un tutoriel (fichier manifest.json)',
                    home_dir)
        if not path.endswith("manifest.json"):
            return None
        self._load_tutorial_from_path(path)

    def _load_tutorial_from_path(self, path):
        tutorial_widget = self.findChild(QtGui.QWidget, "tutorial")
        # Create the tutorial instance
        self.tutorial = tutorial_from_manifest(path)

        if self.tutorial.title not in self.recent_tutorials.keys():
            self.recent_tutorials[self.tutorial.title] = path
            settings = QtCore.QSettings()
            settings.setValue("recent_tutorials", self.recent_tutorials)

        # Render the tutorial instance
        render_tutorial(self.tutorial, tutorial_widget, self.open_extract)

        self.setWindowTitle("ZestEd — " + self.tutorial.title)

    def _load_recent_tutorial(self):
        select = self.findChild(QtGui.QWidget, "selectRecentTutorial")
        name = select.currentText()
        try:
            return self._load_tutorial_from_path(self.recent_tutorials[name])
        except KeyError:
            return self.load_tutorial()

    def open_extract(self, extract):
        if self.state != "editor":
            self.change_state("editor")

        editor = self.findChild(ZestedEditorTab)
        editor.load_extract(extract)

    def close_tab(self):
        editor = self.findChild(ZestedEditorTab)
        editor.remove_current_tab()

    def save_tab(self):
        editor = self.findChild(ZestedEditorTab)
        editor.save_current_tab()

    def _get_recent_files_list(self):
        settings = QtCore.QSettings()
        self.recent_tutorials = settings.value("recent_tutorials", {})

        if self.state == "home":
            select = self.findChild(QtGui.QWidget, "selectRecentTutorial")
            select.clear()
            for name in self.recent_tutorials.keys():
                select.addItem(name)
            select.addItem("Nouveau tutoriel ...")

        recents_tuto_menu = self.findChild(QtGui.QWidget, "menuTutorielsRecents")
        recents_tuto_menu.clear()

        for name in self.recent_tutorials.keys():
            action = QtGui.QAction(name, self)
            action.setData(self.recent_tutorials[name])
            action.triggered.connect(self._load_tutorial_from_menu)
            recents_tuto_menu.addAction(action)

    def _load_tutorial_from_menu(self):
        action = self.sender()
        self._load_tutorial_from_path(action.data())
