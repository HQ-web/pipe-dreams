import math
import os
import sys
import turtle as t

from PIL import Image


class Grid(object):
    # first pass - indexed from (0,0) - so 
    # (0,0) is southwest (lower left) corner
    # Only column 0 can be a 0-width column
    row_height = 25
    col_width = 25
    def __init__(self, rows, cols, fine_grid=False, has_zero_width=False):
        super(Grid,self).__init__()
        self.s = t.Screen()
        self.s.setup(height=rows*Grid.row_height,width=cols*Grid.col_width)
        t.setworldcoordinates(0,0,cols*Grid.col_width,rows*Grid.row_height)
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


class GridElement(object):
    height = Grid.row_height        # distance between rows - translate along y axis
    width = Grid.col_width      # distance between cols - translate along x axis
    def __init__(self, row_index, col_index):
        # (x, y)
        super(GridElement,self).__init__()
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
        t.teleport(*self.lr)
        t.setpos(self.ur)
    def draw_element(self):
        t.teleport(*self.ll)
        t.setpos(self.lr)
        t.setpos(self.ur)
        t.setpos(self.ul)
        t.setpos(self.ll)

# row_length is also the number of columns - column dimension
def grid2list(row, col, row_length):
    index = row*row_length + col
    return index

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


# pipeline segment external to grid elements
def pipe_ext(node1, node2, pen_color="red"):
        t.teleport(node1)
        t.pencolor(pen_color)
        t.pensize(5)
        t.setpos(node2)
        t.pencolor("black")
        t.pensize(1)

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
