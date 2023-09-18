import sys
from PyQt5.QtWidgets import QApplication
from ESPLogger import ESPLogger

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ESPLogger()
    sys.exit(app.exec_())
