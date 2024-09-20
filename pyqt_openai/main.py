#!/usr/bin/env python3

import os
import sys

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

# for testing pyside6
# os.environ['QT_API'] = 'pyside6'

# for testing pyqt6
# os.environ['QT_API'] = 'pyqt6'

from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import QApplication, \
    QSplashScreen
from PySide6.QtSql import QSqlDatabase

from pyqt_openai.config_loader import CONFIG_MANAGER

from pyqt_openai.mainWindow import MainWindow
from pyqt_openai.util.script import handle_exception
from pyqt_openai.sqlite import get_db_filename

from pyqt_openai import DEFAULT_APP_ICON


# Application
class App(QApplication):
    def __init__(self, *args):
        super().__init__(*args)
        self.setQuitOnLastWindowClosed(False)
        self.setWindowIcon(QIcon(DEFAULT_APP_ICON))
        self.splash = QSplashScreen(QPixmap(DEFAULT_APP_ICON))
        self.splash.show()

        self.__initQSqlDb()
        self.__initFont()

        self.__showMainWindow()
        self.splash.finish(self.main_window)

    def __initQSqlDb(self):
        # Set up the database and table model (you'll need to configure this part based on your database)
        self.__imageDb = QSqlDatabase.addDatabase('QSQLITE')
        self.__imageDb.setDatabaseName(get_db_filename())
        self.__imageDb.open()

    def __initFont(self):
        font_family = CONFIG_MANAGER.get_general_property('font_family')
        font_size = CONFIG_MANAGER.get_general_property('font_size')
        QApplication.setFont(QFont(font_family, font_size))

    def __showMainWindow(self):
        self.main_window = MainWindow()
        self.main_window.show()

# Set the global exception handler
sys.excepthook = handle_exception

def main():
    app = App(sys.argv)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()