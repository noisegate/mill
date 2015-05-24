#curses interface for the Mill
import curses
import time
import mill

class Interface(object):

    def __init__(self):
        self.screen = curses.initscr()
        self.size = self.screen.getmaxyx()
        self.height = self.size[0]
        self.width = self.size[1]
        curses.cbreak()
        self.callback=None

        self.halfwidth = self.width/2
        self.halfheight = self.height/2

        self.win2 = curses.newwin(1, self.halfwidth-1 , self.height-1, self.halfwidth-1)
        self.menu = curses.newwin(1, 1, self.height, self.halfwidth-1)

    def main(self):
        self.screen.clear()
        #self.screen.box()
        #self.screen.addstr(10,10,"Hello world")
        self.screen.refresh()

    def draw(self):
        self.menu.box()
        self.menu.refresh()
        self.win2.box()
        self.win2.refresh()

    def menu(self):
        self.menu.addstr(1, 1, "MENU")

    def loop(self):
        go=1
        self.draw()
        #self.menu()
        while(go):
            c = self.screen.getch()

            if (c==ord('q')):
                go=0
            if (c==ord('s')):    
                self.screen.addstr(11,10,"Pressed s")
            if (c==ord('c')):
                self.screen.addstr(12,10,"Invoked callback")
                self.win2.addstr(0,0,"win")
                self.callback()

    def quit(self):
        curses.endwin()

if __name__ == "__main__":

    controller = mill.Controll() 
    controller.loop()
    exit()
    
    myscreen =Interface()
    
    myscreen.main()
    myscreen.loop()
    myscreen.quit()
    

