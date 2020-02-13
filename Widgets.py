from PyQt5.QtWidgets import (QWidget,QGridLayout)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class Plot(QWidget):
    def __init__(self):
        super().__init__()
        self.main_grid = QGridLayout()
        self.setLayout(self.main_grid)
        self.canvas = FigureCanvas()
