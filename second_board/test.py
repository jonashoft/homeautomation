
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def interrup_handler(channel):
    print("button pressed")

if __name__ == '__main__':
    GPIO.add_event_detect(22, GPIO.BOTH, callback=interrup_handler, bouncetime=100)
    while True:
        time.sleep(0.1)
    
