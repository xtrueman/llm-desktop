import requests

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QLabel, QWidget

from pyqt_openai.config_loader import CONFIG_MANAGER
from pyqt_openai.pyqt_openai_data import set_openai_enabled, set_api_key_and_client_global, OPENAI_REQUEST_URL


class ApiWidget(QWidget):
    onAIEnabled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initUi()

    def __initUi(self):
        self.__apiCheckPreviewLbl = QLabel()
        self.__apiCheckPreviewLbl.setFont(QFont('Arial', 10))

        apiLbl = QLabel('OpenAI API Key')

        self.__apiLineEdit = QLineEdit()
        self.__apiLineEdit.setPlaceholderText('Write your OpenAI API Key...')
        self.__apiLineEdit.returnPressed.connect(self.setApi)
        self.__apiLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        apiBtn = QPushButton('Use')
        apiBtn.clicked.connect(self.setApi)

        lay = QHBoxLayout()
        lay.addWidget(apiLbl)
        lay.addWidget(self.__apiLineEdit)
        lay.addWidget(apiBtn)
        lay.addWidget(self.__apiCheckPreviewLbl)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.setLayout(lay)

    def setApiKeyAndClient(self, api_key):
        set_api_key_and_client_global(api_key)

        # for showing to the user
        self.__apiLineEdit.setText(api_key)

    def setApi(self):
        try:
            api_key = self.__apiLineEdit.text()
            response = requests.get(OPENAI_REQUEST_URL, headers={'Authorization': f'Bearer {api_key}'})
            f = set_openai_enabled(response.status_code == 200)
            self.onAIEnabled.emit(f)
            if f:
                self.setApiKeyAndClient(api_key)
                CONFIG_MANAGER.set_general_property('API_KEY', api_key)

                self.__apiCheckPreviewLbl.setStyleSheet("color: {}".format(QColor(0, 200, 0).name()))
                self.__apiCheckPreviewLbl.setText('Valid')
            else:
                raise Exception
        except Exception as e:
            self.__apiCheckPreviewLbl.setStyleSheet("color: {}".format(QColor(255, 0, 0).name()))
            self.__apiCheckPreviewLbl.setText('Invalid!')
            self.onAIEnabled.emit(False)
            print(e)
        finally:
            self.__apiCheckPreviewLbl.show()

    def showApiCheckPreviewLbl(self, f):
        self.__apiCheckPreviewLbl.show() if f else self.__apiCheckPreviewLbl.hide()