from serial import Serial, portNotOpenError
import serial.tools.list_ports as lp
from PyQt5.QtCore import QRunnable, pyqtSlot

class SerialCommunicator(QRunnable):
    def __init__(self, port, baudrate = 115200, timeout = 0.03, **kwargs):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.callbackFuns = []
        self.buffer = set()
        self.timeout = timeout
        try:
            self.serial = Serial(port, baudrate, timeout=timeout)
        except Exception as e:
            print('[Serial] What we have here is the failure to communicate ;)', e)

    def reset_serial(self):
        print('reset')
        try:
            self.serial = Serial(self.port, self.baudrate, timeout=self.timeout)
        except Exception as e:
            pass

    def readline(self):
        try:
            data=self.serial.readline()
            #return data
            return str(data)[2:-4]
        except Exception as e:
             #print('[Serial]', e)
            pass
        except portNotOpenError as e:
            print('xff')

    def set_timeout(self, timeout):
        self.serial.timeout = timeout

    def writeline(self, data):
        data = bytes(data, 'utf-8')
        self.serial.write(data)

    def setOnReadCallback(self, fun):
        self.callbackFuns.append(fun)

    def add_to_outbuffer(self, *args):
        for a in args:
            self.buffer.add(str(a))

    def connection_status(self):
        if not hasattr(self, 'serial'):
            return 0
        if self.serial.isOpen():
            return 1
        return -1


    @pyqtSlot()
    def run(self):
        self.main_loop = True
        while self.main_loop:
            self.run_condition = True
            while self.run_condition:
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

    def tell_name(self):
        port = 'COM7'
        ser = Serial(port)
        print(ser.portstr)
        print(ser.name)
