from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup([16, 18], GPIO.OUT)

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/', methods=['GET'])
def home():
    return "use main board's front-end", 200

@app.route('/relay', methods=['GET'])
def relay_handler():
    state = request.args.get('state', type=str)
    lamp = request.args.get('light_source', type=str)
    light_state = {'On': 1, 'Off': 0}
    light_pin = {'desk': 11, 'chain': 13}
    GPIO.output(light_pin[lamp], light_state[state])
    return jsonify(result='Turned {lamp} {state}'), 200

if __name__ == '__main__':
    GPIO.output(16, 1)
    GPIO.output(18, 1)
    app.run(port=3000, host='0.0.0.0')