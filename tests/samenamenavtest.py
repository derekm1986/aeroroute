import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import nav_data_library as ndl

print("success")
# this file is just to test imports so I can put tests in a separate directory

# now go through all nav data libraries and look for navaids, airports, airways with the same names

