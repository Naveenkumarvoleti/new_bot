import time
##x=0
def measurement(value):
    for i in range(value):
        i+=1
        time.sleep(0.2)
    return True
##def measurement(value):
##    global x
##    if x < value:
##        x+=1
##        print(x)
##    return x
