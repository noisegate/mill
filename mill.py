import pololu.pololu as pololu
import wiringpi2 as wp
import time
import RPi.GPIO as GPIO
import gcoder

pinbase = 65
i2c_addr = 0x20

class Movements(object):

    UP    = "up   "
    RIGHT = "right"
    DOWN  = "down "
    LEFT  = "left "
    NONE  = "none "

class Controll(object):

    def __init__(self):
        # $U3 = X
        # $U4 = Y
        self.y = pololu.Pololu(pololu.Pins(enable=15, direction=11,step=13))
        self.x = pololu.Pololu(pololu.Pins(enable=22, direction=16,step=18))    
        self.x.speed = 120
        self.y.speed = 120

        self.xcoord = 0
        self.ycoord = 0

        self.movement = Movements.NONE

        GPIO.setmode(GPIO.BCM)
        #GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        #interrupt
        GPIO.setup(19,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(19, GPIO.FALLING, callback=self.callback) 
        
        self.i2c = wp.I2C()
        self.dev = self.i2c.setup(i2c_addr)
         
        wp.wiringPiSetup()
        wp.mcp23016Setup(pinbase, i2c_addr)

        self.state =0

        #wp.pinMode(19,0)
        #wp.pullUpDnControl(19,2)

        for i in range(65,73):
            wp.pinMode(i,1)
            wp.pullUpDnControl(i,2)

        for i in range(73,81):
            wp.pinMode(i,0)

        #wp.pinMode(65, 1)#pin 65 output
        #wp.digitalWrite(65, 1)#pin 65 high

    def callback(self, channel):
        state = self.i2c.readReg8(self.dev, 0x09)
        if (state == 0b11111110): 
            self.movement = Movements.RIGHT

        if (state == 0b11111101):
            self.movement = Movements.DOWN
        
        if (state == 0b11111011):
            self.movement = Movements.LEFT

        if (state == 0b11110111):
            self.movement = Movements.UP

        if (state == 0b11111111):
            self.movement = Movements.NONE

    def up(self):
        print "moving up"
        self.x.stepsleft(1)

    def down(self):
        print "moving down"
        self.x.stepsright(1)

    def left(self):
        self.y.stepsleft(1)

    def right(self):
        self.y.stepsright(1)
   
    def handler(self):
        if (self.movement == Movements.UP):
            self.ycoord+=1
        if (self.movement == Movements.DOWN):
            self.ycoord-=1
        if (self.movement == Movements.RIGHT):
            self.xcoord+=1
        if (self.movement == Movements.LEFT):
            self.xcoord-=1
            
   
    def load(self, filename):
        
        try:
            lines = open(filename,'r')
            for line in lines:
                if (line==[]):
                    pass
                elif (line[0:3]=="G21"):
                    print "working in mm"
                elif (line[0:3]=="G1"):
                    pass

        except:
            pass
            

if __name__ == '__main__':

    instance = Controll()


