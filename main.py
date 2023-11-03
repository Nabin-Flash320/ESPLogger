import sys
from PyQt5.QtWidgets import QApplication
from ESPLogger import ESPLogger
import serial.tools.list_ports as winports

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ESPLogger()
    sys.exit(app.exec_())
