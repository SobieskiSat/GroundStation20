from DataManager import MemoryManager
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.Qt import Qt
from PyQt5.QtCore import QThread, QRunnable, QThreadPool, pyqtSlot, pyqtSignal
import sys
import time
from MainWindow import MainWindow
from Communication import SerialCommunicator, DeviceSearcher
from Widgets import (PortSetWindow, AntenaLocationSetWindow,
FlightTargetSetWindow, FlightDirectionSetWindow, FlightModeSetWindow)

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
        self.af.set_antena_location_signal.connect(
        self.open_set_antena_location_dialog)
        self.af.set_flight_mode_signal.connect(self.open_set_flight_mode_dialog)
        self.af.set_flight_target_signal.connect(self.open_set_flight_target_dialog)
        self.af.set_flight_direction_signal.connect(self.open_set_flight_direction_dialog)
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
        # ans = None
        self.dialog.value_changed_signal.connect(
        lambda: dialog_callback(self, args))
        self.dialog.exec_()

    def open_set_antena_location_dialog(self, args):
        def dialog_callback(self, args):
            ans = self.dialog.ans
            self.dialog.close()
            self.mm.dyn['antena_location'] = ans
            args['callback']()

        self.dialog = AntenaLocationSetWindow(self.main_window)
        if 'antena_location' in self.mm.dyn:
            self.dialog.set_current_location(self.mm.dyn['antena_location'])
        self.dialog.value_changed_signal.connect(
        lambda: dialog_callback(self, args))
        self.dialog.exec_()

    def open_set_flight_mode_dialog(self, args):
        def dialog_callback(self, args):
            ans = self.dialog.ans
            self.dialog.close()
            self.mm.dyn['flightmode'] = ans
            args['callback']()

        self.dialog = FlightModeSetWindow(self.main_window)
        self.dialog.value_changed_signal.connect(
        lambda: dialog_callback(self, args))
        self.dialog.exec_()

    def open_set_flight_direction_dialog(self, args):
        def dialog_callback(self, args):
            ans = self.dialog.ans
            self.dialog.close()
            self.mm.dyn['direction'] = ans
            args['callback']()

        self.dialog = FlightDirectionSetWindow(self.main_window)
        self.dialog.value_changed_signal.connect(
        lambda: dialog_callback(self, args))
        self.dialog.exec_()

    def open_set_flight_target_dialog(self, args):
        def dialog_callback(self, args):
            ans = self.dialog.ans
            self.dialog.close()
            self.mm.dyn['target'] = ans
            args['callback']()

        self.dialog = FlightTargetSetWindow(self.main_window)
        self.dialog.value_changed_signal.connect(
        lambda: dialog_callback(self, args))
        self.dialog.exec_()

# AdditionalThread is used for time consuming logic

class AdditionalThread(QThread):

    port_dialog_signal = pyqtSignal(dict)
    set_antena_location_signal = pyqtSignal(dict)
    set_flight_mode_signal = pyqtSignal(dict)
    set_flight_target_signal = pyqtSignal(dict)
    set_flight_direction_signal = pyqtSignal(dict)

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
                f['func'](self, f['args'], **f['kwargs'])

    # Decorator used to enable functions to be queued and executed properly

    def inner_runner(function):
        # By default inst should be set to false
        # Setting it to True makes it skip the queue
        # ToDo: Change the way function is added to the queue

        def wrapper(self, inst = False, *args, **kwargs):
            if inst:
                return function(**kwargs)
            self.queue.append({'func':function, 'args':args, 'kwargs':kwargs})

        return wrapper
    # _____________
    # Functions that can be excecuted in this thread:
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
    # ToDo: Add validation and inner commands
    @inner_runner
    def send_command_line(self, *args):
        text = str(self.parent.main_window.command_box.text())
        self.parent.main_window.command_box.setText('')
        try:
            self.parent.log.ser.writeline(text)
        except Exception as e:
            print('[AddThr5] Wysyłanie nie powiodło się. \n', e)

    # Changes map focus to the last position of satelite

    @inner_runner
    def find_point(self, *args):
        try:
            last = self.parent.mm.dm.get_last(1)[0]['processed']
            if not last:
                return
            x, y = last['X'], last['Y']
            try:
                self.parent.main_window.rocket_map.map_view.findPoint(x, y, 13)
            except Exception as e:
                print('[AddThr3]', e)
        except Exception as e:
            print('[AddThr4] satelite location not saved!', e)

    # Excecuted when SER ANTENA LOCATION is clicked

    @inner_runner
    def set_antena_location_clicked(self, *args):
        self.set_antena_location_signal.emit(
        {'callback':self.set_antena_loacation})

    # Action to do after the new location of antena is set
    @inner_runner
    def set_antena_loacation(self, *args, **kwargs):
        self.send_by_serial(
        data = self.parent.mm.dyn['antena_location']['x'], code ='ant_x')
        self.send_by_serial(
        data = self.parent.mm.dyn['antena_location']['y'], code = 'ant_y')
        self.send_by_serial(
        data = self.parent.mm.dyn['antena_location']['h'], code = 'ant_h')
        self.parent.main_window.antena_location_label.update_location(
        self.parent.mm.dyn['antena_location'])
        self.parent.main_window.rocket_map.map_view.setAntenaPoint(
        self.parent.mm.dyn['antena_location']['x'],
        self.parent.mm.dyn['antena_location']['y'])

    @inner_runner
    def send_by_serial(self, *args, **kwargs):
        code = kwargs['code']
        data = kwargs['data']
        try:
            code = self.parent.mm.conf['send_code'][code]
        except Exception as e:
            print(f'[AddThr6] Code not found {code} \n', e)
            return
        try:
            data = str(data)
            end = code.upper()
        except Exception as e:
            print('[AddThr7] Failed to compress data \n', e)
            return
        try:
            msg = f'{code}{data}{end}'
            self.parent.log.ser.add_to_outbuffer(msg)
        except Exception as e:
            print(f'[AddThr8] Failed to send msg: {msg} \n', e)

    @inner_runner
    def set_flight_mode_clicked(self, *args):
        self.set_flight_mode_signal.emit(
        {'callback':self.set_flight_mode})

    # Action to do after the new flightmode is set
    @inner_runner
    def set_flight_mode(self, *args, **kwargs):
        mode = self.parent.mm.dyn['flightmode']
        try:
            data = self.parent.mm.conf['flightmodes'][mode]
        except Exception as e:
            print(f'[AddThr9] Mode {mode} not found in configs!', e)
            return

        self.send_by_serial(data = data, code ='flightmode')

    @inner_runner
    def set_flight_target_clicked(self, *args):
        self.set_flight_target_signal.emit(
        {'callback':self.set_flight_target})

    # Action to do after the new flightmode is set
    @inner_runner
    def set_flight_target(self, *args, **kwargs):
        target = self.parent.mm.dyn['target']
        self.send_by_serial(data = target['x'], code ='tar_x')
        self.send_by_serial(data = target['y'], code ='tar_y')
        self.send_by_serial(data = target['h'], code ='tar_h')

    @inner_runner
    def set_flight_direction_clicked(self, *args):
        self.set_flight_direction_signal.emit(
        {'callback':self.set_flight_direction})

    # Action to do after the new flightmode is set
    @inner_runner
    def set_flight_direction(self, *args, **kwargs):
        target = self.parent.mm.dyn['direction']
        self.send_by_serial(data = target, code ='direction')

# Class responible for presenting data in Graphical format
# LiveFlightGui requires parrent (Main_Logic_Thread such as LiveFlight)

class LiveFlightGui(QRunnable):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

# Main GUI loop stated from main thread

    @pyqtSlot()
    def run(self):
        # Initializing data arrengers for both plots
        # Then adding all possible readings to plots
        da1 = self.parent.mm.dm.new_data_arranger('flight_time', 'temperature')
        self.parent.main_window.plot1.start_data_ploter(da1)
        da2 = self.parent.mm.dm.new_data_arranger('flight_time', 'temperature')
        self.parent.main_window.plot2.start_data_ploter(da2)
        possible_readings = self.parent.mm.conf['new_structure'].values()
        self.parent.main_window.plot2.set_possible_readings(possible_readings)
        self.parent.main_window.plot1.set_possible_readings(possible_readings)

        # Seting upper Menu
        self.parent.main_window.find_arduino_menu.triggered.connect(
        self.parent.af.restart_serial)
        self.parent.main_window.set_port_menu.triggered.connect(
        self.parent.af.set_port_menu)

        #Seting buttons
        self.parent.main_window.send_command_button.clicked.connect(
        self.parent.af.send_command_line)
        self.parent.main_window.find_point_button.clicked.connect(
        self.parent.af.find_point)
        self.parent.main_window.set_antena_loactio_button.clicked.connect(
        self.parent.af.set_antena_location_clicked)
        self.parent.main_window.set_flight_mode_button.clicked.connect(
        self.parent.af.set_flight_mode_clicked)
        self.parent.main_window.set_destination_button.clicked.connect(
        self.parent.af.set_flight_target_clicked)
        self.parent.main_window.set_direction_button.clicked.connect(
        self.parent.af.set_flight_direction_clicked)


        # Only functions inside inner loop are refreshed
        # ToDo: Check most efficent refresh time (if any sleep needed)

        while True:
            self.parent.main_window.plot1.update()
            self.parent.main_window.plot2.update()
            self.update_serial_status()
            self.parent.main_window.data_set_widget.refresh()
            # time.sleep(0.1)

    # Updates status of device conected by serial port
    # It takes connection_status from logic thread
    # Then updates port_status_label in main window
    # ToDo: Make sure it doesnt refreh to often in logic thread

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

# Class responible for logic operations durnig live flight
# LiveFlightLogic requires parrent (Main_Logic_Thread such as LiveFlight)

class LiveFlightLogic(QRunnable):

    # This __init__ is a mess
    # [v] ToDo: Find better way to initialize all this properties (maybe config)
    # New ToDo: Create methodes that dynamicly delivers requested data

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def keyPressEvent(self, event):
        pass
        # Might be useful in the future..

    def keyReleaseEvent(self, event):
        pass
        # Might be useful in the future...

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

    def newDataCallback(self, data):
        new_data = self.parent.mm.dm.append(data)
        self.parent.main_window.data_set_widget.update(**new_data)

        try:
            def RGBbyRSSI(rssi):
                rssi = abs(int(rssi))
                max_rssi = 255
                red, green = rssi, max_rssi - rssi
                red_h = str(hex(red))[2:]
                green_h = str(hex(green))[-2:]
                if len(red_h) == 1:
                    red_h = '0'+red_h
                if len(green_h) == 1:
                    green_h = '0'+green_h
                color = '#'+red_h+green_h+'00'
                return color

            self.parent.main_window.rocket_map.map_view.addPointToPath(
            new_data['X'], new_data['Y'], RGBbyRSSI(new_data['rssi'])
            )
        except Exception as e:
            print('[newDataCallback1]', e)

        try:
            if 'antena_location' in self.parent.mm.dyn:
                x = self.parent.mm.dyn['antena_location']['x']
                y = self.parent.mm.dyn['antena_location']['y']
                angle = self.parent.mm.dm.get_last(1)[0]['rotor_horizontal']
                print(x, y, angle)
                self.parent.main_window.rocket_map.map_view.setAntenaDirection(
                x, y, x, y)
        except Exception as e:
            print('[newDataCallback2]', e)

lf = LiveFlight()
lf.run()
