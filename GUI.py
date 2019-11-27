import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from functools import partial
import entry_management
from time import sleep

en = entry_management.Entry()


# --------------------------------------------Entry_gui CLASS CODE STARTS-------------------------------------------------
class Entry_gui(object):
    def __init__(self):
        self.app = QApplication(sys.argv)



    def init_UI(self):
        ui = uic.loadUi("main1.ui")
        #welcome screen
        logo = QtGui.QImage('logo1.jpeg')
        logo = logo.scaled(2000, 440, aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        ui2.logo.setPixmap(QtGui.QPixmap.fromImage(logo))









sys.exit(app.exec_())






