import sys
import csv
import os
import subprocess
from datetime import datetime
import pygame
import matplotlib.pyplot as plt
from collections import Counter

pygame.init()

# user input
if len(sys.argv) < 3:
    print("Usage: python game.py player1 player2")
    sys.exit(1)

player1 = sys.argv[1]
player2 = sys.argv[2]

# ---------------- FILE ----------------
HISTORY_FILE = "history.csv"

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["Winner", "Loser", "Date", "Game"])

def clean(name):
    return str(name).strip() if name else "Draw"

def record_result(winner, loser, game):
    winner = clean(winner)
    loser = clean(loser) if loser else "Draw"

    with open(HISTORY_FILE, "a", newline="") as f:
        csv.writer(f).writerow([winner, loser, datetime.now(), game])

# ---------------- GRAPHS ----------------
def show_graphs():
    winners = []
    games = []

    if not os.path.exists(HISTORY_FILE):
        print("No data")
        return

    with open(HISTORY_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader, None)

        for row in reader:
            if len(row) < 4:
                continue

            w = row[0].strip()
            g = row[3].strip()

            if w and w.lower() != "draw":
                winners.append(w)

            if g:
                games.append(g)

    if not winners and not games:
        print("No valid data")
        return

    if winners:
        top = Counter(winners).most_common(5)
        players = [p for p, _ in top]
        wins = [w for _, w in top]

        plt.figure()
        plt.bar(players, wins)
        plt.title("Top 5 Players")

    if games:
        counts = Counter(games)

        plt.figure()
        plt.pie(counts.values(), labels=counts.keys(), autopct="%1.1f%%")
        plt.title("Game Frequency")

    plt.show()

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

# ---------------- LEADERBOARD ----------------
def show_leaderboard(sort_by):
    try:
        result = subprocess.run(
            ["bash", "leaderboard.sh", sort_by],
            capture_output=True,
            text=True
        )
        print(result.stdout)
    except Exception as e:
        print("Error:", e)

# ---------------- DISPLAY ----------------
WIDTH, HEIGHT = 600, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Game Hub")

# load background properly
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

# overlay
overlay = pygame.Surface((WIDTH, HEIGHT))
overlay.set_alpha(120)
overlay.fill((0, 0, 0))

font = pygame.font.SysFont(None, 36)
WHITE = (255, 255, 255)

# 🔥 RESET DISPLAY FUNCTION
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
    options = ["win", "loss", "ratio", "game"]

    while True:
        screen.blit(background, (bg_x, bg_y))
        screen.blit(overlay, (0, 0))

        title = font.render("Sort Leaderboard", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 40)))

        buttons = []
        for i, opt in enumerate(options):
            b = Button(opt.upper(), 180, 100 + i * 60, 240, 40, opt)
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
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 60)))

        buttons = [
            Button("Play Again", 180, 120, 240, 40, "again"),
            Button("Main Menu", 180, 180, 240, 40, "menu"),
            Button("Graphs", 180, 240, 240, 40, "graphs"),
            Button("Leaderboard", 180, 300, 240, 40, "leaderboard"),
            Button("Exit", 180, 360, 240, 40, "exit"),
        ]

        for b in buttons:
            b.draw()

        pygame.display.flip()

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

        winner = result[0] if isinstance(result, tuple) else result

        loser = player2 if winner == player1 else player1
        if winner == "Draw":
            loser = None

        record_result(winner, loser, game_name)

        # 🔥 CLEAN RESET
        reset_main_display()

        action = post_game_screen(winner, game_name)

        if action == "again":
            continue
        elif action == "menu":
            break
        elif action == "exit":
            pygame.quit()
            sys.exit()

# ---------------- MAIN MENU ----------------
def game_menu_gui():
    running = True

    buttons = [
        Button("TicTacToe", 180, 100, 240, 40, "ttt"),
        Button("Connect4", 180, 160, 240, 40, "c4"),
        Button("Othello", 180, 220, 240, 40, "oth"),
        Button("Exit", 180, 280, 240, 40, "exit"),
    ]

    while running:
        screen.blit(background, (bg_x, bg_y))
        screen.blit(overlay, (0, 0))

        title = font.render(f"{player1} vs {player2}", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 40)))

        for b in buttons:
            b.draw()

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