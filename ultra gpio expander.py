##from pins import *
import time
##GPIO.setmode(GPIO.BCM)
import wiringpi

pinBase =65
i2cAddr = 0x20
wiringpi.wiringPiSetup()
wiringpi.mcp23017Setup(pinBase,i2cAddr)

TRIG = 78
retries=10
data=[]

def ultrasonic(ECHO):
    wiringpi.pinMode(TRIG,1)
    wiringpi.pinMode(ECHO,0)
    wiringpi.digitalWrite(TRIG, 1)
    time.sleep(0.1)
    wiringpi.digitalWrite(TRIG, 0)
    
    while wiringpi.digitalRead(ECHO)==0:
      pulse_start = time.time()
      
    while wiringpi.digitalRead(ECHO)==1:
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
    
while True:
    ultrasonic(77)
    time.sleep(1)
