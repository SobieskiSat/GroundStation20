from PyQt5.QtWidgets import (QMainWindow, QApplication, QSplitter, QGridLayout,
QWidget, QLabel)
from PyQt5.QtCore import Qt
import sys
from RocketMaps import RocketMap
from Widgets import Plot

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
        self.temp = QLabel('Label1')
        self.left_grid.addWidget(self.temp, 1, 1)
        self.plot1 = Plot()
        self.left_grid.addWidget(self.plot1, 2, 1)

        #right_widget
        self.right_splitter = QSplitter(Qt.Vertical)
        self.rocket_map = RocketMap()
        self.right_splitter.addWidget(self.rocket_map)
        self.temp2 = QLabel('Label2')
        self.right_splitter.addWidget(self.temp2)
        self.right_grid.addWidget(self.right_splitter, 1, 1)
