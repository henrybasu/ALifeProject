
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
    MAX_FOOD = 1
    time = 12

    def __init__(self, gridSize, numAgents, geneticStrings):
        """Takes in the side length of the foodMap, and makes the foodMap representation, and also the number
        of agents, who are randomly created and placed on the foodMap. Multiple agents per foodMap cell are allowed."""
        self.gridSize = gridSize
        self.numAgents = numAgents
        self.maxFood = 10
        self.foodMap = dict()
        self.agentMap = dict()
        for row in range(gridSize):
            for col in range(gridSize):
                self.foodMap[row, col] = 0
                self.agentMap[row, col] = []


        self._placeFood()
        # self.printGrid()


        self.deadAgents = []
        self.eatenFood = []
        self.agentList = []
        self.stepNum = 0
        self.verbose = False

        for i in range(numAgents):
            agentPose = self._genRandomPose()
            r, c, h = agentPose

            if geneticStrings is None or len(geneticStrings) <= i:
                nextAgent = Agent(initPose=agentPose)
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


    # def _addFoodClump(self):
    #     """Adds a clump of food at a random location."""
    #     (randRow, randCol) = self._genRandomLoc()
    #     for deltaR in range(-1, 2):
    #         offsetR = (randRow + deltaR) % self.gridSize
    #         for deltaC in range(-1, 2):
    #             offsetC = (randCol + deltaC) % self.gridSize
    #             foodAmt = 20 - (5 * (abs(deltaR) + abs(deltaC)))
    #             self.foodMap[offsetR, offsetC] += foodAmt

    def _addFoodClump(self):
        """Adds a clump of food at a random location."""
        (randRow, randCol) = self._genRandomLoc()
        self.foodMap[randRow, randCol] += 1


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
        #     print("~ Energy ~")
        #     print(self.agentList[i].getEnergy())
        #     print("~ Vision ~")
        #     self._printVision(self.agentList[i])
            print("~ Smell Food ~")
            self._printSmell(self.agentList[i], "food")

            # print("~ Smell Agent ~")
            # self._printSmell(self.agentList[i], "agent")
            # print(self.detectSmellRadius(self.agentList[i]), "agent")


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
        if self.verbose:
            print("aLifeSim object is using _updateAgents() for step " + str(self.stepNum))

        if self.verbose:
            print("--------------------------------------------------------------------------------------------")
        while i < len(self.agentList):
            if self.verbose:
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

            # checks to see if there is food where the agent currently is
            isFoodHere = self.foodAt(agentR, agentC)

            # checks to see if there is a creature in the agent's vision
            isCreatureAhead = self._areCreaturesInVision(self.agentList[i])

            # checks to see if there is a creature in the agent's smell radius
            canSmellCreature = self.detectSmellRadius(agent)


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

            # print("Agent is ready to breed: " + str(agent.getReadyToBreed()))


            if not agent.isDead:

                action = agent.determineAction(self.agentList[i], isCreatureHere, isCreatureAhead, canSmellCreature, self.time, isFoodHere)

                if action == 'breed':
                    self.makeABaby(self.agentMap[agentR, agentC][0], self.agentMap[agentR, agentC][1])
                    isOkay = agent.changeEnergy(0)

                elif action == 'eat':
                    self._foodEaten(agentR, agentC)
                    isOkay = agent.changeEnergy(0)

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

                if self.verbose:
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
        # print("AssessFood")
        foodAmt = self.foodMap[row, col]
        #print("FoodMap: " + str(self.foodMap))
        # print("Row and Col: " + str(row) + ", " + str(col))
        # print("FoodMap[row,col] " + str(self.foodMap[row, col]))
        if foodAmt == 0:
            return 0
        else:
            return 3

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
            for i in range(len(creatureAmt)):
                if agent.getColor() == creatureAmt[i].getColor():
                    print("TRUE")
                    return 2
            return 1

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
        if foodAtCell == 1:
            self.foodMap[row, col] = 0




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

    def _printSmell(self, agent, type):
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
            if type == "agent":
                cellsSmelled = self.smellRadiusCreature1(agent)
            else:
                cellsSmelled = self.smellRadiusFood1(agent)
            # cellsSmelled = self.smellRadiusCreature1(agent)
            print(cellsSmelled)

            print("\t" + str(cellsSmelled[0]) + "\t")
            print(str(cellsSmelled[3]) + "   " + direction + " \t" + str(cellsSmelled[2]))
            print("\t" + str(cellsSmelled[1]) + "\t")

        elif int(smellRadius) == 2:
            if type == "agent":
                cellsSmelled = self.smellRadiusCreature2(agent)
            else:
                cellsSmelled = self.smellRadiusFood2(agent)
            # cellsSmelled = self.smellRadiusCreature2(agent)
            print(cellsSmelled)

            print("\t\t" + str(cellsSmelled[4]) + "\t\t")
            print("\t" + str(cellsSmelled[8]) + "\t" + str(cellsSmelled[0]) + " \t" + str(cellsSmelled[9]))
            print(str(cellsSmelled[7]) + "\t" + str(cellsSmelled[3]) + "   " + direction + " \t" + str(cellsSmelled[2])+ " \t" + str(cellsSmelled[6]))
            print("\t" + str(cellsSmelled[10]) + "\t" + str(cellsSmelled[1]) + " \t" + str(cellsSmelled[11]))
            print("\t\t" + str(cellsSmelled[5]) + "\t\t")
        else:
            print("NO SMELL")


    def combineStrings(self, creatureString, foodString, agent):
        finalString = []
        for i in range(len(creatureString)):
            if foodString[i] != 0 & creatureString[i] != 0:
                if agent.getEnergy() < 15:
                    finalString.append(foodString[i])
                else:
                    finalString.append(foodString[i])
            elif foodString[i] != 0 and creatureString[i] == 0:
                finalString.append(foodString[i])
            elif creatureString[i] != 0 and foodString[i] == 0:
                finalString.append(creatureString[i])
            else:
                finalString.append(0)

        print("final String: " + str(finalString))
        return finalString


    def smellRadiusFood1(self, agent):
        ownY, ownX, heading = agent.getPose()
        cellsSmelled = []

        cellAbove = self._assessFood((ownY - 1) % self.gridSize, ownX)
        cellBelow = self._assessFood((ownY + 1) % self.gridSize, ownX)
        cellRight = self._assessFood(ownY, (ownX + 1) % self.gridSize)
        cellLeft = self._assessFood(ownY, (ownX - 1) % self.gridSize)

        cellsSmelled.append(cellAbove)
        cellsSmelled.append(cellBelow)
        cellsSmelled.append(cellRight)
        cellsSmelled.append(cellLeft)

        return cellsSmelled

    def smellRadiusFood2(self, agent):
        ownY, ownX, heading = agent.getPose()
        cellsSmelled = []

        cellAbove = self._assessFood((ownY - 1) % self.gridSize, ownX)
        cellBelow = self._assessFood((ownY + 1) % self.gridSize, ownX)
        cellRight = self._assessFood(ownY, (ownX + 1) % self.gridSize)
        cellLeft = self._assessFood(ownY, (ownX - 1) % self.gridSize)

        cellTwoAbove = self._assessFood((ownY - 2) % self.gridSize, ownX)
        cellTwoBelow = self._assessFood((ownY + 2) % self.gridSize, ownX)
        cellTwoRight = self._assessFood(ownY, (ownX + 2) % self.gridSize)
        cellTwoLeft = self._assessFood(ownY, (ownX - 2) % self.gridSize)

        cellAboveLeft = self._assessFood((ownY - 1) % self.gridSize, (ownX - 1) % self.gridSize)
        cellAboveRight = self._assessFood((ownY - 1) % self.gridSize, (ownX + 1) % self.gridSize)
        cellBelowRight = self._assessFood((ownY + 1) % self.gridSize, (ownX + 1) % self.gridSize)
        cellBelowLeft = self._assessFood((ownY + 1) % self.gridSize, (ownX - 1) % self.gridSize)

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


    def smellRadiusCreature1(self, agent):
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

    def smellRadiusCreature2(self, agent):
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

    def detectSmellRadius(self, agent):
        ownY, ownX, heading = agent.getPose()
        smellRadius = agent.geneticString[1]

        # actions for if the agent has a smell radius of 1
        if int(smellRadius) == 1:

            creaturesSmelled = self.smellRadiusCreature1(agent)
            foodSmelled = self.smellRadiusFood1(agent)

            cellsSmelled = self.combineStrings(creaturesSmelled, foodSmelled, agent)

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
            creaturesSmelled = self.smellRadiusCreature2(agent)
            foodSmelled = self.smellRadiusFood2(agent)

            cellsSmelled = self.combineStrings(creaturesSmelled, foodSmelled, agent)

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

    def attackCreature(self, agent, row, col):
        for j in range(len(self.agentsAt(row, col))):

            if int(self.agentsAt(row, col)[j].getColor()) != agent.getColor():
                deadCreature = self.agentsAt(row, col)[j]

                deadCreature.changeEnergy(-100)
                deadCreature.isDead = True


    def makeABaby(self, agent1, agent2):

        if agent1.getReadyToBreed() == 0 and agent2.getReadyToBreed() == 0:
            agentPose = agent1.getPose()
            r, c, h = agentPose

            agent1GeneticString = agent1.getGeneticString()
            agent2GeneticString = agent2.getGeneticString()

            babyGeneticStringPart1 = agent1GeneticString[:4]
            babyGeneticStringPart2 = agent2GeneticString[4:]

            babyGeneticString = babyGeneticStringPart1 + babyGeneticStringPart2

            babyAgent = Agent(geneticString=babyGeneticString, initPose=agentPose)

            self.agentList.append(babyAgent)
            self.agentMap[r, c].append(babyAgent)


            agent1.setReadyToBreed(24)
            agent2.setReadyToBreed(24)