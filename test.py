import curses
import sys
import app
import time
import subprocess
from Board import *


def init_terminal():
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=40, cols=49))
    create_display()


def reset():
    subprocess.call(["printf", "\033c"])


def create_display():
    reset()
    print("\r" + "=" * 49)
    print("\r" + "2048".center(49, ' '))
    print("\r" + "=" * 49)


def print_message(message):
    print("\033[35m")
    print("\n\r" + "#" * 49)
    print("\r" + "{}".format(message).center(49, ' '))
    print("\r" + "#" * 49)
    print("\033[0m\r")


def self_exit(board, message):
    create_display()
    board.show()
    print_message(message)
    time.sleep(10)
    curses.endwin()
    reset()
    sys.exit(0)


def main():
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
            if direction in [119, 97, 115, 100]:
                board.move(direction)
            if board.did_change():
                board.place_tile()
            if board.is_win():
                self_exit(board, "You won!")
            if board.is_full():
                if board.is_lost():
                    self_exit(board, "You lost!")
    # Terminate curses mode
    except KeyboardInterrupt:
        self_exit(board, "You exited the game manually. Not a nice thing!")

if __name__ == "__main__":
    main()