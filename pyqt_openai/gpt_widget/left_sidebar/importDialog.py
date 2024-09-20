from PySide6.QtCore import Qt
from PySide6.QtWidgets import QButtonGroup, QGroupBox, QRadioButton, QDialogButtonBox, QDialog, QVBoxLayout



class ImportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__selected_import_type = None

    def __initUi(self):
        self.setWindowTitle("Import From...")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)

        self.__generalRadBtn = QRadioButton('General')
        self.__chatGptRadBtn = QRadioButton('ChatGPT')

        self.__generalRadBtn.setChecked(True)

        self.__buttonGroup = QButtonGroup()
        self.__buttonGroup.addButton(self.__generalRadBtn, 1)
        self.__buttonGroup.addButton(self.__chatGptRadBtn, 2)

        lay = QVBoxLayout()
        lay.addWidget(self.__generalRadBtn)
        lay.addWidget(self.__chatGptRadBtn)
        lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        importTypeGrpBox = QGroupBox('Import Type')
        importTypeGrpBox.setLayout(lay)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        lay = QVBoxLayout()
        lay.addWidget(importTypeGrpBox)
        lay.addWidget(buttonBox)

        self.setLayout(lay)

    def getImportType(self):
        selected_button_id = self.__buttonGroup.checkedId()
        if selected_button_id == 1:
            return 'general'
        elif selected_button_id == 2:
            return 'chatgpt'
        else:
            return None