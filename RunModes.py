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
        self.mm.dm.data_processor.set_structure(self.mm.conf['structure'])
        # Logic threads
        self.threadpool = QThreadPool()
        self.log = LiveFlightLogic(self)
        self.gui = LiveFlightGui(self)
        # Communication Thread
        self.ser = SerialCommunicator('COM11')
        time.sleep(1)
        self.ser.setOnReadCallback(self.log.newDataCallback)
        self.threadpool.start(self.ser)
        # main window
        self.main_window = MainWindow()
        self.main_window.show()
        # running it
        self.threadpool.start(self.log)
        self.threadpool.start(self.gui)
        self.app.exec_()

class LiveFlightGui(QRunnable):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent


    @pyqtSlot()
    def run(self):
        self.da = self.parent.mm.dm.new_data_arranger('h', 'temperature')
        self.parent.main_window.plot1.start_data_ploter(self.da)
        while True:
            self.parent.main_window.plot1.update()
            time.sleep(0.2)

class LiveFlightLogic(QRunnable):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.left_motor = 50
        self.right_motor = 50
        self.left_key = False
        self.right_key = False
        self.left_key = False
        self.up_key = False
        self.down_key = False
        self.power = 0
        self.servo = 0xAA

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.left_key = True
        elif event.key() == Qt.Key_Right:
            self.right_key = True
        elif event.key() == Qt.Key_Up:
            self.up_key = True
        elif event.key() == Qt.Key_Down:
            self.down_key = True
        elif event.key() == Qt.Key_D:
            self.servo = 0x55


    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.left_key = False
        elif event.key() == Qt.Key_Right:
            self.right_key = False
        elif event.key() == Qt.Key_Up:
            self.up_key = False
        elif event.key() == Qt.Key_Down:
            self.down_key = False

    @pyqtSlot()
    def run(self):
        self.parent.main_window.keyPressEvent = self.keyPressEvent
        self.parent.main_window.keyReleaseEvent = self.keyReleaseEvent
        step = 5
        while True:
            if self.left_key and self.left_motor<=100-step:
                self.left_motor+=step
                self.right_motor-=step
            if self.right_key and self.right_motor<=100-step:
                self.right_motor+=step
                self.left_motor-=step
            if self.up_key and self.power<=100-step:
                self.power +=step
            if self.down_key and self.power>=step:
                self.power -= step

            temp_text = 'l:{} r:{} p:{}'.format(
            self.left_motor, self.right_motor, self.power)
            self.parent.main_window.temp2.setText(temp_text)

            l_out = int(self.left_motor*self.power/100)*2
            r_out = int(self.right_motor*self.power/100)*2
            motbytes = bytes([0xFF, l_out, r_out, self.servo])
            try:
                self.parent.ser.writeline(motbytes)
            except Exception as e:
                pass
            time.sleep(0.1)

    def newDataCallback(self, data):
        new_data = self.parent.mm.dm.append(data)
        self.parent.main_window.rocket_map.map_view.addPointToPath(
        new_data['x'], new_data['y'], '#123456'
        )
lf = LiveFlight()
lf.run()
