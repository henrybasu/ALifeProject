from Object import Object
import random

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
        # self.stepsUntilBloom = random.randint(5,40)
        self.stepsUntilBloom = 500


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

    def __str__(self):
        formStr = "Tree: row={5}  col={0:>3d}, hasFood={1:>3d}, stepsSpawned={2:^3s})   justChanged={3:^6d}     stepsUntilBloom={4}"
        return formStr.format(self.row, self.col, self.hasFood, self.stepSpawned, self.justChanged, self.stepsUntilBloom)


