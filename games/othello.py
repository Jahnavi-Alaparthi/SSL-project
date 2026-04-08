import pygame
import numpy as np
from game import BoardGame


class Othello(BoardGame):

    def __init__(self, player1, player2):
        super().__init__(player1, player2, ["B", "W"])

        self.size = 8
        self.cell_size = 70

        self.board = np.full((self.size, self.size), "")
        self.game_over = False

        # Initial 4 pieces
        mid = self.size // 2
        self.board[mid-1][mid-1] = "W"
        self.board[mid][mid] = "W"
        self.board[mid-1][mid] = "B"
        self.board[mid][mid-1] = "B"

    def draw(self, screen):
        for row in range(self.size):
            for col in range(self.size):

                pygame.draw.rect(
                    screen,
                    (0, 128, 0),
                    (col * self.cell_size,
                     row * self.cell_size,
                     self.cell_size,
                     self.cell_size)
                )

                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (col * self.cell_size,
                     row * self.cell_size,
                     self.cell_size,
                     self.cell_size),
                    1
                )

                piece = self.board[row][col]

                if piece == "B":
                    pygame.draw.circle(
                        screen, (0, 0, 0),
                        (col * self.cell_size + self.cell_size // 2,
                         row * self.cell_size + self.cell_size // 2),
                        self.cell_size // 3
                    )

                elif piece == "W":
                    pygame.draw.circle(
                        screen, (255, 255, 255),
                        (col * self.cell_size + self.cell_size // 2,
                         row * self.cell_size + self.cell_size // 2),
                        self.cell_size // 3
                    )

    def handle_click(self, pos):
        if self.game_over:
            return

        x, y = pos
        row = y // self.cell_size
        col = x // self.cell_size

        if not self.is_valid_move(row, col):
            return

        symbol = self.get_symbol()
        self.board[row][col] = symbol

        self.flip_pieces(row, col, symbol)

        self.switch_turn()

    def is_valid_move(self, row, col):
        if self.board[row][col] != "":
            return False

        symbol = self.get_symbol()
        opponent = "W" if symbol == "B" else "B"

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0),  (1, 1)
        ]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            found_opponent = False

            while 0 <= r < self.size and 0 <= c < self.size:
                if self.board[r][c] == opponent:
                    found_opponent = True
                elif self.board[r][c] == symbol:
                    if found_opponent:
                        return True
                    break
                else:
                    break

                r += dr
                c += dc

        return False

    def flip_pieces(self, row, col, symbol):

        opponent = "W" if symbol == "B" else "B"

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0),  (1, 1)
        ]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            path = []

            while 0 <= r < self.size and 0 <= c < self.size:
                if self.board[r][c] == opponent:
                    path.append((r, c))
                elif self.board[r][c] == symbol:
                    for pr, pc in path:
                        self.board[pr][pc] = symbol
                    break
                else:
                    break

                r += dr
                c += dc
