import pygame
import numpy as np
import sys
from base_game import BoardGame

ROWS = 10
COLS = 10
CELL_SIZE = 60

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

WHITE = (255, 253, 208)
GOLD = (212, 175, 55)
BLUE = (1, 120, 144)
YELLOW = (255, 215, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


class TicTacToe(BoardGame):
    def __init__(self, player1, player2):
        super().__init__(player1, player2, ROWS, COLS)
        self.board = np.zeros((ROWS, COLS))

    def check_win(self):
        p = self.current_player
        b = self.board

        # Horizontal
        for r in range(self.rows):
            for c in range(self.cols - 4):
                if np.all(b[r, c:c+5] == p):
                    return (r, c), (r, c+4)

        # Vertical
        for c in range(self.cols):
            for r in range(self.rows - 4):
                if np.all(b[r:r+5, c] == p):
                    return (r, c), (r+4, c)

        # Diagonal \
        for r in range(self.rows - 4):
            for c in range(self.cols - 4):
                if all(b[r+i][c+i] == p for i in range(5)):
                    return (r, c), (r+4, c+4)

        # Diagonal /
        for r in range(self.rows - 4):
            for c in range(4, self.cols):
                if all(b[r+i][c-i] == p for i in range(5)):
                    return (r, c), (r+4, c-4)

        return None

    def mark_box(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            if self.board[r][c] == 0:
                self.board[r][c] = self.current_player
                return True
        return False


def draw_board(screen, game):
    screen.fill(WHITE)

    for r in range(game.rows):
        for c in range(game.cols):
            pygame.draw.rect(
                screen, GOLD,
                (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1
            )

            if game.board[r][c] == 1:
                pygame.draw.line(
                    screen, BLUE,
                    (c * CELL_SIZE + 10, r * CELL_SIZE + 10),
                    (c * CELL_SIZE + CELL_SIZE - 10, r * CELL_SIZE + CELL_SIZE - 10), 3
                )
                pygame.draw.line(
                    screen, BLUE,
                    (c * CELL_SIZE + CELL_SIZE - 10, r * CELL_SIZE + 10),
                    (c * CELL_SIZE + 10, r * CELL_SIZE + CELL_SIZE - 10), 3
                )

            elif game.board[r][c] == 2:
                pygame.draw.circle(
                    screen, YELLOW,
                    (c * CELL_SIZE + CELL_SIZE // 2,
                     r * CELL_SIZE + CELL_SIZE // 2),
                    CELL_SIZE // 3, 3
                )


def draw_winning_line(screen, start, end):
    r1, c1 = start
    r2, c2 = end

    x1 = c1 * CELL_SIZE + CELL_SIZE // 2
    y1 = r1 * CELL_SIZE + CELL_SIZE // 2
    x2 = c2 * CELL_SIZE + CELL_SIZE // 2
    y2 = r2 * CELL_SIZE + CELL_SIZE // 2

    pygame.draw.line(screen, RED, (x1, y1), (x2, y2), 5)


def show_winner(screen, text):
    font = pygame.font.SysFont(None, 60)
    render = font.render(text, True, BLACK)
    rect = render.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(render, rect)


def run_game(player1, player2):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TIC-TAC-TOE ")

    game = TicTacToe(player1, player2)
    winner = None
    running = True

    while running:
        draw_board(screen, game)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and winner is None:
                x, y = event.pos
                c = x // CELL_SIZE
                r = y // CELL_SIZE

                if game.mark_box(r, c):

                    win_result = game.check_win()

                    if win_result:
                        winner = game.get_current_player_name()
                        start, end = win_result

                        draw_board(screen, game)
                        draw_winning_line(screen, start, end)
                        show_winner(screen, f"{winner} Wins!")

                        pygame.display.update()
                        pygame.time.delay(3000)
                        running = False
                        break

                    game.switch_turn()

        pygame.display.update()

    pygame.quit()
    return winner


# For testing directly
if __name__ == "__main__":
    p1 = sys.argv[1] if len(sys.argv) > 1 else "Player1"
    p2 = sys.argv[2] if len(sys.argv) > 2 else "Player2"

    run_game(p1, p2)
