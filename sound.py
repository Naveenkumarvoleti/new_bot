import RPi.GPIO as GPIO
import time

channel = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
GPIO.setup(21, GPIO.OUT)

def callback(channel):
        if GPIO.input(channel):
                print ("Sound Detected!")
                GPIO.output(21, True)
        else:
                print ("Sound not Detected!")
                GPIO.output(21, False)
                

while True:
        callback(channel)
        time.sleep(1)
