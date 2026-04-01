touch users.tsv

for i in 1 2; do
    while true; do
        echo "Enter username:"
        read -r username

        echo "Enter password:"
        read -r password

        hashed_pwd=$(echo -n "$password" | sha256sum | awk '{print $1}')

        found=0
        validpwd=0

        while IFS=$'\t' read -r user stored_hash; do
            if [[ "$username" == "$user" ]]; then
                found=1

                if [[ "$hashed_pwd" == "$stored_hash" ]]; then
                    validpwd=1
                    break
                fi
            fi
        done < users.tsv

        if (( found == 1 && validpwd == 1 )); then
            echo "Login successful!"

            if [[ $i -eq 1 ]]; then
                user1="$username"
            else
                user2="$username"
            fi

            break

        elif (( found == 1 && validpwd == 0 )); then
            echo "Password does not match. Try again."

        else
            echo "User not registered! Register? (yes/no)"
            read -r answer

            if [[ "$answer" == "yes" || "$answer" == "Yes" ]]; then
                echo -e "$username\t$hashed_pwd" >> users.tsv
                echo "User registered!"

                if [[ $i -eq 1 ]]; then
                    user1="$username"
                else
                    user2="$username"
                fi

                break
            fi
        fi
    done
done

# Ensure distinct users
if [[ "$user1" == "$user2" ]]; then
    echo "Both users cannot be the same."
    exit 1
fi

python3 game.py "$user1" "$user2"
