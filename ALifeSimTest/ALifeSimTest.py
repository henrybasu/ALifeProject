
import random
import tkinter

from ALifeGUITest import *
from AgentTest import Agent

class ALifeSimTest(object):
    """A simple simulated foodMap world, similar to NetLogo, with agents that each perform their own
    set of behaviors. Each cell of the foodMap has some amount of food on it, Food tends to occur
    in clusters. Each agent has a certain amount of health that is depleted a bit each time step,
    and that is depleted more if the agent moves. They can regain health by eating, up to a max amount."""

    FOOD_PERCENT = 0.10
    NEW_FOOD_PERCENT = 0.005
    GROWTH_RATE = 0.005
    MAX_FOOD = 20
    time = 12

    def __init__(self, gridSize, numAgents, geneticStrings):
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

            if geneticStrings is None or len(geneticStrings) <= i:
                nextAgent = Agent(initPose = agentPose)
            else:
                nextAgent = Agent(geneticString=geneticStrings[i], initPose = agentPose)

            if geneticStrings is None:
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


    def getDeadAgents(self):
        """Returns a list of the dead agents."""
        return self.deadAgents


    def foodAt(self, row, col):
        """Given a row and column, returns the amount of food at that location."""
        return self.foodMap[row, col]


    def agentsAt(self, row, col):
        """Given a row and column, returns a list of the agents at that location."""
        return self.agentMap[row, col]


    def _placeFood(self):
        """Places food in random clumps so that roughly self.percentFood cells have food."""
        totalCells = self.gridSize ** 2
        foodClumps = int(self.FOOD_PERCENT * totalCells)
        for i in range(foodClumps):
            self._addFoodClump()


    def _addFoodClump(self):
        """Adds a clump of food at a random location."""
        (randRow, randCol) = self._genRandomLoc()
        for deltaR in range(-1, 2):
            offsetR = (randRow + deltaR) % self.gridSize
            for deltaC in range(-1, 2):
                offsetC = (randCol + deltaC) % self.gridSize
                foodAmt = 20 - (5 * (abs(deltaR) + abs(deltaC)))
                self.foodMap[offsetR, offsetC] += foodAmt


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
        #TODO Uncomment this to reimplement time VVV
        # self.stepNum += 1
        # if self.time != 24:
        #     self.time += 1
        # else:
        #     self.time = 0


        # self._growFood()
        self._updateAgents()


        for i in range(len(self.agentList)):
            print("==== AGENT COLOR: " + str(self.agentList[i].colorNumberToText(self.agentList[i].getColor())) + " ====")
            print("~ Vision ~")
            self._printVision(self.agentList[i])
            print("~ Smell ~")
            self._printSmell(self.agentList[i])
            print(self.areCreaturesInSmellRadius(self.agentList[i]))

    def _growFood(self):
        """Updates every cell in the food map with more food, up to the maximum amount"""
        # Grow food
        for cell in self.foodMap:
            foodAmt = self.foodMap[cell]
            if foodAmt < self.MAX_FOOD:
                newAmt = int(foodAmt * self.GROWTH_RATE)
                self.foodMap[cell] += newAmt
                if self.foodMap[cell] > self.MAX_FOOD:
                    self.foodMap[cell] = self.MAX_FOOD
        newClump = random.random()
        if newClump <= self.NEW_FOOD_PERCENT:
            self._addFoodClump()

    def _updateAgents(self):
        """Updates the position and energy of every agent based on its chosen action."""
        i = 0
        print("aLifeSim object is using _updateAgents() for step " + str(self.stepNum))
        print("--------------------------------------------------------------------------------------------")
        while i < len(self.agentList):
            print("")
            print("")
            print("*************** AGENT COLOR: " + str(self.agentList[i].colorNumberToText(self.agentList[i].getColor())) + " ***************")

            # print("x, y, heading: " + str(self.agentList[i].getPose()))
            # print(self.agentList[i].geneticString)

            agent = self.agentList[i]
            agentR, agentC, agentH = agent.getPose()
            rAhead, cAhead = self._computeAhead(agentR, agentC, agentH, agent.moveSpeed)

            # if agent.energy <= 0:
            #     print("here")
            #     break


            # checks to see if there is a creature where the agent currently is
            isCreatureHere = self._assessCreatureHere(agentR, agentC)

            # checks to see if there is a creature in the agent's vision
            isCreatureAhead = self._areCreaturesInVision(self.agentList[i])

            # checks to see if there is a creature in the agent's smell radius
            canSmellCreature = self.areCreaturesInSmellRadius(self.agentList[i])

            # foodHereRating = self._assessFood(agentR, agentC)
            # print("foodHereRating: " + str(foodHereRating))
            # foodAheadRating = self._assessFood(rAhead, cAhead)
            # print("foodAheadRating " + str(foodAheadRating))

            creatureHereRating = self._assessCreatureHere(agentR, agentC)
            # print("Creatures at current location: " + str(creatureHereRating))

            creatureAheadRating = self._assessCreature(rAhead,cAhead, agent)
            # print("Agent color " + str(self.agentList[i].colorNumberToText(self.agentList[i].getColor())) + "'s creatureAheadRating before moving: " + str(creatureAheadRating))
            # print("-------------------------------------------------")
            #TODO: replace 0s with foodHereRating and foodAheadRating
            # action = agent.respond(0, 0, creatureHereRating, creatureAheadRating)

            print("Agent is ready to breed: " + str(agent.getReadyToBreed()))


            action = agent.determineAction(self.agentList[i], isCreatureHere, isCreatureAhead, canSmellCreature, self.time)
            if not agent.isDead:

                if action == 'breed':
                    print("MAKIN A BABY")
                    self.makeABaby(self.agentMap[agentR, agentC][0], self.agentMap[agentR, agentC][1])
                    isOkay = agent.changeEnergy(0)

                elif action == 'eat':
                    newEnergy = self._foodEaten(agentR, agentC)
                    isOkay = agent.changeEnergy(newEnergy - 1)

                elif action == 'attack':
                    self.attackCreature(self.agentList[i], agentR, agentC)
                    isOkay = agent.changeEnergy(0)

                elif action == 'forward':
                    agent.updatePose(rAhead, cAhead, agentH)
                    self.agentMap[agentR, agentC].remove(agent)
                    self.agentMap[rAhead, cAhead].append(agent)
                    agentR, agentC = rAhead, cAhead
                    isOkay = agent.changeEnergy(0)

                elif action == 'left':
                    agent.updatePose(agentR, agentC, self._leftTurn(agentH))
                    isOkay = agent.changeEnergy(0)

                elif action == 'right':
                    agent.updatePose(agentR, agentC, self._rightTurn(agentH))
                    isOkay = agent.changeEnergy(0)

                elif action == 'turnAround':
                    agent.updatePose(agentR, agentC, self._turnAround(agentH))
                    isOkay = agent.changeEnergy(0)

                else:
                    print("Unknown action:", action)
                    isOkay = agent.changeEnergy(0)

            agentR, agentC, agentH = agent.getPose()
            rAhead, cAhead = self._computeAhead(agentR, agentC, agentH, agent.moveSpeed)
            creatureHereRating = self._assessCreatureHere(agentR, agentC)
            creatureAheadRating = self._assessCreature(rAhead, cAhead, agent)

            print("--------------------------------------------------------------------------------------------")

            if agent.getReadyToBreed() != 0:
                agent.changeReadyToBreed(1)


            if agent.energy <= 0:
                isOkay = False

            if isOkay:
                i = i + 1
            else:
                self.deadAgents.append((agent, self.stepNum))
                self.agentList.pop(i)
                self.agentMap[agentR, agentC].remove(agent)

    def _computeAhead(self, row, col, heading, moveSpeed):
        """Determine the cell that is one space ahead of current cell, given the heading."""
        if heading == 'n':   # agent is pointing north, row value decreases
            newR = (row - moveSpeed) % self.gridSize
            return newR, col
        elif heading == 's':  # agent is pointing south, row value increases
            newR = (row + moveSpeed) % self.gridSize
            return newR, col
        elif heading == 'w':  # agent is pointing west, col value decreases
            newC = (col - moveSpeed) % self.gridSize
            return row, newC
        else:  # agent is pointing east, col value increases
            newC = (col + moveSpeed) % self.gridSize
            return row, newC

    def _assessFood(self, row, col):
        """Given a row and column, examine the amount of food there, and divide it into
        no food, some food, and plentiful food: returning 0, 1, or 2."""
        print("AssessFood")
        foodAmt = self.foodMap[row, col]
        #print("FoodMap: " + str(self.foodMap))
        print("Row and Col: " + str(row) + ", " + str(col))
        print("FoodMap[row,col] " + str(self.foodMap[row, col]))
        if foodAmt == 0:
            return 0
        elif foodAmt < 20:
            return 1
        else:
            return 2

    def _assessCreature(self, row, col, agent):
        """Given a row and column, examine the amount of creatures there, and divide it into
        no creatures, and some creatures: returning 0 or 1."""
        # print("Looking at location: (" + str(row) + "," + str(col) + ")")
        creatureAmt = self.agentMap[row, col]
        # print("AgentMap: " + str(self.agentMap))
        # print("Row and Col: " + str(row) + ", " + str(col))
        # print("CreatureAmt = AgentMap[" + str(row) + "," + str(col) + "]: " + str(self.agentMap[row, col]))
        # print(self.agentMap[row, col])
        # print("self: " + str(self))

        if creatureAmt == []:
            # print("no creature ahead")
            return 0

        elif len(creatureAmt) >= 1:
            for i in range(len(creatureAmt)-1):
                if creatureAmt[i].getColor() != creatureAmt[i+1].getColor():
                    return 1
            return 2

    def _assessCreatureHere(self, row, col):
        """Given a row and column, examine the amount of creatures there, and divide it into
        no creatures, and some creatures: returning 0 or 1."""
        # print("Looking at current location: (" + str(row) + "," + str(col) + ")")
        creatureAmt = self.agentMap[row, col]
        #print("AgentMap: " + str(self.agentMap))
        #print("Row and Col: " + str(row) + ", " + str(col))
        # print("CreatureAmt = AgentMap[" + str(row) + "," + str(col) + "]: " + str(self.agentMap[row, col]))
        #print(self.agentMap[row, col])
        #print("self: " + str(self))

        if len(creatureAmt) <= 1:
            return 0
        else:
            for i in range(len(creatureAmt)-1):
                if creatureAmt[i].getColor() != creatureAmt[i+1].getColor():
                    return 1
            return 2

    def _foodEaten(self, row, col):
        """Determines what, if any, food is eaten from the current given location. It returns the
        energy value of the food eaten, and updates the foodMap."""
        foodAtCell = self.foodMap[row, col]
        if foodAtCell <= 10:
            self.foodMap[row, col] = 0
            return foodAtCell
        else:
            self.foodMap[row, col] -= 10
            return 10


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

    def _turnAround(self, heading):
        """return the new heading for a right turn"""
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

    def _printVision(self, agent):
        ownY, ownX, heading = agent.getPose()
        visionList = []

        if heading == "n":
            for i in range(int(agent.geneticString[0])):
                visionList.append(self._assessCreature((ownY - (int(agent.geneticString[0]) - i)) % self.gridSize, ownX, agent))
            visionList.append("|  ^  |")

        elif heading == "s":
            visionList.append("|  v  |")
            for i in range(int(agent.geneticString[0])):
                visionList.append(self._assessCreature((ownY + i + 1) % self.gridSize, ownX, agent))

        elif heading == "e":
            visionList.append("|  >  |")
            for i in range(int(agent.geneticString[0])):
                visionList.append(self._assessCreature(ownY, (ownX + i + 1) % self.gridSize, agent))

        elif heading == "w":
            for i in range(int(agent.geneticString[0])):
                visionList.append(self._assessCreature(ownY, (ownX - (int(agent.geneticString[0]) - i)) % self.gridSize, agent))
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

    def _areCreaturesInVision(self, agent):
        ownY, ownX, heading = agent.getPose()
        visionList = []

        if heading == "n":
            for i in range(int(agent.geneticString[0])):
                visionList.append(self._assessCreature((ownY - (int(agent.geneticString[0]) - i)) % self.gridSize, ownX, agent))
                # if visionList[i] != 0:
                #     return 1
                return visionList[i]

        elif heading == "s":
            for i in range(int(agent.geneticString[0])):
                visionList.append(self._assessCreature((ownY + i + 1) % self.gridSize, ownX, agent))
                # if visionList[i] != 0:
                #     return 1
                return visionList[i]


        elif heading == "e":
            for i in range(int(agent.geneticString[0])):
                visionList.append(self._assessCreature(ownY, (ownX + i + 1) % self.gridSize, agent))
                # if visionList[i] != 0:
                #     return 1
                return visionList[i]


        elif heading == "w":
            for i in range(int(agent.geneticString[0])):
                visionList.append(self._assessCreature(ownY, (ownX - (int(agent.geneticString[0]) - i)) % self.gridSize, agent))
                # if visionList[i] != 0:
                #     return 1
                return visionList[i]


        # print("DON't SEE ANYONE")
        return 0

    def _printSmell(self, agent):
        smellRadius = agent.geneticString[1]
        ownY, ownX, heading = agent.getPose()

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
            cellsSmelled = self.smellRadius1(agent)
            print(cellsSmelled)

            print("\t" + str(cellsSmelled[0]) + "\t")
            print(str(cellsSmelled[3]) + "   " + direction + " \t" + str(cellsSmelled[2]))
            print("\t" + str(cellsSmelled[1]) + "\t")

        elif int(smellRadius) == 2:
            cellsSmelled = self.smellRadius2(agent)
            print(cellsSmelled)

            print("\t\t" + str(cellsSmelled[4]) + "\t\t")
            print("\t" + str(cellsSmelled[8]) + "\t" + str(cellsSmelled[0]) + " \t" + str(cellsSmelled[9]))
            print(str(cellsSmelled[7]) + "\t" + str(cellsSmelled[3]) + "   " + direction + " \t" + str(cellsSmelled[2])+ " \t" + str(cellsSmelled[6]))
            print("\t" + str(cellsSmelled[10]) + "\t" + str(cellsSmelled[1]) + " \t" + str(cellsSmelled[11]))
            print("\t\t" + str(cellsSmelled[5]) + "\t\t")
        else:
            print("NO SMELL")




    def smellRadius1(self, agent):
        ownY, ownX, heading = agent.getPose()
        cellsSmelled = []

        cellAbove = self._assessCreature((ownY - 1) % self.gridSize, ownX, agent)
        cellBelow = self._assessCreature((ownY + 1) % self.gridSize, ownX, agent)
        cellRight = self._assessCreature(ownY, (ownX + 1) % self.gridSize, agent)
        cellLeft = self._assessCreature(ownY, (ownX - 1) % self.gridSize, agent)

        cellsSmelled.append(cellAbove)
        cellsSmelled.append(cellBelow)
        cellsSmelled.append(cellRight)
        cellsSmelled.append(cellLeft)

        return cellsSmelled

    def smellRadius2(self, agent):
        ownY, ownX, heading = agent.getPose()
        cellsSmelled = []

        cellAbove = self._assessCreature((ownY - 1) % self.gridSize, ownX, agent)
        cellBelow = self._assessCreature((ownY + 1) % self.gridSize, ownX, agent)
        cellRight = self._assessCreature(ownY, (ownX + 1) % self.gridSize, agent)
        cellLeft = self._assessCreature(ownY, (ownX - 1) % self.gridSize, agent)

        cellTwoAbove = self._assessCreature((ownY - 2) % self.gridSize, ownX, agent)
        cellTwoBelow = self._assessCreature((ownY + 2) % self.gridSize, ownX, agent)
        cellTwoRight = self._assessCreature(ownY, (ownX + 2) % self.gridSize, agent)
        cellTwoLeft = self._assessCreature(ownY, (ownX - 2) % self.gridSize, agent)

        cellAboveLeft = self._assessCreature((ownY - 1) % self.gridSize, (ownX - 1) % self.gridSize, agent)
        cellAboveRight = self._assessCreature((ownY - 1) % self.gridSize, (ownX + 1) % self.gridSize, agent)
        cellBelowRight = self._assessCreature((ownY + 1) % self.gridSize, (ownX + 1) % self.gridSize, agent)
        cellBelowLeft = self._assessCreature((ownY + 1) % self.gridSize, (ownX - 1) % self.gridSize, agent)

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

    def areCreaturesInSmellRadius(self, agent):
        ownY, ownX, heading = agent.getPose()
        smellRadius = agent.geneticString[1]

        # actions for if the agent has a smell radius of 1
        if int(smellRadius) == 1:
            cellsSmelled = self.smellRadius1(agent)

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
            cellsSmelled = self.smellRadius2(agent)
            if (cellsSmelled[0] != 0 or cellsSmelled[4] != 0) and heading == "n":
                return "above"
            elif (cellsSmelled[1] != 0 or cellsSmelled[5] != 0) and heading == "n":
                return "below"
            elif (cellsSmelled[2] != 0 or cellsSmelled[6] != 0) and heading == "n":
                return "right"
            elif (cellsSmelled[3] != 0 or cellsSmelled[7] != 0) and heading == "n":
                return "left"

            elif (cellsSmelled[0] != 0 or cellsSmelled[4] != 0) and heading == "s":
                return "below"
            elif (cellsSmelled[1] != 0 or cellsSmelled[5] != 0) and heading == "s":
                return "above"
            elif (cellsSmelled[2] != 0 or cellsSmelled[6] != 0) and heading == "s":
                return "left"
            elif (cellsSmelled[3] != 0 or cellsSmelled[7] != 0) and heading == "s":
                return "right"

            elif (cellsSmelled[0] != 0 or cellsSmelled[4] != 0) and heading == "e":
                return "left"
            elif (cellsSmelled[1] != 0 or cellsSmelled[5] != 0) and heading == "e":
                return "right"
            elif (cellsSmelled[2] != 0 or cellsSmelled[6] != 0) and heading == "e":
                return "above"
            elif (cellsSmelled[3] != 0 or cellsSmelled[7] != 0) and heading == "e":
                return "below"

            elif (cellsSmelled[0] != 0 or cellsSmelled[4] != 0) and heading == "w":
                return "right"
            elif (cellsSmelled[1] != 0 or cellsSmelled[5] != 0) and heading == "w":
                return "left"
            elif (cellsSmelled[2] != 0 or cellsSmelled[6] != 0) and heading == "w":
                return "below"
            elif (cellsSmelled[3] != 0 or cellsSmelled[7] != 0) and heading == "w":
                return "above"

            elif cellsSmelled[8] != 0 and heading == "n":
                return random.choice(["above", "left"])
            elif cellsSmelled[9] != 0 and heading == "n":
                return random.choice(["above", "right"])
            elif cellsSmelled[10] != 0 and heading == "n":
                return random.choice(["below", "left"])
            elif cellsSmelled[11] != 0 and heading == "n":
                return random.choice(["below", "right"])

            elif cellsSmelled[8] != 0 and heading == "s":
                return random.choice(["below", "right"])
            elif cellsSmelled[9] != 0 and heading == "s":
                return random.choice(["below", "left"])
            elif cellsSmelled[10] != 0 and heading == "s":
                return random.choice(["above", "right"])
            elif cellsSmelled[11] != 0 and heading == "s":
                return random.choice(["above", "left"])

            elif cellsSmelled[8] != 0 and heading == "e":
                return random.choice(["below", "left"])
            elif cellsSmelled[9] != 0 and heading == "e":
                return random.choice(["above", "left"])
            elif cellsSmelled[10] != 0 and heading == "e":
                return random.choice(["below", "right"])
            elif cellsSmelled[11] != 0 and heading == "e":
                return random.choice(["above", "right"])

            elif cellsSmelled[8] != 0 and heading == "w":
                return random.choice(["above", "right"])
            elif cellsSmelled[9] != 0 and heading == "w":
                return random.choice(["below", "right"])
            elif cellsSmelled[10] != 0 and heading == "w":
                return random.choice(["above", "left"])
            elif cellsSmelled[11] != 0 and heading == "w":
                return random.choice(["below", "left"])

            else:
                return "none"

        else:
            return "NO SMELL"

    def attackCreature(self, agent, row, col):
        for j in range(len(self.agentsAt(row, col))):
            print(self.agentsAt(row, col)[j].geneticString)

            print(self.agentsAt(row, col)[j].geneticString[3])
            if int(self.agentsAt(row, col)[j].geneticString[3]) == 0:
                print("DEAD MAN")
                deadCreature = self.agentsAt(row, col)[j]

                deadCreature.changeEnergy(-100)
                deadCreature.isDead = True
                print("DEAD MAN ENERGY: " + str(deadCreature.energy))
                # self.updateGeneticString(deadCreature, 5 )


                # self.deadAgents.append((deadCreature, self.stepNum))
                # # self.agentList.pop(deadCreature)
                # self.agentMap[row, col].remove(deadCreature)

    def makeABaby(self, agent1, agent2):

        if agent1.getReadyToBreed() == 0 and agent2.getReadyToBreed() == 0:
            agentPose = agent1.getPose()
            r, c, h = agentPose

            agent1GeneticString = agent1.getGeneticString()
            agent2GeneticString = agent2.getGeneticString()

            print("Agent 1 Genetic String: " + str(agent1GeneticString))
            print("Agent 2 Genetic String: " + str(agent2GeneticString))

            babyGeneticStringPart1 = agent1GeneticString[:4]
            babyGeneticStringPart2 = agent2GeneticString[4:]

            print("Baby Genetic String 1: " + str(babyGeneticStringPart1))
            print("Baby Genetic String 2: " + str(babyGeneticStringPart2))

            babyGeneticString = babyGeneticStringPart1 + babyGeneticStringPart2

            print("Baby Genetic String: " + str(babyGeneticString))


            babyAgent = Agent(geneticString="11100699", initPose=agentPose)

            self.agentList.append(babyAgent)
            self.agentMap[r, c].append(babyAgent)


            agent1.setReadyToBreed(24)
            agent2.setReadyToBreed(24)




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
        print("ENERGY LEVEL: " + str(self.energy))
        if self.energy <= 0:
            return False
        print(self.energy)
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
            print("action chosen: a")
            return random.choice(['eat', 'forward', 'left', 'right'])
        elif action == 's':
            print("action chosen: s")
            return 'eat'
        elif action == 'f':
            print("action chosen: f")
            return 'forward'
        elif action == 'l':
            print("action chosen: l")
            return 'left'
        elif action == 'r':
            print("action chosen: r")
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

    def getGeneticString(self):
        return self.geneticString


    def __str__(self):
        formStr = "Agent: {0:>3d}  {1:>3d}  {2:^3s}   {3:^6d}"
        return formStr.format(self.row, self.col, self.heading, self.energy)


# if __name__ == '__main__':
#     sim = ALifeSimTest(50, 20)
#     for rounds in range(5):
#         print("Round", rounds)
#         sim.printGrid()
#         # sim.printAgents()
#         sim.step()
#     totalScenarios = dict()
#     for i in range(27):
#         totalScenarios[i] = 0
#     for agents, when in sim.getDeadAgents():
#         for val in agents.whichScenarios:
#             totalScenarios[val] += agents.whichScenarios[val]
#     for agents in sim.agentList:
#         for val in agents.whichScenarios:
#             totalScenarios[val] += agents.whichScenarios[val]
#     vals = list(totalScenarios.keys())
#     vals.sort()
#     for val in vals:
#         print(val, totalScenarios[val])


