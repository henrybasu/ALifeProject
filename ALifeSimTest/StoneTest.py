from ObjectTest import Object

class Stone(Object):
    """A stone object in the ALife simulation."""

    def __init__(self, initPose = (0, 0), geneticString = "00", stepSpawned=0):
        """
        Sets up an agent with a location, energy, geneticString, and step created
        :param initLoc: tuple giving object's initial location
        :param geneticString: string giving the object's type and color classifications
        :param stepSpawned: integer giving the simulation step the object was created in
        """
        super().__init__()
