class Pointinspace(object):

    def __init__(self, identifier, coordinates):
        self.identifier = identifier
        self.coordinates = coordinates

    def getidentifier(self):
        return self.identifier

    def getcoordinates(self):
        return self.coordinates


class Ambiguouselement(object):

    def __init__(self, identifier, possibilities=[]):
        self.identifier = identifier
        self.possibilities = possibilities

    def addpossibility(self, possibility):
        self.possibilities.append(possibility)

    def getidentifier(self):
        return self.identifier

    def getpossibilities(self):
        return self.possibilities

#class Navaid(Pointinspace):
