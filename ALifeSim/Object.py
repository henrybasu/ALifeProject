class Object(object):
    """A template to represent any object in the ALife simulation."""

    def __init__(self, initPose = (0, 0), geneticString = "", stepSpawned=0):
        """
        Sets up an object with a location, geneticString, and step created
        :param initLoc: tuple giving object's initial location
        :param geneticString: string giving the object's genetic string
        :param stepSpawned: integer giving the simulation step the object was created in
        """
        self.row, self.col = initPose
        self.geneticString = geneticString
        self.stepSpawned = stepSpawned
        self.visObjectId = None
        self.color = ""

    def getColor(self):
        """Returns the objects color value."""
        return self.color

    def setVisId(self, id):
        """Sets the tkinter id so the object knows it."""
        self.visObjectId = id

    def getVisId(self):
        """Returns the tkinter object id."""
        return self.visObjectId

    def colorNumberToText(self, color):
        """Returns the text corresponding to the object's color."""
        if color == 1:
            return 'black'
        elif color == 2:
            return 'red'
        elif color == 3:
            return 'orange'
        elif color == 4:
            return 'yellow'
        elif color == 5:
            return 'blue'
        elif color == 6:
            return 'green'
        elif color == 7:
            return 'purple'
        elif color == 8:
            return 'brown'
        elif color == 9:
            return 'pink'
        elif color == 0:
            return 'gray'

    def getPose(self):
        """Returns the row and column of the object."""
        return self.row, self.col

    def __str__(self):
        """Information about the object to print."""
        formStr = "Object: {0:>3d}  {1:>3d}  {2}"
        return formStr.format(self.row, self.col, self.geneticString)