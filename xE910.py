# Import native pyboard libraries
import pyb, time, machine, ujson, ure, micropython
from machine import UART
from pyb import RTC
from machine import I2C
# Import Cawthron specific libraries
import config, i2cgps
from ds3231 import DS3231
from i2cgps import I2CGPS

i2c = I2C('X', freq=400000)
RTC_RH_Pwr = pyb.Pin(config.RTC_RH_Pwr, pyb.Pin.OUT_PP, pyb.Pin.PULL_DOWN)
RTC_RH_Pwr.high()
time.sleep_ms(100)
ds3231 = DS3231(i2c)

micropython.alloc_emergency_exception_buf(
    100)  # Allows error messages to be displayed from the timer interrupt if there are any
rtc = pyb.RTC()
xE910 = UART(config.xE910UART, config.xE910Baud)  # Creates xE910 object so all other methods can work
xE910_3V8reg = pyb.Pin(config.xE910_3V8reg, pyb.Pin.OUT_PP, pyb.Pin.PULL_DOWN)  # 3.8V regulator which powers the xE910
xE910Pwr = pyb.Pin(config.xE910Pwr, pyb.Pin.OUT_PP, pyb.Pin.PULL_DOWN)  # Switches power to the xE910
xE910_ON_OFF = pyb.Pin(config.xE910_ON_OFF, pyb.Pin.OUT_PP, pyb.Pin.PULL_DOWN)  # xE910 on/off control pin
xE910.init(config.xE910Baud)
timer2Flag = False  # Flag that goes high during a timeout when communicating with the xE910
timer = pyb.Timer(
    2)  # Create a timer object using timer 2.  Note this is a 32bit timer.  Not all PYB timers are 32bit and won't work for longer delays
error = False  # Flag that gets raised if communication times out and exceeds retries


def debugWrite(message):
    currDT = ds3231.get_time()
    # Write debug message to file
    debug = open(config.debugFile, 'a')
    debug.write(
        "{:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d}".format(currDT[2], currDT[1], currDT[0], currDT[3], currDT[4],
                                                           currDT[5]) + "\t")
    debug.write(str(message) + "\r\n")
    debug.close()
    pyb.sync()


def timer2(self):  # Timer2 interrupt routine.
    global timer2Flag
    timer2Flag = True


def power(value):  # Turn modem on and off.  Value can be 'on' or 'off
    if (value == 'on'):
        xE910_3V8reg.low()
        xE910Pwr.high()
        print('Turning on xE910')
        print('Holding ON/OFF pin HIGH')
        xE910_ON_OFF.high()
        time.sleep(6)
        print('Released ON/OFF pin')
        xE910_ON_OFF.low()
    if (value == 'off'):
        print('Turning off xE910')
        print('Holding ON/OFF pin HIGH')
        xE910_ON_OFF.high()
        time.sleep(6)
        print('Released ON/OFF pin')
        xE910_ON_OFF.low()
        xE910Pwr.low()
        xE910_3V8reg.low()
        RTC_RH_Pwr.high()  # Turn off DS3231 RTC


def xE910Write(data, checkString, retries, timeout):
    """Sends data to the xE910.  Checks for response from xE910 and compares it to 'checkString'.  Number of retries and a timeout for each retry can be specified.  If no
    'checkString is specified it will just write the data to the xE910 and not check for a response"""
    global error
    found = False
    global timer2Flag
    loop = 0
    if error:  # There has been an error in one of the transmissions to the xE910.  Don't transmit any more.  Wait for the next cycle for reset
        print("There was an error in transmission")
        return False
    print('Entered xE910 Write')
    while True:
        timer.deinit()
        time.sleep(1)
        timer.init(freq=(1 / timeout))  # trigger timer when the timeout period has elapsed
        timer.callback(timer2)  # Defining the callback for the timer interrupt
        if (checkString == None):  # If checkString is None then just write to the xE910 without checking for a response
            xE910.write(data)
            print('CheckString was none')
            break
        if (loop > retries):
            debugWrite(
                'Failed to get response from xE910 after ' + str(loop - 1) + ' retries' + ' while sending: ' + str(
                    data) + 'aborting transmission and shutting down xE910')
            print('Exceeded Retries: ' + str(loop - 1) + ' While sending: ' + str(
                data) + ' aborting transmission and shutting down xE910')
            error = True
            break
        xE910.write(data)
        print('Loops= ' + str(loop))
        print('Entered checkResponse, looking for string: ' + checkString)

        while True:
            time.sleep(0.5)
            xE910Response = str(xE910.read())
            print('xE910Response: ' + str(xE910Response))
            print('timer2Flag =' + str(timer2Flag))
            print('timerCounter= ' + str(timer.counter()))
            if (timer2Flag):
                print('Timeout on loop: ' + str(loop))
                timer2Flag = False
                break
            if (xE910Response != None):
                if (ure.search(checkString, xE910Response)):
                    print('Found " {} " in xE910Response'.format(checkString))
                    found = True
                    break
        if (found):
            break
        loop += 1


def read():  # Reads data from the xE910s UART
    xE910_response = xE910.read()
    return xE910_response


def checkResponse(checkString):
    print('Entered checkResponse, looking for string: ' + checkString)
    while True:
        xE910Response = xE910.read()
        if (xE910Response != None):
            # print('xE910Response = '+xE910Response)
            if (ure.search(checkString, xE910Response)):
                print('Found {} in xE910Response'.format(checkString))
                return True
                break

            time.sleep(1)


def FTP_Init():  # Powers off then on the xE910, gets an ip address, opens and FTP connection and changes the working directrory
    global error
    print("Turning xE910 power on")
    power('on')
    xE910Write('AT\r', 'OK', 2, 5)
    print('Sending AT#SGACT')
    xE910Write('AT#SGACT=1,0\r', 'OK', 2, 5)
    xE910Write('AT#SGACT=1,1\r', 'OK', 2, 10)
    print('Sending AT+CGPADDR')
    xE910Write('AT+CGPADDR=\r', '192.168.150', 2, 20)  # Get Ip address from Caw APN
    print('Sending AT#FTPOPEN')
    xE910Write(
        'AT#FTPOPEN=' + (config.xE910FTP_site) + ',' + (config.xE910Username) + ',' + (config.xE910Password) + '\r',
        'OK', 2, 30)
    print('Sending AT#FTPCWD')
    xE910Write('AT#FTPCWD=' + (config.xE910WorkingDir) + '\r', 'OK', 2, 20)
    if (error):
        debugWrite('Error in FTP init Loop')
        print("Error in FTP init loop")
        return False
    print("FTP_Init was a success")
    return True


def FTP(filename, data):  # Sends a file via FTP.  FTP_Init() must have been run once before this runs

    global error
    print('Sending AT#FTPAPP')
    xE910Write('AT#FTPAPP=' + '"' + filename + '"' + ',0\r', 'CONNECT', 2, 20)
    print('Connection successful.  Ready to FTP data:')
    time.sleep(5)
    print('Sending Data...')
    xE910Write(data, None, 0, 30)
    print('Sending Carriage Return')
    xE910Write('\r\n', None, 0, 20)
    print('Sending +++')
    time.sleep(0.5)
    xE910Write('+++', 'NO CARRIER', 0, 20)
    if (error):
        debugWrite('Error in FTP Loop')
        print("Error in FTP loop")
        return False
    print("FTP was a success")
    return True


def FTP_Shutdown():  # Closes FTP connection and shuts down the xE910
    global error
    print('Sending AT#FTPCLOSE')
    xE910Write('AT#FTPCLOSE\r', 'OK', 2, 20)
    print('Sending AT#SHDN [Disconnect APN & Perform Software Shutdown]')
    xE910Write('AT#SHDN\r', 'OK', 2, 20)
    time.sleep(15)
    power('off')
    if (error):
        debugWrite('Error in FTP_Shutdown Loop')
        print("Error in FTP_Shutdown Loop")
        error = False
        return False
    print("FTP_Shutdown was a success")
    return True