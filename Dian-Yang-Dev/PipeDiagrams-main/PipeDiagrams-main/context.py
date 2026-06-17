import os
import sys

def get_script_path():
    """
    find PipeDream/src/pipedream_diagrams path and append to sys.path so diagram generator programs
    (and examples) can find the modules. Eventually, this should be handled by package management
    setup.py/pyproject.toml/pip install but this is the best I can do for now
    modifying sys.path here modifies it everywhere (global scope)
    """
    root_dir = os.path.dirname(os.path.realpath(__file__))
    src_dir = os.path.join(root_dir, 'src')
    pipedream_dir = os.path.join(src_dir, 'pipedream_diagrams')
    sys.path.append(src_dir)
    return pipedream_dir
