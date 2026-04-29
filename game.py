import sys
import csv
import os
import subprocess
from datetime import datetime
import pygame
import matplotlib.pyplot as plt

# -----------------------------
# INIT
# -----------------------------
pygame.init()

# -----------------------------
# INPUT USERS
# -----------------------------
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

# -----------------------------
# CLEAN
# -----------------------------
def clean(name):
    return str(name).replace('"', '').strip() if name else "DRAW"

# -----------------------------
# RECORD RESULT
# -----------------------------
def record_result(winner, loser, game):
    winner = clean(winner)
    loser = clean(loser) if loser else "DRAW"

    with open(HISTORY_FILE, "a", newline="") as f:
        csv.writer(f).writerow([winner, loser, datetime.now(), game])

# -----------------------------
# GRAPH FUNCTION
# -----------------------------
def show_graphs():
    import csv
    from collections import Counter
    import matplotlib.pyplot as plt
    import os

    if not os.path.exists(HISTORY_FILE):
        print("No data available")
        return

    winners = []
    games = []

    try:
        with open(HISTORY_FILE, "r") as f:
            reader = csv.reader(f)
            header = next(reader, None)  # skip header

            for row in reader:
                if len(row) < 4:
                    continue  # skip bad rows

                winner = row[0].strip()
                game = row[3].strip()

                # Accept all non-empty winners except DRAW (case-insensitive)
                if winner and winner.lower() != "draw":
                    winners.append(winner)

                if game:
                    games.append(game)

        if not winners and not games:
            print("No valid data found in CSV")
            return

        # -------- TOP 5 PLAYERS --------
        if winners:
            win_counts = Counter(winners)
            top5 = win_counts.most_common(5)

            players = [p for p, _ in top5]
            wins = [w for _, w in top5]

            plt.figure()
            plt.bar(players, wins)
            plt.title("Top 5 Players by Wins")
            plt.xlabel("Players")
            plt.ylabel("Wins")

        # -------- MOST PLAYED GAMES --------
        if games:
            game_counts = Counter(games)

            plt.figure()
            plt.pie(
                game_counts.values(),
                labels=game_counts.keys(),
                autopct="%1.1f%%"
            )
            plt.title("Most Played Games")

        plt.show()

    except Exception as e:
        print("Graph error:", e)
# -----------------------------
# GAME IMPORTS
# -----------------------------
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

    result = subprocess.run(
        ["bash", "leaderboard.sh", "win"],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    print("\n========== GRAPHS ==========")
    show_graphs()

# -----------------------------
# PYGAME UI
# -----------------------------
WIDTH, HEIGHT = 600, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Game Hub")

font = pygame.font.SysFont(None, 36)

WHITE = (255, 255, 255)
BLUE = (100, 150, 255)
BLACK = (0, 0, 0)

# -----------------------------
# BUTTON CLASS
# -----------------------------
class Button:
    def __init__(self, text, x, y, w, h, action):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)
        screen.blit(font.render(self.text, True, BLACK),
                    (self.rect.x + 10, self.rect.y + 10))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# -----------------------------
# MAIN MENU
# -----------------------------
def game_menu_gui():
    running = True

    buttons = [
        Button("TicTacToe", 180, 80, 240, 40, "1"),
        Button("Connect4", 180, 140, 240, 40, "2"),
        Button("Othello", 180, 200, 240, 40, "3"),
        Button("Exit", 180, 260, 240, 40, "4"),
    ]

    while running:
        screen.fill(WHITE)

        screen.blit(font.render(f"{player1} vs {player2}", True, BLACK), (180, 20))

        for b in buttons:
            b.draw()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for b in buttons:

                    if b.clicked(pos):

                        # ---------------- TIC TAC TOE ----------------
                        if b.action == "1":
                            result = run_ttt(player1, player2)

                            if isinstance(result, tuple):
                                winner, action = result
                            else:
                                winner, action = result, "end"

                            loser = player2 if winner == player1 else player1
                            if winner == "Draw":
                                loser = None

                            record_result(winner, loser, "TicTacToe")
                            post_game()

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

                            record_result(winner, loser, "Connect4")
                            post_game()

                        # ---------------- OTHELLO ----------------
                        elif b.action == "3":
                            result = run_oth(player1, player2)

                            if isinstance(result, tuple):
                                winner, action = result
                            else:
                                winner, action = result, "end"

                            loser = player2 if winner == player1 else player1
                            if winner == "Draw":
                                loser = None

                            record_result(winner, loser, "Othello")
                            post_game()

                        # ---------------- EXIT ----------------
                        elif b.action == "4":
                            running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# -----------------------------
# START
# -----------------------------
if __name__ == "__main__":
    game_menu_gui()