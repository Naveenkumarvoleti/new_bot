# Turns on each pin of an mcp23017 on address 0x20 ( quick2wire IO expander )
import wiringpi
from time import sleep
pin_base = 65
i2c_addr = 0x20
pins = [65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,89,90]

wiringpi.wiringPiSetup()
wiringpi.mcp23017Setup(pin_base,i2c_addr)

for pin in pins:
        while True:
                for pin in range(65,70):
                        print(pin)
                        wiringpi.pinMode(pin,1)
                        wiringpi.digitalWrite(pin,1)
                        wiringpi.delay(5000)
                        wiringpi.digitalWrite(pin,0)
##CCW=1
##dir_pin=67
##step_pin=69
##wiringpi.pinMode(dir_pin,1)
##wiringpi.pinMode(step_pin,1)
##delay=0.0028
##spr=200
####wiringpi.pinMode(69,1)
####wiringpi.digitalWrite(69,0)
##def forward(spr):
##        wiringpi.digitalWrite(dir_pin, CCW)
##        for x in range(int(round(spr)) if type(spr)==float else int(spr)):
####            print("step: ",x)
##            wiringpi.digitalWrite(step_pin, 1)
##            sleep(delay)
##            wiringpi.digitalWrite(step_pin, 0)
##            sleep(delay)
##forward(200)
