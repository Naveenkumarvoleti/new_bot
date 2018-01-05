import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# shift out function 
stbPin=17
dataPin=18
clkPin=19

GPIO.setup(stbPin,GPIO.OUT)
GPIO.setup(dataPin,GPIO.OUT)
GPIO.setup(clkPin,GPIO.OUT)

def sendByte(data):
    pass

def shiftOut(dataPin,clkPin,MSBFIRST,command):
    i=0
    for i in range(8):
        output=False
        if (MSBFIRST):
            output= command & 0b10000000
            command = command << 1
        else:
            output=command & 0b00000001
            command = command >> 1
        GPIO.output(dataPin, True)
        GPIO.output(clkPin, True)
        time.sleep(1)
        GPIO.output(clkPin,False)
        time.sleep(1)
        i=i+1

def shiftIn(dataPin,clkPin,MSBFIRST):
    i=0
    for i in range(8):
        GPIO.output(clkPin,True)
        if (MSBFIRST):
            output |= GPIO.input(dataPin) << i
        else:
            output |= GPIO.input(dataPin) << (7-i)
        GPIO.output(clkPin,True)
        
def readButtons():
    GPIO.output(stbPin, True)
    shiftOut(dataPin,clkPin,LSBFIRST,comReadButtons)



# new
def shiftOut(self, dataPin, clockPin, pinOrder, value):
        """
        Shift a byte out on the datapin using Arduino's shiftOut()
        Input:
            dataPin (int): pin for data
            clockPin (int): pin for clock
            pinOrder (String): either 'MSBFIRST' or 'LSBFIRST'
            value (int): an integer from 0 and 255
        """
        cmd_str = build_cmd_str("so",
                               (dataPin, clkPin, pinOrder, value))
        self.sr.write(cmd_str)
        self.sr.flush()

    def shiftIn(self, dataPin, clockPin, pinOrder):
        """
        Shift a byte in from the datapin using Arduino's shiftIn().
        Input:
            dataPin (int): pin for data
            clockPin (int): pin for clock
            pinOrder (String): either 'MSBFIRST' or 'LSBFIRST'
        Output:
            (int) an integer from 0 to 255
        """
        cmd_str = build_cmd_str("si", (dataPin, clockPin, pinOrder))
        self.sr.write(cmd_str)
        self.sr.flush()
        rd = self.sr.readline().replace("\r\n", "")
        if rd.isdigit():
            return int(rd)


def readAddress():
    
