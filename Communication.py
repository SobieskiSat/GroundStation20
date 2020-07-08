from serial import Serial, portNotOpenError
import serial.tools.list_ports as lp
from PyQt5.QtCore import QRunnable, pyqtSlot
import os

class SerialCommunicator(QRunnable):
    def __init__(self, baudrate = 115200, timeout = 0.03, **kwargs):
        super().__init__()
        self.baudrate = baudrate
        self.callbackFuns = []
        self.buffer = set()
        self.timeout = timeout

    def reset_serial(self):
        try:
            self.serial.close()
        except Exception as e:
            pass # Its fine, we have to make sure serial is closed
        if hasattr(self, 'serial'):
            delattr(self, 'serial')
        try:
            self.serial = Serial(self.port, self.baudrate, timeout=self.timeout)
            print(self.port)
        except Exception as e:
            print('[Serial2] What we have here is the failure to communicate ;\n',e)

    def readline(self):
        try:
            if not self.serial.is_open:
                return None
            data=self.serial.readline()
            #return data
            return str(data)[2:-4]
        except Exception as e:
             print('[Serial3]', e)
        except portNotOpenError as e:
            print('[serial4]', e)

    def set_timeout(self, timeout):
        self.serial.timeout = timeout

    def writeline(self, data):
        print('sending', data)
        data = bytes(data, 'utf-8')
        self.serial.write(data)

    def setOnReadCallback(self, fun):
        self.callbackFuns.append(fun)

    def add_to_outbuffer(self, *args):
        for a in args:
            self.buffer.add(str(a))
        print(self.buffer)

    def connection_status(self):
        if not hasattr(self, 'serial'):
            return 0
        if self.serial.isOpen():
            if os.path.exists(self.port):
                return 1
            return -2
        return -1


    @pyqtSlot()
    def run(self):
        self.main_loop = True
        while self.main_loop:
            self.run_condition = True
            while self.run_condition and hasattr(self, 'serial'):
                new = self.readline()
                if new:
                    for f in self.callbackFuns:
                        f(new)
                if self.buffer:
                    line = '<'
                    for b in self.buffer:
                        line += b
                    line += '>'
                    self.writeline(line)
                    self.buffer = set()

class DeviceSearcher:
    def find_device_port(self, name='Arduino M0'):
        ports = lp.comports(include_links=False)
        for p in ports:
            #print(p.description)
            if name in p.description:
                return p.device
        return None

    def list_ports(self):
        ports = lp.comports(include_links=False)
        ports = list(map(lambda p: p.device, ports))
        return ports
