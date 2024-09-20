from functools import partial

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QScrollArea, QWidget, QTabWidget, QGridLayout

from pyqt_openai.config_loader import CONFIG_MANAGER
from pyqt_openai.gpt_widget.right_sidebar.chatPage import ChatPage


class GPTRightSideBarWidget(QScrollArea):
    onDirectorySelected = Signal(str)
    onToggleJSON = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initUi()

    def __initUi(self):
        tabWidget = QTabWidget()

        chatPage = ChatPage()

        tabWidget.addTab(chatPage, 'GPT', )

        chatPage.onToggleJSON.connect(self.onToggleJSON)

        lay = QGridLayout()
        lay.addWidget(tabWidget)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setWidget(mainWidget)
        self.setWidgetResizable(True)

        self.setStyleSheet('QScrollArea { border: 0 }')

    def __tabChanged(self, idx):
        CONFIG_MANAGER.set_general_property('TAB_IDX', idx)
