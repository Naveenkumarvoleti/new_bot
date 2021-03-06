import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
TRIG = 6
global retries
retries=10
data=[]

def ultrasonic(ECHO,minLevel):
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO)==0:
      pulse_start = time.time()
##      print("pulse started")
      
    while GPIO.input(ECHO)==1:
      pulse_end = time.time()
##      print("pulse ended")

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150

    distance = round(distance, 2)
    if not distance==0 and distance < minLevel:
        print ("Level: %s cm" %(distance))
        return distance,True
    else:
        print("sensor failed")









##    if errorFinder(data)==0:
##        print("sensor working")
##    else:
##        print("sensor not working")

##def errorFinder(data):
##    if len(data)==retries:
##        reading=reduce(lambda x,y: x+y,data)/len(data)
##        if not reading < 0 or not reading > 10:
##            return 0
##        else:
##            return 1
##    else:
##        pass
##    print(distance)
    
##while True:
##    print("sensor 1 reading")
##    ultrasonic(13,500)
##    time.sleep(0.5)
##    print("sensor 2 reading")
##    ultrasonic(5,10)
##    time.sleep(0.5)
