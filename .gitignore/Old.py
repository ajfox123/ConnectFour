import sys
import numpy as np
import time
import random
import copy
from functools import lru_cache


class Board():
    @lru_cache(maxsize=None)
    def __init__(self, board_string):
        self.board = np.array(list([i for i in x] for x in board_string.split(',')))
        self.nrows = self.board.shape[0]
        self.ncolumns = self.board.shape[1]
        self.r_tokens = np.count_nonzero(self.board == 'r')
        self.y_tokens = np.count_nonzero(self.board == 'y')
        self.rows = ["".join(row) for row in self.board]
        self.columns = ["".join(x[i] for x in self.rows[::-1]) for i in range(self.ncolumns)]
        self.diags_tl_to_br = ["".join(self.board[::-1, :].diagonal(i)) for i in range(-self.nrows + 1, self.ncolumns)]
        self.diags_bl_to_tr = ["".join(self.board.diagonal(i)) for i in range(self.ncolumns - 1, -self.nrows, -1)]
        self.checks = self.rows + self.columns + self.diags_bl_to_tr + self.diags_tl_to_br

    @lru_cache(maxsize=None)
    def update_board(self, piece, col, row):
        if piece == 'r':
            self.r_tokens += 1
        else:
            self.y_tokens += 1
        self.rows = ["".join(row) for row in self.board]
        self.columns = ["".join(x[i] for x in self.rows[::-1]) for i in range(self.ncolumns)]
        self.diags_tl_to_br = ["".join(self.board[::-1, :].diagonal(i)) for i in range(-self.nrows + 1, self.ncolumns)]
        self.diags_bl_to_tr = ["".join(self.board.diagonal(i)) for i in range(self.ncolumns - 1, -self.nrows, -1)]
        self.checks = self.rows + self.columns + self.diags_bl_to_tr + self.diags_tl_to_br

    @lru_cache(maxsize=None)
    def drop_piece(self, col, piece):
        last = self.columns[col][::-1].index('.')
        self.board[last, col] = piece
        self.update_board(piece, col, last)

    def display_board(self):
        for i, line in enumerate(self.board[::-1]):
            print(*line, sep='|')

    def evaluation(self, first_player, second_player):
        if self.utility(first_player):
            return 10000000000000
        if self.utility(second_player):
            return -10000000000000
        eval = self.score(first_player) - self.score(second_player)
        return eval

    def score(self, player):
        s = 0
        player_tokens = player + "_tokens"
        s += getattr(self, player_tokens)
        four = self.in_a_row(4, player)
        three = self.in_a_row(3, player) - (four * 2)
        two = self.in_a_row(2, player) - (three * 2 + four * 3)
        s += 1000 * four + 100 * three + 10 * two
        return s

    def in_a_row(self, n, player):
        sub = player * n
        c = 0
        for row in self.checks:
            start = 0
            while True:
                start = row.find(sub, start) + 1
                if start > 0:
                    c += 1
                else:
                    break
        return c

    @lru_cache(maxsize=None)
    def utility(self, piece):
        win = self.in_a_row(4, piece) > 0
        if win:
            return True
        return False


class ConnectFour():
    @lru_cache(maxsize=None)
    def __init__(self, turn, depth):
        turn_dict = {'red': 'r', 'yellow': 'y'}
        self.turn_1 = turn_dict[turn]
        self.turn_2 = 'y' if self.turn_1 == 'r' else 'r'
        self.depth = int(depth)
        self.c = 1

    @lru_cache(maxsize=None)
    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(board.ncolumns):
            if self.is_valid_drop(board.columns[col]):
                valid_locations.append(col)
        return valid_locations

    @lru_cache(maxsize=None)
    def is_valid_drop(self, col):
        if col[0] == '.':
            return True
        return False

    @lru_cache(maxsize=None)
    def min_max(self, d, board, first_player):
        valid_locations = self.get_valid_locations(board)
        no_move = len(valid_locations) == 0
        util_1 = board.utility(self.turn_1)
        util_2 = board.utility(self.turn_2)
        if util_1:
            return None, 10000000000000
        elif util_2:
            return None, -10000000000000
        elif no_move:
            return None, 0
        elif d == self.depth:
            return None, board.evaluation(self.turn_1, self.turn_2)

        if first_player:
            maxv = np.NINF
            column = random.choice(valid_locations)
            for col in valid_locations:
                self.c += 1
                b_copy = copy.deepcopy(board)
                b_copy.drop_piece(col, self.turn_1)
                # b_copy.display_board()
                m = self.min_max(d + 1, b_copy, False)[1]
                # b_copy.display_board()
                if m > maxv:
                    maxv = m
                    column = col
            return column, maxv

        else:
            minv = np.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                self.c += 1
                b_copy = copy.deepcopy(board)
                b_copy.drop_piece(col, self.turn_2)
                # b_copy.display_board()
                m = self.min_max(d + 1, b_copy, True)[1]
                if m < minv:
                    minv = m
                    column = col
            return column, minv

    @lru_cache(maxsize=None)
    def alpha_beta(self, d, board, a, b, first_player):
        valid_locations = self.get_valid_locations(board)
        no_move = len(valid_locations) == 0
        util_1 = board.utility(self.turn_1)
        util_2 = board.utility(self.turn_2)
        if util_1:
            return None, 10000000000000
        elif util_2:
            return None, -10000000000000
        elif no_move:
            return None, 0
        elif d == self.depth:
            return None, board.evaluation(self.turn_1, self.turn_2)

        if first_player:
            maxv = np.NINF
            column = random.choice(valid_locations)
            for col in valid_locations:
                self.c += 1
                b_copy = copy.deepcopy(board)
                b_copy.drop_piece(col, self.turn_1)
                b_copy.display_board()
                print(self.c)
                m = self.alpha_beta(d + 1, b_copy, a, b, False)[1]
                # b_copy.display_board()
                if m > maxv:
                    maxv = m
                    column = col
                a = max(a, maxv)
                if a >= b:
                    break
            return column, maxv

        else:
            minv = np.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                self.c += 1
                b_copy = copy.deepcopy(board)
                b_copy.drop_piece(col, self.turn_2)
                b_copy.display_board()
                print(self.c)
                m = self.alpha_beta(d + 1, b_copy, a, b, True)[1]
                if m < minv:
                    minv = m
                    column = col
                b = min(b, minv)
                if a >= b:
                    break
            return column, minv


if __name__ == '__main__':
    start = time.time()
    board = Board(sys.argv[1])
    game = ConnectFour(sys.argv[2], sys.argv[4])
    print("STARTING BOARD")
    board.display_board()
    print(board.evaluation(game.turn_1, game.turn_2))
    print("\n")
    if sys.argv[3] == 'A':
        recommended = game.alpha_beta(0, board, np.NINF, np.inf, True)
    else:
        recommended = game.min_max(0, board, True)
    print("\nAI RECOMMENDATION:", recommended[0])
    print("NODES EXPLORED:", game.c)
    if recommended[0] == None:
        print("GAME IS TERMINAL")
    else:
        board.drop_piece(recommended[0], game.turn_1)
        print("EVAL:", board.evaluation(game.turn_1, game.turn_2))
        print("BEST MOVE FOUND")
        board.display_board()
        print("python ConnectFour.py", [",".join(["".join(i) for i in board.board])]
              [0], 'yellow' if sys.argv[2] == 'red' else 'red', sys.argv[3], sys.argv[4])
    end = time.time()
    print(end - start)
