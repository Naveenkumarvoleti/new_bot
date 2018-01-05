import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
ingredientPod=[]
spicePod=[]
spiceDict={1:0,2:45,3:90,4:135,5:180,6:225,7:270,8:315}
ingredientDict={9:0,10:60,11:120,12:180,13:240,14:300}

for (p, value),(p1, value1) in zip(spiceDict.items(),ingredientDict.items()):
     GPIO.setup(p,GPIO.IN)
     GPIO.add_event_detect(p, GPIO.BOTH, callback=lambda x :pod_detect(value,p))
     GPIO.add_event_detect(p1, GPIO.BOTH, callback=lambda x :pod_detect(value1,p1))

    
def interrupts(angle,pin):          
        if not len(ingredientPod)== pods:
            if GPIO.input(pin):
                if not angle in ingredientPod:
                    ingredientPod.append(angle)
            else:
                if not len(ingredientPod)== 0:
                    del ingredientPod[-1]
        else:
            return True


