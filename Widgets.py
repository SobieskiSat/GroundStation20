from PyQt5.QtWidgets import (QWidget,QGridLayout, QApplication, QGraphicsScene,
QGraphicsView, QPushButton, QLabel, QComboBox, QDialog, QLineEdit)
from PyQt5.QtSvg import (QGraphicsSvgItem)
from PyQt5.QtCore import pyqtSignal, QUrl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5.QtQuickWidgets import QQuickWidget
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
        self.main_grid.addWidget(self.canvas, 1, 1)
        self.ax  = self.fig.add_subplot(111)

        self.left_grid = QGridLayout()
        self.zoomin_button = QPushButton('+')
        self.left_grid.addWidget(self.zoomin_button, 1, 1)
        self.zoomin_button.clicked.connect(self.zoomin)
        self.zoomin_button.setMaximumSize(30, 30)
        self.size_label = QLabel()
        self.left_grid.addWidget(self.size_label, 1, 2)
        self.zoomout_button = QPushButton('-')
        self.left_grid.addWidget(self.zoomout_button, 1, 3)
        self.zoomout_button.clicked.connect(self.zoomout)
        self.zoomout_button.setMaximumSize(30, 30)
        self.pause_button = QPushButton('||')
        self.left_grid.addWidget(self.pause_button, 1, 4)
        self.pause_button.clicked.connect(self.should_update_change)
        self.pause_button.setMaximumSize(30, 30)
        self.save_button = QPushButton('S')
        self.left_grid.addWidget(self.save_button, 1, 5)
        self.save_button.clicked.connect(self.save_png)
        self.save_button.setMaximumSize(30, 30)
        self.options_combo_box = QComboBox()
        self.left_grid.addWidget(self.options_combo_box, 1, 6)
        self.main_grid.addLayout(self.left_grid, 2, 1)


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

    def change_da(self):
        self.data_src.change_x_axis(self.options_combo_box.currentText())

    def set_possible_readings(self, data):
        self.options_combo_box.currentTextChanged.connect(self.change_da)
        self.options_combo_box.addItems(data)

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

class Speedometer(QWidget):
    def __init__(self):
        super().__init__()
        self.main_grid = QGridLayout()
        self.setLayout(self.main_grid)
        self.url = QUrl.fromLocalFile('media/speedometer.qml')
        self.quick = QQuickWidget()
        self.quick.initialSize()
        self.quick .setSource(self.url)
        self.main_grid.addWidget(self.quick, 1, 1)



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

class AntenaLocationSetWindow(AdditionalWindow):
    value_changed_signal = pyqtSignal()
    def __init__(self, last = None, *args):
        super().__init__(*args)
        self.ans = last
        if not last:
            self.ans = {'x':0, 'y':0, 'h':0}

        class LocationInput(QWidget):
            def __init__(self, name, val, type):
                super().__init__(*args)
                self.name = name
                self.type = type
                self.main_grid = QGridLayout()
                self.setLayout(self.main_grid)
                self.name_label = QLabel(self.name)
                self.main_grid.addWidget(self.name_label, 1, 1)
                self.error_label = QLabel('')
                self.main_grid.addWidget(self.error_label, 1, 3)
                self.error_label.setStyleSheet('color: Red')
                self.input_box = QLineEdit()
                self.main_grid.addWidget(self.input_box, 1, 2)
                self.input_box.textEdited.connect(self.checkType)

                try:
                    val = str(val)
                    self.input_box.setText(val)
                except Exception as e:
                    pass

            def checkType(self):
                txt = self.input_box.text()
                flag = None
                try:
                    txt = float(txt)
                    if self.type == 'cord_x' or self.type == 'cord_y':
                        if(txt <= -90 or txt >= 90): flag = 'Out_of_range'
                    if self.type == 'cord_h':
                        if (txt <= -200 or txt >= 8000): flag = 'Out_of_range'
                except Exception as e:
                    flag = 'Invalid_Form'
                if flag:
                    self.error_label.setText(flag)
                else:
                    self.error_label.setText('')
                return flag


        self.input_x = LocationInput('X', 0.0, 'cord_x')
        self.input_y = LocationInput('Y', 0.0, 'cord_y')
        self.input_h = LocationInput('H', 0.0, 'cord_h')
        self.input_x.input_box.textEdited.connect(self.edit_event)
        self.input_y.input_box.textEdited.connect(self.edit_event)
        self.input_h.input_box.textEdited.connect(self.edit_event)
        self.main_grid.addWidget(self.input_x, 1, 3)
        self.main_grid.addWidget(self.input_y, 2, 3)
        self.main_grid.addWidget(self.input_h, 3, 3)
        self.accept_button = QPushButton('SAVE')
        self.main_grid.addWidget(self.accept_button, 4, 3)
        self.accept_button.clicked.connect(self.save_clicked)
        self.edit_event()

        self.setGeometry(300, 300, 450, 350)

    def edit_event(self):
        correct_flag = True
        if self.input_x.checkType() != None:
            correct_flag = False
        if self.input_y.checkType() != None:
            correct_flag = False
        if self.input_h.checkType() != None:
            correct_flag = False
        self.accept_button.setEnabled(correct_flag)

    def save_clicked(self):
        self.ans = {
         'x':self.input_x.input_box.text(),
         'y':self.input_y.input_box.text(),
         'h':self.input_h.input_box.text()
        }
        self.value_changed_signal.emit()



class AntenaLocationLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.x = None
        self.y = None
        self.h = 0
        self.set_text()

    def update_location(self, loc):
        self.x = loc['x']
        self.y = loc['y']
        self.h = loc['h']
        self.set_text()

    def set_text(self):
        if not self.x or not self.y:
            color = 'Red'
            self.setText("Lokalizacja anteny nie została ustawiona!")
        else:
            color = 'DarkGreen'
            self.setText(f"Lokalizacja anteny: X_{self.x}, Y_{self.y}, H_{self.h}")
        color = 'color : ' + color
        self.setStyleSheet(color)

class DataPresentationWidget(QWidget):
    def __init__(self):
        self.precison = 3
        super().__init__()
        self.main_grid = QGridLayout()
        self.setLayout(self.main_grid)
        self.name_label = QLabel()
        self.main_grid.addWidget(self.name_label, 1, 1)
        self.data_label = QLabel()
        self.main_grid.addWidget(self.data_label, 2, 1)
        self.update_time_label = QLabel()
        self.main_grid.addWidget(self.update_time_label, 3, 1)


    def set(self, name):
        self.name = name
        self.name_label.setText(name)
        self.data_label.setText('NO_DATA')

    def update(self, data, last_time):
        time_since_last_update = round(time.time() - last_time, self.precison)
        self.data_label.setText(str(data))
        self.update_time_label.setText(str(time_since_last_update))

class DataSetWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.main_grid = QGridLayout()
        self.widgets  = {}
        self.data = {}
        self.width = 3
        self.widgets_limit = 12
        self.setLayout(self.main_grid)
        self.avalible_widgets = []
        for w in range(self.widgets_limit):
            widget = DataPresentationWidget()
            self.main_grid.addWidget(widget, w//3+1, w%3+1)
            self.avalible_widgets.append(widget)

    def update(self, **kwargs):
        for name, data in kwargs.items():
            try:
                current_time = time.time()
                self.data[name] ={
                'data':data, 'update_time':current_time, 'name':name}
            except Exception as e:
                print(e)

    def refresh(self):
        for _, d in self.data.items():
            if d['name'] in self.widgets:
                self.widgets[d['name']].update(d['data'], d['update_time'])
            elif len(self.avalible_widgets) > 0:
                new_widget = self.avalible_widgets.pop(0)
                new_widget.set(d['name'])
                self.widgets[d['name']] = new_widget
            else:
                print('[GUI] Not enough data widgets!')
