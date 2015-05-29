#curses interface for the Mill
import curses
import time
#import mill
import fbpy.fb as fb

class Interface(object):
    LEFTCOLUMN = 10

    menudata =  [
                    [10, LEFTCOLUMN, "MENU"],
                    [11, LEFTCOLUMN, "===="],
                    [12, LEFTCOLUMN, "q)      quit"],
                    [13, LEFTCOLUMN, "c)      user defined"],
                    [14, LEFTCOLUMN, "s)      MENU"],
                    [15, LEFTCOLUMN, "o)      set origin"],
                    [16, LEFTCOLUMN, "l)      load file"],
                    [17, LEFTCOLUMN, "<space> pause/play"],
                    [18, LEFTCOLUMN, "i,j,k,m up/dn/lt/rt"],
                    [19, LEFTCOLUMN, "..."]
                ]

    def __init__(self):
        self.screen = curses.initscr()
        self.size = self.screen.getmaxyx()
        self.height = self.size[0]
        self.width = self.size[1]
        curses.cbreak()
        curses.noecho()
        self.screen.nodelay(1)#nonblocking fethc getch
        self.callback=None

        self.halfwidth = self.width/2
        self.halfheight = self.height/2
    
        self.surface = fb.Surface()
        self.graphics = fb.Surface((400,400),(400,400))

    def main(self):
        self.screen.clear()
        #self.screen.box()
        #self.screen.addstr(10,10,"Hello world")
        self.screen.refresh()
        self.graphics.clear()
        self.graphics.rect((0.0,0.0),(1.0,1.0))
        self.graphics.update()

    def draw(self):
        self.screen.box()
        self.screen.refresh()

    def menu(self):
        for line in self.menudata:
            self.screen.addstr(line[0], line[1],line[2]) 

    def resetorigin(self):
        pass

    def decrementy(self):
        pass

    def decrementx(self):
        pass

    def incrementx(self):
        pass

    def incrementy(self):
        pass

    def millhandler(self):
        pass

    def updatedata(self,direction, x, y):
        self.screen.addstr( int(0.9*self.height),
                            self.LEFTCOLUMN, 
                            "MANUAL CTRL: {0:<10}".format(direction))
        self.screen.addstr( int(0.9*self.height)+1,
                            self.LEFTCOLUMN, 
                            "CURR CRD: x = {0:<4}  y = {1:<4}".format(x,y))

    def loop(self):
        go=1
        self.draw()
        self.menu()
        x=0
        y=0
        direction='NONE'

        while(go):
            c = self.screen.getch()
            """
                this is an overiirude
            self.screen.addstr( int(0.9*self.height),
                                self.LEFTCOLUMN, 
                                "MANUAL CTRL: {0:<10}".format(controller.Movement.names[controller.movement]))
            self.screen.addstr( int(0.9*self.height)+1,
                                self.LEFTCOLUMN, 
                                "CURR CRD: x = {0:<4}  y = {1:<4}".format(str(controller.xcoord), str(controller.ycoord)))
            
            
            self.graphics.point((0.5+controller.xcoord/1000.0, 1.0-0.5+controller.ycoord/1000.0))
            self.graphics.update()
            """
            self.updatedata(direction, x, y)
        
            if (c==ord('q')):
                go=0
            elif (c==ord('s')):   
                pass
            elif (c==ord('o')):
                self.resetorigin()
            elif (c==ord('i')):
                self.decrementy()
            elif (c==ord('m')):
                self.incrementy()
            elif (c==ord('j')):
                self.decrementx()
            elif (c==ord('k')):
                self.incrementx()

            time.sleep(0.02)
            self.millhandler()
            self.screen.refresh()

    def quit(self):
        curses.endwin()

if __name__ == "__main__":

    def mycallback():
        pass

    interface =Interface()
    
    interface.main()
    interface.loop()
    interface.quit()
    

