import random
import time
from led import *

podPins = [1, 2, 3, 4, 5, 6, 7, 8]


class podSelection(object):
    def __init__(self):
        pass

    def ledLightup(self, ledPin):
        ledLight = Led(ledPin)
        ledLight.on_light()

    def ledBlink(self, ledPin, numTimes):
        ledLight = Led(ledPin)
        ledLight.blinkn(numTimes)

    def ledOff(self, ledPin):
        ledLight = Led(ledPin)
        ledLight.off_light()

    def podSelection(self):
        selection = random.choice(podPins)


spiceDict = {1: 0, 2: 45, 3: 90, 4: 135, 5: 180, 6: 225, 7: 270, 8: 315}
ingredientDict = {9: 0, 10: 60, 11: 120, 12: 180, 13: 240, 14: 300}

ingredientPin, ingredientAngle = random.choice(list(ingredientDict.items()))
spicePin, spiceAngle = random.choice(list(spiceDict.items()))

# print(random.sample(range(1,9),8))
print(spicePin)
print(spiceAngle)
print(ingredientPin)
print(ingredientAngle)


def spice(spiceDict):
    spicePin, spiceAngle = random.choice(list(spiceDict.items()))
