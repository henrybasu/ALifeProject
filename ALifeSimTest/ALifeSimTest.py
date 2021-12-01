
import random
import tkinter

from ALifeGUITest import *
from AgentTest import *
from ObjectTest import *
from StoneTest import *
from FoodTest import *

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
        self.initialGeneticStrings = geneticStrings
        self.maxFood = 0
        self.stoneMap = dict()
        self.foodMap = dict()
        self.agentMap = dict()
        self.globalMap = dict()
        for row in range(gridSize):
            for col in range(gridSize):
                self.stoneMap[row, col] = []
                self.foodMap[row, col] = []
                self.agentMap[row, col] = []
                self.globalMap[row, col] = []

        # self.printGrid()

        self.foodList = []
        self.stoneList = []
        self.agentList = []
        self.deadAgents = []
        self.eatenFood = []
        self.agentList = []
        self.stepNum = 0
        self.verbose = False

        self._placeStones()
        self._placeFood()
        self._placeAgents()

    def getSize(self):
        """Returns the size of the grid"""
        return self.gridSize


    def getAgentNumber(self):
        """Returns the number of agents placed on the grid"""
        return self.numAgents

    def getFood(self):
        """Returns the list of agents"""
        return self.foodList[:]

    def getAgents(self):
        """Returns the list of agents"""
        return self.agentList[:]

    def getStones(self):
        """Returns the list of agents"""
        return self.stoneList[:]

    def getDeadAgents(self):
        """Returns a list of the dead agents."""
        return self.deadAgents

    def getEatenFood(self):
        """Returns a list of the food eaten."""
        return self.eatenFood[:]

    def stonesAt(self, row, col):
        """Given a row and column, returns a list of the stones at that location."""
        return self.stoneMap[row, col]

    def foodAt(self, row, col):
        """Given a row and column, returns the amount of food at that location."""
        return self.foodMap[row, col]

    def agentsAt(self, row, col):
        """Given a row and column, returns a list of the agents at that location."""
        return self.agentMap[row, col]

    def objectsAt(self, row, col):
        return self.globalMap[row, col]


    def _placeFood(self):
        """Places food in random clumps so that roughly self.percentFood cells have food."""
        totalCells = self.gridSize ** 2
        foodClumps = int(self.FOOD_PERCENT * totalCells)
        for i in range(foodClumps):
            self._addFoodClump()

    def _placeAgents(self):
        for i in range(self.numAgents):
            agentPose = self._genRandomPose()
            r, c, h = agentPose

            while True:
                if len(self.globalMap[r, c]) != 0:
                    (r, c, h) = self._genRandomPose()
                else:
                    break

            if self.initialGeneticStrings is None or len(self.initialGeneticStrings) <= i:
                nextAgent = Agent(initPose = agentPose)
            else:
                nextAgent = Agent(geneticString=self.initialGeneticStrings[i], initPose = agentPose)

            if self.initialGeneticStrings is None:
                pass

            self.agentList.append(nextAgent)
            self.agentMap[r, c].append(nextAgent)
            self.globalMap[r, c].append(nextAgent)

    def _placeStones(self):
        (randRow, randCol) = self._genRandomLoc()
        while True:
            if len(self.globalMap[randRow, randCol]) != 0:
                (randRow, randCol) = self._genRandomLoc()
            else:
                break
        nextStone = Stone(initPose=(randRow, randCol), geneticString="00")
        self.stoneList.append(nextStone)
        self.stoneMap[randRow, randCol].append(nextStone)
        self.globalMap[randRow, randCol].append(nextStone)


    def _addFoodClump(self):
        """Adds a clump of food at a random location."""
        (randRow, randCol) = self._genRandomLoc()
        while True:
            if len(self.globalMap[randRow, randCol]) != 0:
                (randRow, randCol) = self._genRandomLoc()
            else:
                break

        nextFood = Food(initPose=(randRow, randCol))
        self.foodList.append(nextFood)
        self.foodMap[randRow, randCol].append(nextFood)
        self.globalMap[randRow, randCol].append(nextFood)


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
        # rowLen = 5 * self.gridSize + 1
        # cellStr = "{0:<4d}|"
        # print("-" * rowLen)
        # for row in range(self.gridSize):
        #     foodStr = "|"
        #     agInCellA = "|"
        #     agInCellB = "|"
        #     agInCellC = "|"
        #     for col in range(self.gridSize):
        #         sA, sB, sC = self._agentStringCodes(row, col)
        #         agInCellA += sA
        #         agInCellB += sB
        #         agInCellC += sC
        #         foodStr += cellStr.format(self.foodMap[row, col])
        #     print(foodStr)
        #     print(agInCellA)
        #     print(agInCellB)
        #     print(agInCellC)
        #     print("-" * rowLen)

        for row in range(self.gridSize):
            for col in range(self.gridSize):
                if len(self.stoneMap[row, col]) > 0:
                    print("|   s   |", end="")
                elif len(self.agentMap[row, col]) > 1:
                    print("|  " + str(len(self.agentMap[row, col])) + " a  |", end="")
                elif len(self.foodMap[row, col]) > 0 and len(self.agentMap[row, col]) > 0:
                    print("|  f a  |", end="")
                elif len(self.foodMap[row, col]) > 0:
                    print("|   f   |", end="")
                elif len(self.agentMap[row, col]) > 0:
                    print("|   a   |", end="")
                else:
                    print("|       |", end="")
            print("\n")


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
        """Prints the current location, heading, energy, step spawned, and step died of each agent."""
        #TODO: Add steps created
        print("===== Live Agents =====")
        print("       Row  Col  Hed   Energy    Genetic String  StepFirst  StepDied")
        for agent in self.agentList:
            print(agent, "       ", "x", "         ", "x")
        print("===== Dead Agents =====")
        print("       Row  Col  Hed   Energy    Genetic String  StepFirst  StepDied")
        for agent,stepDied in self.deadAgents:
            print(agent, "       ", "x", "         ", stepDied)


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

        self._growFood()
        self._updateAgents()
        # print(self.foodMap)

        for i in range(len(self.agentList)):
            print("==== AGENT COLOR: " + str(self.agentList[i].colorNumberToText(self.agentList[i].getColor())) + " ====")
        #     print("~ Energy ~")
        #     print(self.agentList[i].getEnergy())
        #     print("~ Vision ~")
        #     self._printVision(self.agentList[i])
        #     print("~ Smell Food ~")
            self.agentList[i]._printSmell(self, "food")

            # print("~ Smell Agent ~")
            # self.agentList[i]._printSmell(self, "agent")
            # print(self.agentList[i].detectSmellRadius(self), "agent")

        # self.printGrid()
        # print(self.globalMap)
        # print(self.agentMap)


    def _growFood(self):
        """Updates every cell in the food map with more food, up to the maximum amount"""
        # Grow food
        for cell in self.foodMap:
            foodAmt = self.foodMap[cell]
            # if foodAmt < self.MAX_FOOD:
            #     newAmt = int(foodAmt * self.GROWTH_RATE)
            #     self.foodMap[cell] += newAmt
            #     if self.foodMap[cell] > self.MAX_FOOD:
            #         self.foodMap[cell] = self.MAX_FOOD
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
            rAhead, cAhead = self.agentList[i]._computeAhead(self.gridSize)

            # if agent.energy <= 0:
            #     print("here")
            #     break


            # checks to see if there is a creature where the agent currently is
            isCreatureHere = self._assessCreatureHere(agentR, agentC)

            # checks to see if there is food where the agent currently is
            isFoodHere = self.foodAt(agentR, agentC)

            # checks to see if there is a creature in the agent's vision
            isCreatureAhead = self.agentList[i]._areCreaturesInVision(self)

            # checks to see if there is a creature in the agent's smell radius
            canSmellCreature = agent.detectSmellRadius(self)


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
                print("action: ", action)

                if action == 'breed':
                    self.makeABaby(self.agentMap[agentR, agentC][0], self.agentMap[agentR, agentC][1])
                    isOkay = agent.changeEnergy(0)

                elif action == 'eat':
                    self.eatFood(agentR, agentC)
                    isOkay = agent.changeEnergy(0)

                elif action == 'attack':
                    self.agentList[i].attackCreature(self, agentR, agentC)
                    isOkay = agent.changeEnergy(0)

                elif action == 'forward':
                    agent.updatePose(rAhead, cAhead, agentH)
                    print("Agent Map at [r,c]: ", self.agentMap[agentR, agentC])
                    print(agent)
                    print("[r,c]: ", agentR, agentC)
                    if len(self.agentMap[agentR, agentC]) != 0:
                        # print("REMOVING",agent,"from agentMap")
                        self.agentMap[agentR, agentC].remove(agent)
                        # print(self.agentMap)
                    if agent in (self.globalMap[agentR, agentC]):
                        # print("REMOVING",agent,"from globalMap")
                        self.globalMap[agentR, agentC].remove(agent)
                        # print(self.globalMap)

                    self.agentMap[rAhead, cAhead].append(agent)
                    self.globalMap[rAhead, cAhead].append(agent)
                    # print("globalMap:",self.globalMap)
                    # print("agentMap",self.agentMap)
                    agentR, agentC = rAhead, cAhead
                    isOkay = agent.changeEnergy(0)

                elif action == 'left':
                    agent.updatePose(agentR, agentC, agent._leftTurn())
                    isOkay = agent.changeEnergy(0)

                elif action == 'right':
                    agent.updatePose(agentR, agentC, agent._rightTurn())
                    isOkay = agent.changeEnergy(0)

                elif action == 'turnAround':
                    agent.updatePose(agentR, agentC, agent._turnAround())
                    isOkay = agent.changeEnergy(0)

                else:
                    print("Unknown action:", action)
                    isOkay = agent.changeEnergy(0)

                agentR, agentC, agentH = agent.getPose()
                rAhead, cAhead = agent._computeAhead(self.gridSize)
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
                self.globalMap[agentR, agentC].remove(agent)

    def _assessFood(self, row, col):
        """Given a row and column, examine the amount of food there, and divide it into
        no food, some food, and plentiful food: returning 0, 1, or 2."""
        # print("AssessFood")
        foodAmt = self.foodMap[row, col]
        #print("FoodMap: " + str(self.foodMap))
        # print("Row and Col: " + str(row) + ", " + str(col))
        # print("FoodMap[row,col] " + str(self.foodMap[row, col]))
        if len(foodAmt) > 0:
            return 3
        else:
            return 0

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

    def _assessObjects(self, row, col, agent):
        listOfObjects =  self.globalMap[row, col]
        if listOfObjects != []:
            for ob in listOfObjects:
                if type(ob) is Stone:
                    return -1
                elif type(ob) is Agent:
                    if ob.getColor() == agent.getColor():
                        return 2
                    else:
                        return 1
                elif type(ob) is Food:
                    return 3
        return 0

    def eatFood(self, row, col):
        """Determines what, if any, food is eaten from the current given location. It returns the
        energy value of the food eaten, and updates the foodMap."""
        foodAtCell = self.foodMap[row, col]
        if len(foodAtCell) > 0:
            self.eatenFood.append(foodAtCell)
            for ob in self.globalMap[row, col]:
                if type(ob) is Food:
                    self.foodMap[row, col] = []
                    self.globalMap[row, col] = []

            for i in range(len(self.foodList)):
                if foodAtCell == self.foodList[i]:
                    self.foodList.pop(i)



    def makeABaby(self, agent1, agent2):

        if agent1.getReadyToBreed() == 0 and agent2.getReadyToBreed() == 0:
            agentPose = agent1.getPose()
            r, c, h = agentPose

            agent1GeneticString = agent1.getGeneticString()
            agent2GeneticString = agent2.getGeneticString()

            # TODO: if we extend geneticString's length, this will need to be changed.
            babyGeneticStringPart1 = agent1GeneticString[:4]
            babyGeneticStringPart2 = agent2GeneticString[4:]

            babyGeneticString = babyGeneticStringPart1 + babyGeneticStringPart2

            babyAgent = Agent(geneticString=babyGeneticString, initPose=agentPose, stepSpawned=self.stepNum)

            self.agentList.append(babyAgent)
            self.agentMap[r, c].append(babyAgent)
            self.globalMap[r,c].append(babyAgent)

            agent1.setReadyToBreed(24)
            agent2.setReadyToBreed(24)

