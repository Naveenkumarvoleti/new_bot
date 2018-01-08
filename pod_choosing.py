import RPi.GPIO as GPIO
import time
##from led import Led
import random
from pins import*
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
global ingredientPod
global spicePod
ingredientPod=[]
spicePod=[]
trigStatus=False
##def ledControll(dictionary):
##    numbers=range(6)
##    random.shuffle(numbers)
##    for number in numbers:
##        start=Led(number)
##        start.on_light()

for (key,value) in ingredientDict.items():
    GPIO.setup(key,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    
for (key,value) in spiceDict.items():
    GPIO.setup(key,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    
def ledControll(dictionary):
    if dictionary == ingredientDict:
        angle= ingredientPod
    else:
        angle= spicePod
    global key
    global value
    for key,value in dictionary.iteritems():
        if value in enumerate(angle):
            continue
        else:
            start=Led(key)
            start.on_light()
            print("led "+str(key)+" on")
        break

##def aingredientSetup():
##    for (p, value) in ingredientDict.items():
##        print(p,value)
##        GPIO.add_event_detect(p, GPIO.BOTH, callback=lambda x :detection('ingredient',value,p),bouncetime=100)
####        ledControll(ingredientDict)
##        
##def spiceSetup():
##    for (p1, value1) in spiceDict.items():
####        GPIO.setup(p1,GPIO.IN)
##        GPIO.add_event_detect(p1, GPIO.BOTH, callback=lambda x :detection('spice',value1,p1),bouncetime=100)
####        ledControll(spiceDict)
    
def spiceSetup(podLen):
    try:
        GPIO.add_event_detect(20, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',20,60),bouncetime=300)
        GPIO.add_event_detect(16, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',16,120),bouncetime=300)
        GPIO.add_event_detect(12, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',12,180),bouncetime=300)
        GPIO.add_event_detect(25, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',25,240),bouncetime=300)
        GPIO.add_event_detect(24, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',24,300),bouncetime=300)
        GPIO.add_event_detect(23, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',23,360),bouncetime=300)
    except RuntimeError:
        pass

def ingredientSetup(podLen):
    try:
        GPIO.add_event_detect(20, GPIO.BOTH, callback=lambda x :detection(podLen,'ingredient',20,60),bouncetime=300)
        GPIO.add_event_detect(16, GPIO.BOTH, callback=lambda x :detection(podLen,'ingredient',16,120),bouncetime=300)
        GPIO.add_event_detect(12, GPIO.BOTH, callback=lambda x :detection(podLen,'ingredient',12,180),bouncetime=300)
        GPIO.add_event_detect(25, GPIO.BOTH, callback=lambda x :detection(podLen,'ingredient',25,240),bouncetime=300)
        GPIO.add_event_detect(24, GPIO.BOTH, callback=lambda x :detection(podLen,'ingredient',24,300),bouncetime=300)
        GPIO.add_event_detect(23, GPIO.BOTH, callback=lambda x :detection(podLen,'ingredient',23,360),bouncetime=300)
    except RuntimeError:
        pass

##def removeInterrupts():
##    for (p,value),(p1,value1) in zip(spiceDict.items(), ingredientDict.items()):
##        GPIO.remove_event_detect(p)
##        GPIO.remove_event_detect(p1)

def removeInterrupts():
        GPIO.remove_event_detect(20)#, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',20,60),bouncetime=300)
        GPIO.remove_event_detect(16)#, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',16,120),bouncetime=300)
        GPIO.remove_event_detect(12)#, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',12,180),bouncetime=300)
        GPIO.remove_event_detect(25)#, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',25,240),bouncetime=300)
        GPIO.remove_event_detect(24)#, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',24,300),bouncetime=300)
        GPIO.remove_event_detect(23)#, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',23,360),bouncetime=300)
    
    
def trigger():
    if trigStatus==True:
        return True
    else:
        return False

         
def detection(podlen,mode,pin,angle):
##    print(ingredientPod)
        global podDict
        if mode=='ingredient':
            podDict=ingredientPod
        elif mode=='spice':
            podDict = spicePod
        if not len(podDict) == 8:
            if GPIO.input(pin):
                if angle in podDict:
                    print('already inserted')
                else:
                    podDict.insert(0,angle)
##                    print('inserted')
                    if len(podDict)==podlen:
                        global trigStatus
                        trigStatus=True
                        print(podDict)
                    trigStatus=True
##                    print(podDict)
##            elif not len(ingredientPod)== 0:
####                    del podDict[-1]
####                    print(podDict)
##                    print("removed")
