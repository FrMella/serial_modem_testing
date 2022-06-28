import serial
import time, sys
import datetime

i=0
time_found=False
response=''
SERIAL_PORT="COM3"
ser=serial.Serial(SERIAL_PORT, baudrate = 115200, timeout = 15)

while time_found==False:
        ser.write('AT'))
        response = ser.readline()
        while ('OK\n').encode() not in response:
                response=ser.readline()
                time.sleep(0.2)
                ++i
                if i==200:
                        break
        if ('OK\n').encode() in response:
                time_found=True
        else:
                time.sleep(20)

print (response)