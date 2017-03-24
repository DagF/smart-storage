import json

try:
    import serial
    ser = serial.Serial('/dev/ttyACM0', 9600)
    s = [0]


    def read_line():
        return ser.readline()
except:
    from random import randint, choice
    import string


    def read_line():
        active = False
        rfid = ""
        if randint(0, 9) == 2:
            active = True
        if randint(0, 9) == 8:
            rfid = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(16))
        return json.dumps({"active": active, "rfid": rfid})