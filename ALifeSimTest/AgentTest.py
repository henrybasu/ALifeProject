import random

class Agent(object):
    """An agent has a ruleset that governs its behavior, given by a string (random behavior is the
    default), and it has an amount of energy and a location on the foodMap (given when created and then updated).

    Agent behavior: The agent can see the cell it is on, plus the cell ahead of it.
    It can distinguish three values on each cell: no food, a little bit of food, and plentiful food.

    It also can evaluate its own energy level: low, medium, high and incorporate that into its decision-making.

    That gives it 27 different scenarios (3 for food here * 3 for food ahead * 3 for energy level).

    For each scenario the agent has five possible behaviors: stay, move, left, right, and random.
    If the agent "stays", then it doesn't move or turn, and if there ss food here the agent will eat.
    If the agent "moves", then it doesn't eat, it moves forward one square in the direction it is facing.
    If the agent does "left", then it stays put, doesn't eat, but turns left in place.
    If the agent does "right", then it stays put, doesn't eat, but turns right in place.
    If the agent does "arbitrary", then it randomly chooses one of the other actions, all equally likely."""

    ARBITRARY_BEHAVIOR = "a" * 27

    def __init__(self, initPose = (0, 0, 'n'), initEnergy = 40, geneticString = "00000000"):
        """
        Sets up an agent with a ruleset, location, and energy
        :param ruleset:   string describing behaviors of agent in different scenarios
        :param initLoc:   tuple giving agent's initial location
        :param initEnergy: integer initial energy
        """
        self.geneticString = geneticString
        self.row, self.col, self.heading = initPose
        self.whichScenarios = dict()
        self.visObjectId = None

        self.visionRange = int(self.geneticString[0])
        self.moveSpeed = int(self.geneticString[2])
        self.Aggression = int(self.geneticString[3])
        self.sleepValue = int(self.geneticString[4])
        self.color = int(self.geneticString[5])
        self.energy = int(self.geneticString[6:7])

        self.score = 0

        """
        X0000000 - Vision
        0X000000 - Smell
        00X00000 - Movement Speed
        000X0000 - Predator (0) or Prey (1)
        0000X000 - Sleep Type
        00000X00 - Color
        000000XX - Energy
        """


    def setVisId(self, id):
        """Set the tkinter id so the object knows it"""
        self.visObjectId = id


    def getVisId(self):
        """return the tkinter object id"""
        return self.visObjectId


    def getEnergy(self):
        """Returns the current energy value"""
        return self.energy


    def getColor(self):
        "Returns the agent's color as a digit 0-9"
        return self.color


    def getGeneticString(self):
        """Returns the agent's genetic string"""
        return self.geneticString


    def getPose(self):
        """Return the row, column, and heading of the agent."""
        return self.row, self.col, self.heading


    def colorNumberToText(self, color):
        """Returns the text value of the agent's color"""
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
            return 'teal'


    def updatePose(self, row, col, heading):
        """Updates the agent's pose to a new position and heading"""
        self.row = row
        self.col = col
        self.heading = heading


    def changeEnergy(self, changeVal):
        """Changes the energy value by adding changeVal to it, reports back if the value goes to zero
        or below: the agent "dies" in that case."""
        self.energy += changeVal
        if self.energy <= 0:
            return False
        print(self.energy)
        return True


    def respond(self, foodHere, foodAhead, creatureHere, creatureAhead):
        """
        This performs the action the rules would require, given how much food is here and food ahead, and
        the internal energy level
        :param foodHere: 0, 1, or 2, where 0 = no food, 1 = some food, 2 = plentiful food
        :param foodAhead: same as foodHere, but for cell ahead of agent
        :return: None
        """
        eLevel = self._assessEnergy()
        behavIndex = (3 ** 2) * foodHere + 3 * foodAhead + eLevel
        # return self.chooseAction(behavIndex)
        #TODO: Change this to use determineAction instead of chooseAction (chooseAction no longer exists)


    def _assessEnergy(self):
        """Converts energy level into 0 for low, 1 for medium, and 2 for high amounts of energy."""
        if self.energy < 20:
            return 0
        elif self.energy < 60:
            return 1
        else:
            return 2


    def determineAction(self, agent, isCreatureHere, isCreatureAhead, cellsSmelled, time):
        if self.isAwake(agent.sleepValue, time) == "awake":
            if agent.Aggression == 0:
                return self.determineActionDocile(agent, isCreatureAhead, cellsSmelled)
            elif agent.Aggression == 1:
                return self.determineActionAggressive(agent, isCreatureHere, isCreatureAhead, cellsSmelled)
            else:
                print("SHOULD NOT GET HERE")

        elif self.isAwake(agent.sleepValue, time) == "sleeping":
            return "none"


    def determineActionDocile(self, agent, isCreatureAhead, cellsSmelled):
        creaturesAround = cellsSmelled

        if isCreatureAhead == 1:
            return random.choice(['left', 'right', 'turnAround'])

        # if it can't see any creatures, and can't smell any creatures: go forwards
        elif isCreatureAhead == 0 and creaturesAround == "none":
            return random.choice(['left', 'right', 'forward', 'forward', 'forward'])

        # if it can't see any creatures, and but it can smell any creatures:
        elif isCreatureAhead == 0 and creaturesAround != "none":
            if creaturesAround == "above":
                return random.choice(['left', 'right', 'turnAround'])
            elif creaturesAround == "left":
                return random.choice(['right', 'forward', 'turnAround'])
            elif creaturesAround == "right":
                return random.choice(['left', 'forward', 'turnAround'])
            elif creaturesAround == "below":
                return random.choice(['left', 'right', 'forward'])

        else:
            print("action chosen: NONE(SHOULD NEVER GET HERE) --- choosing 'forward' as action")
            return 'forward'

    def determineActionAggressive(self, agent, isCreatureHere, isCreatureAhead, cellsSmelled):
        creaturesAround = cellsSmelled

        if isCreatureHere == 1:
            return "attack"

        elif isCreatureAhead == 1:
            return random.choice(['forward'])

        # if it can't see any creatures, and can't smell any creatures: go forwards
        elif isCreatureAhead == 0 and creaturesAround == "none":
            return random.choice(['left', 'right', 'forward', 'forward', 'forward'])

        # if it can't see any creatures, and but it can smell any creatures:
        elif isCreatureAhead == 0 and creaturesAround != "none":
            if creaturesAround == "above":
                return random.choice(['forward'])
            elif creaturesAround == "left":
                return random.choice(['left'])
            elif creaturesAround == "right":
                return random.choice(['right'])
            elif creaturesAround == "below":
                return random.choice(['turnAround'])

        else:
            print("action chosen: NONE(SHOULD NEVER GET HERE) --- choosing 'forward' as action")
            return 'forward'


    def isAwake(self, sleepValue, time):
        if sleepValue == 0 and 6 <= time <= 18:
            return "awake"
        elif sleepValue == 1 and (time < 6 or time > 18):
            return "awake"
        else:
            return "sleeping"


    def __str__(self):
        formStr = "Agent: {0:>3d}  {1:>3d}  {2:^3s}   {3:^6d}"
        return formStr.format(self.row, self.col, self.heading, self.energy)
