#import serial
#ser = serial.Serial('/dev/ttyACM0', 9600)

#s = [0]
#while(True):
#    value = ser.readline()
#    print(value)
import json

token = "2567e7599f9ee43f567152ca954d482160566fb5"

import requests

def post(path, data):
    response = requests.post('http://dagfro.de:9000/api/box/'+path+'?format=json',
                            data = json.dumps(data),
                            headers={
                                'Authorization': 'token ' + token,
                                'Content-Type': 'application/json'
                            })
    print(response)
    print(response.content)

#post("box/", {"name": "test"})
#post("activities/", {"box": "test"})
#post("rfid/", {"box": "test", "value": "hex value"})