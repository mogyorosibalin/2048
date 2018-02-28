import curses
import sys
import app
import time
import subprocess
from Board import *


def init_terminal():
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=40, cols=49))
    create_display()


def create_display():
    subprocess.call(["printf", "\033c"])
    print("\r" + "=" * 49)
    print("\r" + "2048".center(49, ' '))
    print("\r" + "=" * 49)

try:
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    
    init_terminal()
    create_display()

    board = Board()
    board.place_tile()
    

    while True:
        create_display()
        old_board = board.create_old()
        board.show()
        direction = stdscr.getch()
        # print(direction)
        # time.sleep(1)
        if direction in [119, 97, 115, 100]:
            board.move(direction)
        if board.did_change():
            board.place_tile()
        if board.is_full():
            if board.is_lost():
                create_display()
                board.show()
                print("You lost")
                time.sleep(2)
                curses.endwin()
                exit()
# Terminate curses mode
except KeyboardInterrupt:
    curses.endwin()