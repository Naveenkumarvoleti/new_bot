import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
TRIG = 6
retries=10
data=[]

def ultrasonic(ECHO):
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO)==0:
      pulse_start = time.time()
      
    while GPIO.input(ECHO)==1:
      pulse_end = time.time()


    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)
    if not distance==0:
        print ("Level: %s cm" %(distance))
        return distance
    else:
        print("sensor failed")

def errorfinder(data):
    if len(data)==retries:
        reading=reduce(lambda x,y: x+y,data)/len(data)
        if not reading < 0 or not reading > 10:
            return 0
        else:
            return 1
    else:
        pass
    print(distance)
