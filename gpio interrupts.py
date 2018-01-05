import time

import pigpio

TIME=30

gpioA7=24       # gpio connected to port A bit 7.
gpioPortAInt=23 # gpio connected to port A interrupt line.

INTENA=4  # Port A interrupt register.
DEFVALA=6 # Port A default values.
INTCONA=8 # Port A interrupt control.

GPIOA=18    # Port A bits register.

portABits = 0
changedABits = 0

def IntA(gpio, level, tick):
   global portABits, changedABits
   # Read port A, clear interrupt.
   now = pi.i2c_read_byte_data(chip, GPIOA)
   changedABits = now ^ portABits
   portABits = now
   print("port A is {:08b} changed {:08b}".format(portABits, changedABits))

pi = pigpio.pi("tom") # Connect to tom.

pi.set_mode(gpioA7, pigpio.OUTPUT)

chip = pi.i2c_open(0, 0x20) # tom is a Rev.1 board.

pi.i2c_write_byte_data(chip, DEFVALA, 0)
pi.i2c_write_byte_data(chip, INTCONA, 0)
pi.i2c_write_byte_data(chip, INTENA, 0xFF) # Interrupt on any PORTA change.

# Call IntA on Port A interrupt.
cb = pi.callback(gpioPortAInt, pigpio.FALLING_EDGE, IntA)

# Make sure gpio changes state when first interrupt arrives.
# Otherwise the callback won't be called and the interrupt
# won't be cleared.
pi.write(gpioPortAInt, 0)
pi.set_mode(gpioPortAInt, pigpio.INPUT)

start = time.time()

bitA7 = 1

while (time.time() - start) < TIME:
   pi.write(gpioA7, bitA7) # Change bit.
   bitA7 = not bitA7
   time.sleep(1)

pi.i2c_close(chip)

pi.stop()
