import subprocess
import random
import sys


def init_terminal():
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=40, cols=49))
    create_display()


def create_display():
    subprocess.call(["printf", "\033c"])
    print("=" * 49)
    print("2048".center(49, ' '))
    print("=" * 49)
    pass


def get_tile_colors(num):
    index = 0
    if num == 0:
        return None
    while num != 2:
        num /= 2
        index += 1
    return index % len(colors)

colors = [
    "\033[1;30;43m",
    "\033[1;30;46m",
    "\033[1;30;44m",
    "\033[1;30;45m",
    "\033[1;30;41m",
    "\033[1;30;42m",
    "\033[1;37;40m"
]


def create_blank_board():
    board = []
    for i in range(0, 4):
        row = []
        for j in range(0, 4):
            row.append(0)
        board.append(row)
    return board


def create_old_board(board):
    old_board = []
    for i in range(len(board)):
        row = []
        for j in range(len(board[i])):
            row.append(board[i][j])
        old_board.append(row)
    return old_board


def rotate_board_horizontally(board):
    for i in range(len(board)):
        board[i] = board[i][::-1]
    return board


def rotate_board_up_to_left(board):
    temp_board = [[], [], [], []]
    for i in range(len(board)):
        for j in range(len(board[i])):
            temp_board[j].append(board[i][j])
    return temp_board


def board_did_change(old, new):
    for i in range(len(old)):
        for j in range(len(old[i])):
            if new[i][j] != old[i][j]:
                return True
    return False


def show_board(board):
    print("/" + "-" * 47 + "\\")
    for i in range(len(board)):
        for k in range(2):
            print("|", end="")
            for j in range(len(board[i])):
                print("{}{:^11s}{}".format(colors[get_tile_colors(board[i][j])] if board[i][j] != 0 else "", " ", "\033[0m" if board[i][j] != 0 else ""), end="|")
            print()
        for j in range(len(board[i])):
            print("|{}{:^11s}{}".format(colors[get_tile_colors(board[i][j])] if board[i][j] != 0 else "", str(board[i][j]) if board[i][j] != 0 else " ", "\033[0m" if board[i][j] != 0 else ""), end="")
        print("|")
        for k in range(2):
            print("|", end="")
            for j in range(len(board[i])):
                print("{}{:^11s}{}".format(colors[get_tile_colors(board[i][j])] if board[i][j] != 0 else "", " ", "\033[0m"), end="|")
            print()
        if i < len(board) - 1:
            print("|" + "-" * 47 + "|")
    print("\\" + "-" * 47 + "/")


def place_random_tile(board):
    while True:
        row = random.randint(0, len(board[0]) - 1)
        col = random.randint(0, len(board) - 1)
        if board[row][col] == 0:
            board[row][col] = 2
            return board


def move(board):
    board = board[:]
    while True:
        direction = input("Direction: ")
        if direction == "w":
            board = rotate_board_up_to_left(board)
            board = move_board_horizontal(board)
            board = rotate_board_up_to_left(board)
            break
        elif direction == "a":
            board = move_board_horizontal(board)
            break
        elif direction == "s":
            board = rotate_board_horizontally(rotate_board_up_to_left(board))
            board = move_board_horizontal(board)
            board = rotate_board_up_to_left(rotate_board_horizontally(board))
            break
        elif direction == "d":
            board = rotate_board_horizontally(move_board_horizontal(rotate_board_horizontally(board)))
            break
        else:
            print("Invalid direction")
    return board


def move_board_horizontal(board):
    for i in range(len(board)):
        for j in range(len(board[i]) - 1):
            same = same_after_tile(j, board[i])
            if isinstance(same, int):
                board[i][j] *= 2
                board[i][same] = 0
        for j in range(len(board[i])):
            leading_zeros = count_leading_zeros(board[i], j)
            if leading_zeros != 0:
                board[i] = shift_tiles_left(board[i], leading_zeros, j)
    return board


def same_after_tile(index, row):
    for i in range(index + 1, len(row)):
        if row[i] == 0:
            continue
        elif row[i] == row[index]:
            return i
        else:
            return None


def count_leading_zeros(row, index):
    for i in range(0, len(row) - index):
        if row[i + index] != 0:
            return i
    return 0


def shift_tiles_left(row, num, index):
    for i in range(index, len(row) - num):
        row[i], row[i + num] = row[i + num], 0
    return row


def main():
    init_terminal()
    board = create_blank_board()
    board = place_random_tile(board)
    while True:
        create_display()
        old_board = create_old_board(board)
        show_board(board)
        board = move(board)
        if board_did_change(old_board, board):
            board = place_random_tile(board)


if __name__ == "__main__":
    main()
