# This file parses the vasFMC format Airports.txt file
# Airports.txt file must be in same directory

# This file does not attempt to read runway data

def airportdictmaker():

    airport_file = open("Airports.txt")

    global airportdict    
    
    airportdict = {} # make an empty dictionary
    
    for line in airport_file:
        if line.startswith("A"):
            linefirstletter, airportid, airportname, airportlat, airportlong, airportelevation = line.rstrip().split("|")
            airportlatwithdecimal = airportlat[:len(airportlat)-6] + "." + airportlat[len(airportlat)-6:] #6 decimal places
            airportlongwithdecimal = airportlong[:len(airportlong)-6] + "." + airportlong[len(airportlong)-6:] #6 decimal places
            airportdict.setdefault(airportid, []).append((airportlatwithdecimal, airportlongwithdecimal))

    airport_file.close()
        
    print "Airports loaded into memory"