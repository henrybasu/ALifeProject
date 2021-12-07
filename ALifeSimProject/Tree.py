from Object import Object

class Tree(Object):
    """A tree object in the ALife simulation."""

    def __init__(self, initPose = (0, 0), geneticString = "0", stepSpawned=0):
        """
        Sets up an agent with a location, energy, geneticString, and step created
        :param initPose: tuple giving stone's initial location
        :param geneticString: string giving the stone's color
        :param stepSpawned: integer giving the simulation step the stone was created in
        """
        super().__init__()
        self.geneticString = geneticString
        self.canGrowFood = geneticString[0]
        # self.color = int(self.geneticString[0])
        
    def getCanGrowFood(self):
        return self.canGrowFood

    def getTypeAbbreviation(self):
        return "t"


