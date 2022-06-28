from serial import Serial
from constant import *




class Port:
    def __init__(self, serial_port, baud_rate, time_out):
        self.serial_port = serial_port
        self.time_out = time_out

    @property
    def check_serial_port_isopen(self):
        if self.serial_instance.isOpen():
            return True
        else:
            return False

    def write_port(self, data):
        if self.serial_instance.isOpen():
            self.serial_instance.write((data + return_carrier_r).encode())
            print(self.read_port)
            self.serial_instance.flush()
        else:
            self.serial_instance.close()

    @property
    def read_port(self):
        if self.serial_instance.isOpen():
            decode_answer = self.serial_instance.read(50).decode()
            return decode_answer
        else:
            return None
    def serial_port_open(self):
        if self.check_serial_port_isopen:
            return False
        else:
            self.serial_instance.applySettingsDict()



