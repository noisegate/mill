import wiringpi2 as wp
import time
import RPi.GPIO as GPIO  

GPIO.setmode(GPIO.BCM)  
pinbase = 65
i2c_addr = 0x20

count=0

class Callbacks(object):

    def __init__(self):
        self.count = 0
        self.i2c = wp.I2C()
        self.dev = self.i2c.setup(0x20)
        self.state = 0

    def mycallback(self,channel):
        #print "interrupti {0}!".format(self.count)
        #print channel
        self.count +=1
        #print bin(self.i2c.readReg8(self.dev, 0x09))
        # wp.digitalRead(74)

        state = self.i2c.readReg8(self.dev, 0x09)
        if ((state&0b1)<(self.state&0b1)):
            #print "falling edgei ch 1"
            if (wp.digitalRead(74)):
                print "left"
            else:
                print "right"
        if ((state&0b10)<(self.state&0b10)):
            #print "falling edge ch 2"
            pass
            if (wp.digitalRead(73)):
                print "right"
            else:
                print "left"

        self.state = state    


if __name__ == '__main__':
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
    instance = Callbacks()
    GPIO.add_event_detect(19, GPIO.FALLING, callback=instance.mycallback) 
    #interrupt of mcp23016 is opendrain
    
    wp.wiringPiSetup()
    wp.mcp23016Setup(pinbase, i2c_addr)

    for i in range(65,81):
        wp.pinMode(i,0)
        wp.pullUpDnControl(i,2)

    wp.pinMode(73,0)#pin 0 input
    wp.pullUpDnControl(73,0)#pull none

    wp.pinMode(74,0)#input

    wp.pinMode(65, 1)#pin 65 output
    wp.digitalWrite(65, 1)#pin 65 high

    time.sleep(.5)
    
    #wp.pinMode(66, 0)#pin 66 input
    #wp.pullUpDnControl(66,2)
    
    while(1):
        if (not wp.digitalRead(73)):
            print "RIGHT"    
        if (not wp.digitalRead(74)):
            print "DOWN"
        if (not wp.digitalRead(75)):
            print "LEFT"
        if (not wp.digitalRead(76)):
            print "UP"
            
        time.sleep(0.1)
