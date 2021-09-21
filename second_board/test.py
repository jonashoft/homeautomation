
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def interrup_handler():
    print("button pressed")

if __name__ == '__main__':
    GPIO.add_event_detect(22, GPIO.BOTH, callback=interrup_handler, bouncetime=100)
    
