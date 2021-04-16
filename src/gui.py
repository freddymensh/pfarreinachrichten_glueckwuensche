from threading import Thread
import configparser
import logging

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QFile, QObject

import ressources.ressources
from src.textwriter import Textwriter

CONFIG_FILE = "./config.ini"


def threaded(fn):
    def wrapper(*args, **kwargs):
        Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper


class GUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        uiFile = QFile(':/gui/gui.ui')
        uiFile.open(QFile.ReadOnly)
        uic.loadUi(uiFile, self)

        # logging
        QTextEditLogger.setup_logger(name="my_logger")
        loggTextBox = QTextEditLogger(widget=self.plainTextEdit_Logger)
        loggTextBox.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger = logging.getLogger('my_logger')
        self.logger.addHandler(loggTextBox)
        self.logger.info("logging setup completed")

        # connect callbacks
        self.pushButton_indata.clicked.connect(self._pushButton_indata_clicked)
        self.pushButton_outpath.clicked.connect(self._pushButton_outpath_clicked)
        self.pushButton_start.clicked.connect(self._pushButton_start_clicked)
        self.checkBox_savesettings.stateChanged.connect(self._checkBox_savesettings_stateChanged)

        # read config
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_FILE)
        self.config_use_user = self.config['default']['use_user'].lower() == 'true'
        self.logger.info("config loaded")

        # write gui values
        self.write_config_to_gui()
        # TODO Ladebalken

    def write_config_to_gui(self):
        self.setWindowTitle(self.config['default']['window_title'])
        if self.config_use_user:
            config = self.config['user']
            self.logger.info("benutze user-config")
        else:
            config = self.config['default']
            self.logger.info("benutze default-config")
        self.plainTextEdit_indata.setPlainText(config['indata'])
        self.plainTextEdit_outpath.setPlainText(config['outpath'])
        self.checkBox_savesettings.setChecked(self.config['default']['use_user'].lower() == 'true')

    def _write_config(self):
        if self.config_use_user:
            self.config['user']['indata'] = self.plainTextEdit_indata.toPlainText()
            self.config['user']['outpath'] = self.plainTextEdit_outpath.toPlainText()
        with open(CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)
            self.logger.info("config mit neuen Werten gespeichert")

    def _pushButton_indata_clicked(self):
        data, _ = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Eingabe"), "C:\\", self.tr("Excel (*.xls *.xlsx *.xlsm *.xlsb *.odf *.ods *.odt)"))
        print(data)
        self.plainTextEdit_indata.setPlainText(data)
        if self.config_use_user:
            self.config['user']['indata'] = data

    def _pushButton_outpath_clicked(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(None, self.tr("Ausgabe"), "C:\\", QtWidgets.QFileDialog.ShowDirsOnly)
        self.plainTextEdit_outpath.setPlainText(path)
        if self.config_use_user:
            self.config['user']['outpath'] = path

    def _pushButton_start_clicked(self):
        # save config-dict
        self._write_config()
        # start process
        self._main_process()

    def _checkBox_savesettings_stateChanged(self):
        self.config['default']['use_user'] = str(self.checkBox_savesettings.isChecked())
        self.config_use_user = self.checkBox_savesettings.isChecked()

    @threaded
    def _main_process(self):
        mode = {'birth': self.checkBox_birth.isChecked(), 'baptize': self.checkBox_baptize.isChecked(), 'dead': self.checkBox_dead.isChecked()}
        indata = self.plainTextEdit_indata.toPlainText()
        outpath = self.plainTextEdit_outpath.toPlainText()
        textwriter = Textwriter(indata=indata, outpath=outpath, mode=mode, config=self.config)
        textwriter.write_txt()


class QTextEditLogger(logging.Handler, QObject):
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

