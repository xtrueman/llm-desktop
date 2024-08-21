from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import QWidget, QDoubleSpinBox, QSpinBox, QFormLayout, QSizePolicy, QComboBox, QTextEdit, \
    QLabel, QVBoxLayout, QCheckBox, QPushButton, QScrollArea, QGroupBox

from pyqt_openai import DEFAULT_SHORTCUT_JSON_MODE, OPENAI_TEMPERATURE_RANGE, OPENAI_TEMPERATURE_STEP, \
    MAX_TOKENS_RANGE, TOP_P_RANGE, TOP_P_STEP, FREQUENCY_PENALTY_RANGE, PRESENCE_PENALTY_STEP, PRESENCE_PENALTY_RANGE, \
    FREQUENCY_PENALTY_STEP
from pyqt_openai.config_loader import CONFIG_MANAGER
from pyqt_openai.lang.translations import LangClass
from pyqt_openai.pyqt_openai_data import get_chat_model, init_llama
from pyqt_openai.util.script import getSeparator


class ChatPage(QWidget):
    onToggleLlama = Signal(bool)
    onToggleJSON = Signal(bool)

    def __init__(self):
        super().__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__stream = CONFIG_MANAGER.get_general_property('stream')
        self.__model = CONFIG_MANAGER.get_general_property('model')
        self.__system = CONFIG_MANAGER.get_general_property('system')
        self.__temperature = CONFIG_MANAGER.get_general_property('temperature')
        self.__max_tokens = CONFIG_MANAGER.get_general_property('max_tokens')
        self.__top_p = CONFIG_MANAGER.get_general_property('top_p')
        self.__frequency_penalty = CONFIG_MANAGER.get_general_property('frequency_penalty')
        self.__presence_penalty = CONFIG_MANAGER.get_general_property('presence_penalty')
        self.__json_object = CONFIG_MANAGER.get_general_property('json_object')

        self.__use_max_tokens = CONFIG_MANAGER.get_general_property('use_max_tokens')
        self.__use_llama_index = CONFIG_MANAGER.get_general_property('use_llama_index')

    def __initUi(self):
        systemlbl = QLabel(LangClass.TRANSLATIONS['System'])

        self.__systemTextEdit = QTextEdit()
        self.__systemTextEdit.setText(self.__system)
        self.__systemTextEdit.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        saveSystemBtn = QPushButton(LangClass.TRANSLATIONS['Save System'])
        saveSystemBtn.clicked.connect(self.__saveSystem)

        modelCmbBox = QComboBox()
        modelCmbBox.addItems(get_chat_model())
        modelCmbBox.setCurrentText(self.__model)
        modelCmbBox.currentTextChanged.connect(self.__modelChanged)

        advancedSettingsScrollArea = QScrollArea()

        self.__temperatureSpinBox = QDoubleSpinBox()
        self.__temperatureSpinBox.setRange(*OPENAI_TEMPERATURE_RANGE)
        self.__temperatureSpinBox.setAccelerated(True)
        self.__temperatureSpinBox.setSingleStep(OPENAI_TEMPERATURE_STEP)
        self.__temperatureSpinBox.setValue(self.__temperature)
        self.__temperatureSpinBox.valueChanged.connect(self.__valueChanged)

        self.__maxTokensSpinBox = QSpinBox()
        self.__maxTokensSpinBox.setRange(*MAX_TOKENS_RANGE)
        self.__maxTokensSpinBox.setAccelerated(True)
        self.__maxTokensSpinBox.setValue(self.__max_tokens)
        self.__maxTokensSpinBox.valueChanged.connect(self.__valueChanged)

        self.__toppSpinBox = QDoubleSpinBox()
        self.__toppSpinBox.setRange(*TOP_P_RANGE)
        self.__toppSpinBox.setAccelerated(True)
        self.__toppSpinBox.setSingleStep(TOP_P_STEP)
        self.__toppSpinBox.setValue(self.__top_p)
        self.__toppSpinBox.valueChanged.connect(self.__valueChanged)

        self.__frequencyPenaltySpinBox = QDoubleSpinBox()
        self.__frequencyPenaltySpinBox.setRange(*FREQUENCY_PENALTY_RANGE)
        self.__frequencyPenaltySpinBox.setAccelerated(True)
        self.__frequencyPenaltySpinBox.setSingleStep(FREQUENCY_PENALTY_STEP)
        self.__frequencyPenaltySpinBox.setValue(self.__frequency_penalty)
        self.__frequencyPenaltySpinBox.valueChanged.connect(self.__valueChanged)

        self.__presencePenaltySpinBox = QDoubleSpinBox()
        self.__presencePenaltySpinBox.setRange(*PRESENCE_PENALTY_RANGE)
        self.__presencePenaltySpinBox.setAccelerated(True)
        self.__presencePenaltySpinBox.setSingleStep(PRESENCE_PENALTY_STEP)
        self.__presencePenaltySpinBox.setValue(self.__presence_penalty)
        self.__presencePenaltySpinBox.valueChanged.connect(self.__valueChanged)

        useMaxTokenChkBox = QCheckBox()
        useMaxTokenChkBox.toggled.connect(self.__useMaxChecked)
        useMaxTokenChkBox.setChecked(self.__use_max_tokens)
        useMaxTokenChkBox.setText(LangClass.TRANSLATIONS['Use Max Tokens'])

        self.__maxTokensSpinBox.setEnabled(self.__use_max_tokens)

        lay = QFormLayout()

        lay.addRow(useMaxTokenChkBox)
        lay.addRow('temperature', self.__temperatureSpinBox)
        lay.addRow('maxTokens', self.__maxTokensSpinBox)
        lay.addRow('topp', self.__toppSpinBox)
        lay.addRow('frequencyPenalty', self.__frequencyPenaltySpinBox)
        lay.addRow('presencePenalty', self.__presencePenaltySpinBox)

        paramWidget = QWidget()
        paramWidget.setLayout(lay)

        advancedSettingsScrollArea.setWidgetResizable(True)
        advancedSettingsScrollArea.setWidget(paramWidget)

        lay = QVBoxLayout()
        lay.addWidget(advancedSettingsScrollArea)

        advancedSettingsGrpBox = QGroupBox(LangClass.TRANSLATIONS['Advanced Settings'])
        advancedSettingsGrpBox.setLayout(lay)

        streamChkBox = QCheckBox()
        streamChkBox.setChecked(self.__stream)
        streamChkBox.toggled.connect(self.__streamChecked)
        streamChkBox.setText(LangClass.TRANSLATIONS['Stream'])

        jsonChkBox = QCheckBox()
        jsonChkBox.setChecked(self.__json_object)
        jsonChkBox.toggled.connect(self.__jsonObjectChecked)

        jsonChkBox.setText(LangClass.TRANSLATIONS['Enable JSON mode'])
        jsonChkBox.setShortcut(DEFAULT_SHORTCUT_JSON_MODE)
        jsonChkBox.setToolTip(LangClass.TRANSLATIONS['When enabled, you can send a JSON object to the API and the response will be in JSON format. Otherwise, it will be in plain text.'])

        llamaChkBox = QCheckBox()
        llamaChkBox.setChecked(self.__use_llama_index)
        llamaChkBox.toggled.connect(self.__use_llama_indexChecked)
        llamaChkBox.setText(LangClass.TRANSLATIONS['Use LlamaIndex'])

        sep = getSeparator('horizontal')

        lay = QVBoxLayout()
        lay.addWidget(systemlbl)
        lay.addWidget(self.__systemTextEdit)
        lay.addWidget(saveSystemBtn)
        lay.addWidget(modelCmbBox)
        lay.addWidget(streamChkBox)
        lay.addWidget(jsonChkBox)
        lay.addWidget(llamaChkBox)
        lay.addWidget(sep)
        lay.addWidget(advancedSettingsGrpBox)
        lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(lay)

    def __saveSystem(self):
        self.__system = self.__systemTextEdit.toPlainText()
        CONFIG_MANAGER.set_general_property('system', self.__system)

    def __modelChanged(self, v):
        self.__model = v
        CONFIG_MANAGER.set_general_property('model', v)

    def __streamChecked(self, f):
        self.__stream = f
        CONFIG_MANAGER.set_general_property('stream', f)

    def __jsonObjectChecked(self, f):
        self.__json_object = f
        CONFIG_MANAGER.set_general_property('json_object', f)
        self.onToggleJSON.emit(f)

    def __use_llama_indexChecked(self, f):
        self.__use_llama_index = f
        CONFIG_MANAGER.set_general_property('use_llama_index', f)
        if f:
            # Set llama index directory if it exists
            init_llama()
        self.onToggleLlama.emit(f)

    def __useMaxChecked(self, f):
        self.__use_max_tokens = f
        CONFIG_MANAGER.set_general_property('use_max_tokens', f)
        self.__maxTokensSpinBox.setEnabled(f)

    def __valueChanged(self, v):
        sender = self.sender()
        if sender == self.__temperatureSpinBox:
            self.__temperature = v
            CONFIG_MANAGER.set_general_property('temperature', v)
        elif sender == self.__maxTokensSpinBox:
            self.__max_tokens = v
            CONFIG_MANAGER.set_general_property('max_tokens', v)
        elif sender == self.__toppSpinBox:
            self.__top_p = v
            CONFIG_MANAGER.set_general_property('top_p', v)
        elif sender == self.__frequencyPenaltySpinBox:
            self.__frequency_penalty = v
            CONFIG_MANAGER.set_general_property('frequency_penalty', v)
        elif sender == self.__presencePenaltySpinBox:
            self.__presence_penalty = v
            CONFIG_MANAGER.set_general_property('presence_penalty', v)
