# skeleton script to create diagrams
# Has required imports and setup content.
# Compare with other examples (e.g. grid2.py) to see what functions to use to create 
# Pipedream diagrams
import sys
import turtle as t

from context import get_script_path

if __name__ == "__main__":
    get_script_path()
    from pipedream_diagrams.pipe_grid import Grid

    t.tracer(0,0)
    #---- modify to set appropriate grid size --
    row_length = 10
    col_length = 10
    g = Grid(col_length, row_length, fine_grid=True, has_zero_width=True)

    #---- Insert appropriate grid description here ----

    #---- Insert appropriate grid description above ----
    g.dump_png()

    t.exitonclick()
