from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)

# Time between min and max = 4 seconds
DIMM_VALUE = 50

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html'), 200

@app.route('/background_process', methods=['GET', 'POST'])
def background_process():
    state = request.args.get('state', 0, type=str)
    print(state)
    if state == 'On':
        turnOnLights()
        return jsonify(result='Turned on')
    elif state == 'Off':
        turnOffLights()
        return jsonify(result='Turned on')

@app.route('/dimm', methods=['GET', 'POST'])
def background_dimm():
    state = request.args.get('value', 0, type=int)
    dimm(state)
    return jsonify(result='Dimmed')

def turnOnLights(delay=0.1):
    GPIO.output(37, 1)
    print('turned on')
    time.sleep(delay)
    GPIO.output(37, 0)

def turnOffLights(delay=0.1):
    GPIO.output(31, 1)
    print('turned off')
    time.sleep(delay)
    GPIO.output(31, 0)

def dimm(dimm_value):
    global DIMM_VALUE
    
    if dimm_value < DIMM_VALUE:
        dimm = 4.5 / (100 / (DIMM_VALUE - dimm_value))
        turnOffLights(dimm)
        DIMM_VALUE = dimm_value

    elif dimm_value > DIMM_VALUE and not dimm_value == 100:
        dimm = 4.5 / (100 / (dimm_value - DIMM_VALUE))
        turnOnLights(dimm)
        DIMM_VALUE = dimm_value

    elif dimm_value == 100:
        dimm = 4.5 / (100 / (dimm_value - DIMM_VALUE))
        turnOnLights(4)
        DIMM_VALUE = 100

if __name__ == '__main__':
    turnOffLights(4)
    turnOnLights(2)
    app.run(debug=True, port=80, host='0.0.0.0')
