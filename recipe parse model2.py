import json
file= 'maggi.json'
myDict={}
with open(file) as f:
    recipeData= json.loads(f.read())
    myDict.update(recipeData)
    try:
        newDict=dict(recipeData.iteritems())
    except AttributeError:
        newDict= dict(recipeData.items())

operationDictionary=newDict['process']
##for d in operationDictionary:
##    operation=d['operation']
##    if operation == 'heat':
##        print('heating')
##        print(d['temperature'])
##    elif operation== 'dispense':
##        if d['type']=='oil':
##            print('dispencing oil')
##            print(d['value'],d['metric'])
##        elif d['type']=='ingredient':
##            print('dispencing ingredient',d['ingredient'])
##            print(d['value'],d['metric'])
##        elif d['type']== 'spice':
##            print('dispencing spice',d['ingredient'])
##            print(d['value'],d['metric'])
##        elif d['type']== 'water':
##            print('dispencing water')
##            print(d['value'],d['metric'])
##    elif operation== 'stir':
##        print('stirring')
##        print(d['time'],d['value'])


for i in newDict.keys(): #reaching the keys of dict
    try:
        for x in newDict[i]: #reaching every element in tuples
                if x in newDict['ingredients']: #if match found..
                    print ("put {} in {} rack.".format(x,i)) #printing it..
                elif x in newDict['spices']: #if match found..
                    print ("put {} in {} rack.".format(x,i)) #printing it..
    except TypeError:
        pass
def podDetect(Dict):
    for i in Dict.keys():
        try:
            for x in Dict[i]:
                if x in Dict['ingredients']:
                    print("weigh the "+ str(x)+ " in weight scale")
                    x=0
                    while True:
                        if x==0:
                            if load(1,'weight')>10:
                                x=1
                            else:
                                pass
                        else:
                            if load(1,'weight')< 2:
                                break
                            else:
                                continue

                    print ("put {} in {} rack.".format(x,i)) 
                elif x in Dict['spices']: 
                    print ("put {} in {} rack.".format(x,i))
        except TypeError:
            pass
    return True
