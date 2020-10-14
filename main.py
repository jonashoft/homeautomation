from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('Turn On') == 'Turn On':
            turnOnLights()
            return render_template('index.html'), 200
        
        elif request.form.get('Turn Off') == 'Turn Off':
            turnOffLights()
            return render_template('index.html'), 200
    
    elif request.method == 'GET':
        return render_template('index.html')

def turnOnLights():
    GPIO.output(37, 1)
    time.sleep(0.1)
    GPIO.output(37, 0)

def turnOffLights():
    GPIO.output(31, 1)
    time.sleep(0.1)
    GPIO.output(31, 0) 

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')