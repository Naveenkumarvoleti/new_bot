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
        GPIO.add_event_detect(22, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',22,300),bouncetime=10)
        GPIO.add_event_detect(26, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',26,60),bouncetime=10)
        GPIO.add_event_detect(5, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',5,0),bouncetime=10)
        GPIO.add_event_detect(6, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',6,120),bouncetime=10)
        GPIO.add_event_detect(19, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',19,180),bouncetime=10)
        GPIO.add_event_detect(17, GPIO.BOTH, callback=lambda x :detection(podLen,'spice',17,240),bouncetime=10)
    except RuntimeError:
        pass

def ingredientSetup(podLen):
    try:
        GPIO.add_event_detect(22, GPIO.BOTH, callback=lambda x :detection(podLen,'ingredient',22,300),bouncetime=10)
        GPIO.add_event_detect(26, GPIO.BOTH, callback=lambda x :detection(podLen,'ingredient',26,60),bouncetime=10)
        GPIO.add_event_detect(5, GPIO.BOTH, callback=lambda x :detection(podLen,'ingredient',5,0),bouncetime=10)
        GPIO.add_event_detect(6, GPIO.BOTH, callback=lambda x :detection(podLen,'ingredient',6,120),bouncetime=10)
        GPIO.add_event_detect(19, GPIO.BOTH, callback=lambda x :detection(podLen,'ingredient',19,180),bouncetime=10)
        GPIO.add_event_detect(17, GPIO.BOTH, callback=lambda x :detection(podLen,'ingredient',17,240),bouncetime=10)
    except RuntimeError:
        pass

def removeInterrupts():
    for (p,value),(p1,value1) in zip(spiceDict.items(), ingredientDict.items()):
        GPIO.remove_event_detect(p)
        GPIO.remove_event_detect(p1)
        
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
                    print('inserted')
                    if len(podDict)==podlen:
                        global trigStatus
                        trigStatus=True
                        print(podDict)
##                    print(podDict)
            else:
                if not len(ingredientPod)== 0:
                    del podDict[-1]
##                    print(podDict)
                    print("removed")
