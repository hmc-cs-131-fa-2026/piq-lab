# shapes.py -- Lab Part 1: simple shapes drawn with the five low-level plotter
# commands. This is the kind of code the piq compiler generates.
#
# Make a preview picture (from the piq-lab folder):
#     py2png part1/shapes.py            writes part1/shapes.png
#
# Units are millimetres, x points RIGHT and y points UP. Every move_rel is
# relative to where the pen is now. The pen starts at the centre of the page.
#
# Each shape below has an ANCHOR: its bottom-left corner. Every shape starts
# at its anchor and ends back at its anchor, with the pen up. That way the
# "travel" move from one shape to the next is always just the distance
# between their anchors.

import sys
sys.path.insert(0, "/opt/piq/python")     # the plotter runtime, on the course server
from plotter_runtime import start, finish, pen_up, pen_down, move_rel

start()
try:
    # travel from the page centre to the square's anchor
    pen_up()
    move_rel(-130.0, -15.0)

    # --- 1. SQUARE, 30 x 30 (starts & ends at bottom-left corner) ---
    pen_down()
    move_rel(30.0, 0.0)      # bottom edge, going right
    move_rel(0.0, 30.0)      # right edge, going up
    move_rel(-30.0, 0.0)     # top edge, going left
    move_rel(0.0, -30.0)     # left edge, going down
    pen_up()

    # travel to next shape
    move_rel(50.0, 0.0)

    # --- 2. TRIANGLE, base 30, height 26 (starts & ends at bottom-left corner) ---
    pen_down()
    move_rel(30.0, 0.0)      # base, going right
    move_rel(-15.0, 26.0)    # right side, up to the apex
    move_rel(-15.0, -26.0)   # left side, back down to the anchor
    pen_up()

    # travel to next shape
    move_rel(50.0, 0.0)

    # --- 3. X, 30 x 30 (starts & ends at bottom-left corner) ---
    pen_down()
    move_rel(30.0, 30.0)     # first diagonal: bottom-left to top-right
    pen_up()
    move_rel(-30.0, 0.0)     # hop over to the top-left corner
    pen_down()
    move_rel(30.0, -30.0)    # second diagonal: top-left to bottom-right
    pen_up()
    move_rel(-30.0, 0.0)     # back to the anchor

    # travel to next shape
    move_rel(50.0, 0.0)

    # --- 4. PLUS SIGN, 30 x 30 (starts & ends at bottom-left of its box) ---
    move_rel(15.0, 0.0)      # to the bottom of the vertical bar
    pen_down()
    move_rel(0.0, 30.0)      # vertical bar
    pen_up()
    move_rel(-15.0, -15.0)   # to the left end of the horizontal bar
    pen_down()
    move_rel(30.0, 0.0)      # horizontal bar
    pen_up()
    move_rel(-30.0, -15.0)   # back to the anchor

    # travel to next shape
    move_rel(50.0, 0.0)

    # --- 5a. LETTER H, 20 wide x 30 tall (starts & ends at bottom-left) ---
    pen_down()
    move_rel(0.0, 30.0)      # left post, going up
    pen_up()
    move_rel(0.0, -15.0)     # down to the middle
    pen_down()
    move_rel(20.0, 0.0)      # crossbar
    pen_up()
    move_rel(0.0, 15.0)      # up to the top of the right post
    pen_down()
    move_rel(0.0, -30.0)     # right post, going down
    pen_up()
    move_rel(-20.0, 0.0)     # back to the anchor

    # travel to next letter
    move_rel(30.0, 0.0)

    # --- 5b. LETTER I, 16 wide x 30 tall (starts & ends at bottom-left) ---
    pen_down()
    move_rel(16.0, 0.0)      # bottom serif
    pen_up()
    move_rel(-8.0, 0.0)      # back to the middle
    pen_down()
    move_rel(0.0, 30.0)      # the stem
    pen_up()
    move_rel(-8.0, 0.0)      # to the left end of the top serif
    pen_down()
    move_rel(16.0, 0.0)      # top serif
    pen_up()
    move_rel(-16.0, -30.0)   # back to the anchor

    # travel to the dot
    move_rel(25.0, 0.0)

    # --- 6. DOT: pen down then straight back up, with no move in between ---
    pen_down()
    pen_up()

finally:
    finish()
