print("game started")
import pygame
import numpy as np
import sys

ROWS = 7
COLS = 7
CELL_SIZE = 80

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)


def check_win(board, player):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == player for i in range(4)):
                return True

    # vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == player for i in range(4)):
                return True

    # diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == player for i in range(4)):
                return True

    # diagonal /
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            if all(board[r+i][c-i] == player for i in range(4)):
                return True

    return False



def draw_board(screen, board):
    screen.fill(WHITE)

    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(screen, BLACK,
                             (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

            if board[r][c] == 1:
                pygame.draw.circle(screen, RED,
                                   (c*CELL_SIZE + 40, r*CELL_SIZE + 40), 30)

            elif board[r][c] == 2:
                pygame.draw.circle(screen, BLUE,
                                   (c*CELL_SIZE + 40, r*CELL_SIZE + 40), 30)



def drop_piece(board, col, player):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            board[r][col] = player
            return True
    return False



def run_game(player1, player2):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect 4")

    board = np.zeros((ROWS, COLS))
    current_player = 1
    winner = None

    running = True

    while running:
        draw_board(screen, board)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and winner is None:
                x, _ = event.pos
                col = x // CELL_SIZE

                # place coin
                if drop_piece(board, col, current_player):

                    # check win
                    if check_win(board, current_player):
                        winner = player1 if current_player == 1 else player2
                        print("Winner:", winner)
                        pygame.time.delay(2000)
                        running = False

                    # switch turn
                    current_player = 2 if current_player == 1 else 1

        pygame.display.update()

    pygame.quit()
    return winner



if __name__ == "__main__":
    run_game("Player1", "Player2")