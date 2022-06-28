def send_command(self, command):
    if self.serial_instance.isOpen():
        print("Sending Command {} through port {}".format(command, self.serial_port))
        command_concat = str(command)
        self.serial_instance.write(command_concat.encode())
        # self.serial_instance.flush()
        response_from_modem = self.read_port
        print(response_from_modem)
    else:
        print("Port {} is not open".format(self.serial_port))
        self.serial_instance.close()


def encode_command(input_encode):
    input_encoded = input_encode.encode()
    return input_encoded

def decode_command(input_decoded):
    input_decoded = input_decoded.decode()
    return input_decoded


def transfer_data(self, filename, buffer):
    address_directory = ('AT#FTPCWD=' + 'test2').encode()
    self.send_command(address_directory)
    self.send_command('AT#FTPAPP=' + '"' + filename + '"' + ',0')
    data_buffer = buffer.readline()
    for lines in buffer:
        self.serial_instance.write(data_buffer.encode())
        print(data_buffer.encode())
    self.send_command('\r\n')
    self.send_command('+++')
