import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QSplitter, \
    QFileDialog, QMessageBox, QPushButton

from pyqt_openai import THREAD_TABLE_NAME, JSON_FILE_EXT_LIST_STR, ICON_SIDEBAR, ICON_SETTING, \
    FILE_NAME_LENGTH, DEFAULT_SHORTCUT_FIND, DEFAULT_SHORTCUT_LEFT_SIDEBAR_WINDOW, \
    DEFAULT_SHORTCUT_RIGHT_SIDEBAR_WINDOW, QFILEDIALOG_DEFAULT_DIRECTORY
from pyqt_openai.config_loader import CONFIG_MANAGER
from pyqt_openai.gpt_widget.center.chatWidget import ChatWidget
from pyqt_openai.gpt_widget.left_sidebar.chatNavWidget import ChatNavWidget
from pyqt_openai.gpt_widget.right_sidebar.gptRightSideBarWidget import GPTRightSideBarWidget
from pyqt_openai.models import ChatThreadContainer, ChatMessageContainer
from pyqt_openai.pyqt_openai_data import DB
from pyqt_openai.util.script import open_directory, get_generic_ext_out_of_qt_ext, message_list_to_txt, \
    conv_unit_to_html, \
    add_file_to_zip, getSeparator
from pyqt_openai.widgets.button import Button


class GPTMainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__notify_finish = CONFIG_MANAGER.get_general_property('notify_finish')

        self.__show_chat_list = CONFIG_MANAGER.get_general_property('show_chat_list')
        self.__show_setting = CONFIG_MANAGER.get_general_property('show_setting')

        self.__background_image = CONFIG_MANAGER.get_general_property('background_image')

        self.__maximum_messages_in_parameter = CONFIG_MANAGER.get_general_property('maximum_messages_in_parameter')

    def __initUi(self):
        self.__chatNavWidget = ChatNavWidget(ChatThreadContainer.get_keys(), THREAD_TABLE_NAME)

        self.__chatWidget = ChatWidget()
        self.__chatWidget.addThread.connect(self.__addThread)
        self.__chatWidget.onMenuCloseClicked.connect(self.__onMenuCloseClicked)

        self.__browser = self.__chatWidget.getChatBrowser()

        self.__gptRightSideBarWidget = GPTRightSideBarWidget()
        self.__gptRightSideBarWidget.onToggleJSON.connect(self.__chatWidget.toggleJSON)


        self.__sideBarBtn = Button()
        self.__sideBarBtn.setStyleAndIcon(ICON_SIDEBAR)
        self.__sideBarBtn.setCheckable(True)
        self.__sideBarBtn.setToolTip('Chat List' + f' ({DEFAULT_SHORTCUT_LEFT_SIDEBAR_WINDOW})')
        self.__sideBarBtn.setChecked(self.__show_chat_list)
        self.__sideBarBtn.toggled.connect(self.toggleSideBar)
        self.__sideBarBtn.setShortcut(DEFAULT_SHORTCUT_LEFT_SIDEBAR_WINDOW)

        self.__settingBtn = Button()
        self.__settingBtn.setStyleAndIcon(ICON_SETTING)
        self.__settingBtn.setToolTip(
            'Chat Settings' + f' ({DEFAULT_SHORTCUT_RIGHT_SIDEBAR_WINDOW})')
        self.__settingBtn.setCheckable(True)
        self.__settingBtn.setChecked(self.__show_setting)
        self.__settingBtn.toggled.connect(self.toggleSetting)
        self.__settingBtn.setShortcut(DEFAULT_SHORTCUT_RIGHT_SIDEBAR_WINDOW)

        sep = getSeparator('vertical')

        self.__toggleFindToolButton = QPushButton('Show Find Tool')
        self.__toggleFindToolButton.setCheckable(True)
        self.__toggleFindToolButton.setChecked(False)
        self.__toggleFindToolButton.toggled.connect(self.__chatWidget.toggleMenuWidget)
        self.__toggleFindToolButton.setShortcut(DEFAULT_SHORTCUT_FIND)

        lay = QHBoxLayout()
        lay.addWidget(self.__sideBarBtn)
        lay.addWidget(self.__settingBtn)
        lay.addWidget(sep)
        lay.addWidget(self.__toggleFindToolButton)
        lay.setContentsMargins(2, 2, 2, 2)
        lay.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.__menuWidget = QWidget()
        self.__menuWidget.setLayout(lay)
        self.__menuWidget.setMaximumHeight(self.__menuWidget.sizeHint().height())

        self.__chatNavWidget.added.connect(self.__addThread)
        self.__chatNavWidget.clicked.connect(self.__showChat)
        self.__chatNavWidget.cleared.connect(self.__clearChat)
        self.__chatNavWidget.onFavoriteClicked.connect(self.__showFavorite)

        mainWidget = QSplitter()
        mainWidget.addWidget(self.__chatNavWidget)
        mainWidget.addWidget(self.__chatWidget)
        mainWidget.addWidget(self.__gptRightSideBarWidget)
        mainWidget.setSizes([100, 500, 400])
        mainWidget.setChildrenCollapsible(False)
        mainWidget.setHandleWidth(2)
        mainWidget.setStyleSheet(
            '''
            QSplitter::handle:horizontal
            {
                background: #CCC;
                height: 1px;
            }
            ''')

        sep = getSeparator('horizontal')

        lay = QVBoxLayout()
        lay.addWidget(self.__menuWidget)
        lay.addWidget(sep)
        lay.addWidget(mainWidget)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        self.setLayout(lay)

        # self.__lineEdit.setFocus()

    def toggleSideBar(self, x):
        self.__chatNavWidget.setVisible(x)
        self.__show_chat_list = x
        CONFIG_MANAGER.set_general_property('show_chat_list', self.__show_chat_list)

    def toggleSetting(self, x):
        self.__gptRightSideBarWidget.setVisible(x)
        self.__show_setting = x
        CONFIG_MANAGER.set_general_property('show_setting', self.__show_setting)

    def toggleButtons(self, x):
        self.__sideBarBtn.setChecked(x)
        self.__settingBtn.setChecked(x)

    def showThreadToolWidget(self, f):
        self.__toggleFindToolButton.setChecked(f)

    def __onMenuCloseClicked(self):
        self.__toggleFindToolButton.setChecked(False)

    def showSecondaryToolBar(self, f):
        self.__menuWidget.setVisible(f)
        CONFIG_MANAGER.set_general_property('show_secondary_toolbar', f)

    def __showChat(self, id, title):
        self.__showFavorite(False)
        self.__chatNavWidget.activateFavoriteFromParent(False)
        self.__chatWidget.showTitle(title)
        self.__chatWidget.showMessages(id)

    def __clearChat(self):
        self.__chatWidget.showTitle('')
        self.__chatWidget.clearMessages()

    def __addThread(self):
        title = 'New Chat'
        cur_id = DB.insertThread(title)
        self.__chatWidget.showTitle(title)
        self.__chatWidget.showMessages(cur_id)

        self.__chatNavWidget.add(called_from_parent=True)

    def __importChat(self, data):
        try:
            # Import thread
            for thread in data:
                cur_id = DB.insertThread(thread['name'], thread['insert_dt'], thread['update_dt'])
                messages = thread['messages']
                # Import message
                for message in messages:
                    message['thread_id'] = cur_id
                    container = ChatMessageContainer(**message)
                    DB.insertMessage(container, deactivate_trigger=True)
            self.__chatNavWidget.refreshData()
        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 'Check whether the file is a valid JSON file for importing.')

    def __exportChat(self, ids):
        file_data = QFileDialog.getSaveFileName(self, 'Save', QFILEDIALOG_DEFAULT_DIRECTORY,
                                                f'{JSON_FILE_EXT_LIST_STR};;txt files Compressed File (*.zip);;html files Compressed File (*.zip)')
        if file_data[0]:
            filename = file_data[0]
            ext = os.path.splitext(filename)[-1] or get_generic_ext_out_of_qt_ext(file_data[1])
            if ext == '.zip':
                compressed_file_type = file_data[1].split(' ')[0].lower()
                ext_dict = {'txt': {'ext': '.txt', 'func': message_list_to_txt},
                            'html': {'ext': '.html', 'func': conv_unit_to_html}}
                for id in ids:
                    row_info = DB.selectThread(id)
                    # Limit the title length to file name length
                    title = row_info['name'][:FILE_NAME_LENGTH]
                    txt_filename = f'{title}_{id}{ext_dict[compressed_file_type]["ext"]}'
                    txt_content = ext_dict[compressed_file_type]['func'](DB, id, title)
                    add_file_to_zip(txt_content, txt_filename, os.path.splitext(filename)[0] + '.zip')
            elif ext == '.json':
                DB.export(ids, filename)
            open_directory(os.path.dirname(filename))

    def setColumns(self, columns):
        self.__chatNavWidget.setColumns(columns)

    def __showFavorite(self, f):
        if f:
            lst = DB.selectFavorite()
            if len(lst) == 0:
                return
            else:
                lst = [ChatMessageContainer(**dict(c)) for c in lst]
                self.__browser.replaceThreadForFavorite(lst)
