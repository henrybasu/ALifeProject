from Object import Object

class Snow(Object):
    """A snow object in the ALife simulation."""

    def __init__(self, initPose = (0, 0), geneticString = "0", stepSpawned=0):
        """
        Sets up snow with a location, geneticString, and step created
        :param initPose: tuple giving snow's initial location
        :param geneticString: string giving information about the snow
        :param stepSpawned: integer giving the simulation step the snow was created in
        """
        super().__init__()
        self.geneticString = geneticString
        self.row, self.col = initPose
        self.stepSpawned = stepSpawned

    def getTypeAbbreviation(self):
        """Returns the abbreviation for a snow object, "sn"."""
        return "sn"


