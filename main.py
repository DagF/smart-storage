from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)

import time
import os
import RPi.GPIO as GPIO
import threading
import json

# settings
SETTINGS_FILE = os.path.dirname(os.path.realpath(__file__)) + '/settings.json'

def create_settings_dict(
        project = "Nytt prosjekt",
        description = "Beskrivelse",
        ):
    return {
        "project": project,
        "description": description,
    }


def get_values_from_settings( settings  = create_settings_dict()):
    return settings.get("project"), settings.get("description")

def get_settings():
    try:
        with open(SETTINGS_FILE) as data_file:
            data = json.load(data_file)
            project, description = get_values_from_settings(data)
    except:
        save_settings_to_file(create_settings_dict())
        with open(SETTINGS_FILE) as data_file:
            data = json.load(data_file)
            project, description = get_values_from_settings(data)
    return project, description  

def save_settings_to_file(values):
    with open(SETTINGS_FILE , 'w') as outfile:
            json.dump(values, outfile) 

GPIO.setmode(GPIO.BCM)
DEBUG = 1

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 26
SPIMISO = 19
SPIMOSI = 13
SPICS = 6

RED_LED_1 = 16
RED_LED_2 = 20
RED_LED_3 = 21

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
GPIO.setup(RED_LED_1, GPIO.OUT)
GPIO.setup(RED_LED_2, GPIO.OUT)
GPIO.setup(RED_LED_3, GPIO.OUT)

# 10k trim pot connected to adc #0
potentiometer_adc = 0;

def indicateLoading():
    GPIO.output(RED_LED_1, GPIO.HIGH)
    time.sleep(1)
    print("led1")
    GPIO.output(RED_LED_1, GPIO.LOW)
    GPIO.output(RED_LED_2, GPIO.HIGH)
    print("led2")
    time.sleep(1)
    GPIO.output(RED_LED_2, GPIO.LOW)
    GPIO.output(RED_LED_3, GPIO.HIGH)
    print("led3")
    time.sleep(1)
    GPIO.output(RED_LED_3, GPIO.LOW)




def show_activity():
    GPIO.output(RED_LED_1, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(RED_LED_1, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(RED_LED_1, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(RED_LED_1, GPIO.LOW)

def watch_analog_input():
    last_input_value = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
    threshold = 10
    while(True):
        value = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
        if(abs(last_input_value - value) > threshold):
                show_activity()
        last_input_value = value
        time.sleep(1)
                
threading.Thread(target=watch_analog_input).start()




@app.route('/')
def hello_world():
    threading.Thread(target=indicateLoading).start()
    project, description = get_settings()
    current_value = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
    return render_template(
            'index.html',
            project =project,
            description=description,
            current_value=current_value)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        project = request.form.get("project")
        description = request.form.get("description")
        save_settings_to_file({"project" : project, "description": description})
        return redirect(url_for('hello_world'))
        
    project, description = get_settings()
    
    return render_template(
        "settings.html",
        project=project,
        description=description)

def startup():
    GPIO.output(RED_LED_1, GPIO.HIGH)
    GPIO.output(RED_LED_2, GPIO.HIGH)
    GPIO.output(RED_LED_3, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(RED_LED_2, GPIO.LOW)
    GPIO.output(RED_LED_1, GPIO.LOW)
    GPIO.output(RED_LED_3, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(RED_LED_1, GPIO.HIGH)
    GPIO.output(RED_LED_2, GPIO.HIGH)
    GPIO.output(RED_LED_3, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(RED_LED_2, GPIO.LOW)
    GPIO.output(RED_LED_1, GPIO.LOW)
    GPIO.output(RED_LED_3, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(RED_LED_1, GPIO.HIGH)
    GPIO.output(RED_LED_2, GPIO.HIGH)
    GPIO.output(RED_LED_3, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(RED_LED_2, GPIO.LOW)
    GPIO.output(RED_LED_1, GPIO.LOW)
    GPIO.output(RED_LED_3, GPIO.LOW)

if __name__ == '__main__':
    threading.Thread(target=startup).start()
    app.debug = True
    app.run(host='0.0.0.0', port=3000, use_reloader=True)
    
