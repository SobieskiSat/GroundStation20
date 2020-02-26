from serial import Serial
import serial
from PyQt5.QtCore import QRunnable, pyqtSlot

class SerialCommunicator(QRunnable):
    def __init__(self, port, baudrate = 115200, timeout = 1, **kwargs):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.callbackFuns = []
        self.timeout = timeout
        try:
            self.serial = Serial(port, baudrate)
        except Exception as e:
            print('[Serial]', e)

    def readline(self):
        try:
            data=self.serial.readline()
            #return data
            return str(data)[2:-4]
        except Exception as e:
            print('[Serial]', e)

    def writeline(self, data):
        data = bytes(data)
        self.serial.write(data)

    def setOnReadCallback(self, fun):
        self.callbackFuns.append(fun)

    @pyqtSlot()
    def run(self):
        self.main_loop = True
        while self.main_loop:
            self.run_condition = True
            while self.run_condition:
                new = self.readline()
                for f in self.callbackFuns:
                    f(new)

class DeviceSearcher:
    def find_device_port(self):
        ports = serial.tools.list_ports.comports(include_links=False)
        print(ports)
    def tell_name(self):
        port = 'COM10'
        ser = Serial(port)
        print(ser.portstr)
        print(ser.name)

#ds = DeviceSearcher()
#ds.find_device_port()
