from threading import Thread
import configparser
import logging

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QFile


CONFIG_FILE = "./setup.ini"


def threaded(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper


class GUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        uiFile = QFile('src/gui.ui')
        uiFile.open(QFile.ReadOnly)
        uic.loadUi(uiFile, self)

        # logging
        QTextEditLogger.setup_logger(name="my_logger")
        loggTextBox = QTextEditLogger(widget=self.plainTextEdit_Logger)
        loggTextBox.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger = logging.getLogger('my_logger')
        self.logger.addHandler(loggTextBox)
        self.logger.info("logging setup completed")


class QTextEditLogger(logging.Handler, QtCore.QObject):
    appendPlainText = QtCore.pyqtSignal(str)

    def __init__(self, widget):
        super().__init__()
        QtCore.QObject.__init__(self)
        self.widget = widget
        self.widget.setReadOnly(True)
        self.appendPlainText.connect(self.widget.appendPlainText)

    def emit(self, record):
        msg = self.format(record)
        self.appendPlainText.emit(msg)

    @staticmethod
    def setup_logger(name):
        formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if logger.hasHandlers():
            logger.handlers.clear()
        logger.addHandler(handler)

