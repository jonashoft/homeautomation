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
    global DIMM_VALUE
    if request.method == 'POST':
        if request.form.get('Turn on Lights') == 'Turn on Lights':
            turnOnLights()
            return render_template('index.html', dimm_value=DIMM_VALUE), 200
        
        elif request.form.get("Turn off Lights") == "Turn off Lights":
            turnOffLights()
            return render_template('index.html', dimm_value=DIMM_VALUE), 200
        
        elif request.form.get("Dimm") == "Dimm":
            dimm_value = request.form["Dimmer Value"]
            dimm(int(dimm_value))
            print('dimmed lights: ', int(dimm_value))
            return render_template('index.html', dimm_value=DIMM_VALUE), 200

        elif request.form.get("25") == "25":
            dimm(25)
            return render_template('index.html', dimm_value=DIMM_VALUE), 200

        elif request.form.get("50") == "50":
            dimm(50)
            return render_template('index.html', dimm_value=DIMM_VALUE), 200
        
        elif request.form.get("75") == "75":
            dimm(75)
            return render_template('index.html', dimm_value=DIMM_VALUE), 200
        
        elif request.form.get("100") == "100":
            dimm(100)
            return render_template('index.html', dimm_value=DIMM_VALUE), 200

    elif request.method == 'GET':
        return render_template('index.html', dimm_value=DIMM_VALUE), 200

@app.route('/background_process1')
def background_process():
    state = request.args.get('state', 0, type=str)
    print(state)
    if state == 'On':
        turnOnLights()
        return jsonify(result='Turned on')
    elif state == 'Off':
        turnOffLights()
        return jsonify(result='Turned off')

@app.route('/background_process2')
def background_process2():
    dimmerValue = request.form['DimmerValue']
    return jsonify({'response' : dimmerValue})

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
        dimm = 4 / (100 / (DIMM_VALUE - dimm_value))
        print('downto: ', dimm)
        turnOffLights(dimm)
        DIMM_VALUE = dimm_value

    elif dimm_value > DIMM_VALUE:
        dimm = 4 / (100 / (dimm_value - DIMM_VALUE))
        print('upto: ', dimm)
        turnOnLights(dimm)
        DIMM_VALUE = dimm_value

if __name__ == '__main__':
    turnOffLights(4)
    turnOnLights(2)
    app.run(debug=True, port=80, host='0.0.0.0')