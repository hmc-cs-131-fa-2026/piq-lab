# Lab: Two Ways to Draw: Plotter Python and piq

In this course we build a compiler for **piq**, a small drawing language for a pen plotter. The compiler translates
a piq program into a **Python** program made of just five low-level plotter commands.

Today you'll use **both** languages and compare them:

- **Part 1, the target language:** run and change Python programs written with the five commands.
- **Part 2, the source language:** run and change piq programs, look at the Python the compiler makes from them, and
  extend a drawing using piq's loops and procedures.

Both parts draw the **same stick person**, so you can see how much work each language takes.

You don't need a plotter. Every drawing is saved as a **preview picture (PNG)**. About 50 minutes in all.

**Submitting (Gradescope):** you'll paste your answers and upload pictures and code. Keep notes in `answers.md` as you
go; its headings match the Gradescope questions. [What to submit](#what-to-submit) lists everything.

---

## Setup (2 minutes)
On the course server, clone the lab into your home folder and work there:

```
git clone https://github.com/hmc-cs-131-fa-2026/piq-lab.git ~/piq-lab
cd ~/piq-lab
```

**Run every command from this `piq-lab` folder.** The tools you'll use are already installed on the server:

| Command | What it does |
|---|---|
| `py2png part1/shapes.py` | Runs a plotter **Python** program on a pretend plotter and saves the drawing as `part1/shapes.png` |
| `piq2png part2/shapes.piq` | Compiles a **piq** program to Python (`part2/shapes.py`), then draws it (`part2/shapes.png`) |
| `piq2py part2/shapes.piq` | Only compiles: writes `part2/shapes.py` so you can read it |

To look at a PNG, open it in your editor (VS Code shows images), or copy it to your own computer.

### Reading a preview
- **Blue** lines are drawn with the pen **down**: that's the drawing.
- **Pink** lines are pen-**up** travel. The plotter moves along them without drawing. The two long pink lines to the
  top-left corner are the trip from the plotter's home corner to the centre of the paper at the start, and back home
  at the end.
- The **grey dashed box** is the **safe area**: the pen must stay at least 1 inch from the edges of the 17 × 11 inch
  paper. Anything that goes outside it is drawn in **red**, with a WARNING. The real plotter refuses to draw such a
  drawing at all.
- **Units are millimetres.** **x points right, y points up.** Drawing starts at the **centre** of the paper. The safe
  area is **190.5 mm left/right and 114.3 mm up/down** of the centre.

---

## Part 1: the target language (about 20 minutes)

### The five commands
| Command | Meaning |
|---|---|
| `start()` | Start a drawing. The pen is **up**, at the **centre of the paper**. |
| `pen_up()` | Lift the pen. Moves after this do **not** draw. |
| `pen_down()` | Lower the pen. Moves after this **do** draw. |
| `move_rel(dx, dy)` | Move `dx` mm right and `dy` mm up **from where the pen is now**. Negative numbers go left or down. |
| `finish()` | Check that the whole drawing stays in the safe area, draw it, then lift the pen and go home. |

A **dot** is `pen_down()` followed straight away by `pen_up()`.

Every program has the same outline. The commands between `start()` and `finish()` are only **recorded**;
`finish()` checks the whole drawing and then draws it. The `try` / `finally` makes sure `finish()` runs even if the
drawing code crashes (then the real plotter draws nothing, and a preview shows what was recorded):

```python
import sys
sys.path.insert(0, "/opt/piq/python")     # where the plotter commands live on the server
from plotter_runtime import start, finish, pen_up, pen_down, move_rel

start()
try:
    ...drawing commands...
finally:
    finish()
```

**Moves are relative.** `move_rel(10, 0)` means "10 mm to the right of wherever the pen is now", not "go to x = 10".
So every line's effect depends on all the lines before it. The programs below use one rule to stay sane: each shape
**starts and ends at its anchor point**, with the pen up.

**Before each change below, write your prediction in `answers.md`. Then run it and check.** A wrong prediction that
you then explain is worth as much as a right one.

### 1.1 Run it
Open `part1/shapes.py` and read it. Then run:
```
py2png part1/shapes.py
```
and open `part1/shapes.png`. You should see, left to right: a square, a triangle, an X, a plus sign, the letters "HI",
and a dot.

- **(a)** How many `pen_down()` calls are in the file? How many separate shapes do you see? Why are the two numbers
  different?
- **(b)** Why does the X need a `pen_up()` in the middle, but the square doesn't?

### 1.2 One number, everywhere
In `part1/shapes.py`, change **only** the square's last stroke, `move_rel(0.0, -30.0)`, to `move_rel(0.0, -40.0)`.

- **Predict first:** what happens to the square? What happens to **every shape after it**?
- Run `py2png part1/shapes.py` again and check. In one or two sentences, explain why one number changed the whole rest
  of the drawing.
- **Save this picture for Gradescope:** `cp part1/shapes.png part1/shapes_1_2.png`. Then change the line back to
  `-30.0`.

### 1.3 Bug hunt: the missing `pen_up()`
In the X block, delete the `pen_up()` on the line right after the **first diagonal**.

- **Predict first:** what extra line will appear, and exactly where?
- Run it and check. Then put the `pen_up()` back.

A missing `pen_up()` is the most common plotter bug. On paper, that line can't be erased!

### 1.4 Dress up the stick person
Run `py2png part1/stick_person.py` and look at the picture. Read the code: each body part starts and ends at the
**neck** (the middle of the bottom of the head).

Work in a copy, so the original stays unchanged for Part 2:
```
cp part1/stick_person.py part1/dressed.py
```
In `part1/dressed.py`, add these at the end of the drawing (just above `finally:`), using only the five commands:

1. **A hat:** a **brim**, a 40 mm horizontal line lying on top of the head, centred, plus a **crown**, a 20 mm wide,
   15 mm tall box standing on the middle of the brim.
2. **A face:** two **eyes** (dots) 20 mm above the neck and 7 mm to either side, and a **mouth**, a 12 mm
   horizontal line 8 mm above the neck, centred.

Here the top of the head is 30 mm above the neck, and the head is 30 mm wide.

Tips: sketch it first, and label each move with its `(dx, dy)`. Do the hat, run `py2png part1/dressed.py`, then do
the face, and run it again.
End each part back at the neck with the pen up. Comments (`# …`) help.

- **Record:** how many lines of code did you add? (Don't count blank lines or comments.)
- **Save for Gradescope:** `part1/dressed.py` and `part1/dressed.png`.

---

## Part 2: piq (about 25 minutes)

### piq in one table
| piq | Meaning |
|---|---|
| `square 30` | A 30 × 30 square **centred on the pen**. The pen ends where it started. |
| `rectangle 40 20` | A 40 wide, 20 tall rectangle, centred on the pen |
| `circle 15` | A circle of **radius** 15, centred on the pen |
| `dot` | A dot where the pen is |
| `line right 20` | Draw a line 20 mm to the right. The pen **ends at the far end.** Directions: `left`, `right`, `up`, `down`. |
| `move up 10` | Travel 10 mm up **without** drawing |
| `x = 20` | Set a variable. Expressions use `+ - * /` and parentheses, e.g. `square x * 2 + 5`. |
| `for i from 1 to 4 { … }` | Repeat the block with `i` = 1, 2, 3, 4 |
| `define box(s) { … }` | Define a procedure with a parameter `s` (definitions go **first** in the file) |
| `box(20)` | Call it |

Also worth knowing:

- The pen is up between statements, and all shapes return to where they started.
- Lines and moves can only go left, right, up or down. **piq has no diagonal lines.**
- Spacing and newlines don't matter, and piq has **no comments**.
- If a program has a mistake, `piq2png` prints an error with a line and column number, like
  `error: part2/shapes.piq:3:3 -- …`. The problem is at that spot or just before it. No picture is made.

### 2.1 Run it, and look at what the compiler made
Read `part2/shapes.piq`, then run:
```
piq2png part2/shapes.piq
```
and open `part2/shapes.png`. Then open the Python file the compiler wrote, `part2/shapes.py`. It uses the same five
commands you used in Part 1.

- **(a)** Which lines of `shapes.piq` drew the right-most shape? What happened to the `for` loop in the Python: is
  there a loop in `shapes.py`?
- **(b)** `wc -l part2/shapes.piq part2/shapes.py` counts the lines of each file. How many lines are there in each?
  Find the Python for `circle 15`. Roughly how many `move_rel` calls is one circle?

### 2.2 Predict, then change
Make each change, **predicting first**, and run `piq2png part2/shapes.piq` after each.

- **(a)** Change the loop to `for i from 1 to 8 {` and its body to `square i * 5`. What will the right-most shape look
  like now? Is it bigger, smaller, or the same size overall?
- **(b)** In the `flower` procedure, change the last line, `move up 3 * r`, to `move up 2 * r`. Which shapes will
  move, and in which direction? Which question from Part 1 is this like? Afterwards, change it back.

### 2.3 The same stick person, in piq
Run `piq2png part2/stick_person.piq`. It draws **exactly the same** stick person as `part1/stick_person.py` (the
original, without your hat and face). Compare the three versions:
```
wc -l part1/stick_person.py part2/stick_person.piq part2/stick_person.py
```
(The hand-written Python has lots of comments, so also compare only the lines that do something.)

- **(a)** Roughly how many lines does each version need to draw the person? The compiled `part2/stick_person.py` and
  the hand-written `part1/stick_person.py` draw the same picture. Count the plotter commands in each:
  ```
  grep -cE 'pen_up|pen_down|move_rel' part1/stick_person.py part2/stick_person.py
  ```
  Which one uses more commands? Look inside the compiled file: where do the extra commands come from?

Now **extend the piq drawing**. Save your work as `part2/scene.piq`:
```
cp part2/stick_person.piq part2/scene.piq
```
and run `piq2png part2/scene.piq` often.

1. **Hat and face:** add the same hat and face as in 1.4 (same sizes and positions). Count the lines you added, and
   compare with your count from 1.4.
2. **A crowd:** turn the person into a procedure, `define person() { … }`, and use a `for` loop to draw **three
   people side by side**, 90 mm apart and centred on the paper.
   - Hint: a procedure is only easy to reuse if it **ends where it started**. `stick_person.piq` starts by moving up
     to the neck and ends at the neck. What must you add or remove so that `person()` ends where it began?
3. **Your own addition:** add something else to the scene: a sun, the ground, trees, a house, a dog … It must include:
   - at least one **procedure with a parameter** that you call **at least twice** with different arguments (for
     example `tree(30)` and `tree(50)`);
   - at least one `circle` and one `rectangle`;
   - at least one arithmetic expression (such as `h / 2 + 12`).

   Keep everything inside the safe area (no red in the preview).

- **Save for Gradescope:** `part2/scene.piq` and `part2/scene.png`.

---

## Reflection (5 minutes)
Answer in 2–4 sentences each.

1. For the hat and face, how many lines did Python (1.4) and piq (2.3 step 1) each take? Why was the difference small
   there, but huge for the crowd and for circles? Use numbers from `wc -l`, or from `grep -c move_rel`, to support
   your answer.
2. Name two things the piq compiler does for you that you had to do by hand in Part 1.
3. What's one feature you would add to piq, and why? (For example: diagonal lines, comments, a "go back to the start"
   command, colours, …)

---

## What to submit
Upload to Gradescope:

| Question | Submit |
|---|---|
| 1.1–1.3 | Your answers, and `part1/shapes_1_2.png` |
| 1.4 | Your line count, `part1/dressed.py`, and `part1/dressed.png` |
| 2.1–2.2 | Your answers |
| 2.3 | Your answers and line count, `part2/scene.piq`, and `part2/scene.png` |
| Reflection | Your answers |

---

## Optional: on the real plotter
Your instructor may plot some of the best scenes on the real NextDraw plotter. The Python the compiler writes is
exactly what drives it, so a drawing that looks right in the preview is what ends up on paper, pink travel and all.
