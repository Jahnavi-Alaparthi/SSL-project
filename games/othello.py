import pygame
import numpy as np
import sys
from base_game import BoardGame

ROWS = 8
COLS = 8
CELL_SIZE = 60

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

BLACK = (0, 0, 0)
WHITE = (245, 245, 245)
GREEN = (0, 140, 0)
RED = (255, 0, 0)

class Othello(BoardGame):
    def __init__(self, player1, player2):
        super().__init__(player1, player2, ROWS, COLS)
        self.board = np.zeros((ROWS, COLS), dtype=int)

        self.board[3][3] = 2
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = 2

    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]

    def get_flips(self, r, c, player):
        if self.board[r][c] != 0:
            return []

        opponent = 2 if player == 1 else 1
        flips = []

        for dr, dc in self.directions:
            x, y = r + dr, c + dc
            path = []

            while 0 <= x < self.rows and 0 <= y < self.cols:
                if self.board[x][y] == opponent:
                    path.append((x, y))
                elif self.board[x][y] == player:
                    if path:
                        flips.extend(path)
                    break
                else:
                    break

                x += dr
                y += dc

        return flips

    def get_valid_moves(self, player):
        moves = {}
        for r in range(self.rows):
            for c in range(self.cols):
                flips = self.get_flips(r, c, player)
                if flips:
                    moves[(r, c)] = flips
        return moves

    def apply_move(self, r, c, player, flips):
        self.board[r][c] = player
        for x, y in flips:
            self.board[x][y] = player

    def check_win(self):
        p1 = np.sum(self.board == 1)
        p2 = np.sum(self.board == 2)

        if not self.get_valid_moves(1) and not self.get_valid_moves(2):
            if p1 > p2:
                return "Player 1 Wins"
            elif p2 > p1:
                return "Player 2 Wins"
            else:
                return "Draw"
        return None
    
def draw_board(screen, game, valid_moves):
    screen.fill(GREEN)

    for r in range(game.rows):
        for c in range(game.cols):

            rect = pygame.Rect(
                c * CELL_SIZE,
                r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(screen, BLACK, rect, 2)

            center = (
                c * CELL_SIZE + CELL_SIZE // 2,
                r * CELL_SIZE + CELL_SIZE // 2
            )

            value = game.board[r][c]

            if value == 1:
                pygame.draw.circle(screen, BLACK, center, 22)
            elif value == 2:
                pygame.draw.circle(screen, WHITE, center, 22)

            # legal move hints
            if (r, c) in valid_moves:
                hint_color = BLACK if game.current_player == 1 else WHITE
                pygame.draw.circle(screen, hint_color, center, 6)


def show_text(screen, text):
    font = pygame.font.SysFont(None, 60)
    render = font.render(text, True, RED)
    rect = render.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(render, rect)



def run_game(player1, player2):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Othello")

    game = Othello(player1, player2)
    winner = None
    running = True

    while running:

        valid_moves = game.get_valid_moves(game.current_player)

        
        if not valid_moves:
            game.switch_turn()
            valid_moves = game.get_valid_moves(game.current_player)

            if not valid_moves:
                winner = game.check_win()
                break

        draw_board(screen, game, valid_moves)
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                c = x // CELL_SIZE
                r = y // CELL_SIZE

                if (r, c) in valid_moves:
                    game.apply_move(
                        r, c,
                        game.current_player,
                        valid_moves[(r, c)]
                    )

                    winner = game.check_win()
                    if winner:
                        running = False
                        break

                    game.switch_turn()

    
    if winner:
        draw_board(screen, game, {})
        show_text(screen, winner)
        pygame.display.update()
        pygame.time.delay(3000)

    pygame.quit()
    return winner



if __name__ == "__main__":
    p1 = sys.argv[1] if len(sys.argv) > 1 else "Player1"
    p2 = sys.argv[2] if len(sys.argv) > 2 else "Player2"

    run_game(p1, p2)
