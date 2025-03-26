import sys
import os

# Add the src directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from parsers import cdrreader # type: ignore

# test aeroroute using all cdrs

cdr_dict = cdrreader.cdr_dict_maker()

for val in cdr_dict.values():
    print(val.cdr_id, val.distance)
