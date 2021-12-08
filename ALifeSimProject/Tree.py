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
        self.hasFood = geneticString[0]
        self.row,self.col = initPose
        self.stepSpawned = stepSpawned
        self.justChanged = False
        self.stepsUntilBloom = 5
        # self.color = int(self.geneticString[0])
        
    def getHasFood(self):
        return self.hasFood

    def setHasFood(self, newCanGrowFood):
        self.hasFood = newCanGrowFood
        self.justChanged = True

    def setJustChangedBloom(self, newVal):
        self.justChanged = newVal

    def getStepsUntilBloom(self):
        return self.stepsUntilBloom

    def setStepsUntilBloom(self, newVal):
        self.stepsUntilBloom = newVal

    def getTypeAbbreviation(self):
        return "t"


