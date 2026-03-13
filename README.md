# py+ Programming Language

> A beginner-friendly language that reads like plain English.  
> Built on Python — runs anywhere Python runs.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Running py+ Code](#running-py-code)
3. [Variables](#variables)
4. [Math & Operators](#math--operators)
5. [Text (Strings)](#text-strings)
6. [Conditionals](#conditionals)
7. [Loops](#loops)
8. [Functions](#functions)
9. [Classes & Objects](#classes--objects)
10. [Lists](#lists)
11. [Maps (Dictionaries)](#maps-dictionaries)
12. [Error Handling](#error-handling)
13. [Importing Modules](#importing-modules)
14. [Input & Output](#input--output)
15. [Comments](#comments)
16. [Full Example Programs](#full-example-programs)

---

## Getting Started

**Requirements:** Python 3.10 or newer (no other installs needed).

Save `pyplus.py` anywhere on your computer. That single file *is* the language.

```
your-project/
├── pyplus.py        ← the interpreter
├── hello.pyp        ← your py+ programs go here
└── game.pyp
```

py+ programs are plain text files with the `.pyp` extension.

---

## Running py+ Code

### Run a file
```bash
python pyplus.py my_program.pyp
```

### Interactive REPL (type and run code live)
```bash
python pyplus.py
```
```
py+> set name to "Alice"
py+> say "Hello, {name}!"
Hello, Alice!
```

### Run a quick one-liner
```bash
python pyplus.py -c "say 'Hello, World!'"
```

---

## Variables

Use `set` to create a variable and `change` to update it.

```
set name to "Alice"
set age to 25
set height to 5.8
set active to true
set nothing_here to nothing
```

You can optionally declare the type with `as`:

```
set score as Integer to 100
set message as Text to "Hello"
```

To update a variable that already exists:

```
set lives to 3
change lives to lives - 1
```

> ⚠️ Using `set` twice on the same name just overwrites it.  
> Using `change` on a name that was never `set` is an error.

### Types

| Type | What it holds | Example |
|---|---|---|
| `Integer` | Whole numbers | `42`, `-7`, `0` |
| `Decimal` | Numbers with decimals | `3.14`, `-0.5` |
| `Text` | A string of characters | `"Hello"`, `""` |
| `Boolean` | True or false | `true`, `false` |
| `List` | Ordered collection | `[1, 2, 3]` |
| `Map` | Key-value pairs | `{"a": 1}` |
| `Nothing` | No value / null | `nothing` |

---

## Math & Operators

py+ supports both **English words** and **symbols** — use whichever feels natural.

### Arithmetic

| English | Symbol | Meaning |
|---|---|---|
| `x plus y` | `x + y` | Addition |
| `x minus y` | `x - y` | Subtraction |
| `x times y` | `x * y` | Multiplication |
| `x divided by y` | `x / y` | Division |
| `x mod y` | `x % y` | Remainder |
| `x to the power of y` | `x ** y` | Exponentiation |

```
set a to 10
set b to 3

say a + b          -- 13
say a minus b      -- 7
say a times b      -- 30
say a divided by b -- 3.333...
say a mod b        -- 1
say a ** 2         -- 100
```

### Comparison

| English | Symbol | Meaning |
|---|---|---|
| `x is equal to y` | `x == y` | Equal |
| `x is not equal to y` | `x != y` | Not equal |
| `x is greater than y` | `x > y` | Greater than |
| `x is less than y` | `x < y` | Less than |
| `x is greater than or equal to y` | `x >= y` | Greater or equal |
| `x is less than or equal to y` | `x <= y` | Less or equal |

### Logic

```
if x > 0 and y > 0:
    say "both positive"

if x == 0 or y == 0:
    say "at least one is zero"

if not active:
    say "not active"
```

---

## Text (Strings)

### String interpolation

Embed variables directly inside strings using `{curly braces}`:

```
set name to "Alice"
set age to 30
say "My name is {name} and I am {age} years old."
```
Output: `My name is Alice and I am 30 years old.`

### Joining strings

```
set greeting to "Hello, " + name + "!"
```

### String operations

```
set msg to "  Hello, World!  "

say msg trimmed          -- "Hello, World!"
say msg in uppercase     -- "  HELLO, WORLD!  "
say msg in lowercase     -- "  hello, world!  "

say "hello" contains "ell"       -- true
say "hello" starts with "hel"    -- true
say "hello" ends with "llo"      -- true

say "a,b,c" split by ","         -- [a, b, c]
say "Hello" replaced "Hello" with "Goodbye"  -- Goodbye
```

---

## Conditionals

### Basic if

```
if score is greater than 90:
    say "Excellent!"
```

### if / else

```
if temperature > 30:
    say "It's hot outside."
else:
    say "It's comfortable."
```

### if / else if / else

```
if score >= 90:
    say "Grade: A"
else if score >= 80:
    say "Grade: B"
else if score >= 70:
    say "Grade: C"
else:
    say "Grade: F"
```

> **Indentation matters.** Always indent the body of an `if` block with **4 spaces**.

---

## Loops

### Repeat N times

```
repeat 5 times:
    say "Hello!"
```

### Repeat with a counter variable

```
repeat 5 times with i:
    say "Step " + i
```
Output: `Step 0`, `Step 1`, `Step 2`, `Step 3`, `Step 4`

### While loop

```
set count to 1
while count <= 10:
    say count
    change count to count + 1
```

### For each (iterate a list)

```
set fruits to ["apple", "banana", "cherry"]
for each fruit in fruits:
    say fruit
```

### For each with index

```
for each fruit at index i in fruits:
    say i + ": " + fruit
```

### For range

```
for each n from 1 to 10:
    say n
```

With a step size:

```
for each n from 0 to 100 step 10:
    say n
```

### Loop controls

```
while true:
    set x to ask number "Enter a number (0 to quit): "
    if x == 0:
        stop loop        -- exits the loop immediately
    if x < 0:
        skip to next     -- skips back to the top of the loop
    say "You entered: " + x
```

---

## Functions

### Defining a function

```
define greet:
    say "Hello, World!"
```

### Function with parameters

```
define greet with name:
    say "Hello, " + name + "!"
```

### Function with multiple parameters

```
define add with a, b:
    give back a + b
```

### Calling a function

```
greet()
greet("Alice")
greet with "Bob"

set result to add(3, 4)
set result to add with 3, 4
say result      -- 7
```

### Returning a value

```
define square with n:
    give back n * n

set area to square(5)
say area     -- 25
```

### Recursion

```
define factorial with n:
    if n == 0:
        give back 1
    give back n * factorial(n - 1)

say factorial(5)   -- 120
```

---

## Classes & Objects

### Defining a class

```
class Animal:
    has name
    has sound

    setup with name, sound:
        my name is name
        my sound is sound

    define speak:
        say my name + " says " + my sound
```

- `has` declares a field
- `setup` is the constructor (runs when you create a new object)
- `my` refers to the current object (like `self` in Python or `this` in Java)

### Creating an object

```
set cat to new Animal with "Cat", "Meow"
set dog to new Animal with "Dog", "Woof"

cat.speak()    -- Cat says Meow
dog.speak()    -- Dog says Woof
```

### Inheritance

```
class Dog extends Animal:
    has tricks

    setup with name:
        parent setup with name, "Woof"
        my tricks is []

    define learn with trick:
        add trick to my tricks
        say my name + " learned: " + trick

    define show_tricks:
        say my name + " knows: " + my tricks
```

```
set rex to new Dog with "Rex"
rex.speak()              -- Rex says Woof
rex.learn("sit")
rex.learn("shake")
rex.show_tricks()        -- Rex knows: [sit, shake]
```

### Type checking

```
if rex is a Dog:
    say "rex is a Dog"

if rex is an Animal:
    say "rex is an Animal"    -- true via inheritance
```

---

## Lists

```
set scores to [10, 20, 30, 40, 50]
```

### Access by index (starts at 0)

```
say scores at 0     -- 10
say scores at 4     -- 50
```

### Add and remove items

```
add 60 to scores
remove 10 from scores
```

### Count items

```
say count of scores
```

### Loop through a list

```
for each score in scores:
    say score
```

### Update an item

```
change scores at 2 to 99
```

---

## Maps (Dictionaries)

Maps store key-value pairs.

```
set person to {"name": "Alice", "age": 30, "city": "Paris"}
```

### Access a value

```
say person at "name"    -- Alice
```

### Update a value

```
change person at "age" to 31
```

### Check if a key exists

```
if person contains "city":
    say "city is set"
```

### Loop through a map

```
for each key in person:
    say key + ": " + person at key
```

---

## Error Handling

### Try / catch

```
try:
    set result to 10 / 0
catch DivisionError as err:
    say "Math error: " + err.message
```

### Catch any error

```
try:
    -- risky code here
catch as err:
    say "Something went wrong: " + err.message
```

### Finally (always runs)

```
try:
    say "trying..."
catch as err:
    say "error!"
finally:
    say "this always runs"
```

### Raise your own errors

```
define safe_sqrt with n:
    if n < 0:
        raise ValueError with "Cannot take square root of a negative number"
    use math
    give back math.sqrt(n)

try:
    set r to safe_sqrt(-4)
catch ValueError as err:
    say err.message
```

---

## Importing Modules

### Import a whole module

```
use math

say math.pi           -- 3.141592653589793
say math.sqrt(16)     -- 4
say math.floor(3.7)   -- 3
say math.ceil(3.2)    -- 4
say math.abs(-5)      -- 5
```

### Import specific items

```
use sqrt, pi from math

say sqrt(25)    -- 5
say pi          -- 3.14159...
```

### Built-in modules

| Module | What it provides |
|---|---|
| `math` | `pi`, `e`, `sqrt`, `floor`, `ceil`, `abs`, `round`, `sin`, `cos`, `log` |
| `random` | `random`, `randint`, `choice`, `shuffle` |
| `time` | `now`, `sleep`, `format` |

```
use random

set dice to random.randint(1, 6)
say "You rolled: " + dice
```

```
use time

time.sleep(1)       -- pause for 1 second
say time.format()   -- prints current date/time
```

### Import from another py+ file

```
-- mytools.pyp
define double with n:
    give back n * 2
```

```
-- main.pyp
use double from mytools

say double(5)    -- 10
```

---

## Input & Output

### Output

```
say "Hello!"
say 42
say true
say my_list
```

### Input (text)

```
set name to ask "What is your name? "
say "Hello, {name}!"
```

### Input (number)

```
set age to ask number "How old are you? "
say "In 10 years you will be " + (age + 10)
```

---

## Comments

```
-- This is a single-line comment

---
This is a
multi-line comment.
It can span many lines.
---
```

---

## Full Example Programs

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

### Number Guessing Game

```
use random

set secret to random.randint(1, 100)
set attempts to 0

say "Guess a number between 1 and 100!"

while true:
    set guess to ask number "Your guess: "
    change attempts to attempts + 1

    if guess is equal to secret:
        say "Correct! You got it in {attempts} attempt(s)!"
        stop loop
    else if guess is less than secret:
        say "Too low! Try higher."
    else:
        say "Too high! Try lower."
```

### Calculator

```
define calculate with a, op, b:
    if op == "+": give back a + b
    else if op == "-": give back a - b
    else if op == "*": give back a * b
    else if op == "/":
        if b == 0:
            raise ValueError with "Cannot divide by zero"
        give back a / b
    else:
        raise ValueError with "Unknown operator: " + op

set a to ask number "First number: "
set op to ask "Operator (+, -, *, /): "
set b to ask number "Second number: "

try:
    set result to calculate(a, op, b)
    say "{a} {op} {b} = {result}"
catch ValueError as err:
    say "Error: " + err.message
```

### Student Grade Tracker

```
class Student:
    has name
    has grades

    setup with name:
        my name is name
        my grades is []

    define add_grade with grade:
        add grade to my grades

    define average:
        if count of my grades is equal to 0:
            give back 0
        set total to 0
        for each g in my grades:
            change total to total + g
        give back total / count of my grades

    define report:
        set avg to my average()
        say "--- {my name} ---"
        say "Grades: " + my grades
        say "Average: " + avg
        if avg >= 90:
            say "Result: A"
        else if avg >= 80:
            say "Result: B"
        else if avg >= 70:
            say "Result: C"
        else:
            say "Result: F"

set alice to new Student with "Alice"
alice.add_grade(92)
alice.add_grade(88)
alice.add_grade(95)
alice.report()

set bob to new Student with "Bob"
bob.add_grade(72)
bob.add_grade(65)
bob.add_grade(78)
bob.report()
```

---

## Quick Reference Card

```
-- Variables
set x to 5                    change x to 10

-- Output / Input
say "Hello, {x}!"             set name to ask "Name? "
                              set n to ask number "Age? "

-- Math
x + y   x - y   x * y   x / y   x % y   x ** 2
x plus y   x minus y   x times y   x divided by y   x mod y

-- Comparisons
x == y   x != y   x > y   x < y   x >= y   x <= y
x is equal to y   x is greater than y   x is less than or equal to y

-- Logic
and   or   not

-- If
if x > 5:           else if x > 0:         else:

-- Loops
repeat 10 times:             repeat 10 times with i:
while x < 100:               stop loop      skip to next
for each item in my_list:    for each n from 1 to 10:
for each n from 0 to 50 step 5:

-- Functions
define greet with name:      greet("Alice")   greet with "Alice"
    give back "Hi " + name   set r to add(3, 4)

-- Classes
class Dog extends Animal:    set d to new Dog with "Rex"
    has name                 d.speak()
    setup with name:         d.name
        my name is name

-- Lists
set lst to [1, 2, 3]         lst at 0           count of lst
add 4 to lst                 remove 2 from lst   change lst at 0 to 99

-- Maps
set m to {"a": 1}            m at "a"           change m at "a" to 2

-- Errors
try:                         raise ValueError with "msg"
catch ValueError as e:
    say e.message

-- Imports
use math                     use sqrt from math
math.sqrt(16)                sqrt(16)

-- Comments
-- single line               --- multi line ---
```

---

## Common Mistakes

**Tabs instead of spaces**
```
-- ❌ Wrong (using tab)
if x > 0:
	say "yes"

-- ✅ Right (4 spaces)
if x > 0:
    say "yes"
```

**Changing a variable that was never set**
```
-- ❌ Wrong
change score to score + 1    -- error if 'score' not defined yet

-- ✅ Right
set score to 0
change score to score + 1
```

**Forgetting the colon**
```
-- ❌ Wrong
if x > 5
    say "big"

-- ✅ Right
if x > 5:
    say "big"
```

**Using `and` with function arguments**
```
-- ❌ Ambiguous (old style)
set r to add with 3 and 4   -- 'and' may be parsed as logical AND

-- ✅ Use commas for arguments
set r to add(3, 4)
set r to add with 3, 4
```

---

*py+ — programming that reads like English.*
