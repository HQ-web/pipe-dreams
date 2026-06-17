import sys
import turtle as t


def patch_teleport():
    if sys.platform == 'linux':
        pass #t.teleport() remains as-is
    elif sys.platform == 'darwin':
        t.teleport = teleport
        print('Using teleport workaround')

def teleport(xpos=0, ypos=0):
    t.penup()
    t.setpos(xpos, ypos)
    t.pendown()

