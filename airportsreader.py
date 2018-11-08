# This file parses the vasFMC format Airports.txt file
# Airports.txt file must be in AIRAC directory

# This file does not attempt to read runway data

from objects import Airport


def airportdictmaker():

    airport_file = open("AIRAC/Airports.txt")

    global airportdict

    airportdict = {}

    for line in airport_file:
        if line.startswith("A"):
            currentline = line.rstrip().split("|")
            airportid = currentline[1]
            airportname = currentline[2]
            airportlat = currentline[3]
            airportlong = currentline[4]

            airportlatisnegative = False  # establish variable

            if airportlat.startswith("-"):
                airportlatisnegative = True
                airportlat = airportlat[1:]

            if len(airportlat) < 7:
                airportlat = "0" * (7 - len(airportlat)) + airportlat

            airportlatwithdecimal = airportlat[:len(airportlat)-6] + "." + airportlat[len(airportlat)-6:]  # 6 decimal places

            if airportlatisnegative is True:
                airportlatwithdecimal = "-" + airportlatwithdecimal

            airportlongisnegative = False  # establish variable

            if airportlong.startswith("-"):
                airportlongisnegative = True
                airportlong = airportlong[1:]

            if len(airportlong) < 7:
                airportlong = "0" * (7 - len(airportlong)) + airportlong

            airportlongwithdecimal = airportlong[:len(airportlong)-6] + "." + airportlong[len(airportlong)-6:]  # 6 decimal places

            if airportlongisnegative is True:
                airportlongwithdecimal = "-" + airportlongwithdecimal

            airportobj = Airport(airportid, (airportlatwithdecimal, airportlongwithdecimal), airportname)

            airportdict[airportid] = airportobj

    airport_file.close()
