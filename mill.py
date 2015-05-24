import pololu.pololu as pololu
import wiringpi2 as wp
import time
import RPi.GPIO as GPIO
import gcoder

pinbase = 65
i2c_addr = 0x20

class Controll(object):

    def __init__(self):
        # $U3 = X
        # $U4 = Y
        self.y = pololu.Pololu(pololu.Pins(enable=15, direction=11,step=13))
        self.x = pololu.Pololu(pololu.Pins(enable=22, direction=16,step=18))    
        self.x.speed = 120
        self.y.speed = 120

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

        wp.pinMode(19,0)
        wp.pullUpDnControl(19,2)

        for i in range(65,81):
            wp.pinMode(i,0)
            wp.pullUpDnControl(i,2)

        #wp.pinMode(65, 1)#pin 65 output
        #wp.digitalWrite(65, 1)#pin 65 high

    def callback(self, channel):
        print "ISR"
        state = self.i2c.readReg8(self.dev, 0x09)

        if ((state&0b1) < (self.state&0b1)):
            #falling edge channel 1
            if (not wp.digitalRead(73)):
                print "DOWN"
                self.down()
        
        if ((state&0b10) < (self.state&0b10)):
            #falling edge channel 2
            if (not wp.digitalRead(74)):
                print "UP"
                self.up()
         
        #if (not wp.digitalRead(74)):
        #    print "UP" 
        #    self.up()
        #if (not wp.digitalRead(75)):
        #    print "LEFT" 
        #    self.left()
        #if (not wp.digitalRead(76)):
        #    print "DOWN"
        #    self.down()
  
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
   
    def loop(self):
        while(1):
            time.sleep(0.1)
            print wp.digitalRead(19)
   
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


