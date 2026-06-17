import sys
import turtle as t

def teleport(xpos=0, ypos=0):
    gt = t.getturtle()
    gt.penup()
    gt.setpos(xpos, ypos)
    gt.pendown()

