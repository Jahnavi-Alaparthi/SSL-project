gamename=(Tictactoe Othello Connectfour)

metric=$1

# Determining which column to sort
if [[ "$metric" == "win" ]]; then
    col=3
elif [[ "$metric" == "loss" ]]; then
    col=4
elif [[ "$metric" == "ratio" ]]; then
    col=5
else
    col=3  
    # Default sorting win column
fi

printf "%-12s %-12s %-5s %-5s %-6s\n" "Game" "User" "Win" "Loss" "Ratio"
echo "---------------------------------------------------------"
for game in "${gamename[@]}"; do
    while IFS=$'\t' read username pwd; do
        awk -F "," -v username="$username" -v game="$game" '
        BEGIN {
            loss=0; win=0
        }
       
        $3 == game {
            if ($1 == username) win++
            if ($2 == username) loss++
        }
        END {
            ratio = (loss == 0 ? win : win/loss)
           printf "%-12s %-12s %-5d %-5d %-6.2f\n", game, username, win, loss, ratio
        }' history.csv
    done < users.tsv
done | sort -k${col} -nr
