#!/bin/bash

metric=$1

if [[ "$metric" == "win" ]]; then
    sort_col=3
elif [[ "$metric" == "loss" ]]; then
    sort_col=4
elif [[ "$metric" == "ratio" ]]; then
    sort_col=5
elif [[ "$metric" == "game" ]]; then
    sort_col=1
else
    sort_col=3
fi

# printing the header
printf "%-12s %-12s %-6s %-6s %-6s\n" "Game" "User" "Win" "Loss" "Ratio"
echo "------------------------------------------------------------"

awk -F "," '
{
    winner = $1
    loser  = $2
    game   = $4

    #trim whitespace and carriage return characters
    gsub(/\r/, "", game)
    gsub(/^[ \t]+|[ \t]+$/, "", game)
    gsub(/^[ \t]+|[ \t]+$/, "", winner)
    gsub(/^[ \t]+|[ \t]+$/, "", loser)

    win[game "|" winner]++
    loss[game "|" loser]++

    users[game "|" winner] = 1
    users[game "|" loser] = 1
}

END {
    for (k in users) {

        split(k, a, "|")
        game = a[1]
        user = a[2]

        w = win[game "|" user] + 0
        l = loss[game "|" user] + 0

        if (l == 0)
            ratio = w
        else
            ratio = w / l

        printf "%-12s %-12s %-6d %-6d %-6.2f\n",
               game, user, w, l, ratio
    }
}
' history.csv | sort -k1,1 -k${sort_col} -nr