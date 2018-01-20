##from pins import *
import time
##GPIO.setmode(GPIO.BCM)
import wiringpi

pinBase =65
i2cAddr = 0x20
wiringpi.wiringPiSetup()
wiringpi.mcp23017Setup(pinBase,i2cAddr)

wiringpi.pinMode(78,1)
wiringpi.pinMode(79,0)
wiringpi.digitalWrite(79,0)

GPIO_TRIGGER = 78
GPIO_ECHO    = 79

def measure():
  # This function measures a distance
  stop = time.time()
  wiringpi.digitalWrite(GPIO_TRIGGER, 1)
  time.sleep(0.00001)
  wiringpi.digitalWrite(GPIO_TRIGGER, 0)
  start = time.time()

  while wiringpi.digitalRead(GPIO_ECHO)==0:
    start = time.time()

  while wiringpi.digitalRead(GPIO_ECHO)==1:
    stop = time.time()

  elapsed = stop-start
  distance = elapsed*17150
  distance=round(distance,2)
  return distance


while True:
    print(measure())
    time.sleep(1)
# Wrap main content in a try block so we can
# catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent
# the user seeing lots of unnecessary error
# messages.
#  distance = measure_average()
   #  print "Ultrasonic Measurement"
   #  print "Distance : %.1f" % distance
   #  if distance < 8:
   #      wiringpi.digitalWrite(121,1)
   #  else:
    #     wiringpi.digitalWrite(121,0)
    # time.sleep(2)
