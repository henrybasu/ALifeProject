
import random
import tkinter
import math

from ALifeGUITest import *
from AgentTest import *
from ObjectTest import *
from StoneTest import *
from FoodTest import *
from WaterTest import *
from TreeTest import *
from PitTest import *

class ALifeSimTest(object):
    """A simple simulated foodMap world, similar to NetLogo, with agents that each perform their own
    set of behaviors. Each cell of the foodMap has some amount of food on it, Food tends to occur
    in clusters. Each agent has a certain amount of health that is depleted a bit each time step,
    and that is depleted more if the agent moves. They can regain health by eating, up to a max amount."""

    FOOD_PERCENT = 0.1
    NEW_FOOD_PERCENT = 0.005
    GROWTH_RATE = 0.005
    MAX_FOOD = 1
    time = 12
    numStones = 0
    numWaters = 0
    numTrees = 0
    numPits = 0

    def __init__(self, gridSize, numAgents, numStones, geneticStrings):
        """Takes in the side length of the foodMap, and makes the foodMap representation, and also the number
        of agents, who are randomly created and placed on the foodMap. Multiple agents per foodMap cell are allowed."""
        self.gridSize = gridSize

        self.numAgents = numAgents
        self.numStones = numStones
        self.numWaters = 0
        self.numTrees = 10
        self.numRivers = 1
        self.numPonds = 2
        self.numForests = 10
        self.numPits = 0


        self.initialGeneticStrings = geneticStrings
        self.maxFood = 0
        self.globalMap = dict()

        for row in range(gridSize):
            for col in range(gridSize):
                self.globalMap[row, col] = []

        self.foodList = []
        self.stoneList = []
        self.pitList = []
        self.waterList = []
        self.treeList = []
        self.agentList = []
        self.deadAgents = []
        self.eatenFood = []
        self.agentList = []
        self.stepNum = 0
        self.verbose = False

        self._placeTreesOnHalf()

        # self._placeWaters()
        self._placePits()
        # self._placeTrees(self.numForests, random.randint(3,5))
        # self._placeTrees(self.numForests, 20)

        # self._placeStones()
        # self._placeFood()
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

    def getPits(self):
        """Returns the list of agents"""
        return self.pitList[:]

    def getWaters(self):
        return self.waterList[:]

    def getTrees(self):
        return self.treeList[:]

    def getDeadAgents(self):
        """Returns a list of the dead agents."""
        return self.deadAgents

    def getEatenFood(self):
        """Returns a list of the food eaten."""
        return self.eatenFood[:]

    def stonesAt(self, row, col):
        """Given a row and column, returns a list of the stones at that location."""
        stonesAtList = self.globalMap[row, col].copy()
        for ob in stonesAtList:
            if type(ob) is not Stone:
                stonesAtList.remove(ob)
        return stonesAtList

    def pitAt(self, row, col):
        """Given a row and column, returns a list of the pits at that location."""
        pitsAtList = self.globalMap[row, col].copy()
        for ob in pitsAtList:
            if type(ob) is not Pit:
                pitsAtList.remove(ob)
        return pitsAtList

    def waterAt(self,row,col):
        waterAtList = self.globalMap[row, col].copy()
        for ob in waterAtList:
            if type(ob) is not Water:
                waterAtList.remove(ob)
        return waterAtList

    def treeAt(self,row,col):
        treeAtList = self.globalMap[row, col].copy()
        for ob in treeAtList:
            if type(ob) is not Tree:
                treeAtList.remove(ob)
        return treeAtList

    def foodAt(self, row, col):
        """Given a row and column, returns the food at that location."""
        foodAtList = self.globalMap[row, col].copy()
        # print("Before: ", foodAtList)
        for ob in foodAtList:
            if type(ob) is Food:
                return [ob]
        return []
        #TODO: There used to be a bug here where it would fail to remove some objects that were not food.
        # This caused len(this list) to be > 1, which caused agents to choose 'eat' over and over
        # print(len(foodAtList))
        # for ob in foodAtList:
        #     print(type(ob))
        #     print(ob)
        #     if type(ob) is not Food:
        #         foodAtList.remove(ob)
        # print("After: ", foodAtList)
        # return foodAtList


    def agentsAt(self, row, col):
        # TODO: Potential issue here
        """Given a row and column, returns a list of the agents at that location."""
        agentAtList = self.globalMap[row, col].copy()
        for ob in agentAtList:
            if type(ob) is not Agent:
                agentAtList.remove(ob)
        return agentAtList

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
            self.globalMap[r, c].append(nextAgent)

    def _placeStones(self):
        for i in range(self.numStones):
            (randRow, randCol) = self._genRandomLoc()
            while True:
                if len(self.globalMap[randRow, randCol]) != 0:
                    (randRow, randCol) = self._genRandomLoc()
                else:
                    break
            nextStone = Stone(initPose=(randRow, randCol), geneticString="0")
            self.stoneList.append(nextStone)
            self.globalMap[randRow, randCol].append(nextStone)

    def _placePits(self):
        for i in range(self.numPits):
            (randRow, randCol) = self._genRandomLoc()
            while True:
                if len(self.globalMap[randRow, randCol]) != 0:
                    (randRow, randCol) = self._genRandomLoc()
                else:
                    break
            nextPit = Pit(initPose=(randRow, randCol), geneticString="0")
            self.pitList.append(nextPit)
            self.globalMap[randRow, randCol].append(nextPit)

    def _placeWaters(self):
        self._placePonds(self.numPonds)
        self._placeRivers()

    def _placePonds(self, numPonds, pondSize=random.choice([3,3])):
        for i in range(numPonds):
            thisPondSize = random.randint(1,pondSize)
            rowLoc = random.randint(0, self.gridSize - thisPondSize)
            colLoc = random.randint(0, self.gridSize - thisPondSize)
            # print("row, col: ", rowLoc, colLoc)
            for row in range(thisPondSize):
                for col in range(thisPondSize):
                    isWaterHere = random.choice([1, 1])
                    if isWaterHere == 1:
                        if len(self.objectsAt(rowLoc + row, colLoc + col)) == 0:
                            nextWater = Water(initPose=(rowLoc + row, colLoc + col), geneticString="0")
                            self.waterList.append(nextWater)
                            self.globalMap[rowLoc + row, colLoc + col].append(nextWater)

    def _placeRivers(self):
        for numberOfRivers in range(self.numRivers):
            randomOrientation = random.randint(0, 1)

            place = random.randint(0, self.gridSize-1)
            for i in range(self.gridSize):
                while True:
                    place = random.choice([place-1, place, place+1])
                    if place < 0 or place > self.gridSize-1:
                        place = random.choice([place - 1, place, place + 1])
                    else:
                        break

                if randomOrientation == 0:
                    if len(self.objectsAt(i, place)) == 0:
                        nextWater = Water(initPose=(i, place), geneticString="0")
                        self.waterList.append(nextWater)
                        self.globalMap[i, place].append(nextWater)

                elif randomOrientation == 1:
                    if len(self.objectsAt(place, i)) == 0:
                        nextWater = Water(initPose=(place, i), geneticString="0")
                        self.waterList.append(nextWater)
                        self.globalMap[place, i].append(nextWater)

    def dist(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def make_circle(self, tiles, cx, cy, r):
        for x in range(cx - r, cx + r):
            for y in range(cy - r, cy + r):
                if self.dist(cx, cy, x, y) <= r:
                    tiles[x][y] = 1


    def _placeTreesOnHalf(self):
        for row in range(self.gridSize):
            for col in range(self.gridSize//2):
                if len(self.objectsAt(row,col)) == 0:
                    nextTree = Tree(initPose=(row,col),
                                    geneticString=random.choice(["1"]))
                    self.treeList.append(nextTree)
                    self.globalMap[row,col].append(nextTree)

    def _placeTrees(self, numForests, forestSize):

        r = forestSize // 2
        # r = self.gridSize

        for forest in range(numForests):
            rowLoc = random.randint(-r + 1, self.gridSize - r + 1)
            colLoc = random.randint(-r + 1, self.gridSize - r + 1)
            # print("row, col: ", rowLoc, colLoc)

            width = forestSize
            height = forestSize

            cx = width // 2
            cy = height // 2

            tiles = [[0 for _ in range(height)] for _ in range(width)]

            self.make_circle(tiles, cx, cy, r)

            for i in range(len(tiles)):
                for j in range(len(tiles)):
                    isTreeHere = random.choice([0, 1, 1])
                    if tiles[i][j] == 1:
                        if isTreeHere == 1:
                            if self.gridSize > rowLoc + i >= 0 and self.gridSize > colLoc + j >= 0:
                                if len(self.objectsAt(rowLoc + i, colLoc + j)) == 0:
                                    nextTree = Tree(initPose=(rowLoc + i, colLoc + j), geneticString=random.choice(["0","0","0","0","1"]))
                                    # print(nextTree.geneticString)
                                    # print(nextTree.getCanGrowFood())
                                    self.treeList.append(nextTree)
                                    self.globalMap[rowLoc + i, colLoc + j].append(nextTree)


        # print("\n".join("".join(map(str, i)) for i in tiles))


        # for i in range(numForrests):
        #     rowLoc = random.randint(0, self.gridSize - forrestSize)
        #     colLoc = random.randint(0, self.gridSize - forrestSize)
        #
        #     print("row, col: ", rowLoc, colLoc)
        #
        #     for row in range(forrestSize):
        #         for col in range(forrestSize):
        #             isTreeHere = random.randint(0, 1)
        #             if isTreeHere == 1:
        #                 if len(self.objectsAt(rowLoc + row, colLoc + col)) == 0:
        #                     nextTree = Tree(initPose=(rowLoc + row, colLoc + col), geneticString="0")
        #                     self.treeList.append(nextTree)
        #                     self.globalMap[rowLoc + row, colLoc + col].append(nextTree)

        # for i in range(self.numTrees):
        #     (randRow, randCol) = self._genRandomLoc()
        #     while True:
        #         if len(self.globalMap[randRow, randCol]) != 0:
        #             (randRow, randCol) = self._genRandomLoc()
        #         else:
        #             break
        #     nextTree = Tree(initPose=(randRow, randCol), geneticString="0")
        #     self.treeList.append(nextTree)
        #     self.globalMap[randRow, randCol].append(nextTree)


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
        for row in range(self.gridSize):
            for col in range(self.gridSize):
                if len(self.globalMap[row, col]) == 0:
                    print("|       |", end="")
                else:
                    for i in range(len(self.globalMap[row, col])):
                        print("|   " + str(self.globalMap[row, col][i].getTypeAbbreviation()) + "   |", end="")

            print("\n")

    def _agentStringCodes(self, row, col):
        """Produces three strings for the first three agents (if that many) sitting in
        the given cell."""
        agentStr = "{0:s}{1:<3d}|"
        emptyStr = "    |"
        strings = [emptyStr, emptyStr, emptyStr]
        agentsHere = self.globalMap[row, col]
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
        self.stepNum += 1
        # if self.time != 24:
        #     self.time += 1
        # else:
        #     self.time = 0
        self._growFood()
        self._updateAgents()

        print("--------------------------------------------------------------------------------------------")

        # for i in range(len(self.agentList)):
        #     print("\n\n")
        #     print("==== AGENT COLOR: " + str(self.agentList[i].colorNumberToText(self.agentList[i].getColor())) + " ====")
        #     print("~ Energy ~")
        #     print("   ", self.agentList[i].getEnergy())
        #     print(self.agentList)
        #     print(self.getDeadAgents())
        #     print("~ Vision ~")
        #     self.agentList[i]._printVision(self)
        #     print("~ Smell Food ~")
        #     self.agentList[i]._printSmell(self, "food")

            # print("~ Smell Agent ~")
            # self.agentList[i]._printSmell(self, "agent")
            # print(self.agentList[i].detectSmellRadius(self), "agent")

        # self.printGrid()
        # print(self.globalMap)
        # print("self.globalMap:",self.globalMap)


    def _growFood(self):
        """Updates every cell in the food map with more food, up to the maximum amount"""
        # Grow food
        for cell in self.globalMap:
            foodAmt = self.globalMap[cell]
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

            agent = self.agentList[i]
            agentR, agentC, agentH = agent.getPose()
            rAhead, cAhead = self.agentList[i]._computeAhead(self.gridSize)

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
            isOkay = True

            if not agent.isDead:
                action = agent.determineAction(self, self.agentList[i], self.time)
                print(agent.colorNumberToText(agent.getColor()), action)
                if action == 'breed':
                    twoAgents = []
                    agentsHere = self.agentsAt(agentR,agentC)
                    for i in range(2):
                        # print(type(ob))
                        # if ob is Agent:
                        twoAgents.append(agentsHere[i])
                        # print("twoAgents",twoAgents)
                    self.makeABaby(twoAgents[0], twoAgents[1])
                    for ag in agentsHere:
                        ag.setReadyToBreed(24)
                    isOkay = agent.changeEnergy(-1)

                elif action == 'eat':
                    self.eatFood(agentR, agentC)
                    isOkay = agent.changeEnergy(50)

                elif action == 'attack':
                    self.agentList[i].attackCreature(self, agentR, agentC)
                    isOkay = agent.changeEnergy(50)

                elif action == 'forward':
                    agent.updatePose(rAhead, cAhead, agentH)
                    # TODO: this if shouldn't be here, and it should remove the agent every time it moves
                    if agent in (self.globalMap[agentR, agentC]):
                        # print("REMOVING",agent,"from globalMap")
                        self.globalMap[agentR, agentC].remove(agent)
                        # print(self.globalMap)

                    self.globalMap[rAhead, cAhead].append(agent)
                    # print("globalMap:",self.globalMap)
                    agentR, agentC = rAhead, cAhead
                    isOkay = agent.changeEnergy(-1)

                elif action == 'left':
                    agent.updatePose(agentR, agentC, agent._leftTurn())
                    isOkay = agent.changeEnergy(-1)

                elif action == 'right':
                    agent.updatePose(agentR, agentC, agent._rightTurn())
                    isOkay = agent.changeEnergy(-1)

                elif action == 'turnAround':
                    agent.updatePose(agentR, agentC, agent._turnAround())
                    isOkay = agent.changeEnergy(-1)

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


            # for j in range(len(self.agentList)-1):
            #     print("AGENT 1 ID: ", self.agentList[j].getVisId)
            #     print("AGENT 2 ID: ", self.agentList[j+1].getVisId)
            #     if self.agentList[j].getVisId == self.agentList[j+1].getVisId:
            #         print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DUPLICATE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


            if len(self.agentList) != len(set(self.agentList)):
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DUPLICATES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            if agent.energy <= 0:
                isOkay = False

            # if isOkay:
            #     i = i + 1

            if not isOkay:
                self.deadAgents.append((agent, self.stepNum-agent.stepSpawned))
                self.agentList.pop(i)
                if agent in self.globalMap[agentR,agentC]:
                    self.globalMap[agentR, agentC].remove(agent)
                i = i + 1

            if isOkay:
                i = i + 1

    def _assessFood(self, row, col):
        """Given a row and column, examine the amount of food there, and divide it into
        no food, some food, and plentiful food: returning 0, 1, or 2."""
        # print("AssessFood")
        foodAmt = self.foodAt(row, col)
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
        creatureAmt = self.agentsAt(row,col)

        if creatureAmt == []:
            # print("no creature ahead")
            return 0

        elif len(creatureAmt) >= 1:
            for i in range(len(creatureAmt)):
                if agent.getColor() == creatureAmt[i].getColor():
                    return 2
            return 1

    def _assessCreatureHere(self, row, col):
        """Given a row and column, examine the amount of creatures there, and divide it into
        no creatures, and some creatures: returning 0 or 1."""
        # print("Looking at current location: (" + str(row) + "," + str(col) + ")")
        creatureAmt = self.agentsAt(row,col)
        # print("creatureHere",creatureAmt)
        # for i in range(len(creatureAmt)):
        #     print(creatureAmt[i].getColor())
        #print("Row and Col: " + str(row) + ", " + str(col))
        #print("self: " + str(self))

        if len(creatureAmt) <= 1:
            return 0
        else:
            for i in range(len(creatureAmt)-1):
                if creatureAmt[i].getColor() != creatureAmt[i+1].getColor():
                    return 1
            return 2

    def _assessObjectsHere(self, row, col, agent):
        listOfObjects = self.globalMap[row, col]
        # print("listOfObjects",listOfObjects)
        if listOfObjects != []:
            for ob in listOfObjects:
                if type(ob) is Tree:
                    return 4
                elif type(ob) is Stone:
                    return -1
                elif type(ob) is Agent:
                    if ob.getColor() == agent.getColor():
                        return 2
                    else:
                        return 1
                elif type(ob) is Food:
                    return 3
                elif type(ob) is Water:
                    return -2
                elif type(ob) is Pit:
                    return -3
        return 0

    def _listOfObjectsHere(self, row, col, agent):
        listOfObjects = self.globalMap[row, col]
        # print("listOfObjects",listOfObjects)
        listOfObjectsHere = []

        if listOfObjects != []:
            for ob in listOfObjects:
                if type(ob) is Stone:
                    listOfObjectsHere.append(-1)
                elif type(ob) is Agent:
                    if ob.getColor() == agent.getColor():
                        listOfObjectsHere.append(2)
                    else:
                        listOfObjectsHere.append(1)
                elif type(ob) is Food:
                    listOfObjectsHere.append(3)
                elif type(ob) is Water:
                    listOfObjectsHere.append(-2)
                elif type(ob) is Tree:
                    listOfObjectsHere.append(4)
                elif type(ob) is Pit:
                    listOfObjectsHere.append(-3)
        return listOfObjectsHere

    def eatFood(self, row, col):
        """Determines what, if any, food is eaten from the current given location. It returns the
        energy value of the food eaten, and updates the foodMap."""
        foodAtCell = self.foodAt(row, col)
        if len(foodAtCell) > 0:
            self.eatenFood.append(foodAtCell)
            for ob in self.globalMap[row, col]:
                if type(ob) is Food:
                    self.globalMap[row, col].remove(ob) #TODO: what if there is something else on that square other than food?

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
            halfway = round(len(agent1.getGeneticString()) / 2)
            babyGeneticStringPart1 = agent1GeneticString[:halfway]
            babyGeneticStringPart2 = agent2GeneticString[halfway:]

            babyGeneticString = babyGeneticStringPart1 + babyGeneticStringPart2

            newBabyGeneticString = self.mutate(babyGeneticString)

            babyAgent = Agent(geneticString=newBabyGeneticString, initPose=agentPose, stepSpawned=self.stepNum)
            # print(self.stepNum)
            # print("baby",babyAgent.stepSpawned)

            self.agentList.append(babyAgent)
            self.globalMap[r,c].append(babyAgent)

            agent1.setReadyToBreed(24)
            agent2.setReadyToBreed(24)

    def mutate(self, babyGeneticString):
        newBabyGeneticString = babyGeneticString
        randElem = random.randrange(len(babyGeneticString))
        newVal = 0
        if randElem == 0:
            newVal =  random.choice([0, 1, 2, 3])
        elif randElem == 1:
            newVal =  random.choice([0, 1, 2])
        elif randElem == 2:
            newVal =  random.choice([0, 1])
        elif randElem == 3:
            newVal =  random.choice([0, 1])
        elif randElem == 4:
            newVal = random.choice([0, 1])
        elif randElem == 5:
            newVal = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        elif randElem == 6:
            newVal = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        elif randElem == 7:
            newVal = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        elif randElem == 8:
            newVal = random.choice([0, 1])

        babyGeneticStringAsList = list(newBabyGeneticString)
        print(babyGeneticStringAsList)
        babyGeneticStringAsList[randElem] = newVal
        newBabyGeneticString = ""
        for j in range(len(babyGeneticStringAsList)):
            newBabyGeneticString+=str(babyGeneticStringAsList[j])
        print(newBabyGeneticString)
        return newBabyGeneticString



