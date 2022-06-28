from serial import Serial


class Port:

    def __init__(self, serial_comm, baud_rate, time_out):
        self.baud_rate = baud_rate
        self.timeout = time_out
        self.serial_buffer = Serial(serial_comm, baudrate=baud_rate, timeout=time_out)


    @property
    def connect(self):
        if self.serial_buffer.isOpen():
            Serial.print("Connected")
        else:
            raise Exception("Serial communication error")
        self.serial_buffer.flush()

    def send_command(self, input_string: object) -> object:
        input_string_encode = (input_string + '\n').encode()
        self.serial_buffer.write(input_string_encode)
        self.serial_buffer.flush()
        print(self.serial_buffer.readline())

    @property
    def recv_command(self):
        return str(self.serial_buffer.readline())
