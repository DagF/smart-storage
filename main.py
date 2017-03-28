import json
import time
import requests
from read_line import read_line

token = "2567e7599f9ee43f567152ca954d482160566fb5"


def post(path, data):
    response = requests.post('http://dagfro.de:9000/api/box/' + path + '?format=json',
                             data=json.dumps(data),
                             headers={
                                 'Authorization': 'token ' + token,
                                 'Content-Type': 'application/json'
                             })
    print(response)
    print(response.content)

    # post("box/", {"name": "test"})
    # post("activities/", {"box": "test"})
    # post("rfid/", {"box": "test", "value": "hex value"})


while (True):
    value = read_line()
    if value:
        data = json.loads(value)

        print(data)
        if data.get('active'):
            post("activities/", {"box": "abc"})
        if data.get('rfid'):
            post("rfid/", {"box": "abc", "value": data['rfid']})
        if data.get('weight'):
            post("weight/", {"box": "abc", "value": data['weight']})

    time.sleep(1)
