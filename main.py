

from flask import Flask, request, render_template, redirect, url_for
from flask import make_response

app = Flask(__name__)

import time
import threading
from utils import read_adc, load_settings, save_settings, load_image, save_image

DEBUG = 1

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler


RED_LED_1 = 16
RED_LED_2 = 20
RED_LED_3 = 21

# GPIO.setup(RED_LED_1, GPIO.OUT)
# GPIO.setup(RED_LED_2, GPIO.OUT)
# GPIO.setup(RED_LED_3, GPIO.OUT)

# 10k trim pot connected to adc #0
potentiometer_adc = 0


def indicateLoading():
    # GPIO.output(RED_LED_1, GPIO.HIGH)
    time.sleep(1)
    print("led1")
    # GPIO.output(RED_LED_1, GPIO.LOW)
    # GPIO.output(RED_LED_2, GPIO.HIGH)
    print("led2")
    time.sleep(1)
    # GPIO.output(RED_LED_2, GPIO.LOW)
    # GPIO.output(RED_LED_3, GPIO.HIGH)
    print("led3")
    time.sleep(1)
    # GPIO.output(RED_LED_3, GPIO.LOW)


def show_activity():
    # GPIO.output(RED_LED_1, GPIO.HIGH)
    time.sleep(0.5)
    # GPIO.output(RED_LED_1, GPIO.LOW)
    time.sleep(0.5)
    # GPIO.output(RED_LED_1, GPIO.HIGH)
    time.sleep(0.5)
    # GPIO.output(RED_LED_1, GPIO.LOW)


def watch_analog_input():
    last_input_value = read_adc(potentiometer_adc)
    threshold = 10
    while (True):
        value = read_adc(potentiometer_adc)
        if (abs(last_input_value - value) > threshold):
            show_activity()
        last_input_value = value
        time.sleep(1)


# threading.Thread(target=watch_analog_input).start()


@app.route('/')
def hello_world():
    threading.Thread(target=indicateLoading).start()
    settings = load_settings()
    current_value = read_adc(potentiometer_adc)
    return render_template(
        'index.html',
        settings=settings,
        current_value=current_value)


@app.route("/image.jpg")
def getImage():
    image = load_image()
    response = make_response(image)
    response.headers['Content-Type'] = 'image/jpeg'
    response.headers['Content-Disposition'] = 'attachment; filename=img.jpg'
    return response


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        save_settings({
            "project": request.form.get("project"),
            "description": request.form.get("description"),
            "owner": request.form.get("owner"),
            "number": request.form.get("number")
        })
        save_image(request.files['image'])
        return redirect(url_for('hello_world'))

    settings = load_settings()

    return render_template(
        "settings.html",
        settings=settings)


def startup():
    pass
    # GPIO.output(RED_LED_1, GPIO.HIGH)
    # GPIO.output(RED_LED_2, GPIO.HIGH)
    # GPIO.output(RED_LED_3, GPIO.HIGH)
    # time.sleep(0.5)
    # GPIO.output(RED_LED_2, GPIO.LOW)
    # GPIO.output(RED_LED_1, GPIO.LOW)
    # GPIO.output(RED_LED_3, GPIO.LOW)
    # time.sleep(0.5)
    # GPIO.output(RED_LED_1, GPIO.HIGH)
    # GPIO.output(RED_LED_2, GPIO.HIGH)
    # GPIO.output(RED_LED_3, GPIO.HIGH)
    # time.sleep(0.5)
    # GPIO.output(RED_LED_2, GPIO.LOW)
    # GPIO.output(RED_LED_1, GPIO.LOW)
    # GPIO.output(RED_LED_3, GPIO.LOW)
    # time.sleep(0.5)
    # GPIO.output(RED_LED_1, GPIO.HIGH)
    # GPIO.output(RED_LED_2, GPIO.HIGH)
    # GPIO.output(RED_LED_3, GPIO.HIGH)
    # time.sleep(0.5)
    # GPIO.output(RED_LED_2, GPIO.LOW)
    # GPIO.output(RED_LED_1, GPIO.LOW)
    # GPIO.output(RED_LED_3, GPIO.LOW)


if __name__ == '__main__':
    threading.Thread(target=startup).start()
    app.debug = True
    app.run(host='0.0.0.0', port=3000, use_reloader=True)
