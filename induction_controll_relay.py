import time
##import RPi.GPIO as GPIO
import threading
from threading import Thread, Event
from pins import *

temperatures=[35,50,100,130,160,170,190,200,220]
watts = [100, 300, 500, 800, 1000, 1100, 1200]
currentOutput=220
currentIndex=9
global powerState
global warmState
powerState=False
warmState= False

class induction(object):
    def __init__(self):
        self.__setup_gpio__()
        global powerState
        global warmState
    def __setup_gpio__(self):
##        GPIO.setmode(GPIO.BCM)
        wiringpi.pinMode(incrementPin,1)
        wiringpi.pinMode(decrementPin,1)
        wiringpi.pinMode(onOffPin,1)
        wiringpi.pinMode(warmPin,1)
        
    def power(self,mode):
        global powerState
        if mode == "on":
            if not powerState ==True:
                self.highLow(onOffPin)
                print("power on")
                powerState = not powerState
            else:
                print("already powerd on")
        elif mode =="off":
            if not powerState == False:
                self.highLow(onOffPin)
                print("power off")
                powerState = not powerState
            else:
               print(" already powered off") 
            
    def highLow(self,pinNumber):
        wiringpi.digitalWrite(pinNumber,True)
        time.sleep(0.1)
        wiringpi.digitalWrite(pinNumber,False)
        time.sleep(0.1)
        
    def fullHeat(self):
        if powerState== False:
            self.power("on")
            self.highLow(incrementPin)
        else:
            self.highLow(incrementPin)
        
    def increaseHeat(self,numberOfSteps):
        for i in range(numberOfSteps):
            self.highLow(incrementPin)
            
    def decreaseHeat(self,numberOfSteps):
        for i in range(numberOfSteps):
            self.highLow(decrementPin)
                        
    def warmMode(self,mode):
        global warmState
        if mode=="on":
            if not warmState== True:
                wiringpi.digitalWrite(warmPin,True)
                warmState= not WarmState
        elif mode == "off":
            self.power("off")

    def tempControll(self,temperature):
##        tempdata = self.tempCalc(temperature)
        if temperature != 0:
            self.fullHeat()
            for i,data in enumerate(temperatures):
                if temperature >= temperatures[i] and temperature <= temperatures[i+1]:
                    watt=watts[i]
                    temp=temperatures[i]
                    j=i+1
                    print("reaching nearest temperature" ,temp)
                    global currentIndex
                    if currentIndex < j:
                        print("increasing Temperature")
                        self.increaseHeat(j-currentIndex)
                    else:
                        print("decreasing Temperature")
                        self.decreaseHeat(currentIndex-j)
                    currentIndex=i
                    break
            else:
                print("current temperature not in list")
        else:
            self.power("off")

inductionControll = induction()

