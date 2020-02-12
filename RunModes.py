from DataManager import MemoryManager
from PyQt5.QtWidgets import QApplication
from PyQt5.Qt import Qt
from PyQt5.QtCore import QThread, QRunnable, QThreadPool, pyqtSlot
import sys
import time
from MainWindow import MainWindow
from Communication import SerialCommunicator

class LiveFlight():
    def __init__(self):
        pass

    def run(self):
        self.app = QApplication(sys.argv)
        self.mm = MemoryManager()
        # Logic threads
        self.threadpool = QThreadPool()
        self.log = LiveFlightLogic(self)
        # Communication Thread
        self.ser = SerialCommunicator('COM10')
        self.ser.setOnReadCallback(self.log.newDataCallback)
        self.threadpool.start(self.ser)
        # main window
        self.main_window = MainWindow()
        self.main_window.show()
        # running it
        self.threadpool.start(self.log)
        self.app.exec_()

class LiveFlightLogic(QRunnable):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.left_motor = 0
        self.right_motor = 0

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.left_motor = 1
        if event.key() == Qt.Key_Right:
            self.right_motor = 1

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.left_motor = 0
        if event.key() == Qt.Key_Right:
            self.right_motor = 0

    @pyqtSlot()
    def run(self):
        self.parent.main_window.keyPressEvent = self.keyPressEvent
        self.parent.main_window.keyReleaseEvent = self.keyReleaseEvent
        while True:
            line = '{}{}\n'.format(self.left_motor, self.right_motor)
            self.parent.ser.writeline(bytes(line, encoding='utf8'))
            print(self.parent.mm.dm.get_last(3))
            time.sleep(0.1)

    def newDataCallback(self, data):
        self.parent.main_window.temp.setText(data)
        self.parent.mm.dm.append(data)

lf = LiveFlight()
lf.run()
