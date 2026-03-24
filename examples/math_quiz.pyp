-- math_quiz.pyp
use random
use time

say "=== Math Master ==="
say "Answer 5 questions correctly to win!"
say ""

set score to 0
set rounds to 5

for each i from 1 to rounds:
    set a to random.randint(1, 10)
    set b to random.randint(1, 10)
    set op_num to random.randint(1, 3)
    set op to "+"
    set answer to a + b

    -- If op_num is 2, make it subtraction
    if op_num == 2:
        set op to "-"
        -- Swap so 'a' is always bigger to keep answers positive
        if a < b:
            set temp to a
            set a to b
            set b to temp
        set answer to a - b
    
    -- If op_num is 3, make it multiplication
    else if op_num == 3:
        set op to "*"
        set answer to a * b

    set guess to ask number "Q{i}: What is {a} {op} {b}? "
    
    if guess == answer:
        say "Correct! +1 point."
        change score to score + 1
    else:
        say "Wrong! The correct answer was {answer}."
    
    time.sleep(1)
    say ""

say "=== Game Over ==="
say "Your final score is {score} out of {rounds}."

if score == rounds:
    say "Perfect score! You are a Math Master!"