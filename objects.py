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

    def __iter__(self):
        for possibility in self.possibilities:
            yield possibility

    def addpossibility(self, possibility):
        self.possibilities.append(possibility)

    def getidentifier(self):
        return self.identifier

    def getpossibilities(self):
        return self.possibilities


class Possibility(object):

    def __init__(self, originalposition, possibility):
        self.originalposition = originalposition
        self.possibility = possibility

    def getoriginalposition(self):
        return self.originalposition

    def getpossibility(self):
        return self.possibility

class Route(object):

    def __init__(self):
        self.route = []
        self.containsmultiples = False

    def addelement(self, element):
        self.route.append(element)

    def deambiguate(self, position, possibilitynumber):
        self.route[position] = self.route[position].getpossibilities()[possibilitynumber]

    def getroute(self):
        return self.route