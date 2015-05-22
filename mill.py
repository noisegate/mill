import pololu.pololu as pololu
import wiringpi2 as wp
import time
import RPi.GPIO as GPIO
import gcoder

class Controll(object):

    def __init__(self):
        self.y = pololu.Pololu(pololu.Pins(enable=22, direction=24,step=23))
        self.x = pololu.Pololu(pololu.Pins(enable=26, direction=21,step=20))    
        self.x.speed = 120
        self.y.speed = 120

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
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
            if (not wp.digitalRead(73)):
                print "RIGHT"
                self.right()
            if (not wp.digitalRead(74)):
                print "UP" 
                self.up()
            if (not wp.digitalRead(75)):
                print "LEFT" 
                self.left()
            if (not wp.digitalRead(76)):
                print "DOWN"
                self.down()
    
            time.sleep(0.001)

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
    instance.loop()


