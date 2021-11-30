import random
from ObjectTest import Object

class Agent(Object):
    """An agent object in the ALife simulation. An agent has a geneticString that governs its behavior, given by
    a string, and it has an amount of energy and a location on the agentMap (given when created and then updated)."""

    def __init__(self, initPose = (0, 0, 'n'), initEnergy = 40, geneticString = "00000000", stepSpawned=0):
        """
        Sets up an agent with a location, energy, geneticString, and step created
        :param initPose:   tuple giving agent's initial location
        :param initEnergy: integer initial energy
        :param geneticString: string to determine agent's behavior
        :param stepSpawned: integer giving the simulation step the agent was created in
        """
        super().__init__()
        self.row, self.col, self.heading = initPose
        self.geneticString = geneticString
        # self.whichScenarios = dict()
        # self.stepSpawned = stepSpawned
        # self.visObjectId = None
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
        # self.score = 0

    def getEnergy(self):
        """Returns the current energy value"""
        return self.energy

    def getAggression(self):
        return self.Aggression

    def getGeneticString(self):
        return self.geneticString

    def getPose(self):
        """Return the row, column, and heading of the agent."""
        return self.row, self.col, self.heading

    def getReadyToBreed(self):
        return self.readyToBreed

    def updatePose(self, newRow, newCol, newHeading):
        """Updates the agent's pose to a new position and heading"""
        self.row = newRow
        self.col = newCol
        self.heading = newHeading

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


    def isAwake(self, sleepValue, time):
        if sleepValue == 0 and 6 <= time <= 18:
            return "awake"
        elif sleepValue == 1 and (time < 6 or time > 18):
            return "awake"
        else:
            return "sleeping"


    def _computeAhead(self, gridSize):
        row, col, heading = self.getPose()
        moveSpeed = self.moveSpeed
        """Determine the cell that is one space ahead of current cell, given the heading."""
        if heading == 'n':   # agent is pointing north, row value decreases
            newR = (row - moveSpeed) % gridSize
            return newR, col
        elif heading == 's':  # agent is pointing south, row value increases
            newR = (row + moveSpeed) % gridSize
            return newR, col
        elif heading == 'w':  # agent is pointing west, col value decreases
            newC = (col - moveSpeed) % gridSize
            return row, newC
        else:  # agent is pointing east, col value increases
            newC = (col + moveSpeed) % gridSize
            return row, newC

    def _areCreaturesInVision(self, sim):
        ownY, ownX, heading = self.getPose()
        visionList = []

        if heading == "n":
            for i in range(int(self.visionRange)):
                visionList.append(sim._assessCreature((ownY - (int(self.geneticString[0]) - i)) % sim.gridSize, ownX, self))
                # if visionList[i] != 0:
                #     return 1
                return visionList[i]

        elif heading == "s":
            for i in range(int(self.visionRange)):
                visionList.append(sim._assessCreature((ownY + i + 1) % sim.gridSize, ownX, self))
                # if visionList[i] != 0:
                #     return 1
                return visionList[i]

        elif heading == "e":
            for i in range(int(self.visionRange)):
                visionList.append(sim._assessCreature(ownY, (ownX + i + 1) % sim.gridSize, self))
                # if visionList[i] != 0:
                #     return 1
                return visionList[i]

        elif heading == "w":
            for i in range(int(self.visionRange)):
                visionList.append(sim._assessCreature(ownY, (ownX - (int(self.geneticString[0]) - i)) % sim.gridSize, self))
                # if visionList[i] != 0:
                #     return 1
                return visionList[i]

        # print("DON't SEE ANYONE")
        return 0

    def smellRadius1(self, sim):
        ownY, ownX, heading = self.getPose()
        cellsSmelled = []

        cellAbove = sim._assessCreature((ownY - 1) % sim.gridSize, ownX, self)
        cellBelow = sim._assessCreature((ownY + 1) % sim.gridSize, ownX, self)
        cellRight = sim._assessCreature(ownY, (ownX + 1) % sim.gridSize, self)
        cellLeft = sim._assessCreature(ownY, (ownX - 1) % sim.gridSize, self)

        cellsSmelled.append(cellAbove)
        cellsSmelled.append(cellBelow)
        cellsSmelled.append(cellRight)
        cellsSmelled.append(cellLeft)

        return cellsSmelled

    def smellRadius2(self, sim):
        ownY, ownX, heading = self.getPose()
        cellsSmelled = []

        cellAbove = sim._assessCreature((ownY - 1) % sim.gridSize, ownX, self)
        cellBelow = sim._assessCreature((ownY + 1) % sim.gridSize, ownX, self)
        cellRight = sim._assessCreature(ownY, (ownX + 1) % sim.gridSize, self)
        cellLeft = sim._assessCreature(ownY, (ownX - 1) % sim.gridSize, self)

        cellTwoAbove = sim._assessCreature((ownY - 2) % sim.gridSize, ownX, self)
        cellTwoBelow = sim._assessCreature((ownY + 2) % sim.gridSize, ownX, self)
        cellTwoRight = sim._assessCreature(ownY, (ownX + 2) % sim.gridSize, self)
        cellTwoLeft = sim._assessCreature(ownY, (ownX - 2) % sim.gridSize, self)

        cellAboveLeft = sim._assessCreature((ownY - 1) % sim.gridSize, (ownX - 1) % sim.gridSize, self)
        cellAboveRight = sim._assessCreature((ownY - 1) % sim.gridSize, (ownX + 1) % sim.gridSize, self)
        cellBelowRight = sim._assessCreature((ownY + 1) % sim.gridSize, (ownX + 1) % sim.gridSize, self)
        cellBelowLeft = sim._assessCreature((ownY + 1) % sim.gridSize, (ownX - 1) % sim.gridSize, self)

        cellsSmelled.append(cellAbove)
        cellsSmelled.append(cellBelow)
        cellsSmelled.append(cellRight)
        cellsSmelled.append(cellLeft)

        cellsSmelled.append(cellTwoAbove)
        cellsSmelled.append(cellTwoBelow)
        cellsSmelled.append(cellTwoRight)
        cellsSmelled.append(cellTwoLeft)

        cellsSmelled.append(cellAboveLeft)
        cellsSmelled.append(cellAboveRight)
        cellsSmelled.append(cellBelowLeft)
        cellsSmelled.append(cellBelowRight)

        return cellsSmelled

    def areCreaturesInSmellRadius(self, sim):
        ownY, ownX, heading = self.getPose()
        smellRadius = self.geneticString[1]

        # actions for if the agent has a smell radius of 1
        if int(smellRadius) == 1:
            cellsSmelled = self.smellRadius1(sim)

            if cellsSmelled[0] != 0 and heading == "n":
                return "above", cellsSmelled[0]
            elif cellsSmelled[1] != 0 and heading == "n":
                return "below", cellsSmelled[1]
            elif cellsSmelled[2] != 0 and heading == "n":
                return "right", cellsSmelled[2]
            elif cellsSmelled[3] != 0 and heading == "n":
                return "left", cellsSmelled[3]

            elif cellsSmelled[0] != 0 and heading == "s":
                return "below", cellsSmelled[0]
            elif cellsSmelled[1] != 0 and heading == "s":
                return "above", cellsSmelled[1]
            elif cellsSmelled[2] != 0 and heading == "s":
                return "left", cellsSmelled[2]
            elif cellsSmelled[3] != 0 and heading == "s":
                return "right", cellsSmelled[3]

            elif cellsSmelled[0] != 0 and heading == "e":
                return "left", cellsSmelled[0]
            elif cellsSmelled[1] != 0 and heading == "e":
                return "right", cellsSmelled[1]
            elif cellsSmelled[2] != 0 and heading == "e":
                return "above", cellsSmelled[2]
            elif cellsSmelled[3] != 0 and heading == "e":
                return "below", cellsSmelled[3]

            elif cellsSmelled[0] != 0 and heading == "w":
                return "right", cellsSmelled[0]
            elif cellsSmelled[1] != 0 and heading == "w":
                return "left", cellsSmelled[1]
            elif cellsSmelled[2] != 0 and heading == "w":
                return "below", cellsSmelled[2]
            elif cellsSmelled[3] != 0 and heading == "w":
                return "above", cellsSmelled[3]
            else:
                return "none"

        elif int(smellRadius) == 2:
            cellsSmelled = self.smellRadius2(sim)
            if cellsSmelled[0] != 0 and heading == "n":
                return "above", cellsSmelled[0]
            elif cellsSmelled[1] != 0 and heading == "n":
                return "below", cellsSmelled[1]
            elif cellsSmelled[2] != 0 and heading == "n":
                return "right", cellsSmelled[2]
            elif cellsSmelled[3] != 0 and heading == "n":
                return "left", cellsSmelled[3]

            elif cellsSmelled[0] != 0 and heading == "s":
                return "below", cellsSmelled[0]
            elif cellsSmelled[1] != 0 and heading == "s":
                return "above", cellsSmelled[1]
            elif cellsSmelled[2] != 0 and heading == "s":
                return "left", cellsSmelled[2]
            elif cellsSmelled[3] != 0 and heading == "s":
                return "right", cellsSmelled[3]

            elif cellsSmelled[0] != 0 and heading == "e":
                return "left", cellsSmelled[0]
            elif cellsSmelled[1] != 0 and heading == "e":
                return "right", cellsSmelled[1]
            elif cellsSmelled[2] != 0 and heading == "e":
                return "above", cellsSmelled[2]
            elif cellsSmelled[3] != 0 and heading == "e":
                return "below", cellsSmelled[3]

            elif cellsSmelled[0] != 0 and heading == "w":
                return "right", cellsSmelled[0]
            elif cellsSmelled[1] != 0 and heading == "w":
                return "left", cellsSmelled[1]
            elif cellsSmelled[2] != 0 and heading == "w":
                return "below", cellsSmelled[2]
            elif cellsSmelled[3] != 0 and heading == "w":
                return "above", cellsSmelled[3]

            elif (cellsSmelled[4] != 0) and heading == "n":
                return "above", cellsSmelled[4]
            elif (cellsSmelled[5] != 0) and heading == "n":
                return "below", cellsSmelled[5]
            elif (cellsSmelled[6] != 0) and heading == "n":
                return "right", cellsSmelled[6]
            elif (cellsSmelled[7] != 0) and heading == "n":
                return "left", cellsSmelled[7]

            elif (cellsSmelled[4] != 0) and heading == "s":
                return "below", cellsSmelled[4]
            elif (cellsSmelled[5] != 0) and heading == "s":
                return "above", cellsSmelled[5]
            elif (cellsSmelled[6] != 0) and heading == "s":
                return "left", cellsSmelled[6]
            elif (cellsSmelled[7] != 0) and heading == "s":
                return "right", cellsSmelled[7]

            elif (cellsSmelled[4] != 0) and heading == "e":
                return "left", cellsSmelled[4]
            elif (cellsSmelled[5] != 0) and heading == "e":
                return "right", cellsSmelled[5]
            elif (cellsSmelled[6] != 0) and heading == "e":
                return "above", cellsSmelled[6]
            elif (cellsSmelled[7] != 0) and heading == "e":
                return "below", cellsSmelled[7]

            elif (cellsSmelled[4] != 0) and heading == "w":
                return "right", cellsSmelled[4]
            elif (cellsSmelled[5] != 0) and heading == "w":
                return "left", cellsSmelled[5]
            elif (cellsSmelled[6] != 0) and heading == "w":
                return "below", cellsSmelled[6]
            elif (cellsSmelled[7] != 0) and heading == "w":
                return "above", cellsSmelled[7]

            elif cellsSmelled[8] != 0 and heading == "n":
                return random.choice(["above", "left"]), cellsSmelled[8]
            elif cellsSmelled[9] != 0 and heading == "n":
                return random.choice(["above", "right"]), cellsSmelled[9]
            elif cellsSmelled[10] != 0 and heading == "n":
                return random.choice(["below", "left"]), cellsSmelled[10]
            elif cellsSmelled[11] != 0 and heading == "n":
                return random.choice(["below", "right"]), cellsSmelled[11]

            elif cellsSmelled[8] != 0 and heading == "s":
                return random.choice(["below", "right"]), cellsSmelled[8]
            elif cellsSmelled[9] != 0 and heading == "s":
                return random.choice(["below", "left"]), cellsSmelled[9]
            elif cellsSmelled[10] != 0 and heading == "s":
                return random.choice(["above", "right"]), cellsSmelled[10]
            elif cellsSmelled[11] != 0 and heading == "s":
                return random.choice(["above", "left"]), cellsSmelled[11]

            elif cellsSmelled[8] != 0 and heading == "e":
                return random.choice(["below", "left"]), cellsSmelled[8]
            elif cellsSmelled[9] != 0 and heading == "e":
                return random.choice(["above", "left"]), cellsSmelled[9]
            elif cellsSmelled[10] != 0 and heading == "e":
                return random.choice(["below", "right"]), cellsSmelled[10]
            elif cellsSmelled[11] != 0 and heading == "e":
                return random.choice(["above", "right"]), cellsSmelled[11]

            elif cellsSmelled[8] != 0 and heading == "w":
                return random.choice(["above", "right"]), cellsSmelled[8]
            elif cellsSmelled[9] != 0 and heading == "w":
                return random.choice(["below", "right"]), cellsSmelled[9]
            elif cellsSmelled[10] != 0 and heading == "w":
                return random.choice(["above", "left"]), cellsSmelled[10]
            elif cellsSmelled[11] != 0 and heading == "w":
                return random.choice(["below", "left"]), cellsSmelled[11]

            else:
                return "none"

        else:
            return "none"

    def _leftTurn(self):
        """return the new heading for a left turn"""
        r,c,heading = self.getPose()
        if heading == 'n':
            return 'w'
        elif heading == 'w':
            return 's'
        elif heading == 's':
            return 'e'
        else:
            return 'n'

    def _rightTurn(self):
        """return the new heading for a right turn"""
        r, c, heading = self.getPose()
        if heading == 'n':
            return 'e'
        elif heading == 'e':
            return 's'
        elif heading == 's':
            return 'w'
        else:
            return 'n'

    def _turnAround(self):
        """return the new heading for turning around"""
        r, c, heading = self.getPose()
        if heading == 'n':
            return 's'
        elif heading == 'e':
            return 'w'
        elif heading == 's':
            return 'n'
        elif heading == 'w':
            return 'e'
        else:
            return 'BROKEN'

    def attackCreature(self, sim, row, col):
        for j in range(len(sim.agentsAt(row, col))):
            if int(sim.agentsAt(row, col)[j].getColor()) != self.getColor():
                deadCreature = sim.agentsAt(row, col)[j]
                deadCreature.changeEnergy(-100)
                deadCreature.isDead = True

    def determineAction(self, agent, isCreatureHere, isCreatureAhead, cellsSmelled, time, isFoodHere):
        if self.isAwake(agent.sleepValue, time) == "awake":
            if agent.Aggression == 0:
                return self.determineActionDocile(agent, isCreatureHere, isCreatureAhead, cellsSmelled, isFoodHere)
            elif agent.Aggression == 1:
                return self.determineActionAggressive(agent, isCreatureHere, isCreatureAhead, cellsSmelled)
            else:
                print("SHOULD NOT GET HERE")

        elif self.isAwake(agent.sleepValue, time) == "sleeping":
            return "none"


    def determineActionDocile(self, agent, isCreatureHere, isCreatureAhead, cellsSmelled, isFoodHere):
        creaturesAround = cellsSmelled
        # print("Creatures around: " + str(creaturesAround))

        # if the agent is on the same square as a friend
        if isCreatureHere == 2:
            if agent.getReadyToBreed() == 0:
                return "breed"
            else:
                return random.choice(['left', 'right', 'turnAround', "forward"])

        elif len(isFoodHere) > 0:
            return "eat"

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
            elif (creaturesAround[1] == 2 and agent.getReadyToBreed()) or creaturesAround[1] == 3:
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

    def _printVision(self, sim):
        ownY, ownX, heading = self.getPose()
        visionList = []

        if heading == "n":
            for i in range(int(self.geneticString[0])):
                visionList.append(sim._assessCreature((ownY - (int(self.geneticString[0]) - i)) % sim.gridSize, ownX, self))
            visionList.append("|  ^  |")

        elif heading == "s":
            visionList.append("|  v  |")
            for i in range(int(self.geneticString[0])):
                visionList.append(sim._assessCreature((ownY + i + 1) % sim.gridSize, ownX, self))

        elif heading == "e":
            visionList.append("|  >  |")
            for i in range(int(self.geneticString[0])):
                visionList.append(sim._assessCreature(ownY, (ownX + i + 1) % sim.gridSize, self))

        elif heading == "w":
            for i in range(int(self.geneticString[0])):
                visionList.append(sim._assessCreature(ownY, (ownX - (int(self.geneticString[0]) - i)) % sim.gridSize, self))
            visionList.append("|  <  |")


        if len(visionList) > 0:
            for i in range(len(visionList)):
                if visionList[i] == 0:
                    visionList[i] = "|     |"
                    if heading == "n" or heading == "s":
                        print(visionList[i])
                    else:
                        print(visionList[i], end="")
                elif visionList[i] == 1:
                    visionList[i] = "|  *  |"
                    if heading == "n" or heading == "s":
                        print(visionList[i])
                    else:
                        print(visionList[i], end="")
                else:
                    if heading == "n" or heading == "s":
                        print(visionList[i])
                    else:
                        print(visionList[i], end="")

        print("\n")


    def _assess(self, sim):
        ownY, ownX, heading = self.getPose()
        cellsSmelled = []
        cellAbove = sim.objectsAt((ownY - 1) % sim.gridSize, ownX)
        cellBelow = sim.objectsAt((ownY + 1) % sim.gridSize, ownX)
        cellRight = sim.objectsAt(ownY, (ownX + 1) % sim.gridSize)
        cellLeft = sim.objectsAt(ownY, (ownX - 1) % sim.gridSize)

        cellsSmelled.append(cellAbove)
        cellsSmelled.append(cellBelow)
        cellsSmelled.append(cellRight)
        cellsSmelled.append(cellLeft)
        print("cellsSmelled: ", cellsSmelled)

        return cellsSmelled


    def smellRadiusFood1(self, sim):
        ownY, ownX, heading = self.getPose()
        cellsSmelled = []

        cellAbove = sim._assessFood((ownY - 1) % sim.gridSize, ownX)
        cellBelow = sim._assessFood((ownY + 1) % sim.gridSize, ownX)
        cellRight = sim._assessFood(ownY, (ownX + 1) % sim.gridSize)
        cellLeft = sim._assessFood(ownY, (ownX - 1) % sim.gridSize)

        cellsSmelled.append(cellAbove)
        cellsSmelled.append(cellBelow)
        cellsSmelled.append(cellRight)
        cellsSmelled.append(cellLeft)

        return cellsSmelled

    def smellRadiusFood2(self, sim):
        ownY, ownX, heading = self.getPose()
        cellsSmelled = []

        cellAbove = sim._assessFood((ownY - 1) % sim.gridSize, ownX)
        cellBelow = sim._assessFood((ownY + 1) % sim.gridSize, ownX)
        cellRight = sim._assessFood(ownY, (ownX + 1) % sim.gridSize)
        cellLeft = sim._assessFood(ownY, (ownX - 1) % sim.gridSize)

        cellTwoAbove = sim._assessFood((ownY - 2) % sim.gridSize, ownX)
        cellTwoBelow = sim._assessFood((ownY + 2) % sim.gridSize, ownX)
        cellTwoRight = sim._assessFood(ownY, (ownX + 2) % sim.gridSize)
        cellTwoLeft = sim._assessFood(ownY, (ownX - 2) % sim.gridSize)

        cellAboveLeft = sim._assessFood((ownY - 1) % sim.gridSize, (ownX - 1) % sim.gridSize)
        cellAboveRight = sim._assessFood((ownY - 1) % sim.gridSize, (ownX + 1) % sim.gridSize)
        cellBelowRight = sim._assessFood((ownY + 1) % sim.gridSize, (ownX + 1) % sim.gridSize)
        cellBelowLeft = sim._assessFood((ownY + 1) % sim.gridSize, (ownX - 1) % sim.gridSize)

        cellsSmelled.append(cellAbove)
        cellsSmelled.append(cellBelow)
        cellsSmelled.append(cellRight)
        cellsSmelled.append(cellLeft)

        cellsSmelled.append(cellTwoAbove)
        cellsSmelled.append(cellTwoBelow)
        cellsSmelled.append(cellTwoRight)
        cellsSmelled.append(cellTwoLeft)

        cellsSmelled.append(cellAboveLeft)
        cellsSmelled.append(cellAboveRight)
        cellsSmelled.append(cellBelowLeft)
        cellsSmelled.append(cellBelowRight)

        return cellsSmelled


    def smellRadiusCreature1(self, sim):
        ownY, ownX, heading = self.getPose()
        cellsSmelled = []

        cellAbove = sim._assessCreature((ownY - 1) % sim.gridSize, ownX, self)
        cellBelow = sim._assessCreature((ownY + 1) % sim.gridSize, ownX, self)
        cellRight = sim._assessCreature(ownY, (ownX + 1) % sim.gridSize, self)
        cellLeft = sim._assessCreature(ownY, (ownX - 1) % sim.gridSize, self)

        cellsSmelled.append(cellAbove)
        cellsSmelled.append(cellBelow)
        cellsSmelled.append(cellRight)
        cellsSmelled.append(cellLeft)

        return cellsSmelled

    def smellRadiusCreature2(self, sim):
        ownY, ownX, heading = self.getPose()
        cellsSmelled = []

        cellAbove = sim._assessCreature((ownY - 1) % sim.gridSize, ownX, self)
        cellBelow = sim._assessCreature((ownY + 1) % sim.gridSize, ownX, self)
        cellRight = sim._assessCreature(ownY, (ownX + 1) % sim.gridSize, self)
        cellLeft = sim._assessCreature(ownY, (ownX - 1) % sim.gridSize, self)

        cellTwoAbove = sim._assessCreature((ownY - 2) % sim.gridSize, ownX, self)
        cellTwoBelow = sim._assessCreature((ownY + 2) % sim.gridSize, ownX, self)
        cellTwoRight = sim._assessCreature(ownY, (ownX + 2) % sim.gridSize, self)
        cellTwoLeft = sim._assessCreature(ownY, (ownX - 2) % sim.gridSize, self)

        cellAboveLeft = sim._assessCreature((ownY - 1) % sim.gridSize, (ownX - 1) % sim.gridSize, self)
        cellAboveRight = sim._assessCreature((ownY - 1) % sim.gridSize, (ownX + 1) % sim.gridSize, self)
        cellBelowRight = sim._assessCreature((ownY + 1) % sim.gridSize, (ownX + 1) % sim.gridSize, self)
        cellBelowLeft = sim._assessCreature((ownY + 1) % sim.gridSize, (ownX - 1) % sim.gridSize, self)

        cellsSmelled.append(cellAbove)
        cellsSmelled.append(cellBelow)
        cellsSmelled.append(cellRight)
        cellsSmelled.append(cellLeft)

        cellsSmelled.append(cellTwoAbove)
        cellsSmelled.append(cellTwoBelow)
        cellsSmelled.append(cellTwoRight)
        cellsSmelled.append(cellTwoLeft)

        cellsSmelled.append(cellAboveLeft)
        cellsSmelled.append(cellAboveRight)
        cellsSmelled.append(cellBelowLeft)
        cellsSmelled.append(cellBelowRight)

        return cellsSmelled

    def detectSmellRadius(self, sim):
        ownY, ownX, heading = self.getPose()
        smellRadius = self.geneticString[1]

        # actions for if the agent has a smell radius of 1
        if int(smellRadius) == 1:

            creaturesSmelled = self.smellRadiusCreature1(sim)
            foodSmelled = self._assess(sim)

            cellsSmelled = self.combineStrings(creaturesSmelled, foodSmelled, self)

            if cellsSmelled[0] != 0 and heading == "n":
                return "above", cellsSmelled[0]
            elif cellsSmelled[1] != 0 and heading == "n":
                return "below", cellsSmelled[1]
            elif cellsSmelled[2] != 0 and heading == "n":
                return "right", cellsSmelled[2]
            elif cellsSmelled[3] != 0 and heading == "n":
                return "left", cellsSmelled[3]

            elif cellsSmelled[0] != 0 and heading == "s":
                return "below", cellsSmelled[0]
            elif cellsSmelled[1] != 0 and heading == "s":
                return "above", cellsSmelled[1]
            elif cellsSmelled[2] != 0 and heading == "s":
                return "left", cellsSmelled[2]
            elif cellsSmelled[3] != 0 and heading == "s":
                return "right", cellsSmelled[3]

            elif cellsSmelled[0] != 0 and heading == "e":
                return "left", cellsSmelled[0]
            elif cellsSmelled[1] != 0 and heading == "e":
                return "right", cellsSmelled[1]
            elif cellsSmelled[2] != 0 and heading == "e":
                return "above", cellsSmelled[2]
            elif cellsSmelled[3] != 0 and heading == "e":
                return "below", cellsSmelled[3]

            elif cellsSmelled[0] != 0 and heading == "w":
                return "right", cellsSmelled[0]
            elif cellsSmelled[1] != 0 and heading == "w":
                return "left", cellsSmelled[1]
            elif cellsSmelled[2] != 0 and heading == "w":
                return "below", cellsSmelled[2]
            elif cellsSmelled[3] != 0 and heading == "w":
                return "above", cellsSmelled[3]
            else:
                return "none"

        elif int(smellRadius) == 2:
            creaturesSmelled = self.smellRadiusCreature2(sim)
            foodSmelled = self.smellRadiusFood2(sim)

            cellsSmelled = self.combineStrings(creaturesSmelled, foodSmelled, self)

            if cellsSmelled[0] != 0 and heading == "n":
                return "above", cellsSmelled[0]
            elif cellsSmelled[1] != 0 and heading == "n":
                return "below", cellsSmelled[1]
            elif cellsSmelled[2] != 0 and heading == "n":
                return "right", cellsSmelled[2]
            elif cellsSmelled[3] != 0 and heading == "n":
                return "left", cellsSmelled[3]

            elif cellsSmelled[0] != 0 and heading == "s":
                return "below", cellsSmelled[0]
            elif cellsSmelled[1] != 0 and heading == "s":
                return "above", cellsSmelled[1]
            elif cellsSmelled[2] != 0 and heading == "s":
                return "left", cellsSmelled[2]
            elif cellsSmelled[3] != 0 and heading == "s":
                return "right", cellsSmelled[3]

            elif cellsSmelled[0] != 0 and heading == "e":
                return "left", cellsSmelled[0]
            elif cellsSmelled[1] != 0 and heading == "e":
                return "right", cellsSmelled[1]
            elif cellsSmelled[2] != 0 and heading == "e":
                return "above", cellsSmelled[2]
            elif cellsSmelled[3] != 0 and heading == "e":
                return "below", cellsSmelled[3]

            elif cellsSmelled[0] != 0 and heading == "w":
                return "right", cellsSmelled[0]
            elif cellsSmelled[1] != 0 and heading == "w":
                return "left", cellsSmelled[1]
            elif cellsSmelled[2] != 0 and heading == "w":
                return "below", cellsSmelled[2]
            elif cellsSmelled[3] != 0 and heading == "w":
                return "above", cellsSmelled[3]

            elif (cellsSmelled[4] != 0) and heading == "n":
                return "above", cellsSmelled[4]
            elif (cellsSmelled[5] != 0) and heading == "n":
                return "below", cellsSmelled[5]
            elif (cellsSmelled[6] != 0) and heading == "n":
                return "right", cellsSmelled[6]
            elif (cellsSmelled[7] != 0) and heading == "n":
                return "left", cellsSmelled[7]

            elif (cellsSmelled[4] != 0) and heading == "s":
                return "below", cellsSmelled[4]
            elif (cellsSmelled[5] != 0) and heading == "s":
                return "above", cellsSmelled[5]
            elif (cellsSmelled[6] != 0) and heading == "s":
                return "left", cellsSmelled[6]
            elif (cellsSmelled[7] != 0) and heading == "s":
                return "right", cellsSmelled[7]

            elif (cellsSmelled[4] != 0) and heading == "e":
                return "left", cellsSmelled[4]
            elif (cellsSmelled[5] != 0) and heading == "e":
                return "right", cellsSmelled[5]
            elif (cellsSmelled[6] != 0) and heading == "e":
                return "above", cellsSmelled[6]
            elif (cellsSmelled[7] != 0) and heading == "e":
                return "below", cellsSmelled[7]

            elif (cellsSmelled[4] != 0) and heading == "w":
                return "right", cellsSmelled[4]
            elif (cellsSmelled[5] != 0) and heading == "w":
                return "left", cellsSmelled[5]
            elif (cellsSmelled[6] != 0) and heading == "w":
                return "below", cellsSmelled[6]
            elif (cellsSmelled[7] != 0) and heading == "w":
                return "above", cellsSmelled[7]

            elif cellsSmelled[8] != 0 and heading == "n":
                return random.choice(["above", "left"]), cellsSmelled[8]
            elif cellsSmelled[9] != 0 and heading == "n":
                return random.choice(["above", "right"]), cellsSmelled[9]
            elif cellsSmelled[10] != 0 and heading == "n":
                return random.choice(["below", "left"]), cellsSmelled[10]
            elif cellsSmelled[11] != 0 and heading == "n":
                return random.choice(["below", "right"]), cellsSmelled[11]

            elif cellsSmelled[8] != 0 and heading == "s":
                return random.choice(["below", "right"]), cellsSmelled[8]
            elif cellsSmelled[9] != 0 and heading == "s":
                return random.choice(["below", "left"]), cellsSmelled[9]
            elif cellsSmelled[10] != 0 and heading == "s":
                return random.choice(["above", "right"]), cellsSmelled[10]
            elif cellsSmelled[11] != 0 and heading == "s":
                return random.choice(["above", "left"]), cellsSmelled[11]

            elif cellsSmelled[8] != 0 and heading == "e":
                return random.choice(["below", "left"]), cellsSmelled[8]
            elif cellsSmelled[9] != 0 and heading == "e":
                return random.choice(["above", "left"]), cellsSmelled[9]
            elif cellsSmelled[10] != 0 and heading == "e":
                return random.choice(["below", "right"]), cellsSmelled[10]
            elif cellsSmelled[11] != 0 and heading == "e":
                return random.choice(["above", "right"]), cellsSmelled[11]

            elif cellsSmelled[8] != 0 and heading == "w":
                return random.choice(["above", "right"]), cellsSmelled[8]
            elif cellsSmelled[9] != 0 and heading == "w":
                return random.choice(["below", "right"]), cellsSmelled[9]
            elif cellsSmelled[10] != 0 and heading == "w":
                return random.choice(["above", "left"]), cellsSmelled[10]
            elif cellsSmelled[11] != 0 and heading == "w":
                return random.choice(["below", "left"]), cellsSmelled[11]

            else:
                return "none"

        else:
            return "none"

    def _printSmell(self, sim, type):
        smellRadius = self.geneticString[1]
        ownY, ownX, heading = self.getPose()

        if heading == "n":
            direction = "^"
        elif heading == "s":
            direction = "v"
        elif heading == "e":
            direction = ">"
        elif heading == "w":
            direction = "<"
        else:
            direction = "x"

        if int(smellRadius) == 1:
            if type == "agent":
                cellsSmelled = self._assess(sim)
            else:
                cellsSmelled = self._assess(sim)
            # cellsSmelled = self.smellRadiusCreature1(agent)
            print(cellsSmelled)

            print("\t" + str(cellsSmelled[0]) + "\t")
            print(str(cellsSmelled[3]) + "   " + direction + " \t" + str(cellsSmelled[2]))
            print("\t" + str(cellsSmelled[1]) + "\t")

        elif int(smellRadius) == 2:
            if type == "agent":
                cellsSmelled = self.smellRadiusCreature2(sim)
            else:
                cellsSmelled = self.smellRadiusFood2(sim)
            # cellsSmelled = self.smellRadiusCreature2(agent)
            print(cellsSmelled)

            print("\t\t" + str(cellsSmelled[4]) + "\t\t")
            print("\t" + str(cellsSmelled[8]) + "\t" + str(cellsSmelled[0]) + " \t" + str(cellsSmelled[9]))
            print(str(cellsSmelled[7]) + "\t" + str(cellsSmelled[3]) + "   " + direction + " \t" + str(
                cellsSmelled[2]) + " \t" + str(cellsSmelled[6]))
            print("\t" + str(cellsSmelled[10]) + "\t" + str(cellsSmelled[1]) + " \t" + str(cellsSmelled[11]))
            print("\t\t" + str(cellsSmelled[5]) + "\t\t")
        else:
            print("NO SMELL")

    def combineStrings(self, creatureString, foodString, sim):
        finalString = []
        for i in range(len(creatureString)):
            if foodString[i] != 0 & creatureString[i] != 0:
                if self.getEnergy() < 15:
                    finalString.append(foodString[i])
                else:
                    finalString.append(foodString[i])
            elif foodString[i] != 0 and creatureString[i] == 0:
                finalString.append(foodString[i])
            elif creatureString[i] != 0 and foodString[i] == 0:
                finalString.append(creatureString[i])
            else:
                finalString.append(0)

        # print("final String: " + str(finalString))
        return finalString

    def __str__(self):
        formStr = "Agent: {0:>3d}  {1:>3d}  {2:^3s}   {3:^6d}      {4}"
        return formStr.format(self.row, self.col, self.heading, self.energy, self.geneticString)