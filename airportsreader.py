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
            
            airportlatisnegative = False #establish variable
            
            if airportlat.startswith("-"):
                airportlatisnegative = True
                airportlat = airportlat[1:]
            
            if len(airportlat) < 7:
                airportlat = "0" * (7 - len(airportlat)) + airportlat
            
            airportlatwithdecimal = airportlat[:len(airportlat)-6] + "." + airportlat[len(airportlat)-6:] #6 decimal places
            
            if airportlatisnegative == True:
                airportlatwithdecimal = "-" + airportlatwithdecimal
            

            
            
            airportlongisnegative = False #establish variable
            
            if airportlong.startswith("-"):
                airportlongisnegative = True
                airportlong = airportlong[1:]

            if len(airportlong) < 7:
                airportlong = "0" * (7 - len(airportlong)) + airportlong
                
            airportlongwithdecimal = airportlong[:len(airportlong)-6] + "." + airportlong[len(airportlong)-6:] #6 decimal places
            
            if airportlongisnegative == True:
                airportlongwithdecimal = "-" + airportlongwithdecimal


            
            
            airportdict.setdefault(airportid, []).append((airportlatwithdecimal, airportlongwithdecimal))

    airport_file.close()