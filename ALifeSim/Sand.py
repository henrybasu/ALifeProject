from Object import Object

class Sand(Object):
    """A sand object in the ALife simulation."""

    def __init__(self, initPose = (0, 0), geneticString = "0", stepSpawned=0):
        """
        Sets up sand with a location, geneticString, and step created
        :param initPose: tuple giving sand's initial location
        :param geneticString: string giving information about the sand
        :param stepSpawned: integer giving the simulation step the sand was created in
        """
        super().__init__()
        self.geneticString = geneticString
        self.row, self.col = initPose
        self.stepSpawned = stepSpawned

    def getTypeAbbreviation(self):
        """Returns the abbreviation for a sand object, "sa"."""
        return "sa"


