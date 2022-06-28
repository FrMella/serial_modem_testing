import serial


ser = serial.Serial('COM3', baudrate=115200, timeout=15)

if ser.isOpen():
    ser.write('AT#SS\r'.encode())
    ser.flush()
else:
    ser.close()

line = ser.read(200).decode()
print(line)


