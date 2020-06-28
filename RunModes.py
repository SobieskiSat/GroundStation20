from DataManager import MemoryManager
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.Qt import Qt
from PyQt5.QtCore import QThread, QRunnable, QThreadPool, pyqtSlot, pyqtSignal
import sys
import time
from MainWindow import MainWindow
from Communication import SerialCommunicator, DeviceSearcher
from Widgets import PortSetWindow

class LiveFlight():
    def __init__(self):
        pass

    def run(self):
        self.app = QApplication(sys.argv)
        self.mm = MemoryManager()
        self.mm.dm.data_processor.set_structure(self.mm.conf['new_structure'])
        # Logic threads
        self.threadpool = QThreadPool()
        self.log = LiveFlightLogic(self)
        self.gui = LiveFlightGui(self)
        self.af = AdditionalThread(self)
        self.af.port_dialog_signal.connect(self.open_port_dialog)
        self.af.start()
        # main window
        self.main_window = MainWindow()
        self.main_window.show()
        # running it
        self.threadpool.start(self.log)
        self.threadpool.start(self.gui)
        self.app.exec_()

    def open_port_dialog(self, args):

        # Used when any port choice button is clicked
        # Sets answer in dynamic memory as 'port'
        # Then callbacks function from args

        def dialog_callback(self, args):
            ans = self.dialog.ans
            self.dialog.close()
            self.mm.dyn['port'] = ans
            args['callback']()

        # Opens new window with port choice (it takes some time to load this)
        # ToDo: make it load ports dynamicly
        # If any choice made it calls dialog_callback

        self.dialog = PortSetWindow(self.main_window)
        self.dialog.set_port(args['ports'])
        ans = None
        self.dialog.value_changed_signal.connect(
        lambda: dialog_callback(self, args))
        self.dialog.exec_()


# AdditionalThread is used for time consuming logic

class AdditionalThread(QThread):

    port_dialog_signal = pyqtSignal(dict)
    # AdditionalThread requires parrent (Main_Logic_Thread such as LiveFlight)
    # Every function run in this thread should be written is this class
    # and requires @inner_runner decorator to be executed properly by main loop
    # ToDo: enable other functions to be executed in this thread

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.queue = []
        self.condition = True

    # Used to start main main loop
    # It keeps running while condition is set to True
    # It keeps checking if any function is waiting in a queue
    # When it is time to execute function is sets inst to True

    def run(self):
        while self.condition:
            if len(self.queue)>0:
                f = self.queue.pop(0)
                f(self, True)

    # Decorator used to enable functions to be queued and executed properly

    def inner_runner(function):
        # By default inst should be set to false
        # Setting it to True makes it skip the queue
        # ToDo: Change the way function is added to the queue

        def wrapper(self, inst = False, **kwargs):
            if inst:
                return function(**kwargs)
            self.queue.append(function)

        return wrapper
    # _____________
    # Functions that can be excecuted it this thread:
    # _____________

    # Restarts the device
    # [?] Why it Searches only for CanSat Kit
    # ToDo: Enable Reset for last used type of port

    @inner_runner
    def restart_serial(self, *args):
        try:
            self.parent.log.ser.port = DeviceSearcher().find_device_port()
            self.parent.log.ser.reset_serial()
        except Exception as e:
            print('[AddThr1] I wish I knew how to quit you! \n', e)

    # Gets readings structure from configuration files
    # It is not time consumin any more
    # Can be moved to main thread if needed

    @inner_runner
    def get_possible_readings(self, *args):
        return self.parent.mm.conf['new_structure'].values()

    # Opens Dialog that asks to choose a port to connect

    @inner_runner
    def set_port_menu(self, *args):
        ports = DeviceSearcher().list_ports()
        self.port_dialog_signal.emit({'ports':ports, 'callback': self.set_port})

    # Sets new port from dynamic memory 'port'
    # It can be spaned with reset_serial

    @inner_runner
    def set_port(self, *args, **kwargs):
        try:
            self.parent.log.ser.port = self.parent.mm.dyn['port']
        except Exception as e:
            print('[AddThr2] Frankly, my dear, I don\'t give a damn. \n', e)
        self.parent.log.ser.reset_serial()

    # Takes command from command_box and sends it to serial
    # ToDo: Add validation
    
    @inner_runner
    def send_command_line(self, *args):
        text = str(self.parent.main_window.command_box.text())
        self.parent.log.ser.writeline(text)

class LiveFlightGui(QRunnable):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    @pyqtSlot()
    def run(self):
        da1 = self.parent.mm.dm.new_data_arranger('flight_time', 'temperature')
        self.parent.main_window.plot1.start_data_ploter(da1)
        da2 = self.parent.mm.dm.new_data_arranger('flight_time', 'temperature')
        self.parent.main_window.plot2.start_data_ploter(da2)
        self.parent.main_window.find_arduino_menu.triggered.connect(
        self.parent.af.restart_serial)
        self.parent.main_window.set_port_menu.triggered.connect(
        self.parent.af.set_port_menu)
        self.parent.main_window.send_command_button.clicked.connect(
        self.parent.af.send_command_line)
        possible_readings = self.parent.mm.conf['new_structure'].values()
        self.parent.main_window.plot2.set_possible_readings(possible_readings)
        self.parent.main_window.plot1.set_possible_readings(possible_readings)
        while True:
            self.parent.main_window.plot1.update()
            self.parent.main_window.plot2.update()
            self.update_serial_status()
            time.sleep(0.2)

    def update_serial_status(self):
        color = ''
        if not hasattr(self.parent.log, 'ser'):

            text = 'Loading...'
            color = 'DarkOrange'
        else:
            status = self.parent.log.ser.connection_status()
            if status == 0:
                text = 'Waiting for connection...'
                color = 'DarkOrange'
            elif status == 1:
                text = 'Device ready at port '
                text += str(self.parent.log.ser.port)
                color = 'DarkGreen'
            elif status == -2:
                text = 'Disconnected!'
                color = 'Red'
            else:
                text = 'Failed to connect'
                color = 'Red'
        self.parent.main_window.port_status_label.setText(text)
        color = 'color : ' + color
        self.parent.main_window.port_status_label.setStyleSheet(color)


class LiveFlightLogic(QRunnable):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.angle = 0
        self.last_angle = 0
        self.left_motor = 50
        self.right_motor = 50
        self.left_key = False
        self.right_key = False
        self.left_key = False
        self.up_key = False
        self.down_key = False
        self.power = 0
        self.servo = 0
        self.engines = 0

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_N:
            self.left_key = True
        elif event.key() == Qt.Key_M:
            self.right_key = True
        elif event.key() == Qt.Key_R:
            if self.engines == 0:
                self.engines = 1
            else:
                self.engines = 0
            self.ser.add_to_outbuffer("m{}M".format(str(self.engines)))
        elif event.key() == Qt.Key_Up:
            self.up_key = True
        elif event.key() == Qt.Key_Down:
            self.down_key = True
        elif event.key() == Qt.Key_D:
            if self.servo == 0:
                self.servo = 1
            else:
                self.servo = 0
            self.ser.add_to_outbuffer("s{}S".format(str(self.servo)))



    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_N:
            self.left_key = False
        elif event.key() == Qt.Key_M:
            self.right_key = False
        elif event.key() == Qt.Key_Up:
            self.up_key = False
        elif event.key() == Qt.Key_Down:
            self.down_key = False

    @pyqtSlot()
    def run(self):
        self.ser = SerialCommunicator()
        self.ser.setOnReadCallback(self.newDataCallback)
        while not hasattr(self.ser, 'serial'):
            pass
        self.parent.threadpool.start(self.ser)
        self.parent.main_window.keyPressEvent = self.keyPressEvent
        self.parent.main_window.keyReleaseEvent = self.keyReleaseEvent
        step = 1
        while True:
            if self.left_key:
                self.angle -= step
            if self.right_key:
                self.angle += step
            if self.up_key and self.power<=100-step:
                self.power +=step
            if self.down_key and self.power>=step:
                self.power -= step
            self.angle = self.angle%360

            if self.angle != self.last_angle:
                self.ser.add_to_outbuffer("a{}A".format(str(self.angle)))
                self.last_angle = self.angle


            temp_text = 'l:{} r:{} p:{} a:{}'.format(
            self.left_motor, self.right_motor, self.power, self.angle)
            self.parent.main_window.temp2.setText(temp_text)

            l_out = int(self.left_motor*self.power/100)*2
            r_out = int(self.right_motor*self.power/100)*2
            #motbytes = bytes([0xFF, l_out, r_out, self.servo])
            try:
                self.ser.writeline(motbytes)
            except Exception as e:
                pass
            time.sleep(0.1)

    def newDataCallback(self, data):
        new_data = self.parent.mm.dm.append(data)

        try:
            self.parent.main_window.rocket_map.map_view.addPointToPath(
            new_data['x'], new_data['y'], '#123456'
            )
        except Exception as e:
            pass
        print(data)

lf = LiveFlight()
lf.run()
