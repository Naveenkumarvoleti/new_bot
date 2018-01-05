import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
from pins import*
import pod_choosing as pod
import led,stepper,Test
##from dsb18_temp import measurement
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
import os.path
from loadcell import *
from progressbar import progress
import induction_controll_relay
from gui import*
global j
pumpSpeed = 100 #ml/min
currentIngredientPos=0
currentSpicePos=0

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
    sleep(0.5)
    
# Switching to low and stay for given time and switch to high
##def gpio_low_high(pinNumber, timeInSeconds):
##    GPIO.output(pinNumber,False)
##    sleep(timeInSeconds)
##    GPIO.output(pinNumber,True)

def gpio_low_high(pinNumber, timeInSeconds):
    wiringpi.digitalWrite(pinNumber,0)
    sleep(timeInSeconds)
    wiringpi.digitalWrite(pinNumber,1)
    sleep(0.5)

# Dispensing Liquids based on PumpSpeed
def dispenseLiquid(pinNumber,quantity,metric):
    quantity = quantity*14 if metric == 'tbsp' else quantity
    totalDispensingTimeInSeconds = (quantity*60)/pumpSpeed
    print("Dispencing for {} sec quantity: {}ml".format(round(totalDispensingTimeInSeconds),quantity))
    gpio_high_low(pinNumber,totalDispensingTimeInSeconds)


# Stirring
def stir(totalTime,metric):
    if metric == "min":
        finalTime = totalTime*60
        print(finalTime)
    else:
        finalTime = totalTime
        print(finalTime)
    closeTime=round(time.time())+finalTime
    print(round(closeTime))
    while round(time.time()) < closeTime:
        stepper.start.forward(1)
    stepper.start.stop()


def getLocation(pin,mode=None,name=None):
  print("getting location")
  print("engaging" ,pin)
  getLocationEvent = threading.Event()
  time.sleep(1)
  if mode=="ingredient":
      wiringpi.digitalWrite(pin,1)
      angle=ingredients[name]
      print("dict angle ",angle)
##      global currentIngredientPos
##      angle=ingredientPod[currentIngredientPos]
      print("moving to angle",angle)
      currentIngredientPos+=1
      
      if stepper.start.move_to(angle):
          print("disengaging" ,pin)
          wiringpi.digitalWrite(pin,0)
          print("reached location at", angle)

      
  elif mode=="spice":
      wiringpi.digitalWrite(pin,1)
      GPIO.setup(dirPin1,GPIO.OUT)
      GPIO.setup(stepPin1,GPIO.OUT)
      angle=spices[name]
      print("dict angle ",angle)
##      global currentSpicePos
##      angle=spicePod[currentSpicePos]
      print("moving to angle",angle)
      currentSpicePos+=1

      if stepper.start1.move_to(angle):
          print("disengaging" ,pin)
          wiringpi.digitalWrite(pin,0)
          print("reached location at", angle)
      
  else:
      print("mode is not specified")


#closeCookingLid
def closeCookingLid(lidPos):
  stepper.start.stop()
  print("closing lid")
##  gpio_high_low(lidPin,time)
  if stepper.start.forward(lidPos):
      stepper.start.stop()
      print('lid closed')
  return True


#liftCookingLid
def liftCookingLid(lidPos):
  stepper.start.stop()
##  gpio_high_low(lidPin,time)
  if not GPIO.input(liftStop):
      print("lifting lid")
      stepper.start.backward(lidPos)
  print("lid opened")
  stepper.start.stop()
  return True

## get weight
def load(loadcell,mode):
    if loadcell==1:
         if mode=='weight':
            print(hx.get_weight(5))
            return hx.get_weight(5)
         elif mode=='reset':
            return hx.reset()
         elif mode=='tare':
            return hx.tare()
    elif loadcell==2:
         if mode=='weight':
            return hx1.get_weight(5)
         elif mode=='reset':
            return hx1.reset()
         elif mode=='tare':
            return hx1.tare()
    
### Dispensing Ingredients
def dispenseIngredient(mode,dispensePin,quantity):
    if mode == 'spice':
        liftCookingLid(dispensePos)
        print("dispencing spice\n")
        load(1,'tare')
        while True:
            GPIO.setup(dirPin1,GPIO.OUT)
            GPIO.setup(stepPin1,GPIO.OUT)
            stepper.start1.forward(50)
            if load(1,'weight') > quantity:
                print("weight reached")
                stepper.start1.stop()
                break
    elif mode == 'ingredient':
        wiringpi.digitalWrite(dispensePin,1)
        print("dispencing ingredient\n")
        liftCookingLid(dispensePos)
        time.sleep(2)
        wiringpi.digitalWrite(dispensePin,1)
##        load(1,'tare')
##        while True:
##            if load(1,'weight') > quantity:
##                print("weight reached")
##    ##            time.sleep(2)
##                wiringpi.digitalWrite(dispensePin,0)
##                break
    closeCookingLid(closePos)

def isThreadAlive(name):
    if name.isAlive():
      return True
    return False
      

#induction heat
def inductor(temperature=0): # hardware control mode
    inductionControll= induction_controll_relay.induction()
    if temperature == 0:
        inductionControll.tempControll("off")
    elif temperature == 1:
        inductionControll.tempControll("on")
    elif temperature > 1:
        inductionControll.tempControll(temperature)
    return True
        
def startBoth(file,riceType):
    rice=threading.Thread(target=cookRice,args=(riceType,)).start()
    readRecipe(file)
    
def ultrasonicDetection(ultrasonicDictionary):
  print("sensing")
  for u in ultrasonicDictionary: # including ultrasonic dictionary
      reading=ultrasonic(u)
      if reading > maxOilLevel and reading < minOilLevel:
          print("sensor failed or fill the oil container")
          print(reading)
      else:
          return True

#start process
def startProcess(operationDictionary):
##        start.stepper.pos_zero
        for d in operationDictionary:
            operation=d['operation']
            if operation == 'heat':
                print('heating {}'.format(d['temperature']))
                inductor_run = threading.Thread(target= inductor,args=(d['temperature'],)).start()
    ##            inductor_run.join()
            elif operation== 'dispense':
                if d['type']=='oil':
                    print('dispencing oil')
                    dispenseLiquid(oilPin,d['value'],d['metric'])
                elif d['type']=='ingredient':
                    print('getting ingredient location')
                    getLocation(ingredientPin,mode="ingredient",name=d['ingredient'])
                    dispenseIngredient('ingredient',ingredientPin,d['value'])
                elif d['type']== 'spice':
                    print('getting spice location')
                    getLocation(spicePin,mode="spice")
                    dispenseIngredient('spice',spicePin,d['value'])
                elif d['type']== 'water':
                    print('dispencing water')
                    dispenseLiquid(waterPin,d['value'],d['metric'])
            elif operation== 'stir':
                print('stirring')
                stir(d['time'],d['value'])
            time.sleep(1)
        print("curry Done")
                          

ingredients={}
spices={}
def podDetect(Dict):
    for i in Dict.keys():
        try:
            for j in Dict[i]:
                if j in Dict['ingredients']:
                    print("weigh the "+ str(j)+ " in weight scale")
                    x=0
                    while True:
                        if x==0:
                            if load(1,'weight')>10:
                                x=1
                            else:
                                pass
                        else:
                            if load(1,'weight')< 2:
                                break
                            else:
                                continue
                    print ("put {} in {} rack.".format(j,i))
                    pod.trigStatus = False
                    pod.ingredientSetup(1)
                    while True:
                        if pod.trigStatus==True:
                            print("placed {} in the rack".format(j))
                            ingredients[str(j)]=ingredientPod[0]
                            print("ingredient Dict: ",ingredients)
##                            del ingredientPod[-1]
                            time.sleep(1)
                            break
                        else:
                            continue
##                    pod.removeInterrupts()
                    
                elif j in Dict['spices']: 
                    print ("put {} in {} rack".format(j,i))
                    pod.trigStatus=False
                    pod.spiceSetup(1)
                    while True:
                        if pod.trigStatus==True:
                            print("placed {} in the rack".format(j))
                            spices[str(j)]=spicePod[0]
                            print("spice Dict: ",spices)
##                            del spicePod[-1]
                            time.sleep(1)
                            break
                        else:
                            continue
                pod.removeInterrupts()            
        except TypeError:
            pass
    print("all ingredients inserted")
    pod.removeInterrupts() 
    return True


##operationDictionary={}
# Read the recipe file
def readRecipe(file,delay):
    time.sleep(delay)
    with open(file) as f:
        recipeData =json.loads(f.read())
        try:
            operationDictionary=dict(recipeData.items())
            print(operationDictionary)
        except AttributeError:
            operationDictionary=dict(recipeData.iteritems())
##            print(operationDictionary)
        print("no of operations to be done :" + str(operationDictionary['no_of_operations']))
        print(" ")
        global operations
        operations=operationDictionary['no_of_operations']
        runTime = ((operationDictionary['totalCookingTimeInMinutes']) + (operationDictionary['totalHandsOnTimeInMinutes']))*60
        if podDetect(operationDictionary) == True:
            preview=threading.Thread(target=progress,args=(runTime,)).start()
            startP=threading.Thread(target=startProcess,args=(operationDictionary["process"],))
            if isThreadAlive(startP) == True:
                print("already process running")
            elif isThreadAlive(startP) == False:
                print("steps to make "+ recipeData["name"])
                print(operationDictionary["human_readable_steps"])
                print(" ")
                startP.start()
    
if __name__ == '__main__':
    level=threading.Timer(10.0,ultrasonicDetection,args=(ultrasonicDictionary,)).start()
##    riceMaker=threading.Thread(target=cookRice,args=(temperature,delay,ricePin,riceWarmPin))
