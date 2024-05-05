import math
import logging

def vincenty_indirect(pair, heading=False):
    """
    calculates distance between two coordinates using Vincenty's indirect formula
    :param pair: tuple of two Coordinates objects
    :param heading: boolean, if True, returns distance and headings
    :return: distance in nautical miles
    """
    #  Requires a tuple of two Coordinates objects

    lat1 = float(pair[0].latitude)
    lon1 = float(pair[0].longitude)
    lat2 = float(pair[1].latitude)
    lon2 = float(pair[1].longitude)

    if lat1 == lat2 and lon1 == lon2:
        return 0.0

    # official WGS-84 ellipsoid parameters for output in meters
    a = 6378137.0
    b = 6356752.314245
    f = 1 / 298.257223563  
    
    L = math.radians(lon2 - lon1)
    U1 = math.atan((1 - f) * math.tan(math.radians(lat1)))
    U2 = math.atan((1 - f) * math.tan(math.radians(lat2)))
    sinU1 = math.sin(U1)
    cosU1 = math.cos(U1)
    sinU2 = math.sin(U2)
    cosU2 = math.cos(U2)

    lmbda = L  # "lambda" is a reserved word in Python
    iterLimit = 100
    lmbdaP = 0.0  # jury-rig filling lmbdaP with something first

    while True:
        
        sinlmbda = math.sin(lmbda)
        coslmbda = math.cos(lmbda)
        sinSigma = math.sqrt(((cosU2 * sinlmbda) ** 2.0) + (((cosU1 * sinU2) - (sinU1 * cosU2 * coslmbda)) ** 2.0))
        cosSigma = (sinU1 * sinU2) + (cosU1 * cosU2 * coslmbda)
        sigma = math.atan2(sinSigma, cosSigma)
        sinAlpha = (cosU1 * cosU2 * sinlmbda) / sinSigma
        cosSqAlpha = 1.0 - (sinAlpha ** 2.0)  # this will equal zero if two points are along the equator
        
        if cosSqAlpha == 0.0:
            cos2SigmaM = 0.0  # to protect from division error due to cosSqAlpha=0, also C will equal zero below
        else:
            cos2SigmaM = cosSigma - ((2.0 * sinU1 * sinU2) / cosSqAlpha)

        C = f / 16.0 * cosSqAlpha * (4.0 + f * (4.0 - 3.0 * cosSqAlpha))
        lmbdaP = lmbda
        lmbda = L + (1.0 - C) * f * sinAlpha * (
                    sigma + C * sinSigma * (cos2SigmaM + C * cosSigma * (-1.0 + 2.0 * cos2SigmaM * cos2SigmaM)))

        iterLimit -= 1
        
        if abs(lmbda - lmbdaP) < 1e-12:  # we have a winner
            break

        if iterLimit == 0:
            logging.warning("Vincenty formula failed to converge")
            print('formula failed to converge')
            return float("NaN")

    uSq = cosSqAlpha * (a ** 2.0 - b ** 2.0) / (b ** 2.0)
    A = 1.0 + uSq / 16384.0 * (4096.0 + uSq * (-768.0 + uSq * (320.0 - 175.0 * uSq)))
    B = uSq / 1024.0 * (256.0 + uSq * (-128.0 + uSq * (74.0 - 47.0 * uSq)))
    deltaSigma = B * sinSigma * (
                cos2SigmaM + B / 4.0 * (cosSigma * (-1.0 + 2.0 * cos2SigmaM * cos2SigmaM) - B / 6.0 * cos2SigmaM *
                                      (-3.0 + 4.0 * sinSigma * sinSigma) * (-3.0 + 4.0 * cos2SigmaM * cos2SigmaM)))
    s = b * A * (sigma - deltaSigma)

    # to return initial/final azimuths in addition to distance
    fwdAz = math.degrees(math.atan2(cosU2 * sinlmbda, cosU1 * sinU2 - sinU1 * cosU2 * coslmbda))
    revAz = math.degrees(math.atan2(cosU1 * sinlmbda, -sinU1 * cosU2 + cosU1 * sinU2 * coslmbda))

    distanceinNM = s / 1852.0  # s is output in meters, converting to nautical miles ->
    # 1852 meters in a nautical mile (official and exact)

    distanceinNM = round(distanceinNM, 6)  # round to 1mm precision - Vincenty's formulae are only accurate to within
    # .5mm, which is 0.000000269 nm

    if heading is True:
        return distanceinNM, fwdAz, revAz
    else:
        return distanceinNM
