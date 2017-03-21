import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

s = [0]
while(True):
    value = ser.readline()
    print(value)

