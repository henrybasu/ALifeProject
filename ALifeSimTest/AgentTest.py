import random

class Agent(object):
    """An agent has a geneticString that governs its behavior, given by a string, and it has an amount of energy and a
    location on the agentMap (given when created and then updated)."""

    ARBITRARY_BEHAVIOR = "a" * 27

    def __init__(self, initPose = (0, 0, 'n'), initEnergy = 40, geneticString = "00000000", stepSpawned=0):
        """
        Sets up an agent with a location, energy, geneticString, and step created
        :param initLoc:   tuple giving agent's initial location
        :param initEnergy: integer initial energy
        :param geneticString: string to determine agent's behavior
        :param stepSpawned: integer giving the simulation step the agent was created in
        """
        self.row, self.col, self.heading = initPose
        self.geneticString = geneticString
        # self.whichScenarios = dict()
        self.stepSpawned = stepSpawned
        self.visObjectId = None
        self.isDead = False
        self.readyToBreed = 10

        """
        X0000000 - Vision
        0X000000 - Smell
        00X00000 - Movement
        000X0000 - Predator (0) or Prey (1)
        0000X000 - 
        00000X00 - Color
        000000XX - Energy
        """

        self.visionRange = int(self.geneticString[0])
        self.moveSpeed = int(self.geneticString[2])
        self.Aggression = int(self.geneticString[3])
        self.sleepValue = int(self.geneticString[4])
        self.color = int(self.geneticString[5])
        self.energy = int(self.geneticString[6:])

        self.score = 0


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
        return self.color

    def getAggression(self):
        return self.Aggression

    def getGeneticString(self):
        return self.geneticString

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
            return 'gray'

    def getPose(self):
        """Return the row, column, and heading of the agent."""
        return self.row, self.col, self.heading

    def getReadyToBreed(self):
        return self.readyToBreed

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
        return True

    def changeIsDead(self, deadVal):
        self.isDead = deadVal

    def changeReadyToBreed(self, breedVal):
        self.readyToBreed = self.readyToBreed - breedVal

    def setReadyToBreed(self, breedVal):
        self.readyToBreed = breedVal

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
        return self.chooseAction(behavIndex)


    def _assessEnergy(self):
        """Converts energy level into 0 for low, 1 for medium, and 2 for high amounts of energy."""
        if self.energy < 20:
            return 0
        elif self.energy < 60:
            return 1
        else:
            return 2


    def chooseAction(self, index):
        """
        Does the specified action.
        :param action: one of 's' for stay, 'f' for forward, 'l' for left, 'r' for right, or 'a' for arbitrary
        :return: returns the specified action, unless the action is 'a', in which case it picks an action at random.
        """
        if index in self.whichScenarios:
            self.whichScenarios[index] += 1
        else:
            self.whichScenarios[index] = 1
        action = 0
        if action == 'a':
            return random.choice(['eat', 'forward', 'left', 'right'])
        elif action == 's':
            return 'eat'
        elif action == 'f':
            return 'forward'
        elif action == 'l':
            return 'left'
        elif action == 'r':
            return 'right'
        else:
            print("action chosen: NONE(SHOULD NEVER GET HERE) --- choosing 'forward' as action")
            return 'forward'

        # action = self.geneticString[0]
        # for i in range(len(self.geneticString[0])):
        #     print("movement: " + str(i))
        #     return 'forward'

    def isAwake(self, sleepValue, time):
        if sleepValue == 0 and 6 <= time <= 18:
            return "awake"
        elif sleepValue == 1 and (time < 6 or time > 18):
            return "awake"
        else:
            return "sleeping"


    def determineAction(self, agent, isCreatureHere, isCreatureAhead, cellsSmelled, time):
        if self.isAwake(agent.sleepValue, time) == "awake":
            if agent.Aggression == 0:
                return self.determineActionDocile(agent, isCreatureHere, isCreatureAhead, cellsSmelled)
            elif agent.Aggression == 1:
                return self.determineActionAggressive(agent, isCreatureHere, isCreatureAhead, cellsSmelled)
            else:
                print("SHOULD NOT GET HERE")

        elif self.isAwake(agent.sleepValue, time) == "sleeping":
            return "none"


    def determineActionDocile(self, agent, isCreatureHere, isCreatureAhead, cellsSmelled):
        creaturesAround = cellsSmelled

        # if the agent is on the same square as a friend
        if isCreatureHere == 2:
            if agent.getReadyToBreed() == 0:
                return "breed"
            else:
                return random.choice(['left', 'right', 'turnAround', "forward"])

        # if the agent sees an enemy on a square ahead
        elif isCreatureAhead == 1:
            return random.choice(['left', 'right', 'turnAround'])

        # if the agent sees a friend ahead
        elif isCreatureAhead == 2:
            # if they are ready to breed, go forward
            if agent.getReadyToBreed() == 0:
                return "forward"
            # if they aren't, go anywhere
            else:
                return random.choice(['left', 'right', 'turnAround', "forward"])

        # if it can't see any creatures, and can't smell any creatures: go anywhere
        elif isCreatureAhead == 0 and creaturesAround == "none":
            return random.choice(['left', 'right', 'forward', 'forward', 'forward'])

        # if it can't see any creatures, and but it can smell creatures:
        elif isCreatureAhead == 0 and creaturesAround != "none":
            if creaturesAround[1] == 1:
                if creaturesAround[0] == "above":
                    return random.choice(['left', 'right', 'turnAround'])
                elif creaturesAround[0] == "left":
                    return random.choice(['right', 'forward', 'turnAround'])
                elif creaturesAround[0] == "right":
                    return random.choice(['left', 'forward', 'turnAround'])
                elif creaturesAround[0] == "below":
                    return random.choice(['left', 'right', 'forward'])
            elif creaturesAround[1] == 2 and agent.getReadyToBreed() == 0:
                if creaturesAround[0] == "above":
                    return "forward"
                elif creaturesAround[0] == "left":
                    return "left"
                elif creaturesAround[0] == "right":
                    return "right"
                elif creaturesAround[0] == "below":
                    return "turnAround"
            else:
                return random.choice(['left', 'right', 'forward', 'forward', 'forward'])

        else:
            print("action chosen: NONE(SHOULD NEVER GET HERE) --- choosing 'forward' as action")
            return 'forward'

    def determineActionAggressive(self, agent, isCreatureHere, isCreatureAhead, cellsSmelled):
        creaturesAround = cellsSmelled

        if isCreatureHere == 1:
            return "attack"

        # if the agent is on the same square as a friend
        elif isCreatureHere == 2:
            if agent.getReadyToBreed() == 0:
                return "breed"
            else:
                return random.choice(['left', 'right', 'turnAround', "forward"])

        elif isCreatureAhead == 1:
            return random.choice(['forward'])

        # if it can't see any creatures, and can't smell any creatures: go anywhere
        elif isCreatureAhead == 0 and creaturesAround == "none":
            return random.choice(['left', 'right', 'forward', 'forward', 'forward'])

        # if it can't see any creatures, and but it can smell any creatures:
        elif isCreatureAhead == 0 and creaturesAround != "none":

            if creaturesAround[1] == 1:
                if creaturesAround[0] == "above":
                    return random.choice(['forward'])
                elif creaturesAround[0] == "left":
                    return random.choice(['left'])
                elif creaturesAround[0] == "right":
                    return random.choice(['right'])
                elif creaturesAround[0] == "below":
                    return random.choice(['turnAround'])
            elif creaturesAround[1] == 2 and agent.getReadyToBreed() == 0:
                if creaturesAround[0] == "above":
                    return "forward"
                elif creaturesAround[0] == "left":
                    return "left"
                elif creaturesAround[0] == "right":
                    return "right"
                elif creaturesAround[0] == "below":
                    return "turnAround"
            else:
                return random.choice(['left', 'right', 'forward', 'forward', 'forward'])

        else:
            print("action chosen: NONE(SHOULD NEVER GET HERE) --- choosing 'forward' as action")
            return 'forward'


    def __str__(self):
        formStr = "Agent: {0:>3d}  {1:>3d}  {2:^3s}   {3:^6d}      {4}"
        return formStr.format(self.row, self.col, self.heading, self.energy, self.geneticString)