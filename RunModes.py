from DataManager import MemoryManager
from PyQt5.QtWidgets import QApplication
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
        self.threadpool.start(self.log)
        # main window
        self.main_window = MainWindow()
        self.main_window.show()
        self.app.exec_()

class LiveFlightLogic(QRunnable):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    @pyqtSlot()
    def run(self):
        self.serial = SerialCommunicator('COM10')
        while True:
            data = self.serial.readline()
            self.parent.main_window.temp.setText(str(data))
lf = LiveFlight()
lf.run()
