
import pygame
import numpy as np
import sys
from base_game import BoardGame

ROWS = 7
COLS = 7
CELL_SIZE = 80

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GREEN = (0, 200, 0)

class Connect4(BoardGame):
    def __init__(self, player1, player2):
        super().__init__(player1, player2, ROWS, COLS)
        self.board = np.zeros((ROWS, COLS))

    def check_win(self):
        p = self.current_player
        b = self.board

        # Horizontal
        for r in range(self.rows):
            for c in range(self.cols - 3):
                if np.all(b[r, c:c+4] == p):
                    return (r, c), (r, c+3)

        # Vertical
        for c in range(self.cols):
            for r in range(self.rows - 3):
                if np.all(b[r:r+4, c] == p):
                    return (r, c), (r+3, c)

        # Diagonal \
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                if all(b[r+i][c+i] == p for i in range(4)):
                    return (r, c), (r+3, c+3)

        # Diagonal /
        for r in range(self.rows - 3):
            for c in range(3 , self.cols):
                if all(b[r+i][c-i] == p for i in range(4)):
                    return (r, c), (r+3, c-3)

        return None
 
    # Drop the coin in the specified column for the current player 
    def drop_piece(self, c):
        if 0 <= c < self.cols:
            for r in range(self.rows - 1, -1, -1):
                if self.board[r][c] == 0:
                    self.board[r][c] = self.current_player
                    return True
        return False

# making the board and marking the box when the player clicks on the column
def draw_board(screen, game):
    screen.fill(WHITE)

    for r in range(game.rows):
        for c in range(game.cols):
            pygame.draw.rect(
                screen, BLACK,
                (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1
            )

            if game.board[r][c] == 1:
                
                pygame.draw.circle(
                    screen, RED,
                    (c*CELL_SIZE + 40, r*CELL_SIZE + 40), 30)

                

            elif game.board[r][c] == 2:
                pygame.draw.circle(
                    screen, BLUE,
                    (c*CELL_SIZE + 40, r*CELL_SIZE + 40), 30)


def draw_winning_line(screen, start, end):
    r1, c1 = start
    r2, c2 = end

    x1 = c1 * CELL_SIZE + CELL_SIZE // 2
    y1 = r1 * CELL_SIZE + CELL_SIZE // 2
    x2 = c2 * CELL_SIZE + CELL_SIZE // 2
    y2 = r2 * CELL_SIZE + CELL_SIZE // 2

    pygame.draw.line(screen, GREEN, (x1, y1), (x2, y2), 4)


def show_winner(screen, text):
    font = pygame.font.SysFont(None, 60)
    render = font.render(text, True,  GREEN)
    rect = render.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(render, rect)


def run_game(player1, player2):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect 4")

    game = Connect4(player1, player2)
    winner = None
    running = True

    while running:
        draw_board(screen, game)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and winner is None:
                x, _ = event.pos
                c = x // CELL_SIZE
                

                if game.drop_piece(c):

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


 
