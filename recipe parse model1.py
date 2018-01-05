
def startProcess(operationDictionary):
##  while True:
##    sense.wait()
    print("running process")
    i = 0
    gpio_high_low(inductionOnOff,0.2)
    if stepper.start.pos_zero() == True:
##### process count starts from here ####
        for i in range(operations):
          if operationDictionary[i]["operation"] == "heat":
            print("heating induction at level: "+str(operationDictionary[i]["temperature"])+"C")
            inductor_run = threading.Thread(target= inductor,args=(operationDictionary[i]["temperature"],))
            inductor_run.start()
            inductor_run.join()

          elif operationDictionary[i]["operation"] == "dispense":
            if operationDictionary[i]["type"]== "spice":
              print("getting location of spice")
              getLocation(spicePin,mode="spice")
              dispenseIngredient('spice',spicePin,operationDictionary[i]["value"])
            elif operationDictionary[i]["type"]== "ingredient":
              print("getting ingredient")
              getLocation(ingredientPin,mode="ingredient")
              dispenseIngredient('ingredient',ingredientPin,operationDictionary[i]["value"])

            elif operationDictionary[i]["type"] == "water":
                  print("pouring water")
                  dispenseLiquid(waterPin,operationDictionary[i]["value"])
            elif operationDictionary[i]["type"] == "oil":
                  print("dispensing oil")
                  dispenseLiquid(oilPin,operationDictionary[i]["value"],metric)

          elif operationDictionary[i]["operation"] == "stir":
              print("stirring")
              stir(operationDictionary[i]["time"],operationDictionary[i]["value"])
          i+=1
        print("curry done")
        gpio_high_low(inductionOnOff,0.2)
    else:
      print("stepper is not moving or sensor is not working")
