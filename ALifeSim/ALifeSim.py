import random
import tkinter
import math
from ALifeGUI import *

# Import all objects used in the simulation.
from Object import *
from Agent import *
from Stone import *
from Food import *
from Water import *
from Tree import *
from Pit import *
from Sand import *
from Snow import *
from Grass import *
from Mushroom import *

class ALifeSimTest(object):
    """An artificial life predator/prey simulation, similar to NetLogo, with agents that each perform their own
    set of behaviors. Each cell can have objects on it, and agents base their actions on detected objects.
    Each agent has a genetic string that determines their characteristics such as behavior patterns and energy level."""

    FOOD_PERCENT = 0.01
    NEW_FOOD_PERCENT = 0.005
    GROWTH_RATE = 0.005
    MAX_FOOD = 1
    time = 12
    numStones = 15
    numForest = 0
    numPonds = 0
    numRivers = 0
    numWaters = 0
    numTrees = 0
    numPits = 0
    numSands = 0
    numSnows = 0
    numGrass = 0
    numMushrooms = 0

    def __init__(self, gridSize, numAgents, numStones, numForests, numRivers, numPonds, geneticStrings):
        """Takes in the side length of the grid, as well as what objects to place in the simulation.
        Creates the simulation and initializes variables based on the input."""
        self.gridSize = gridSize

        self.numAgents = numAgents
        self.numStones = numStones
        self.numWaters = 0
        self.numTrees = 10
        self.numRivers = numRivers
        self.numPonds = numPonds
        self.numForests = numForests
        self.numPits = 5
        self.numMushrooms = 5
        #TODO: make this a user input?
        self.numSands = (self.gridSize * self.gridSize) // 100
        self.numSnows = (self.gridSize * self.gridSize) // 100
        self.numGrass = (self.gridSize * self.gridSize) // 50

        self.initialGeneticStrings = geneticStrings
        self.maxFood = 0
        self.globalMap = dict()

        for row in range(gridSize):
            for col in range(gridSize):
                self.globalMap[row, col] = []

        self.foodList = []
        self.stoneList = []
        self.pitList = []
        self.grassDict = {}
        self.sandDict = {}
        self.snowDict = {}
        self.mushroomList = []
        self.waterList = []
        self.treeList = []
        self.agentList = []
        self.deadAgents = []
        self.eatenFood = []
        self.eatenMushrooms = []
        self.agentList = []
        self.stepNum = 0
        self.verbose = False

        for row in range(self.gridSize):
            for col in range(self.gridSize):
                self.grassDict[row,col] = []
                self.sandDict[row,col] = []
                self.snowDict[row,col] = []

        self._placeWaters()

        # objects w/ no effect
        self._placeGrass()
        self._placeSand()
        self._placeSnow()

        # inanimate objects
        # self._placeTreesOnHalf()
        self._placePits()
        self._placeMushrooms()
        self._placeTrees(self.numForests, random.randint(3, 10))
        self._placeStones()
        self._placeFood()

        # agent objects
        self._placeAgents()

    # =================================================================
    # Getter functions
    def getSize(self):
        """Returns the side length of the grid"""
        return self.gridSize

    def getAgentNumber(self):
        """Returns the number of agents placed on the grid"""
        return self.numAgents

    def getFood(self):
        """Returns the list of food objects"""
        return self.foodList[:]

    def getAgents(self):
        """Returns the list of agent objects"""
        return self.agentList[:]

    def getStones(self):
        """Returns the list of stone objects"""
        return self.stoneList[:]

    def getPits(self):
        """Returns the list of pit objects"""
        return self.pitList[:]

    def getMushrooms(self):
        """Returns the list of mushroom objects"""
        return self.mushroomList[:]

    def getGrass(self):
        """Returns the list of grass objects, with the keys being their row and col numbers"""
        return self.grassDict[:]

    def getSands(self):
        """Returns the list of sand objects, with the keys being their row and col numbers"""
        return self.sandDict[:]

    def getSnows(self):
        """Returns the list of snow objects, with the keys being their row and col numbers"""
        return self.snowDict[:]

    def getWaters(self):
        """Returns the list of water objects"""
        return self.waterList[:]

    def getTrees(self):
        """Returns the list of tree objects"""
        return self.treeList[:]

    def getDeadAgents(self):
        """Returns a list of the dead agents."""
        return self.deadAgents

    def getEatenFood(self):
        """Returns a list of the food eaten."""
        return self.eatenFood[:]

    def getEatenMushrooms(self):
        """Returns a list of the mushrooms eaten."""
        return self.eatenMushrooms[:]

    # =================================================================
    # Checking the grid functions
    def stonesAt(self, row, col):
        """Given a row and column, returns a list of the stones at that location."""
        objectsHereList = self.globalMap[row, col].copy()
        stonesAtList = objectsHereList.copy()
        for ob in objectsHereList:
            if type(ob) is not Stone:
                stonesAtList.remove(ob)
        return stonesAtList

    def pitAt(self, row, col):
        """Given a row and column, returns a list of the pits at that location."""
        objectsHereList = self.globalMap[row, col].copy()
        pitsAtList = objectsHereList.copy()
        for ob in objectsHereList:
            if type(ob) is not Pit:
                pitsAtList.remove(ob)
        return pitsAtList

    def mushroomAt(self, row, col):
        """Given a row and column, returns a list of the mushrooms at that location."""
        objectsHereList = self.globalMap[row, col].copy()
        mushroomsAtList = objectsHereList.copy()
        for ob in objectsHereList:
            if type(ob) is not Mushroom:
                mushroomsAtList.remove(ob)
        return mushroomsAtList

    def grassAt(self, row, col):
        """Given a row and column, returns a list of the grass objects at that location."""
        return self.grassDict[row,col]

    def sandAt(self, row, col):
        """Given a row and column, returns a list of the sand objects at that location."""
        return self.sandDict[row,col]

    def snowAt(self, row, col):
        """Given a row and column, returns a list of the snow objects at that location."""
        return self.snowDict[row,col]

    def waterAt(self,row,col):
        """Given a row and column, returns a list of the water objects at that location."""
        objectsHereList = self.globalMap[row, col].copy()
        waterAtList = objectsHereList.copy()
        for ob in objectsHereList:
            if type(ob) is not Water:
                waterAtList.remove(ob)
        return waterAtList

    def treeAt(self,row,col):
        """Given a row and column, returns a list of the tree objects at that location."""
        objectsHereList = self.globalMap[row, col].copy()
        treeAtList = objectsHereList.copy()
        for ob in objectsHereList:
            if type(ob) is not Tree:
                treeAtList.remove(ob)
        return treeAtList

    def foodAt(self, row, col):
        """Given a row and column, returns a list of the food objects at that location."""
        objectsHereList = self.globalMap[row, col].copy()
        foodAtList = objectsHereList.copy()
        for ob in objectsHereList:
            if type(ob) is Food:
                return [ob]
        return []
        #TODO: There used to be a bug here where it would fail to remove some objects that were not food.
        # This caused len(this list) to be > 1, which caused agents to choose 'eat' over and over.
        # How to test if it's fixed?

    def agentsAt(self, row, col):
        """Given a row and column, returns a list of the agents at that location."""
        objectsHereList = self.globalMap[row, col].copy()
        agentAtList = objectsHereList.copy()
        for ob in objectsHereList:
            if type(ob) is not Agent:
                agentAtList.remove(ob)
        return agentAtList

    def objectsAt(self, row, col):
        """Given a row and column, returns a list of all objects at the location."""
        return self.globalMap[row, col]

    def _assessFood(self, row, col):
        """Given a row and column, examine the food there, and return 3 if food exists there."""
        #TODO: do we need this function?
        foodAmt = self.foodAt(row, col)
        if len(foodAmt) > 0:
            return 3
        else:
            return 0

    def _assessCreature(self, row, col, agent):
        """Given a row and column, examine the agents there, and divide it into
        no creatures, friendly creatures, and enemy creatures, returning 0, 2, or 1 respectively."""
        creatureAmt = self.agentsAt(row,col)

        if creatureAmt == []:
            return 0

        elif len(creatureAmt) >= 1:
            for i in range(len(creatureAmt)):
                if agent.getColor() == creatureAmt[i].getColor():
                    return 2
            return 1

    def _assessCreatureHere(self, row, col):
        """Given a row and column, examine the creatures there, and divide it into
        no creatures, creatures with the same color, and creatures with different colors,
        returning 0, 2, or 1 respectively."""
        creatureAmt = self.agentsAt(row,col)
        # for i in range(len(creatureAmt)):
        #     print(creatureAmt[i].getColor())

        if len(creatureAmt) <= 1:
            return 0
        else:
            for i in range(len(creatureAmt)-1):
                if creatureAmt[i].getColor() != creatureAmt[i+1].getColor():
                    return 1
            return 2

    def _assessObjectsHere(self, row, col, agent):
        """Given a row and column, examine the objects there, return a number corresponding to the most
        important object there."""
        listOfObjects = self.globalMap[row, col]
        # print("listOfObjects",listOfObjects)
        if listOfObjects != []:
            if len(agent.removeSelfFromList(self.treeAt(row, col))) > 0:
                return agent.removeSelfFromList(self.treeAt(row, col))[0]
            elif len(agent.removeSelfFromList(self.stonesAt(row, col))) > 0:
                return agent.removeSelfFromList(self.stonesAt(row, col))[0]
            elif len(agent.removeSelfFromList(self.agentsAt(row, col))) > 0:
                return agent.removeSelfFromList(self.agentsAt(row, col))[0]
            elif len(agent.removeSelfFromList(self.foodAt(row, col))) > 0:
                return agent.removeSelfFromList(self.foodAt(row, col))[0]
            elif len(agent.removeSelfFromList(self.waterAt(row, col))) > 0:
                return agent.removeSelfFromList(self.waterAt(row, col))[0]
            elif len(agent.removeSelfFromList(self.mushroomAt(row, col))) > 0:
                return agent.removeSelfFromList(self.mushroomAt(row, col))[0]
            elif len(agent.removeSelfFromList(self.pitAt(row, col))) > 0:
                return agent.removeSelfFromList(self.pitAt(row, col))[0]
        return None

    def _listOfObjectsHere(self, row, col, agent):
        """Looks at the global map, returns all objects at a location."""
        listOfObjects = self.globalMap[row, col].copy()
        return listOfObjects

    def _agentStringCodes(self, row, col):
        """Produces three strings for the first three agents (if that many) sitting in the given cell."""
        #TODO: Remove this function? Do we ever use it?
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

    # =================================================================
    # Functions to place objects on the grid -- used to initialize simulation.
    def _placeFood(self):
        """Places food objects in random clumps so that roughly self.percentFood cells have food."""
        totalCells = self.gridSize ** 2
        foodClumps = int(self.FOOD_PERCENT * totalCells)
        for i in range(foodClumps):
            self._addFoodClump()

    def _placeAgents(self):
        """Places agent objects randomly, avoiding locations where the globalMap already contains something"""
        for i in range(self.numAgents):
            while True:
                agentPose = self._genRandomPose()
                (r, c, h) = agentPose
                if len(self.globalMap[r, c]) == 0:
                    break

            if self.initialGeneticStrings is None or len(self.initialGeneticStrings) <= i:
                nextAgent = Agent(initPose = agentPose,stepSpawned=self.stepNum)
            else:
                nextAgent = Agent(geneticString=self.initialGeneticStrings[i], initPose = agentPose,stepSpawned=self.stepNum)

            if self.initialGeneticStrings is None:
                pass

            self.agentList.append(nextAgent)
            self.globalMap[r, c].append(nextAgent)

    def _placeStones(self):
        """Places stone objects randomly, avoiding locations where the globalMap already contains something"""
        for i in range(self.numStones):
            (randRow, randCol) = self._genRandomLoc()
            while True:
                if len(self.globalMap[randRow, randCol]) != 0:
                    (randRow, randCol) = self._genRandomLoc()
                else:
                    break
            nextStone = Stone(initPose=(randRow, randCol), geneticString="0", stepSpawned=self.stepNum)
            self.stoneList.append(nextStone)
            self.globalMap[randRow, randCol].append(nextStone)

    def _placePits(self):
        """Places pit objects randomly, avoiding locations where the globalMap already contains something"""
        for i in range(self.numPits):
            (randRow, randCol) = self._genRandomLoc()
            while True:
                if len(self.globalMap[randRow, randCol]) != 0:
                    (randRow, randCol) = self._genRandomLoc()
                else:
                    break
            nextPit = Pit(initPose=(randRow, randCol), geneticString="0", stepSpawned=self.stepNum)
            self.pitList.append(nextPit)
            self.globalMap[randRow, randCol].append(nextPit)

    def _placeMushrooms(self):
        """Places mushroom objects randomly, avoiding locations where the globalMap already contains something"""
        for i in range(self.numMushrooms):
            (randRow, randCol) = self._genRandomLoc()
            while True:
                if len(self.globalMap[randRow, randCol]) != 0:
                    (randRow, randCol) = self._genRandomLoc()
                else:
                    break
            nextMushroom = Mushroom(initPose=(randRow, randCol), geneticString=random.choice(["0","1","1","1","1","1","1","1","1","2","3","4"]), stepSpawned=self.stepNum)
            self.mushroomList.append(nextMushroom)
            self.globalMap[randRow, randCol].append(nextMushroom)

    def _placeGrass(self):
        """Places patches of grass objects randomly."""
        for grassPatch in range(self.numGrass):
            r = random.randint(1, self.gridSize // 5)
            rowLoc = random.randint(-r + 1, self.gridSize - r + 1)
            colLoc = random.randint(-r + 1, self.gridSize - r + 1)
            width = r*2
            height = r*2
            cx = width // 2
            cy = height // 2
            tiles = [[0 for _ in range(height)] for _ in range(width)]

            self.make_circle(tiles, cx, cy, r)

            for i in range(len(tiles)):
                for j in range(len(tiles)):
                    isGrassHere = random.choice([0, 1, 1])
                    if tiles[i][j] == 1:
                        if isGrassHere == 1:
                            if self.gridSize > rowLoc + i >= 0 and self.gridSize > colLoc + j >= 0:
                                if len(self.objectsAt(rowLoc + i, colLoc + j)) == 0:
                                    nextGrass = Grass(initPose=(rowLoc + i, colLoc + j),
                                                    geneticString=random.choice(["0"]),
                                                    stepSpawned=self.stepNum)
                                    self.grassDict[rowLoc+i,colLoc+j].append(nextGrass)

    def _placeSand(self):
        """Places patches of sand objects randomly."""
        for sandPatch in range(self.numSands):
            r = random.randint(1, self.gridSize // 5)
            rowLoc = random.randint(-r + 1, self.gridSize - r + 1)
            colLoc = random.randint(-r + 1, self.gridSize - r + 1)
            width = r*2
            height = r*2
            cx = width // 2
            cy = height // 2
            tiles = [[0 for _ in range(height)] for _ in range(width)]

            self.make_circle(tiles, cx, cy, r)

            for i in range(len(tiles)):
                for j in range(len(tiles)):
                    isSandHere = random.choice([0, 1, 1])
                    if tiles[i][j] == 1:
                        if isSandHere == 1:
                            if self.gridSize > rowLoc + i >= 0 and self.gridSize > colLoc + j >= 0:
                                if len(self.objectsAt(rowLoc + i, colLoc + j)) == 0:
                                    nextSand = Sand(initPose=(rowLoc + i, colLoc + j),
                                                    geneticString=random.choice(["0"]),
                                                    stepSpawned=self.stepNum)
                                    self.sandDict[rowLoc+i,colLoc+j].append(nextSand)

    def _placeSnow(self):
        """Places patches of snow objects randomly."""
        #TODO: make this place snow objects in natural patterns -- high elevation has higher likelihood? Tree+snow?
        for snowPatch in range(self.numSnows):
            r = random.randint(1, self.gridSize // 5)
            rowLoc = random.randint(-r + 1, self.gridSize - r + 1)
            colLoc = random.randint(-r + 1, self.gridSize - r + 1)
            width = r*2
            height = r*2
            cx = width // 2
            cy = height // 2
            tiles = [[0 for _ in range(height)] for _ in range(width)]

            self.make_circle(tiles, cx, cy, r)

            for i in range(len(tiles)):
                for j in range(len(tiles)):
                    isSnowHere = random.choice([0, 1, 1])
                    if tiles[i][j] == 1:
                        if isSnowHere == 1:
                            if self.gridSize > rowLoc + i >= 0 and self.gridSize > colLoc + j >= 0:
                                if len(self.objectsAt(rowLoc + i, colLoc + j)) == 0:
                                    nextSnow = Snow(initPose=(rowLoc + i, colLoc + j),
                                                    geneticString=random.choice(["0"]),
                                                    stepSpawned=self.stepNum)
                                    self.snowDict[rowLoc+i,colLoc+j].append(nextSnow)

    def _placeWaters(self):
        """Places water objects in the form of rivers and ponds,
        avoiding locations where the globalMap already contains something"""
        self._placePonds(self.numPonds)
        self._placeRivers()

    def _placePonds(self, numPonds, pondSize=random.choice([3,3])):
        """Places water objects in the form of square clusters,
        avoiding locations where the globalMap already contains something"""
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
                            nextWater = Water(initPose=(rowLoc + row, colLoc + col), geneticString="0", stepSpawned=self.stepNum)
                            self.waterList.append(nextWater)
                            self.globalMap[rowLoc + row, colLoc + col].append(nextWater)

    def _placeRivers(self):
        """Places water objects in the form of vertical or horizontal rivers,
        avoiding locations where the globalMap already contains something"""
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
                        nextWater = Water(initPose=(i, place), geneticString="0", stepSpawned=self.stepNum)
                        self.waterList.append(nextWater)
                        self.globalMap[i, place].append(nextWater)

                elif randomOrientation == 1:
                    if len(self.objectsAt(place, i)) == 0:
                        nextWater = Water(initPose=(place, i), geneticString="0", stepSpawned=self.stepNum)
                        self.waterList.append(nextWater)
                        self.globalMap[place, i].append(nextWater)

    def _placeTreesOnHalf(self):
        """Places berry trees on the left half of the simulation, avoiding objects that were placed first."""
        for row in range(self.gridSize):
            for col in range(self.gridSize//2):
                if len(self.objectsAt(row,col)) == 0:
                    nextTree = Tree(initPose=(row,col),geneticString=random.choice(["1"]),stepSpawned=self.stepNum)
                    self.treeList.append(nextTree)
                    self.globalMap[row,col].append(nextTree)

    def _placeTrees(self, numForests, forestSize):
        """Randomly places trees in forest (circular) patterns, with diameters of forestSize."""
        r = forestSize // 2

        for forest in range(numForests):
            rowLoc = random.randint(-r + 1, self.gridSize - r + 1)
            colLoc = random.randint(-r + 1, self.gridSize - r + 1)

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
                                    nextTree = Tree(initPose=(rowLoc + i, colLoc + j), geneticString=random.choice(["0","0","0","0","1"]),stepSpawned=self.stepNum)
                                    self.treeList.append(nextTree)
                                    self.globalMap[rowLoc + i, colLoc + j].append(nextTree)

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
        #                     nextTree = Tree(initPose=(rowLoc + row, colLoc + col), geneticString="0",stepSpawned=self.stepNum)
        #                     self.treeList.append(nextTree)
        #                     self.globalMap[rowLoc + row, colLoc + col].append(nextTree)

        # for i in range(self.numTrees):
        #     (randRow, randCol) = self._genRandomLoc()
        #     while True:
        #         if len(self.globalMap[randRow, randCol]) != 0:
        #             (randRow, randCol) = self._genRandomLoc()
        #         else:
        #             break
        #     nextTree = Tree(initPose=(randRow, randCol), geneticString="0",stepSpawned=self.stepNum)
        #     self.treeList.append(nextTree)
        #     self.globalMap[randRow, randCol].append(nextTree)

    def _addFoodClump(self):
        """Adds a clump of food at a random location, avoiding preexisting objects."""
        (randRow, randCol) = self._genRandomLoc()
        while True:
            if len(self.globalMap[randRow, randCol]) != 0:
                (randRow, randCol) = self._genRandomLoc()
            else:
                break
        nextFood = Food(initPose=(randRow, randCol),geneticString="0",stepSpawned=self.stepNum)
        self.foodList.append(nextFood)
        self.globalMap[randRow, randCol].append(nextFood)

    # =================================================================
    # Math helper functions
    def dist(self, x1, y1, x2, y2):
        """Takes in two points (x1,y1) and (x2,y2) and returns the distance between them"""
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def make_circle(self, tiles, cx, cy, r):
        """Generates a circular shape composed of square tiles"""
        for x in range(cx - r, cx + r):
            for y in range(cy - r, cy + r):
                if self.dist(cx, cy, x, y) <= r:
                    tiles[x][y] = 1

    def _genRandomPose(self):
        """Generates a random location and direction on the grid with equal probability."""
        row = random.randrange(self.gridSize)
        col = random.randrange(self.gridSize)
        heading = random.choice(['n', 'e', 'w', 's'])
        return (row, col, heading)

    def _genRandomLoc(self):
        """Generates a random location on the grid with equal probability."""
        row = random.randrange(self.gridSize)
        col = random.randrange(self.gridSize)
        return (row, col)

    # =================================================================
    # Updating the sim functions.
    def step(self):
        """Update one step of the simulation. This means updating each object, and updating each agent
        with its chosen behavior. That could also mean managing agents who "die" because they run out
        of energy."""
        if self.verbose:
            print("----------------------------------------- STEP " + str(self.stepNum) + " ---------------------------------------------------")
        self.stepNum += 1

        if self.time != 24:
            self.time += 1
        else:
            self.time = 0

        self._updateTrees()
        self._updateMushrooms()
        self._updateAgents()

        if self.verbose:
            print("--------------------------------------------------------------------------------------------")

    def _updateTrees(self):
        """Keeps track of when a tree should bloom, and makes them bloom when needed."""
        i = 0
        while i < len(self.treeList):
            tree = self.treeList[i]
            treeR, treeC = tree.getPose()
            if (tree.getStepsUntilBloom() >= 50):
                tree.setHasFood("-1")
                tree.setStepsUntilBloom(tree.getStepsUntilBloom() - 1)
                if tree.getStepsUntilBloom() < 50:
                    self.globalMap[treeR, treeC].append(tree)
                    tree.setHasFood("0")
            if (tree.getStepsUntilBloom() > 0) and (tree.getStepsUntilBloom() < 50):
                tree.setHasFood("0")
                tree.setStepsUntilBloom(tree.getStepsUntilBloom() - 1)
            if tree.getStepsUntilBloom() == 0:
                tree.setHasFood("1")
                # TODO: WHy can't we call this from the tree V ???
                # tree.setStepsUntilBloom(random.randint(10,40))
            i = i + 1

    def _updateMushrooms(self):
        """Keeps track of when a tree should bloom, and makes them bloom when needed."""
        i = 0
        while i < len(self.mushroomList):
            currentMushroom = self.mushroomList[i]
            r, c = currentMushroom.getPose()
            if currentMushroom.getStepsUntilGrowth() > 0:
                currentMushroom.setStepsUntilGrowth(currentMushroom.getStepsUntilGrowth() - 1)
            if currentMushroom.getStepsUntilGrowth() == 0:
                currentMushroom.setDroppingType(1)

            i = i + 1


    def _updateAgents(self):
        """Updates the each living agent based on its chosen action."""
        i = 0
        if self.verbose:
            print("aLifeSim object is using _updateAgents() for step " + str(self.stepNum))

        if self.verbose:
            print("--------------------------------------------------------------------------------------------")
        while i < len(self.agentList):

            if self.verbose:
                print("*************** AGENT COLOR: " + str(self.agentList[i].colorNumberToText(self.agentList[i].getColor())) + " ***************")

            agent = self.agentList[i]
            agentR, agentC, agentH = agent.getPose()
            rAhead, cAhead = agent._computeAhead(self.gridSize)

            if self.verbose:
                print("==== AGENT COLOR: " + str(self.agentList[i].colorNumberToText(self.agentList[i].getColor())) + " ====")
                print("Steps until healthy: ", agent.getStepsUntilHealthy())

            if agent.getStepsUntilHealthy() > 0:
                agent.isSick = True
                agent.setStepsUntilHealthy(agent.getStepsUntilHealthy() - agent.resistanceVal)
            if agent.getStepsUntilHealthy() <= 0:
                agent.isSick = False
                agent.setStepsUntilHealthy(0)

            # print("Steps until no mushroom influence: ", agent.getStepsUntilNoMushroomInfluence())
            if agent.getStepsUntilNoMushroomInfluence() > 0:
                agent.setStepsUntilNoMushroomInfluence(agent.getStepsUntilNoMushroomInfluence() - 1)
            if agent.getStepsUntilNoMushroomInfluence() <= 0:
                agent.mushroomInfluence = 0
                agent.setStepsUntilNoMushroomInfluence(0)
            isOkay = True

            if not agent.isDead:
                action = agent.determineAction(self, self.time)
                if action == 'breed':
                    twoAgents = []
                    agentsHere = self.agentsAt(agentR,agentC)
                    for i in range(2):
                        # print(type(ob))
                        # if ob is Agent:
                        twoAgents.append(agentsHere[i])
                    self.makeABaby(twoAgents[0], twoAgents[1])
                    for ag in agentsHere:
                        ag.setReadyToBreed(24)
                    isOkay = agent.changeEnergy(-1)

                elif action == 'eat':
                    self.eatItem(agent, agentR, agentC)
                    isOkay = agent.changeEnergy(0)

                elif action == 'eatBerries':
                    agent.setObjectConsumed(2)
                    isOkay = agent.changeEnergy(2)

                elif action == 'pause':
                    agent.updatePose(agentR, agentC, agent._leftTurn())
                    time.sleep(0.1)
                    agent.updatePose(agentR, agentC, agent._rightTurn())
                    time.sleep(0.1)
                    agent.updatePose(agentR, agentC, agent._turnAround())
                    isOkay = agent.changeEnergy(-5)

                elif action == 'roost':
                    isOkay = agent.changeEnergy(10)

                elif action == 'rest':
                    isOkay = agent.changeEnergy(2)

                elif action == 'attack':
                    self.agentList[i].attackCreature(self, agentR, agentC)
                    isOkay = agent.changeEnergy(50)

                elif action == 'forward':
                    agent.updatePose(rAhead, cAhead, agentH)
                    # TODO: this if shouldn't be here, and it should remove the agent every time it moves
                    if agent in (self.globalMap[agentR, agentC]):
                        # print("REMOVING",agent,"from globalMap")
                        self.globalMap[agentR, agentC].remove(agent)
                        # print("globalMap after removing before adding:")
                        # self.printGrid()
                    else:
                        pass
                        # print("Agent not where expected:", agent, agentR, agentC)
                        # self.printGrid()
                        # print("globalMap after removing before adding:",self.globalMap)

                    self.globalMap[rAhead, cAhead].append(agent)
                    # print("globalMap after removing AND adding:")
                    # self.printGrid()
                    # print("globalMap after removing AND adding:",self.globalMap)
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

                elif action == 'die':
                    agent.updatePose(agentR, agentC, agent._turnAround())
                    isOkay = agent.changeEnergy(-1000)

                else:
                    # print("Unknown action:", action)
                    isOkay = agent.changeEnergy(0)

                if self.verbose:
                    print("--------------------------------------------------------------------------------------------")

                if agent.getReadyToBreed() != 0:
                    agent.changeReadyToBreed(1)
                if self.verbose:
                    print("~~~~~~~~~ Energy After Step ~~~~~~~~~")
                    print("OBJECT CONSUMED:",agent.getObjectConsumed())
                    print("GlobalMap:",self.globalMap)
                    print("   ", self.agentList[i].getEnergy())
                    print("----------------------------------------------------------------------------")

            # for j in range(len(self.agentList)-1):
            #     print("AGENT 1 ID: ", self.agentList[j].getVisId)
            #     print("AGENT 2 ID: ", self.agentList[j+1].getVisId)
            #     if self.agentList[j].getVisId == self.agentList[j+1].getVisId:
            #         print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DUPLICATE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            # if len(self.agentList) != len(set(self.agentList)):
            #     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DUPLICATES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            # numAgentsInGlobalMap = 0
            # for r, c in self.globalMap:
            #     for n in self.globalMap[r, c]:
            #         if type(n) is Agent:
            #             numAgentsInGlobalMap += 1

            # if len(self.agentList) < numAgentsInGlobalMap:
            #     print("!!!!!!!!!! GHOST AGENT CREATED")
            #     print("agentList", self.agentList)
            #     for j in self.agentList:
            #         print(j)
            #     print("globalMap", self.globalMap)
            #
            # print('printGrid:',self.printGrid())

            if agent.energy <= 0:
                isOkay = False

            if not isOkay:
                self.deadAgents.append((agent, self.stepNum-agent.stepSpawned))
                agent.dropObject(self)
                self.agentList.pop(i)
                if agent in self.globalMap[agentR,agentC]:
                    self.globalMap[agentR, agentC].remove(agent)

            if isOkay:
                i = i + 1

    # =================================================================
    # Agent action functions
    def eatItem(self, agent, row, col):
        """Removes a food object from a location on the global map."""
        foodAtCell = self.foodAt(row, col)
        if len(foodAtCell) > 0:
            agent.changeEnergy(50)
            agent.setObjectConsumed(1)
            self.eatenFood.append(foodAtCell)
            for ob in self.globalMap[row, col]:
                if type(ob) is Food:
                    self.globalMap[row, col].remove(ob) #TODO: what if there is something else on that square other than food?
            for i in range(len(self.foodList)):
                if foodAtCell == self.foodList[i]:
                    self.foodList.pop(i)

        mushroomsAtCell = self.mushroomAt(row, col)
        if len(mushroomsAtCell) > 0:
            agent.setObjectConsumed(3)
            mushroomTypeEaten = mushroomsAtCell[0].getTypeOfMushroom()
            self.eatenMushrooms.append(mushroomsAtCell)
            agent.setMushroomInfluence(mushroomTypeEaten)
            agent.setStepsUntilNoMushroomInfluence(10)
            # print("MUSHROOM TYPE EATEN:", mushroomTypeEaten)
            if (mushroomTypeEaten == 4):
                agent.changeEnergy(-10)
            else:
                agent.changeEnergy(50)
            if (mushroomTypeEaten == 1):
                # print("SICK")
                agent.isSick = True
                agent.setStepsUntilHealthy(random.randint(10, 50))
            for ob in self.globalMap[row, col]:
                if type(ob) is Mushroom:
                    self.globalMap[row, col].remove(ob)
            for i in range(len(self.mushroomList)):
                if mushroomsAtCell == self.mushroomList[i]:
                    self.mushroomList.pop(i)

    def makeABaby(self, agent1, agent2):
        """Takes in two agents and produces a baby agent with a combination of their genetic strings
        plus a random mutation."""
        if agent1.getReadyToBreed() == 0 and agent2.getReadyToBreed() == 0:
            agentPose = agent1.getPose()
            r, c, h = agentPose

            agent1GeneticString = agent1.getGeneticString()
            agent2GeneticString = agent2.getGeneticString()

            babyGeneticString = ''
            geneticStringLength = len(agent1GeneticString)
            for i in range(geneticStringLength):
                if i % 2 == 0:
                    babyGeneticString = babyGeneticString + agent1GeneticString[i]
                else:
                    babyGeneticString = babyGeneticString + agent2GeneticString[i]

            # print("babyGeneticString before mutating", babyGeneticString)
            newBabyGeneticString = self.mutate(babyGeneticString)

            babyAgent = Agent(geneticString=newBabyGeneticString, initPose=agentPose, stepSpawned=self.stepNum)

            self.agentList.append(babyAgent)
            self.globalMap[r,c].append(babyAgent)

            agent1.setReadyToBreed(24)
            agent2.setReadyToBreed(24)

    def mutate(self, babyGeneticString):
        """Makes a random change to a genetic string."""
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
            newVal = random.choice([0, 0, 1])
        elif randElem == 9:
            newVal = random.choice([0, 0, 1])
        elif randElem == 10:
            newVal = random.choice([0, 0, 1])
        elif randElem == 11:
            newVal = random.choice([0, 0, 1])

        babyGeneticStringAsList = list(newBabyGeneticString)
        # print(babyGeneticStringAsList)
        babyGeneticStringAsList[randElem] = newVal
        newBabyGeneticString = ""
        for j in range(len(babyGeneticStringAsList)):
            newBabyGeneticString+=str(babyGeneticStringAsList[j])
        # print(newBabyGeneticString)
        return newBabyGeneticString

    # =================================================================
    # Print functions
    def printGrid(self):
        """Prints the globalMap."""
        for row in range(self.gridSize):
            for col in range(self.gridSize):
                if len(self.globalMap[row, col]) == 0:
                    print("|       |", end="")
                else:
                    for i in range(len(self.globalMap[row, col])):
                        print("|   " + str(self.globalMap[row, col][i].getTypeAbbreviation()) + "   |", end="")

            print("\n")

    def printAgents(self):
        """Prints the current location, heading, energy, genetic string, step spawned, and step died of each agent."""
        # TODO: Add steps created
        print("===== Live Agents =====")
        print("       Row  Col  Hed   Energy    Genetic String  StepFirst  StepDied")
        for agent in self.agentList:
            print(agent, "       ", "x", "         ", "x")
        print("===== Dead Agents =====")
        print("       Row  Col  Hed   Energy    Genetic String  StepFirst  StepDied")
        for agent, stepDied in self.deadAgents:
            print(agent, "       ", "x", "         ", stepDied)


