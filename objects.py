class Pointinspace(object):

    def __init__(self, identifier, coordinates, typeelement, elementname=None):
        self.identifier = identifier
        self.coordinates = coordinates
        self.typeelement = typeelement
        self.elementname = elementname

    def getidentifier(self):
        return self.identifier

    def getcoordinates(self):
        return self.coordinates

    def gettypeelement(self):
        return self.typeelement

    def getelementname(self):
        if self.elementname is not None:
            return self.elementname
        else:
            pass

class Airport(object):

        def __init__(self, identifier, coordinates, elementname=None):
            self.identifier = identifier
            self.coordinates = coordinates
            self.typeelement = 'airport'
            self.elementname = elementname

        def getidentifier(self):
            return self.identifier

        def getcoordinates(self):
            return self.coordinates

        def gettypeelement(self):
            return self.typeelement

        def getelementname(self):
            if self.elementname is not None:
                return self.elementname
            else:
                pass


class Ambiguouselement(object):

    def __init__(self, identifier, initialpossibility):
        self.identifier = identifier
        self.possibilities = [initialpossibility]

    def addpossibility(self, possibility):
        self.possibilities.append(possibility)

    def getidentifier(self):
        return self.identifier

    def getpossibilities(self):
        return self.possibilities
