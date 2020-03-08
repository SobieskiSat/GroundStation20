from PyQt5.QtWidgets import (QWidget,QGridLayout, QApplication, QGraphicsScene,
QGraphicsView, QPushButton, QLabel, QComboBox, QDialog)
from PyQt5.QtSvg import (QGraphicsSvgItem)
from PyQt5.QtCore import pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import os
import time

## TEMP:
import random
import sys

class Plot(QWidget):
    def __init__(self):
        super().__init__()
        self.main_grid = QGridLayout()
        self.setLayout(self.main_grid)
        self.fig = Figure()
        self.title = ''
        self.data_src = None
        self.size = 100
        self.zoom_step = 50
        self.should_update = True
        self.canvas = FigureCanvas(self.fig)
        self.main_grid.addWidget(self.canvas, 1, 2)
        self.ax  = self.fig.add_subplot(111)
        #self.example_plot()

        self.left_grid = QGridLayout()
        self.zoomin_button = QPushButton('+')
        self.left_grid.addWidget(self.zoomin_button, 2, 1)
        self.zoomin_button.clicked.connect(self.zoomin)
        self.zoomin_button.setMaximumSize(30, 30)
        self.size_label = QLabel()
        self.left_grid.addWidget(self.size_label, 3, 1)
        self.zoomout_button = QPushButton('-')
        self.left_grid.addWidget(self.zoomout_button, 4, 1)
        self.zoomout_button.clicked.connect(self.zoomout)
        self.zoomout_button.setMaximumSize(30, 30)
        self.pause_button = QPushButton('||')
        self.left_grid.addWidget(self.pause_button, 5, 1)
        self.pause_button.clicked.connect(self.should_update_change)
        self.pause_button.setMaximumSize(30, 30)
        self.save_button = QPushButton('S')
        self.left_grid.addWidget(self.save_button, 6, 1)
        self.save_button.clicked.connect(self.save_png)
        self.save_button.setMaximumSize(30, 30)
        self.main_grid.addLayout(self.left_grid, 1, 1)

    def plot(self, data1, data2='r-'):
        self.ax.clear()
        self.ax.plot(data1, data2)
        self.canvas.draw()

    def start_data_ploter(self, data_src):
        self.data_src = data_src

    def should_update_change(self):
        self.should_update = not self.should_update

    def zoomin(self):
        self.size += self.zoom_step

    def zoomout(self):
        new_size = self.size - self.zoom_step
        if new_size > 0:
            self.size = new_size

    def save_png(self):
        cur_time = time.localtime()
        time_str = time.strftime("%Y-%m-%d_%H_%M_%S")
        name = 'png/fig-'+time_str+'.png'
        self.fig.savefig(name)

    def update(self):
        super().update()
        if self.data_src and self.should_update:
            try:
                self.update_data()
            except Exception as e:
                print('[Plot] ',e)
        self.size_label.setText(str(self.size))

    def update_data(self):
        data = self.data_src(self.size)
        self.plot(data[0], data[1])

    def get_possible_readings(self):
        pass

    def set_size(self, size):
        self.size = size

    def set_title(self, title):
        self.ax.set_title(title)

    def example_plot(self):
        data = [random.random() for i in range(25)]
        self.ax.plot(data, 'r-')
        self.ax.set_title('Example')
        self.canvas.draw()

class HSI(QWidget):
    def __init__(self):
        self.face = Q

class AdditionalWindow(QDialog):
    def __init__(self, *args):
        super().__init__(*args)
        self.main_grid = QGridLayout()
        self.setLayout(self.main_grid)

    def end(self, *args):
        return ends

class PortSetWindow(AdditionalWindow):
    value_changed_signal = pyqtSignal()
    def __init__(self, *args):
        super().__init__(*args)
        self.label = QLabel('Choose COM port:')
        self.main_grid.addWidget(self.label, 1, 1)
        self.setGeometry(300, 300, 450, 350)
        self.ans = None

    def set_port(self, ports):
        for i, p in enumerate(ports):
                button = QPushButton(str(p))
                button.clicked.connect(lambda: self.click_event(p))
                self.main_grid.addWidget(button, i+2, 1)

    def click_event(self, p):
        self.ans = p
        self.value_changed_signal.emit()
'''
app = QApplication(sys.argv)
pl = Plot()
pl.show()
app.exec_()
'''
