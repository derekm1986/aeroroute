# This file parses the vasFMC format Navaids.txt file
# Navaids.txt file must be in same directory

def navaiddictmaker():

    navaid_file = open("Navaids.txt")

    global navaiddict

    navaiddict = {} # make an empty dictionary

    for line in navaid_file:
        navaidid, navaidname, navaidfrequency, navaidunknown1, navaidunknown2, navaidunknown3, navaidlat, navaidlong, navaidelevation, navaidregion = line.rstrip().split("|")
        navaidlatisnegative = False #establish variable
            
        if navaidlat.startswith("-"):
            navaidlatisnegative = True
            navaidlat = navaidlat[1:]
          
        if len(navaidlat) < 6:
            navaidlat = "0" * (7 - len(navaidlat)) + navaidlat
           
        navaidlatwithdecimal = navaidlat[:len(navaidlat)-6] + "." + navaidlat[len(navaidlat)-6:] #6 decimal places
           
        if navaidlatisnegative == True:
            navaidlatwithdecimal = "-" + navaidlatwithdecimal
            
        navaidlatwithdecimal = float(navaidlatwithdecimal)
            
            
        navaidlongisnegative = False #establish variable
            
        if navaidlong.startswith("-"):
            navaidlongisnegative = True
            navaidlong = navaidlong[1:]

        if len(navaidlong) < 6:
            navaidlong = "0" * (7 - len(navaidlong)) + navaidlong
                
        navaidlongwithdecimal = navaidlong[:len(navaidlong)-6] + "." + navaidlong[len(navaidlong)-6:] #6 decimal places
            
        if navaidlongisnegative == True:
            navaidlongwithdecimal = "-" + navaidlongwithdecimal

        navaidlongwithdecimal = float(navaidlongwithdecimal)
        navaiddict.setdefault(navaidid, []).append((navaidlatwithdecimal, navaidlongwithdecimal))

    navaid_file.close()
    
    print "NAVAIDs loaded into memory"