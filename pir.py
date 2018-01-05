import RPi.GPIO as GPIO
import time

class pir(object):
    def __init__(self, pin_num,led_pin,seconds):
        self.pin_num= pin_num
        self.led_pin= led_pin
        self.seconds = seconds
        self.__setup_gpio__()

    def __setup_gpio__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_num, GPIO.IN)
        GPIO.setup(self.led_pin, GPIO.OUT)

    def Detect(self):
        i = GPIO.input(self.pin_num)
        if i==0:
            print("No one is here")
            GPIO.output(self.led_pin, 0)
            time.sleep(self.seconds)
        else:
            print("Detected")
            GPIO.output(self.led_pin, 1)
            time.sleep(self.seconds)

run = pir(pin_num= 25,led_pin= 16, seconds=1)

while True:
    run.Detect()
