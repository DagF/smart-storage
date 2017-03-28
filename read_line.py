import json

try:
    import serial
    ser = serial.Serial('/dev/ttyUSB1', 9600)
    s = [0]
    def write(w):
	ser.write(w)

    def read_line():
        return ser.readline().replace("'", '"')
except Exception as e:
    print(e)
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
