from PyQt5.QtWidgets import (QMainWindow, QApplication, QSplitter, QGridLayout,
QWidget, QLabel, QAction, QLineEdit, QPushButton)
from PyQt5.QtCore import Qt
import sys
from RocketMaps import RocketMap
from Widgets import Plot, PortSetWindow, AntenaLocationLabel, DataSetWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #central widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_grid = QGridLayout()
        self.main_widget.setLayout(self.main_grid)
        self.initToolbar()

        #main_grid and main main_splitter
        self.left_grid = QGridLayout()
        self.right_grid = QGridLayout()
        self.left_widget = QWidget()
        self.left_widget.setLayout(self.left_grid)
        self.right_widget = QWidget()
        self.right_widget.setLayout(self.right_grid)
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.addWidget(self.left_widget)
        self.main_splitter.addWidget(self.right_widget)
        self.main_grid.addWidget(self.main_splitter, 1, 1)

        #left_widget
        self.data_set_widget = DataSetWidget()
        self.left_grid.addWidget(self.data_set_widget, 1, 1)
        self.plot1 = Plot()
        self.left_grid.addWidget(self.plot1, 2, 1)
        self.plot2 = Plot()
        self.left_grid.addWidget(self.plot2, 2, 2)

        #right_widget
        self.rocket_map = RocketMap()
        self.right_grid.addWidget(self.rocket_map, 1, 1)
        self.text_grid = QGridLayout()
        self.right_grid.addLayout(self.text_grid, 2, 1)
        self.antena_location_label = AntenaLocationLabel()
        self.text_grid.addWidget(self.antena_location_label, 1, 1)
        self.set_antena_loactio_button =  QPushButton('SET ANTENA LOCATION')
        self.text_grid.addWidget(self.set_antena_loactio_button, 1, 2)
        self.find_point_button =  QPushButton('FIND POINT')
        self.text_grid.addWidget(self.find_point_button, 1, 3)
        self.port_status_label = QLabel('PortNotWorking')
        self.text_grid.addWidget(self.port_status_label, 2, 1)
        self.command_box = QLineEdit()
        self.text_grid.addWidget(self.command_box, 3, 1)
        self.send_command_button = QPushButton('SEND')
        self.text_grid.addWidget(self.send_command_button, 3, 2)


    def initToolbar(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Communication')
        self.find_arduino_menu = QAction('&Find Kit')
        self.set_port_menu = QAction('&Set Port')
        fileMenu.addAction(self.find_arduino_menu)
        fileMenu.addAction(self.set_port_menu)
        flightMenu = menubar.addMenu('&Flight')
        self.start_flight_menu = QAction('&Start new flight')
        flightMenu.addAction(self.start_flight_menu)
