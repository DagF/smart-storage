box = "s010"
import json
import time
import requests
from read_line import read_line, write

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

#box = "s003"
while (True):
    write('{"test":1}')
    value = read_line()
    print(value)
    if value:
        data = json.loads(value)
	
        print(data)
        if data.get('active'):
            r = post("activities/", {"box": box})
	if data.get('rfid'):
            r = post("rfid/", {"box": box, "value": data['rfid']})
	if data.get('weight'):
            r = post("weight/", {"box": box, "value": data['weight']})
    print(r)
    time.sleep(1)
