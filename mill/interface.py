#curses interface for the Mill
import curses
import time
#import mill
import fbpy.fb as fb
import gcodeparser.gcodeparser as gcode

class Interface(object):
    LEFTCOLUMN = 10

    menudata =  [
                    [10, LEFTCOLUMN, "MENU"],
                    [11, LEFTCOLUMN, "===="],
                    [12, LEFTCOLUMN, "q)      quit"],
                    [13, LEFTCOLUMN, "c)      user defined"],
                    [14, LEFTCOLUMN, "s)      simulate"],
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

    def main(self):
        self.screen.clear()
        self.screen.refresh()
        self.surf.clear()
        self.surf.rect((0.0,0.0),(1.0,1.0))
        self.surf.update()

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

    def dowhateverSis(self):
        pass

    def updatedata(self,direction, x, y):
        self.screen.addstr( int(0.9*self.height),
                            self.LEFTCOLUMN, 
                            "MANUAL CTRL: {0:<10}".format(direction))
        self.screen.addstr( int(0.9*self.height)+1,
                            self.LEFTCOLUMN, 
                            "CURR CRD: x = {0:<4}  y = {1:<4}".format(x,y))

    def loadfile(self):
        pass        
        
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
            self.graphics.point((0.5+controller.xcoord/1000.0, 1.0-0.5+controller.ycoord/1000.0))
            self.graphics.update()
            """
            self.updatedata(direction, x, y)
        
            if (c==ord('q')):
                go=0
            elif (c==ord('l')):
                self.loadfile()
            elif (c==ord('s')):   
                self.dowhateverSis()
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
        self.screen.clear()
        self.screen.refresh()
        curses.endwin()

if __name__ == "__main__":

    def mycallback():
        pass

    class Mysim(gcode.Simulator):

        def __init__(self, surf, interfaceself):
            self.interfaceself = interfaceself
            gcode.Simulator.__init__(self, surf)

        def raisedrill(self):
            self.surf.pixelstyle.color = self.color1
            self.interfaceself.drillmessage("raise mill and press space to continue...")

        def lowerdrill(self):
            self.surf.pixelstyle.color = self.color2
            self.interfaceself.drillmessage("lower mill and press space to continue...") 

        def simfinished(self):
            self.interfaceself.drillmessage("Simulation finished, press space to continue") 

        def pause(self):
            self.interfaceself.ifpause()

        def movex(self, dx):
            pass

        def movey(self, dy):
            pass

    class Myinterface(Interface):
    
        def __init__(self):
            self.surface = fb.Surface()
            self.surf = fb.Surface((800,200),(300,300))
            self.parser = gcode.Parse()
            self.sim = Mysim(self.surf, self)
            Interface.__init__(self)

        def pause(self):
            go = 1
            while (go):
                c=self.screen.getch()
                if (c==ord(' ')): 
                    go=0

        def ifpause(self):
            c=self.screen.getch()
            if (c==ord(' ')): self.pause()

        def resetorigin(self):
            pass

        def decrementx(self):
            pass

        def decrementy(self):
            pass

        def incrementx(self):
            #print "move x"
            self.sim.movex(1)

        def incrementy(self):
            pass

        def dowhateverSis(self):
            self.sim.sim()

        def drillmessage(self, message):
            self.screen.addstr(int(0.8*self.height),self.LEFTCOLUMN, "Drill MSG:{0}".format(message))
            self.screen.refresh()
            self.pause()
            self.screen.addstr(int(0.8*self.height),self.LEFTCOLUMN,"                                                       ")
            self.screen.refresh()

        def loadfile(self):
            self.parser.filename = "spacer.ngc"
            self.parser.parse()
            self.sim.geometries = self.parser.geometries
            self.sim.draw()

    interface =Myinterface()
        
    interface.main()
    interface.loop()
    interface.quit()
    

