import random
from Object import Object
from ALifeSim import *
from Tree import Tree
from Stone import Stone
from Water import Water
from Food import Food


class Agent(Object):
    """An agent object in the ALife simulation. An agent has a geneticString that governs its behavior, given by
    a string, and it has an amount of energy and a location on the agentMap (given when created and then updated)."""

    def __init__(self, initPose = (0, 0, 'n'), initEnergy = 40, geneticString = "0000000000", stepSpawned=0):
        """
        Sets up an agent with a location, energy, geneticString, and step created
        :param initPose:   tuple giving agent's initial location
        :param initEnergy: integer initial energy
        :param geneticString: string to determine agent's behavior
        :param stepSpawned: integer giving the simulation step the agent was created in
        """
        super().__init__()
        self.colorNames = ['none', 'black', 'red', 'orange', 'yellow', 'blue', 'green', 'purple', 'brown', 'pink', 'gray']
        self.colorAbbrevs = ['non', 'blk', 'red', 'org', 'yel', 'blu', 'grn', 'pur', 'brn', 'pnk', 'gry']
        self.row, self.col, self.heading = initPose
        self.geneticString = geneticString
        # self.whichScenarios = dict()
        # self.stepSpawned = stepSpawned
        # self.visObjectId = None
        self.isDead = False
        self.readyToBreed = 10
        self.stepSpawned = stepSpawned

        """
        X000000000 - Vision [0]
        0X00000000 - Smell [1]
        00X0000000 - Movement [2]
        000X000000 - Aggression [3]
        0000X00000 - Sleep Type - Diurnal (0) or Nocturnal (1) [4]
        00000X0000 - Color [5]
        0000000X00 - Energy [6:7]
        00000000X0 - Jump [8]
        000000000X - Swim [9]
        """

        self.visionRange = int(self.geneticString[0])
        self.smellRadius = int(self.geneticString[1])
        # self.moveSpeed = int(self.geneticString[2])
        self.moveSpeed = 1
        self.Aggression = int(self.geneticString[3])
        self.sleepValue = int(self.geneticString[4])
        self.color = int(self.geneticString[5])
        self.energy = int(self.geneticString[6:8])
        # self.energy = self.color #TODO: remove this line
        self.jumpVal = int(self.geneticString[8])
        self.swimVal = int(self.geneticString[9])

        self.canSwim = False
        self.canJump = False

        if self.swimVal == 1:
            self.canSwim = True
        if self.jumpVal == 1:
            self.canJump = True

        # self.score = 0

    def getEnergy(self):
        """Returns the current energy value"""
        return self.energy

    def getAggression(self):
        return self.Aggression

    def getVisionRange(self):
        return self.visionRange

    def getSmellRadius(self):
        return self.smellRadius

    def getGeneticString(self):
        return self.geneticString

    def getPose(self):
        """Return the row, column, and heading of the agent."""
        return self.row, self.col, self.heading

    def getReadyToBreed(self):
        return self.readyToBreed

    def updatePose(self, newRow, newCol, newHeading):
        """Updates the agent's pose to a new position and heading"""
        # print("before updating pos",self)
        self.row = newRow
        self.col = newCol
        self.heading = newHeading
        # print("after updating pos", self)

    def changeEnergy(self, changeVal):
        """Changes the energy value by adding changeVal to it, reports back if the value goes to zero
        or below: the agent "dies" in that case."""
        self.energy += changeVal
        if self.energy <= 0:
            return False
        return True

    def changeIsDead(self, deadVal):
        self.isDead = deadVal

    def getJump(self):
        return self.jumpVal

    def getSwim(self):
        return self.swimVal

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
        visionRange = self.visionRange

        print("Object Here: ", sim._assessObjectsHere(ownY, ownX, self))
        if sim._assessObjectsHere(ownY, ownX, self) == 4:
            print("IM ON A TREE")
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

    def removeSelfFromList(self, list):
        newList = list.copy()
        if self in newList:
            newList.remove(self)
        return newList


    def checkHere(self, sim, listOfPossibleActions):
        ownX, ownY, ownH = self.getPose()

        # Might not need this -------- VVV
        objectHere = sim._listOfObjectsHere(ownX, ownY, self)
        # list of objects without the current agent
        objectHere = self.removeSelfFromList(objectHere)
        print(objectHere)
        # Might not need this -------- ^^^^

        if not self.canSwim:
            # if standing on water, die
            if len(self.removeSelfFromList(sim.waterAt(ownX, ownY))) > 0:
                print("There is water here")
                return ['die']

        if not self.canJump:
            # if standing on rocks, die
            if len(self.removeSelfFromList(sim.stonesAt(ownX, ownY))) > 0:
                print("There is a rock here")
                return ['die']

        # if standing on agent
        if len(self.removeSelfFromList(sim.agentsAt(ownX, ownY))) > 0:
            # the agent is a friend
            if self.getColor() == self.removeSelfFromList(sim.agentsAt(ownX, ownY))[0].getColor():
                print("Time to breed")
                # if both agents are ready to breed
                if self.getReadyToBreed() == 0 and self.removeSelfFromList(sim.agentsAt(ownX, ownY))[0].getReadyToBreed() == 0:
                    return ['breed']


            # the agent is not a friend
            else:
                # if we aren't aggressive
                if self.getAggression() == 0:
                    # TODO: change to random movement
                    listOfPossibleActions = ['forward']
                # if we are aggressive
                else:
                    return ['attack']

        # if standing on food, eat
        elif len(self.removeSelfFromList(sim.foodAt(ownX, ownY))) > 0:
            print("There is food here")
            # if we can eat
            if self.getAggression() == 0:
                return ['eat']

        return listOfPossibleActions

    def checkVision(self, sim, listOfPossibleActions):
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
                    break

                # if it doesn't see a tree, add whatever it sees
                else:
                    visionList.append(sim._assessObjectsHere(ownY, currentAboveCell, self))



        print("Vision List: ", visionList)

        # if it can't see anything, return nothing
        if visionList == []:
            return listOfPossibleActions

        # if the vision is not blocked by a tree
        firstThingInVision = None
        for i in visionList:
            if i is not None:
                firstThingInVision = i
                break

        # if the thing it can see is none, return nothing
        if firstThingInVision is None:
            return listOfPossibleActions

        # if there is a stone directly in front and we can't jump, then take 'forward' out of the options
        if type(firstThingInVision) is Stone and visionList[0] == firstThingInVision:
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
        if type(firstThingInVision) is Food and self.getAggression == 0:
            # if we are hungry, eat
            if self.getEnergy() < 50:
                listOfPossibleActions = ['forward']
            # if we aren't, random
            else:
                return listOfPossibleActions

        # if the first thing we see is an agent
        if type(firstThingInVision) is Agent:
            # if we are friends
            if self.getColor() == firstThingInVision.getColor():
                if self.getReadyToBreed() == 0:
                    listOfPossibleActions = ['forward']
                else:
                    listOfPossibleActions = ['forward']
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
                    listOfPossibleActions = ['forward']

        print("possible actions: ", listOfPossibleActions)
        return listOfPossibleActions



        # TODO: add logic for what the agent does based on the first thing in vision list


                # for ob in sim._listOfObjectsHere((ownY - (int(self.geneticString[0]) - i)) % sim.gridSize, ownX, self):
                #     if type(ob) is Tree:
                #         visionList.append(0)
                #         break
                #     else:
                #         visionList.append(sim._assessCreature((ownY - (int(self.geneticString[0]) - i)) % sim.gridSize, ownX, self))
                # # if visionList[i] != 0:
                # #     return 1
                # if len(visionList) == 0:
                #     return 0

    def reorderListBasedOnHeading(self, list):
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

    def checkSmell(self,sim, listOfPossibleActions):
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
                if (type(object) is Stone and not self.canJump) or (type(object) is Water and not self.canSwim):
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
                            listOfPossibleActions = ['forward']
                    #enemy is in front
                    elif (object.getColor() != self.getColor()):
                        if self.getAggression() == 0:
                            try:
                                while True:
                                    listOfPossibleActions.remove('forward')
                            except ValueError:
                                pass
                        else:
                            listOfPossibleActions = ['forward']

                if (type(object) is Food and self.getAggression()==0 and self.getEnergy()<50):
                    listOfPossibleActions = ['forward']

            # Looking at the cell behind
            for object in cellsSmelled[1]:
                if (type(object) is Stone and not self.canJump) or (type(object) is Water and not self.canSwim):
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
                            listOfPossibleActions = ['turnAround']
                    #enemy is behind
                    elif (object.getColor() != self.getColor()):
                        if self.getAggression() == 0:
                            try:
                                while True:
                                    listOfPossibleActions.remove('turnAround')
                            except ValueError:
                                pass
                        else:
                            listOfPossibleActions = ['turnAround']

                if (type(object) is Food and self.getAggression()==0 and self.getEnergy()<50):
                    listOfPossibleActions = ['turnAround']

            # Looking at the cell to the right
            for object in cellsSmelled[2]:
                if (type(object) is Stone and not self.canJump) or (type(object) is Water and not self.canSwim):
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
                            listOfPossibleActions = ['right']
                    #enemy is to the right
                    elif (object.getColor() != self.getColor()):
                        if self.getAggression() == 0:
                            try:
                                while True:
                                    listOfPossibleActions.remove('right')
                            except ValueError:
                                pass
                        else:
                            listOfPossibleActions = ['right']

                if (type(object) is Food and self.getAggression()==0 and self.getEnergy()<50):
                    listOfPossibleActions = ['right']

            # Looking at the cell to the left
            for object in cellsSmelled[3]:
                if (type(object) is Stone and not self.canJump) or (type(object) is Water and not self.canSwim):
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
                            listOfPossibleActions = ['left']
                    #enemy is to the left
                    elif (object.getColor() != self.getColor()):
                        if self.getAggression() == 0:
                            try:
                                while True:
                                    listOfPossibleActions.remove('left')
                            except ValueError:
                                pass
                        else:
                            listOfPossibleActions = ['left']

                if (type(object) is Food and self.getAggression()==0 and self.getEnergy()<50):
                    listOfPossibleActions = ['left']

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
            print("R2CellsSmelled:",radius2cellssmelled)

            # Looking at the cell in 2 squares front
            for object in radius2cellssmelled[0]:
                if (type(object) is Agent):
                    # if it is a friend
                    if (object.getColor() == self.getColor()):
                        # if ready to breeed
                        if self.getReadyToBreed() == 0 and 'forward' in listOfPossibleActions:
                                listOfPossibleActions = ['forward']
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
                                listOfPossibleActions = ['forward']

                if (type(object) is Food and self.getAggression() == 0 and self.getEnergy() < 50):
                    if 'forward' in listOfPossibleActions:
                        listOfPossibleActions = ['forward']

            # Looking at the cell 2 squares behind
            for object in radius2cellssmelled[1]:
                if (type(object) is Agent):
                    # if it is a friend
                    if (object.getColor() == self.getColor()):
                        # if ready to breed
                        if self.getReadyToBreed() == 0 and 'turnAround' in listOfPossibleActions:
                            listOfPossibleActions = ['turnAround']
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
                                listOfPossibleActions = ['turnAround']

                if (type(object) is Food and self.getAggression() == 0 and self.getEnergy() < 50):
                    if 'turnAround' in listOfPossibleActions:
                        listOfPossibleActions = ['turnAround']

            # Looking at the cell 2 squares to the right
            for object in radius2cellssmelled[2]:
                if (type(object) is Agent):
                    # if it is a friend
                    if (object.getColor() == self.getColor()):
                        # if ready to breeed
                        if self.getReadyToBreed() == 0 and 'right' in listOfPossibleActions:
                            listOfPossibleActions = ['right']
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
                                listOfPossibleActions = ['right']

                if (type(object) is Food and self.getAggression() == 0 and self.getEnergy() < 50):
                    if 'right' in listOfPossibleActions:
                        listOfPossibleActions = ['right']

            # Looking at the cell 2 squares to the left
            for object in radius2cellssmelled[3]:
                if (type(object) is Agent):
                    # if it is a friend
                    if (object.getColor() == self.getColor()):
                        # if ready to breeed
                        if self.getReadyToBreed() == 0 and 'left' in listOfPossibleActions:
                            listOfPossibleActions = ['left']
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
                                listOfPossibleActions = ['left']

                if (type(object) is Food and self.getAggression() == 0 and self.getEnergy() < 50):
                    if 'left' in listOfPossibleActions:
                        listOfPossibleActions = ['left']

            # Looking at the cell above and left
            for object in radius2cellssmelled[4]:
                if (type(object) is Agent):
                    # if it is a friend
                    if (object.getColor() == self.getColor()):
                        # if ready to breed
                        if self.getReadyToBreed() == 0:
                            if 'forward' in listOfPossibleActions:
                                listOfPossibleActions = ['forward']
                            elif 'left' in listOfPossibleActions:
                                listOfPossibleActions = ['left']
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
                                listOfPossibleActions = ['forward']
                            elif 'left' in listOfPossibleActions:
                                listOfPossibleActions = ['left']

                if (type(object) is Food and self.getAggression() == 0 and self.getEnergy() < 50):
                    if 'forward' in listOfPossibleActions:
                        listOfPossibleActions = ['forward']
                    elif 'left' in listOfPossibleActions:
                        listOfPossibleActions = ['left']

            # Looking at the cell above and right
            for object in radius2cellssmelled[5]:
                if (type(object) is Agent):
                    # if it is a friend
                    if (object.getColor() == self.getColor()):
                        # if ready to breed
                        if self.getReadyToBreed() == 0:
                            if 'forward' in listOfPossibleActions:
                                listOfPossibleActions = ['forward']
                            elif 'right' in listOfPossibleActions:
                                listOfPossibleActions = ['right']
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
                                listOfPossibleActions = ['forward']
                            elif 'right' in listOfPossibleActions:
                                listOfPossibleActions = ['right']

                if (type(object) is Food and self.getAggression() == 0 and self.getEnergy() < 50):
                    if 'forward' in listOfPossibleActions:
                        listOfPossibleActions = ['forward']
                    elif 'right' in listOfPossibleActions:
                        listOfPossibleActions = ['right']

            # Looking at the cell below and left
            for object in radius2cellssmelled[6]:
                if (type(object) is Agent):
                    # if it is a friend
                    if (object.getColor() == self.getColor()):
                        # if ready to breed
                        if self.getReadyToBreed() == 0:
                            if 'turnAround' in listOfPossibleActions:
                                listOfPossibleActions = ['turnAround']
                            elif 'left' in listOfPossibleActions:
                                listOfPossibleActions = ['left']
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
                                listOfPossibleActions = ['turnAround']
                            elif 'left' in listOfPossibleActions:
                                listOfPossibleActions = ['left']

                if (type(object) is Food and self.getAggression() == 0 and self.getEnergy() < 50):
                    if 'turnAround' in listOfPossibleActions:
                        listOfPossibleActions = ['turnAround']
                    elif 'left' in listOfPossibleActions:
                        listOfPossibleActions = ['left']

            # Looking at the cell below and right
            for object in radius2cellssmelled[7]:
                if (type(object) is Agent):
                    # if it is a friend
                    if (object.getColor() == self.getColor()):
                        # if ready to breed
                        if self.getReadyToBreed() == 0:
                            if 'turnAround' in listOfPossibleActions:
                                listOfPossibleActions = ['turnAround']
                            elif 'right' in listOfPossibleActions:
                                listOfPossibleActions = ['right']
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
                                listOfPossibleActions = ['turnAround']
                            elif 'right' in listOfPossibleActions:
                                listOfPossibleActions = ['right']

                if (type(object) is Food and self.getAggression() == 0 and self.getEnergy() < 50):
                    if 'turnAround' in listOfPossibleActions:
                        listOfPossibleActions = ['turnAround']
                    elif 'right' in listOfPossibleActions:
                        listOfPossibleActions = ['right']
        else:
            print("CANT SMELL")

        print("Actions after smell: " + str(listOfPossibleActions))
        return listOfPossibleActions


    def determineAction(self, sim, time):
        listOfPossibleActions = ['left', 'right', 'turnAround', 'forward', 'forward', 'forward']


        # ---------- Check where we are ---------- #
        # sets the action based on what we are standing on
        listOfPossibleActions = self.checkHere(sim, listOfPossibleActions)
        print("Actions after here: ", listOfPossibleActions)

        # ---------- Check what we see ---------- #
        # if it isn't standing on anything, keep going
        # sets the action based on what we see
        listOfPossibleActions = self.checkVision(sim, listOfPossibleActions)
        print("Actions after vision: ", listOfPossibleActions)

        # ---------- Check what we smell ---------- #
        # sets the action based on what we can smell
        listOfPossibleActions = self.checkSmell(sim, listOfPossibleActions)
        print("Actions after smell: ", listOfPossibleActions)


        if listOfPossibleActions == []:
            return random.choice(['left', 'right', 'turnAround'])

        action = random.choice(listOfPossibleActions)
        print("Action: ", action)
        return action

    # TEST
    # def determineAction(self, sim, agent, time):
    #     agentR, agentC, agentH = self.getPose()
    #     # checks to see if there is a creature where the agent currently is
    #     isCreatureHere = sim._assessCreatureHere(agentR, agentC)
    #     # checks to see if there is a creature in the agent's vision
    #     isCreatureAhead = self._areCreaturesInVision(sim)
    #
    #     if sim._assessObjectsHere == 4:
    #         isCreatureAhead=[]
    #     print("Can I see a creature: ", isCreatureAhead)
    #
    #     # checks to see if there is food where the agent currently is
    #     isFoodHere = sim.foodAt(agentR, agentC)
    #     # checks to see if there is a creature in the agent's smell radius
    #     cellsSmelled = self.detectSmellRadius(sim)
    #     detectedRocks = self.detectRocks(sim)
    #     detectedWater = self.detectWater(sim)
    #
    #     listOfRandomActionsPossible = ['left', 'right', 'turnAround', 'forward', 'forward', 'forward']
    #     listOfRandomActionsPossible = self.filterActionsByWater(listOfRandomActionsPossible, detectedWater)
    #     listOfRandomActionsPossible = self.filterActionsByRocks(listOfRandomActionsPossible,detectedRocks)
    #     if self.isAwake(agent.sleepValue, time) == "awake":
    #         if agent.Aggression == 0:
    #             # print(self.determineActionDocile(agent, isCreatureHere, isCreatureAhead, cellsSmelled, isFoodHere, detectedRocks, listOfRandomActionsPossible))
    #             return self.determineActionDocile(agent, isCreatureHere, isCreatureAhead, cellsSmelled, isFoodHere, detectedRocks, listOfRandomActionsPossible)
    #         elif agent.Aggression == 1:
    #             # print(self.determineActionAggressive(agent, isCreatureHere, isCreatureAhead, cellsSmelled, detectedRocks, listOfRandomActionsPossible))
    #             return self.determineActionAggressive(agent, isCreatureHere, isCreatureAhead, cellsSmelled, detectedRocks, listOfRandomActionsPossible)
    #         else:
    #             print("SHOULD NOT GET HERE")
    #
    #     elif self.isAwake(agent.sleepValue, time) == "sleeping":
    #         return "none"
    #
    #
    # def determineActionDocile(self, agent, isCreatureHere, isCreatureAhead, cellsSmelled, isFoodHere, detectedRocks, listOfRandomActionsPossible):
    #     # print("Creatures around: " + str(creaturesAround))
    #     # if the agent is on the same square as a friend
    #     # print("list of actions possible docile:", listOfRandomActionsPossible)
    #     if len(listOfRandomActionsPossible) == 0:
    #         return "turnAround"
    #
    #     # print(listOfRandomActionsPossible)
    #
    #     if isCreatureHere == 2:
    #         if agent.getReadyToBreed() == 0:
    #             return "breed"
    #         else:
    #             return random.choice(listOfRandomActionsPossible)
    #
    #     elif len(isFoodHere) > 0:
    #         return "eat"
    #
    #     # if the agent sees an enemy on a square ahead
    #     elif isCreatureAhead == 1:
    #         if 'forward' in listOfRandomActionsPossible:
    #             if len(listOfRandomActionsPossible) != 1:
    #                 listOfRandomActionsPossible.remove('forward')
    #         return random.choice(listOfRandomActionsPossible)
    #
    #     # if the agent sees a friend ahead
    #     elif isCreatureAhead == 2:
    #         # if they are ready to breed, go forward
    #         if agent.getReadyToBreed() == 0:
    #             return "forward"
    #         # if they aren't, go a anywhere
    #         else:
    #             return random.choice(listOfRandomActionsPossible)
    #
    #     # if it can't see any creatures, and can't smell any creatures: go anywhere
    #     elif isCreatureAhead == 0 and cellsSmelled == "none":
    #         # for i in range(2):
    #         #     listOfRandomActionsPossible.append('forward')
    #         return random.choice(listOfRandomActionsPossible)
    #
    #     # if it can't see any creatures, and but it can smell creatures:
    #     elif isCreatureAhead == 0 and cellsSmelled != "none":
    #         # print("MADE IT HERE - can't see anything, can smell something")
    #         if cellsSmelled[1] == 1:
    #             if cellsSmelled[0] == "above":
    #                 if 'forward' in listOfRandomActionsPossible:
    #                     if len(listOfRandomActionsPossible) != 1:
    #                         listOfRandomActionsPossible.remove('forward')
    #                 return random.choice(listOfRandomActionsPossible)
    #
    #             elif cellsSmelled[0] == "left":
    #                 if 'left' in listOfRandomActionsPossible:
    #                     if len(listOfRandomActionsPossible) != 1:
    #                         listOfRandomActionsPossible.remove('left')
    #                 if detectedRocks[0] == -1:
    #                     return random.choice(listOfRandomActionsPossible)
    #                 else:
    #                     if 'forward' in listOfRandomActionsPossible:
    #                         listOfRandomActionsPossible.append('forward')
    #                     return random.choice(listOfRandomActionsPossible)
    #
    #             elif cellsSmelled[0] == "right":
    #                 if 'right' in listOfRandomActionsPossible:
    #                     if len(listOfRandomActionsPossible) != 1:
    #                         listOfRandomActionsPossible.remove('right')
    #                 if detectedRocks[0] == -1:
    #                     return random.choice(listOfRandomActionsPossible)
    #                 else:
    #                     if 'forward' in listOfRandomActionsPossible:
    #                         listOfRandomActionsPossible.append('forward')
    #                     return random.choice(listOfRandomActionsPossible)
    #
    #             elif cellsSmelled[0] == "below":
    #                 if 'turnAround' in listOfRandomActionsPossible:
    #                     if len(listOfRandomActionsPossible) != 1:
    #                         listOfRandomActionsPossible.remove('turnAround')
    #                 if detectedRocks[0] == -1:
    #                     return random.choice(listOfRandomActionsPossible)
    #                 else:
    #                     if 'forward' in listOfRandomActionsPossible:
    #                         listOfRandomActionsPossible.append('forward')
    #                     return random.choice(listOfRandomActionsPossible)
    #
    #         elif (cellsSmelled[1] == 2 and agent.getReadyToBreed()) or cellsSmelled[1] == 3:
    #             if cellsSmelled[0] == "above":
    #                 if 'forward' in listOfRandomActionsPossible:
    #                     return "forward"
    #                 else:
    #                     return random.choice(listOfRandomActionsPossible)
    #             elif cellsSmelled[0] == "left":
    #                 if 'left' in listOfRandomActionsPossible:
    #                     return "left"
    #                 else:
    #                     return random.choice(listOfRandomActionsPossible)
    #             elif cellsSmelled[0] == "right":
    #                 if 'right' in listOfRandomActionsPossible:
    #                     return "right"
    #                 else:
    #                     return random.choice(listOfRandomActionsPossible)
    #             elif cellsSmelled[0] == "below":
    #                 if 'turnAround' in listOfRandomActionsPossible:
    #                     return "turnAround"
    #                 else:
    #                     return random.choice(listOfRandomActionsPossible)
    #         else:
    #             # if 'forward' in listOfRandomActionsPossible:
    #             #     for i in range(2):
    #             #         listOfRandomActionsPossible.append('forward')
    #             return random.choice(listOfRandomActionsPossible)
    #
    #     else:
    #         print("action chosen: NONE(SHOULD NEVER GET HERE) --- choosing 'forward' as action")
    #         return 'forward'
    #
    # def determineActionAggressive(self, agent, isCreatureHere, isCreatureAhead, cellsSmelled, detectedRocks, listOfRandomActionsPossible):
    #     # print("list of actions possible aggressive:",listOfRandomActionsPossible)
    #
    #     if len(listOfRandomActionsPossible) == 0:
    #         return "turnAround"
    #
    #     creaturesAround = cellsSmelled
    #
    #     if isCreatureHere == 1:
    #         return "attack"
    #
    #     # if the agent is on the same square as a friend
    #     elif isCreatureHere == 2:
    #         if agent.getReadyToBreed() == 0:
    #             return "breed"
    #         else:
    #             return random.choice(listOfRandomActionsPossible)
    #
    #     elif isCreatureAhead == 1:
    #         return "forward"
    #
    #     # if it can't see any creatures, and can't smell any creatures: go anywhere, prioritizing forward moves
    #     elif isCreatureAhead == 0 and creaturesAround == "none":
    #         for i in range(2):
    #             listOfRandomActionsPossible.append('forward')
    #         return random.choice(listOfRandomActionsPossible)
    #
    #     # if it can't see any creatures, and but it can smell any creatures:
    #     elif isCreatureAhead == 0 and creaturesAround != "none":
    #         if creaturesAround[1] == 1:
    #             if creaturesAround[0] == "above":
    #                 return 'forward'
    #             elif creaturesAround[0] == "left":
    #                 return 'left'
    #             elif creaturesAround[0] == "right":
    #                 return 'right'
    #             elif creaturesAround[0] == "below":
    #                 return 'turnAround'
    #         elif creaturesAround[1] == 2 and agent.getReadyToBreed() == 0:
    #             if creaturesAround[0] == "above":
    #                 return "forward"
    #             elif creaturesAround[0] == "left":
    #                 return "left"
    #             elif creaturesAround[0] == "right":
    #                 return "right"
    #             elif creaturesAround[0] == "below":
    #                 return "turnAround"
    #         elif creaturesAround[1] == -1:
    #             return random.choice(listOfRandomActionsPossible)
    #
    #         else:
    #             return random.choice(listOfRandomActionsPossible)
    #
    #     else:
    #         print("action chosen: NONE(SHOULD NEVER GET HERE) --- choosing 'forward' as action")
    #         return 'forward'

    def filterActionsByWater(self, listOfRandomActionsPossible, detectedWater):
        newListOfRandomActionsPossible = listOfRandomActionsPossible.copy()
        if self.getSwim() == 0:
            if detectedWater[0] == -2:
                while True:
                    if 'forward' in newListOfRandomActionsPossible:
                        newListOfRandomActionsPossible.remove('forward') #Removes ALL instances of 'forward'
                    else:
                        break
            if detectedWater[1] == -2:
                while True:
                    if 'turnAround' in newListOfRandomActionsPossible:
                        newListOfRandomActionsPossible.remove('turnAround')  # Removes ALL instances of 'turnAround'
                    else:
                        break
            if detectedWater[2] == -2:
                while True:
                    if 'right' in newListOfRandomActionsPossible:
                        newListOfRandomActionsPossible.remove('right')  # Removes ALL instances of 'right'
                    else:
                        break
            if detectedWater[3] == -2:
                while True:
                    if 'left' in newListOfRandomActionsPossible:
                        newListOfRandomActionsPossible.remove('left')  # Removes ALL instances of 'left'
                    else:
                        break
        return newListOfRandomActionsPossible

    def filterActionsByRocks(self, listOfRandomActionsPossible, detectedRocks):
        newListOfRandomActionsPossible = listOfRandomActionsPossible.copy()
        if self.getJump() == 0:
            if detectedRocks[0] == -1:
                while True:
                    if 'forward' in newListOfRandomActionsPossible:
                        newListOfRandomActionsPossible.remove('forward') #Removes ALL instances of 'forward'
                    else:
                        break
            if detectedRocks[1] == -1:
                while True:
                    if 'turnAround' in newListOfRandomActionsPossible:
                        newListOfRandomActionsPossible.remove('turnAround')  # Removes ALL instances of 'turnAround'
                    else:
                        break
            if detectedRocks[2] == -1:
                while True:
                    if 'right' in newListOfRandomActionsPossible:
                        newListOfRandomActionsPossible.remove('right')  # Removes ALL instances of 'right'
                    else:
                        break
            if detectedRocks[3] == -1:
                while True:
                    if 'left' in newListOfRandomActionsPossible:
                        newListOfRandomActionsPossible.remove('left')  # Removes ALL instances of 'left'
                    else:
                        break
        return newListOfRandomActionsPossible

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


    def smellRadiusGlobal1(self, sim):
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

    def detectRocks(self, sim):
        detectedRocks = self.smellRadiusGlobal1(sim)
        # print("Dectected Rocks: ", detectedRocks)
        order = []

        ownY, ownX, heading = self.getPose()

        if heading == "n":
            return detectedRocks
        elif heading == "s":
            order = [1, 0, 2, 3]
        elif heading == "e":
            order = [2, 3, 1, 0]
        elif heading == "w":
            order = [3, 2, 0, 1]
        else:
            print("HEADING INVALID: RETURNING NORTH")
            return detectedRocks

        detectedRocks = [detectedRocks[i] for i in order]

        return detectedRocks

    def detectWater(self, sim):
        detectedWater = self.smellRadiusGlobal1(sim)

        ownY, ownX, heading = self.getPose()

        if heading == "n":
            return detectedWater
        elif heading == "s":
            order = [1, 0, 2, 3]
        elif heading == "e":
            order = [2, 3, 1, 0]
        elif heading == "w":
            order = [3, 2, 0, 1]
        else:
            print("HEADING INVALID: RETURNING NORTH")
            return detectedWater

        detectedWater = [detectedWater[i] for i in order]

        return detectedWater


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

    def getTypeAbbreviation(self):
        # return "a"
        return self.colorAbbrevs[self.color]


    def __str__(self):
        formStr = "Agent: col={5}  pos=({0:>3d}, {1:>3d}, {2:^3s})   energ={3:^6d}     genStr={4}"
        return formStr.format(self.row, self.col, self.heading, self.energy, self.geneticString, self.colorNames[self.color])





    # def smellRadiusFood1(self, sim):
    #     ownY, ownX, heading = self.getPose()
    #     cellsSmelled = []
    #
    #     cellAbove = sim._assessFood((ownY - 1) % sim.gridSize, ownX)
    #     cellBelow = sim._assessFood((ownY + 1) % sim.gridSize, ownX)
    #     cellRight = sim._assessFood(ownY, (ownX + 1) % sim.gridSize)
    #     cellLeft = sim._assessFood(ownY, (ownX - 1) % sim.gridSize)
    #
    #     cellsSmelled.append(cellAbove)
    #     cellsSmelled.append(cellBelow)
    #     cellsSmelled.append(cellRight)
    #     cellsSmelled.append(cellLeft)
    #
    #     return cellsSmelled
    #
    # def smellRadiusFood2(self, sim):
    #     ownY, ownX, heading = self.getPose()
    #     cellsSmelled = []
    #
    #     cellAbove = sim._assessFood((ownY - 1) % sim.gridSize, ownX)
    #     cellBelow = sim._assessFood((ownY + 1) % sim.gridSize, ownX)
    #     cellRight = sim._assessFood(ownY, (ownX + 1) % sim.gridSize)
    #     cellLeft = sim._assessFood(ownY, (ownX - 1) % sim.gridSize)
    #
    #     cellTwoAbove = sim._assessFood((ownY - 2) % sim.gridSize, ownX)
    #     cellTwoBelow = sim._assessFood((ownY + 2) % sim.gridSize, ownX)
    #     cellTwoRight = sim._assessFood(ownY, (ownX + 2) % sim.gridSize)
    #     cellTwoLeft = sim._assessFood(ownY, (ownX - 2) % sim.gridSize)
    #
    #     cellAboveLeft = sim._assessFood((ownY - 1) % sim.gridSize, (ownX - 1) % sim.gridSize)
    #     cellAboveRight = sim._assessFood((ownY - 1) % sim.gridSize, (ownX + 1) % sim.gridSize)
    #     cellBelowRight = sim._assessFood((ownY + 1) % sim.gridSize, (ownX + 1) % sim.gridSize)
    #     cellBelowLeft = sim._assessFood((ownY + 1) % sim.gridSize, (ownX - 1) % sim.gridSize)
    #
    #     cellsSmelled.append(cellAbove)
    #     cellsSmelled.append(cellBelow)
    #     cellsSmelled.append(cellRight)
    #     cellsSmelled.append(cellLeft)
    #
    #     cellsSmelled.append(cellTwoAbove)
    #     cellsSmelled.append(cellTwoBelow)
    #     cellsSmelled.append(cellTwoRight)
    #     cellsSmelled.append(cellTwoLeft)
    #
    #     cellsSmelled.append(cellAboveLeft)
    #     cellsSmelled.append(cellAboveRight)
    #     cellsSmelled.append(cellBelowLeft)
    #     cellsSmelled.append(cellBelowRight)
    #
    #     return cellsSmelled


    # def smellRadiusCreature1(self, sim):
    #     ownY, ownX, heading = self.getPose()
    #     cellsSmelled = []
    #
    #     cellAbove = sim._assessCreature((ownY - 1) % sim.gridSize, ownX, self)
    #     cellBelow = sim._assessCreature((ownY + 1) % sim.gridSize, ownX, self)
    #     cellRight = sim._assessCreature(ownY, (ownX + 1) % sim.gridSize, self)
    #     cellLeft = sim._assessCreature(ownY, (ownX - 1) % sim.gridSize, self)
    #
    #     cellsSmelled.append(cellAbove)
    #     cellsSmelled.append(cellBelow)
    #     cellsSmelled.append(cellRight)
    #     cellsSmelled.append(cellLeft)
    #
    #     return cellsSmelled
    #
    # def smellRadiusCreature2(self, sim):
    #     ownY, ownX, heading = self.getPose()
    #     cellsSmelled = []
    #
    #     cellAbove = sim._assessCreature((ownY - 1) % sim.gridSize, ownX, self)
    #     cellBelow = sim._assessCreature((ownY + 1) % sim.gridSize, ownX, self)
    #     cellRight = sim._assessCreature(ownY, (ownX + 1) % sim.gridSize, self)
    #     cellLeft = sim._assessCreature(ownY, (ownX - 1) % sim.gridSize, self)
    #
    #     cellTwoAbove = sim._assessCreature((ownY - 2) % sim.gridSize, ownX, self)
    #     cellTwoBelow = sim._assessCreature((ownY + 2) % sim.gridSize, ownX, self)
    #     cellTwoRight = sim._assessCreature(ownY, (ownX + 2) % sim.gridSize, self)
    #     cellTwoLeft = sim._assessCreature(ownY, (ownX - 2) % sim.gridSize, self)
    #
    #     cellAboveLeft = sim._assessCreature((ownY - 1) % sim.gridSize, (ownX - 1) % sim.gridSize, self)
    #     cellAboveRight = sim._assessCreature((ownY - 1) % sim.gridSize, (ownX + 1) % sim.gridSize, self)
    #     cellBelowRight = sim._assessCreature((ownY + 1) % sim.gridSize, (ownX + 1) % sim.gridSize, self)
    #     cellBelowLeft = sim._assessCreature((ownY + 1) % sim.gridSize, (ownX - 1) % sim.gridSize, self)
    #
    #     cellsSmelled.append(cellAbove)
    #     cellsSmelled.append(cellBelow)
    #     cellsSmelled.append(cellRight)
    #     cellsSmelled.append(cellLeft)
    #
    #     cellsSmelled.append(cellTwoAbove)
    #     cellsSmelled.append(cellTwoBelow)
    #     cellsSmelled.append(cellTwoRight)
    #     cellsSmelled.append(cellTwoLeft)
    #
    #     cellsSmelled.append(cellAboveLeft)
    #     cellsSmelled.append(cellAboveRight)
    #     cellsSmelled.append(cellBelowLeft)
    #     cellsSmelled.append(cellBelowRight)
    #
    #     return cellsSmelled