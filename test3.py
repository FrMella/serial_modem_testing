from _curses import baudrate
from serial import Serial
modem_config = {'port': 'COM3',
                'baudrate': 115200,
                'bytesize': 8,
                'parity': 'N',
                'stopbits': 1,
                'timeout': 15,
                'xonxoff': 0,
                'rtscts': 0}

print(modem_config)

#ser = Serial(modem_config)

# ser.write_port('ATZ')
# ser.write_port('ATZ')

# ftp init

buf = open('\s.txt', 'r')

# for line in buf:
#    print(buf.readline())

test = 0

if test != 1:
    print(ser.check_serial_port_isopen)


else:
    scriptList_A = ['AT#SGACT=1,0',
                    'AT#SGACT=1,1',
                    'AT+CGPADDR=',
                    'AT#FTPOPEN="172.16.10.81","IoTBuoy","pwd-C@wthr0nInst",0']

    for i in scriptList_A:
        ser.send_command(i)

    ser.transfer_data("s.txt", buf)
