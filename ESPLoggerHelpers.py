from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
import serial.tools.list_ports as ports_list
import os
import json

class ESPLoggerSignals(QObject):
    add_to_logger_signal = pyqtSignal(str)

logger_add_to_logger_signal = ESPLoggerSignals()

add_to_logger_signal = pyqtSignal(str)

class ESPLoggerDialog(QDialog):
    def __init__(self, message):
        super(ESPLoggerDialog, self).__init__()

        self.logger_dialog_buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        self.logger_dialog_buttons.clicked.connect(self.dialog_OK_button_clicked)

        self.message = QLabel(message)

        self.dialog_layout = QVBoxLayout()

        self.dialog_layout.addWidget(self.message)
        self.dialog_layout.addWidget(self.logger_dialog_buttons)
        self.setLayout(self.dialog_layout)

        self.setWindowTitle('Error!!')
        self.move(600, 300)
    
    def dialog_OK_button_clicked(self):
        self.close()

class ESPLoggerColor(QWidget):
    def __init__(self, color):
        super(ESPLoggerColor, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class ESPLoggerSplitter(QSplitter):
    def __init__(self, parent):
        super(ESPLoggerSplitter, self).__init__(parent)
        
    def place_widgets(self, *widgets: tuple):
        for widget in widgets:
            self.addWidget(widget)

# This class holds logger dropdown, file name setter, baudrate selector, file saving directory selector and the add to the logger button.
class ESPLoggerLeftSideExplorerFirst(QVBoxLayout):
    def __init__(self):
        super(ESPLoggerLeftSideExplorerFirst, self).__init__()
        self.addStretch(2)
        self.logger_file_directory_selector_dialog = str()

        self.logger_dropdown = QComboBox()
        self.ports_connected = ports_list.comports()
        for port, desc, hwid in sorted(self.ports_connected):
            self.logger_dropdown.addItem(port)
        
        self.logger_file_name = QLineEdit()
        self.baudrate_dropdown = QComboBox()
        self.baudrate_dropdown.addItems(('9600', '14400', '19200', '38400', '57600', '115200', '128000', '256000'))
        self.logger_file_directory_selector_button = QPushButton('Select a directory')
        self.logger_file_directory_selector_button.clicked.connect(self.logger_file_directory_selector_button_clicked)
        self.logger_add_button = QPushButton(text="Add to Logger")
        self.logger_add_button.clicked.connect(self.logger_add_button_clicked)
        
        self.place_widgets(self.logger_dropdown, self.baudrate_dropdown, self.logger_file_name, self.logger_file_directory_selector_button, self.logger_add_button)
    
    def logger_file_directory_selector_button_clicked(self):
        self.logger_file_directory_selector_dialog = QFileDialog.getExistingDirectory(caption='Select a Directory')
        self.directory_name = self.logger_file_directory_selector_dialog.split('/')
        self.logger_file_directory_selector_button.setText('{0}'.format(self.directory_name[-1]))
    
    def logger_add_button_clicked(self):
        self.port_name = self.logger_dropdown.currentText()
        self.file_name = self.logger_file_name.text()
        self.is_empty = False
        self.message = str()
        if len(self.port_name) == 0:
            self.is_empty = True
            self.message = 'Empty port name.'
        if len(self.baudrate_dropdown) == 0:
            self.is_empty = True
            self.message = 'Empty baudrate.'
        elif len(self.file_name) == 0:
            self.is_empty = True
            self.message = 'Empty file name.'
        elif len(self.logger_file_directory_selector_dialog) == 0:
            self.is_empty = True
            self.message = 'File direcotry not selected.'
        else:
            self.is_empty = False
            self.message = ''
        if self.is_empty:
            self.dialog = ESPLoggerDialog(message=self.message)
            self.dialog.exec()
        else:
            self.logger_port_add_detail = {
                "Port": self.port_name,
                "File": self.file_name,
                "Directory": self.logger_file_directory_selector_dialog
            }
            self.port_details = json.dumps(self.logger_port_add_detail, indent = 8)
            logger_add_to_logger_signal.add_to_logger_signal.emit(self.port_details)

    def place_widgets(self, *widgets: tuple):
        for widget in widgets:
            self.addWidget(widget)

class ESPLoggerLeftSideExplorerSecondPortBox(QHBoxLayout):
    def __init__(self, name='Port'):
        super(ESPLoggerLeftSideExplorerSecondPortBox, self).__init__()
        self.logger_left_side_explorer_second_hbox_port_button = QPushButton(name)
        self.logger_left_side_explorer_second_hbox_port_check_box = QCheckBox()
        self.place_widgets(self.logger_left_side_explorer_second_hbox_port_button, self.logger_left_side_explorer_second_hbox_port_check_box)

    def place_widgets(self, *widgets: tuple):
        for widget in widgets:
            self.addWidget(widget)

# This class holds the portname and the checkbox.
class ESPLoggerLeftSideExplorerSecond(QVBoxLayout):
    def __init__(self):
        super(ESPLoggerLeftSideExplorerSecond, self).__init__()
        self.addStretch(2)
        logger_add_to_logger_signal.add_to_logger_signal.connect(self.logger_connect_to_add_to_logger_signal)   
        self.added_ports = list()
    
    def place_widgets(self, *widgets: tuple):
        for widget in widgets:
            self.addWidget(widget)
    
    def logger_connect_to_add_to_logger_signal(self, detail):
        self.details = json.loads(detail)
        if self.added_ports and self.details['Port'] in self.added_ports:
            if self.check_file_if_exist(self.details['Directory'], self.details['File']):
                print('File exist in the directory')
            else:
                print('File doesn\'t exist in the directory')
        else:
            self.added_ports.append(self.details['Port'])
            self.logger_left_side_explorer_second_hbox_widget = QWidget()
            self.logger_left_side_explorer_second_hbox = ESPLoggerLeftSideExplorerSecondPortBox(name=self.details['Port'])
            self.logger_left_side_explorer_second_hbox_widget.setLayout(self.logger_left_side_explorer_second_hbox)
            self.place_widgets(self.logger_left_side_explorer_second_hbox_widget)
    
    def check_file_if_exist(self, directory_path=None, filename=None):
        self.exist = False
        if directory_path is None and filename is None:
            self.exist = False
        else:
            print(directory_path)
            for root, dirs, files in os.walk(directory_path):
                if filename in [file.split('.')[0] for file in files]:
                    self.exist = True
                else:
                    self.exist = False
                dirs.clear()
        return self.exist
            

# This class holds all the widgets in the left side of the logger UI.
class ESPLoggerLeftSideExplorer(QVBoxLayout):
    def __init__(self, parent):
        super(ESPLoggerLeftSideExplorer, self).__init__()

        self.logger_left_side_splitter_widget = QWidget()
        self.logger_left_side_first_vbox_widget = QWidget()
        self.logger_left_side_second_vbox_widget = QWidget()

        self.logger_left_side_splitter = ESPLoggerSplitter(self.logger_left_side_splitter_widget)
        self.logger_left_side_first_vbox = ESPLoggerLeftSideExplorerFirst()
        self.logger_left_side_second_vbox = ESPLoggerLeftSideExplorerSecond()
        self.logger_left_side_delete_button = QPushButton('Remove from Logger')

        self.logger_left_side_first_vbox_widget.setLayout(self.logger_left_side_first_vbox)
        self.logger_left_side_second_vbox_widget.setLayout(self.logger_left_side_second_vbox)
        self.logger_left_side_splitter.setOrientation(2)
        self.logger_left_side_splitter.place_widgets(self.logger_left_side_first_vbox_widget, self.logger_left_side_second_vbox_widget, self.logger_left_side_delete_button)

        self.place_widgets(self.logger_left_side_splitter)

        self.addStretch(2)
    
    def place_widgets(self, *widgets: tuple):
        for widget in widgets:
            self.addWidget(widget)

class ESPLoggerRightSideExplorer(QVBoxLayout):
    def __init__(self, parent):
        super(ESPLoggerRightSideExplorer, self).__init__()
        self.logger_text_area = QTextEdit()
        self.logger_text_area.setReadOnly(True)
        self.logger_text_area.setFixedHeight(575)
        self.logger_text_area.setFixedWidth(775)
        self.place_widgets(self.logger_text_area)
        
    def place_widgets(self, *widgets: tuple):
        for widget in widgets:
            self.addWidget(widget)
    