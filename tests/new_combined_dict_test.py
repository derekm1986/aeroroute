import sys
import os

# Add the src directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import nav_data_library as ndl # type: ignore

new_ndl = ndl.NavDataLibrary()

testitem1 = new_ndl.combined_dict_entries['HYLND']

print("test 1", testitem1)



testitem2 = new_ndl.combined_dict_entries['J4']

print("test 5", type(testitem2))

print("test 6", testitem2)


testitem3 = new_ndl.combined_dict_entries['KBOS']

print("test 9", type(testitem3))

print("test 10", testitem3)

