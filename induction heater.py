import dht
import RPi.GPIO as GPIO
from time import sleep
from threading import Thread, Event
import threading



#induction heat
class inductor(threading.thread,temperature):
  def __init__(self,temperature):
    Thread.__init__(self)
    self.Temperature= temperature
  def induction_heat(self):
      while not self.temperature == 0:
          if self.Temperature <= dht.tempesence.READ():
            print(temperature)
            gpio_high_low(inductionPlusPin,0.2)
            print("induction heating")
          else:
            gpio_high_low(inductionMinusPin,0.2)
            
  def induction_on(self):
    sendByte(onCommand)
    
  def inductionOff(self):
    sendByte(offCommand)

  def getByte(self):
    GPIO.setup(self.dio, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    temp=0
    for i in range(8):
      temp >>= 1
      GPIO.output(self.clk, False)
      if GPIO.input(self.dio):
        temp |= 0x80
      GPIO.output(self.clk,True)

  def sendByte(self, data):
     for i in range(8):
       GPIO.output(self.clk, False)
       GPIO.output(self.dio, (data & 1) == 1)
       data >>= 1
       GPIO.output(self.clk, True)
       
  def setDataMode(self):
    self.sendByte(0x40 | wrMode | addrMode)


  def getData(self):
    GPIO.output(self.stb,False)
    self.setDataMode(READ_MODE, INC_ADDR)
    sleep(20e-6)
    b=[]
    for i in range(8):
      b.append(self.getByte())
    GPIO.output(self.stb, True)

  def sendData(self):
    pass
    
while True:
    temp = 35
    induction= threading.Thread(target=inductor,args=(temp),name="induction")
    induction.start()
