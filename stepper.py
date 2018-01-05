from time import sleep
import RPi.GPIO as GPIO
from pins import *
CW = 1
CCW = 0
GPIO.setwarnings(False)
GPIO.setup(dirPin1,GPIO.OUT)
GPIO.setup(stepPin1,GPIO.OUT)
class stepper():

    def __init__(self,dir_pin,step_pin,spr,delay,sense_pin):
        self.dir_pin= dir_pin
        self.step_pin= step_pin
        self.spr= spr
        self.delay= delay
        self.sense_pin = sense_pin
        self.__setup_gpio__()
        self.deg_per_step = 1.8  # for half-step drive (mode 3)
        self.steps_per_rev = int(360 / self.deg_per_step)  # 4096
        self.step_angle = 0  # Assume the way it is pointing is zero degrees
        self.kill = False
        
    def __setup_gpio__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.sense_pin,GPIO.IN)

    def forward(self,spr):
        GPIO.output(self.dir_pin, CCW)
        for x in range(int(round(spr))):
##            print("step: ",x)
            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(self.delay)
        self.stop()
        return True

    def backward(self,spr):
        GPIO.output(self.dir_pin, CW)
        for x in range(int(round(spr))):
##            print("step: ",x)
            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(self.delay)
        self.stop()
        return True

    def stop(self):
        GPIO.output(self.step_pin, GPIO.LOW)
        self.kill= True
            
    
    def both(self,spr):
        self.forward(spr)
        sleep(self.delay)
        self.backward(spr)
        sleep(self.delay)
        self.stop()
        return True
        
            
    def move_to(self, angle):
        prev_angle=0
        target_step_angle = angle/self.deg_per_step
        steps=round(target_step_angle - self.step_angle)
        steps = round((steps % self.steps_per_rev))
        if steps > self.steps_per_rev/2:
##        if angle < prev_angle:
            steps -= self.steps_per_rev
            print ("moving " + str(-steps) + " steps backward")
            self.backward(-(steps))
        else:
            print ("moving " + str(steps) + " steps forward")
            self.forward(steps)
        self.step_angle = target_step_angle
##        prev_angle= angle
        sleep(1)
        return True
    
    def pos_zero(self):
        print("moving to start pos")
        while not GPIO.input(self.sense_pin)==True:
            self.backward(self.spr)
##        else:
        self.stop()
        return True
            
start = stepper(dirPin,stepPin,200,defaultStepSpeed,stepperSensor)
start1 = stepper(dirPin1,stepPin1,200,defaultStepSpeed,stepperSensor)
