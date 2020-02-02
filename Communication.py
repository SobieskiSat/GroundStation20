from serial import Serial

class SerialCommunicator:
    def __init__(self, port, baudrate = 115200, timeout = 1, **kwargs):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        try:
            self.serial = Serial(port, baudrate)
        except Exception as e:
            print('[Serial]', e)

    def readline(self):
        try:
            data=self.serial.readline()
            print(data)
            return data
        except Exception as e:
            pass
