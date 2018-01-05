import RPi.GPIO as GPIO
from pins import podPins
ingredientPod=[]
GPIO.setmode(GPIO.BCM)

for p in podPins:
    GPIO.setup(p, GPIO.IN)
    

def interrupts(mode,Type):
        global pods
        if mode=='ingredient':
            GPIO.add_event_detect(23, GPIO.BOTH, callback=lambda x :pod_detect(180,23))
            GPIO.add_event_detect(24, GPIO.BOTH, callback=lambda x :pod_detect(225,24))
            GPIO.add_event_detect(25, GPIO.BOTH, callback=lambda x :pod_detect(270,25))
            pods=Type
        elif mode== 'spice':
            GPIO.add_event_detect(12, GPIO.BOTH, callback=lambda x :pod_detect(180,23))
            GPIO.add_event_detect(13, GPIO.BOTH, callback=lambda x :pod_detect(225,24))
            GPIO.add_event_detect(14, GPIO.BOTH, callback=lambda x :pod_detect(270,25))
            pods=Type
            
def pod_detect(mode,angle,pin):          
        if not len(ingredientPod)== pods:
            if GPIO.input(pin):
                if angle in ingredientPod:
                    pass
                else:
                    ingredientPod.append(angle)
            else:
                if not len(ingredientPod)== 0:
                    del ingredientPod[-1]
        else:
            return True
