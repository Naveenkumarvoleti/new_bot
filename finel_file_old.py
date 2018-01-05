import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
from pins import*
import led,loadcell,stepper,Test
from dsb18_temp import measurement
import sys
import json
from time import sleep
import os,glob
from threading import Thread, Event
import threading
from ultra import ultrasonic
global index
global value
import time
global lidPos
from Tkinter import*
import ttk
import os.path
import numpy as np
import gui
#operationDictionary
operationDictionary= {}

#pod dictionary
ingredientPod=[45,90,135,180,225,270,315,360]
spicePod= []
read=[]
pumpSpeed= 100 #ml/min
currentIngredientPos=0
currentSpicePos=0
global currentLidPos
currentLidPos=0
lock=threading.Lock()

# Switching to high and stay for given time and switch to low
##def gpio_high_low(pinNumber, timeInSeconds):
##    GPIO.output(pinNumber,True)
##    sleep(timeInSeconds)
##    GPIO.output(pinNumber,False)

def gpio_high_low(pinNumber,timeInSeconds):
    wiringpi.digitalWrite(pinNumber,1)
    sleep(timeInSeconds)
    wiringpi.digitalWrite(pinNumber,0)

# Switching to low and stay for given time and switch to high
##def gpio_low_high(pinNumber, timeInSeconds):
##    GPIO.output(pinNumber,False)
##    sleep(timeInSeconds)
##    GPIO.output(pinNumber,True)

def gpio_low_high(pinNumber, timeInSeconds):
    wiringpi.digitalWrite(pinNumber,0)
    sleep(timeInSeconds)
    wiringpi.digitalWrite(pinNumber,1)

# Dispensing Liquids based on PumpSpeed
def dispenseLiquid(pinNumber,quantity):
    totalDispensingTimeInSeconds = (quantity*60)/pumpSpeed
    print(round(totalDispensingTimeInSeconds),"sec"," quantity: ",quantity,"ml")
    gpio_high_low(pinNumber,totalDispensingTimeInSeconds)

# Rice cooker
def cookRice(temperature,delay):
  time.sleep(delay)
  print ("cooking Rice")
  if (Test.measurement(temperature)) <= 100:
##    GPIO.output(ricePin,True)
      wiringpi.digitalWrite(ricePin,1)
##  GPIO.output(ricePin,False)
##  GPIO.output(riceWarmPin,True)
  wiringpi.digitalWrite(ricePin,0)
  wiringpi.digitalWrite(riceWarmPin,1)
  print("rice cooking done")
  print("warm mode active")


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


#location detect:
def getLocation(pin,mode=None):
  print("getting location")
##  GPIO.output(pin,True)
  wiringpi.digitalWrite(pin,1)
  getLocationEvent = threading.Event()
  time.sleep(1)
  try:
      if mode=="ingredient":
          global currentIngredientPos
          angle=ingredientPod[currentIngredientPos]
          currentIngredientPos+=1
      elif mode=="spice":
          global currentSpicePos
          angle=spicePod[currentSpicePos]
          currentSpicePos+=1
      if stepper.start.move_to(angle):
          print("reached location at", angle)
          getLocationEvent.set()
      else:
          getLocationEvent.clear()
  except IndexError:
      pass
  if IndexError:
      print("please insert pods")
##      popupmsg(msg="please insert pods and start again",Type=1,st=NORMAL)
##  GPIO.output(pin,False)
  wiringpi.digitalWrite(pin,0)

#liftCookingLid
def liftCookingLid(lidPos):
  stepper.start.stop()
  print("lifting lid")
  if currentLidPos !=0:
      currentLidPos=lidPos-currentLidPos
  while not stepper.start.forward(lidPos):
      print("lid moving up")
  print("lid readched final pos")
  stepper.start.stop()


def lidZeroPos(lidEndPin):
    while not GPIO.input(lidEndPin)== True:
        stepper.start.forward()
    print("lid position gained")
    global currentLidPos
    currentLidPos=0
    stepper.start.stop()

#closingCookingLid
def closeCookingLid(lidPos):
  stepper.start.stop()
##  gpio_high_low(lidPin,time)
  while not GPIO.input(liftStop)==True:
      stepper.start.backward(liftPos)
  stepper.start.forward(closePos)
  print("closing lid")
  stepper.start.stop()


# Dispensing Ingredients
##def dispenseIngredient(dispensePin,quantity):
##    liftCookingLid(dispensePos)
##    print("lid reached at final position")
##    print("weighing")
##    if not loadcell.get_weight(quantity):# < quantity == True:
####      GPIO.output(dispensePin,True)
##        wiringpi.digitalWrite(dispensePin,1)
##    else:
####      GPIO.output(dispensePin,False)
##        wiringpi.digitalWrite(dispensePin,0)
##      time.sleep(1)
##      closeCookingLid(closePos)

def dispenseIngredient(mode=None,dispensePin,quantity):
    if mode== 'spice':
        wiringpi.digitalWrite(dispensePin,1)
        print("spice pin connected\n")
        if loadcell.get_weight(quantity):
            break
    elif mode== 'ingredient':
        wiringpi.digitalWrite(dispencePin,1)
        time.sleep(2)
        

def isThreadAlive(name):
    if name.isAlive():
      return True
    else:
      return False

# Read the recipe file
def readRecipe(file,delay):
  time.sleep(delay)
  with open(file) as f:
    recipeData =json.loads(f.read())
    operationDictionary.update(recipeData)
    print("no of operations to be done :" + str(recipeData["no_of_operations"]))
    print(" ")
    global operations
    operations=(operationDictionary["no_of_operations"])
##  if podDetect and sense == True:
##    popupmsg(msg="Are you sure",st=NORMAL,cmd=startProcess(operationDictionary["process"]))
    startTest = threading.Thread(target=startUp,args=(operationDictionary,)).start()
    startP=threading.Thread(target=startProcess,args=(operationDictionary["process"],))

    if isThreadAlive(startP) == True:
        print("already process running")
    else:
        print("steps to make "+ recipeData["name"])
        print(operationDictionary["human_readable_steps"])
        print(" ")
        startP.start()

def startUp(dictionary):
  if stepper.start.pos_zero():
    return "position zero: ok"
  if lidZeroPos():
    return "position Zero: ok"
  if getUltrasonicReading(oilPin):
    return "oil Level: ok"
  if getUltrasonicReading(waterPin):
    return "water Level: ok"

#induction heat
def inductor(temperature=0): # hardware control mode
  gpio_high_low(inductionOnOff,0.2)
  while True:
      temp = Test.measurement(temperature)
      if temperature == temp:
          print("temperature reached")
          break
##      temp = dsb18_temp.measurement
      if temperature > temp:
        print(temp)
        gpio_high_low(inductionPlusPin,0.2)
        print("induction heating up")
        time.sleep(1)
      elif temperature < temp:
        gpio_high_low(inductionMinusPin,0.2)
        print("induction heating down")
        time.sleep(1)

def getWeight():
  weight=loadcell.get_weight()
  return weight

##def inductor(temperature=0):
##  if getCurrentTemp()> tempearature:
##      send(highTempData)
##  else:
##      send(lowTempData)

def averageFind(dictionary):
    avg = np.mean(dictionary)
    return avg

def ultrasonicDetection(ultrasonicDictionary):
  print("sensing")
  for u in ultrasonicDictionary: # including ultrasonic dictionary
      reading=getUltrasonicReading(u)
      print(reading)
      return reading
      read.append(reading)
  if averageFind(read) > avgSensorValue:
      print("sensor is not working")
  else:
      print("sensor is working")

def getUltrasonicReading(pinNo):
    return ultrasonic(pinNo)

def getSensorReading(pinNo,sensorType=None):
  pass

class diagnostics():
    def __init__(self,pinNo=None,dictionary=None,mode=None,avgvalue=0):
        self.pinNo = pinNo
        self.dictionary=dictionary
        self.mode=mode
        read=[]

    def avreageFind(self):
      avg=np.mean(self.dictionary)
      return avg

    def ultrasonicTest(self):
      self.averageFind(self.dictionary)
      if avg > avgValue:
        print(" sensor is not working")
      else:
        print("sensor is working")

    def lidTest(self,avgTimeToComplete):
      currentTime=time.timenow()
      if stepper.start.pos_zero():
        currentTime=round(currentTime-time.timenow())
        if currentTime > avgTimeTComplete:
          print("lid endstop is problem")
        else:
          print("lid endstop is working")
        return True
      else:
        return False




##      if reading < minOilLevel and minWaterLevel:
##          print("oil is not enough, checkreading: " + str(reading))
##          popupmsg(msg="oil level"+ str(reading))
##          lock.acquire()
##      elif reading < minWaterLevel:
##          print("water is not enough, check reading: "+str(reading))
##          popupmsg(msg="water level"+ str(reading))
##          lock.acquire()
##      else:
##          print(str(reading))
##          lock.release()
##          popupmsg.configure(st=NORMAL)


##def waterLevel():

#start process
def startProcess(operationDictionary):
##  while True:
##    sense.wait()
    print("running process")
    i = 0
    gpio_low_high(inductionOnOff,0.2)
    if stepper.start.pos_zero() == True:
##### process count starts from here ####
        for i in range(operations):
          if operationDictionary[i]["operation"] == "heat":
            print("preheat running")
            inductor_run = threading.Thread(target= inductor,args=(operationDictionary[i]["temperature"],))
            inductor_run.start()
            inductor_run.join()

          elif operationDictionary[i]["operation"] == "dispense":
            if operationDictionary[i]["type"]== "spice":
              print("getting location of spice")
              getLocation(spicePin,mode="spice")
              dispenseIngredient(mode='spice',spicePin,operationDictionary[i]["value"])
            elif operationDictionary[i]["type"]== "ingredient":
              print("getting location ingredient")
              getLocation(ingredientPin,mode="ingredient")
              dispenseIngredient(mode='ingredient',ingredientPin,operationDictionary[i]["value"])

            elif operationDictionary[i]["type"] == "water":
                  print("pouring water")
                  dispenseLiquid(waterPin,operationDictionary[i]["value"])
            elif operationDictionary[i]["type"] == "oil":
                  print("dispensing oil")
                  dispenseLiquid(oilPin,operationDictionary[i]["value"])


          elif operationDictionary[i]["operation"] == "stir":
              print("stirring")
              stir(operationDictionary[i]["time"],operationDictionary[i]["value"])
          i+=1
        print("curry done")
        gpio_low_high(inductionOnOff,0.2)
    else:
      print("stepper is not moving or sensor is not working")


print("insert ingredients as per recipe")
def pod_detect(angle,pin):
        if not len(ingredientPod)== 3:
            if GPIO.input(pin):
                if angle in ingredientPod:
                    pass
                else:
                    ingredientPod.append(angle)
                    print("xxxx inserted in pod")
            else:
                if not len(ingredientPod)== 0:
                    del ingredientPod[-1]
        else:
            print("all ingredients inserted starting process")
            return True



if __name__ == "__main__()":
    level=threading.Timer(10.0,ultrasonicDetection,args=(ultrasonicDictionary,)).start()
    try:
        GPIO.add_event_detect(23, GPIO.BOTH, callback=lambda x :pod_detect(180,23),bouncetime=100)
        GPIO.add_event_detect(24, GPIO.BOTH, callback=lambda x :pod_detect(225,24),bouncetime=100)
        GPIO.add_event_detect(25, GPIO.BOTH, callback=lambda x :pod_detect(270,25),bouncetime=100)

        lidZeroPos(lidEndPin)

    except KeyboardInterrupt:
      print("cleaning everything")
      GPIO.cleanup()
      sys.exit()
