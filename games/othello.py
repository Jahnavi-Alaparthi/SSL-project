import pygame
import sys
import numpy as np

SIZE = 8
CELL = 80

WIDTH = SIZE * CELL
HEIGHT = SIZE * CELL + 50  # space for text

# colours
WHITE = (255, 255, 255)
GREEN = (0, 120, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
BLUE = (0, 0, 255)


# using base class
class Game:
    def __init__(self):
        self.board = np.zeros((SIZE, SIZE))

        mid = SIZE // 2
        self.board[mid-1][mid-1] = 2
        self.board[mid][mid] = 2
        self.board[mid-1][mid] = 1
        self.board[mid][mid-1] = 1


# code for othello game
class Othello(Game):

    def draw_board(self, screen, current):
        screen.fill(WHITE)

        current_moves = self.get_moves(current)
        other = 2 if current == 1 else 1
        other_moves = self.get_moves(other)

        for r in range(SIZE):
            for c in range(SIZE):
                pygame.draw.rect(screen, GREEN,
                                 (c*CELL, r*CELL, CELL, CELL))
                pygame.draw.rect(screen, BLACK,
                                 (c*CELL, r*CELL, CELL, CELL), 2)

                # yellow colours for Current player moves
                if (r, c) in current_moves:
                    pygame.draw.circle(screen, YELLOW,
                                       (c*CELL + CELL//2, r*CELL + CELL//2), 8)

                # blue colour for Other player moves
                elif (r, c) in other_moves:
                    pygame.draw.circle(screen, BLUE,
                                       (c*CELL + CELL//2, r*CELL + CELL//2), 6)

                # black and white coins
                if self.board[r][c] == 1:
                    pygame.draw.circle(screen, BLACK,
                                       (c*CELL + CELL//2, r*CELL + CELL//2), 32)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(screen, WHITE,
                                       (c*CELL + CELL//2, r*CELL + CELL//2), 32)

    def is_valid(self, r, c, player):
        if self.board[r][c] != 0:
            return False

        opp = 2 if player == 1 else 1
        dirs = [(-1,-1), (-1,0), (-1,1),
                (0,-1),         (0,1),
                (1,-1), (1,0), (1,1)]

        for dr, dc in dirs:
            x, y = r+dr, c+dc
            found = False

            while 0 <= x < SIZE and 0 <= y < SIZE:
                if self.board[x][y] == opp:
                    found = True
                elif self.board[x][y] == player:
                    if found:
                        return True
                    break
                else:
                    break

                x += dr
                y += dc

        return False

    def make_move(self, r, c, player):
        opp = 2 if player == 1 else 1
        self.board[r][c] = player

        dirs = [(-1,-1), (-1,0), (-1,1),
                (0,-1),         (0,1),
                (1,-1), (1,0), (1,1)]

        for dr, dc in dirs:
            x, y = r+dr, c+dc
            path = []

            while 0 <= x < SIZE and 0 <= y < SIZE:
                if self.board[x][y] == opp:
                    path.append((x, y))
                elif self.board[x][y] == player:
                    for px, py in path:
                        self.board[px][py] = player
                    break
                else:
                    break
                x += dr
                y += dc

    def get_moves(self, player):
        return [(r, c) for r in range(SIZE)
                        for c in range(SIZE)
                        if self.is_valid(r, c, player)]

    def get_winner(self, p1, p2):
        b = np.sum(self.board == 1)
        w = np.sum(self.board == 2)

        if b > w:
            return p1
        elif w > b:
            return p2
        else:
            return "Draw"


# main game 
def run_othello(player1, player2):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Othello")

    font = pygame.font.SysFont(None, 40)
    win_font = pygame.font.SysFont(None, 60)

    game = Othello()
    current = 1
    winner = None

    running = True

    while running:
        game.draw_board(screen, current)

        # shows who turn it is
        turn_text = "Black Turn" if current == 1 else "White Turn"
        text = font.render(turn_text, True, BLACK)
        screen.blit(text, (10, HEIGHT - 40))

        # shows name of winner
        if winner:
            screen.fill(WHITE)
            win_text = win_font.render(f"🏆 {winner} Wins!", True, BLACK)
            rect = win_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(win_text, rect)
            pygame.display.update()
            pygame.time.delay(3000)
            break

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                c = x // CELL
                r = y // CELL

                if r < SIZE and c < SIZE:
                    if (r, c) in game.get_moves(current):
                        game.make_move(r, c, current)

                        # switch player
                        current = 2 if current == 1 else 1

                        # check game over
                        if not game.get_moves(1) and not game.get_moves(2):
                            winner = game.get_winner(player1, player2)

        pygame.display.update()

    pygame.quit()
    return winner


# run the game
if __name__ == "__main__":
    run_othello("Player1", "Player2")

