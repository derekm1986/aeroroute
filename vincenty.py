#  Requires a list of two objects with the attribute .getcoordinates() which returns a tuple of type (-lat.00, lon.00)

import math


def vincenty(position1, position2):

    lat1 = float(position1.getcoordinates()[0])
    lon1 = float(position1.getcoordinates()[1])
    lat2 = float(position2.getcoordinates()[0])
    lon2 = float(position2.getcoordinates()[1])
    
    if lat1 == lat2 and lon1 == lon2:
        return 0.0
    
    a = 6378137.0
    b = 6356752.314245
    f = 1/298.257223563  # official WGS-84 ellipsoid parameters for output in meters
    L = math.radians(lon2-lon1)
    U1 = math.atan((1-f)*math.tan(math.radians(lat1)))
    U2 = math.atan((1-f)*math.tan(math.radians(lat2)))
    sinU1 = math.sin(U1)
    cosU1 = math.cos(U1)
    sinU2 = math.sin(U2)
    cosU2 = math.cos(U2)

    lmbda = L  # "lambda" is a reserved word in Python
    iterLimit = 100
    lmbdaP = 0.0  # jury-rig filling lmbdaP with something first

    while (abs(lmbda-lmbdaP) > 1e-12 and iterLimit > 0):
        
        sinlmbda = math.sin(lmbda)
        coslmbda = math.cos(lmbda)
        sinSigma = math.sqrt(((cosU2*sinlmbda)**2)+(((cosU1*sinU2)-(sinU1*cosU2*coslmbda))**2))
        cosSigma = (sinU1*sinU2)+(cosU1*cosU2*coslmbda)
        sigma = math.atan2(sinSigma, cosSigma)
        sinAlpha = (cosU1*cosU2*sinlmbda)/sinSigma
        cosSqAlpha = 1 - (sinAlpha**2)  # this will equal zero if two points are along the equator
        
        if cosSqAlpha == 0: 
            cos2SigmaM = 0  # to protect from division error due to cosSqAlpha=0, also C will equal zero below
        else:            
            cos2SigmaM = cosSigma - ((2*sinU1*sinU2)/cosSqAlpha)
        
        C = f/16*cosSqAlpha*(4+f*(4-3*cosSqAlpha))
        lmbdaP = lmbda
        lmbda = L + (1-C) * f * sinAlpha * (sigma + C * sinSigma*(cos2SigmaM+C*cosSigma*(-1+2*cos2SigmaM*cos2SigmaM)))
        
        iterLimit -= 1
        
        if iterLimit == 0:
            print('formula failed to converge')
            return float("NaN")

    uSq = cosSqAlpha * (a**2 - b**2) / (b**2)
    A = 1 + uSq/16384*(4096+uSq*(-768+uSq*(320-175*uSq)))
    B = uSq/1024 * (256+uSq*(-128+uSq*(74-47*uSq)))
    deltaSigma = B*sinSigma*(cos2SigmaM+B/4*(cosSigma*(-1+2*cos2SigmaM*cos2SigmaM)-B/6*cos2SigmaM*
        (-3+4*sinSigma*sinSigma)*(-3+4*cos2SigmaM*cos2SigmaM)))
    s = b*A*(sigma-deltaSigma)

    # s = round(s,3) #round to 1mm precision - Vincenty's formulae are only accurate to within .5mm

    #        to return initial/final bearings in addition to distance, use something like:
    fwdAz = math.atan2(cosU2*sinlmbda,  cosU1*sinU2-sinU1*cosU2*coslmbda)
    revAz = math.atan2(cosU1*sinlmbda, -sinU1*cosU2+cosU1*sinU2*coslmbda)

    print('firstazimuth: '+fwdAz+'secondazimuth: '+revAz)
    
    # return { distance:
    #         s, initialBearing:
    #       fwdAz.toDeg(), finalBearing:
    #                 revAz.toDeg()
    #               };
    
    distanceinNM = s/1852.0  # s is output in meters, converting to nautical miles ->
                                # 1852 meters in a nautical mile (official and exact)
    return distanceinNM
