from Object import Object

class Food(Object):
    """A food object in the ALife simulation."""
    def __init__(self, initPose = (0, 0), geneticString = "0", stepSpawned=0):
        """
        Sets up food with a location, geneticString, and step created
        :param initPose: tuple giving food's initial location
        :param geneticString: string giving information about the food
        :param stepSpawned: integer giving the simulation step the food was created in
        """
        super().__init__()
        self.geneticString = geneticString
        self.row, self.col = initPose
        self.stepSpawned = stepSpawned

    def __str__(self):
        """Information about the food to print."""
        formStr = "Food: {0:>3d}  {1:>3d}  {2}"
        return formStr.format(self.row, self.col, self.geneticString)

    def getTypeAbbreviation(self):
        """Returns the abbreviation for a food object, "f"."""
        return "f"
