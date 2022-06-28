import time

from portlib import Port

time_found = False
i = 0

comm_port = 'COM3'
comm_AT_command = 'AT'
comm_baud_rate = 115200
comm_timeout = 15

port = Port(comm_port, comm_baud_rate, comm_timeout)
print("{} {} {} {}".format(comm_port, comm_baud_rate, comm_timeout, comm_AT_command))
response = 'OK\r'.encode()

while time_found == False:
    port.send_command('AT')
    response = port.recv_command
    while response != 'OK\r':
        response = port.recv_command
        time.sleep(0.2)
        ++i
        if i == 200:
            break
    if response == 'OK\r':
        time_found = True
    else:
        time.sleep(5)

print(response)
