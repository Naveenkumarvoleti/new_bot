from pins import*
from time import sleep
from ultra import ultrasonic

def ultrasonicDetection(ultrasonicDictionary):
  print("sensing")
  for u in ultrasonicDictionary: # including ultrasonic dictionary
      reading=ultrasonic(u)
      if reading > maxOilLevel and reading < minOilLevel:
          print("sensor failed or fill the oil container")
          print(reading)
      else:
          print("sensor working", reading)
          return True 
