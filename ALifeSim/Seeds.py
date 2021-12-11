from Object import Object

class Seeds(Object):
    """A pit object in the ALife simulation."""
    def __init__(self, initPose = (0, 0), geneticString = "0", stepSpawned=0):
        """
        Sets up pit with a location, geneticString, and step created
        :param initPose: tuple giving pit's initial location
        :param geneticString: string giving information about the pit
        :param stepSpawned: integer giving the simulation step the pit was created in
        """
        super().__init__()
        self.geneticString = geneticString
        self.row,self.col = initPose
        self.stepSpawned = stepSpawned

    def getTypeAbbreviation(self):
        """Returns the abbreviation for a pit object, "p"."""
        return "se"


