from flask import Flask, render_template, request, jsonify
from flask_mobility import Mobility
import time
import os

deployedRasp = False

if os.uname()[0] == 'Linux':
    deployedRasp = True
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    pins = [11, 13, 31, 37] # desklamp, chain light, ceiling light on/off
    GPIO.setup(pins, GPIO.OUT)

# Time between min and max = 4 seconds
DIMM_VALUE = 50

app = Flask(__name__)
Mobility(app)

@app.route('/', methods=['GET'])
def home():
    if request.MOBILE:
        print('mobile request')
        return render_template('index_mobile.html'), 200
    else:
        print('other request')
        return render_template('index.html'), 200

@app.route('/relay', methods=['GET'])
def relay_handler():
    state = request.args.get('state', type=str)
    lamp = request.args.get('light_source', type=str)
    light_state = {'On': 1, 'Off': 0}
    light_pin = {'desk': 11, 'chain': 13}
    if deployedRasp:
        GPIO.output(light_pin[lamp], light_state[state])
    return jsonify(result='Turned {} {}'.format(lamp, state)), 200

@app.route('/ikea_lights', methods=['GET'])
def ikea_lights_handler():
    state = request.args.get('state', type=str)
    dimmValue = request.args.get('value', type=str)
    if state != None:
        a = Lights(state)
        print('Turned {} : {}'.format(state, a))
    if dimmValue != None:
        dimm(int(dimmValue))
        print('Dimmed {}'.format(dimmValue))
    return jsonify(result='Ok'), 200

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

def Lights(state, delay=0.1): # Default delay represents a click on the button
    light_pin = {'On': 37, 'Off': 31}
    if deployedRasp:
        GPIO.output(light_pin[state], 1)
        time.sleep(delay)
        GPIO.output(light_pin[state], 0)
        return False
    return True

if __name__ == '__main__':
    if deployedRasp:
        GPIO.output(11, 1)
        GPIO.output(13, 1)
    Lights(state='Off', delay=4)
    Lights(state='On', delay=2)
    app.run(debug=True, port=3000, host='0.0.0.0')
