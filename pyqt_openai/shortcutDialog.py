from PySide6.QtWidgets import QLabel, QFormLayout, QGroupBox, QDialog

from pyqt_openai import DEFAULT_SHORTCUT_FIND_PREV, DEFAULT_SHORTCUT_FIND_NEXT, DEFAULT_SHORTCUT_PROMPT_BEGINNING, \
    DEFAULT_SHORTCUT_PROMPT_ENDING, DEFAULT_SHORTCUT_SUPPORT_PROMPT_COMMAND, DEFAULT_SHORTCUT_FULL_SCREEN, \
    DEFAULT_SHORTCUT_FIND, DEFAULT_SHORTCUT_JSON_MODE, DEFAULT_SHORTCUT_LEFT_SIDEBAR_WINDOW, \
    DEFAULT_SHORTCUT_RIGHT_SIDEBAR_WINDOW, DEFAULT_SHORTCUT_CONTROL_PROMPT_WINDOW, DEFAULT_SHORTCUT_SETTING, \
    DEFAULT_SHORTCUT_SEND, DEFAULT_SHORTCUT_SHOW_TOOLBAR, DEFAULT_SHORTCUT_SHOW_SECONDARY_TOOLBAR, DEFAULT_SHORTCUT_FOCUS_MODE


class ShortcutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__shortcuts = {
            'SHORTCUT_FIND_PREV': {'label': f"{'Find'} - {'Previous'}", 'value': DEFAULT_SHORTCUT_FIND_PREV},
            'SHORTCUT_FIND_NEXT': {'label': f"{'Find'} - {'Next'}", 'value': DEFAULT_SHORTCUT_FIND_NEXT},
            'SHORTCUT_PROMPT_BEGINNING': {'label': 'Prompt Beginning', 'value': DEFAULT_SHORTCUT_PROMPT_BEGINNING},
            'SHORTCUT_PROMPT_ENDING': {'label': 'Prompt Ending', 'value': DEFAULT_SHORTCUT_PROMPT_ENDING},
            'SHORTCUT_SUPPORT_PROMPT_COMMAND': {'label': 'Support Prompt Command', 'value': DEFAULT_SHORTCUT_SUPPORT_PROMPT_COMMAND},
            'SHORTCUT_SHOW_TOOLBAR': {'label': 'Show Toolbar', 'value': DEFAULT_SHORTCUT_SHOW_TOOLBAR},
            'SHOW_SECONDARY_TOOLBAR': {'label': 'Show Secondary Toolbar', 'value': DEFAULT_SHORTCUT_SHOW_SECONDARY_TOOLBAR },
            'SHORTCUT_FOCUS_MODE': {'label': 'Focus Mode', 'value': DEFAULT_SHORTCUT_FOCUS_MODE},
            'SHORTCUT_FULL_SCREEN': {'label': 'Full Screen', 'value': DEFAULT_SHORTCUT_FULL_SCREEN},
            'SHORTCUT_FIND': {'label': 'Find', 'value': DEFAULT_SHORTCUT_FIND},
            'SHORTCUT_JSON_MODE': {'label': 'JSON Mode', 'value': DEFAULT_SHORTCUT_JSON_MODE},
            'SHORTCUT_LEFT_SIDEBAR_WINDOW': {'label': 'Left Sidebar Window', 'value': DEFAULT_SHORTCUT_LEFT_SIDEBAR_WINDOW},
            'SHORTCUT_RIGHT_SIDEBAR_WINDOW': {'label': 'Right Sidebar Window', 'value': DEFAULT_SHORTCUT_RIGHT_SIDEBAR_WINDOW},
            'SHORTCUT_CONTROL_PROMPT_WINDOW': {'label': 'Control Prompt Window', 'value': DEFAULT_SHORTCUT_CONTROL_PROMPT_WINDOW},
            'SHORTCUT_SETTING': {'label': 'Setting', 'value': DEFAULT_SHORTCUT_SETTING},
            'SHORTCUT_SEND': {'label': 'Send', 'value': DEFAULT_SHORTCUT_SEND},
        }
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('Shortcuts')

        lay = QFormLayout()

        shortcutGroupBox = QGroupBox('Shortcuts')
        shortcutGroupBox.setLayout(lay)

        for key, shortcut in self.__shortcuts.items():
            lineEdit = QLabel()
            lineEdit.setText(shortcut['value'])
            shortcut['lineEdit'] = lineEdit
            lay.addRow(shortcut['label'], lineEdit)

        self.setLayout(lay)