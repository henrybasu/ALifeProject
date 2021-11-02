

import random

class ALifeSim(object):
    """A simple simulated foodMap world, similar to NetLogo, with agents that each perform their own
    set of behaviors. Each cell of the foodMap has some amount of food on it, Food tends to occur
    in clusters. Each agent has a certain amount of health that is depleted a bit each time step,
    and that is depleted more if the agent moves. They can regain health by eating, up to a max amount."""

    FOOD_PERCENT = 0.10
    NEW_FOOD_PERCENT = 0.005
    GROWTH_RATE = 0.005
    MAX_FOOD = 20

    def __init__(self, gridSize, numAgents, rulesets = None, geneticString = None):
        """Takes in the side length of the foodMap, and makes the foodMap representation, and also the number
        of agents, who are randomly created and placed on the foodMap. Multiple agents per foodMap cell are allowed."""
        self.gridSize = gridSize
        self.numAgents = numAgents
        self.maxFood = 0
        self.foodMap = dict()
        self.agentMap = dict()
        for row in range(gridSize):
            for col in range(gridSize):
                self.foodMap[row, col] = 0
                self.agentMap[row, col] = []
        # self._placeFood()
        self.deadAgents = []
        self.agentList = []
        self.stepNum = 0

        for i in range(numAgents):
            agentPose = self._genRandomPose()
            r, c, h = agentPose

            if rulesets is None or len(rulesets) <= i:
                nextAgent = Agent(initPose = agentPose)
            else:
                nextAgent = Agent(ruleset=rulesets[i], initPose = agentPose)

            if geneticString is None:
                pass



            self.agentList.append(nextAgent)
            self.agentMap[r, c].append(nextAgent)

    def getSize(self):
        """Returns the size of the grid"""
        return self.gridSize


    def getAgentNumber(self):
        """Returns the number of agents placed on the grid"""
        return self.numAgents

    def getAgents(self):
        """Returns the list of agents"""
        return self.agentList[:]


    def foodAt(self, row, col):
        """Given a row and column, returns the amount of food at that location."""
        return self.foodMap[row, col]

    def agentsAt(self, row, col):
        """Given a row and column, returns a list of the agents at that location."""
        return self.agentMap[row, col]

    def _genRandomPose(self):
        """Generates a random location on the foodMap with equal probability."""
        row = random.randrange(self.gridSize)
        col = random.randrange(self.gridSize)
        heading = random.choice(['n', 'e', 'w', 's'])
        return (row, col, heading)

    def _genRandomLoc(self):
        """Generates a random location on the foodMap with equal probability."""
        row = random.randrange(self.gridSize)
        col = random.randrange(self.gridSize)
        return (row, col)


    def printGrid(self):
        """Prints the foodMap, giving each square 3 places"""
        rowLen = 5 * self.gridSize + 1
        cellStr = "{0:<4d}|"
        print("-" * rowLen)
        for row in range(self.gridSize):
            foodStr = "|"
            agInCellA = "|"
            agInCellB = "|"
            agInCellC = "|"
            for col in range(self.gridSize):
                sA, sB, sC = self._agentStringCodes(row, col)
                agInCellA += sA
                agInCellB += sB
                agInCellC += sC
                foodStr += cellStr.format(self.foodMap[row, col])
            print(foodStr)
            print(agInCellA)
            print(agInCellB)
            print(agInCellC)
            print("-" * rowLen)

    def _agentStringCodes(self, row, col):
        """Produces three strings for the first three agents (if that many) sitting in
        the given cell."""
        agentStr = "{0:s}{1:<3d}|"
        emptyStr = "    |"
        strings = [emptyStr, emptyStr, emptyStr]
        agentsHere = self.agentMap[row, col]
        for i in range(3):
            if len(agentsHere) > i:
                agent = agentsHere[i]
                (r, c, h) = agent.getPose()
                en = agent.getEnergy()
                strings[i] = agentStr.format(h, en)
        return strings


    def printAgents(self):
        """Prints the current location, heading, and energy of each agent."""
        print("===== Live Agents =====")
        print("       Row  Col  Hed   Energy")
        for agent in self.agentList:
            print(agent)
        print("===== Dead Agents =====")
        print("       Row  Col  Hed   Energy")
        for agent,step in self.deadAgents:
            print(agent, "died in step", step)


    def getDeadAgents(self):
        """Returns a list of the dead agents."""
        return self.deadAgents


    def step(self):
        """Update one step of the simulation. This means growing food, and then updating each agent
        with its chosen behavior. That could also mean managing agents who "die" because they run out
        of energy."""
        self.stepNum += 1
        self._updateAgents()


    def _updateAgents(self):
        """Updates the position and energy of every agent based on its chosen action."""
        i = 0
        while i < len(self.agentList):
            agent = self.agentList[i]
            agentR, agentC, agentH = agent.getPose()
            rAhead, cAhead = self._computeAhead(agentR, agentC, agentH)



    # TODO: Change this
    def _computeAhead(self, row, col, heading):
        """Determine the cell that is one space ahead of current cell, given the heading."""
        if heading == 'n':   # agent is pointing north, row value decreases
            newR = (row - 1) % self.gridSize
            return newR, col
        elif heading == 's':  # agent is pointing south, row value increases
            newR = (row + 1) % self.gridSize
            return newR, col
        elif heading == 'w':  # agent is pointing west, col value decreases
            newC = (col - 1) % self.gridSize
            return row, newC
        else:  # agent is pointing east, col value increases
            newC = (col + 1) % self.gridSize
            return row, newC


    def _leftTurn(self, heading):
        """return the new heading for a left turn"""
        if heading == 'n':
            return 'w'
        elif heading == 'w':
            return 's'
        elif heading == 's':
            return 'e'
        else:
            return 'n'

    def _rightTurn(self, heading):
        """return the new heading for a right turn"""
        if heading == 'n':
            return 'e'
        elif heading == 'e':
            return 's'
        elif heading == 's':
            return 'w'
        else:
            return 'n'



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

    def __init__(self, ruleset = None, initPose = (0, 0, 'n'), initEnergy = 40, geneticString="0000000000"):
        """
        Sets up an agent with a ruleset, location, and energ
        :param ruleset:   string describing behaviors of agent in different scenarios
        :param initLoc:   tuple giving agent's initial location
        :param initEnergy: integer initial energy
        """
        self.row, self.col, self.heading = initPose
        self.whichScenarios = dict()
        self.energy = initEnergy
        self.visObjectId = None

        self.visionRange = geneticString[0]

        if ruleset is None:
            self.ruleset = self.ARBITRARY_BEHAVIOR
        else:
            self.ruleset = ruleset

        if geneticString is None:
            self.geneticString = "123456789"
            print(self.geneticString)

    def setVisId(self, id):
        """Set the tkinter id so the object knows it"""
        self.visObjectId = id


    def getVisId(self):
        """return the tkinter object id"""
        return self.visObjectId


    def getEnergy(self):
        """Returns the current energy value"""
        return self.energy

    def getPose(self):
        """Return the row, column, and heading of the agent."""
        return self.row, self.col, self.heading

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

    def respond(self, foodHere, foodAhead):
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
        action = self.ruleset[index]
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
            print("SHOULD NEVER GET HERE")
            return 'eat'

        # action = self.geneticString[0]
        #
        # for i in range(len(self.geneticString[0])):
        #     print("movement: " + str(i))
        #     return 'forward'

    def __str__(self):
        formStr = "Agent: {0:>3d}  {1:>3d}  {2:^3s}   {3:^6d}"
        return formStr.format(self.row, self.col, self.heading, self.energy)


    def getFirstValue(self, geneticString):
        return self.geneticString[0]


if __name__ == '__main__':
    sim = ALifeSim(50, 20)
    for rounds in range(5):
        print("Round", rounds)
        sim.printGrid()
        sim.printAgents()
        sim.step()
    totalScenarios = dict()
    for i in range(27):
        totalScenarios[i] = 0
    for agents, when in sim.getDeadAgents():
        for val in agents.whichScenarios:
            totalScenarios[val] += agents.whichScenarios[val]
    for agents in sim.agentList:
        for val in agents.whichScenarios:
            totalScenarios[val] += agents.whichScenarios[val]
    vals = list(totalScenarios.keys())
    vals.sort()
    for val in vals:
        print(val, totalScenarios[val])


