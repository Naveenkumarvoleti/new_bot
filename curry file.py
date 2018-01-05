import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import sys
import json
import os,glob
import threading
import ttk
import os.path
import time
from time import sleep
import led,loadcell,Test,switches
from stepper import stepper
from pins import*
from progressbar import progress
from Tkinter import*


global index
global value


def gpio_high_low(pinNumber,timeInSeconds):
    wiringpi.digitalWrite(pinNumber,1)
    sleep(timeInSeconds)
    wiringpi.digitalWrite(pinNumber,0)

def gpio_low_high(pinNumber, timeInSeconds):
    wiringpi.digitalWrite(pinNumber,0)
    sleep(timeInSeconds)
    wiringpi.digitalWrite(pinNumber,1)

# Dispensing Liquids based on PumpSpeed
def dispenseLiquid(pinNumber,quantity):
    totalDispensingTimeInSeconds = (quantity*60)/pumpSpeed
    print(round(totalDispensingTimeInSeconds),"sec"," quantity: ",quantity,"ml")
    gpio_high_low(pinNumber,totalDispensingTimeInSeconds)

# Stirring
def stir(delay,value):
    if value == "min":
        finalTime = delay*60
        print(finalTime)
    else:
        finalTime = delay
        print(finalTime)
    closeTime=round(time.time())+finalTime
    print(round(closeTime))
    while round(time.time()) < closeTime:
        stepper.start.forward(1)
    stepper.start.stop()

def stepperMovement(mode,speed,spr=1):
    start = stepper(dir_pin=dirPin,step_pin=stepPin,spr=200,
                    delay=defaultStepSpeed,sense_pin=stepperSensor)
    if mode='forward':
        start.forward(spr)
    elif mode='backward':
        start.backwrad(spr)
    elif mode='both':
        start.both(spr)
    elif mode='
