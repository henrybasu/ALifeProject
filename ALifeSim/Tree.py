from Object import Object
import random

class Tree(Object):
    """A tree object in the ALife simulation."""

    def __init__(self, initPose = (0, 0), geneticString = "0", stepSpawned=0):
        """
        Sets up tree with a location, geneticString, and step created
        :param initPose: tuple giving tree's initial location
        :param geneticString: string giving information about the tree
        :param stepSpawned: integer giving the simulation step the tree was created in
        """
        super().__init__()
        self.geneticString = geneticString
        self.row,self.col = initPose
        self.stepSpawned = stepSpawned

        self.hasFood = geneticString[0]
        self.justChanged = False
        self.stepsUntilBloom = random.randint(5,40)
        # self.stepsUntilBloom = 500
        
    def getHasFood(self):
        """Returns 0 if the tree currently has no food, 1 if the tree currently has food."""
        return self.hasFood

    def setHasFood(self, newCanGrowFood):
        """Sets the hasFood attribute, and if it is a new value, marks the tree's justChanged attribute to True."""
        if (self.hasFood != newCanGrowFood):
            self.justChanged = True
        self.hasFood = newCanGrowFood

    def setJustChangedBloom(self, newVal):
        """Sets the tree's justChanged attribute."""
        self.justChanged = newVal

    def getStepsUntilBloom(self):
        """Returns the # of simulation steps until the tree blooms."""
        return self.stepsUntilBloom

    def setStepsUntilBloom(self, newVal):
        """Sets the number of simulation steps until the tree blooms."""
        self.stepsUntilBloom = newVal

    def getTypeAbbreviation(self):
        """Returns the abbreviation for a tree object, "t"."""
        return "t"

    def __str__(self):
        """Information about the tree to print."""
        formStr = "Tree: row={5}  col={0:>3d}, hasFood={1:>3d}, stepsSpawned={2:^3s})   justChanged={3:^6d}     stepsUntilBloom={4}"
        return formStr.format(self.row, self.col, self.hasFood, self.stepSpawned, self.justChanged, self.stepsUntilBloom)


