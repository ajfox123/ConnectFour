import sys
import numpy as np
import time
import pygame
import math


class Board():
    def __init__(self, board_string):
        self.board = self.board = np.array(np.array([[i for i in x] for x in board_string.split(',')]))
        self.won = ''
        self.r_tokens = np.count_nonzero(self.board == 'r')
        self.y_tokens = np.count_nonzero(self.board == 'y')
        self.nrows = self.board.shape[0]
        self.ncolumns = self.board.shape[1]
        self.rows = ["".join(row) for row in self.board]
        self.columns = ["".join(x[i] for x in self.rows[::-1]) for i in range(self.ncolumns)]
        self.diags_tl_to_br = ["".join(self.board[::-1, :].diagonal(i)) for i in range(-self.nrows + 1, self.ncolumns)]
        self.diags_bl_to_tr = ["".join(self.board.diagonal(i)) for i in range(self.ncolumns - 1, -self.nrows, -1)]
        self.checks = self.rows + self.columns + self.diags_bl_to_tr + self.diags_tl_to_br
        self.score_r = self.r_tokens
        self.score_y = self.y_tokens
        self.score_r += self.score('r')
        self.score_y += self.score('y')

    def score(self, player):
        s = 0
        four = self.in_a_row(4, player)
        three = self.in_a_row(3, player) - (four * 2)
        two = self.in_a_row(2, player) - (three * 2 + four * 3)
        s += 1000 * four + 100 * three + 10 * two
        if four > 0:
            self.won = player
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

    def display_board(self):
        for line in self.board[:: -1]:
            print(*line, sep='|')

    def drop_piece(self, row, col, piece):
        score_map = {0: 0, 1: 0, 2: 10, 3: 100, 4: 1000}
        score_increase = 1
        self.board[row, col] = piece

        tokens_below = 0
        i = 1
        while i <= 5 and self.board[row - i, col] == piece:
            tokens_below += 1
            i += 1
        new_length = min(tokens_below + 1, 4)
        if new_length == 4:
            self.won = piece
        score_increase += score_map[new_length] - score_map[tokens_below]

        tokens_left = 0
        i = col - 1
        while i >= 0 and self.board[row, i] == piece:
            tokens_left += 1
            i -= 1
        tokens_right = 0
        i = col + 1
        while i <= 6 and self.board[row, i] == piece:
            tokens_right += 1
            i += 1
        new_length = min(tokens_left + tokens_right + 1, 4)
        if new_length == 4:
            self.won = piece
        old_length_left = min(tokens_left, 4)
        old_length_right = min(tokens_right, 4)
        score_increase += score_map[new_length] - (score_map[old_length_left] + score_map[old_length_right])

        tokens_up_right = 0
        i = 1
        while row + i <= 5 and col + i <= 6 and self.board[row + i, col + i] == piece:
            tokens_up_right += 1
            i += 1
        tokens_down_left = 0
        i = 1
        while row - i >= 0 and col - i >= 0 and self.board[row - i, col - i] == piece:
            tokens_down_left += 1
            i += 1
        new_length = min(tokens_up_right + tokens_down_left + 1, 4)
        if new_length == 4:
            self.won = piece
        old_length_up_right = min(tokens_up_right, 4)
        old_length_down_left = min(tokens_down_left, 4)
        score_increase += score_map[new_length] - (score_map[old_length_up_right] + score_map[old_length_down_left])

        tokens_up_left = 0
        i = 1
        while row + i <= 5 and col - i >= 0 and self.board[row + i, col - i] == piece:
            tokens_up_left += 1
            i += 1
        tokens_down_right = 0
        i = 1
        while row - i >= 0 and col + i <= 6 and self.board[row - i, col + i] == piece:
            tokens_down_right += 1
            i += 1
        new_length = min(tokens_up_left + tokens_down_right + 1, 4)
        if new_length == 4:
            self.won = piece
        old_length_up_left = min(tokens_up_left, 4)
        old_length_down_right = min(tokens_down_right, 4)
        score_increase += score_map[new_length] - (score_map[old_length_up_left] + score_map[old_length_down_right])

        if piece == 'r':
            self.score_r += score_increase
        else:
            self.score_y += score_increase

    def utility(self, player):
        if self.won == player:
            return True
        return False

    def evaluation(self, first_player, second_player):
        if first_player == 'r':
            return self.score_r - self.score_y
        return self.score_y - self.score_r


class ConnectFour():
    def __init__(self, turn, depth):
        self.turn_1 = turn
        self.turn_2 = 'r'
        self.depth = int(depth)

    def get_valid_locations(self, board_array):
        valid_locations = [3, 2, 4, 1, 5, 0, 6]
        for col in range(7):
            if not self.is_valid_drop(board_array[5], col):
                valid_locations.remove(col)
        return valid_locations

    def get_next_open_row(self, board_array, col):
        for row in range(6):
            if board_array[row, col] == '.':
                return row

    def is_valid_drop(self, last_row, col):
        if last_row[col] == '.':
            return True
        return False

    def alpha_beta(self, d, board, a, b, first_player):
        valid_locations = self.get_valid_locations(board.board)
        no_move = len(valid_locations) == 0
        util_1 = board.utility(self.turn_1)
        util_2 = board.utility(self.turn_2)
        if util_1:
            return None, 10000
        elif util_2:
            return None, -10000
        elif no_move:
            return None, 0
        elif d == self.depth:
            return None, board.evaluation(self.turn_1, self.turn_2)

        if first_player:
            maxv = np.NINF
            for col in valid_locations:
                row = self.get_next_open_row(board.board, col)
                curr_score_1 = board.score_r if self.turn_1 == 'r' else board.score_y
                curr_score_2 = board.score_y if self.turn_2 == 'y' else board.score_r
                was_won = board.won != ''
                board.drop_piece(row, col, self.turn_1)
                if d == 0 and board.utility(self.turn_1):
                    board.board[row, col] = '.'
                    board.score_r = curr_score_1 if self.turn_1 == 'r' else curr_score_2
                    board.score_y = curr_score_2 if self.turn_2 == 'y' else curr_score_1
                    if not was_won:
                        board.won = ''
                    return col, board.evaluation(self.turn_1, self.turn_2)
                m = self.alpha_beta(d + 1, board, a, b, False)[1]
                board.board[row, col] = '.'
                board.score_r = curr_score_1 if self.turn_1 == 'r' else curr_score_2
                board.score_y = curr_score_2 if self.turn_2 == 'y' else curr_score_1
                if not was_won:
                    board.won = ''
                if m > maxv:
                    maxv = m
                    column = col
                a = max(a, maxv)
                if a >= b:
                    break
            return column, maxv

        else:
            minv = np.inf
            for col in valid_locations:
                row = self.get_next_open_row(board.board, col)
                curr_score_1 = board.score_r if self.turn_1 == 'r' else board.score_y
                curr_score_2 = board.score_r if self.turn_2 == 'r' else board.score_y
                was_won = board.won != ''
                board.drop_piece(row, col, self.turn_2)
                m = self.alpha_beta(d + 1, board, a, b, True)[1]
                board.board[row, col] = '.'
                board.score_r = curr_score_1 if self.turn_1 == 'r' else curr_score_2
                board.score_y = curr_score_1 if self.turn_1 == 'y' else curr_score_2
                if not was_won:
                    board.won = ''
                if m < minv:
                    minv = m
                    column = col
                b = min(b, minv)
                if a >= b:
                    break
            return column, minv


def draw_board(board):
    for c in range(7):
        for r in range(6):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                               int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    for c in range(7):
        for r in range(6):
            if board[r, c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                                 height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r, c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                                    height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


if __name__ == '__main__':
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    SQUARESIZE = 100

    width = 7 * SQUARESIZE
    height = (6 + 1) * SQUARESIZE

    size = (width, height)

    RADIUS = int(SQUARESIZE / 2 - 5)

    PLAYER = 0
    AI = 1
    EMPTY = '.'
    PLAYER_PIECE = 'r'
    AI_PIECE = 'y'
    moves = 0

    board_string = '.......,.......,.......,.......,.......,.......'
    board = Board(board_string)
    search_depth = 4
    game = ConnectFour(AI_PIECE, search_depth)
    game_over = False
    turn = PLAYER
    pygame.init()
    screen = pygame.display.set_mode(size)
    draw_board(board.board)
    pygame.display.update()
    myfont = pygame.font.SysFont("monospace", 75)

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))
                    row = game.get_next_open_row(board.board, col)
                    if row is not None:
                        board.drop_piece(row, col, PLAYER_PIECE)

                        if board.utility(PLAYER_PIECE):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                        moves += 1
                        if moves == 42 and not board.utility(PLAYER_PIECE):
                            label = myfont.render("It's a draw...", 1, BLUE)
                            screen.blit(label, (40, 10))
                            game_over = True

                        draw_board(board.board)
                        turn += 1
                        turn = turn % 2
                    else:
                        label = myfont.render("Invalid column. Try again.", 1, BLUE)
                        screen.blit(label, (40, 10))

        if turn == AI and not game_over:
            col, minimax_score = game.alpha_beta(0, board, np.NINF, np.inf, True)
            if game.is_valid_drop(board.board[game.get_next_open_row(board.board, col)], col):
                row = game.get_next_open_row(board.board, col)
                board.drop_piece(row, col, AI_PIECE)

                if board.utility(AI_PIECE):
                    label = myfont.render("AI wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                moves += 1
                if moves == 42 and not board.utility(AI_PIECE):
                    label = myfont.render("It's a draw...", 1, BLUE)
                    game_over = True

                draw_board(board.board)
                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)
