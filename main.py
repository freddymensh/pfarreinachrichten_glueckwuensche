import os
import sys
from PyQt5 import QtWidgets

def load_ressources():
    if os.path.isfile(r"ressources/ressources.qrc"):
        os.system(r"pyrcc5 ressources/ressources.qrc -o ressources/ressources.py")


if __name__ == "__main__":
    APP = 0
    if QtWidgets.QApplication.instance():
        APP = QtWidgets.QApplication.instance()
    else:
        APP = QtWidgets.QApplication(sys.argv)
    APP.setStyle('fusion')
    if True:
        load_ressources()
    if True:
        from src.gui import GUI
        window = GUI()
        window.show()

        #if APP:
        #    sys.exit(APP.quit())
        sys.exit(APP.exec_())