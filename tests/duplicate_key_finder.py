import sys
import os

# Add the src directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import nav_data_library # type: ignore

nav_library = nav_data_library.NavDataLibrary()

airport_dict = nav_library.airports
points_in_space_dict = nav_library.points_in_space
airway_dict = nav_library.airways

def duplicate_key_finder():
    """
    Finds duplicate keys in the nav_data_library
    """
    all_keys = []
    for key in airport_dict:
        all_keys.append(key)
    for key in points_in_space_dict:
        all_keys.append(key)
    for key in airway_dict:
        all_keys.append(key)
    
    all_keys.sort()

    duplicates = []
    for i in range(1, len(all_keys)):
        if all_keys[i] == all_keys[i-1]:
            duplicates.append(all_keys[i])

    return duplicates

print(duplicate_key_finder())

