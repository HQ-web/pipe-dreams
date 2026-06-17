import sys
import turtle as t

from context import get_script_path


if __name__ == "__main__":
    get_script_path()
    from pipedream_diagrams.pipe_grid import Grid

    row_length = 10
    col_length = 10
    g = Grid(col_length, row_length)

    ge = [(0,0,'0width')]
    ge += [(i,1) for i in range(1,3)]
    ge += [(i,j) for i in range(3,6) for j in range(2,4)]
    ge += [(i,j) for i in range(6,8) for j in range(4,7)]
    ge += [(i,j) for i in range(8,9) for j in range(7,9)]
    ge += [(i,j) for i in range(9,10) for j in range(9,10)]
    g.add_grid_elements(ge)

    pipeline1 = [(1,1,'h'),]
    pipeline2 = [
        ((0,0,'em'),(1,1,'sm'),'ext'),
        (1,1,'v'),(2,1,'lr'),
        ((2,1,'em'),(3,2,'sm'),'ext'),
        (3,2,'lr'),(3,3,'h'),
        ((3,3,'em'),(6,6,'sm'),'ext'),
        (6,6,'lr')
    ]
    pipeline3 = [(3,2,'ul'),(4,2,'lr'),(4,3,'h')]
    pipeline4 = [(4,2,'ul'),(5,2,'lr'),(5,3,'h')]
    pipeline5 = [
        (6,4,'ul'),(7,4,'lr'),(7,5,'h'),
        (7,6,'h'),
        ((7,6,'em'),(8,7,'sm'),'ext'),
        (8,7,'lr'),(8,8,'h'),
        ((8,8,'em'),(9,9,'sm'),'ext'),
        (9,9,'lr')
    ]

    g.add_pipeline(pipeline1, pen_color="salmon")
    g.add_pipeline(pipeline2, pen_color="blue")
    g.add_pipeline(pipeline3, pen_color="purple")
    g.add_pipeline(pipeline4, pen_color="purple")
    g.add_pipeline(pipeline5, pen_color="green")

    g.dump_png()

    t.exitonclick()
