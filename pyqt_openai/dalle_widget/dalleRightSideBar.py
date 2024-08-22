from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMessageBox, QScrollArea, QWidget, QCheckBox, QSpinBox, QGroupBox, QVBoxLayout, QPushButton, \
    QComboBox, \
    QPlainTextEdit, \
    QFormLayout, QLabel, QRadioButton

from pyqt_openai.config_loader import CONFIG_MANAGER
from pyqt_openai.dalle_widget.dalleThread import DallEThread
from pyqt_openai.lang.translations import LangClass
from pyqt_openai.models import ImagePromptContainer
from pyqt_openai.util.script import getSeparator
from pyqt_openai.widgets.findPathWidget import FindPathWidget
from pyqt_openai.widgets.notifier import NotifierWidget
from pyqt_openai.widgets.toast import Toast


class DallERightSideBarWidget(QScrollArea):
    submitDallE = Signal(ImagePromptContainer)
    submitDallEAllComplete = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__quality = CONFIG_MANAGER.get_dalle_property('quality')
        self.__n = CONFIG_MANAGER.get_dalle_property('n')
        self.__size = CONFIG_MANAGER.get_dalle_property('size')
        self.__directory = CONFIG_MANAGER.get_dalle_property('directory')
        self.__is_save = CONFIG_MANAGER.get_dalle_property('is_save')
        self.__continue_generation = CONFIG_MANAGER.get_dalle_property('continue_generation')
        self.__number_of_images_to_create = CONFIG_MANAGER.get_dalle_property('number_of_images_to_create')
        self.__style = CONFIG_MANAGER.get_dalle_property('style')
        self.__response_format = CONFIG_MANAGER.get_dalle_property('response_format')
        self.__save_prompt_as_text = CONFIG_MANAGER.get_dalle_property('save_prompt_as_text')
        self.__prompt_type = CONFIG_MANAGER.get_dalle_property('prompt_type')
        self.__width = CONFIG_MANAGER.get_dalle_property('width')
        self.__height = CONFIG_MANAGER.get_dalle_property('height')
        self.__prompt = CONFIG_MANAGER.get_dalle_property('prompt')

    def __initUi(self):
        self.__numberOfImagesToCreateSpinBox = QSpinBox()
        self.__promptTypeToShowRadioGrpBox = QGroupBox(LangClass.TRANSLATIONS['Prompt Type To Show'])

        self.__findPathWidget = FindPathWidget()
        self.__findPathWidget.setAsDirectory(True)
        self.__findPathWidget.getLineEdit().setPlaceholderText(LangClass.TRANSLATIONS['Choose Directory to Save...'])
        self.__findPathWidget.getLineEdit().setText(self.__directory)
        self.__findPathWidget.added.connect(self.__setSaveDirectory)

        self.__saveChkBox = QCheckBox(LangClass.TRANSLATIONS['Save After Submit'])
        self.__saveChkBox.setChecked(True)
        self.__saveChkBox.toggled.connect(self.__saveChkBoxToggled)
        self.__saveChkBox.setChecked(self.__is_save)

        self.__continueGenerationChkBox = QCheckBox(LangClass.TRANSLATIONS['Continue Image Generation'])
        self.__continueGenerationChkBox.setChecked(True)
        self.__continueGenerationChkBox.toggled.connect(self.__continueGenerationChkBoxToggled)
        self.__continueGenerationChkBox.setChecked(self.__continue_generation)

        self.__numberOfImagesToCreateSpinBox.setRange(2, 1000)
        self.__numberOfImagesToCreateSpinBox.setValue(self.__number_of_images_to_create)
        self.__numberOfImagesToCreateSpinBox.valueChanged.connect(self.__numberOfImagesToCreateSpinBoxValueChanged)

        self.__savePromptAsTextChkBox = QCheckBox(LangClass.TRANSLATIONS['Save Prompt (Revised) as Text'])
        self.__savePromptAsTextChkBox.setChecked(True)
        self.__savePromptAsTextChkBox.toggled.connect(self.__savePromptAsTextChkBoxToggled)
        self.__savePromptAsTextChkBox.setChecked(self.__save_prompt_as_text)

        self.__normalOne = QRadioButton(LangClass.TRANSLATIONS['Normal'])
        self.__revisedOne = QRadioButton(LangClass.TRANSLATIONS['Revised'])

        if self.__prompt_type == 1:
            self.__normalOne.setChecked(True)
        else:
            self.__revisedOne.setChecked(True)

        self.__normalOne.toggled.connect(self.__promptTypeToggled)
        self.__revisedOne.toggled.connect(self.__promptTypeToggled)

        lay = QVBoxLayout()
        lay.addWidget(self.__normalOne)
        lay.addWidget(self.__revisedOne)
        self.__promptTypeToShowRadioGrpBox.setLayout(lay)

        self.__generalGrpBox = QGroupBox()
        self.__generalGrpBox.setTitle(LangClass.TRANSLATIONS['General'])

        lay = QVBoxLayout()
        lay.addWidget(self.__findPathWidget)
        lay.addWidget(self.__saveChkBox)
        lay.addWidget(self.__continueGenerationChkBox)
        lay.addWidget(self.__numberOfImagesToCreateSpinBox)
        lay.addWidget(self.__savePromptAsTextChkBox)
        lay.addWidget(self.__promptTypeToShowRadioGrpBox)
        self.__generalGrpBox.setLayout(lay)

        self.__qualityCmbBox = QComboBox()
        self.__qualityCmbBox.addItems(['standard', 'hd'])
        self.__qualityCmbBox.setCurrentText(self.__quality)
        self.__qualityCmbBox.currentTextChanged.connect(self.__dalleChanged)

        self.__nSpinBox = QSpinBox()
        self.__nSpinBox.setRange(1, 10)
        self.__nSpinBox.setValue(self.__n)
        self.__nSpinBox.valueChanged.connect(self.__dalleChanged)
        self.__nSpinBox.setEnabled(False)

        self.__sizeLimitLabel = QLabel(LangClass.TRANSLATIONS['※ Images can have a size of 1024x1024, 1024x1792 or 1792x1024 pixels.'])
        self.__sizeLimitLabel.setWordWrap(True)

        self.__widthCmbBox = QComboBox()
        self.__widthCmbBox.addItems(['1024', '1792'])
        self.__widthCmbBox.setCurrentText(str(self.__width))
        self.__widthCmbBox.currentTextChanged.connect(self.__dalleChanged)

        self.__heightCmbBox = QComboBox()
        self.__heightCmbBox.addItems(['1024', '1792'])
        self.__heightCmbBox.setCurrentText(str(self.__height))
        self.__heightCmbBox.currentTextChanged.connect(self.__dalleChanged)

        self.__promptWidget = QPlainTextEdit()
        self.__promptWidget.setPlaceholderText(LangClass.TRANSLATIONS['Enter prompt here...'])
        self.__promptWidget.setPlainText(self.__prompt)
        self.__promptWidget.textChanged.connect(self.__dalleTextChanged)

        self.__styleCmbBox = QComboBox()
        self.__styleCmbBox.addItems(['vivid', 'natural'])
        self.__styleCmbBox.currentTextChanged.connect(self.__dalleChanged)

        self.__submitBtn = QPushButton(LangClass.TRANSLATIONS['Submit'])
        self.__submitBtn.clicked.connect(self.__submit)

        self.__stopGeneratingImageBtn = QPushButton(LangClass.TRANSLATIONS['Stop Generating Image'])
        self.__stopGeneratingImageBtn.clicked.connect(self.__stopGeneratingImage)
        self.__stopGeneratingImageBtn.setEnabled(False)

        paramGrpBox = QGroupBox()
        paramGrpBox.setTitle(LangClass.TRANSLATIONS['Parameters'])

        lay = QFormLayout()
        lay.addRow(LangClass.TRANSLATIONS['Quality'], self.__qualityCmbBox)
        lay.addRow(LangClass.TRANSLATIONS['Total'], self.__nSpinBox)
        lay.addRow(self.__sizeLimitLabel)
        lay.addRow(LangClass.TRANSLATIONS['Width'], self.__widthCmbBox)
        lay.addRow(LangClass.TRANSLATIONS['Height'], self.__heightCmbBox)
        lay.addRow(LangClass.TRANSLATIONS['Style'], self.__styleCmbBox)
        lay.addRow(QLabel(LangClass.TRANSLATIONS['Prompt']))
        lay.addRow(self.__promptWidget)

        paramGrpBox.setLayout(lay)

        sep = getSeparator('horizontal')

        lay = QVBoxLayout()
        lay.addWidget(self.__generalGrpBox)
        lay.addWidget(paramGrpBox)
        lay.addWidget(sep)
        lay.addWidget(self.__submitBtn)
        lay.addWidget(self.__stopGeneratingImageBtn)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setWidget(mainWidget)
        self.setWidgetResizable(True)

    def __dalleChanged(self, v):
        sender = self.sender()
        if sender == self.__qualityCmbBox:
            self.__quality = v
            CONFIG_MANAGER.set_dalle_property('quality', self.__quality)
        elif sender == self.__nSpinBox:
            self.__n = v
            CONFIG_MANAGER.set_dalle_property('n', self.__n)
        elif sender == self.__widthCmbBox:
            if self.__widthCmbBox.currentText() == '1792' and self.__heightCmbBox.currentText() == '1792':
                self.__heightCmbBox.setCurrentText('1024')
            self.__width = v
            CONFIG_MANAGER.set_dalle_property('width', self.__width)
        elif sender == self.__heightCmbBox:
            if self.__widthCmbBox.currentText() == '1792' and self.__heightCmbBox.currentText() == '1792':
                self.__widthCmbBox.setCurrentText('1024')
            self.__height = v
            CONFIG_MANAGER.set_dalle_property('height', self.__height)
        elif sender == self.__styleCmbBox:
            self.__style = v
            CONFIG_MANAGER.set_dalle_property('style', self.__style)

    def __dalleTextChanged(self):
        sender = self.sender()
        if isinstance(sender, QPlainTextEdit):
            if sender == self.__promptWidget:
                self.__prompt = sender.toPlainText()
                CONFIG_MANAGER.set_dalle_property('prompt', self.__prompt)

    def __setSaveDirectory(self, directory):
        self.__directory = directory
        CONFIG_MANAGER.set_dalle_property('directory', self.__directory)

    def __saveChkBoxToggled(self, f):
        self.__is_save = f
        CONFIG_MANAGER.set_dalle_property('is_save', self.__is_save)

    def __continueGenerationChkBoxToggled(self, f):
        self.__continue_generation = f
        CONFIG_MANAGER.set_dalle_property('continue_generation', self.__continue_generation)
        self.__numberOfImagesToCreateSpinBox.setEnabled(f)

    def __numberOfImagesToCreateSpinBoxValueChanged(self, value):
        self.__number_of_images_to_create = value
        CONFIG_MANAGER.set_dalle_property('number_of_images_to_create', self.__number_of_images_to_create)

    def __savePromptAsTextChkBoxToggled(self, f):
        self.__save_prompt_as_text = f
        CONFIG_MANAGER.set_dalle_property('save_prompt_as_text', self.__save_prompt_as_text)

    def __promptTypeToggled(self, f):
        sender = self.sender()
        # Prompt type to show on the image
        # 1 is normal, 2 is revised
        if sender == self.__normalOne:
            self.__prompt_type = 1
            CONFIG_MANAGER.set_dalle_property('prompt_type', self.__prompt_type)
        elif sender == self.__revisedOne:
            self.__prompt_type = 2
            CONFIG_MANAGER.set_dalle_property('prompt_type', self.__prompt_type)

    def __submit(self):
        openai_arg = {
            "model": "dall-e-3",
            "prompt": self.__promptWidget.toPlainText(),
            "n": self.__n,
            "size": f'{self.__width}x{self.__height}',
            'quality': self.__quality,
            "style": self.__style,
            'response_format': self.__response_format,
        }
        number_of_images = self.__number_of_images_to_create if self.__continue_generation else 1

        self.__t = DallEThread(openai_arg, number_of_images)
        self.__t.start()
        self.__t.started.connect(self.__toggleWidget)
        self.__t.replyGenerated.connect(self.__afterGenerated)
        self.__t.errorGenerated.connect(self.__failToGenerate)
        self.__t.finished.connect(self.__toggleWidget)
        self.__t.allReplyGenerated.connect(self.submitDallEAllComplete)

    def __toggleWidget(self):
        f = not self.__t.isRunning()
        self.__generalGrpBox.setEnabled(f)
        self.__qualityCmbBox.setEnabled(f)
        self.__nSpinBox.setEnabled(f)
        self.__widthCmbBox.setEnabled(f)
        self.__heightCmbBox.setEnabled(f)
        self.__submitBtn.setEnabled(f)
        self.__styleCmbBox.setEnabled(f)
        if self.__continue_generation:
            self.__stopGeneratingImageBtn.setEnabled(not f)

    def __stopGeneratingImage(self):
        if self.__t.isRunning():
            self.__t.stop()

    def __failToGenerate(self, event):
        if not self.isVisible() or not self.window().isActiveWindow():
            informative_text = 'Error 😥'
            detailed_text = event
            self.__notifierWidget = NotifierWidget(informative_text=informative_text, detailed_text = detailed_text)
            self.__notifierWidget.show()
            self.__notifierWidget.doubleClicked.connect(self.__bringWindowToFront)
            QMessageBox.critical(self, informative_text, detailed_text)
        else:
            toast = Toast(text=event, parent=self)
            toast.show()

    def __bringWindowToFront(self):
        window = self.window()
        window.showNormal()
        window.raise_()
        window.activateWindow()

    def __afterGenerated(self, arg):
        self.submitDallE.emit(arg)

    def getArgument(self):
        return {
            'prompt': self.__promptWidget.toPlainText(),
            'n': self.__n,
            'size': self.__size,
            'quality': self.__quality,
            'style': self.__style
        }

    def getSavePromptAsText(self):
        return self.__save_prompt_as_text

    def isSavedEnabled(self):
        return self.__is_save

    def getDirectory(self):
        return self.__directory

