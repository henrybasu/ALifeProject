from Object import Object

class Mushroom(Object):
    """A mushroom object in the ALife simulation."""

    def __init__(self, initPose = (0, 0), geneticString = "0", stepSpawned=0):
        """
        Sets up an agent with a location, energy, geneticString, and step created
        :param initPose: tuple giving stone's initial location
        :param geneticString: string giving the stone's color
        :param stepSpawned: integer giving the simulation step the stone was created in
        """
        super().__init__()
        self.geneticString = geneticString
        self.row,self.col = initPose
        self.stepSpawned = stepSpawned
        # self.color = int(self.geneticString[0])

    def getTypeAbbreviation(self):
        return "m"


