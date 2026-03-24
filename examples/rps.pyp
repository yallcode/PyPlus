-- rps.pyp
use random

set player_score to 0
set cpu_score to 0

say "=== Rock, Paper, Scissors ==="
say "First to 3 wins! Type 'quit' to exit."
say ""

while player_score < 3 and cpu_score < 3:
    set player to ask "Rock, Paper, or Scissors? "
    change player to player in lowercase

    if player == "quit":
        say "Thanks for playing!"
        stop loop
    
    -- Check if the input is valid
    else if player == "rock" or player == "paper" or player == "scissors":
        set cpu to random.choice(["rock", "paper", "scissors"])
        say "Computer chose: " + cpu

        if player == cpu:
            say "It's a tie!"
        else if player == "rock" and cpu == "scissors":
            say "Rock smashes scissors! You win this round!"
            change player_score to player_score + 1
        else if player == "paper" and cpu == "rock":
            say "Paper covers rock! You win this round!"
            change player_score to player_score + 1
        else if player == "scissors" and cpu == "paper":
            say "Scissors cut paper! You win this round!"
            change player_score to player_score + 1
        else:
            say "Computer wins this round!"
            change cpu_score to cpu_score + 1
            
        say "Score -> You: {player_score} | CPU: {cpu_score}"
        say "----------------------------------------"
    else:
        say "Invalid choice. Please type rock, paper, scissors, or quit."
        say ""

-- Final win/loss messages
if player_score == 3:
    say "🎉 Congratulations! You won the game!"
else if cpu_score == 3:
    say "💀 Game over! The computer won."