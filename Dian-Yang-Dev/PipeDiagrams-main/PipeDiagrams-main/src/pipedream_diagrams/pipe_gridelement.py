import math
import os
import sys
import turtle as t

from PIL import Image
from pipedream_diagrams.teleport import teleport

# use (share) anaonymous turtle by default.
# Can add specialized functions to use a separate turtle instance
class GridElement(object):
    height = 30        # distance between rows - translate along y axis
    width = 30      # distance between cols - translate along x axis
    # (x, y)
    def __init__(self, row_index, col_index):
        super(GridElement,self).__init__()
        self.t = t.getturtle()
        if not hasattr(self.t,'teleport'):
            self.t.teleport = teleport
        self.lower_left = self.ll = self.sw_corner = self.grid2xy(row_index, col_index, 'll')
        self.lower_right = self.lr = self.se_corner = self.grid2xy(row_index, col_index, 'lr')
        self.upper_left = self.ul = self.nw_corner = self.grid2xy(row_index, col_index, 'ul')
        self.upper_right = self.ur = self.ne_corner = self.grid2xy(row_index, col_index, 'ur')
        self.east_midpoint = self.em = self.grid2xy(row_index, col_index, 'em')
        self.north_midpoint = self.nm = self.grid2xy(row_index, col_index, 'nm')
        self.west_midpoint = self.wm = self.grid2xy(row_index, col_index, 'wm')
        self.south_midpoint = self.sm = self.grid2xy(row_index, col_index, 'sm')

    def grid2xy(self, row_index, col_index, label = 'll'):
        # translate grid coordinate (row_index, col_index) to (x,y) coordinate
        # x,y displacements are relative to lower left (southwest) corner coordinates
        # i.e. lower left corner is (0,0), upper right corner is (width, height)
        # other points on the grid element are simple height and width translations
        # e.g. lower right corner is lower left corner coords + (width,0)
        # e.g. upper right corner is lower left corner coords + (width,height)
        # e.g. upper (north) midpoint is lower left corner coords + (0.5*width,height))
        if label == 'll' or label == 'lower_left':
            x = (col_index+0)*self.width
            y = (row_index+0)*self.height
        elif label == 'lr' or label == 'lower_right':
            x = (col_index+1)*self.width
            y = (row_index+0)*self.height
        elif label == 'ur' or label == 'upper_right':
            x = (col_index+1)*self.width
            y = (row_index+1)*self.height
        elif label == 'ul' or label == 'upper_left':
            x = (col_index+0)*self.width
            y = (row_index+1)*self.height
        elif label == 'nm' or label == 'north_midpoint':
            x = (col_index+0.5)*self.width
            y = (row_index+1)*self.height
        elif label == 'em' or label == 'east_midpoint':
            x = (col_index+1)*self.width
            y = (row_index+0.5)*self.height
        elif label == 'sm' or label == 'south_midpoint':
            x = (col_index+0.5)*self.width
            y = (row_index+0)*self.height
        elif label == 'wm' or label == 'west_midpoint':
            x = (col_index+0)*self.width
            y = (row_index+0.5)*self.height
        else:
            print('bad args',row_index, col_index, label)
            sys.exit(1)
        return x,y
    def draw0width_element(self):
        self.t.teleport(*self.lr)
        self.t.setpos(self.ur)
    def draw_element(self):
        self.t.teleport(*self.ll)
        self.t.setpos(self.lr)
        self.t.setpos(self.ur)
        self.t.setpos(self.ul)
        self.t.setpos(self.ll)

