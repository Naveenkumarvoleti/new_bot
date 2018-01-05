import simpletest,led,loadcell,stepper,switches
import sys
import json
import RPi.GPIO as GPIO
from time import sleep
import os,glob
import subprocess
from threading import Thread, Event
import threading
import pins

global index
global value

#operationDictionary
operationDictionary= {}
#pod dictionary
ingredientPod=[]
spicePod= []
# Switching to high and stay for given time and switch to low

def gpio_high_low(pinNumber, timeInSeconds):
    GPIO.output(pinNumber,True)
    sleep(timeInSeconds)
    GPIO.output(pinNumber,False)

# Switching to low and stay for given time and switch to high
def gpio_low_high(pinNumber, timeInSeconds):
    GPIO.output(pinNumber,False)
    sleep(timeInSeconds)
    GPIO.output(pinNumber,True)

# Dispensing Liquids based on PumpSpeed
def dispense_liquid(pinNumber,quantity,pumpSpeed):
    totalDispensingTimeInSeconds = (quantity * pumpSpeed)/60
    gpio_high_low(pinNumber,totalDispensingTimeInSeconds)

#liftCookingLid
def liftCookingLid(time):
  stepper.start.stop()
  gpio_high_low(lidPin,time)
  stepper.start.forward(delay = 0.006)
  sleep(time)
  stepper.start.stop()
#closingCookingLid

def closecookingLid(time):
  stepper.start.stop()
  gpio_high_low(lidpin,time)
  stepper.start.backward()
  stepper.start.stop()
# Stirring
def stir(time):
    stepper.start.forward()
    sleep(time)
    stepper.start.stop()

# Dispensing Ingredients
def dispense_ingredient(dispence_pin,quantity):
    liftCookingLid()
    GPIO.output(dispence_pin,True)
    while True:
        if loadcell.get_weight(quantity) <= quantity:
            continue
        else:
            break
    GPIO.output(pinNumber,False)
    closeCookingLid()

class rice_cooker(threding.Thread):
  # Rice COOker
  def __init__(rice_pin):
    self.rice_pin = rice_pin
  def rice_cooker(self.rice_pin):
      for i in range(simpletest.temp_read(temperatureThreshold =100)):
        GPIO.output(rice_pin,True)
      GPIO.output(rice_pin,False)
#pan detect
def pan_detect():
    if panPin == 1:
        return 1

def induction(inductionPin):
    gpio_low_high(InductionPin,0.5)
#stepper rotation controll
#def pot_control(steps):
    #stepper.start.forward(steps)
    #sleep(0.1)
    #stepper.start.stop()

# spice pod Dectection
def spice_detect():
  for spice in range (8) #(OperationDictioary["no_of_spices"]):
    if sPod1:
      spicePod.insert(1)
      print("spice inserted in spice pod 1")
    elif sPod2:
      spicePod.insert(2)
      print("spice inserted in spice pod 2")
    elif sPod3:
      spicePod.insert(3)
      print("spice inserted in spice pod 3")
    elif sPod4:
      spicePod.insert(4)
      print("spice inserted in spice pod 4")
    elif sPod5:
      spicePod.insert(5)
      print("spice inserted in spice pod 5")
    elif sPod6:
      spicePod.insert(6)
      print("spice inserted in spice pod 6")
  return 1

#location detect:
def get_location(pin):
  print("getting location")
  stepper.start.pos_zero()
  stepper.start.move_to(angle=ingredient_pod[i])


# if pot >=0 and pot < 1.25:
#   pos = 0
# elif pot >= 1.25 and pot < 2.5:
#   pos = 1
# elif pot >= 2.5 and pot < 3.75:
#   pos = 2
# elif pot >= 3.75 and pot < 5:
#   pos = 3
# elif pot >= 5 and pot > 6.25:
#   pos = 4
# elif pot >= 6.25 and pot < 7.5:
#   pos = 5
# elif pot >= 7.5 and pot < 8.25:
#   pos = 6
# elif pot >= 8.25 and pot < 9.5:
#   pos = 7

# ingredient pod Detection
def pod_detect():
  for ingredient in range(8):
    if Pod1:
      ingredientPod.insert(0)
      print("ingredient inserted in spice pod 1")
    elif Pod2:
      ingredientPod.insert(60)
      print("ingredient inserted in spice pod 2")
    elif Pod3:
      ingredientPod.insert(120)
      print("ingredient inserted in spice pod 3")
    elif Pod4:
      ingredientPod.insert(180)
      print("ingredient inserted in spice pod 4")
    elif Pod5:
      ingredientPod.insert(240)
      print("ingredient inserted in spice pod 5")
    elif Pod6:
      ingredientPod.insert(360)
      print("ingredient inserted in spice pod 6")
  return 1

  #for x in range(operationDictionary["no_of_ingredients"]):
  #  while True:
  #    print"add ingredient to pod")
  #    pod.insert(GPIO_input())
  #  break
  #return 1
  #print("all ingredients inserted")

# Read the recipe file
def readRecipe(file):
  with open(file) as f:
    recipeData =json.loads(f.read())
    operationDictionary.update(recipeData)
    print(operationDictionary["human_readable_steps"])
  start_process(operationDictionary["process"])

# Diagnostic Cycle
# Check Pan is places, check the volume of water, check the spice quantities, check the rice cooker avaialble
# Min requirement of the each.
class sense(threading.Tread):
  def __init__(self,pan_pin,waterPin,oilPin):
    self.pan_pin=pan_pin
    self.water_pin=waterPin
    self.oil_pin=oilPin
  #sense glass wether placed or not
  def pan_sense(self,self.pan_pin):
    if pan_pin:
      print("pan is placed")
      led.run.onlight()
      return True
      break
    else:
      print("please place the pan")
      continue

  #lid detection
  def water_detect(self,self.waterPin):
    ultrasonic_level=Thread(target=ultrasonic,args=(pin_number=self.waterPin))
    ultrasonic.start()
    if level <= 5:
      led.run2.onlight()
      print("lid is opened. please close the lid"))
      return False
      continue
    else:
      led.run2.off_light()
      print("place the glass")
      return True
      break
  def oil_sense:
    ultrasonic_level=Thread(target=ultrasonic,args=(pin_number=self.oilPin))
    ultrasonic.start()
    if level <=8:
      return True:
      break
    else:
      print("fill oil container")
      return False
      continue
  while True:
    if pan_sense and water_detect and oil_sense == True:
      return True
    else:
      return False

# water level detection
class ultrasonic(Thread,pin_number):
    def __init__(self,TRIG=24, pin_number):
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(pin_number,GPIO.IN)
        self.stop= False

    def liquid_level(self):
        while not self.stop:
            GPIO.output(TRIG, True)
            time.sleep(0.001)
            GpIO.output(TRIG, False)

        while GPIO.input(pin_number)== 0:
            start_pulse= time.time()

        while GPIO.input(pin_number)== 1:
            stop_pulse= time.time()

            pulse_width = stop_pulse - start_pulse

            distance = pulse_width* 17150
            level = round(distance/2)
    while True:
      return level

#induction heat
class inductor(threading.thread,Temperature):
  def __init__(self,Temperature):
    self.Tempearture= temperature
  def induction_heat(self):
      if self.Temperature <= (simpletest.temp_read(temperatureThreshold =self.Temperature)):
        gpio_high_low(inductionPlusPin,0.2)
        print("induction heating")
      else:
        gpio_high_low(inductionMinusPin,0.2)

#start process
def start_process(operationDictionary):
  while True:
    sense.start():
      if True:
        for process in range(operationDictionary["no_of_operations"])
          value = 0
          if operationDictionary[value]["operation"] == "pre-heat":
            inductor_run = Thread(target= inductor,args=(operationDictionary[value]["temperature"]))

          elif operationDictionary[value]["operation"] == "dispense":
            if operationDictionary[value]["type"]== "spice":
              location(spice_pin,operationDictionary["quantity"])
              inductor_run = Thread(target= inductor,args=(operationDictionary[value]["temperature"]))
            else:
              location(ingredient_pin,operationDictionary["quantity"])
              inductor_run = Thread(target= inductor,args=(operationDictionary[value]["temperature"]))

          elif operationdictionary[value]["type"] == "water":
              dispance_liquid(waterPin,operationDictionary[value]["quantity"],100)

          elif operationdictionary[value]["type"] == "oil":
              dispance_liquid(oilPin,operationDictionary[value]["quantity"],100)

          elif operationDictionary[value]["operation"] == "stir":
            stir(operationDictionary[value]["time"])
          value+=1


if __name__ == '__main__':
  # List all files in the folder
  cook = raw_input("Do you want to cook rice or curry")
  if cook == "rice" or "Rice" or "RICE":
    rice_cooker.start()
  elif cock == "curry" or "Curry" or "CURRY":
    os.chdir(".")
    for file in glob.glob("*.json"):
        print(file)
    file = raw_input("Select a Recipe from the list: ")
    readRecipe(file)
    sense.start()
    ultrasonic_level =ultrasonic(pin_number)
    ultrasonic.start()
    inductor.start()
GPIO.cleanup()
sys.exit()
