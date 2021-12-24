import random
from Object import Object
from ALifeSim import *

# Import objects the agent might interact with
from Tree import Tree
from Stone import Stone
from Water import Water
from Food import Food
from Pit import Pit
from Mushroom import Mushroom

class Agent(Object):
    """An agent object in the ALife simulation. An agent has a geneticString that governs its attributes and behavior,
    and it has a location on the globalMap (given when created and then updated)."""

    def __init__(self, initPose = (0, 0, 'n'), initEnergy = 40, geneticString = "0000000000", stepSpawned=0):
        """
        Sets up an agent with a location, energy, geneticString, and step created
        :param initPose:   tuple giving agent's initial location and heading
        :param initEnergy: integer initial energy
        :param geneticString: string to determine agent's attributes and behavior
        :param stepSpawned: integer giving the simulation step the agent was created in
        """
        super().__init__()
        self.colorNames = ['none', 'black', 'red', 'orange', 'yellow', 'blue', 'green', 'purple', 'brown', 'pink', 'gray']
        self.colorAbbrevs = ['non', 'blk', 'red', 'org', 'yel', 'blu', 'grn', 'pur', 'brn', 'pnk', 'gry']
        self.row, self.col, self.heading = initPose
        self.geneticString = geneticString
        # self.visObjectId = None
        self.isDead = False
        self.readyToBreed = 10
        self.stepSpawned = stepSpawned

        """
        X000000000000000 - Vision [0]
        0X00000000000000 - Smell [1]
        00X0000000000000 - Movement [2]
        000X000000000000 - Aggression [3]
        0000X00000000000 - Sleep Type - Diurnal (0) or Nocturnal (1) [4]
        00000X0000000000 - Color [5]
        000000XX00000000 - Energy [6:7]
        00000000X0000000 - Jump [8]
        000000000X000000 - Swim [9]
        0000000000X00000 - Fly [10]
        00000000000X0000 - Scavenge [11]
        000000000000X000 - Has a sickness [12]
        0000000000000X00 - Disease Resistance [13]
        """

        # Initiating agent's attributes based on its genetic string
        self.visionRange = int(self.geneticString[0])
        self.smellRadius = int(self.geneticString[1])
        # self.moveSpeed = int(self.geneticString[2])
        self.moveSpeed = 1 #TODO: implement different move speeds
        self.Aggression = int(self.geneticString[3])
        self.sleepValue = int(self.geneticString[4])
        self.color = int(self.geneticString[5])
        self.energy = int(self.geneticString[6:8])
        self.jumpVal = int(self.geneticString[8])
        self.swimVal = int(self.geneticString[9])
        self.flyVal = int(self.geneticString[10])
        self.scavengeVal = int(self.geneticString[11])
        self.sickVal = int(self.geneticString[12])
        self.resistanceVal = int(self.geneticString[13])

        # Setting default values
        self.canSwim = False
        self.canJump = False
        self.canFly = False
        self.canScavenge = False

        self.isSick = False
        self.stepsUntilHealthy = 0

        self.mushroomInfluence = 0
        self.stepsUntilNoMushroomInfluence = 0

        self.objectConsumed = 0
        """
        0 - Nothing
        1 - Food
        2 - Tree Berry
        3 - Mushroom
        4 - Agent
        """

        if self.swimVal == 1:
            self.canSwim = True
        if self.jumpVal == 1:
            self.canJump = True
        if self.flyVal == 1:
            self.canFly = True
        if self.scavengeVal == 1:
            self.canScavenge = True
        if self.sickVal == 1:
            self.isSick = True
            # TODO: make this scale by gridsize
            sicknessLength = random.randint(10, 50)
            self.setStepsUntilHealthy(sicknessLength)
            # print("Sickness length: ", sicknessLength)

        # self.score = 0 #TODO: use this variable?

    # =================================================================
    # Getter functions
    def getEnergy(self):
        """Returns the current energy value."""
        return self.energy

    def getAggression(self):
        """Returns 0 if the agent is docile, 1 if it is aggressive."""
        return self.Aggression

    def getVisionRange(self):
        """Returns the vision range attribute."""
        return self.visionRange

    def getSmellRadius(self):
        """Returns the smell radius attribute."""
        return self.smellRadius

    def getGeneticString(self):
        """Returns the agent's genetic string."""
        return self.geneticString

    def getPose(self):
        """Returns a tuple containing the row, column, and heading of the agent."""
        return self.row, self.col, self.heading

    def getReadyToBreed(self):
        """Returns the number of steps until the agent is ready to breed."""
        return self.readyToBreed

    def getIsSick(self):
        """Returns a boolean that tells if the agent is sick."""
        return self.isSick

    def getStepsUntilHealthy(self):
        """Returns the agent's mushroomInfluence attribute."""
        return self.stepsUntilHealthy

    def getMushroomInfluence(self):
        """Returns an integer that tells which mushroom influence the agent is currently affected by."""
        return self.mushroomInfluence

    def getObjectConsumed(self):
        """Returns which object the agent has consumed most recently."""
        return self.objectConsumed

    def getStepsUntilNoMushroomInfluence(self):
        """Returns the number of steps until the agent's mushroomInfluence wears off."""
        return self.stepsUntilNoMushroomInfluence

    def isAwake(self, sleepValue, time):
        """Returns a string that tells whether the agent is awake or asleep
        based on its sleep pattern and the time of day."""
        if sleepValue == 0 and 6 <= time <= 18:
            return "awake"
        elif sleepValue == 1 and (time < 6 or time > 18):
            return "awake"
        else:
            return "sleeping"

    # =================================================================
    # Setter functions
    def updatePose(self, newRow, newCol, newHeading):
        """Updates the agent's pose to a new position and heading"""
        self.row = newRow
        self.col = newCol
        self.heading = newHeading

    def changeEnergy(self, changeVal):
        """Changes the energy value by adding changeVal to it, reports back if the value goes to zero
        or below: the agent "dies" in that case."""
        if self.isSick:
            randomInt = random.randint(0, 100)
            chanceOfSurviving = .5-(self.resistanceVal*.05)

            if randomInt < chanceOfSurviving * 100:
                changeVal = -1000

            if changeVal < 0:
                changeVal = changeVal * 2

        self.energy += changeVal
        if self.energy <= 0:
            return False
        return True

    def changeIsDead(self, deadVal):
        """Changes the agent's isDead status."""
        self.isDead = deadVal

    def getJump(self):
        """Returns 0 if the agent cannot jump, 1 if it can."""
        return self.jumpVal

    def getSwim(self):
        """Returns 0 if the agent cannot swim, 1 if it can."""
        return self.swimVal

    def changeReadyToBreed(self, breedVal):
        """Reduces an agents steps until ready to breed by an input value."""
        self.readyToBreed = self.readyToBreed - breedVal

    def setReadyToBreed(self, breedVal):
        """Sets agents steps until ready to breed."""
        self.readyToBreed = breedVal

    def setMushroomInfluence(self, newVal):
        """Sets the agent's mushroomInfluence attribute."""
        self.mushroomInfluence = newVal

    def setStepsUntilHealthy(self, newVal):
        """Sets the agent's stepsUntilHealthy attribute."""
        self.stepsUntilHealthy = newVal

    def setObjectConsumed(self, newObject):
        """Sets the agent's objectConsumed attribute."""
        self.objectConsumed = newObject

    def setStepsUntilNoMushroomInfluence(self, newVal):
        """Sets the agent's steps until its mushroomInfluence reverts to 0."""
        self.stepsUntilNoMushroomInfluence = newVal

    # =================================================================
    # Coordinate-related functions

    def _computeAhead(self, gridSize):
        """Determines the cell that is one space ahead of current cell, given the heading."""
        row, col, heading = self.getPose()
        moveSpeed = self.moveSpeed
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

    def _leftTurn(self):
        """Returns the new heading after a left turn."""
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
        """Returns the new heading after a right turn."""
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
        """Returns the new heading after turning around."""
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
        """Kills an agent at a given location if it is an enemy."""
        for j in range(len(sim.agentsAt(row, col))):
            if int(sim.agentsAt(row, col)[j].getColor()) != self.getColor():
                deadCreature = sim.agentsAt(row, col)[j]
                self.setObjectConsumed(deadCreature.getObjectConsumed())
                deadCreature.changeEnergy(-100)
                deadCreature.isDead = True

    # =================================================================
    # Detection helper functions
    def _areCreaturesInVision(self, sim):
        """Returns the first object in the agents line of sight."""
        #TODO: do we still need this function?
        ownY, ownX, heading = self.getPose()
        visionList = []
        visionRange = self.visionRange

        # print("Object Here: ", sim._assessObjectsHere(ownY, ownX, self))
        if sim._assessObjectsHere(ownY, ownX, self) == 4:
            # print("IM ON A TREE")
            return 0

        if heading == "n":
            for i in range(int(visionRange)):
                for ob in sim._listOfObjectsHere((ownY - (int(self.geneticString[0]) - i)) % sim.gridSize, ownX, self):
                    if type(ob) is Tree:
                        visionList.append(0)
                        break
                    else:
                        visionList.append(sim._assessCreature((ownY - (int(self.geneticString[0]) - i)) % sim.gridSize, ownX, self))
                # if visionList[i] != 0:
                #     return 1
                if len(visionList) == 0:
                    return 0

        elif heading == "s":
            for i in range(int(visionRange)):
                for ob in sim._listOfObjectsHere((ownY + i + 1) % sim.gridSize, ownX, self):
                    if type(ob) is Tree:
                        visionList.append(0)
                        break
                    else:
                        visionList.append(sim._assessCreature((ownY + i + 1) % sim.gridSize, ownX, self))
                # if visionList[i] != 0:
                #     return 1
                if len(visionList) == 0:
                    return 0

        elif heading == "e":
            for i in range(int(visionRange)):
                for ob in sim._listOfObjectsHere(ownY, (ownX + i + 1) % sim.gridSize, self):
                    if type(ob) is Tree:
                        visionList.append(0)
                        break
                    else:
                        visionList.append(sim._assessCreature(ownY, (ownX + i + 1) % sim.gridSize, self))
                # if visionList[i] != 0:
                #     return 1
                if len(visionList) == 0:
                    return 0

        elif heading == "w":
            for i in range(int(visionRange)):
                for ob in sim._listOfObjectsHere(ownY, (ownX - (int(self.geneticString[0]) - i)) % sim.gridSize, self):
                    if type(ob) is Tree:
                        visionList.append(0)
                        break
                    else:
                        visionList.append(sim._assessCreature(ownY, (ownX - (int(self.geneticString[0]) - i)) % sim.gridSize, self))
                # if visionList[i] != 0:
                #     return 1
                if len(visionList) == 0:
                    return 0

        for v in visionList:
            if v != 0:
                return v

        # if they don't see anything
        return 0

    def smellRadius1(self, sim):
        """Returns a list of agents in the 4 squares around the agent."""
        #TODO: do we still need this function?
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
        """Returns a list of agents in the 12 squares around the agent."""
        # TODO: do we still need this function?
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

    def smellRadiusGlobal1(self, sim):
        """Returns a list of all objects in the 4 squares around the agent."""
        ownY, ownX, heading = self.getPose()
        cellsSmelled = []
        cellAbove = sim._assessObjectsHere((ownY - 1) % sim.gridSize, ownX, self)
        cellBelow = sim._assessObjectsHere((ownY + 1) % sim.gridSize, ownX, self)
        cellRight = sim._assessObjectsHere(ownY, (ownX + 1) % sim.gridSize, self)
        cellLeft = sim._assessObjectsHere(ownY, (ownX - 1) % sim.gridSize, self)

        cellsSmelled.append(cellAbove)
        cellsSmelled.append(cellBelow)
        cellsSmelled.append(cellRight)
        cellsSmelled.append(cellLeft)
        return cellsSmelled

    def smellRadiusGlobal2(self, sim):
        """Returns a list of all objects in the 12 squares around the agent."""
        ownY, ownX, heading = self.getPose()
        cellsSmelled = []

        cellAbove = sim._assessObjectsHere((ownY - 1) % sim.gridSize, ownX, self)
        cellBelow = sim._assessObjectsHere((ownY + 1) % sim.gridSize, ownX, self)
        cellRight = sim._assessObjectsHere(ownY, (ownX + 1) % sim.gridSize, self)
        cellLeft = sim._assessObjectsHere(ownY, (ownX - 1) % sim.gridSize, self)

        cellTwoAbove = sim._assessObjectsHere((ownY - 2) % sim.gridSize, ownX, self)
        cellTwoBelow = sim._assessObjectsHere((ownY + 2) % sim.gridSize, ownX, self)
        cellTwoRight = sim._assessObjectsHere(ownY, (ownX + 2) % sim.gridSize, self)
        cellTwoLeft = sim._assessObjectsHere(ownY, (ownX - 2) % sim.gridSize, self)

        cellAboveLeft = sim._assessObjectsHere((ownY - 1) % sim.gridSize, (ownX - 1) % sim.gridSize, self)
        cellAboveRight = sim._assessObjectsHere((ownY - 1) % sim.gridSize, (ownX + 1) % sim.gridSize, self)
        cellBelowRight = sim._assessObjectsHere((ownY + 1) % sim.gridSize, (ownX + 1) % sim.gridSize, self)
        cellBelowLeft = sim._assessObjectsHere((ownY + 1) % sim.gridSize, (ownX - 1) % sim.gridSize, self)

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
        # print("Cells Smelled: ", cellsSmelled)

        return cellsSmelled

    def detectSmellRadius(self, sim):
        """Returns the direction and object of one object in the agent's smell radius."""
        ownY, ownX, heading = self.getPose()
        smellRadius = self.geneticString[1]

        # actions for if the agent has a smell radius of 1
        if int(smellRadius) == 1:

            creaturesSmelled = self.smellRadiusGlobal1(sim)
            foodSmelled = self.smellRadiusGlobal1(sim)

            cellsSmelled = self.combineStrings(creaturesSmelled, foodSmelled, self)

            if cellsSmelled[0] > 0 and heading == "n":
                return "above", cellsSmelled[0]
            elif cellsSmelled[1] > 0 and heading == "n":
                return "below", cellsSmelled[1]
            elif cellsSmelled[2] > 0 and heading == "n":
                return "right", cellsSmelled[2]
            elif cellsSmelled[3] > 0 and heading == "n":
                return "left", cellsSmelled[3]

            elif cellsSmelled[0] > 0 and heading == "s":
                return "below", cellsSmelled[0]
            elif cellsSmelled[1] > 0 and heading == "s":
                return "above", cellsSmelled[1]
            elif cellsSmelled[2] > 0 and heading == "s":
                return "left", cellsSmelled[2]
            elif cellsSmelled[3] > 0 and heading == "s":
                return "right", cellsSmelled[3]

            elif cellsSmelled[0] > 0 and heading == "e":
                return "left", cellsSmelled[0]
            elif cellsSmelled[1] > 0 and heading == "e":
                return "right", cellsSmelled[1]
            elif cellsSmelled[2] > 0 and heading == "e":
                return "above", cellsSmelled[2]
            elif cellsSmelled[3] > 0 and heading == "e":
                return "below", cellsSmelled[3]

            elif cellsSmelled[0] > 0 and heading == "w":
                return "right", cellsSmelled[0]
            elif cellsSmelled[1] > 0 and heading == "w":
                return "left", cellsSmelled[1]
            elif cellsSmelled[2] > 0 and heading == "w":
                return "below", cellsSmelled[2]
            elif cellsSmelled[3] > 0 and heading == "w":
                return "above", cellsSmelled[3]
            else:
                return "none"

        elif int(smellRadius) == 2:
            cellsSmelled = self.smellRadiusGlobal2(sim)
            if cellsSmelled[0] > 0 and heading == "n":
                return "above", cellsSmelled[0]
            elif cellsSmelled[1] > 0 and heading == "n":
                return "below", cellsSmelled[1]
            elif cellsSmelled[2] > 0 and heading == "n":
                return "right", cellsSmelled[2]
            elif cellsSmelled[3] > 0 and heading == "n":
                return "left", cellsSmelled[3]

            elif cellsSmelled[0] > 0 and heading == "s":
                return "below", cellsSmelled[0]
            elif cellsSmelled[1] > 0 and heading == "s":
                return "above", cellsSmelled[1]
            elif cellsSmelled[2] > 0 and heading == "s":
                return "left", cellsSmelled[2]
            elif cellsSmelled[3] > 0 and heading == "s":
                return "right", cellsSmelled[3]

            elif cellsSmelled[0] > 0 and heading == "e":
                return "left", cellsSmelled[0]
            elif cellsSmelled[1] > 0 and heading == "e":
                return "right", cellsSmelled[1]
            elif cellsSmelled[2] > 0 and heading == "e":
                return "above", cellsSmelled[2]
            elif cellsSmelled[3] > 0 and heading == "e":
                return "below", cellsSmelled[3]

            elif cellsSmelled[0] > 0 and heading == "w":
                return "right", cellsSmelled[0]
            elif cellsSmelled[1] > 0 and heading == "w":
                return "left", cellsSmelled[1]
            elif cellsSmelled[2] > 0 and heading == "w":
                return "below", cellsSmelled[2]
            elif cellsSmelled[3] > 0 and heading == "w":
                return "above", cellsSmelled[3]

            elif (cellsSmelled[4] > 0) and heading == "n":
                return "above", cellsSmelled[4]
            elif (cellsSmelled[5] > 0) and heading == "n":
                return "below", cellsSmelled[5]
            elif (cellsSmelled[6] > 0) and heading == "n":
                return "right", cellsSmelled[6]
            elif (cellsSmelled[7] > 0) and heading == "n":
                return "left", cellsSmelled[7]

            elif (cellsSmelled[4] > 0) and heading == "s":
                return "below", cellsSmelled[4]
            elif (cellsSmelled[5] > 0) and heading == "s":
                return "above", cellsSmelled[5]
            elif (cellsSmelled[6] > 0) and heading == "s":
                return "left", cellsSmelled[6]
            elif (cellsSmelled[7] > 0) and heading == "s":
                return "right", cellsSmelled[7]

            elif (cellsSmelled[4] > 0) and heading == "e":
                return "left", cellsSmelled[4]
            elif (cellsSmelled[5] > 0) and heading == "e":
                return "right", cellsSmelled[5]
            elif (cellsSmelled[6] > 0) and heading == "e":
                return "above", cellsSmelled[6]
            elif (cellsSmelled[7] > 0) and heading == "e":
                return "below", cellsSmelled[7]

            elif (cellsSmelled[4] > 0) and heading == "w":
                return "right", cellsSmelled[4]
            elif (cellsSmelled[5] > 0) and heading == "w":
                return "left", cellsSmelled[5]
            elif (cellsSmelled[6] > 0) and heading == "w":
                return "below", cellsSmelled[6]
            elif (cellsSmelled[7] > 0) and heading == "w":
                return "above", cellsSmelled[7]

            elif cellsSmelled[8] > 0 and heading == "n":
                return random.choice(["above", "left"]), cellsSmelled[8]
            elif cellsSmelled[9] > 0 and heading == "n":
                return random.choice(["above", "right"]), cellsSmelled[9]
            elif cellsSmelled[10] > 0 and heading == "n":
                return random.choice(["below", "left"]), cellsSmelled[10]
            elif cellsSmelled[11] > 0 and heading == "n":
                return random.choice(["below", "right"]), cellsSmelled[11]

            elif cellsSmelled[8] > 0 and heading == "s":
                return random.choice(["below", "right"]), cellsSmelled[8]
            elif cellsSmelled[9] > 0 and heading == "s":
                return random.choice(["below", "left"]), cellsSmelled[9]
            elif cellsSmelled[10] > 0 and heading == "s":
                return random.choice(["above", "right"]), cellsSmelled[10]
            elif cellsSmelled[11] > 0 and heading == "s":
                return random.choice(["above", "left"]), cellsSmelled[11]

            elif cellsSmelled[8] > 0 and heading == "e":
                return random.choice(["below", "left"]), cellsSmelled[8]
            elif cellsSmelled[9] > 0 and heading == "e":
                return random.choice(["above", "left"]), cellsSmelled[9]
            elif cellsSmelled[10] > 0 and heading == "e":
                return random.choice(["below", "right"]), cellsSmelled[10]
            elif cellsSmelled[11] > 0 and heading == "e":
                return random.choice(["above", "right"]), cellsSmelled[11]

            elif cellsSmelled[8] > 0 and heading == "w":
                return random.choice(["above", "right"]), cellsSmelled[8]
            elif cellsSmelled[9] > 0 and heading == "w":
                return random.choice(["below", "right"]), cellsSmelled[9]
            elif cellsSmelled[10] > 0 and heading == "w":
                return random.choice(["above", "left"]), cellsSmelled[10]
            elif cellsSmelled[11] > 0 and heading == "w":
                return random.choice(["below", "left"]), cellsSmelled[11]

            else:
                return "none"

        else:
            return "none"

    # =================================================================
    # Detection main functions - for determining actions
    def checkHere(self, sim, listOfPossibleActions):
        """Returns a list of possible actions after checking what objects are on the same square as the agent."""
        ownX, ownY, ownH = self.getPose()

        # Might not need this -------- VVV
        objectHere = sim._listOfObjectsHere(ownX, ownY, self)
        # list of objects without the current agent
        objectHere = self.removeSelfFromList(objectHere)
        # print("Here List:", objectHere)
        # Might not need this -------- ^^^^

        if not self.canSwim:
            # if standing on water, die
            if len(self.removeSelfFromList(sim.waterAt(ownX, ownY))) > 0:
                # print("There is water here")
                if self.canFly:
                    self.changeEnergy(-5)
                else:
                    return ['die']

        if not self.canJump:
            # if standing on rocks, die
            if len(self.removeSelfFromList(sim.stonesAt(ownX, ownY))) > 0:
                # print("There is a rock here")
                if self.canFly:
                    self.changeEnergy(-5)
                else:
                    return ['die']

        # if standing on agent
        if len(self.removeSelfFromList(sim.agentsAt(ownX, ownY))) > 0:
            if self.removeSelfFromList(sim.agentsAt(ownX, ownY))[0].getIsSick() is True:
                self.isSick = True
                self.setStepsUntilHealthy(random.randint(5, 30))
            # the agent is a friend
            if self.getColor() == self.removeSelfFromList(sim.agentsAt(ownX, ownY))[0].getColor():
                # print("Time to breed")
                # if both agents are ready to breed
                if self.getReadyToBreed() == 0 and self.removeSelfFromList(sim.agentsAt(ownX, ownY))[0].getReadyToBreed() == 0:
                    return ['breed']


            # the agent is not a friend
            else:
                # if we aren't aggressive
                if self.getAggression() == 0:
                    # TODO: change to random movement
                    return ['forward']
                # if we are aggressive
                else:
                    return ['attack']

        # if standing on food, eat
        elif len(self.removeSelfFromList(sim.foodAt(ownX, ownY))) > 0 or len(self.removeSelfFromList(sim.mushroomAt(ownX, ownY))) > 0:
            # print("There is food here")
            # if we can eat
            if self.getAggression() == 0:
                return ['eat']

        # if standing on tree
        elif len(self.removeSelfFromList(sim.treeAt(ownX, ownY))) > 0:
            # print("There is a tree here")
            if self.removeSelfFromList(sim.treeAt(ownX, ownY))[0].getHasFood() == "1" and self.canScavenge and self.getEnergy() < 50:
                self.removeSelfFromList(sim.treeAt(ownX, ownY))[0].setHasFood("0")
                # print(self.removeSelfFromList(sim.treeAt(ownX, ownY))[0])
                self.removeSelfFromList(sim.treeAt(ownX, ownY))[0].setStepsUntilBloom(random.randint(10,40))
                return ['eatBerries']
        return listOfPossibleActions

    def checkVision(self, sim, listOfPossibleActions):
        """Returns a list of possible actions after checking what objects the agent can see."""
        ownY, ownX, heading = self.getPose()
        visionList = []
        visionRange = self.visionRange

        # if the heading is north
        if heading == "n":
            # loop through vision length
            for i in range(int(visionRange)):

                currentAboveCell = (ownY - i - 1) % sim.gridSize

                # if it sees a tree, return the vision list
                if len(self.removeSelfFromList(sim.treeAt(currentAboveCell, ownX))) > 0:
                    if self.removeSelfFromList(sim.treeAt(currentAboveCell, ownX))[0].getHasFood() == "1" and self.canScavenge and self.getEnergy() < 50:
                        visionList.append(self.removeSelfFromList(sim.treeAt(currentAboveCell, ownX))[0])
                        return ['forward']
                    else:
                        break

                # if it doesn't see a tree, add whatever it sees
                else:
                    visionList.append(sim._assessObjectsHere(currentAboveCell, ownX, self))


        # if the heading is south
        elif heading == "s":
            # loop through vision length
            for i in range(int(visionRange)):

                currentAboveCell = (ownY + i + 1) % sim.gridSize

                # if it sees a tree, return the vision list
                if len(self.removeSelfFromList(sim.treeAt(currentAboveCell, ownX))) > 0:
                    if self.removeSelfFromList(sim.treeAt(currentAboveCell, ownX))[0].getHasFood() == "1" and self.canScavenge and self.getEnergy() < 100:
                        visionList.append(self.removeSelfFromList(sim.treeAt(currentAboveCell, ownX))[0])
                        return ['forward']
                    else:
                        break

                # if it doesn't see a tree, add whatever it sees
                else:
                    visionList.append(sim._assessObjectsHere(currentAboveCell, ownX, self))

        # if the heading is east
        elif heading == "e":
            # loop through vision length
            for i in range(int(visionRange)):

                currentAboveCell = (ownX + i + 1) % sim.gridSize

                # if it sees a tree, return the vision list
                if len(self.removeSelfFromList(sim.treeAt(ownY, currentAboveCell))) > 0:
                    if self.removeSelfFromList(sim.treeAt(ownY, currentAboveCell))[0].getHasFood() == "1" and self.canScavenge and self.getEnergy() < 100:
                        visionList.append(self.removeSelfFromList(sim.treeAt(ownY, currentAboveCell)))
                        return ['forward']
                    else:
                        break

                # if it doesn't see a tree, add whatever it sees
                else:
                    visionList.append(sim._assessObjectsHere(ownY, currentAboveCell, self))

        # if the heading is west
        elif heading == "w":
            # loop through vision length
            for i in range(int(visionRange)):

                currentAboveCell = (ownX - i - 1) % sim.gridSize

                # if it sees a tree, return the vision list
                if len(self.removeSelfFromList(sim.treeAt(ownY, currentAboveCell))) > 0:
                    if self.removeSelfFromList(sim.treeAt(ownY, currentAboveCell))[0].getHasFood() == "1" and self.canScavenge and self.getEnergy() < 100:
                        visionList.append(self.removeSelfFromList(sim.treeAt(ownY, currentAboveCell)))
                        return ['forward']
                    else:
                        break

                # if it doesn't see a tree, add whatever it sees
                else:
                    visionList.append(sim._assessObjectsHere(ownY, currentAboveCell, self))

        # print("Vision List: ", visionList)

        try:
            while True:
                visionList.remove(None)
        except ValueError:
            pass

        # print("Vision List after removing none: ", visionList)

        # if it can't see anything, return nothing
        if visionList == []:
            return listOfPossibleActions

        # if the vision is not blocked by a tree
        # firstThingInVision = None
        # for i in visionList:
        #     if i is not None:
        #         firstThingInVision = i
        #         break
        firstThingInVision = visionList[0]
        # print("First thing in vision:",firstThingInVision)
        # print(type(firstThingInVision))

        # if the thing it can see is none, return nothing
        if firstThingInVision is None:
            # print("SITUATION 0")
            return listOfPossibleActions

        # if there is a stone directly in front and we can't jump, then take 'forward' out of the options
        if type(firstThingInVision) is Stone and visionList[0] == firstThingInVision:
            # print("SITUATION 1")
            if self.canJump:
                return listOfPossibleActions
            else:
                try:
                    while True:
                        listOfPossibleActions.remove('forward')
                except ValueError:
                    pass
                return listOfPossibleActions

        # if there is a water directly in front and we can't swim, then take 'forward' out of the options
        if type(firstThingInVision) is Water and visionList[0] == firstThingInVision:
            # print("SITUATION 2")
            if self.canSwim:
                return listOfPossibleActions
            else:
                try:
                    while True:
                        listOfPossibleActions.remove('forward')
                except ValueError:
                    pass
                return listOfPossibleActions

        # if the first thing it sees is food
        if ((type(firstThingInVision) is Food ) or type(firstThingInVision) is Mushroom ) and (self.getAggression()==0):
            # print("FIRST THING IN VISION IS FOOD")
            # if we are hungry, eat
            if self.getEnergy() < 50:
                return ['forward']
            # if we aren't, random
            else:
                return listOfPossibleActions

        # if the first thing we see is an agent
        if type(firstThingInVision) is Agent:
            # print("SITUATION 3")
            # if we are friends
            if self.getColor() == firstThingInVision.getColor():
                if self.getReadyToBreed() == 0:
                    return ['forward']
                else:
                    return ['forward']
            # if we aren't friends
            else:
                # if I'm not aggressive, run
                if self.getAggression() == 0:
                    try:
                        while True:
                            listOfPossibleActions.remove('forward')
                    except ValueError:
                        pass
                # if I am, try to attack
                else:
                    return ['forward']

        # print("SITUATION 5")
        # print("possible actions: ", listOfPossibleActions)
        return listOfPossibleActions

    def checkSmell(self,sim, listOfPossibleActions):
        """Returns a list of possible actions after checking what objects the agent can smell."""
        ownY, ownX, heading = self.getPose()
        cellsSmelled = []

        if self.getSmellRadius() == 1 or self.getSmellRadius() == 2:
            cellAbove = sim._listOfObjectsHere((ownY - 1) % sim.gridSize, ownX, self)
            cellBelow = sim._listOfObjectsHere((ownY + 1) % sim.gridSize, ownX, self)
            cellRight = sim._listOfObjectsHere(ownY, (ownX + 1) % sim.gridSize, self)
            cellLeft = sim._listOfObjectsHere(ownY, (ownX - 1) % sim.gridSize, self)

            cellsSmelled.append(cellAbove)
            cellsSmelled.append(cellBelow)
            cellsSmelled.append(cellRight)
            cellsSmelled.append(cellLeft)

            cellsSmelled = self.reorderListBasedOnHeading(cellsSmelled)

            #Looking at the cell in front
            for object in cellsSmelled[0]:
                if (type(object) is Stone and not self.canJump) or (type(object) is Water and not self.canSwim) and not self.canFly:
                    try:
                        while True:
                            listOfPossibleActions.remove('forward')
                    except ValueError:
                        pass

                if (type(object) is Agent):
                    #if it is a friend
                    if (object.getColor() == self.getColor()) :
                        #if ready to breeed
                        if self.getReadyToBreed() == 0:
                            return ['forward']
                    #enemy is in front
                    elif (object.getColor() != self.getColor()):
                        if self.getAggression() == 0:
                            try:
                                while True:
                                    listOfPossibleActions.remove('forward')
                            except ValueError:
                                pass
                        else:
                            return ['forward']

                if ( ((type(object) is (Food)) or (type(object) is Mushroom) ) and (self.getAggression()==0) and (self.getEnergy()<50)):
                    return ['forward']

            # Looking at the cell behind
            for object in cellsSmelled[1]:
                if (type(object) is Stone and not self.canJump) or (type(object) is Water and not self.canSwim) and not self.canFly:
                    try:
                        while True:
                            listOfPossibleActions.remove('turnAround')
                    except ValueError:
                        pass

                if (type(object) is Agent):
                    #if it is a friend
                    if (object.getColor() == self.getColor()) :
                        #if ready to breeed
                        if self.getReadyToBreed() == 0:
                            return ['turnAround']
                    #enemy is behind
                    elif (object.getColor() != self.getColor()):
                        if self.getAggression() == 0:
                            try:
                                while True:
                                    listOfPossibleActions.remove('turnAround')
                            except ValueError:
                                pass
                        else:
                            return ['turnAround']

                if ( ((type(object) is (Food)) or (type(object) is Mushroom) ) and (self.getAggression()==0) and (self.getEnergy()<50)):
                    return ['turnAround']

            # Looking at the cell to the right
            for object in cellsSmelled[2]:
                if (type(object) is Stone and not self.canJump) or (type(object) is Water and not self.canSwim) and not self.canFly:
                    try:
                        while True:
                            listOfPossibleActions.remove('right')
                    except ValueError:
                        pass

                if (type(object) is Agent):
                    #if it is a friend
                    if (object.getColor() == self.getColor()) :
                        #if ready to breeed
                        if self.getReadyToBreed() == 0:
                            return ['right']
                    #enemy is to the right
                    elif (object.getColor() != self.getColor()):
                        if self.getAggression() == 0:
                            try:
                                while True:
                                    listOfPossibleActions.remove('right')
                            except ValueError:
                                pass
                        else:
                            return ['right']

                if ( ((type(object) is (Food)) or (type(object) is Mushroom) ) and (self.getAggression()==0) and (self.getEnergy()<50)):
                    return ['right']

            # Looking at the cell to the left
            for object in cellsSmelled[3]:
                if (type(object) is Stone and not self.canJump) or (type(object) is Water and not self.canSwim) and not self.canFly:
                    try:
                        while True:
                            listOfPossibleActions.remove('left')
                    except ValueError:
                        pass

                if (type(object) is Agent):
                    #if it is a friend
                    if (object.getColor() == self.getColor()) :
                        #if ready to breeed
                        if self.getReadyToBreed() == 0:
                            return ['left']
                    #enemy is to the left
                    elif (object.getColor() != self.getColor()):
                        if self.getAggression() == 0:
                            try:
                                while True:
                                    listOfPossibleActions.remove('left')
                            except ValueError:
                                pass
                        else:
                            return ['left']

                if ( ((type(object) is (Food)) or (type(object) is Mushroom) ) and (self.getAggression()==0) and (self.getEnergy()<50)):
                    return ['left']

        if self.getSmellRadius() == 2:
            radius2cellssmelled = []
            cellTwoAbove = sim._listOfObjectsHere((ownY - 2) % sim.gridSize, ownX, self)
            cellTwoBelow = sim._listOfObjectsHere((ownY + 2) % sim.gridSize, ownX, self)
            cellTwoRight = sim._listOfObjectsHere(ownY, (ownX + 2) % sim.gridSize, self)
            cellTwoLeft = sim._listOfObjectsHere(ownY, (ownX - 2) % sim.gridSize, self)

            cellAboveLeft = sim._listOfObjectsHere((ownY - 1) % sim.gridSize, (ownX - 1) % sim.gridSize, self)
            cellAboveRight = sim._listOfObjectsHere((ownY - 1) % sim.gridSize, (ownX + 1) % sim.gridSize, self)
            cellBelowRight = sim._listOfObjectsHere((ownY + 1) % sim.gridSize, (ownX + 1) % sim.gridSize, self)
            cellBelowLeft = sim._listOfObjectsHere((ownY + 1) % sim.gridSize, (ownX - 1) % sim.gridSize, self)

            radius2cellssmelled.append(cellTwoAbove)
            radius2cellssmelled.append(cellTwoBelow)
            radius2cellssmelled.append(cellTwoRight)
            radius2cellssmelled.append(cellTwoLeft)
            radius2cellssmelled.append(cellAboveLeft)
            radius2cellssmelled.append(cellAboveRight)
            radius2cellssmelled.append(cellBelowLeft)
            radius2cellssmelled.append(cellBelowRight)

            radius2cellssmelled = self.reorderListBasedOnHeadingLength8(radius2cellssmelled)
            # print("R2CellsSmelled:",radius2cellssmelled)

            # Looking at the cell in 2 squares front
            for object in radius2cellssmelled[0]:
                if (type(object) is Agent):
                    # if it is a friend
                    if (object.getColor() == self.getColor()):
                        # if ready to breeed
                        if self.getReadyToBreed() == 0 and 'forward' in listOfPossibleActions:
                                return ['forward']
                    # enemy is in front
                    elif (object.getColor() != self.getColor()):
                        if self.getAggression() == 0:
                            try:
                                while True:
                                    listOfPossibleActions.remove('forward')
                            except ValueError:
                                pass
                        else:
                            if 'forward' in listOfPossibleActions:
                                return ['forward']

                if ( ((type(object) is (Food)) or (type(object) is Mushroom) ) and (self.getAggression()==0) and (self.getEnergy()<50)):
                    if 'forward' in listOfPossibleActions:
                        return ['forward']

            # Looking at the cell 2 squares behind
            for object in radius2cellssmelled[1]:
                if (type(object) is Agent):
                    # if it is a friend
                    if (object.getColor() == self.getColor()):
                        # if ready to breed
                        if self.getReadyToBreed() == 0 and 'turnAround' in listOfPossibleActions:
                            return ['turnAround']
                    # enemy is behind
                    elif (object.getColor() != self.getColor()):
                        if self.getAggression() == 0:
                            try:
                                while True:
                                    listOfPossibleActions.remove('turnAround')
                            except ValueError:
                                pass
                        else:
                            if 'turnAround' in listOfPossibleActions:
                                return ['turnAround']

                if ( ((type(object) is (Food)) or (type(object) is Mushroom) ) and (self.getAggression()==0) and (self.getEnergy()<50)):
                    if 'turnAround' in listOfPossibleActions:
                        return ['turnAround']

            # Looking at the cell 2 squares to the right
            for object in radius2cellssmelled[2]:
                if (type(object) is Agent):
                    # if it is a friend
                    if (object.getColor() == self.getColor()):
                        # if ready to breeed
                        if self.getReadyToBreed() == 0 and 'right' in listOfPossibleActions:
                            return ['right']
                    # enemy is to the right
                    elif (object.getColor() != self.getColor()):
                        if self.getAggression() == 0:
                            try:
                                while True:
                                    listOfPossibleActions.remove('right')
                            except ValueError:
                                pass
                        else:
                            if 'right' in listOfPossibleActions:
                                return ['right']

                if ( ((type(object) is (Food)) or (type(object) is Mushroom) ) and (self.getAggression()==0) and (self.getEnergy()<50)):
                    if 'right' in listOfPossibleActions:
                        return ['right']

            # Looking at the cell 2 squares to the left
            for object in radius2cellssmelled[3]:
                if (type(object) is Agent):
                    # if it is a friend
                    if (object.getColor() == self.getColor()):
                        # if ready to breeed
                        if self.getReadyToBreed() == 0 and 'left' in listOfPossibleActions:
                            return ['left']
                    # enemy is to the right
                    elif (object.getColor() != self.getColor()):
                        if self.getAggression() == 0:
                            try:
                                while True:
                                    listOfPossibleActions.remove('left')
                            except ValueError:
                                pass
                        else:
                            if 'left' in listOfPossibleActions:
                                return ['left']

                if ( ((type(object) is (Food)) or (type(object) is Mushroom) ) and (self.getAggression()==0) and (self.getEnergy()<50)):
                    if 'left' in listOfPossibleActions:
                        return ['left']

            # Looking at the cell above and left
            for object in radius2cellssmelled[4]:
                if (type(object) is Agent):
                    # if it is a friend
                    if (object.getColor() == self.getColor()):
                        # if ready to breed
                        if self.getReadyToBreed() == 0:
                            if 'forward' in listOfPossibleActions:
                                return ['forward']
                            elif 'left' in listOfPossibleActions:
                                return ['left']
                    # enemy is to the above + left
                    elif (object.getColor() != self.getColor()):
                        if self.getAggression() == 0:
                            try:
                                while True:
                                    listOfPossibleActions.remove('left')
                            except ValueError:
                                pass
                            try:
                                while True:
                                    listOfPossibleActions.remove('forward')
                            except ValueError:
                                pass
                        #If we're aggressive
                        else:
                            if 'forward' in listOfPossibleActions:
                                return ['forward']
                            elif 'left' in listOfPossibleActions:
                                return ['left']

                if ( ((type(object) is (Food)) or (type(object) is Mushroom) ) and (self.getAggression()==0) and (self.getEnergy()<50)):
                    if 'forward' in listOfPossibleActions:
                        return ['forward']
                    elif 'left' in listOfPossibleActions:
                        return ['left']

            # Looking at the cell above and right
            for object in radius2cellssmelled[5]:
                if (type(object) is Agent):
                    # if it is a friend
                    if (object.getColor() == self.getColor()):
                        # if ready to breed
                        if self.getReadyToBreed() == 0:
                            if 'forward' in listOfPossibleActions:
                                return ['forward']
                            elif 'right' in listOfPossibleActions:
                                return ['right']
                    # enemy is to the above + right
                    elif (object.getColor() != self.getColor()):
                        if self.getAggression() == 0:
                            try:
                                while True:
                                    listOfPossibleActions.remove('right')
                            except ValueError:
                                pass
                            try:
                                while True:
                                    listOfPossibleActions.remove('forward')
                            except ValueError:
                                pass
                        # If we're aggressive
                        else:
                            if 'forward' in listOfPossibleActions:
                                return ['forward']
                            elif 'right' in listOfPossibleActions:
                                return ['right']

                if ( ((type(object) is (Food)) or (type(object) is Mushroom) ) and (self.getAggression()==0) and (self.getEnergy()<50)):
                    if 'forward' in listOfPossibleActions:
                        return ['forward']
                    elif 'right' in listOfPossibleActions:
                        return ['right']

            # Looking at the cell below and left
            for object in radius2cellssmelled[6]:
                if (type(object) is Agent):
                    # if it is a friend
                    if (object.getColor() == self.getColor()):
                        # if ready to breed
                        if self.getReadyToBreed() == 0:
                            if 'turnAround' in listOfPossibleActions:
                                return ['turnAround']
                            elif 'left' in listOfPossibleActions:
                                return ['left']
                    # enemy is to the below + left
                    elif (object.getColor() != self.getColor()):
                        if self.getAggression() == 0:
                            try:
                                while True:
                                    listOfPossibleActions.remove('left')
                            except ValueError:
                                pass
                            try:
                                while True:
                                    listOfPossibleActions.remove('turnAround')
                            except ValueError:
                                pass
                        # If we're aggressive
                        else:
                            if 'turnAround' in listOfPossibleActions:
                                return ['turnAround']
                            elif 'left' in listOfPossibleActions:
                                return ['left']

                if ( ((type(object) is (Food)) or (type(object) is Mushroom) ) and (self.getAggression()==0) and (self.getEnergy()<50)):
                    if 'turnAround' in listOfPossibleActions:
                        return ['turnAround']
                    elif 'left' in listOfPossibleActions:
                        return ['left']

            # Looking at the cell below and right
            for object in radius2cellssmelled[7]:
                if (type(object) is Agent):
                    # if it is a friend
                    if (object.getColor() == self.getColor()):
                        # if ready to breed
                        if self.getReadyToBreed() == 0:
                            if 'turnAround' in listOfPossibleActions:
                                return ['turnAround']
                            elif 'right' in listOfPossibleActions:
                                return ['right']
                    # enemy is to the below + right
                    elif (object.getColor() != self.getColor()):
                        if self.getAggression() == 0:
                            try:
                                while True:
                                    listOfPossibleActions.remove('right')
                            except ValueError:
                                pass
                            try:
                                while True:
                                    listOfPossibleActions.remove('turnAround')
                            except ValueError:
                                pass
                        # If we're aggressive
                        else:
                            if 'turnAround' in listOfPossibleActions:
                                return ['turnAround']
                            elif 'right' in listOfPossibleActions:
                                return ['right']

                if ( ((type(object) is (Food)) or (type(object) is Mushroom) ) and (self.getAggression()==0) and (self.getEnergy()<50)):
                    if 'turnAround' in listOfPossibleActions:
                        return ['turnAround']
                    elif 'right' in listOfPossibleActions:
                        return ['right']
        else:
            pass
            # print("CANT SMELL")

        # print("Actions after smell: " + str(listOfPossibleActions))
        return listOfPossibleActions


    def determineAction(self, sim, time):
        """Starts with an initial list of actions, decides which ones are still viable options after checking here,
        checking vision, and checking smell, and chooses a random action from the remaining viable choices."""
        listOfPossibleActions = ['left', 'right', 'turnAround', 'forward', 'forward', 'forward']
        # print("isSick: ", self.isSick)
        # print("Mushroom influence: ", self.mushroomInfluence)

        if self.mushroomInfluence == 2:
            return 'pause'
        elif self.mushroomInfluence == 3:
            #random movement
            return listOfPossibleActions
        # elif self.mushroomInfluence == 4:
        #     self.changeEnergy(-5)

        if self.isAwake(self.sleepValue, time) == "awake":

            # ---------- Check where we are ---------- #
            # sets the action based on what we are standing on
            listOfPossibleActions = self.checkHere(sim, listOfPossibleActions)
            # print("Actions after here: ", listOfPossibleActions)
            if len(listOfPossibleActions) == 1:
                return listOfPossibleActions[0]

            # ---------- Check what we see ---------- #
            # if it isn't standing on anything, keep going
            # sets the action based on what we see
            listOfPossibleActions = self.checkVision(sim, listOfPossibleActions)
            # print("Actions after vision: ", listOfPossibleActions)
            if len(listOfPossibleActions) == 1:
                return listOfPossibleActions[0]

            # ---------- Check what we smell ---------- #
            # sets the action based on what we can smell
            listOfPossibleActions = self.checkSmell(sim, listOfPossibleActions)
            # print("Actions after smell: ", listOfPossibleActions)
            if len(listOfPossibleActions) == 1:
                return listOfPossibleActions[0]

            if listOfPossibleActions == []:
                return random.choice(['left', 'right', 'turnAround'])

            if listOfPossibleActions == ['left', 'right', 'turnAround', 'forward', 'forward', 'forward']:
                if self.getEnergy() < 25:
                    if self.canFly and len(self.removeSelfFromList(sim.treeAt(self.getPose()[0], self.getPose()[1]))) > 0:
                        # print("I AM ROOSTING")
                        return 'roost'
                    else:
                        return 'rest'

            action = random.choice(listOfPossibleActions)
            # print("Action: ", action)
            return action

        elif self.isAwake(self.sleepValue, time) == "sleeping":
            return 'rest'
            action = random.choice(listOfPossibleActions)
            # print("Action: ", action)
            return action
        else:
            pass
            # print("ERROR WITH SLEEP VALUE")

    # =================================================================
    # Print functions
    def _printVision(self, sim):
        """Prints what the agent can see."""
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

    def _printSmell(self, sim, type):
        """Prints what the agent can smell."""
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
                cellsSmelled = self.smellRadiusGlobal1(sim)
            else:
                cellsSmelled = self.smellRadiusGlobal1(sim)
            # cellsSmelled = self.smellRadiusCreature1(agent)
            print(cellsSmelled)

            print("\t" + str(cellsSmelled[0]) + "\t")
            print(str(cellsSmelled[3]) + "   " + direction + " \t" + str(cellsSmelled[2]))
            print("\t" + str(cellsSmelled[1]) + "\t")

        elif int(smellRadius) == 2:
            if type == "agent":
                cellsSmelled = self.smellRadiusGlobal2(sim)
            else:
                cellsSmelled = self.smellRadiusGlobal2(sim)
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


    # =================================================================
    # Helper functions
    def combineStrings(self, creatureString, foodString, sim):
        #TODO: do we still need this function?
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
        return finalString

    def dropObject(self, sim):
        r,c,h = self.getPose()
        if self.objectConsumed == 0:
            pass
            # print("DROPPING OBJECT NONE")
            # nextTree = Tree(initPose=(r, c), geneticString="0", stepSpawned=sim.stepNum)
            # sim.treeList.append(nextTree)
            # sim.globalMap[r, c].append(nextTree)

        elif self.objectConsumed == 1:
            # print("DROPPING OBJECT FOOD SEEDS")
            pass

        elif self.objectConsumed == 2:
            ownX, ownY, ownH = self.getPose()
            objectHere = sim._listOfObjectsHere(ownX, ownY, self)
            objectHere = self.removeSelfFromList(objectHere)
            if (len(objectHere) == 0):
                # print("DROPPING OBJECT TREE SEEDS")
                nextTree = Tree(initPose=(r, c), geneticString="0", stepSpawned=sim.stepNum)
                nextTree.setHasFood("-1")
                nextTree.setStepsUntilBloom(51)
                sim.treeList.append(nextTree)
            # sim.globalMap[r, c].append(nextTree)

        elif self.objectConsumed == 3:
            ownX,ownY,ownH = self.getPose()
            objectHere = sim._listOfObjectsHere(ownX, ownY, self)
            objectHere = self.removeSelfFromList(objectHere)
            if (len(objectHere) == 0):
                nextMushroom = Mushroom(initPose=(r, c), geneticString="0", stepSpawned=sim.stepNum)
                nextMushroom.setDroppingType(0)
                sim.mushroomList.append(nextMushroom)
                sim.globalMap[r, c].append(nextMushroom)
                # print("DROPPING OBJECT MUSHROOM SPORES")

        # elif self.objectConsumed == 4:
        #     print("DROPPING OBJECT FROM EATEN AGENT")
        #     pass

    def removeSelfFromList(self, list):
        """Takes in a list and removes this agent from the list."""
        newList = list.copy()
        if self in newList:
            newList.remove(self)
        return newList

    def reorderListBasedOnHeading(self, list):
        """Takes in a list (length 4) and reorders it to [above,below,right,left] based on the agent's current heading."""
        heading = self.heading
        if heading == 'n':
            return list
        elif heading == 's':
            order = [1,0,3,2]
        elif heading == 'e':
            order = [2,3,1,0]
        elif heading == 'w':
            order = [3,2,0,1]
        else:
            print("heading invalid in reorder list function, returning north")
            return list

        list = [list[i] for i in order]
        return list

    def reorderListBasedOnHeadingLength8(self, list):
        """Takes in a list (length 8) and reorders it to
            [2above,2below,2right,2left,aboveLeft,aboveRight,belowLeft,belowRight]
        based on the agent's current heading."""
        heading = self.heading
        if heading == 'n':
            return list
        elif heading == 's':
            order = [1,0,3,2,7,6,5,4]
        elif heading == 'e':
            order = [2,3,1,0,5,7,4,6]
        elif heading == 'w':
            order = [3,2,0,1,6,4,7,5]
        else:
            print("heading invalid in reorder list function, returning north")
            return list

        list = [list[i] for i in order]
        return list

    def getTypeAbbreviation(self):
        """Returns the abbreviation for an agent object, "a"."""
        return self.colorAbbrevs[self.color]

    def __str__(self):
        """Information about the agent to print."""
        formStr = "Agent: col={5}  pos=({0:>3d}, {1:>3d}, {2:^3s})   energ={3:^6d}     genStr={4}"
        return formStr.format(self.row, self.col, self.heading, self.energy, self.geneticString, self.colorNames[self.color])
