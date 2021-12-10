from Object import Object

class Mushroom(Object):
    """A mushroom object in the ALife simulation."""

    def __init__(self, initPose = (0, 0), geneticString = "0", stepSpawned=0):
        """
        Sets up mushroom with a location, geneticString, and step created
        :param initPose: tuple giving mushroom's initial location
        :param geneticString: string giving information about the mushroom
        :param stepSpawned: integer giving the simulation step the mushroom was created in
        """
        super().__init__()
        self.geneticString = geneticString
        self.row,self.col = initPose
        self.stepSpawned = stepSpawned

    def getTypeAbbreviation(self):
        """Returns the abbreviation for a mushroom object, "m"."""
        return "m"


