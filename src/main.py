import os
import sys
from PyQt5 import QtWidgets

from gui import GUI

if __name__ == "__main__":
    APP = 0
    if QtWidgets.QApplication.instance():
        APP = QtWidgets.QApplication.instance()
    else:
        APP = QtWidgets.QApplication(sys.argv)
    APP.setStyle('fusion')
    window = GUI()
    window.show()

    #if APP:
    #    sys.exit(APP.quit())
    sys.exit(APP.exec_())