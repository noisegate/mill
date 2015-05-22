#curses interface for the Mill
import curses
import time

class Interface(object):

    def __init__(self):
        self.screen = curses.initscr()
        curses.cbreak()
        self.callback=None
        self.win2 = curses.newwin(30, 30, 0, 20)

    def main(self):
        self.screen.clear()
        self.screen.addstr(10,10,"Hello world")
        self.screen.refresh()
        self.win2.clear()
        self.win2.box()
        self.win2.refresh()

    def loop(self):
        go=1
        while(go):
            c = self.screen.getch()
            if (c==ord('q')):
                go=0
            if (c==ord('s')):    
                self.screen.addstr(11,10,"Pressed s")
            if (c==ord('c')):
                self.screen.addstr(12,10,"Invoked callback")
                self.win2.addstr(0,0,"win")
                self.win2.refresh()
                self.callback()

    def quit(self):
        curses.endwin()

if __name__ == "__main__":

    def callback():
        print "H"

    myscreen =Interface()
    myscreen.main()
    myscreen.callback = callback
    myscreen.loop()
    myscreen.quit()


