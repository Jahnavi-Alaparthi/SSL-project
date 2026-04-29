import pygame
import numpy as np
import sys
from games.base_game import BoardGame

SIZE = 8
CELL = 60

WIDTH = SIZE * CELL
HEIGHT = SIZE * CELL + 50

WHITE = (255,255,255)
GREEN = (0,120,0)
BLACK = (0,0,0)


class Othello(BoardGame):
    def __init__(self, player1, player2):
        super().__init__(player1, player2, SIZE, SIZE)

        self.board = np.zeros((SIZE, SIZE))

        mid = SIZE // 2
        self.board[mid-1][mid-1] = 2
        self.board[mid][mid] = 2
        self.board[mid-1][mid] = 1
        self.board[mid][mid-1] = 1

    def is_valid(self, r, c, player):
        if self.board[r][c] != 0:
            return False

        opp = 2 if player == 1 else 1
        dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

        for dr,dc in dirs:
            x,y = r+dr,c+dc
            found=False

            while 0<=x<SIZE and 0<=y<SIZE:
                if self.board[x][y]==opp:
                    found=True
                elif self.board[x][y]==player:
                    if found:
                        return True
                    break
                else:
                    break
                x+=dr
                y+=dc

        return False

    def get_moves(self, player):
        return [(r,c) for r in range(SIZE) for c in range(SIZE)
                if self.is_valid(r,c,player)]

    def make_move(self, r, c):
        player = self.current_player
        opp = 2 if player == 1 else 1

        self.board[r][c] = player

        dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

        for dr,dc in dirs:
            x,y = r+dr,c+dc
            path=[]

            while 0<=x<SIZE and 0<=y<SIZE:
                if self.board[x][y]==opp:
                    path.append((x,y))
                elif self.board[x][y]==player:
                    for px,py in path:
                        self.board[px][py]=player
                    break
                else:
                    break
                x+=dr
                y+=dc


def run_game(player1, player2):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Othello")

    game = Othello(player1, player2)

    running = True

    while running:
        screen.fill(WHITE)

        moves = game.get_moves(game.current_player)

        for r in range(SIZE):
            for c in range(SIZE):
                pygame.draw.rect(screen, GREEN, (c*CELL,r*CELL,CELL,CELL))
                pygame.draw.rect(screen, BLACK, (c*CELL,r*CELL,CELL,CELL),1)

                if (r,c) in moves:
                    pygame.draw.circle(screen, BLACK,
                        (c*CELL+CELL//2,r*CELL+CELL//2),5)

                if game.board[r][c]==1:
                    pygame.draw.circle(screen, BLACK,
                        (c*CELL+CELL//2,r*CELL+CELL//2),25)
                elif game.board[r][c]==2:
                    pygame.draw.circle(screen, WHITE,
                        (c*CELL+CELL//2,r*CELL+CELL//2),25)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.MOUSEBUTTONDOWN:
                x,y=event.pos
                c=x//CELL
                r=y//CELL

                if (r,c) in game.get_moves(game.current_player):
                    game.make_move(r,c)
                    game.switch_turn()

        pygame.display.update()

    pygame.quit()
