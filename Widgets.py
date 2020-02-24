from PyQt5.QtWidgets import (QWidget,QGridLayout, QApplication)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

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
        self.canvas = FigureCanvas(self.fig)
        self.main_grid.addWidget(self.canvas, 1, 1)
        self.ax  = self.fig.add_subplot(111)
        #self.example_plot()

    def plot(self, data1, data2='r-'):
        self.ax.clear()
        self.ax.plot(data1, data2)
        self.canvas.draw()

    def start_data_ploter(self, data_src):
        self.data_src = data_src

    def update(self):
        super().update()
        if self.data_src:
            try:
                self.update_data()
            except Exception as e:
                print('[Plot] ',e)

    def update_data(self):
        data = self.data_src()
        self.plot(data[0], data[1])


    def set_title(self, title):
        self.ax.set_title(title)

    def example_plot(self):
        data = [random.random() for i in range(25)]
        self.ax.plot(data, 'r-')
        self.ax.set_title('Example')
        self.canvas.draw()

'''
app = QApplication(sys.argv)
pl = Plot()
pl.show()
app.exec_()
'''
