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
        self.typeOfMushroom = int(self.geneticString[0])
        """
        Types of Mushroom:
        0 - Is the same as food
        1 - Makes sick
        2 - Paralyzes
        3 - Causes random movement
        4 - Takes energy
        """
        self.droppingType = 1
        self.justChanged = False
        self.stepsUntilGrowth = 5

    def getDroppingType(self):
        """Returns 0 if the tree currently has no food, 1 if the tree currently has food."""
        return self.droppingType

    def setDroppingType(self, newDroppingType):
        """Sets the hasFood attribute, and if it is a new value, marks the tree's justChanged attribute to True."""
        if (self.droppingType != newDroppingType):
            self.justChanged = True
        self.droppingType = newDroppingType

    def setJustChanged(self, newVal):
        """Sets the tree's justChanged attribute."""
        self.justChanged = newVal

    def getStepsUntilGrowth(self):
        """Returns the # of simulation steps until the tree blooms."""
        return self.stepsUntilGrowth

    def setStepsUntilGrowth(self, newVal):
        """Sets the number of simulation steps until the tree blooms."""
        self.stepsUntilGrowth = newVal

    def getTypeAbbreviation(self):
        """Returns the abbreviation for a mushroom object, "m"."""
        return "m"

    def getTypeOfMushroom(self):
        """Returns an integer for the type of mushroom."""
        return self.typeOfMushroom

    def setTypeOfMushroom(self, newVal):
        """Sets the type of this mushroom."""
        self.typeOfMushroom = newVal



