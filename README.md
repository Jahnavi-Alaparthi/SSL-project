# SSL-lab-project
A Mini Game Hub containing connect4,othello(reversi),tic-tac-toe

proposed features:

1. can register any number of users with strong hashing security
2. 2 Players play 3 games with GUI specific to each game
3. while playing the game user may choose to quit (user quitting depends upon the which player's turn it was) leading to the other player win
4. return to the main menu while not storing any information about the game left midway(i.e winner or loser is not determined and not included in the leaderboard information)
5. you can quit from the playing completely if you press the quit in main menu terminating the game loop
6. can view the leaderboard at any time apart from the time while playing

Initial implementation plan:

1.File named main.sh which is used to authenticate users, for registration and also logging in , stores the usernames and corresponding passwords after hashing them using SHA-256 in 'users.tsv' file.
  This script after authenticating calls the game.py and sends the 2 participating usernames to it.

2.game.py contains the class which contains the common aspects of the 3 games(ex:- player names, player's turn deciding function, overridable check-win method, quitting method, return to main menu(without saving the results) method, restart method).
  This contain a loop that runs as long as the players want to play and terminate cleanly if the players want to stop playing
  This contain the GUI of 'sort by' option to view leaderboard
  This contain the menu GUI to choose the game to play
  After choosing the game to play it sends the usernames to the chosen game.py(ex: connect4.py) present in the 'games' folder (after terminating the GUI of menu)
  After the completion of the game it gives the results of the game and the history.csv is updated accordingly (by the date, winner, loser, game name, etc)
  After updating the history.csv leaderboard.sh is called by specifying the metric to sort the content
  after the results are displayed in the terminal, this show the matplotlib charts (A bar chart of the Top 5 Players by total win count, A pie chart of the Most Played Games by frequency in history.csv, A graph of the top player containing no of games played plotted against date for all three games, etc)
  After this a prompt appears on the screen to let the player choose to quit or continue playing. Depending upon the input, loop stops or keep running

3.leaderboard.sh goes through the history.csv and calculates few metrics (per game, per user: number of wins, number of losses, and Win/Loss ratio, etc) and sorts the results by the given argument from the game.py then displays the result in the terminal.

4.games contain 3 files (games) connect4.py, othello.py, tictactoe.py 
  each one of these files import the class which is in common to these 3 and override the check-win method and contain their own methods to play effectively and efficiently
  This contain the game specific GUI
  After the completion (it uses the check-win method to determine if the game is draw or won by someone) this sends the appropriate results to the game.py after terminating the GUI of the game.
  menu GUI appears again(managed by game.py)
