import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup([22, 24, 26], GPIO.IN)

def interrup_handler(channel):
    print(channel)
    print(type(channel))

if __name__ == '__main__':
    GPIO.add_event_detect(22, GPIO.FALLING, callback=interrup_handler, bouncetime=1500)
    GPIO.add_event_detect(24, GPIO.FALLING, callback=interrup_handler, bouncetime=1500)
    GPIO.add_event_detect(26, GPIO.FALLING, callback=interrup_handler, bouncetime=1500)
    # GPIO.add_event_detect(28, GPIO.FALLING, callback=interrup_handler, bouncetime=1500)
    while(1):
        pass
