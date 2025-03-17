import collections
import copy
import itertools
import random
import math

############################################################
# Section 1: Blockade Game
############################################################


def create_blockade_game(rows, cols):
    return BlockadeGame([[False]*cols for _ in range(rows)])


class BlockadeGame(object):

    # Required
    def __init__(self, board):
        self._board = board
        self._row = len(board)
        self._col = len(board[0])

    def get_board(self):
        return self._board

    def reset(self):
        self._board = [[False]*self._col for _ in range(self._row)]

    def is_legal_move(self, row, col, vertical):
        if vertical:
            nr, nc = row+1, col
        else:
            nr, nc = row, col+1
        if (row < 0 or col < 0 or nr < 0 or nc < 0 or
                row > self._row-1 or col > self._col-1 or
                nr > self._row-1 or nc > self._col-1 or
                self._board[row][col] or self._board[nr][nc]):
            return False
        return True

    def legal_moves(self, vertical):
        for r in range(self._row):
            for c in range(self._col):
                if self.is_legal_move(r, c, vertical):
                    yield (r, c)


    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row, col, vertical):
            if vertical:
                nr, nc = row + 1, col
            else:
                nr, nc = row, col + 1
            self._board[row][col] = True
            self._board[nr][nc] = True

    def game_over(self, vertical):
        if len(list(self.legal_moves(vertical))) == 0:
            return True
        return False

    def copy(self):
        return BlockadeGame([row[:] for row in self._board])

    def successors(self, vertical):
        for r in range(self._row):
            for c in range(self._col):
                if self.is_legal_move(r, c, vertical):
                    copy = self.copy()
                    copy.perform_move(r, c, vertical)
                    yield (r, c), copy

    def get_random_move(self, vertical):
        return random.choice(list(self.legal_moves(vertical)))

    # Required
    def get_best_move(self, vertical, limit):
        def get_value(state, limit, is_max_turn, move, alpha, beta):
            if limit == 0 or state.game_over(is_max_turn):
                player_moves = len(list(state.legal_moves(True)))
                opponent_moves = len(list(state.legal_moves(False)))
                return (move, player_moves - opponent_moves, 1)
            if is_max_turn:
                return max_value(state, limit, is_max_turn, move, alpha, beta)
            else:
                return min_value(state, limit, is_max_turn, move, alpha, beta)

        def max_value(state, limit_remain, is_max_turn, move, alpha, beta):
            best_value = -float("inf")
            nodes = 0
            best_move = move
            for next_step, successor in state.successors(is_max_turn):
                _, value, node = get_value(successor, limit_remain-1, not is_max_turn, next_step, alpha, beta)
                nodes += node
                if value > best_value:
                    best_move = next_step
                    best_value = value
                if value >= beta:
                    return best_move, best_value, nodes
                alpha = max(alpha, best_value)
            return best_move, best_value, nodes

        def min_value(state, limit_remain, is_max_turn, move, alpha, beta):
            best_value = float("inf")
            nodes = 0
            best_move = move
            for next_step, successor in state.successors(is_max_turn):
                _, value, node = get_value(successor, limit_remain-1, not is_max_turn, next_step, alpha, beta)
                nodes += node
                if value < best_value:
                    best_move = next_step
                    best_value = value
                if value <= alpha:
                    return best_move, best_value, nodes
                beta = min(beta, best_value)
            return best_move, best_value, nodes

        return get_value(self.copy(), limit, vertical, None, -float('inf'), float('inf'))

