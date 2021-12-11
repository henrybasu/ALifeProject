from Object import Object

class Stone(Object):
    """A stone object in the ALife simulation."""

    def __init__(self, initPose = (0, 0), geneticString = "0", stepSpawned=0):
        """
        Sets up stone with a location, geneticString, and step created
        :param initPose: tuple giving stone's initial location
        :param geneticString: string giving information about the stone
        :param stepSpawned: integer giving the simulation step the stone was created in
        """
        super().__init__()
        self.geneticString = geneticString
        self.row, self.col = initPose
        self.stepSpawned = stepSpawned

    def getTypeAbbreviation(self):
        """Returns the abbreviation for a stone object, "st"."""
        return "st"


