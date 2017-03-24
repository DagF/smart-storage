import json
import time
import requests
from read_line import read_line

token = "4e6af50e893a5064ac5b6200aa7bc3565c5f71c4"


def post(path, data):
    response = requests.post('http://0.0.0.0:8000/api/box/' + path + '?format=json',
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
    data = json.loads(value)

    print(data)
    if data['active']:
        post("activities/", {"box": "abc"})
    if data['rfid']:
        post("rfid/", {"box": "abc", "value": data['rfid']})

    time.sleep(1)
