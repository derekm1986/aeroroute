# This file parses the vasFMC format Navaids.txt file
# Navaids.txt file must be in AIRAC directory

from objects import PointInSpace
from objects import AmbiguousPoint


def navaid_dict_maker():

    navaid_file = open("AIRAC/Navaids.txt")

    navaid_dict = {}

    for line in navaid_file:
        currentline = line.rstrip().split("|")
        navaidid = currentline[0]
        navaidname = currentline[1]
        navaidlat = currentline[6]
        navaidlong = currentline[7]

        navaidlatisnegative = False  # establish variable
            
        if navaidlat.startswith("-"):
            navaidlatisnegative = True
            navaidlat = navaidlat[1:]
          
        if len(navaidlat) < 7:
            navaidlat = "0" * (7 - len(navaidlat)) + navaidlat
           
        navaidlatwithdecimal = navaidlat[:-6] + "." + navaidlat[-6:]  # 6 decimal places
           
        if navaidlatisnegative is True:
            navaidlatwithdecimal = "-" + navaidlatwithdecimal
            
        navaidlongisnegative = False  # establish variable
            
        if navaidlong.startswith("-"):
            navaidlongisnegative = True
            navaidlong = navaidlong[1:]

        if len(navaidlong) < 7:
            navaidlong = "0" * (7 - len(navaidlong)) + navaidlong
                
        navaidlongwithdecimal = navaidlong[:-6] + "." + navaidlong[-6:]  # 6 decimal places
            
        if navaidlongisnegative is True:
            navaidlongwithdecimal = "-" + navaidlongwithdecimal

        navaidobj = PointInSpace(navaidid, (navaidlatwithdecimal, navaidlongwithdecimal), 'NAVAID', navaidname)

        if navaidid in navaid_dict:
            if type(navaid_dict[navaidid]) is AmbiguousPoint:
                navaid_dict[navaidid].add_possibility(navaidobj)
            else:
                navaid_dict[navaidid] = AmbiguousPoint(navaidid, navaid_dict[navaidid])
                navaid_dict[navaidid].add_possibility(navaidobj)
        else:
            navaid_dict[navaidid] = navaidobj

    navaid_file.close()

    return navaid_dict
