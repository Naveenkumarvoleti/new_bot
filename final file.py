import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import led,loadcell,stepper,Test
from dsb18_temp import measurement
import sys
import json
from time import sleep
import os,glob
from threading import Thread, Event
import threading
from pins import*
from ultra import ultrasonic
global index
global value
import time
from tkinter import*
import os.path
#operationDictionary
operationDictionary= {}

#pod dictionary
ingredientPod=[45,90,180,135,225,360,270,315]
spicePod= [45,135,90,180,225,360,315,270]

pumpSpeed= 100 #ml/min
currentIngredientPos=0
currentSpicePos=0

lock=threading.Lock()

# Switching to high and stay for given time and switch to low
def gpio_high_low(pinNumber, timeInSeconds):
    GPIO.output(pinNumber,True)
    sleep(timeInSeconds)
    GPIO.output(pinNumber,False)

# Switching to low and stay for given time and switch to high
def gpio_low_high(pinNumber, timeInSeconds):
    GPIO.output(pinNumber,False)
    sleep(timeInSeconds)
    GPIO.output(pinNumber,True)

# Dispensing Liquids based on PumpSpeed
def dispenseLiquid(pinNumber,quantity):
    totalDispensingTimeInSeconds = (quantity*60)/pumpSpeed
    print(round(totalDispensingTimeInSeconds),"sec"," quantity: ",quantity,"ml")
    gpio_high_low(pinNumber,totalDispensingTimeInSeconds)

# Rice cooker
def cookRice(temperature,delay):
  time.sleep(delay)
  print ("cooking Rice")
  if (Test.measurement(temperature)) <= 100:
    GPIO.output(ricePin,True)
  GPIO.output(ricePin,False)
  GPIO.output(riceWarmPin,True)
  print("rice cooking done")
  print("warm mode active")
 
# Stirring
def stir(delay,value):
    if value == "min":
        finalTime= delay*60
        print(finalTime)
    else:
        finalTime=delay
        print(finalTime)
    closeTime=round(time.time())+finalTime
    print(round(closeTime))
    while round(time.time()) < closeTime:
        stepper.start.forward(1)
    stepper.start.stop()

#location detect:
def getLocation(pin,mode=None):
  print("getting location")
  GPIO.output(pin,True)
  getLocationEvent = threading.Event()
  time.sleep(1)
  if mode=="ingredient":
      global currentIngredientPos
      angle=ingredientPod[currentIngredientPos]
      currentIngredientPos+=1
  elif mode=="spice":
      global currentSpicePos
      angle=spicePod[currentSpicePos]
      currentSpicePos+=1
  if stepper.start.move_to(angle) == True:
      print("reached location at", angle)
      getLocationEvent.set()
  else:
      getLocationEvent.clear()  
  GPIO.output(pin,False)

def gpioToggle(gpioNum=None, OnOff=None):
    
    if len(pinGPIOList) >= int(GPIO_Num):
        out = {"pin" : pinGPIOList[int(gpioNum)-1], "status" : "off"}
        if onoff == "on":
            GPIO.output(pinGPIOList[int(gpioNum)-1], ON)
            out["status"] = "on"
            print("GPIO Pin #%s is toggled on" % pinGPIOList[int(gpioNum)-1]) 
        else: #off
            GPIO.output(pinGPIOList[int(gpioNum)-1], OFF)
            print("GPIO Pin #%s is toggled off" % pinGPIOList[int(gpioNum)-1]) 
    else:
        out = {"pin" : 0, "status" : "off"}

#liftCookingLid
def liftCookingLid(lidPos):
  stepper.start.stop()
  print("lifting lid")
##  gpio_high_low(lidPin,time)
  if stepper.start.forward(lidPos)== True:
      stepper.start.stop()

#closingCookingLid
def closeCookingLid(lidPos):
  stepper.start.stop()
##  gpio_high_low(lidPin,time)
  while not GPIO.input(liftStop)==True:
      stepper.start.backward(lidPos)
  stepper.start.forward(closePos)
  print("closing lid")
  stepper.start.stop()

# Dispensing Ingredients
def dispenseIngredient(dispensePin,quantity):
    liftCookingLid(dispensePos)
    if not loadcell.get_weight(quantity) < quantity == True:
      GPIO.output(dispensePin,True)
    else:
      GPIO.output(dispensePin,False)
      time.sleep(1)
      closeCookingLid(closePos)

# Read the recipe file
def readRecipe(file,delay):
  time.sleep(delay)
  with open(file) as f:
    recipeData =json.loads(f.read())
    operationDictionary.update(recipeData)
    print(recipeData["no_of_operations"])
    global operations
    operations=(operationDictionary["no_of_operations"])
    print(operationDictionary["human_readable_steps"])
  startProcess(operationDictionary["process"])

#induction heat
def inductor(temperature=0):
  gpio_low_high(inductionOnOff,0.2)
  while not temperature == 0:
      temp = Test.measurement(temperature)
##      temp = dsb18_temp.measurement
      if temperature > temp:
        print(temp)
        gpio_high_low(inductionPlusPin,0.2)
        print("induction heating up")
        time.sleep(5)
      elif temperature < temp:
        gpio_high_low(inductionMinusPin,0.2)
        print("induction heating down")
        time.sleep(5)
      else:
          print("temperature reached")
  gpio_low_high(inductionOnOff,0.2)
  
def ultrasonic(ultrasonicDictionary):
  print("sensing")
  for u in ultrasonicDictionary:
      reading=ultrasonic(u)
      if reading < minOilLevel:
          print("oil is not enough, checkreading: " + str(reading))
          start_process.acquire()  
      elif reading < minwaterLevel:
          print("water is not enough, check reading: "+str(reading))
          lock.acquire()
      else:
          print(str(reading))
          lock.release()
    
#start process
def startProcess(operationDictionary):
##  while True:
##    sense.wait()
    i = 0
    gpio_low_high(inductionOnOff,0.2)
    if stepper.start.pos_zero() == True and lock.acquire !=True:
        for i in range(operations):
          if operationDictionary[i]["operation"] == "heat":
            print("preheat running")
            inductor_run = threading.Thread(target= inductor,args=(operationDictionary[i]["temperature"],))
            inductor_run.start()
            inductor_run.join()

          elif operationDictionary[i]["operation"] == "dispense":
            if operationDictionary[i]["type"]== "spice":
              print("getting location of spice")
              getLocation(spicePin,mode="spice")
              dispenseIngredient(spicePin,operationDictionary[i]["value"])


            elif operationDictionary[i]["type"]== "ingredient":
              print("getting ingredient")
              getLocation(ingredientPin,mode="ingredient")
              dispenseIngredient(ingredientPin,operationDictionary[i]["value"])

            elif operationDictionary[i]["type"] == "water":
                  print("pouring water")
                  dispenseLiquid(waterPin,operationDictionary[i]["value"])
        ##
            elif operationDictionary[i]["type"] == "oil":
                  print("dispensing oil")
                  dispenseLiquid(oilPin,operationDictionary[i]["value"])

          elif operationDictionary[i]["operation"] == "stir":
              print("stirring")
              stir(operationDictionary[i]["time"],operationDictionary[i]["value"])
          i+=1
        print("curry done")
        gpio_low_high(inductionOnOff,0.2)
    else:
      print("stepper is not moving or sensor is not working")

global win
win = Tk()
##win.attributes("-zoomed",True)
##win.minsize(width=480, height=320)
##win.config(menu=blank_menu)
win.title("Olly")
f= Frame(win)
l= Label(win,text = "HI...")
b1= Button(f,text = "Let's cook something")
##b2 = Button(f,text = "Bottle update")
##b2.pack()
l.pack()
f.pack()
global file

level=threading.Timer(5.0,ultrasonic,args=(ultrasonicDictionary,)).start()

def popupmsg(msg,Type=0,bT="ok",cmd=None):
    global popup
    popup = Tk()
    popup.wm_title("ERROR")
    label = Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    if Type == 1:
        b1=Button(popup,text=bT,command= popup.destroy)
        b1.pack()
    else:
        B1 = Button(popup, text="Yes", command = lambda :cmd)
        B1.pack()
        B2 = Button(popup, text="NO", command = popup.destroy)
        B2.pack()
    popup.mainloop()
              
try:
      def interrupt1(channel):
            lock.acquire()
            print("lid opened..please close the lid")
##            GPIO.wait_for_edge(20,GPIO.RISING)
##            time.sleep(60)
            lock.release()
            
      def interrupt2(channel):
            print("place the glass")
            lock.acquire()
##            GPIO.wait_for_edge(21,GPIO.RISING)
##            time.sleep(60)
            lock.release()
            
##      GPIO.add_event_detect(LidPin,GPIO.FALLING,callback=interrupt1,bouncetime=300)
##      GPIO.add_event_detect(wasteWaterPin,GPIO.FALLING,callback=lambda :popupmsg("waste water is full",Type=1,bt="retry",cmd=popup.destroy()),bouncetime=300)
##      GPIO.add_event_detect(glassPin,GPIO.FALLING,callback=interrupt2,bouncetime=300)

      def display_menu():
        f.pack_forget()
        f.grid_forget()
        l.pack_forget()
        win.title("Olly")
        global b4
        global b5
        global b6
        global b7
        b4 = Button(win,text ="Select curry")
        b5 = Button(win,text ="cook rice")
        b6 = Button(win,text = "Testing")
        b7=Button(win,text="cook both")
        b4.pack(side=TOP,padx= 10,pady=10)
        b5.pack(side = TOP,pady=10,padx=10)
        b6.pack(side =TOP,padx=10,pady=10)
        b7.pack(side =TOP,padx=10,pady=10)
        b5.configure(command= riceCook)
        b4.configure(command =displayFiles)
        b6.configure(command = testing)
        b7.configure(command = cookBoth)

      def riceCook():
          b4.pack_forget()
          b5.pack_forget()
          b6.pack_forget()
          b7.pack_forget()
          l1=Label(win,text = "choose rice type")
          l1.pack()
          slct = StringVar(win)
          slct.set("Bhasmati")
          choices = {'bhasmati','Brown rice','paraboiledrice','Arborio rice'}
          popupmenu = OptionMenu(win,slct,*choices)
          l5 = Label(win,text = "start after : ")
          amt=Scale(win,from_=1,to= 60,orient=HORIZONTAL,resolution=1)
          popupmenu.pack()
          amt.pack()
          but=Button(win,text="make")
          but.configure(command= lambda :cookRice(100,amt.get()))
          but.pack()
          
      def displayFiles():
          b4.pack_forget()
          b5.pack_forget()
          b6.pack_forget()
          b7.pack_forget()
          win.title("Olly")
          l6=Label(win,text="Select curry")
          l5 = Label(win,text = "start after : ")
          l6.pack()
          lb = Listbox(win,width=15,height=2)
          lb.pack(side=TOP,pady=2)
          os.chdir(".")
          for file in glob.glob("*.json"):
            files=file
            lb.insert(END,files)
          b8=Button(win,text="MAKE....")
          amt=Scale(win,from_=1,to= 60,orient=HORIZONTAL,resolution=1)
          b8.configure(command = lambda :readRecipe(lb.get(ACTIVE),amt.get()))
          l5.pack
          amt.pack()
          b8.pack()
##          b7=Button(win,text="back",command= display_menu)
##          b7.pack()


      def testing():
          b4.pack_forget()
          b5.pack_forget()
          b6.pack_forget()
          b7.pack_forget()
          win.title("Olly")

          label_1 = Label(win, text="temperature")
          label_2 = Label(win, text="select bottle, 1-6:")
          label_3 = Label(win,text=z)
          label_1.grid(row=1,column=2)
          label_2.grid(row=3,column=2)
          label_3.grid(row=6,column=2)

          entry_1.grid(row=2, column=2)
##          entry_2.grid(row=4, column=0)
          but = Button(win, text="Update", command=lambda :commando(x.get(), slct.get()))
          but.grid(row=5, column=2)
          but1=Button(win,text="Main menu")
          but1.grid(row=10,column=10)
          but1.configure(command=None)
            
      def cookBoth():
          b4.pack_forget()
          b5.pack_forget()
          b6.pack_forget()
          b7.pack_forget()
          win.title("Olly")
          l1=Label(win,text = "choose rice type")
          selct=StringVar(win)
          l2=Label(win,text = "select curry")
          l1.grid(row=1)
          l2.grid(row=2)
          l3.grid(row=3)
          l4.grid(row=4)
          l5.grid(row=5)
          lb = Listbox(win,width=15,height=2)
          lb.pack(side=TOP,pady=2)
          os.chdir(".")
          for file in glob.glob("*.json"):
            files=file
            lb.insert(END,files)
          butt = Button(win,text = "MAKE",command = lambda : cookRice(slct.get()))
          butt.grid(row=2)
          slct = StringVar(win)
          slct.set("Bhasmati")
          choices = {'bhasmati','Brown rice','paraboiledrice','Arboriorice'}
          popupmenu = OptionMenu(win,slct,*choices)
          popupmenu.grid(row = 5,column = 2)
              
      b1.pack()
      b1.configure(command = display_menu)
      time.sleep(20)
##      b1.invoke()
      win.mainloop()
except KeyboardInterrupt:
  print("cleaning everything")
  GPIO.cleanup()
