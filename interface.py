#curses interface for the Mill
import curses
import time
import mill

class Interface(object):

    def __init__(self, controller):
        self.screen = curses.initscr()
        self.size = self.screen.getmaxyx()
        self.height = self.size[0]
        self.width = self.size[1]
        curses.cbreak()
        self.screen.nodelay(1)#nonblocking fethc getch
        self.callback=None

        self.halfwidth = self.width/2
        self.halfheight = self.height/2
    
        self.controller = controller

    def main(self):
        self.screen.clear()
        #self.screen.box()
        #self.screen.addstr(10,10,"Hello world")
        self.screen.refresh()

    def draw(self):
        self.screen.box()
        self.screen.refresh()

    def menu(self):
        pass

    def loop(self):
        go=1
        self.draw()
        #self.menu()
        while(go):
            c = self.screen.getch()

        
            self.screen.addstr(int(0.9*self.height),2, "MANUAL CTRL:"+controller.movement)
            self.screen.addstr(int(0.9*self.height)+1,2, "CURR CRD:"+str(controller.xcoord)+":"+str(controller.ycoord))

            if (c==ord('q')):
                go=0
            if (c==ord('s')):    
                self.screen.addstr(11,10,"Pressed s")
            if (c==ord('c')):
                self.screen.addstr(12,10,"Invoked callback")
                self.callback()

            time.sleep(0.1)
            controller.handler()
            self.screen.refresh()

    def quit(self):
        curses.endwin()

if __name__ == "__main__":

    def mycallback():
        print "cb"

    controller = mill.Controll() 
    
    myscreen =Interface(controller)
    myscreen.callback = mycallback
    myscreen.main()
    myscreen.loop()
    myscreen.quit()
    

