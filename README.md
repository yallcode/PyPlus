# py+ Programming Language — Complete Tutorial

> **py+** is a beginner-friendly language that reads like plain English.  
> One file. No installs. Runs anywhere Python 3.10+ runs.

---

## Table of Contents

1. [Installation & Setup](#1-installation--setup)
2. [Your First Program](#2-your-first-program)
3. [Variables](#3-variables)
4. [Data Types](#4-data-types)
5. [Math & Operators](#5-math--operators)
6. [Text (Strings)](#6-text-strings)
7. [Getting Input from the User](#7-getting-input-from-the-user)
8. [Conditionals](#8-conditionals--if--else)
9. [Loops](#9-loops)
10. [Functions](#10-functions)
11. [Classes & Objects](#11-classes--objects)
12. [Lists](#12-lists)
13. [Maps (Dictionaries)](#13-maps-dictionaries)
14. [Error Handling](#14-error-handling)
15. [Modules & Imports](#15-modules--imports)
16. [Comments](#16-comments)
17. [Complete Programs](#17-complete-programs)
18. [Common Mistakes](#18-common-mistakes)
19. [Quick Reference Card](#19-quick-reference-card)

---

## 1. Installation & Setup

**Requirements:** Python 3.10 or newer — nothing else.

1. Download `pyplus.py` — that single file **is** the entire language.
2. Create a text file ending in `.pyp` — that is your py+ program.
3. Run it.

```
your-project/
├── pyplus.py          ← the interpreter (never edit this)
├── hello.pyp          ← your programs go here
├── game.pyp
└── my_project.pyp
```

### Running py+ programs

```bash
# Run a program
python pyplus.py hello.pyp

# Start an interactive session (REPL)
python pyplus.py

# Run a one-liner directly
python pyplus.py -c "say 'Hello, World!'"

# Show help
python pyplus.py --help

# Show version
python pyplus.py --version
```

### The interactive REPL

Type `python pyplus.py` with no arguments and you enter live mode.

```
py+> set name to "Alice"
py+> say "Hello, {name}!"
Hello, Alice!
py+> set x to 10
py+> say x * x
→ 100
py+> quit
```

For multi-line blocks, end with `:` then press Enter on a blank line to run:

```
py+> if 5 > 3:
...>     say "yes"
...>
yes
```

---

## 2. Your First Program

Create `hello.pyp`:

```
say "Hello, World!"
```

Run it:

```bash
python pyplus.py hello.pyp
```

Make it interactive:

```
set name to ask "What is your name? "
say "Hello, {name}! Welcome to py+!"
```

---

## 3. Variables

### Creating — `set`

```
set x to 5
set name to "Alice"
set price to 9.99
set active to true
set result to nothing
```

### Updating — `change`

```
set lives to 3
change lives to lives - 1
say lives        -- 2
```

> Use `set` the first time. Use `change` every time after that.

### Optional type annotation

```
set score as Integer to 0
set username as Text to "guest"
set temperature as Decimal to 36.6
set logged_in as Boolean to false
```

### Constants — `define`

```
define PI as 3.14159
define MAX_PLAYERS as 4

say PI           -- 3.14159
say MAX_PLAYERS  -- 4
```

---

## 4. Data Types

| Type | Description | Examples |
|---|---|---|
| `Integer` | Whole numbers | `0`, `42`, `-7` |
| `Decimal` | Numbers with decimals | `3.14`, `-0.5`, `2.0` |
| `Text` | Characters / strings | `"hello"`, `""` |
| `Boolean` | True or false | `true`, `false` |
| `List` | Ordered collection | `[1, 2, 3]` |
| `Map` | Key-value pairs | `{"name": "Alice"}` |
| `Nothing` | No value (null) | `nothing` |

### Checking a type

```
set num to 42

if num is an Integer:
    say "It's an Integer"

if num is a Decimal:
    say "It's a Decimal"
```

---

## 5. Math & Operators

### Arithmetic — symbols or English, both work

```
set a to 10
set b to 3

say a + b            -- 13     (also: a plus b)
say a - b            -- 7      (also: a minus b)
say a * b            -- 30     (also: a times b)
say a / b            -- 3.333  (also: a divided by b)
say a % b            -- 1      (also: a mod b)
say a ** 2           -- 100    (also: a to the power of 2)
```

### Comparisons — symbols or English

```
say x == y                              -- equal
say x != y                              -- not equal
say x > y                               -- greater than
say x < y                               -- less than
say x >= y                              -- greater or equal
say x <= y                              -- less or equal

say x is equal to y                     -- same as ==
say x is not equal to y                 -- same as !=
say x is greater than y                 -- same as >
say x is less than y                    -- same as <
say x is greater than or equal to y     -- same as >=
say x is less than or equal to y        -- same as <=
```

### Logic

```
if age >= 18 and has_ticket:
    say "Enter"

if score < 50 or absent:
    say "Fail"

if not logged_in:
    say "Please log in"
```

### Parentheses control order

```
say 2 + 3 * 4       -- 14  (multiplication first)
say (2 + 3) * 4     -- 20  (parentheses first)
```

---

## 6. Text (Strings)

### Creating strings

```
set greeting to "Hello, World!"
set empty to ""
set quote to "She said \"hello\""
```

### Multi-line strings

```
set poem to """
Roses are red,
Violets are blue,
py+ is fun,
And so are you.
"""
```

### String interpolation `{}`

```
set name to "Alice"
set age to 30

say "My name is {name}."
say "I am {age} years old."
say "Next year I will be {age + 1}."
```

### Joining with `+`

```
say "Hello, " + name + "!"
say "Score: " + 100          -- numbers auto-convert to text
```

### String operations

```
set msg to "  Hello, World!  "

say msg trimmed                              -- "Hello, World!"
say msg in uppercase                         -- "  HELLO, WORLD!  "
say msg in lowercase                         -- "  hello, world!  "

say "hello" contains "ell"                   -- true
say "hello" starts with "hel"                -- true
say "hello" ends with "llo"                  -- true

say "one,two,three" split by ","             -- [one, two, three]
say "Hello" replaced "Hello" with "Goodbye"  -- Goodbye
```

---

## 7. Getting Input from the User

```
-- Text input
set name to ask "What is your name? "
say "Hello, {name}!"

-- Number input
set age to ask number "How old are you? "
say "In 10 years you will be {age + 10}."
```

Full example:

```
set name to ask "Enter your name: "
set age to ask number "Enter your age: "

if age < 18:
    say "You are a minor, {name}."
else if age < 65:
    say "You are an adult, {name}."
else:
    say "You are a senior, {name}."
```

---

## 8. Conditionals — if / else

### Simple if

```
if temperature > 30:
    say "It's hot!"
```

### if / else

```
if hour < 12:
    say "Good morning!"
else:
    say "Good afternoon!"
```

### if / else if / else

```
if score >= 90:
    say "Grade: A"
else if score >= 80:
    say "Grade: B"
else if score >= 70:
    say "Grade: C"
else if score >= 60:
    say "Grade: D"
else:
    say "Grade: F"
```

### Nested if

```
if age >= 18:
    if has_id:
        say "Welcome in!"
    else:
        say "You need ID."
else:
    say "Must be 18 or older."
```

> **Always indent with exactly 4 spaces. Tabs are not allowed.**

---

## 9. Loops

### `repeat` — run N times

```
repeat 5 times:
    say "Hello!"
```

### `repeat` with a counter (starts at 0)

```
repeat 5 times with i:
    say "Step " + i
-- Output: Step 0, Step 1, Step 2, Step 3, Step 4
```

### `while` — repeat while condition is true

```
set count to 1
while count <= 5:
    say count
    change count to count + 1
```

### `for each` — iterate a list

```
set fruits to ["apple", "banana", "cherry"]
for each fruit in fruits:
    say fruit
```

### `for each` with index

```
for each fruit at index i in fruits:
    say i + ": " + fruit
```

### `for each` over a range

```
for each n from 1 to 10:
    say n

-- with step
for each n from 0 to 100 step 10:
    say n

-- counting down
for each n from 10 to 1 step -1:
    say n
```

### Loop controls

```
while true:
    set x to ask number "Number (0 to quit): "
    if x == 0:
        stop loop        -- exit immediately
    if x < 0:
        skip to next     -- jump to next iteration
    say "You entered: " + x
```

### Nested loops

```
for each row from 1 to 3:
    for each col from 1 to 3:
        say row + "," + col
```

---

## 10. Functions

### Define and call

```
define say_hello:
    say "Hello, World!"

say_hello()
```

### With parameters

```
define greet with name:
    say "Hello, " + name + "!"

greet("Alice")
greet with "Bob"          -- 'with' syntax also works
```

### Multiple parameters (use commas)

```
define add with a, b:
    give back a + b

define introduce with first, last, age:
    say "I am {first} {last}, age {age}."

set result to add(3, 4)       -- 7
introduce("Alice", "Smith", 30)
```

### Returning values — `give back`

```
define square with n:
    give back n * n

define max_of with a, b:
    if a > b:
        give back a
    give back b

say square(5)           -- 25
say max_of(10, 7)       -- 10
```

### Recursion

```
define factorial with n:
    if n == 0:
        give back 1
    give back n * factorial(n - 1)

say factorial(5)        -- 120
say factorial(10)       -- 3628800
```

```
define fibonacci with n:
    if n <= 1:
        give back n
    give back fibonacci(n - 1) + fibonacci(n - 2)

for each i from 0 to 10:
    say fibonacci(i)
```

---

## 11. Classes & Objects

### Define a class

```
class Dog:
    has name
    has breed
    has age

    setup with name, breed, age:
        my name is name
        my breed is breed
        my age is age

    define bark:
        say my name + " says: Woof!"

    define describe:
        say "I am {my name}, a {my breed}, age {my age}."
```

- `has` — declares a field
- `setup` — the constructor (runs on `new`)
- `my` — refers to the current object
- `define` inside a class — a method

### Create objects

```
set rex to new Dog with "Rex", "German Shepherd", 4
set fluffy to new Dog with "Fluffy", "Poodle", 2

rex.bark()            -- Rex says: Woof!
fluffy.describe()     -- I am Fluffy, a Poodle, age 2.
say rex.name          -- Rex
```

### Methods that return values

```
class Rectangle:
    has width
    has height

    setup with width, height:
        my width is width
        my height is height

    define area:
        give back my width * my height

    define perimeter:
        give back 2 * (my width + my height)

    define is_square:
        give back my width is equal to my height

set r to new Rectangle with 4, 6
say r.area()          -- 24
say r.perimeter()     -- 20
say r.is_square()     -- false
```

### Inheritance — `extends`

```
class Animal:
    has name
    has sound

    setup with name, sound:
        my name is name
        my sound is sound

    define speak:
        say my name + " says " + my sound + "!"


class Cat extends Animal:
    has indoor

    setup with name, indoor:
        parent setup with name, "Meow"
        my indoor is indoor

    define describe:
        if my indoor:
            say my name + " is an indoor cat."
        else:
            say my name + " is an outdoor cat."


class Dog extends Animal:
    has tricks

    setup with name:
        parent setup with name, "Woof"
        my tricks is []

    define learn with trick:
        add trick to my tricks
        say my name + " learned: " + trick

    define perform:
        say my name + " can do: " + my tricks


set cat to new Cat with "Whiskers", true
set dog to new Dog with "Rex"

cat.speak()           -- Whiskers says Meow!
cat.describe()        -- Whiskers is an indoor cat.

dog.speak()           -- Rex says Woof!
dog.learn("sit")
dog.learn("shake")
dog.perform()         -- Rex can do: [sit, shake]
```

### Type checking

```
if dog is a Dog:
    say "It's a Dog"          -- true

if dog is an Animal:
    say "It's also an Animal"  -- true (via inheritance)
```

---

## 12. Lists

```
set numbers to [1, 2, 3, 4, 5]
set names to ["Alice", "Bob", "Carol"]
set empty to []
```

### Access — `at` (index starts at 0)

```
set fruits to ["apple", "banana", "cherry"]

say fruits at 0     -- apple
say fruits at 2     -- cherry
```

### Modify

```
change fruits at 1 to "blueberry"   -- update item
add "date" to fruits                -- append
remove "apple" from fruits          -- remove first occurrence
```

### Count

```
say count of fruits     -- 3
```

### Loop

```
set scores to [88, 72, 95, 61, 83]
set total to 0

for each score in scores:
    change total to total + score

say "Average: " + total / count of scores
```

### Build a list

```
set squares to []
for each n from 1 to 10:
    add n * n to squares

say squares     -- [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

---

## 13. Maps (Dictionaries)

```
set person to {"name": "Alice", "age": 30, "city": "Paris"}
```

### Access

```
say person at "name"     -- Alice
say person at "age"      -- 30
```

### Update / add keys

```
change person at "age" to 31
change person at "job" to "Engineer"
```

### Check key existence

```
if person contains "city":
    say "City: " + person at "city"
```

### Loop over a map

```
for each key in person:
    say key + ": " + person at key
```

### Maps as records

```
define make_student with name, grade, score:
    give back {"name": name, "grade": grade, "score": score}

set students to [
    make_student("Alice", "A", 95),
    make_student("Bob",   "B", 82),
    make_student("Carol", "C", 71)
]

for each s in students:
    say s at "name" + " — " + s at "grade" + " (" + s at "score" + ")"
```

---

## 14. Error Handling

### try / catch

```
try:
    set result to 10 / 0
catch DivisionError as err:
    say "Math error: " + err.message
```

### Catch any error

```
try:
    -- risky code
catch as err:
    say "Error: " + err.message
    say "Type: " + err.type
```

### Multiple catch blocks

```
try:
    set x to ask number "Enter a number: "
    set result to 100 / x
    say "Result: " + result
catch DivisionError as err:
    say "You can't divide by zero!"
catch ValueError as err:
    say "That's not a valid number."
catch as err:
    say "Unexpected error: " + err.message
```

### finally — always runs

```
try:
    say "Trying..."
catch as err:
    say "Error: " + err.message
finally:
    say "Always runs, with or without error."
```

### Raise your own errors

```
define check_age with age:
    if age < 0:
        raise ValueError with "Age cannot be negative: " + age
    if age > 150:
        raise ValueError with "Age seems unrealistic: " + age
    give back age

try:
    set a to check_age(-5)
catch ValueError as err:
    say err.message
```

### Built-in error types

| Error | When |
|---|---|
| `DivisionError` | Dividing by zero |
| `ValueError` | Wrong value |
| `TypeError` | Wrong type |
| `NameError` | Variable not defined |
| `IndexError` | List index out of range |
| `KeyError` | Map key not found |
| `ArgumentError` | Wrong number of arguments |
| `ImportError` | Module not found |
| `AttributeError` | No such field or method |

---

## 15. Modules & Imports

### Import a whole module

```
use math

say math.pi               -- 3.14159265...
say math.sqrt(16)         -- 4
say math.floor(3.9)       -- 3
say math.ceil(3.1)        -- 4
say math.abs(-42)         -- 42
say math.round(3.567)     -- 4
say math.max(3, 7, 2)     -- 7
say math.min(3, 7, 2)     -- 2
say math.pow(2, 10)       -- 1024
say math.sin(0)           -- 0
say math.cos(0)           -- 1
say math.log(100, 10)     -- 2
```

### Import specific items

```
use sqrt, pi, floor from math

say sqrt(25)     -- 5
say pi           -- 3.14159...
say floor(7.9)   -- 7
```

### Random numbers

```
use random

set coin to random.randint(0, 1)
set dice to random.randint(1, 6)
set picked to random.choice(["apple", "banana", "cherry"])

say "Coin: " + coin
say "Dice: " + dice
say "Picked: " + picked
```

### Time

```
use time

say time.format()     -- "2025-01-15 14:32:00"
time.sleep(1)         -- pause 1 second
say "Done."
```

### Import from another .pyp file

`utils.pyp`:
```
define clamp with value, low, high:
    if value < low:
        give back low
    if value > high:
        give back high
    give back value

define is_even with n:
    give back n mod 2 is equal to 0
```

`main.pyp`:
```
use clamp, is_even from utils

say clamp(150, 0, 100)   -- 100
say clamp(-5, 0, 100)    -- 0
say is_even(4)           -- true
say is_even(7)           -- false
```

### Built-in modules

| Module | What it provides |
|---|---|
| `math` | `pi`, `e`, `sqrt`, `floor`, `ceil`, `abs`, `round`, `max`, `min`, `pow`, `log`, `sin`, `cos`, `tan` |
| `random` | `random()`, `randint(min, max)`, `choice(list)`, `shuffle(list)` |
| `time` | `now()`, `sleep(seconds)`, `format(pattern)` |

---

## 16. Comments

```
-- This is a single-line comment.

set x to 5   -- inline comment

---
This is a multi-line comment.
It can span many lines.
---
```

---

## 17. Complete Programs

### FizzBuzz

```
for each n from 1 to 100:
    if n mod 15 is equal to 0:
        say "FizzBuzz"
    else if n mod 3 is equal to 0:
        say "Fizz"
    else if n mod 5 is equal to 0:
        say "Buzz"
    else:
        say n
```

---

### Number Guessing Game

```
use random

set secret to random.randint(1, 100)
set attempts to 0
set max_attempts to 7
set won to false

say "=== Number Guessing Game ==="
say "I'm thinking of a number between 1 and 100."
say "You have {max_attempts} guesses."
say ""

repeat max_attempts times:
    change attempts to attempts + 1
    set remaining to max_attempts - attempts
    set guess to ask number "Guess #{attempts}: "

    if guess is equal to secret:
        say "Correct! You won in {attempts} guess(es)!"
        change won to true
        stop loop
    else if guess is less than secret:
        say "Too low!"
    else:
        say "Too high!"

    if remaining > 0:
        say "{remaining} guess(es) left."

if not won:
    say ""
    say "Game over! The answer was {secret}."
```

---

### Calculator

```
define calculate with a, op, b:
    if op == "+":  give back a + b
    else if op == "-":  give back a - b
    else if op == "*":  give back a * b
    else if op == "/":
        if b == 0:
            raise DivisionError with "Cannot divide by zero"
        give back a / b
    else:
        raise ValueError with "Unknown operator: " + op

say "=== Calculator ==="

while true:
    set a to ask number "First number (0 to quit): "
    if a == 0:
        stop loop
    set op to ask "Operator (+, -, *, /): "
    set b to ask number "Second number: "

    try:
        set result to calculate(a, op, b)
        say "{a} {op} {b} = {result}"
    catch DivisionError as err:
        say "Error: " + err.message
    catch ValueError as err:
        say "Error: " + err.message
    say ""

say "Goodbye!"
```

---

### Student Grade Tracker

```
class Student:
    has name
    has grades

    setup with name:
        my name is name
        my grades is []

    define add_grade with subject, score:
        add {"subject": subject, "score": score} to my grades

    define average:
        if count of my grades == 0:
            give back 0
        set total to 0
        for each g in my grades:
            change total to total + g at "score"
        give back total / count of my grades

    define letter_grade:
        set avg to my average()
        if avg >= 90: give back "A"
        else if avg >= 80: give back "B"
        else if avg >= 70: give back "C"
        else if avg >= 60: give back "D"
        else: give back "F"

    define report:
        say "=== " + my name + " ==="
        for each g in my grades:
            say "  " + g at "subject" + ": " + g at "score"
        say "  Average: " + my average()
        say "  Grade:   " + my letter_grade()
        say ""


set alice to new Student with "Alice"
alice.add_grade("Math", 95)
alice.add_grade("English", 88)
alice.add_grade("Science", 92)
alice.report()

set bob to new Student with "Bob"
bob.add_grade("Math", 72)
bob.add_grade("English", 65)
bob.add_grade("Science", 78)
bob.report()
```

---

### Bank Account

```
class BankAccount:
    has owner
    has balance

    setup with owner, initial_balance:
        if initial_balance < 0:
            raise ValueError with "Opening balance cannot be negative"
        my owner is owner
        my balance is initial_balance

    define deposit with amount:
        if amount <= 0:
            raise ValueError with "Deposit must be positive"
        change my balance to my balance + amount
        say "{my owner} deposited {amount}. Balance: {my balance}"

    define withdraw with amount:
        if amount <= 0:
            raise ValueError with "Withdrawal must be positive"
        if amount > my balance:
            raise ValueError with "Insufficient funds (balance: {my balance})"
        change my balance to my balance - amount
        say "{my owner} withdrew {amount}. Balance: {my balance}"

    define transfer with amount, target:
        my withdraw(amount)
        target.deposit(amount)

    define show_balance:
        say "{my owner}'s balance: ${my balance}"


set alice to new BankAccount with "Alice", 1000
set bob to new BankAccount with "Bob", 500

alice.deposit(250)
bob.deposit(100)
alice.transfer(200, bob)

try:
    alice.withdraw(5000)
catch ValueError as err:
    say "Transfer failed: " + err.message

say ""
alice.show_balance()
bob.show_balance()
```

---

### Mini To-Do List

```
class TodoList:
    has title
    has items

    setup with title:
        my title is title
        my items is []

    define add with task:
        add {"task": task, "done": false} to my items
        say "Added: " + task

    define complete with index:
        if index < 0 or index >= count of my items:
            raise IndexError with "No item at index " + index
        set item to my items at index
        change item at "done" to true
        say "Done: " + item at "task"

    define show:
        say "=== " + my title + " ==="
        if count of my items is equal to 0:
            say "  (empty)"
        else:
            for each item at index i in my items:
                if item at "done":
                    say "  [x] " + i + ". " + item at "task"
                else:
                    say "  [ ] " + i + ". " + item at "task"
        say ""


set todo to new TodoList with "My Tasks"
todo.add("Buy groceries")
todo.add("Write py+ programs")
todo.add("Go for a walk")
todo.add("Read a book")
todo.show()

todo.complete(0)
todo.complete(2)
todo.show()
```

---

## 18. Common Mistakes

### Tabs instead of 4 spaces

```
-- Wrong (tab)
if x > 0:
	say "yes"

-- Right (4 spaces)
if x > 0:
    say "yes"
```

### `change` before `set`

```
-- Wrong
change score to score + 1    -- error: not defined

-- Right
set score to 0
change score to score + 1
```

### Forgetting the colon

```
-- Wrong
if x > 5
    say "big"

-- Right
if x > 5:
    say "big"
```

### Using `=` to compare instead of `==`

```
-- Wrong
if x = 5:
    say "five"

-- Right
if x == 5:
    say "five"

if x is equal to 5:
    say "five"
```

### Forgetting `my` inside a class

```
class Counter:
    has count

    setup:
        my count is 0

    define increment:
        -- Wrong
        change count to count + 1

        -- Right
        change my count to my count + 1
```

### Calling a no-argument function without `()`

```
define get_pi:
    give back 3.14159

say get_pi       -- prints: <function get_pi>
say get_pi()     -- prints: 3.14159
```

### Off-by-one in `for each from`

```
-- This prints 1, 2, 3, 4, 5  (BOTH ends are inclusive)
for each n from 1 to 5:
    say n

-- This prints 0, 1, 2, 3, 4
for each n from 0 to 4:
    say n
```

---

## 19. Quick Reference Card

```
─────────────────────────────────────────────────────────
 VARIABLES
─────────────────────────────────────────────────────────
  set x to 5                 change x to x + 1
  define PI as 3.14159       set name as Text to "Alice"

 OUTPUT / INPUT
─────────────────────────────────────────────────────────
  say "Hello, {name}!"
  set name to ask "Name? "
  set age  to ask number "Age? "

 MATH
─────────────────────────────────────────────────────────
  x + y   x - y   x * y   x / y   x % y   x ** 2
  x plus y   x minus y   x times y   x divided by y
  x mod y   x to the power of 2

 COMPARISONS
─────────────────────────────────────────────────────────
  x == y   x != y   x > y   x < y   x >= y   x <= y
  x is equal to y            x is not equal to y
  x is greater than y        x is less than y
  x is greater than or equal to y
  x is less than or equal to y

 LOGIC
─────────────────────────────────────────────────────────
  a and b      a or b      not a

 CONDITIONALS
─────────────────────────────────────────────────────────
  if x > 5:
      ...
  else if x > 0:
      ...
  else:
      ...

 LOOPS
─────────────────────────────────────────────────────────
  repeat 10 times:
  repeat 10 times with i:
  while x < 100:
  for each item in my_list:
  for each item at index i in my_list:
  for each n from 1 to 10:
  for each n from 0 to 100 step 5:
  stop loop              skip to next

 FUNCTIONS
─────────────────────────────────────────────────────────
  define add with a, b:       add(3, 4)
      give back a + b         add with 3, 4

 CLASSES
─────────────────────────────────────────────────────────
  class Dog extends Animal:   set d to new Dog with "Rex"
      has name                d.speak()
      setup with name:        d.name
          my name is name
      define speak:
          say my name + " barks"

 LISTS
─────────────────────────────────────────────────────────
  set lst to [1, 2, 3]
  lst at 0                    change lst at 0 to 99
  add item to lst             remove item from lst
  count of lst
  for each x in lst:

 MAPS
─────────────────────────────────────────────────────────
  set m to {"a": 1, "b": 2}
  m at "a"                    change m at "a" to 99
  m contains "key"
  for each key in m:

 STRINGS
─────────────────────────────────────────────────────────
  msg trimmed          msg in uppercase     msg in lowercase
  msg contains "x"     msg starts with "x"  msg ends with "x"
  msg split by ","     msg replaced "a" with "b"

 ERRORS
─────────────────────────────────────────────────────────
  try:
      ...
  catch ValueError as e:
      say e.message
  finally:
      ...
  raise TypeError with "bad input"

 IMPORTS
─────────────────────────────────────────────────────────
  use math                use sqrt, pi from math
  math.sqrt(16)           sqrt(16)

 TYPE CHECKS
─────────────────────────────────────────────────────────
  if x is an Integer:     if x is a Text:
  if obj is a ClassName:

 COMMENTS
─────────────────────────────────────────────────────────
  -- single line          --- multi line ---
─────────────────────────────────────────────────────────
```

---

*py+ v1.0 — Programming that reads like English.*
