from pyqt_openai import COLUMN_TO_EXCLUDE_FROM_SHOW_HIDE_CHAT, \
    DB_NAME_REGEX, \
    MAXIMUM_MESSAGES_IN_PARAMETER_RANGE
from pyqt_openai.config_loader import CONFIG_MANAGER
from pyqt_openai.widgets.checkBoxListWidget import CheckBoxListWidget

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QComboBox, QGridLayout, QFormLayout, QLineEdit, QCheckBox, QSizePolicy, \
    QVBoxLayout, QHBoxLayout, QGroupBox, QSplitter, QLabel, QWidget, QSpinBox

from pyqt_openai.models import ImagePromptContainer, ChatThreadContainer, SettingsParamsContainer


class GeneralSettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.apikey_openai = CONFIG_MANAGER.get_general_property('apikey_openai')
        self.apikey_anthro = CONFIG_MANAGER.get_general_property('apikey_anthro')
        self.baseurl_openai = CONFIG_MANAGER.get_general_property('baseurl_openai')
        self.baseurl_anthro = CONFIG_MANAGER.get_general_property('baseurl_anthro')
        self.db = CONFIG_MANAGER.get_general_property('db')
        self.do_not_ask_again = CONFIG_MANAGER.get_general_property('do_not_ask_again')
        self.notify_finish = CONFIG_MANAGER.get_general_property('notify_finish')
        self.show_toolbar = CONFIG_MANAGER.get_general_property('show_toolbar')
        self.show_secondary_toolbar = CONFIG_MANAGER.get_general_property('show_secondary_toolbar')
        self.chat_column_to_show = CONFIG_MANAGER.get_general_property('chat_column_to_show')
        self.maximum_messages_in_parameter = CONFIG_MANAGER.get_general_property('maximum_messages_in_parameter')
        self.show_as_markdown = CONFIG_MANAGER.get_general_property('show_as_markdown')
        self.run_at_startup = CONFIG_MANAGER.get_general_property('run_at_startup')

    def __initUi(self):
        # General

        # API KEYS

        self.__leOpenAIAPIKey = QLineEdit()
        self.__leOpenAIAPIKey.setPlaceholderText('Your OpenAI API Key...')
        self.__leOpenAIAPIKey.setText( self.apikey_openai)

        self.__leAnthroAPIKey = QLineEdit()
        self.__leAnthroAPIKey.setPlaceholderText('Your Anthropic API Key...')
        self.__leAnthroAPIKey.setText( self.apikey_anthro )

        self.__leOpenAIBaseUrl = QLineEdit()
        self.__leOpenAIBaseUrl.setPlaceholderText('OpenAI API proxy base url...')
        self.__leOpenAIBaseUrl.setText( self.baseurl_openai)

        self.__leAnthroBaseUrl = QLineEdit()
        self.__leAnthroBaseUrl.setPlaceholderText('Anthropic API proxy base url...')
        self.__leAnthroBaseUrl.setText( self.baseurl_anthro)
    
        layout = QGridLayout()

        layout.addWidget( QLabel("OpenAI key"), 0, 0 )
        layout.addWidget( self.__leOpenAIAPIKey, 0, 1 )

        layout.addWidget( QLabel("Anthropic key"), 1, 0 )
        layout.addWidget( self.__leAnthroAPIKey, 1, 1 )

        layout.addWidget( QLabel("OpenAI API base url"), 2, 0 )
        layout.addWidget( self.__leOpenAIBaseUrl, 2, 1 )

        layout.addWidget( QLabel("Anthropic API base url"), 3, 0 )
        layout.addWidget( self.__leAnthroBaseUrl, 3, 1 )


        grpboxAPIKeys = QGroupBox('API keys')
        grpboxAPIKeys.setLayout( layout )

        # Database setting
        dbLayout = QHBoxLayout()
        self.__dbLineEdit = QLineEdit(self.db)
        self.__validator = QRegularExpressionValidator()
        re = QRegularExpression(DB_NAME_REGEX)
        self.__validator.setRegularExpression(re)
        self.__dbLineEdit.setValidator(self.__validator)

        dbLayout.addWidget(QLabel("Name of target database (without extension)"))
        dbLayout.addWidget(self.__dbLineEdit)

        # Checkboxes
        self.__doNotAskAgainCheckBox = QCheckBox(f'{"Do not ask again when closing"} ({"Always close the application"})')
        self.__doNotAskAgainCheckBox.setChecked(self.do_not_ask_again)

        self.__notifyFinishCheckBox = QCheckBox("Notify when finish processing any task (Conversion, etc.)")
        self.__notifyFinishCheckBox.setChecked(self.notify_finish)
        self.__showToolbarCheckBox = QCheckBox("Show Toolbar")
        self.__showToolbarCheckBox.setChecked(self.show_toolbar)
        self.__showSecondaryToolBarChkBox = QCheckBox('Show Secondary Toolbar')
        self.__showSecondaryToolBarChkBox.setChecked(self.show_secondary_toolbar)

        lay = QVBoxLayout()
        lay.addLayout(dbLayout)
        lay.addWidget(self.__doNotAskAgainCheckBox)
        lay.addWidget(self.__notifyFinishCheckBox)
        lay.addWidget(self.__showToolbarCheckBox)
        lay.addWidget(self.__showSecondaryToolBarChkBox)

        generalGrpBox = QGroupBox('General')
        generalGrpBox.setLayout(lay)

        # Chat Browser

        self.__maximumMessagesInParameterSpinBox = QSpinBox()
        self.__maximumMessagesInParameterSpinBox.setRange(*MAXIMUM_MESSAGES_IN_PARAMETER_RANGE)
        self.__maximumMessagesInParameterSpinBox.setValue(self.maximum_messages_in_parameter)

        self.__show_as_markdown = QCheckBox('Show as Markdown')
        self.__show_as_markdown.setChecked(self.show_as_markdown)

        lay = QFormLayout()
        lay.addRow('Maximum Messages in Parameter', self.__maximumMessagesInParameterSpinBox)
        lay.addRow(self.__show_as_markdown)

        chatBrowserGrpBox = QGroupBox('Chat Browser')
        chatBrowserGrpBox.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(grpboxAPIKeys)
        lay.addWidget(generalGrpBox)
        lay.addWidget(chatBrowserGrpBox)

        self.setLayout(lay)

    def getParam(self):
        return {
            "apikey_openai": self.__leOpenAIAPIKey.text(),
            "apikey_anthro": self.__leAnthroAPIKey.text(),
            "baseurl_openai": self.__leOpenAIBaseUrl.text(),
            "baseurl_anthro": self.__leAnthroBaseUrl.text(),

            "db": self.__dbLineEdit.text(),
            "do_not_ask_again": self.__doNotAskAgainCheckBox.isChecked(),
            "notify_finish": self.__notifyFinishCheckBox.isChecked(),
            "show_toolbar": self.__showToolbarCheckBox.isChecked(),
            "show_secondary_toolbar": self.__showSecondaryToolBarChkBox.isChecked(),
            "maximum_messages_in_parameter": self.__maximumMessagesInParameterSpinBox.value(),
            "show_as_markdown": self.__show_as_markdown.isChecked(),
        }
