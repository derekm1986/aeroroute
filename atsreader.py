# This file parses the vasFMC format ATS.txt file
# ATS.txt file must be in AIRAC directory

from objects import Airway
from objects import PointInSpace
from objects import AmbiguousAirway
from objects import Coordinates


def airway_lat_long_maker(input_string) -> str:

    input_was_negative = False  # fill it with something

    if input_string.startswith('-'):
        input_was_negative = True

    # remove the negative, if necessary
    if input_was_negative:
        input_string = input_string[1:]

    degrees = input_string[:-6]

    # remove leading zeroes
    degrees = degrees.lstrip('0')

    if degrees == "":
        degrees = "0"

    decimal = input_string[-6:]  # 6 decimal places

    input_with_decimal = degrees + '.' + decimal

    if input_was_negative:
        # put the negative sign back if needed
        input_with_decimal = '-' + input_with_decimal

    output = input_with_decimal

    return output


def airway_dict_maker():

    ats_file = open("AIRAC/ATS.txt")

    airway_dict = {}

    contents = ats_file.read()

    paragraphs = contents.split("\n\n")  # each paragraph should be an airway

    #  remove blank strings that will occur at end of list
    while "" in paragraphs:
        paragraphs.remove("")

    split_paragraphs = []

    for paragraph in paragraphs:
        split_paragraphs.append(paragraph.split('\n'))
    #  each split paragraph is an airway with lines in a list

    for split_paragraph in split_paragraphs:

        for line in split_paragraph:

            if line.startswith("A"):  # this is the beginning of an airway
                current_line = line.rstrip().split("|")
                route_id = current_line[1]

                currentairway = Airway(route_id)

                airwaylist = []
                simpleairwaylist = []

            elif line.startswith("S"):

                current_line = line.rstrip().split("|")
                firstid = current_line[1]
                firstlat = current_line[2]
                firstlong = current_line[3]
                secondid = current_line[4]
                secondlat = current_line[5]
                secondlong = current_line[6]

                firstlat = airway_lat_long_maker(firstlat)
                firstlong = airway_lat_long_maker(firstlong)
                secondlat = airway_lat_long_maker(secondlat)
                secondlong = airway_lat_long_maker(secondlong)

                firstwaypoint = [firstid, firstlat, firstlong]
                secondwaypoint = [secondid, secondlat, secondlong]

                if firstwaypoint not in simpleairwaylist:
                    airwaylist.append(PointInSpace(firstwaypoint[0], Coordinates(firstwaypoint[1], firstwaypoint[2]),
                                                   'airwaywaypoint'))
                    simpleairwaylist.append(firstwaypoint)

                if secondwaypoint not in simpleairwaylist:
                    airwaylist.append(PointInSpace(secondwaypoint[0], Coordinates(secondwaypoint[1], secondwaypoint[2]),
                                                   'airwaywaypoint'))
                    simpleairwaylist.append(secondwaypoint)

        currentairway.set_waypoints(airwaylist)

        if route_id in airway_dict:
            if type(airway_dict[route_id]) is AmbiguousAirway:
                airway_dict[route_id].add_possibility(currentairway)
            else:
                airway_dict[route_id] = AmbiguousAirway(route_id, airway_dict[route_id])
                airway_dict[route_id].add_possibility(currentairway)
        else:
            airway_dict[route_id] = currentairway

    ats_file.close()

    return airway_dict
