from Object import Object

class Grass(Object):
    """A grass object in the ALife simulation."""

    def __init__(self, initPose = (0, 0), geneticString = "0", stepSpawned=0):
        """
        Sets up grass with a location, geneticString, and step created
        :param initPose: tuple giving grass's initial location
        :param geneticString: string giving information about the grass
        :param stepSpawned: integer giving the simulation step the grass was created in
        """
        super().__init__()
        self.geneticString = geneticString
        self.row, self.col = initPose
        self.stepSpawned = stepSpawned

    def getTypeAbbreviation(self):
        """Returns the abbreviation for a grass object, "g"."""
        return "g"


