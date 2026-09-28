# stick_person.py -- Lab Part 1: a stick person, written by hand with the five
# low-level plotter commands. Part 2 draws exactly the same person in piq.
#
# Make a preview picture (from the piq-lab folder):
#     py2png part1/stick_person.py      writes part1/stick_person.png
#
# The ANCHOR is the NECK: the middle of the bottom edge of the head. Every body
# part starts at the neck and ends back at the neck with the pen up, so each
# part can be changed without breaking the others.
#
#                 +------+
#                 | head |  30 x 30
#                 +--+---+
#     ---------------+---------------   arms: 60 wide, 10 below the neck
#                    |
#                    |      body: 50 down from the neck
#                 +--+--+   hips: 20 wide
#                 |     |
#                 |     |   legs: 40 down
#
# Units are millimetres, x points RIGHT and y points UP.

import sys
sys.path.insert(0, "/opt/piq/python")     # the plotter runtime, on the course server
from plotter_runtime import start, finish, pen_up, pen_down, move_rel

start()
try:
    # travel from the centre up to the neck (the anchor)
    pen_up()
    move_rel(0.0, 40.0)

    # === HEAD: a 30 x 30 box sitting on the neck ===
    move_rel(-15.0, 0.0)     # to the bottom-left corner of the head
    pen_down()
    move_rel(30.0, 0.0)      # bottom edge
    move_rel(0.0, 30.0)      # right edge
    move_rel(-30.0, 0.0)     # top edge
    move_rel(0.0, -30.0)     # left edge
    pen_up()
    move_rel(15.0, 0.0)      # back to the neck

    # === BODY: 50 straight down ===
    pen_down()
    move_rel(0.0, -50.0)
    pen_up()
    move_rel(0.0, 50.0)      # back to the neck

    # === ARMS: one line, 60 wide, 10 below the neck ===
    move_rel(-30.0, -10.0)   # to the left hand
    pen_down()
    move_rel(60.0, 0.0)      # across to the right hand
    pen_up()
    move_rel(-30.0, 10.0)    # back to the neck

    # === LEGS: a 20 wide hip line, and two legs 40 long ===
    move_rel(-10.0, -50.0)   # to the left end of the hips
    pen_down()
    move_rel(20.0, 0.0)      # hips
    move_rel(0.0, -40.0)     # right leg
    pen_up()
    move_rel(-20.0, 40.0)    # to the top of the left leg
    pen_down()
    move_rel(0.0, -40.0)     # left leg
    pen_up()
    move_rel(10.0, 90.0)     # back to the neck

finally:
    finish()
