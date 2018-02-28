import random

class Board:

    def __init__(self):
        self.board = self.create_blank()
        self.score = 0

    def create_blank(self):
        return [[0, 0, 0, 0] for i in range(4)]

    def create_old(self):
        self.old_board = []
        for i in range(len(self.board)):
            row = []
            for j in range(len(self.board[i])):
                row.append(self.board[i][j])
            self.old_board.append(row)

    def rotate_horizontally(self):
        for i in range(len(self.board)):
            self.board[i] = self.board[i][::-1]

    def rotate_up_to_left(self):
        temp_board = [[], [], [], []]
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                temp_board[j].append(self.board[i][j])
        self.board = temp_board

    def same_after_tile(self, index, row):
        for i in range(index + 1, len(row)):
            if row[i] == 0:
                continue
            elif row[i] == row[index]:
                return i
            else:
                return None

    def count_leading_zeros(self, row, index):
        for i in range(0, len(row) - index):
            if row[i + index] != 0:
                return i
        return 0

    def shift_tiles(self, row, num, index):
        for i in range(index, len(row) - num):
            row[i], row[i + num] = row[i + num], 0
        return row

    def move_tiles(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i]) - 1):
                same = self.same_after_tile(j, self.board[i])
                if isinstance(same, int):
                    self.score += self.board[i][j]
                    self.board[i][j] *= 2
                    self.board[i][same] = 0
            for j in range(len(self.board[i])):
                leading_zeros = self.count_leading_zeros(self.board[i], j)
                if leading_zeros != 0:
                    self.board[i] = self.shift_tiles(self.board[i], leading_zeros, j)

    def move(self, direction):
        if direction == 119:
            self.rotate_up_to_left()
            self.move_tiles()
            self.rotate_up_to_left()
        elif direction == 97:
            self.move_tiles()
        elif direction == 115:
            self.rotate_up_to_left()
            self.rotate_horizontally()
            self.move_tiles()
            self.rotate_horizontally()
            self.rotate_up_to_left()
        elif direction == 100:
            self.rotate_horizontally()
            self.move_tiles()
            self.rotate_horizontally()
        

    def did_change(self):
        for i in range(len(self.old_board)):
            for j in range(len(self.old_board[i])):
                if self.board[i][j] != self.old_board[i][j]:
                    return True
        return False

    def place_tile(self):
        while True:
            row = random.randint(0, len(self.board[0]) - 1)
            col = random.randint(0, len(self.board) - 1)
            if self.board[row][col] == 0:
                self.board[row][col] = 2 if random.uniform(0, 1) > 0.4 else 4
                break

    def show(self):
        print("\r/" + "-" * 47 + "\\")
        for i in range(len(self.board)):
            for k in range(5):
                print("\r|", end="")
                for j in range(len(self.board[i])):
                    print("{}{:^11s}{}".format(colors[get_tile_colors(self.board[i][j])] if self.board[i][j] != 0 else "", str(self.board[i][j]) if self.board[i][j] != 0 and k == 2 else " ", "\033[0m" if self.board[i][j] != 0 else ""), end="|")
                print("\r")
            if i < len(self.board) - 1:
                print("\r|" + "-" * 47 + "|")
        print("\r\\" + "-" * 47 + "/\r")
        print("\n\r\033[1m" + "-" * 49)
        print("\r" + "Score: {}".format(self.score).center(49, " "))
        print("\r" + "-" * 49 + "\033[0m\r")

    def is_full(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    return False
        return True

    def is_lost(self):
        self.create_old()  # self.old_board
        for i in [119, 97, 115, 100]:
            self.move(i)
            if self.did_change():
                self.board = self.old_board
                return False
        return True


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