# PipeDream
Create Pipedream diagrams (combinatorics) through the python turtle module

Running this code has some prerequisites

Recommend using a Python version >= python 3.13.3
  - uses turtle (built-in) module
      - On Darwin, turtle.teleport is not available unless you build a version of Python from source
  - compiled Python with support for Tkinter (and several other extensions like curses, readline, dbm, lzma ssl ...)
  - use virtual env and add pillow PYPI package  (the only real PYPI requirement when using a full Python build)

The bpython PYPI package can make interactive runs of code easier to work with (if something goes wrong)

Need to run from the root installation directory - I suggest calling it pipedream or turtle or something similar

Example programs are: (listed from simplest to most complicated)
- grid1.py
- grid1-fine_grid.py
- grid2.py
- grid2-fine_grid.py
- grid2-stamp.py

Other files are source files
