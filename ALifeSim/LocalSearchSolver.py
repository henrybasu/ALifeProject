"""  =================================================================
File: SearchSolver.py

This file contains generic definitions for a state space SearchState class,
and a general SearchSolver class.  These classes should be subclassed to make
solvers for a specific problem.
 ==================================================================="""

import random
import math


# Change this to true to see information about the search as it goes.
verbose = False


class RulesetState(object):
    """
    This represents a "state" for the local search. Essentially, this packages up a particular rule string with some
    methods to generate neighbor states, and the functionality to call an evaluation function and pass the rule string
    to it to determine the value of a string.
    """

    RULE_LEN = 27

    def __init__(self, evalFunction, maxValue, ruleString=None):
        """Initialize the two basic instance variables to some value"""
        self.evalFunction = evalFunction
        self.maxValue = maxValue
        self.stateValue = None
        #TODO: We don't know if this is right VVV
        self.n = 27

        if ruleString is not None:
            self.ruleString = ruleString
        else:
            self.ruleString = self._randomRuleset()

    def getValue(self):
        """Access the value of the myCost instance variable"""
        if self.stateValue is None:
            self.stateValue = self.evalFunction(self.ruleString)
        return self.stateValue

    def getMaxValue(self):
        """Return the maximum value this state has been reported to have."""
        return self.maxValue

    def allNeighbors(self):
        """Generates all neighbors of this state. For the rules, that means all one-symbol changes."""
        neighbors = []
        for i in range(len(self.ruleString)):
            currSym = self.ruleString[i]
            otherSyms = self._otherSymbols(currSym)
            for c in otherSyms:
                newRule = self.ruleString[:i] + c + self.ruleString[i+1:]
                newState = RulesetState(self.evalFunction, self.maxValue, newRule)
                neighbors.append(newState)
        return neighbors

    def someNeighbors(self):
        """Generates 5 neighbors of this state. For the ruleset, that means all one-symbol changes."""
        neighbors = []
        for i in range(5):
            currSym = self.ruleString[i]
            otherSyms = self._otherSymbols(currSym)
            for c in otherSyms:
                newRule = self.ruleString[:i] + c + self.ruleString[i+1:]
                newState = RulesetState(self.evalFunction, self.maxValue, newRule)
                neighbors.append(newState)
        return neighbors

    def _otherSymbols(self, sym):
        """Given a symbol, return a string of the other symbols besides it."""
        if sym == 'a':
            return 'sflr'
        elif sym == 's':
            return 'aflr'
        elif sym == 'f':
            return 'aslr'
        elif sym == 'l':
            return 'asfr'
        elif sym == 'r':
            return 'asfl'
        else:
            print("_otherSymbols: should never get here!")

    def randomNeighbors(self, num):
        """Generate num random neighbors of this state. Note that the same neighbor could be generated more than once."""
        neighbors = []
        for i in range(num):
            newS = self.makeRandomMove()
            neighbors.append(newS)
        return neighbors

    def makeRandomMove(self):
        """Takes a ruleset and returns a new ruleset identical to the original, but with one random change."""
        randElem = random.randrange(len(self.ruleString))
        opts = self._otherSymbols(self.ruleString[randElem])
        newElem = random.choice(opts)
        print(self.ruleString[:randElem])
        print(newElem)
        print(self.ruleString[randElem+1:])
        newRules = self.ruleString[:randElem] + newElem + self.ruleString[randElem+1:]
        return RulesetState(self.evalFunction, self.maxValue, newRules)

    def getRandomStates(self, n):
        """Builds n random states that use the same eval function and max value but are
        unrelated to this state."""
        newStates = []
        for i in range(n):
            newRule = self._randomRuleset()
            newState = RulesetState(self.evalFunction, self.maxValue, newRule)
            newStates.append(newState)
        return newStates

    def _randomRuleset(self):
        """Generate a random ruleset string"""
        options = "sflr"  # Leaving out the "arbitrary" random behavior
        rules = ""
        for i in range(self.RULE_LEN):
            rules += random.choice(options)
        return rules

    def __str__(self):
        """Make a string representation of this state, for printing"""
        return self.ruleString

    def crossover(self, otherState):
        """Given another NQueens state, this computes a crossover point and creates
        two new states that have been crossed over."""
        crossPoint = random.randint(0, self.n)
        if crossPoint == 0 or crossPoint == self.n:
            new1 = self.copyState()
            new2 = otherState.copyState()
            return new1, new2
        else:
            new1String = self.ruleString[:crossPoint]+otherState.ruleString[crossPoint:]
            new2String = otherState.ruleString[:crossPoint] + self.ruleString[crossPoint:]
            new1 = RulesetState(self.evalFunction, self.maxValue, new1String)
            new2 = RulesetState(self.evalFunction, self.maxValue, new2String)
            return new1, new2

    def copyState(self):
        """Builds and returns a new board identical to this one."""
        return RulesetState(self.evalFunction, self.maxValue, self.ruleString)



# ==================================================================
# This section contains an implementation of straightforward
# Hill Climbing. It requires a state class that creates objects
# that implement the following methods: getValue, getMaxValue,
# allNeighbors, randomNeighbors, and that are printable

class HillClimber(object):
    """Contains the algorithm for hill-climbing and some helper methods."""

    def __init__(self, startState, maxRounds=500):
        """Sets up the starting state"""
        self.startState = startState
        self.maxRounds = maxRounds
        self.maxValue = startState.getMaxValue()
        self.currState = startState
        # This next step is EXPENSIVE!
        self.currValue = self.currState.getValue()
        self.count = 0
        if verbose:
            print("============= START ==============")

    def getCount(self):
        """Returns the current count."""
        return self.count

    def getCurrState(self):
        """Returns the current state."""
        return self.currState

    def getCurrValue(self):
        """Returns the value currently associated with the current state."""
        return self.currValue

    def run(self):
        """Perform the hill-climbing algorithm, starting with the given start state and going until a local maxima is
        found or the maximum rounds is reached"""
        status = None

        while self.currValue < self.maxValue and self.count < self.maxRounds:
            status = self.step()

            if status == 'optimal' or status == 'local maxima':
                break

        if verbose:
            print("============== FINAL STATE ==============")
            print(self.currState)
            print("   Number of steps =", self.count)
            if status == 'optimal':
                print("  FOUND PERFECT SOLUTION")
        return self.currValue, self.maxValue, self.count

    def step(self):
        """Runs one step of hill-climbing, generates children and picks the best one, returning it as its value. Also returns
        a second value that tells if the best child is optimal or not."""
        self.count += 1
        if self.count >= self.stopLimit:
            return "local maxima"

        if verbose:
            print("--------- Count =", self.count, "---------")
            print(self.currState)
        neighs = self.currState.allNeighbors()
        print(neighs)
        neighs2 = self.currState.someNeighbors()
        print(neighs2)
        bestNeigh = self.findBestNeighbor(neighs)
        nextValue = bestNeigh.getValue()
        self.currState = bestNeigh
        self.currValue = nextValue
        if nextValue == self.maxValue:
            return 'optimal'
        if nextValue >= self.currValue:
            if verbose:
                print("Best neighbor:")
                print(bestNeigh)
            return 'keep going'
        else:
            # best is worse than current
            return 'local maxima'

    def findBestNeighbor(self, neighbors):
        """Given a list of neighbors and values, find and return a neighbor with
        the best value. If there are multiple neighbors with the same best value,
        a random one is chosen"""
        startBest = neighbors[0]
        print(startBest.ruleString)
        bestValue = startBest.getValue()
        bestNeighs = [startBest]
        for neigh in neighbors[1:]:
            value = neigh.getValue()
            if value > bestValue:
                bestNeighs = [neigh]
                bestValue = value
            elif value == bestValue:
                bestNeighs.append(neigh)
        bestNeigh = random.choice(bestNeighs)
        return bestNeigh



# ==================================================================
# This section contains an implementation of
# Beam Search. It requires a state class that creates objects
# that implement the following methods: getValue, getMaxValue,
# allNeighbors, randomNeighbors, and that are printable

class BeamSearcher(object):
    """Contains the algorithm for beam search and some helper methods."""

    def __init__(self, stateGen, numStates = 2, stopLimit = 5):
        """Sets up the starting state"""
        self.stateGen = stateGen
        self.numStates = numStates
        self.stopLimit = stopLimit
        self.currState = stateGen
        self.currValue = self.currState.getValue()
        self.count = 0
        self.currStates = []
        self.foundOptimal = False
        self.currStates = stateGen.getRandomStates(numStates)

        self.maxValue = self.currStates[0].getMaxValue()
        self.sortByValue(self.currStates)

        if verbose:
            print("============= START ==============")

    def getCount(self):
        """Returns the current count."""
        return self.count

    def getCurrState(self):
        """Returns the current state."""
        return self.currState

    def getCurrValue(self):
        """Returns the value currently associated with the current state."""
        return self.currValue

    def run(self):
        """Perform the beam search algorithm, starting with given start states and going until an optimal solution is
        found or the maximum rounds is reached"""
        status = None

        while (not self.foundOptimal) and (self.count < self.stopLimit):

            status = self.step()

            if status == 'optimal' or status == 'local maxima':
                break

        if verbose:
            print("============== FINAL STATE ==============")
            print(self.currState)
            print("   Number of steps =", self.count)
            if status == 'optimal':
                print("  FOUND PERFECT SOLUTION")
        return self.currValue, self.stopLimit, self.count

    def step(self):
        """Runs one step of beam search, generates children and picks the best one, returning it as its value. Also returns
        a second value that tells the maximum number of steps and a third value that shows the current steps taken."""
        if True:
            print("--------- Count =", self.count, "---------")
            # print("currStates " + str(self.currStates))

        if self.count >= self.stopLimit:
            return "local maxima"

        self.sortByValue(self.currStates)
        foundOptimal = False

        bestNNeighs = []

        for nextState in self.currStates:
            neighs = nextState.randomNeighbors(self.numStates)
            #print("currStates: (before inputting into keepBestNNeighbors) " + str(self.currStates))
            (bestNNeighs, foundOptimal) = self.keepBestNNeighbors(self.currStates, neighs, self.numStates, self.stopLimit)
            #print("BestNNeighs " + str(bestNNeighs))
            if foundOptimal:
                if verbose:
                    return "optimal"
        self.currStates = bestNNeighs
        #print("currStates: " + str(self.currStates))
        self.count += 1
        self.currState = self.currStates[0]
        return self.currState.getValue(), self.stopLimit, self.count

    def findBestNeighbor(self, neighbors):
        """Given a list of neighbors and values, find and return a neighbor with
        the best value. If there are multiple neighbors with the same best value,
        a random one is chosen"""
        startBest = neighbors[0]
        print(startBest.ruleString)
        bestValue = startBest.getValue()
        bestNeighs = [startBest]
        for neigh in neighbors[1:]:
            value = neigh.getValue()
            if value > bestValue:
                bestNeighs = [neigh]
                bestValue = value
            elif value == bestValue:
                bestNeighs.append(neigh)
        bestNeigh = random.choice(bestNeighs)
        return bestNeigh

    def keepBestNNeighbors(self, bestSoFar, neighs, n, maxVal):
        """Takes in a list of all neighbors, and the number to select, and it selects
        the best n neighbors.  If one of the neighbors is optimal, then it returns
        just that neighbor, and the flag True.  If none is optimal, it returns the best
        n of them, with the flag False."""
        neighs.sort(key=lambda neigh: - neigh.getValue())
        bestNeigh = neighs[0]
        if bestNeigh.getValue() == maxVal:  # if we have found an optimal solution
            return ([bestNeigh], True)
        else:
            i = 0
            while i < len(neighs):
                nextNeigh = neighs[i]
                if len(bestSoFar) == n:
                    worstOfBest = bestSoFar[-1]
                    if nextNeigh.getValue() < worstOfBest.getValue():
                        break
                #print(bestSoFar)
                self.insertState(bestSoFar, nextNeigh, n)
                i = i + 1
            return (bestSoFar, False)

    def sortByValue(self, stateList):
        """Takes in a list and sorts it from highest to lowest values."""
        stateList.sort(key=lambda neigh: - neigh.getValue())

    def insertState(self, sortedList, newState, limit):
        """Takes in a list sorted by value, with highest values at the front, and it
        inserts the new state in the proper place. There is a length limit; if exceeded
        then the last element (the one with lowest value) is removed."""
        i = 0
        for state in sortedList:
            if newState.getValue() > state.getValue():
                break
            i = i + 1
        sortedList.insert(i, newState)
        if len(sortedList) > limit:
            sortedList.pop(-1)



# ==================================================================
# This section contains an implementation of
# Genetic Algorithm. It requires a state class that creates objects
# that implement the following methods: getValue, getMaxValue,
# allNeighbors, randomNeighbors, and that are printable

class GASearcher(object):
    """Contains the algorithm for GA and some helper methods."""
    def __init__(self, stateGen, popSize=5, maxGenerations=2000, crossPerc=0.8, mutePerc=0.01):
        """Sets up the starting state"""
        self.stateGen = stateGen
        self.popSize = popSize
        self.currState = stateGen
        self.maxGenerations = maxGenerations
        self.crossPerc = crossPerc
        self.mutePerc = mutePerc
        self.parentPool = []
        self.currValue = self.currState.getValue()

        if popSize % 2 == 1:
            print("Making population size even")
            popSize += 1

        self.currStates = stateGen.getRandomStates(popSize)


        self.maxFit = self.currStates[0].getMaxValue()

        self.sortByValue(self.currStates)

        if verbose:
            print("============= START ==============")

        self.count = 0
        self.foundOptimal = False
        self.overallBest = self.currStates[0]


    def getCount(self):
        """Returns the current count."""
        return self.count

    def getCurrState(self):
        """Returns the current state."""
        return self.currState

    def getCurrValue(self):
        """Returns the value currently associated with the current state."""
        return self.currValue

    def run(self):
        """Perform the genetic algorithm, starting with given start states and going until an optimal solution is
        found or the maximum rounds is reached"""
        status = None

        while (not self.foundOptimal) and self.count < self.maxGenerations:
            if True:
                print("--------- Count =", self.count, "---------")

            status = self.step()

            if status == 'optimal' or status == 'local maxima':
                break

        if verbose:
            print("============== FINAL STATE ==============")
            print(self.currState)
            print("   Number of steps =", self.count)
            if status == 'optimal':
                print("  FOUND PERFECT SOLUTION")
        return self.currValue, self.maxGenerations, self.count

    def step(self):
        """Runs one step of genetic algorithm, generates children and picks the best one, returning it as its value. Also returns
        a second value maxFit that tells the optimal value and a third value that tells the number of steps taken so far."""
        self.count +=1
        print(self.count)
        fits = [state.getValue() for state in self.currStates]

        if self.count >= self.maxGenerations:
            return "optimal"

        if self.maxFit in fits:     # we have an optimal solution
            pos = fits.index(self.maxFit)
            bestOne = self.currStates[pos]
            self.foundOptimal = True
            return "optimal"
        else:
            bestLoc = fits.index(max(fits))
            bestOne = self.currStates[bestLoc]
            self.parentPool = self.selectParents(self.currStates, fits)
            self.currStates = self.mateParents(self.parentPool, self.crossPerc, self.mutePerc)

        if bestOne.getValue() > self.overallBest.getValue():
            self.overallBest = bestOne
            #return "optimal"

        return bestOne.getValue(), self.maxFit, self.count

    def findBestNeighbor(self, neighbors):
        """Given a list of neighbors and values, find and return a neighbor with
        the best value. If there are multiple neighbors with the same best value,
        a random one is chosen"""
        startBest = neighbors[0]
        print(startBest.ruleString)
        bestValue = startBest.getValue()
        bestNeighs = [startBest]
        for neigh in neighbors[1:]:
            value = neigh.getValue()
            if value > bestValue:
                bestNeighs = [neigh]
                bestValue = value
            elif value == bestValue:
                bestNeighs.append(neigh)
        bestNeigh = random.choice(bestNeighs)
        return bestNeigh

    def keepBestNNeighbors(self, bestSoFar, neighs, n, maxVal):
        """Takes in a list of all neighbors, and the number to select, and it selects
        the best n neighbors.  If one of the neighbors is optimal, then it returns
        just that neighbor, and the flag True.  If none is optimal, it returns the best
        n of them, with the flag False."""
        bestNeighbors = bestSoFar.sort(key=lambda neigh: - neigh.getValue())
        bestNeigh = bestNeighbors[0]
        if bestNeigh.getValue() == maxVal:  # if we have found an optimal solution
            return ([bestNeigh], True)
        else:
            i = 0
            while i < len(neighs):
                nextNeigh = neighs[i]
                if len(bestSoFar) == n:
                    worstOfBest = bestSoFar[-1]
                    if nextNeigh.getValue() < worstOfBest.getValue():
                        break
                bestSoFar.insertState(bestSoFar, nextNeigh, n)
                i = i + 1
            return (bestSoFar, False)

    def sortByValue(self, stateList):
        """Takes in a list and sorts it from highest to lowest values."""
        stateList.sort(key=lambda neigh: - neigh.getValue())

    def insertState(self, sortedList, newState, limit):
        """Takes in a list sorted by value, with highest values at the front, and it
        inserts the new state in the proper place. There is a length limit; if exceeded
        then the last element (the one with lowest value) is removed."""
        i = 0
        for state in sortedList:
            if newState.getValue() > state.getValue():
                break
            i = i + 1
        sortedList.insert(i, newState)
        if len(sortedList) > limit:
            sortedList.pop(-1)

    def selectParents(self, states, fitnesses):
        """Given a set of states, repeatedly select parents using roulette selection."""
        parents = []
        for i in range(len(states)):
            nextParentPos = rouletteSelect(fitnesses)
            parents.append(states[nextParentPos])
        return parents

    def mateParents(self, parents, crossoverPerc, mutationPerc):
        """Given a set of parents, pair them up and cross them together to make
        new children."""
        newPop = []
        for i in range(0, len(parents), 2):
            p1 = parents[i]
            p2 = parents[i + 1]
            doCross = random.random()
            if doCross < crossoverPerc:
                n1, n2 = p1.crossover(p2)
                newPop.append(n1)
                newPop.append(n2)
            else:
                newPop.append(p1.copyState())
                newPop.append(p2.copyState())
        for i in range(len(newPop)):
            nextOne = newPop[i]
            doMutate = random.random()
            if doMutate <= mutationPerc:
                newPop[i] = nextOne.makeRandomMove()
        return newPop



# ========================================================================
# This next section contains utility functions used by more than one of the algorithms

def rouletteSelect(valueList):
    """takes in a list giving the values for a set of entities.  It randomly
selects one of the positions in the list by treating the values as a kind of
probability distribution and sampling from that distribution.  Each entity gets
a piece of a roulette wheel whose size is based on comparative value: high-value
entities have the highest probability of being selected, but low-value entities have
*some* probability of being selected."""
    totalValues = sum(valueList)
    pick = random.random() * totalValues
    s = 0
    for i in range(len(valueList)):
        s += valueList[i]
        if s >= pick:
            return i
    return len(valueList) - 1

def addNewRandomMove(state, stateList):
    """Generates new random moves (moving one queen within her column) until
    it finds one that is not already in the list of boards. If it finds one,
    then it adds it to the list. If it tries 100 times and doesn't find one,
    then it returns without changing the list"""
    nextNeigh = state.makeRandomMove()
    count = 0

    while alreadyIn(nextNeigh, stateList):
        nextNeigh = state.makeRandomMove()
        count += 1
        if count > 100:
            # if tried 100 times and no valid new neighbor, give up!
            return
    stateList.append(nextNeigh)

def alreadyIn(state, stateList):
    """Takes a state and a list of state, and determines whether the state
    already appears in the list of states"""
    for s in stateList:
        if state == s:
            return True
    return False

def printNeighbors(neighList, full = True):
    """Takes a list of neighbors and values, and prints them all out"""
    print("Neighbors:")
    for neigh in neighList:
        neigh.setPrintMode(full)
        print(neigh)
