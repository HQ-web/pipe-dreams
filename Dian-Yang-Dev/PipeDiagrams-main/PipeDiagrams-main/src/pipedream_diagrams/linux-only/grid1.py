import sys
import turtle as t

from PIL import ImageGrab

from pipe_grid import Grid

if __name__ == "__main__":
    g = Grid(8,8)
    t.speed(0)

    row_length = 4
    col_length = 4
    ge = [(i,j) for i in range(row_length) for j in range(col_length)]

    g.add_grid_elements(ge)

    pipeline1 = [(0,0,'ul'), (1,0,'v'), (2,0,'v'), (3,0,'v')]
    pipeline2 = [(1,0,'h'), (1,1,'ul'), (2,1,'v'), (3,1,'lr'), (3,2,'ul')] 
    pipeline3 = [(2,0,'h'), (2,1,'h'), (2,2,'ul'), (3,2,'lr'), (3,3,'ul')] 
    pipeline4 = [(3,0,'h'), (3,1,'ul')]
    pipeline5 = [((0,1,'em'),(2,3,'sm'),'ext')]
    pipeline6 = [((0,2,'em'),(1,3,'sm'),'ext')]
    g.add_pipeline(pipeline1, pen_color="red")
    g.add_pipeline(pipeline2, pen_color="green")
    g.add_pipeline(pipeline3, pen_color="blue")
    g.add_pipeline(pipeline4, pen_color="orange")
    g.add_pipeline(pipeline5, pen_color="yellow")
    g.add_pipeline(pipeline6, pen_color="powderblue")

    #g.s is turtle screen

#   t.done()
    t.exitonclick()
