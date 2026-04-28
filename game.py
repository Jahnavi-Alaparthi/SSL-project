import sys
import pygame
import numpy as np
import csv
import subprocess
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt

# game launcher

def launch_game(choice, p1, p2):
    if choice == 1:
        from games.tictactoe import TicTacToe
        game = TicTacToe(p1, p2)

    elif choice == 2:
        from games.othello import Othello
        game = Othello(p1, p2)

    elif choice == 3:
        from games.connect4 import Connect4
        game = Connect4(p1, p2)

    else:
        return None

    winner = game.run()
    return winner, game.__class__.__name__



def show_analytics():
    try:
        with open("history.csv", "r") as f:
            reader = list(csv.reader(f))
    except FileNotFoundError:
        print("No data yet.")
        return

    if not reader:
        print("No games played yet.")
        return

    winners = [row[0] for row in reader]
    games = [row[3] for row in reader]

    # Bar Chart: Top 5 Players
    win_counts = Counter(winners)
    top5 = dict(win_counts.most_common(5))

    plt.figure()
    plt.bar(top5.keys(), top5.values())
    plt.title("Top 5 Players by Wins")
    plt.xlabel("Players")
    plt.ylabel("Wins")
    plt.show()

    # Pie Chart: Game frequency

    game_counts = Counter(games)

    plt.figure()
    plt.pie(game_counts.values(), labels=game_counts.keys(), autopct="%1.1f%%")
    plt.title("Most Played Games")
    plt.show()

