import sys
import csv
import os
import subprocess
from datetime import datetime
import pygame
import matplotlib.pyplot as plt

pygame.init()
bg_image = pygame.image.load("bg.png")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# user input
if len(sys.argv) < 3:
    print("Error: Missing usernames")
    sys.exit(1)

player1 = sys.argv[1]
player2 = sys.argv[2]

if player1 == player2:
    print("Error: Same users not allowed")
    sys.exit(1)

# -----------------------------
# HISTORY FILE
# -----------------------------
HISTORY_FILE = "history.csv"

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["Winner", "Loser", "Date", "Game"])

def clean(name):
    return str(name).replace('"', '').strip() if name else "DRAW"



def record_result(winner, loser, game):
    winner = clean(winner)
    loser = clean(loser) if loser else "DRAW"

    with open(HISTORY_FILE, "a", newline="") as f:
        csv.writer(f).writerow([winner, loser, datetime.now(), game])


# ---------------- GRAPHS ----------------

def show_graphs():
    try:
        import csv
        from collections import Counter

        winners = []
        games = []

        with open(HISTORY_FILE, "r") as f:
            reader = csv.reader(f)
            next(reader, None)

            for row in reader:
                if len(row) < 4:
                    continue

                winner = row[0]
                game = row[3]

                if winner and winner != "DRAW":
                    winners.append(winner)

                games.append(game)

        if not winners and not games:
            print("No data available")
            return

        win_counts = Counter(winners)

        if win_counts:
            plt.figure()
            plt.bar(win_counts.keys(), win_counts.values())
            plt.title("Wins per Player")


        plt.figure()
        plt.bar(players, wins)
        plt.title("Top 5 Players")


        if game_counts:
            plt.figure()
            plt.pie(game_counts.values(), labels=game_counts.keys(), autopct="%1.1f%%")
            plt.title("Games Distribution")

        plt.tight_layout()
        plt.show()

        input("Close graph window and press Enter to continue...")


# ---------------- GAMES ----------------

def run_ttt(p1, p2):
    from games.tictactoe import run_game
    return run_game(p1, p2)

def run_c4(p1, p2):
    from games.connect4 import run_game
    return run_game(p1, p2)

def run_oth(p1, p2):
    from games.othello import run_game
    return run_game(p1, p2)

# -----------------------------
# POST GAME FLOW
# -----------------------------
def post_game():
    print("\n========== LEADERBOARD ==========")

# ---------------- DISPLAY ----------------
WIDTH, HEIGHT = 900, 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Game Hub")

def load_background():
    bg_original = pygame.image.load("background.jpg")
    img_w, img_h = bg_original.get_size()

    scale = min(WIDTH / img_w, HEIGHT / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)

    bg = pygame.transform.smoothscale(bg_original, (new_w, new_h))
    x = (WIDTH - new_w) // 2
    y = (HEIGHT - new_h) // 2

    return bg, x, y

background, bg_x, bg_y = load_background()

overlay = pygame.Surface((WIDTH, HEIGHT))
overlay.set_alpha(120)
overlay.fill((0, 0, 0))

font = pygame.font.SysFont(None, 42)
WHITE = (255, 255, 255)


# ---------------- RESET ----------------
def reset_main_display():
    global screen, background, bg_x, bg_y, overlay

    pygame.display.quit()
    pygame.display.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mini Game Hub")

    background, bg_x, bg_y = load_background()

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(120)
    overlay.fill((0, 0, 0))

# ---------------- BUTTON ----------------
class Button:
    def __init__(self, text, x, y, w, h, action):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action

    def draw(self):

        pygame.draw.rect(screen, (0, 0, 0), self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


# ---------------- LEADERBOARD GUI ----------------
def leaderboard_sort_gui():
    options = ["No of wins", "No of losses", "Win/Loss ratio", "Game Name"]

    while True:
        screen.blit(background, (bg_x, bg_y))
        screen.blit(overlay, (0, 0))

        title = font.render("Sort Leaderboard", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 80)))

        buttons = []
        for i, opt in enumerate(options):
            b = Button(opt.upper(), 300, 150 + i * 80, 300, 50, opt)
            b.draw()
            buttons.append(b)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for b in buttons:
                    if b.clicked(pos):
                        show_leaderboard(b.action)
                        return

# ---------------- POST GAME ----------------
def post_game_screen(winner, game_name):
    while True:
        screen.blit(background, (bg_x, bg_y))
        screen.blit(overlay, (0, 0))

        title = font.render(f"{winner} WON!", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        buttons = [
            Button("Play Again", 300, 180, 300, 50, "again"),
            Button("Main Menu", 300, 250, 300, 50, "menu"),
            Button("Graphs", 300, 320, 300, 50, "graphs"),
            Button("Leaderboard", 300, 390, 300, 50, "leaderboard"),
            Button("Exit", 300, 460, 300, 50, "exit"),
        ]


        for b in buttons:
            b.draw()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return "exit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for b in buttons:

                    if b.clicked(pos):

                        if b.action == "graphs":
                            show_graphs()
                        elif b.action == "leaderboard":
                            leaderboard_sort_gui()
                        else:
                            return b.action

# ---------------- GAME FLOW ----------------
def handle_game(run_func, game_name):
    while True:
        result = run_func(player1, player2)


                        # ---------------- CONNECT 4 ----------------
                        elif b.action == "2":
                            result = run_c4(player1, player2)

                            if isinstance(result, tuple):
                                winner, action = result
                            else:
                                winner, action = result, "end"

                            loser = player2 if winner == player1 else player1
                            if winner == "Draw":
                                loser = None


        reset_main_display()

        action = post_game_screen(winner, game_name)


                        # ---------------- OTHELLO ----------------
                        elif b.action == "3":
                            result = run_oth(player1, player2)


# ---------------- MAIN MENU ----------------
def game_menu_gui():
    running = True

    buttons = [
        Button("TicTacToe", 300, 200, 300, 50, "ttt"),
        Button("Connect4", 300, 270, 300, 50, "c4"),
        Button("Othello", 300, 340, 300, 50, "oth"),
        Button("Exit", 300, 410, 300, 50, "exit"),
    ]

    while running:
        screen.blit(background, (bg_x, bg_y))
        screen.blit(overlay, (0, 0))

        title = font.render(f"{player1} vs {player2}", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))


                        # ---------------- EXIT ----------------
                        elif b.action == "4":
                            running = False

        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for b in buttons:
                    if b.clicked(pos):
                        if b.action == "ttt":
                            handle_game(run_ttt, "TicTacToe")
                        elif b.action == "c4":
                            handle_game(run_c4, "Connect4")
                        elif b.action == "oth":
                            handle_game(run_oth, "Othello")
                        elif b.action == "exit":
                            running = False

    pygame.quit()
    sys.exit()

# ---------------- START ----------------

if __name__ == "__main__":
    game_menu_gui()
