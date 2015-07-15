# This file parses the vasFMC format Navaids.txt file
# Navaids.txt file must be in same directory

def navaiddictmaker():

    navaid_file = open("Navaids.txt")

    global navaiddict

    navaiddict = {} # make an empty dictionary

    for line in navaid_file:
        navaidid, navaidname, navaidfrequency, navaidunknown1, navaidunknown2, navaidunknown3, navaidlat, navaidlong, navaidelevation, navaidregion = line.rstrip().split("|")
        navaidlatwithdecimal = navaidlat[:len(navaidlat)-6] + "." + navaidlat[len(navaidlat)-6:] #6 decimal places
        navaidlongwithdecimal = navaidlong[:len(navaidlong)-6] + "." + navaidlong[len(navaidlong)-6:] #6 decimal places
        navaiddict.setdefault(navaidid, []).append((navaidlatwithdecimal, navaidlongwithdecimal))

    navaid_file.close()
    
    print "NAVAIDs loaded into memory"