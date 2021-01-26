from flask import Flask, render_template, request, jsonify
from flask_mobility import Mobility
import time
import os
import logging 

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)


# Time between min and max = 4 seconds
DIMM_VALUE = 50

# Different states for the different lights
CEILING_LIGHT = 'on'
DESK_LAMP = 'on'
CHRISTMAS_LIGHT = 'on'

app = Flask(__name__)
Mobility(app)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html'), 200

@app.route('/relay', methods=['GET', 'POST'])
def relay_handler():
    state = request.args.get('state', type=str)
    lamp = request.args.get('light_source', type=str)
    light_state = {'On': 1, 'Off': 0}
    light_pin = {'desk': 11, 'chain': 13}
    GPIO.output(light_pin[lamp], light_state[state])
    return jsonify(result='Turned {} {}'.format(lamp, state))

@app.route('/background_process', methods=['GET', 'POST'])
def background_process():
    state = request.args.get('state', type=str)
    a = Lights(state)
    print('Turned {} : {}'.format(state, a))
    return jsonify(result='Turned {} : {}'.format(state, a))

@app.route('/dimm', methods=['GET', 'POST'])
def background_dimm():
    state = request.args.get('value', type=int)
    dimm(state)
    return jsonify(result='Dimmed')

@app.route('/on', methods=['GET'])
def turn_on_all():
    Lights('On')
    GPIO.output(11, 1)
    GPIO.output(13, 1)
    return jsonify(result='Turned all on')

@app.route('/off', methods=['GET'])
def turn_off_all():
    Lights('Off')
    GPIO.output(11, 0)
    GPIO.output(13, 0)
    return jsonify(result='Turned all off')

def Lights(state, delay=0.1):
    global CEILING_LIGHT
    CEILING_LIGHT = 'on'
    light_pin = {'On': 37, 'Off': 31}
    GPIO.output(light_pin[state], 1)
    time.sleep(delay)
    GPIO.output(light_pin[state], 0)
    return True

def dimm(dimm_value):
    global DIMM_VALUE
    
    if dimm_value < DIMM_VALUE:
        dimm = 4.5 / (100 / (DIMM_VALUE - dimm_value))
        Lights(state='Off', delay=dimm)
        DIMM_VALUE = dimm_value

    elif dimm_value > DIMM_VALUE and not dimm_value == 100:
        dimm = 4.5 / (100 / (dimm_value - DIMM_VALUE))
        Lights(state='On', delay=dimm)
        DIMM_VALUE = dimm_value

    elif dimm_value == 100:
        Lights(state='On', delay=4)
        DIMM_VALUE = 100

if __name__ == '__main__':
    GPIO.output(11, 1)
    GPIO.output(13, 1)
    Lights(state='Off', delay=4)
    Lights(state='On', delay=2)
    app.run(debug=True, port=3000, host='0.0.0.0')
