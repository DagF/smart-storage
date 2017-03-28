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
    print("Emulated read_line()")

    def read_line():
        if randint(0, 9) == 2:
            return json.dumps({"active": True})
        if randint(0, 9) == 8:
            return json.dumps({"rfid": ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(16))})
        if randint(0, 9) == 7:
            return json.dumps({"weight": randint(1, 1000)})
        return None