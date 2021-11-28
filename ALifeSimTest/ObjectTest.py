class Object(object):
    """A template to represent a non-living object in the ALife simulation."""

    def __init__(self, initPose = (0, 0), geneticString = "00", stepSpawned=0):
        """
        Sets up an agent with a location, energy, geneticString, and step created
        :param initLoc: tuple giving object's initial location
        :param geneticString: string giving the object's type and color classifications
        :param stepSpawned: integer giving the simulation step the object was created in
        """
        self.row, self.col = initPose
        self.geneticString = geneticString
        self.stepSpawned = stepSpawned
        self.visObjectId = None

        """
        X0 - object type (ex. tree) 
        0X - color
        """
        """
        objectType key: 
        1 - block w/ height=1
        2 - water
        3 - food
        4 - 
        5 - 
        """

        self.objectType = int(self.geneticString[0])
        self.color = int(self.geneticString[1])


    def setVisId(self, id):
        """Set the tkinter id so the object knows it"""
        self.visObjectId = id

    def getVisId(self):
        """return the tkinter object id"""
        return self.visObjectId

    def getColor(self):
        return self.color

    def colorNumberToText(self, color):
        """Returns the text value of the object's color"""
        if color == 1:
            return 'black'
        elif color == 2:
            return 'black'
        elif color == 3:
            return 'black'
        elif color == 4:
            return 'black'
        elif color == 5:
            return 'black'
        elif color == 6:
            return 'black'
        elif color == 7:
            return 'black'
        elif color == 8:
            return 'black'
        elif color == 9:
            return 'black'
        elif color == 0:
            return 'black'

    def getPose(self):
        """Return the row and column of the agent."""
        return self.row, self.col

    def determineAction(self):
          return


    def __str__(self):
        formStr = "Object: {0:>3d}  {1:>3d}  {2}"
        return formStr.format(self.row, self.col, self.geneticString)