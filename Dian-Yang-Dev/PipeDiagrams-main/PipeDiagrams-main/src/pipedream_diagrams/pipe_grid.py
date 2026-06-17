import math
import os
from pathlib import Path
import sys
import turtle as t

from PIL import Image
try:
    from pipedream_diagrams.pipe_gridelement import GridElement
    from pipedream_diagrams.teleport import teleport
except ModuleNotFoundError as mfe:
    msg = (
    "The pipedream_diagrams Package wasn't found in sys.path.\n"
    "Look at the examples in <rootdir>/PipeDiagrams/tests\n"
    "Create a custom script in <rootdir>/PipeDiagrams/diagrams/ to make\n"
    "your own pipe diagram. Start with the skeleton script\n"
    "<rootdir>/PipeDiagrams/diagrams/grid-skel.py to create\n"
    "a custom script with 'context.py' in it.\n"
    "Run from anywhere (but  <rootdir>/PipeDiagrams/diagrams/ make the most sense." 
    )
    print(msg)

    sys.exit(1)


class Grid(object):
    # first pass - indexed from (0,0) - so 
    # (0,0) is southwest (lower left) corner
    # Only column 0 can be a 0-width column
    row_height = GridElement.height
    col_width = GridElement.width
    def __init__(self, rows, cols, startx=0, starty=0, fine_grid=False, has_zero_width=False):
        super(Grid,self).__init__()
        self.t = t.getturtle() # principle turtle is anonymous turtle
        self.s = self.t.screen # principle screen
        self.s.tracer(0,0) # need to use update() to refresh screen after changes
        if not hasattr(self.t,'teleport'):
            print("Grid doesn't have t.teleport")
            self.t.teleport = teleport
        else:
            print('Grid has t.teleport')
        self.t.screen.setup(height=(
            rows+2)*Grid.row_height,
            width=(cols+2)*Grid.col_width,
        startx=startx,
        starty=starty
        )
        self.t.screen.setworldcoordinates(
            -Grid.row_height,
            -Grid.col_width,
            (cols+1)*Grid.col_width,
            (rows+1)*Grid.row_height
        )
        self.pipedream_dir = os.path.dirname(os.path.realpath(__file__))
        self.label_dir = os.path.join(self.pipedream_dir, 'labels')
        self.t.speed(0)
        self.t.ht()
        if fine_grid:
            if has_zero_width:
                ge = [(i,j) for i in range(rows) for j in range(1,cols)]
            else:
                ge = [(i,j) for i in range(rows) for j in range(cols)]
            self.t.pencolor("#E3E3E3") # lighter grey
            self.add_grid_elements(ge)
            self.t.pencolor("black")
    def add_grid_elements(self, element_coord_list):
        self.t.pensize(2)
        for e in element_coord_list:
            label = e[-1]
            if label == '0width':
                x,y = e[:-1]
                ge = GridElement(x,y)
                ge.draw0width_element()
            else:
                ge = GridElement(*e)
                ge.draw_element()
        self.t.pensize(1)
    # on linux, can do one fill after multiple regions are drawn
    # alternative is to fill element by element
    # alternative colors #FFDAB9 #FFC0CB peachpuff1
    def fill_grid_elements(self, element_coord_list, fill_color="powderblue"):
        self.t.fillcolor(fill_color)
        for e in element_coord_list:
            ge = GridElement(*e)
            self.t.begin_fill()
            ge.draw_element()
            self.t.end_fill()
    def add_stamps(self, pipeline_label_list):
        for p in pipeline_label_list:
            label = os.path.join(self.label_dir, p + '.gif')
            t.addshape(label)
    def change_stamp(self, stamp_label):
        label = os.path.join(self.label_dir, stamp_label + '.gif')
        self.t.shape(label)
    def place_stamp(self, stamp_label, row_index, col_index,
                    row_offset=GridElement.height/2, col_offset=GridElement.width/2,
                    for_row=True, print_stamp=False):
        self.change_stamp(stamp_label)
        ge = GridElement(row_index, col_index)
        if for_row: # place to left of grid element
            print_stamp and print(stamp_label,ge.wm)
            self.t.teleport(ge.wm[0]-row_offset, ge.wm[1])
        else:   #place  on top of grid element
            print_stamp and print(stamp_label,ge.nm)
            self.t.teleport(ge.nm[0], ge.nm[1]+col_offset)
        self.t.stamp()
    def add_pipeline(self, pipeline_segment_list, pen_color="red"):
        for p in pipeline_segment_list:
            label = p[-1]
            if label == 'ext':
                node1,node2 = p[:-1]
                coords1 = self.node2coords(node1)
                coords2 = self.node2coords(node2)
                self.t.teleport(*coords1)
                self.t.pencolor(pen_color)
                self.t.pensize(5)
                self.t.setpos(coords2)
                self.t.pencolor("black")
                self.t.pensize(1)
            elif label == 'ul':
                row,col = p[:-1]
                ge = GridElement(row,col)
                self.pipe_arc(ge.ul, ge.width/2, label=label, pen_color=pen_color)
            elif label == 'lr':
                row,col = p[:-1]
                ge = GridElement(row,col)
                self.pipe_arc(ge.lr, ge.width/2, label=label, pen_color=pen_color)
            elif label == 'h' or label == 'v':
                row,col = p[:-1]
                ge = GridElement(row,col)
                self.pipe_line(ge, label=label, pen_color=pen_color)
    def node2coords(self,node):
        row, col, label = node
        ge = GridElement(row,col)
        if label == 'sm':
            return ge.sm
        elif label == 'em':
            return ge.em
        elif label == 'nm':
            return ge.nm
        elif label == 'wm':
            return ge.wm

    def dump_png(self, filename_root='pipepng'):
        self.s.update()
        canvas = self.t.screen.getcanvas()
        canvas.postscript(file= filename_root + '.eps')
        image = Image.open(filename_root + '.eps')
        png_filename = filename_root + '.png'
        image.save(png_filename ,'PNG')
        png = Image.open(png_filename)
        print (f'PNG image file is {png_filename} in directory {os.getcwd()}')
        print (f'PNG image size {image.size}')
        try:
            os.remove(filename_root + '.eps')
        except OSError:
            pass

    # angles are measured from 0 (pos x axis). 
    # east boundary would be 90 deg (pos y axis), south boundary would be 180 deg (neg x axis)
    # arc centered on se corner would be from 90 to 180 deg (ccw draw)
    # arc centered on nw corner would be from 270 to 360 deg (ccw draw)
    # angles are in degrees (resolution is one degree)
    def pipe_arc(self, center, radius, label="ul", pen_color="red"):
        self.t.pencolor(pen_color)
        self.t.pensize(5)
        if label == "ll":
            start_angle = 0
            stop_angle = 90
        elif label == "lr":
            start_angle = 90
            stop_angle = 180
        elif label == "ur":
            start_angle = 180
            stop_angle = 270
        elif label == "ul":
            start_angle = 270
            stop_angle = 360
        angle = math.radians(start_angle)
        startx = center[0] + radius*math.cos(angle)
        starty = center[1] + radius*math.sin(angle)
        self.t.teleport(startx, starty)
        for i in range(start_angle, stop_angle, 3):
            angle = math.radians(i)
            x = center[0] + radius*math.cos(angle)
            y = center[1] + radius*math.sin(angle)
            self.t.setpos(x,y)
        self.t.pencolor("black")
        self.t.pensize(1)

    def pipe_line(self, grid_element, label="h", pen_color="red"):
        if label == 'h':  # horizontal line through west and east grid sides
            self.t.teleport(*grid_element.wm)
            self.t.pencolor(pen_color)
            self.t.pensize(5)
            self.t.setpos(grid_element.em)
            self.t.pencolor("black")
            self.t.pensize(1)
        elif label == 'v':  # vertical line through south and north grid sides
            self.t.teleport(*grid_element.sm)
            self.t.pencolor(pen_color)
            self.t.pensize(5)
            self.t.setpos(grid_element.nm)
            self.t.pencolor("black")
            self.t.pensize(1)
        else:
            print('bad arg', label)
            sys.exit(1)


if __name__ == "__main__":
    # need context.py to actually find the pipedream_diagrams package
    # so run scripts from subdirectories under /home/be/PipeDiagrams
    pass
