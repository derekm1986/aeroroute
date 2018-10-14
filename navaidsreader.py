# This file parses the vasFMC format Navaids.txt file
# Navaids.txt file must be in same directory

from objects import Pointinspace
from objects import Ambiguouselement


def navaiddictmaker():

    navaid_file = open("AIRAC/Navaids.txt")

    global navaiddict

    navaiddict = {}

    for line in navaid_file:
        navaidid, navaidname, navaidfrequency, navaidunknown1, navaidunknown2, navaidunknown3, navaidlat, navaidlong, navaidelevation, navaidregion = line.rstrip().split("|")
        navaidlatisnegative = False  # establish variable
            
        if navaidlat.startswith("-"):
            navaidlatisnegative = True
            navaidlat = navaidlat[1:]
          
        if len(navaidlat) < 7:
            navaidlat = "0" * (7 - len(navaidlat)) + navaidlat
           
        navaidlatwithdecimal = navaidlat[:len(navaidlat)-6] + "." + navaidlat[len(navaidlat)-6:]  # 6 decimal places
           
        if navaidlatisnegative is True:
            navaidlatwithdecimal = "-" + navaidlatwithdecimal
            
        navaidlongisnegative = False  # establish variable
            
        if navaidlong.startswith("-"):
            navaidlongisnegative = True
            navaidlong = navaidlong[1:]

        if len(navaidlong) < 7:
            navaidlong = "0" * (7 - len(navaidlong)) + navaidlong
                
        navaidlongwithdecimal = navaidlong[:len(navaidlong)-6] + "." + navaidlong[len(navaidlong)-6:]  # 6 decimal places
            
        if navaidlongisnegative is True:
            navaidlongwithdecimal = "-" + navaidlongwithdecimal

        navaidobj = Pointinspace(navaidid, (navaidlatwithdecimal, navaidlongwithdecimal), 'NAVAID', navaidname)

        if navaidid in navaiddict:
            if type(navaiddict[navaidid]) is Ambiguouselement:
                navaiddict[navaidid].addpossibility(navaidobj)
            else:
                navaiddict[navaidid] = Ambiguouselement(navaidid, navaiddict[navaidid])
                navaiddict[navaidid].addpossibility(navaidobj)
        else:
            navaiddict[navaidid] = navaidobj

    navaid_file.close()
