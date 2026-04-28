class BoardGame:
    def __init__(self, player1, player2, rows, cols):
        self.player1 = player1
        self.player2 = player2

        self.rows = rows
        self.cols = cols

        self.current_player = 1  # 1 means Player1 and 2 means Player2

    def switch_turn(self):
        "Switch between Player 1 and Player 2"
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    def get_current_player_name(self):
        "Return current player's name"
        if self.current_player == 1:
            return self.player1
        else:
            return self.player2

    def reset_game(self):
        "Optional: Reset game state (useful later)"
        self.current_player = 1
