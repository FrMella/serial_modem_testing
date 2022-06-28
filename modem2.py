from serial import Serial
import time, sys
import datetime


car_ret = '\n'



class Modem:
    def __init__ (self, input_string):
        self.input_string = input_string
        self.baud_rate = 115200
        self.time_out = 15
        #self.serial_port = serial_port
        #self.baud_rate = baud_rate
        #self.time_out = time_out

    def send_command(self):
        ser = Serial(self.serial_port, baudrate=self.baud_rate, timeout=self.time_out)
        #ser=Serial(self.serial_port, baudrate = self.baud_rate, timeout = self.time_out)
       
        print("a")
        #input = (self.inp + car_ret).encode()
        #if ser.inWaiting() > 0:
        #   ser.flushInput()
        #ser.timeout = 1
        #ser.write(input)
        #msg = ser.read(1024)
        #print(msg)