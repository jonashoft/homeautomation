from flask import Flask, request, jsonify
from flask_cors import CORS
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup([16, 18], GPIO.OUT)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

desk = 0
chain = 0

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
    light_pin = {'desk': 16, 'chain': 18}
    GPIO.output(light_pin[lamp], light_state[state])
    return jsonify(result=f'Turned {lamp} {state}'), 200

def interrup_handler():
    global desk, chain
    deskState = 1 if desk == 0 else 0
    chainState = 1 if chain == 0 else 0
    GPIO.output(16, deskState)
    GPIO.output(18, chainState)
    request.get("http://192.168.0.101/toggle_lights")

if __name__ == '__main__':
    GPIO.output(16, 1)
    GPIO.output(18, 1)
    desk, chain = 1, 1
    GPIO.add_event_detect(22, GPIO.FALLING,callback=interrup_handler, bouncetime=100)
    app.run(port=3000, host='0.0.0.0')
