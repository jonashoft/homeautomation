from flask import Flask, request, jsonify
from flask_cors import CORS
import RPi.GPIO as GPIO
# import requests

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup([16, 18], GPIO.OUT)
GPIO.setup([22, 24, 26, 32], GPIO.IN)

# desk, chain = 0, 0

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/', methods=['GET'])
def home():
    return "use main board's front-end", 200

@app.route('/relay', methods=['GET'])
def relay_handler():
    global desk, chain
    state = request.args.get('state', type=str)
    lamp = request.args.get('light_source', type=str)
    light_state = {'On': 1, 'Off': 0}
    light_pin = {'desk': 16, 'chain': 18}
    # if light_pin[lamp] == 16:
    #     desk = light_state[state]
    # elif light_pin[lamp] == 18:
    #     chain = light_state[state]
    GPIO.output(light_pin[lamp], light_state[state])
    return jsonify(result=f'Turned {lamp} {state}'), 200

def interrup_handler(channel):
    global desk, chain
    if channel == 24:
        deskState = 1 if desk == 0 else 0
        chainState = 1 if chain == 0 else 0
        GPIO.output(16, deskState)
        GPIO.output(18, chainState)
        desk, chain = deskState, chainState
    elif channel == 22:
        requests.get("http://192.168.0.101:3000/toggle_lights")
    elif channel == 26:
        requests.get("http://192.168.0.101:3000/toggle_ikea")
    elif channel == 32:
        requests.get("http://192.168.0.101:3000/toggle_desk")


if __name__ == '__main__':
    GPIO.output(16, 1)
    GPIO.output(18, 1)
    desk, chain = 1, 1
    GPIO.add_event_detect(22, GPIO.FALLING, callback=interrup_handler, bouncetime=1500)
    GPIO.add_event_detect(24, GPIO.FALLING, callback=interrup_handler, bouncetime=1500)
    GPIO.add_event_detect(26, GPIO.FALLING, callback=interrup_handler, bouncetime=1500)
    GPIO.add_event_detect(32, GPIO.FALLING, callback=interrup_handler, bouncetime=1500)

    app.run(port=3000, host='0.0.0.0')
