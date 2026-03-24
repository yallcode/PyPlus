-- A simple multiple-choice Trivia Quiz

set questions to [
    {
        "q": "What is the capital of France?",
        "options": ["A) London", "B) Paris", "C) Berlin", "D) Madrid"],
        "answer": "B"
    },
    {
        "q": "Which planet is known as the Red Planet?",
        "options": ["A) Venus", "B) Jupiter", "C) Mars", "D) Saturn"],
        "answer": "C"
    },
    {
        "q": "What is the speed of light?",
        "options": ["A) 300,000 km/s", "B) 150,000 km/s", "C) 1,000,000 km/s", "D) 100 km/h"],
        "answer": "A"
    }
]

set score to 0
set total to count of questions

say "Welcome to the PyPlus Trivia Quiz!"
say "----------------------------------"

for each item at index i in questions:
    say ""
    say "Question {i + 1}: {item at 'q'}"
    
    set opts to item at "options"
    for each opt in opts:
        say "  " + opt
        
    set guess to ask "Your answer (A/B/C/D): "
    
    if guess in uppercase == item at "answer":
        say "Correct! +1 point."
        change score to score + 1
    else:
        say "Wrong! The correct answer was {item at 'answer'}."

say ""
say "======================="
say "       Quiz Over!      "
say "======================="
say "You scored {score} out of {total}."

if score == total:
    say "Perfect score! You're a genius."
else if score > 0:
    say "Good effort! Keep practicing."
else:
    say "Better luck next time."