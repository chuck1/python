import curses

screen = curses.initscr()
screen.addstr("Hello World!!!")
screen.refresh()
while True:
    try:
        c = screen.getch()
    except:
        break
curses.endwin()

