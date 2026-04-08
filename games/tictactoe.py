import pygame
import sys
import numpy as np

# -------- BASE CLASS --------
class BoardGame:
    def __init__(self, p1, p2, size):
        self.players = [p1, p2]
        self.turn = 0
        self.size = size
        self.board = np.zeros((size, size), dtype=int)

    def switch_turn(self):
        self.turn = 1 - self.turn

    def current_player(self):
        return self.players[self.turn]

    def mark(self):
        return self.turn + 1


# -------- TIC TAC TOE --------
class TicTacToe(BoardGame):
    def __init__(self, p1, p2):
        super().__init__(p1, p2, 10)
        self.k = 5

    def check_win(self):
        b = self.board

        h = (b[:, :-4] == b[:, 1:-3]) & \
            (b[:, :-4] == b[:, 2:-2]) & \
            (b[:, :-4] == b[:, 3:-1]) & \
            (b[:, :-4] == b[:, 4:]) & \
            (b[:, :-4] != 0)

        v = (b[:-4, :] == b[1:-3, :]) & \
            (b[:-4, :] == b[2:-2, :]) & \
            (b[:-4, :] == b[3:-1, :]) & \
            (b[:-4, :] == b[4:, :]) & \
            (b[:-4, :] != 0)

        d1 = (b[:-4, :-4] == b[1:-3, 1:-3]) & \
             (b[:-4, :-4] == b[2:-2, 2:-2]) & \
             (b[:-4, :-4] == b[3:-1, 3:-1]) & \
             (b[:-4, :-4] == b[4:, 4:]) & \
             (b[:-4, :-4] != 0)

        d2 = (b[4:, :-4] == b[3:-1, 1:-3]) & \
             (b[4:, :-4] == b[2:-2, 2:-2]) & \
             (b[4:, :-4] == b[1:-3, 3:-1]) & \
             (b[4:, :-4] == b[:-4, 4:]) & \
             (b[4:, :-4] != 0)

        return np.any(h) or np.any(v) or np.any(d1) or np.any(d2)


# -------- GUI --------
class GUI:
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.size = 600
        self.cell = self.size // game.size

        self.screen = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Tic Tac Toe 10x10")

    def draw(self):
        self.screen.fill((255, 255, 255))

        # grid
        for i in range(self.game.size):
            pygame.draw.line(self.screen, (0, 0, 0),
                             (0, i * self.cell), (self.size, i * self.cell))
            pygame.draw.line(self.screen, (0, 0, 0),
                             (i * self.cell, 0), (i * self.cell, self.size))

        # marks
        for r in range(self.game.size):
            for c in range(self.game.size):
                val = self.game.board[r][c]

                if val == 1:
                    pygame.draw.circle(self.screen, (0, 0, 255),
                                       (c*self.cell + self.cell//2,
                                        r*self.cell + self.cell//2),
                                       self.cell//3, 2)

                elif val == 2:
                    pygame.draw.line(self.screen, (255, 0, 0),
                                     (c*self.cell+5, r*self.cell+5),
                                     (c*self.cell+self.cell-5, r*self.cell+self.cell-5), 2)
                    pygame.draw.line(self.screen, (255, 0, 0),
                                     (c*self.cell+self.cell-5, r*self.cell+5),
                                     (c*self.cell+5, r*self.cell+self.cell-5), 2)

    def run(self):
        while True:
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    c = x // self.cell
                    r = y // self.cell

                    if self.game.board[r][c] == 0:
                        self.game.board[r][c] = self.game.mark()

                        if self.game.check_win():
                            print(self.game.current_player(), "wins!")
                            pygame.time.wait(2000)
                            return

                        self.game.switch_turn()

            pygame.display.update()


# -------- START FUNCTION --------
def start(p1, p2):
    game = TicTacToe(p1, p2)
    gui = GUI(game)
    gui.run()


# -------- DIRECT RUN (FOR TESTING) --------
if __name__ == "__main__":
    start("A", "B")