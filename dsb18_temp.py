import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprpobe w1-therm')

base_dir='/sys/bus/w1/devices/'
device_folder=glob.glob(base_dir+'28*')[0]
device_file=device_folder+'/w1_slave'

def readTemp():
    f=open(device_file,'r')
    lines=f.readlines()
    f.close()
    return lines

def measurement():
    lines=readTemp()
    while lines[0].strip()[-3:]!= 'YES':
        time.sleep(0.2)
        lines=readTemp()
    equalPos=lines[1].find("t=")
    if equalPos !=-1:
        tempString=lines[1][equalPos+2:]
        tempC=float(tempString)/1000.0
        tempF=tempC*9.0/5.0+32.0
        return tempC
