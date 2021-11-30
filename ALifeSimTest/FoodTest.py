from ObjectTest import Object

class Food(Object):
    """A stone object in the ALife simulation."""

    def __init__(self, initPose = (0, 0), geneticString = "0", stepSpawned=0):
        """
        Sets up an agent with a location, energy, geneticString, and step created
        :param initPose: tuple giving stone's initial location
        :param geneticString: string giving the stone's color
        :param stepSpawned: integer giving the simulation step the stone was created in
        """
        super().__init__()
        self.geneticString = geneticString

    def __str__(self):
        formStr = "Food: {0:>3d}  {1:>3d}  {2}"
        return formStr.format(self.row, self.col, self.geneticString)
