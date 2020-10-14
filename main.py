from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)

# Time between min and max = 4 seconds

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html'), 200

@app.route('/background_process')
def background_process():
    state = request.args.get('state', 0, type=str)
    print(state)
    if state == 'On':
        turnOnLights()
        return jsonify(result='Turned on')
    elif state == 'Off':
        turnOffLights()
        return jsonify(result='Turned off')

def turnOnLights():
    GPIO.output(37, 1)
    time.sleep(0.1)
    GPIO.output(37, 0)

def turnOffLights():
    GPIO.output(31, 1)
    time.sleep(0.1)
    GPIO.output(31, 0) 

if __name__ == '__main__':
    app.run(debug=True, port=80, host='192.168.0.107')