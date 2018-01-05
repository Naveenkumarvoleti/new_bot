import time
import RPi.GPIO as GPIO
##from pins import*
import threading
from threading import Thread, Event
from pins import *
incrementPin=20
decrementPin=16
onOffPin=12
warmPin=21
fullHeatPin=25
temperatures=[35,50,100,130,160,170,190,200,220]
watts = [100, 300, 500, 800, 1000, 1100, 1200]
currentOutput=220
currentIndex=9
powerState=False
warmState= False

class induction(object):
    def __init__(self):
        self.__setup_gpio__()
        self.powerOn()
    def __setup_gpio__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(incrementPin,GPIO.OUT)
        GPIO.setup(decrementPin,GPIO.OUT)
        GPIO.setup(onOffPin,GPIO.OUT)
        GPIO.setup(fullHeatPin,GPIO.OUT)
        GPIO.setup(warmPin,GPIO.OUT)
        
    def powerOn(self,mode):
        if mode=="on":
            if not powerState == True:
                self.highLow(onOffPin)
                self.fullHeat()
                print("power on")
                global powerState
                powerState = not powerState
            else:
                print("induction power on")
        if mode == "off":
            if not powerState == False:
                self.highLow(onOffPin)
                
            
    def highLow(self,pinNumber):
        GPIO.output(pinNumber,True)
        time.sleep(0.1)
        GPIO.output(pinNumber,False)
        time.sleep(0.1)
        
    def fullHeat(self):
        self.highLow(fullHeatPin)
        
    def increaseHeat(self,numberOfSteps):
        for i in range(numberOfSteps):
            print("increasing Temperature")
            self.highLow(incrementPin)
            
    def decreaseHeat(self,numberOfSteps):
        for i in range(numberOfSteps):
            print("decreasing Temperature")
            self.highLow(decrementPin)
                        
    def warmMode(self):
        if not warmState == True:
            GPIO.output(warmPin,True)
            global warmState
            warmState= not WarmState
        else:
            print("warm mode active")
            
    def tempControll(self, mode,temperature):
        if mode =="turnOn":
            self.powerOn("on")
        elif mode ==" turnOff":
            self.powerOn("off")
            
    def tempControll(self,temperature):
##        tempdata = self.tempCalc(temperature)
        for i,data in enumerate(temperatures):
            print(data)
            print(i)
            if temperature >= temperatures[i] and temperature <= temperatures[i+1]:
                watt=watts[i]
                temp=temperatures[i]
                print("watts: ",watt)
                print("temperature: " ,temp)
                j=i+1
                if temperature != 0:
                    if warmState != True or powerState != False:
                        print("reaching nearest temprature" ,temp)
                        global currentIndex
                        if currentIndex < j:
                            self.increaseHeat(i-currrentIndex)
                        else:
                            self.decreaseHeat(currentIndex-j)
                        currentIndex=i
                        break
                    else:
                        print("warm mode active")
                        self.powerOn()
                else:
                    print("temperature reset to 0")
                    self.powerOn()
            else:
                print("current temperature not in list")

inductionControll = induction()

