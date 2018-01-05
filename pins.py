import RPi.GPIO as GPIO
import wiringpi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
from ConfigParser import SafeConfigParser

pinBase =65
i2cAddr = 0x20
wiringpi.wiringPiSetup()
wiringpi.mcp23017Setup(pinBase,i2cAddr)

config = SafeConfigParser()
config.read('config.ini')


spicePod=[45,90,135,180,225,270,315,360]
ingredientPod=[60,120,180,240,300,360]
incrementPin=20
decrementPin=16
onOffPin=12
warmPin=21

spicePin=68
ingredientPin=69
oilPin=70
waterPin=71

loadcellA=15
loadcellB=18
lidPin=73
liftStop=24
dirPin = 11
stepPin=9
dirPin1=14
stepPin1=23
stepperSensor=5
defaultStepSpeed=0.0028 #ms/step


spiceDict={4:360, 5:45, 6:90, 7:135, 8:180, 10:225, 14:270, 27:315}
ingredientDict={22:300,26:60, 5:360, 6:120, 19:180, 17:240}

out_pins=[15,16,14,23,9,11]
outPinsWiringpi=[65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80]
in_pins =[4,5,6,7,8,10,12,13,16,17,19,27,20,21,22,24,25]
ultrasonicDictionary=[10]
dispensePos=200
closePos=200
##
liftSpeed= config.get('main', 'liftSpeed')
liftPos= config.get('main', 'liftPos')
##closePos= config.get('main', 'closePos')
##dispensePos= config.get('main', 'dispensePos')
minOilLevel= config.get('main', 'minOilLevel')
minWaterLevel = config.get('main', 'minWaterLevel')

LARGE_FONT= config.get('font', 'LARGE_FONT')
NORM_FONT = config.get('font', 'NORM_FONT')
SMALL_FONT = config.get('font', 'SMALL_FONT')

for pin in out_pins:
    GPIO.setup(int(pin),GPIO.OUT)
for pin in in_pins:
    GPIO.setup(int(pin),GPIO.IN)
for pin in outPinsWiringpi:
    wiringpi.pinMode(pin,1)

    
##stirSpeed=0.006

### json read
##with open('data.json')as f:
##    data=json.loads(f.read())
##    print(f)

