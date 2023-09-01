import os
import glob

# Get the names of all Python files in the current directory (controller folder)
__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py")]

# Import the modules defined in each Python file
from . import *
