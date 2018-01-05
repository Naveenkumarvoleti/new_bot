import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
global index
global value

ingredientPod=[]
spicePod= []
sp_sw=[1,2,3,4,5,6,7,8]
in_sw=[16,20,21]

def spice_detect():
  inPut = 0
  while inPut <= (8):
    for i in sp_sw:
      print(i)
      spicePod.append(GPIO.input(i))

#location detect:
def get_location(pin):
  print("getting location")
  stepper.start.pos_zero()
  stepper.start.move_to(angle=ingredient_pod[i])

def pod_detect():
   inPut = 0
   while inPut <= (3):
     print("add ingredient to pod")
     for i in in_sw:
       print (i)
       GPIO.setup(i,GPIO.IN)
       ingredientPod.append(GPIO.input(i))
   return 1
   print("all ingredients inserted")

def switch(threading.thread):
  for p in in_sw:
    GPIO.setup(p,GPIO.IN)
pod_detect()
time.sleep(0.1)
print(ingredientPod)
