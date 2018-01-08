import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
from pins import*
import pod_choosing as pod
import led,Test
from stepper_gpio_expander import stepper
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
from numpy import mean
import os.path
from loadcell import *
from progressbar import progress
import induction_controll_relay

global j
pumpSpeed = 100 #ml/min
##currentIngredientPos=0
##currentSpicePos=0
##                          

ingredients={}
spices={}
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
    wiringpi.digitalWrite(stirPin,1)
    time.sleep(0.5)
    start = stepper(dirPin,stepPin,200,defaultStepSpeed,sense_pin=stepperSensor)
    if metric == "min":
        finalTime = totalTime*60
        print(finalTime)
    else:
        finalTime = totalTime
        print(finalTime)
    closeTime=round(time.time())+finalTime
    print(round(closeTime))
    while round(time.time()) < closeTime:
        start.forward(1)
    start.stop()
    wiringpi.digitalWrite(stirPin,0)
    time.sleep(0.5)


def getLocation(pin,mode=None,name=None):
  start = stepper(dirPin,stepPin,200,defaultStepSpeed,sense_pin=stepperSensor)
  start1 = stepper(dirPin1,stepPin1,200,defaultStepSpeed,sense_pin=stepperSensor)
  print("getting location")
  print("engaging" ,pin)
  getLocationEvent = threading.Event()
  time.sleep(1)
  if mode=="ingredient":
      wiringpi.digitalWrite(pin,1)
      time.sleep(0.5)
      angle=ingredients[name]
      print("dict angle ",angle)
##      global currentIngredientPos
##      angle=ingredientPod[currentIngredientPos]
      print("moving to angle",angle)
##      currentIngredientPos+=1
      
      if start.move_to(angle):
          print("dis engaging" ,pin)
          wiringpi.digitalWrite(pin,0)
          print("reached location at", angle)
      
  elif mode=="spice":
      wiringpi.digitalWrite(pin,1)
      time.sleep(0.5)
##      GPIO.setup(dirPin1,GPIO.OUT)
##      GPIO.setup(stepPin1,GPIO.OUT)
      print(spices)
      angle=spices[name]
      print("dict angle ",angle)
##      global currentSpicePos
##      angle=spicePod[currentSpicePos]
      print("moving to angle",angle)
##      currentSpicePos+=1
      if start1.move_to(angle):
          print("dis engaging" ,pin)
          wiringpi.digitalWrite(pin,0)
          print("reached location at", angle)
      
  else:
      print("mode is not specified")
  time.sleep(0.5)


#closeCookingLid
def closeCookingLid(lidPos,liftSpeed=defaultStepSpeed):
  start = stepper(dirPin,stepPin,200,defaultStepSpeed,sense_pin=stepperSensor)
  start.stop()
  print("closing lid")
##  gpio_high_low(lidPin,time)
  wiringpi.digitalWrite(lidPin,1)
  time.sleep(0.5)
  if start.forward(lidPos):
      start.stop()
      print('lid closed')
  wiringpi.digitalWrite(lidPin,0)
  time.sleep(0.5)
  return True


#liftCookingLid
def liftCookingLid(lidPos,liftSpeed=defaultStepSpeed):
  start = stepper(dirPin,stepPin,200,liftSpeed,sense_pin=lidSensor)
  start.stop()
##  gpio_high_low(lidPin,time)
  wiringpi.digitalWrite(lidPin,1)
  time.sleep(0.5)
  if not GPIO.input(lidSensor):
      print("lifting lid")
##      start=stepper(delay=liftSpeed)
      start.backward(lidPos)
  print("lid opened")
  start.stop()
  wiringpi.digitalWrite(lidPin,0)
  time.sleep(0.5)
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
    start = stepper(dirPin,stepPin,200,defaultStepSpeed,sense_pin=stepperSensor)
    start1 = stepper(dirPin1,stepPin1,200,defaultStepSpeed,sense_pin=stepperSensor)
    if mode == 'spice':
        liftCookingLid(dispensePos)
        print("dispencing spice\n")
        load(1,'tare')
        while True:
##            GPIO.setup(dirPin1,GPIO.OUT)
##            GPIO.setup(stepPin1,GPIO.OUT)
            start1.forward(50)
            if load(1,'weight') > quantity:
                print("weight reached")
                start1.stop()
                break
        print("cleaning the suite")
        wiringpi.digitalWrite(cleaningPin,1)
        time.sleep(2)
        wiringpi.digitalWrite(cleaningPin,0)
    elif mode == 'ingredient':
        wiringpi.digitalWrite(dispensePin,1)
        print("dispencing ingredient\n")
        liftCookingLid(dispensePos)
        time.sleep(2)
        wiringpi.digitalWrite(dispensePin,0)
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
      print("yes")
      return True
    print("no")
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

#start process
def startProcess(operationDictionary):
##        start.stepper.pos_zero
##        induction_controll_relay.power("on")
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
                    getLocation(spicePin,mode="spice",name=d['ingredient'])
                    dispenseIngredient('spice',spicePin,d['value'])
                elif d['type']== 'water':
                    print('dispencing water')
                    dispenseLiquid(waterPin,d['value'],d['metric'])
            elif operation== 'stir':
                print('stirring')
                stir(d['time'],d['value'])
            time.sleep(1)
        print("curry Done")
        inductor_run = threading.Thread(target= inductor,args=(0,)).start()      
        
diagnosticsDict=[]
senDict=[]
class Diagnostics():
    # all positions setup
    # oil and water levels
    # temperature setting
    # 2 loadcells reset
    # cooking lid position
    #
    def __init__(self):
        self.cookingLidPos=None
##        self.senPin=sensor
##        self.waterSensor=waterSensor
##        self.tempSensor=tempSensor
##        self.cookingLid=None
##        self.cookingLid()
##        self.senLevel(self.oilSensor)
##        self.senlevel(self.WaterSensor)
##        self.ingredientRack()

    def slowClose(self,stepSpeed=retractionSpeed):
        print("getting default lid Position")
        closeCookingLid(defaultLidPos,stepSpeed)
        
    def cookingLid(self,stepSpeed=retractionSpeed):
        print("resetting lid position")
        while not self.cookingLid==0:
            start = stepper(dirPin,stepPin,200,defaultStepSpeed,sense_pin=lidSensor)
            if start.pos_zero()== True:
##                self.cookingLidPos=liftPos
                self.slowClose(stepSpeed)
                break
            else:
                continue
    def ingredientRack(self,stepSpeed=defaultStepSpeed):
        wiringpi.digitalWrite(ingredientPin,1)
##        start=stepper(delay=stepSpeed)
        print("resetting ingredient Rack")
        start = stepper(dirPin,stepPin,200,defaultStepSpeed,sense_pin=stepperSensor)
        if  start.pos_zero()== True:
            print("endstop triggered")
            print("stepper at start Pos")
        wiringpi.digitalWrite(ingredientPin,0)
        
    def senLevel(self,senPin,senLevel=None):
        for x in range(10):
            value=ultrasonic(senPin,senLevel)
            senDict.append(value)
##        print(senDict)
        if mean(senDict) > 1:
            print("{} sensor Working".format(senPin))
            return True
        else:
            print("{} sensor is not working".format(sensPin))
            return False
            
    def tempSense(self):
        data=measurement()
        for i in range(10):
            senDict.append(data)
            print(data)
        if mean(senDict)>float(0):
            print("current Temp: {}".format(data))
            del senDict[:]
            return True
        else:
            print("temp sensor not working")
            return False

    def diag(self):
        startTime=time.time()%60

        if self.tempSense():
            print("temp sensor working")
            diagnosticsDict.append(1)
        else:
            diagnosticsDict.append(2)
            
        if self.senLevel(oilSensor,minOilLevel):
            diagnosticsDict.append(1)
        else:
            print(" oil level Sensor is not Working")
            diagnosticsDict.append(2)
            
        if self.senLevel(waterSensor,minWaterLevel):
            diagnosticsDict.append(1)
        else:
            print("water level sensor is not working")
            diagnosticsDict.append(2)
            
        if mean(diagnosticsDict)==1:
            print(mean(diagnosticsDict))
            print("All sensors are working fine")
            return True
        else:
            return False
        
    

def podDetect(Dict):
    pod.removeInterrupts()
    for i in Dict.keys():
        try:
            for j in Dict[i]:
                if j in Dict['ingredients']:
                        choice=raw_input("Do you want to weigh {}. choose: y/n: ".format(j))
                        if choice=='y':
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
                        elif choice=='n':
                            pass
                        print ("put {} in {} rack.".format(j,i))
                        pod.trigStatus = False
                        pod.ingredientSetup(1)
                        while True:
                            if pod.trigStatus==True:
                                print('placed {} in the rack'.format(j))
                                ingredients[str(j)]=pod.ingredientPod[0]
                                print('ingredient Dict: ',ingredients)
    ##                            del ingredientPod[-1]
                                time.sleep(1)
                                break
                            else:
                                pass
                        pod.removeInterrupts()
                        
##                        else:
##                            print("choose your option")
####                            continue
                elif j in Dict['spices']: 
                    print ("put {} in the {} rack".format(j,i))
                    pod.trigStatus=False
                    pod.spiceSetup(1)
                    while True:
                        if pod.trigStatus==True:
                            print('placed {} in the rack'.format(j))
                            spices[str(j)]=pod.spicePod[0]
                            print('spice Dict: ',spices)
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


# Read the recipe file
def readRecipe(file,delay):
    time.sleep(delay)
    with open(file) as f:
        recipeData =json.loads(f.read())
        try:
            operationDictionary=dict(recipeData.items())
            print("making recipe {}".format(operationDictionary['name']))
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
##            isThreadAlive(startP)
            starting=raw_input('\ndo you want to start (y/n)')
            if starting=='y':
                startP.start()
            else:
                print("operation stopped")
##            if isThreadAlive(startP) == True:
##                print("already process running")
##            elif isThreadAlive(startP) == False:
##                print("steps to make "+ recipeData["name"])
##                print(operationDictionary["human_readable_steps"])
##                print(" ")
##                startP.start()



def totalTimeToComplete(file):
    pass



    
if __name__ == '__main__':
    print("Diagnostics Running")
    run=Diagnostics()
    run.cookingLid()
    run.ingredientRack()
##    run.senLevel(oilSensor)
##    run.senLevel(waterSensor)
##    run.tempSense()
    
    if run.diag()== True:
        print("diagnostics Done")
        while True:
            selection=raw_input("Do you want to start(y/n): ")
            if selection=="y":
               from gui import*
            elif selection=="n":
                print("skipped")
            else:
                print("choose right option")
                continue
    else:
        print("something went wrong")




        
##    sensorTest=threading.Thread(10.0,run.diag()).start()
##    if mean(diagnosticsDict)==1:
##        print("everyThing Working Fine")
##    else:
##        print("operation paused")
    
##    level=threading.Timer(10.0,ultrasonicDetection,args=(ultrasonicDictionary,)).start()
##    riceMaker=threading.Thread(target=cookRice,args=(temperature,delay,ricePin,riceWarmPin))
