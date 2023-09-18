
import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ESPLoggerHelpers import *


#********************Main Window class********************#
class ESPLogger(QWidget):
    def __init__(self, title="ESP Logger"):
        super(ESPLogger, self).__init__()
        self.resize(1000, 600)
        self.setWindowTitle(title)
        self.move(200, 50)

        self.mainsplitter = ESPLoggerSplitter(self)

        self.leftwidget = QWidget()
        self.rightwidget = QWidget()

        self.leftexplorer = ESPLoggerLeftSideExplorer(self)
        self.rightexplorer = ESPLoggerRightSideExplorer(self)

        self.leftwidget.setLayout(self.leftexplorer)
        self.rightwidget.setLayout(self.rightexplorer)

        self.leftwidget.setFixedWidth(200)
        self.rightwidget.setFixedWidth(850)

        self.mainsplitter.place_widgets(self.leftwidget, self.rightwidget)
        
        self.show()
    
        


