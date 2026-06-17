import math
import os
from pathlib import Path
import sys
import turtle as t

from PIL import Image
from pipe_gridelement import GridElement


class Grid(object):
    # first pass - indexed from (0,0) - so 
    # (0,0) is southwest (lower left) corner
    # Only column 0 can be a 0-width column
    row_height = GridElement.height
    col_width = GridElement.width
    def __init__(self, rows, cols, fine_grid=False, has_zero_width=False):
        super(Grid,self).__init__()
        self.s = t.Screen()
#       self.s.setup(height=(rows+2)*Grid.row_height,width=(cols+2)*Grid.col_width)
#       t.setworldcoordinates(0,0,cols*Grid.col_width,rows*Grid.row_height)
        self.s.setup(height=(rows+2)*Grid.row_height,width=(cols+2)*Grid.col_width)
        t.setworldcoordinates(-Grid.row_height,-Grid.col_width,(cols+1)*Grid.col_width,(rows+1)*Grid.row_height)
        t.speed(0)
        t.ht()
        if fine_grid:
            if has_zero_width:
                ge = [(i,j) for i in range(rows) for j in range(1,cols)]
            else:
                ge = [(i,j) for i in range(rows) for j in range(cols)]
            t.pencolor("#E3E3E3") # lighter grey
            self.add_grid_elements(ge)
            t.pencolor("black")
    def add_grid_elements(self, element_coord_list):
        t.pensize(2)
        for e in element_coord_list:
            label = e[-1]
            if label == '0width':
                x,y = e[:-1]
                ge = GridElement(x,y)
                ge.draw0width_element()
            else:
                ge = GridElement(*e)
                ge.draw_element()
        t.pensize(1)
    # on linux, can do one fill after multiple regions are drawn
    # alternative is to fill element by element
    # alternative colors #FFDAB9 #FFC0CB peachpuff1
    def fill_grid_elements(self, element_coord_list, fill_color="powderblue"):
        t.fillcolor(fill_color)
        t.begin_fill()
        for e in element_coord_list:
            ge = GridElement(*e)
            ge.draw_element()
        t.end_fill()
    def add_stamps(self, pipeline_label_list):
        for p in pipeline_label_list:
            label = 'labels/' + p + '.gif'
            t.addshape(label)
    def change_stamp(self, stamp_label):
        label = 'labels/' + stamp_label + '.gif'
        t.shape(label)
    def place_stamp(self, stamp_label, row_index, col_index,
                    row_offset=GridElement.height/2, col_offset=GridElement.width/2,
                    for_row=True, print_stamp=False):
        self.change_stamp(stamp_label)
        ge = GridElement(row_index, col_index)
        if for_row: # place to left of grid element
            print_stamp and print(stamp_label,ge.wm)
            t.teleport(ge.wm[0]-row_offset, ge.wm[1])
        else:   #place  on top of grid element
            print_stamp and print(stamp_label,ge.nm)
            t.teleport(ge.nm[0], ge.nm[1]+col_offset)
        t.stamp()
    def add_pipeline(self, pipeline_segment_list, pen_color="red"):
        for p in pipeline_segment_list:
            t.tracer(0,0)
            label = p[-1]
            if label == 'ext':
                node1,node2 = p[:-1]
                coords1 = self.node2coords(node1)
                coords2 = self.node2coords(node2)
                t.teleport(*coords1)
                t.pencolor(pen_color)
                t.pensize(5)
                t.setpos(coords2)
                t.pencolor("black")
                t.pensize(1)
            elif label == 'ul':
                row,col = p[:-1]
                ge = GridElement(row,col)
                pipe_arc(ge.ul, ge.width/2, label=label, pen_color=pen_color)
            elif label == 'lr':
                row,col = p[:-1]
                ge = GridElement(row,col)
                pipe_arc(ge.lr, ge.width/2, label=label, pen_color=pen_color)
            elif label == 'h' or label == 'v':
                row,col = p[:-1]
                ge = GridElement(row,col)
                pipe_line(ge, label=label, pen_color=pen_color)
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
        canvas = self.s.getcanvas()
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
def pipe_arc(center, radius, label="ul", pen_color="red"):
    t.pencolor(pen_color)
    t.pensize(5)
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
    t.teleport(startx, starty)
    for i in range(start_angle, stop_angle, 3):
        angle = math.radians(i)
        x = center[0] + radius*math.cos(angle)
        y = center[1] + radius*math.sin(angle)
        t.setpos(x,y)
    t.pencolor("black")
    t.pensize(1)

def pipe_line(grid_element, label="h", pen_color="red"):
    if label == 'h':  # horizontal line through west and east grid sides
        t.teleport(*grid_element.wm)
        t.pencolor(pen_color)
        t.pensize(5)
        t.setpos(grid_element.em)
        t.pencolor("black")
        t.pensize(1)
    elif label == 'v':  # vertical line through south and north grid sides
        t.teleport(*grid_element.sm)
        t.pencolor(pen_color)
        t.pensize(5)
        t.setpos(grid_element.nm)
        t.pencolor("black")
        t.pensize(1)
    else:
        print('bad arg', label)
        sys.exit(1)


if __name__ == "__main__":
    t.tracer(0,0)
    g = Grid(8,8)
    t.speed(0)

    print(t.pos())

    ge1 = GridElement(1,1)
    ge2 = GridElement(2,3)
    ge1.draw_element()
    ge2.draw_element()

    pipe_arc(ge1.lr, ge1.width/2, "lr")
    pipe_arc(ge2.ul, ge2.width/2, pen_color="green")
    pipe_line(ge1, 'h', pen_color="green")
    pipe_line(ge2, 'v', pen_color="red")
    t.tracer(1,0)

#   t.done()
#   t.exitonclick()
