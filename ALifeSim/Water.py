from Object import Object

class Water(Object):
    """A water object in the ALife simulation."""

    def __init__(self, initPose = (0, 0), geneticString = "0", stepSpawned=0):
        """
        Sets up water with a location, geneticString, and step created
        :param initPose: tuple giving water's initial location
        :param geneticString: string giving information about the water
        :param stepSpawned: integer giving the simulation step the water was created in
        """
        super().__init__()
        self.geneticString = geneticString
        self.row, self.col = initPose
        self.stepSpawned = stepSpawned

    def getTypeAbbreviation(self):
        """Returns the abbreviation for a water object, "w"."""
        return "w"


