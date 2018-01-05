import threading
import RPi.GPIO as GPIO
import time
from threading import Thread
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
class Sensor(object):

    """ultrasonic sensor continous distance reading at given interval in seconds"""
  
    def __init__(self,interval, gpio_trig, gpio_echo):    
        self.inter = interval
        self.trig = gpio_trig
        self.echo = gpio_echo	
	
        #set GPIO pins direction (IN / OUT)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)	
        threading.Thread.__init__(self)
        self.dist = 0        
        self.terminated = False
        self.run()
    
    def run(self):
        while not self.terminated:
            # set Trigger to HIGH
            GPIO.output(self.trig, True)
          
            # set Trigger to LOW after 0.01ms 
            time.sleep(0.00001)
            GPIO.output(self.trig, False)
          
            StartTime = time.time()
            StopTime = time.time()
          
            # save StartTime
            while GPIO.input(self.echo) == 0:
                StartTime = time.time()
          
            # save time of arrival
            while GPIO.input(self.echo) == 1:
                StopTime = time.time()
          
            # time difference between start and arrival
            TimeElapsed = StopTime - StartTime
            # multiply by sonic speed (34300 cm/s)
            # and divide by 2, because there and back
            self.dist = (TimeElapsed * 34300) / 2
          
            time.sleep(self.inter)

    def get_dist(self):
        return self.getdist

    def stop(self):
        self.terminated = True
        self.thread.join(1)
    
#Sensor object "instanciated" with GPIO programmable pins 23 and 24
SensorA = Sensor(interval=1, gpio_trig=13, gpio_echo=19)

while True:
    print(SensorA.get_dist())
##    SensorA.stop()
##try:
##    while True:
##        print("Measured Distance = %.1f cm" % SensorA.get_dist())
##except KeyboardInterrupt:
##    GPIO.cleanup()
##    SensorA.terminated = True
