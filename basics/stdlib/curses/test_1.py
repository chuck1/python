from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    for i in range(0, 10):
        stdscr.addstr(i, 0, 'choice {}'.format(i))

    stdscr.refresh()

    while True:
        c = stdscr.getkey()
        stdscr.addstr(i, 0, 'you pressed {}'.format(c))
        stdscr.refresh()


wrapper(main)

