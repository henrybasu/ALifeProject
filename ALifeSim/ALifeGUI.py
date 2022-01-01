"""  =================================================================
File: ALifeGUI.py

This file contains code, including a Tkinter class, that implements the
GUI for this simulation.  This must be run in Python 3!
 ==================================================================="""

import collections
import time
import random
import string
import tkinter
from tkinter import *
import tkinter.filedialog as tkFileDialog
from PIL import Image,ImageTk

import ALifeSim
from LocalSearchSolver import RulesetState, HillClimber, BeamSearcher, GASearcher

class ALifeGUI:
    """Set up and manage all the variables for the GUI interface."""
    def __init__(self, gridDim, numAgents=10, maxSteps=100):
        """Given the dimension of the grid, and the number of agents set up a new Tk object of the right size"""
        self.root = Tk()
        sizex = 900
        sizey = 800
        posx = 540
        posy = 0
        self.root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
        self.root.title("Jonathan and Henry's ALife Simulation")
        self.gridDim = gridDim
        self.userInputtedGeneticStrings = []
        self.numberAgents = numAgents
        self.numberStones = 0
        self.numberForests = 0
        self.numberPonds = 0
        self.numberRivers = 0
        self.maxSteps = maxSteps
        self.currSteps = 0
        self.delayTime = 0.01

        #Loading in Images
        self.fishUpImage = PhotoImage(file='images/agents/fishUp.png')
        self.fishDownImage = PhotoImage(file='images/agents/fishDown.png')
        self.fishRightImage = PhotoImage(file='images/agents/fishRight.png')
        self.fishLeftImage = PhotoImage(file='images/agents/fishLeft.png')
        self.ghostImage = PhotoImage(file='images/agents/ghost48x48.png')

        self.turnipImage = PhotoImage(file='images/items/turnip48x48.png')
        self.stoneImage = PhotoImage(file='images/items/stone.png')
        self.mushroomImage = PhotoImage(file='images/items/mushroom.png')
        self.treeImage = PhotoImage(file='images/items/tree.png')
        self.treeFruitImage = PhotoImage(file='images/items/tree_fruit.png')
        self.waveImage = PhotoImage(file='images/items/wave.png')
        self.pitImage = PhotoImage(file='images/items/pit.png')
        self.grassImage = PhotoImage(file='images/items/grass.png')
        self.sandImage = PhotoImage(file='images/items/sand.png')
        self.snowImage = PhotoImage(file='images/items/snow.png')
        self.appleImage = PhotoImage(file='images/items/apple.png')
        self.boneImage = PhotoImage(file='images/items/bone.png')
        self.fireImage = PhotoImage(file='images/items/fire.png')
        self.shrubImage = PhotoImage(file='images/items/shrub.png')
        self.shrubFruitImage = PhotoImage(file='images/items/shrub_fruit.png')
        self.sporesImage = PhotoImage(file='images/items/spores.png')
        self.seedsImage = PhotoImage(file='images/items/seeds.png')

        randomGeneticStrings = []
        # randomGeneticStrings.append("21100249000010")
        # randomGeneticStrings.append("11000449000009")
        # randomGeneticStrings.append("11100449000005")
        # randomGeneticStrings.append("11100449000005")
        # randomGeneticStrings.append("11100449000005")
        #
        # randomGeneticStrings.append("12110199001")
        # randomGeneticStrings.append("12110399001")
        # for n in range(self.numberAgents - 1):
        #     randomGeneticStrings.append("11100599")

        """
        X000000000000000 - Vision [0]
        0X00000000000000 - Smell [1]
        00X0000000000000 - Movement [2]
        000X000000000000 - Aggression [3]
        0000X00000000000 - Sleep Type - Diurnal (0) or Nocturnal (1) [4]
        00000X0000000000 - Color [5]
        000000XX00000000 - Initial Energy [6:7]
        00000000X0000000 - Jump [8]
        000000000X000000 - Swim [9]
        0000000000X00000 - Fly [10]
        00000000000X0000 - Scavenge [11]
        000000000000X000 - Has a sickness [12]
        0000000000000X00 - Disease Resistance [13]
        """
        # for n in range(self.numberAgents):
        #     randomVision = str(random.randint(0, 5))
        #     randomSmell = str(random.randint(0, 2))
        #     randomMovement = str(random.randint(1, 1))
        #     randomAggression = str(random.randint(0, 1))
        #     randomSleepType = str(random.randint(0, 1))
        #     randomColor = str(random.randint(1, 9))
        #     randomEnergy = "99"
        #     randomGeneticString = randomVision + randomSmell + randomMovement + randomAggression + randomSleepType + randomColor + randomEnergy
        #     randomGeneticStrings.append(randomGeneticString)
        #     print(randomGeneticString)

        randomGeneticStrings = self.generateRandomGeneticStrings()

        print("--------------------------------------------------------------------------------------------")
        print("The random genetic strings to be assigned to agents: " + str(randomGeneticStrings))
        print("--------------------------------------------------------------------------------------------")
        self.sim = ALifeSim.ALifeSimTest(self.gridDim, self.numberAgents, self.numberStones, self.numberForests, self.numberRivers, self.numberPonds, randomGeneticStrings)

        # Variables to hold the results of a simulation
        self.minTime = None
        self.maxTime = None
        self.avgTime = None
        self.agentsLiving = 0

    def generateRandomGeneticStrings(self):
        """Returns a list of genetic strings to assign to agents, using the user's input strings as the first ones."""
        #TODO: what if user types an invalid string?
        randomGeneticStrings = []
        try:
            g1number = self.g1num.get()
            if len(g1number) == 14 and g1number.isdecimal():
                firstString = str(g1number)
                randomGeneticStrings.append(firstString)
                # print("1stgeneticstring", firstString)
            else:
                print("Choosing randomly for genetic string #1")
        except:
            print("Choosing randomly for genetic string #1")
        try:
            g2number = self.g2num.get()
            if len(g2number) == 14 and g2number.isdecimal():
                secondString = str(g2number)
                randomGeneticStrings.append(secondString)
                # print("2ndgeneticstring", secondString)
            else:
                print("Choosing randomly for genetic string #2")
        except:
            print("Choosing randomly for genetic string #2")

        #IF user inputs x, choose randomly
        #TODO: what if user inputs something else that is not 12 digits?
        # if len(randomGeneticStrings) == 2:
        #     if randomGeneticStrings[0] == "x" and randomGeneticStrings[1] == "x":
        #         print("choosing all genetic strings randomly")
        #         randomGeneticStrings = []

        for n in range(self.numberAgents - len(randomGeneticStrings)):
            randomVision = str(random.randint(1, 2))
            randomSmell = str(random.randint(0, 2))
            randomMovement = str(random.randint(1, 1))
            randomAggression = str(random.randint(0, 1))
            randomSleepType = str(random.randint(0, 1))
            randomColor = str(random.randint(1, 9))
            randomEnergy = str(random.randint(10, 60))
            randomJump = str(random.choice([0, 0, 0, 1]))
            randomSwim = str(random.choice([0, 0, 0, 1]))
            randomFly = str(random.choice([0, 0, 0, 1]))
            randomScavenge = str(random.choice([0, 0, 0, 1]))
            randomSickness = str(random.choice([0, 0, 0, 0, 0, 1]))
            randomResistance = str(random.randint(0, 9))

            randomGeneticString = randomVision + \
                                  randomSmell + \
                                  randomMovement + \
                                  randomAggression + \
                                  randomSleepType + \
                                  randomColor + \
                                  randomEnergy + \
                                  randomJump + \
                                  randomSwim + \
                                  randomFly + \
                                  randomScavenge + \
                                  randomSickness + \
                                  randomResistance
            randomGeneticStrings.append(randomGeneticString)
            print("randomGeneticString: ", randomGeneticString)
        return randomGeneticStrings

    def setupWidgets(self):
        """Set up all the parts of the GUI."""
        # Create title frame and main buttons
        self._initTitle()

        # Create control buttons
        self._initGridBuildingTools()

        # Creates a box for time info
        self._makeTimeBox()

        # Create the search frame
        self._initSimTools()

        # Create the message frame
        self._initMessage()

        # Create the search alg frame
        self._initSearchTools()

        # Create the simulation grid
        self._initGrid()

    def goProgram(self):
        """This starts the whole GUI going"""
        self.root.mainloop()

    # =================================================================
    # Widget-creating helper functions

    def _initTitle(self):
        """Sets up the title section of the GUI, where the Quit and Help buttons are located."""
        titleButtonFrame = Frame(self.root, bd=5, padx=5, pady=5)
        titleButtonFrame.grid(row=1, column=1)
        quitButton = Button(titleButtonFrame, text="Quit", command=self.quit, height=2)
        quitButton.grid(row=1, column=1, padx=5)

        titleFrame =  Frame(self.root, bd=5, padx=5, pady=5)
        titleFrame.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        titleLabel = Label(titleFrame, text="Jonathan and Henry's ALife Simulation", font="Arial 20 bold",
                           anchor=CENTER, padx=5, pady=5)
        titleLabel.grid(row=1, column=1)

    def _initMessage(self):
        """Sets up the section of the window where messages appear, errors, failures, and numbers
        about how much work was done."""
        messageFrame1 = Frame(self.root, bd=5, padx=1, pady=1, height=2, relief="groove")
        messageFrame1.grid(row=2, column=2,  padx=5, pady=1)

        # resultsBoxTitle = Label(messageFrame1, text="Simulation Results", font="Arial 16 bold",
        #                    anchor=CENTER, padx=5, pady=5, wraplength=300, height = 2)
        # resultsBoxTitle.grid(row=1,column=1)

        # messageCanvas = Canvas(messageFrame1)
        # messageCanvas.grid(row=2, column=1, sticky=NS)
        #
        # # myscrollbar = Scrollbar(messageFrame1, orient="vertical", command=messageCanvas.yview)
        # # myscrollbar.grid(row=2, column=2, sticky=NS)
        # # messageCanvas.configure(yscrollcommand=myscrollbar.set)
        #
        # messageTextFrame = Frame(messageCanvas)
        # # messageTextFrame.config(yscrollcommand=myscrollbar.set)
        # # messageTextFrame.grid(row=1,column=1)
        # # messageTextFrame['yscrollcommand'] = myscrollbar.set
        #
        # messageCanvas.create_window((0, 0), window=messageTextFrame, anchor='nw')
        # messageTextFrame.bind("<Configure>", messageCanvas.configure(scrollregion=messageCanvas.bbox("all")))
        #
        # textWidget = Text(messageTextFrame)
        # vsb = Scrollbar(messageTextFrame, orient="vertical", command=textWidget.yview)
        # # vsb.config(command=textWidget.yview)
        # textWidget.config(yscrollcommand=vsb.set)
        # textWidget.grid(row=0, column=1)
        # vsb.grid(row=0, column=0, sticky=NS)
        #
        # self.messageVar = StringVar()
        # # self.messageVar.set("")
        # self.messageVar.set("1 \n2 \n3 \n4 \n5 \n6 \n7 \n8 \n9 \n10 \n11 \n12 \n13 \n14 \n15 \n16 \n17 \n18 \n19 \n20 \n21 \n22")
        # message = Label(textWidget, textvariable=self.messageVar, width=30, height=14, wraplength = 300)
        # message.grid(row=1, column=1)

        canvas1 = Canvas(messageFrame1)
        scroll1 = Scrollbar(messageFrame1, orient='vertical', command=canvas1.yview)
        canvas1.configure(yscrollcommand=scroll1.set)
        frame1 = Frame(
            canvas1)  # frame does not get pack() as it needs to be embedded into canvas throught canvas.
        scroll1.pack(side='right', fill='y')
        canvas1.pack(fill='both', expand='yes')
        canvas1.create_window((0, 0), window=frame1, anchor='nw')
        frame1.bind('<Configure>',
                        lambda x: canvas1.configure(scrollregion=canvas1.bbox('all')))  # lambda function

        # 1st Text Widget
        journal1 = Text(frame1)
        vsb1 = Scrollbar(frame1)
        vsb1.config(command=journal1.yview)
        journal1.config(yscrollcommand=vsb1.set)
        journal1.grid(row=0, column=0)  # grid instead
        vsb1.grid(row=0, column=1, sticky='ns')  # grid instead

    def _initGridBuildingTools(self):
        """Sets up the tools for modifying the grid and the number of agents."""
        gridSetupFrame = Frame(self.root, bd=5, padx=5, pady=5, relief="groove", width=500)
        gridSetupFrame.grid(row=3, column=1, padx=5, pady=5, sticky=NW)
        editTitle = Label(gridSetupFrame, text="Grid Config", font="Arial 16 bold", anchor=CENTER, height=2)
        editTitle.grid(row=0, column=1, padx=5, pady=5)

        # Make a new subframe
        makerFrame = Frame(gridSetupFrame, bd=2, relief="groove", padx=5, pady=5)
        makerFrame.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        makerFrame2 = Frame(gridSetupFrame, bd=2, relief="groove", padx=5, pady=5)
        makerFrame2.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        makerFrame3 = Frame(gridSetupFrame, bd=0, relief="groove", padx=5, pady=5)
        makerFrame3.grid(row=3, column=1, padx=5, pady=5, sticky=W)

        sizeLabel1 = Label(makerFrame, text="Grid Dimension")
        # sizeLabel2 = Label(makerFrame, text="x") #TODO: Reimplement this
        self.rowDimensionText = IntVar()
        self.rowDimensionText.set(str(self.gridDim))
        self.colDimensionText = IntVar()
        self.colDimensionText.set(str(self.gridDim))
        self.rowsEntry = Entry(makerFrame, textvariable=self.rowDimensionText, width=4, justify=CENTER)
        # self.colsEntry = Entry(makerFrame, textvariable=self.colDimensionText, width=4, justify=CENTER)
        agentsLabel = Label(makerFrame2, text="# of Agents")
        self.agentNum = IntVar()
        self.agentNum.set(self.numberAgents)
        self.numAgents = Entry(makerFrame2, textvariable=self.agentNum, width=4, justify=CENTER)

        geneticString1Label = Label(makerFrame2, text="Genetic String 1")
        self.g1num = StringVar()
        sampleString = ""
        #TODO: make this length of genetic string
        self.g1num.set("21100949000009")
        widthOfGeneticStringInput = len(self.g1num.get())-1
        self.numg1 = Entry(makerFrame2, textvariable=self.g1num, width=widthOfGeneticStringInput, justify=CENTER)

        geneticString2Label = Label(makerFrame2, text="Genetic String 2")
        self.g2num = StringVar()
        self.g2num.set("22100730001111")
        self.numg2 = Entry(makerFrame2, textvariable=self.g2num, width=widthOfGeneticStringInput, justify=CENTER)

        stonesLabel = Label(makerFrame, text="Stones")
        self.stonesNum = IntVar()
        self.stonesNum.set(self.numberStones)
        self.numStones = Entry(makerFrame, textvariable=self.stonesNum, width=4, justify=CENTER)

        forestsLabel = Label(makerFrame, text="Forests")
        self.forestsNum = IntVar()
        self.forestsNum.set(self.numberForests)
        self.numForests = Entry(makerFrame, textvariable=self.forestsNum, width=4, justify=CENTER)

        riversLabel = Label(makerFrame, text="Rivers")
        self.riversNum = IntVar()
        self.riversNum.set(self.numberRivers)
        self.numRivers = Entry(makerFrame, textvariable=self.riversNum, width=4, justify=CENTER)

        pondsLabel = Label(makerFrame, text="Ponds")
        self.pondsNum = IntVar()
        self.pondsNum.set(self.numberPonds)
        self.numPonds = Entry(makerFrame, textvariable=self.pondsNum, width=4, justify=CENTER)

        # self.gridButton = Button(gridSetupFrame, text="New Simulation", command=self.resetGridWorld)
        self.gridButton = Button(makerFrame3, text="Generate New Simulation", command=self.resetGridWorld, height=2)
        self.gridButton.grid(row=3, column=2, columnspan=2, pady=5)

        sizeLabel1.grid(row=1, column=1)
        # sizeLabel2.grid(row=1, column=2)
        agentsLabel.grid(row=2, column=2)
        geneticString1Label.grid(row=3,column=2)
        geneticString2Label.grid(row=4,column=2)

        stonesLabel.grid(row=2, column=1)
        forestsLabel.grid(row=3,column=1)
        riversLabel.grid(row=4, column=1)
        pondsLabel.grid(row=5,column=1)

        self.rowsEntry.grid(row=1, column=2)
        # self.colsEntry.grid(row=1, column=6)
        self.numAgents.grid(row=2, column=4)
        self.numg1.grid(row=3,column=4)
        self.numg2.grid(row=4,column=4)

        self.gridButton.grid(row=3, column=3, columnspan=1, pady=5)
        self.numStones.grid(row=2, column=2)
        self.numForests.grid(row=3,column=2)
        self.numRivers.grid(row=4,column=2)
        self.numPonds.grid(row=5,column=2)

    def _initGrid(self):
        """sets up the grid with current assigned dimensions, and number of agents
        done as a helper because it may need to be done over later."""
        self.canvas = None
        self.canvasSize = 500
        self.canvasPadding = 10
        canvasFrame = Frame(self.root, bd=5, padx=10, pady=10, relief="raise", bg="gray")
        canvasFrame.grid(row=3, column=2, rowspan=3, padx=5, pady=5)
        self.canvas = Canvas(canvasFrame,
                             width=self.canvasSize + self.canvasPadding,
                             height=self.canvasSize + self.canvasPadding)
        self.canvas.grid(row=1, column=1)

        self._buildTkinterGrid()

    def _initSimTools(self):
        """Sets up the search frame, with buttons for selecting which search, for starting a search,
        stepping or running it, running it 100 times, and quitting from it.
        You can also choose how many steps should happen for each click of the "step" button."""
        simFrame = Frame(self.root, bd=5, padx=10, pady=10, relief="groove")
        simFrame.grid(row=2, column=1, padx=5, pady=5, sticky=W)
        simTitle = Label(simFrame, text="Run Config", font="Arial 16 bold", height=2, anchor=CENTER)
        simTitle.grid(row=0, column=2, columnspan=1, padx=5, pady=1)

        # Sets the maximum
        stepsLabel = Label(simFrame, text="Max sim steps")
        self.maxStepsText = IntVar()
        self.maxStepsText.set(self.maxSteps)
        self.stepsEntry = Entry(simFrame, textvariable=self.maxStepsText, width=4, justify=CENTER)
        stepsLabel.grid(row=1, column=1, sticky=W)
        self.stepsEntry.grid(row=1, column=2)

        delayLabel = Label(simFrame, text="Step delay")
        self.delayText = StringVar()
        self.delayText.set("{0:4.2f}".format(self.delayTime))
        self.delayEntry = Entry(simFrame, textvariable=self.delayText, width=5, justify=CENTER)
        delayLabel.grid(row=2, column=1, sticky=W)
        self.delayEntry.grid(row=2, column=2)

        # gapLabel = Label(simFrame, text="", width=20, bg="light gray")
        # gapLabel.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

        self.currStepsText = IntVar()
        self.currStepsText.set(self.currSteps)
        currStepLabel = Label(simFrame, text="Current steps:")
        currSteps = Label(simFrame, textvariable=self.currStepsText, width=4, justify=CENTER, relief="raised")
        currStepLabel.grid(row=5, column=1, sticky=W)
        currSteps.grid(row=5, column=2)

        self.run100Button = Button(simFrame, text="Run 100x", command=self.run100Simulations, height=2)
        self.run100Button.grid(row=6, column=3, columnspan=1, pady=5)

        self.runButton = Button(simFrame, text="Run 1x", command=self.runSimulation, height = 2)
        self.runButton.grid(row=6, column=2, columnspan=1, pady=5)

        self.stepButton = Button(simFrame, text="Step", command=self.stepSimulation, height=2)
        self.stepButton.grid(row=6, column=1, columnspan=1, pady=5, sticky=E)

    def _initSearchTools(self):
        """Sets up the searcher for optimal string."""
        #TODO: Use this?
        self.searchType = StringVar()
        self.searchType.set("hillClimb")
        self.currentSearch = None
        self.currentSearcher = None
        self.currentNode = None

    def _makeTimeBox(self):
        """Sets up a box with an image to display the simulation's current time."""
        timeBoxFrame = Frame(self.root, bd=5, padx=10, pady=10, relief="groove")
        timeBoxFrame.grid(row=2, column=2, padx=5, pady=5, sticky=SE)
        timeBoxTitle = Label(timeBoxFrame, text="Time", font="Arial 16 bold")
        #TODO: replace "Time" with the current time as a number
        timeBoxTitle.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        #TODO: change where these images load - put them in the top w/ other images
        self.sunNoonImage=PhotoImage(file='images/time/sunNoon.png')
        self.sunOneImage = PhotoImage(file='images/time/sunOne.png')
        self.sunTwoImage = PhotoImage(file='images/time/sunTwo.png')
        self.sunThreeImage = PhotoImage(file='images/time/sunThree.png')
        self.sunFourImage = PhotoImage(file='images/time/sunFour.png')
        self.sunFiveImage = PhotoImage(file='images/time/sunFive.png')
        self.sunSixImage = PhotoImage(file='images/time/sunSix.png')

        self.moonSevenImage = PhotoImage(file='images/time/moonSeven.png')
        self.moonEightImage = PhotoImage(file='images/time/moonEight.png')
        self.moonNineImage = PhotoImage(file='images/time/moonNine.png')
        self.moonTenImage = PhotoImage(file='images/time/moonTen.png')
        self.moonElevenImage = PhotoImage(file='images/time/moonEleven.png')
        self.moonMidnightImage = PhotoImage(file='images/time/moonMidnight.png')
        self.moonOneImage = PhotoImage(file='images/time/moonOne.png')
        self.moonTwoImage = PhotoImage(file='images/time/moonTwo.png')
        self.moonThreeImage = PhotoImage(file='images/time/moonThree.png')
        self.moonFourImage = PhotoImage(file='images/time/moonFour.png')
        self.moonFiveImage = PhotoImage(file='images/time/moonFive.png')

        self.sunSixAMImage = PhotoImage(file='images/time/sunSixAM.png')
        self.sunSevenImage = PhotoImage(file='images/time/sunSeven.png')
        self.sunEightImage = PhotoImage(file='images/time/sunEight.png')
        self.sunNineImage = PhotoImage(file='images/time/sunNine.png')
        self.sunTenImage = PhotoImage(file='images/time/sunTen.png')
        self.sunElevenImage = PhotoImage(file='images/time/sunEleven.png')

        timeImages = [
            self.moonMidnightImage,
            self.moonOneImage,
            self.moonTwoImage,
            self.moonThreeImage,
            self.moonFourImage,
            self.moonFiveImage,

            self.sunSixAMImage,
            self.sunSevenImage,
            self.sunEightImage,
            self.sunNineImage,
            self.sunTenImage,
            self.sunElevenImage,
            self.sunNoonImage,
            self.sunOneImage,
            self.sunTwoImage,
            self.sunThreeImage,
            self.sunFourImage,
            self.sunFiveImage,
            self.sunSixImage,

            self.moonSevenImage,
            self.moonEightImage,
            self.moonNineImage,
            self.moonTenImage,
            self.moonElevenImage
        ]

        stepsLabel = tkinter.Label(timeBoxFrame, image=timeImages[self.sim.time-1])
        # stepsLabel = tkinter.Canvas(timeBoxFrame)
        # stepsLabel.create_image(0,0,image=self.ghostImage, anchor="nw")
        stepsLabel.grid(row=1, column=1)

    ### =================================================================
    ### The following are callbacks for buttons
    def quit(self):
        """Callback for the quit button: destroy everything"""
        self.root.destroy()

    # ----------------------------------------------------------------
    # Button callbacks for Edit buttons
    def resetGridWorld(self, ruleString=None):
        """This is both a callback for the New Grid button, but also called from other
        places where the ruleString is set to a non-None value"""
        self._removeGridItems()
        self.canvas.delete('all')

        rowSize = self.rowDimensionText.get()
        colSize = self.colDimensionText.get()
        size = self.rowDimensionText.get()
        ageNum = self.agentNum.get()
        stoneNum = self.stonesNum.get()
        # print(stoneNum)
        forestsNum = self.forestsNum.get()
        riversNum = self.riversNum.get()
        pondsNum = self.pondsNum.get()
        # print(forestsNum)
        try:
            self.gridDim = int(size)
            self.numberAgents = int(ageNum)
            self.numberStones = int(stoneNum)
            self.numberForests = int(forestsNum)
            self.numberRivers = int(riversNum)
            self.numberPonds = int(pondsNum)
        except:
            self._postMessage("Dimension must be positive integer.")
            return

        self.sim = ALifeSim.ALifeSimTest(self.gridDim, self.numberAgents, self.numberStones, self.numberForests, self.numberRivers, self.numberPonds, self.generateRandomGeneticStrings())
        self._buildTkinterGrid()
        self.currSteps = 0
        self.currStepsText.set(self.currSteps)
        self.currentSearch = None

    # ----------------------------------------------------------------
    # Button callbacks for Search buttons
    def resetSearch(self):
        """This is a callback for the Set Up Search button. It resets the simulation based on the current
        values, and sets up the algorithm to be called, it initializes the search.
        It disables the grid editing and turns off the edit mode, and turns on the search model."""
        self._clearMessage()

        self.resetGridWorld()
        self.currentNode = None
        self.currentSearch = self.searchType.get()
        print(self.currentSearch)
        self.currentSearcher = HillClimber(RulesetState(self.evalRulestring, self.maxSteps))

        self._disableChanges()
        self._enableSearch()

    def evalRulestring(self, ruleString):
        """Evaluates a given rule string by using it to create agents and running a simulation with those agents."""
        self.resetGridWorld(ruleString)
        self._postMessage("Testing rulestring: " + str(ruleString))
        self.runSimulation()
        return self.avgTime

    def runSearch(self):
        """This callback for the Run Search button keeps running steps of the search until the search is done
        or a problem crops up."""
        keepLooping = True
        while keepLooping:
            keepLooping = self._handleOneStep()

    def stepSearch(self):
        """This repeats the current stepCount number of steps of the search, stopping after that.
        Otherwise, this is very similar to the previous function."""
        keepLooping = self._handleOneStep()

    def _handleOneStep(self):
        """This helper helps both the run search and step search callbacks, by handling the
        different outcomes for one step of the search."""
        status = self.currentSearcher.step()
        count = self.currentSearcher.getCount()
        nextState = self.currentSearcher.getCurrState()
        nextValue = self.currentSearcher.getCurrValue()
        keepGoing = True
        if status == "local maxima":
            self._addMessage("Local maxima found after " + str(count) + " steps: " + str(nextState))
            #keepGoing = False
            self.root.update()
            time.sleep(0.5)
        elif status == "optimal":
            self._addMessage("Optimal solution found after " + str(count) + " steps: " + str(nextState))
            # self.wrapUpSearch(nextState, nextValue)
            #keepGoing = False
            self.root.update()
            time.sleep(0.5)
        else:
            self._addMessage("Search continuing after " + str(count) + " steps.")
            self.root.update()
            time.sleep(0.5)

        return keepGoing

    def wrapUpSearch(self, nextState, nextValue):
        """This produces the ending statistics, finds and marks the final path, and then closes
        down the search so it will not continue"""
        pass
        #
        # printStr = "Total path cost = %d      " % totalCost
        # printStr += "Path length = %d\n" % len(finalPath)
        # printStr += "Nodes created = %d      " % self.currentSearcher.getNodesCreated()
        # printStr += "Nodes visited = %d" % self.currentSearcher.getNodesVisited()
        # self._postMessage(printStr)
        # self.currentSearch = None
        # self.currentNode = None
        #

    def quitSearch(self):
        """A callback for clearing away the search and returning to edit mode."""
        self._disableSearch()
        self._enableChanges()
        self.currentSearch = None
        self.currentNode = None
        self._clearMessage()

    ### =================================================================
    ### Helper functions for running simulation
    def runSimulation(self):
        """Runs the simulation until either all agents die or we reach the max number of steps."""
        self.maxSteps=int(self.maxStepsText.get())
        self.delayTime = float(self.delayText.get())
        while self.currSteps <= self.maxSteps:
            result = self.stepSimulation()
            self.root.update()
            time.sleep(self.delayTime)
            if not result:
                break
        self.reportSimResult()
        self.root.update()
        time.sleep(.5)

    def run100Simulations(self):
        """Runs the simulation 100 times (for testing purposes)."""
        #TODO: How to report 100 sim results?
        for i in range(100):
            self.maxSteps=int(self.maxStepsText.get())
            self.delayTime = float(self.delayText.get())
            while self.currSteps <= self.maxSteps:
                result = self.stepSimulation()
                self.root.update()
                time.sleep(self.delayTime)
                if not result:
                    break
            # self.reportSimResult()
            self.root.update()
            time.sleep(.5)
            if (i==100):
                break
            else:
                self.resetGridWorld()

    def stepSimulation(self):
        """Runs one step of the simulation,
        then updates the GUI with new colors, object positions, and object states."""
        self.sim.step()
        self._makeTimeBox()
        for row in range(self.gridDim):
            for col in range(self.gridDim):
        #         food = self.sim.foodAt(row, col)
        #
        #         if food == 1:
        #             (x1, y1, x2, y2) = self._posToCoords(row, col)
        #             turnipImage = self.canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=self.TurnipImage)
        #             self.canvas.lift(turnipImage)
                cellColor = self._determinePatchColor()
                patchId = self.posToPatchId[row, col]
                self.canvas.itemconfig(patchId, fill=cellColor, outline=cellColor)

        # for object in self.sim.getObjects():
        #     #TODO: Double-check this code to place objects in the GUI / is it necessary (since objects don't move)
        #     obColor = object.colorNumberToText(object.getColor())
        #     if object.getVisId() is None:
        #         offsetCoords = self._determineObjectCoords(object)
        #         coords = [(0 + x, 0 + y) for (x, y) in offsetCoords]
        #         # print(coords)
        #         # print(obColor)
        #         obId = self.canvas.create_polygon(coords, fill=obColor, width=2)
        #         self.agentIdToPose[obId] = object.getPose()
        #         object.setVisId(obId)
        #
        #     id = object.getVisId()
        #     self.canvas.itemconfig(id, fill=obColor)
        #
        #     (newRow, newCol) = object.getPose()
        #     (x1, y1, x2, y2) = self._posToCoords(newRow, newCol)
        #     offsetCoords = self._determineObjectCoords(object)
        #     coords = [(x1 + x, y1 + y) for (x, y) in offsetCoords]
        #     flatCoords = [n for subl in coords for n in subl]
        #     self.canvas.coords(id, flatCoords)
        #     self.canvas.lift(id)
        #
        #     self.agentIdToPose[id] = object.getPose()
        # (x1, y1, x2, y2) = self._posToCoords(treeRow, treeCol)
        for tr in self.sim.getTrees():
            (newRow, newCol) = tr.getPose()
            # print("New coords:",newRow,newCol)
            (x1, y1, x2, y2) = self._posToCoords(newRow, newCol)

            # print("TREE IN GUI")
            if tr.getVisId() is None:
                if tr.getHasFood() == "-1":
                    # print("NO FOOD")
                    trId = self.canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=self.seedsImage)
                    self.agentIdToPose[trId] = tr.getPose()
                    tr.setVisId(trId)
                    self.canvas.lift(trId)
                    tr.setJustChangedBloom(False)
                elif tr.getHasFood() == "0":
                    # print("NO FOOD")
                    trId = self.canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=self.treeImage)
                    self.agentIdToPose[trId] = tr.getPose()
                    tr.setVisId(trId)
                    self.canvas.lift(trId)
                    tr.setJustChangedBloom(False)
                elif tr.getHasFood() == "1":
                    # print("FOOD")
                    trId = self.canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=self.treeFruitImage)
                    self.agentIdToPose[trId] = tr.getPose()
                    tr.setVisId(trId)
                    self.canvas.lift(trId)
                    tr.setJustChangedBloom(False)

            # finds tree tkinter object id
            id = tr.getVisId()
            # print(id)

            # self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill=agColor, width=2)
            # self.canvas.create_image(x1, y1, image=self.ghostImage)
            # ghostGuy = self.canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=self.ghostImage)
            # tr.setVisId(ghostGuy)
            # self.canvas.lift(ghostGuy)
            if tr.getHasFood() == '-1' and tr.justChanged == True:
                # deletes the object
                self.canvas.delete(id)
                trId = self.canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=self.seedsImage)
                self.agentIdToPose[trId] = tr.getPose()
                tr.setVisId(trId)
                self.canvas.lift(trId)
                tr.setJustChangedBloom(False)
            elif tr.getHasFood() == '0' and tr.justChanged == True:
                # deletes the object
                self.canvas.delete(id)
                trId = self.canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=self.treeImage)
                self.agentIdToPose[trId] = tr.getPose()
                tr.setVisId(trId)
                self.canvas.lift(trId)
                tr.setJustChangedBloom(False)
            elif tr.getHasFood() == '1' and tr.justChanged == True:
                # deletes the object
                self.canvas.delete(id)
                trId = self.canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=self.treeFruitImage)
                self.agentIdToPose[trId] = tr.getPose()
                tr.setVisId(trId)
                self.canvas.lift(trId)
                tr.setJustChangedBloom(False)

        for mu in self.sim.getMushrooms():
            (newRow, newCol) = mu.getPose()
            # print("New coords:",newRow,newCol)
            (x1, y1, x2, y2) = self._posToCoords(newRow, newCol)

            if mu.getVisId() is None:
                if mu.getDroppingType() == 0:
                    muId = self.canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=self.sporesImage)
                    self.agentIdToPose[muId] = mu.getPose()
                    mu.setVisId(muId)
                    self.canvas.lift(muId)
                    mu.setJustChanged(False)
                elif mu.getDroppingType() == 1:
                    muId = self.canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=self.mushroomImage)
                    self.agentIdToPose[muId] = mu.getPose()
                    mu.setVisId(muId)
                    self.canvas.lift(muId)
                    mu.setJustChanged(False)

            # finds tree tkinter object id
            id = mu.getVisId()
            print(id)

            # self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill=agColor, width=2)
            # self.canvas.create_image(x1, y1, image=self.ghostImage)
            # ghostGuy = self.canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=self.ghostImage)
            # tr.setVisId(ghostGuy)
            # self.canvas.lift(ghostGuy)

            if mu.getDroppingType() == 0 and mu.justChanged == True:
                # deletes the object
                self.canvas.delete(id)
                muId = self.canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=self.sporesImage)
                self.agentIdToPose[muId] = mu.getPose()
                mu.setVisId(muId)
                self.canvas.lift(muId)
                mu.setJustChanged(False)
            elif mu.getDroppingType() == 1 and mu.justChanged == True:
                # deletes the object
                self.canvas.delete(id)
                muId = self.canvas.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=self.mushroomImage)
                self.agentIdToPose[muId] = mu.getPose()
                mu.setVisId(muId)
                self.canvas.lift(muId)
                mu.setJustChanged(False)

        for agent in self.sim.getAgents():
            # agColor = self._determineAgentColor(agent.getEnergy())
            agColor = self._UpdateAgentColor(agent.getColor(), agent.getEnergy())
            newColor = self.tintColor(agent)

            if agent.isSick:
                agOutlineType = (3, 5)
            else:
                agOutlineType = (1, 1)

            if agent.getVisId() is None:
                offsetCoords = self._determineAgentCoords(agent)

                if agent.getAggression() == 1:
                    agentOutlineColor = "red"
                else:
                    agentOutlineColor = "blue"

                coords = [(x1 + x, y1 + y) for (x, y) in offsetCoords]
                if self.sim.gridSize >= 10:
                    agId = self.canvas.create_polygon(coords, outline=agentOutlineColor, dash=agOutlineType, fill=newColor, width=(20/self.sim.gridSize))
                else:
                    agId = self.canvas.create_polygon(coords, outline=agentOutlineColor, dash=agOutlineType, fill=newColor,width=(2))
                self.agentIdToPose[agId] = agent.getPose()
                agent.setVisId(agId)

                # print("BABY ID: " + str(agent.getVisId()))

            id = agent.getVisId()
            self.canvas.itemconfig(id, fill=newColor, dash=agOutlineType)

            # (oldRow, oldCol, oldHead) = self.agentIdToPose[id]
            (newRow, newCol, newHead) = agent.getPose()
            (x1, y1, x2, y2) = self._posToCoords(newRow, newCol)
            offsetCoords = self._determineAgentCoords(agent)
            coords = [(x1 + x, y1 + y) for (x, y) in offsetCoords]
            flatCoords = [n for subl in coords for n in subl]
            self.canvas.coords(id, flatCoords)
            self.canvas.lift(id)

            self.agentIdToPose[id] = agent.getPose()

        for eatenFood in self.sim.getEatenFood():
            # finds eaten food tkinter object id
            id = eatenFood[0].getVisId()
            self.canvas.delete(id)

            # (newRow, newCol) = eatenFood[0].getPose()
            # (x1, y1, x2, y2) = self._posToCoords(newRow, newCol)

            # self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill=agColor, width=2)
            # self.canvas.create_image(x1, y1, image=self.ghostImage)
            # ghostGuy = self.canvas.create_image((x1 + x2)/2, (y1 + y2) / 2, image=self.ghostImage)
            # self.canvas.lift(ghostGuy)

        for eatenMushrooms in self.sim.getEatenMushrooms():
            # finds eaten mushroom tkinter object id
            id = eatenMushrooms[0].getVisId()
            self.canvas.delete(id)

        for deadAgent in self.sim.getDeadAgents():
            #TODO: make this fade out over time

            # finds dead agent tkinter object id
            id = deadAgent[0].getVisId()

            # deletes the object
            self.canvas.delete(id)

            (newRow, newCol, newHead) = deadAgent[0].getPose()
            (x1, y1, x2, y2) = self._posToCoords(newRow, newCol)

            # self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill=agColor, width=2)
            # self.canvas.create_image(x1, y1, image=self.ghostImage)
            # ghostGuy = self.canvas.create_image((x1 + x2)/2, (y1 + y2) / 2, image=self.ghostImage)
            # deadAgent[0].setVisId(ghostGuy)
            # self.canvas.lift(ghostGuy)


        if len(self.sim.getAgents()) == 0:
            return False

        self.currSteps += 1
        self.currStepsText.set(self.currSteps)
        return True

    def reportSimResult(self):
        """Reports statistics on how the simulation came out."""
        #TODO: All this function does is call assessFinalResult, so do we still need this function?

        # total = 0
        # count = 0
        # self.minTime = 10 * self.maxSteps
        # self.maxTime = 0
        # deadAgents = self.sim.getDeadAgents()
        # self.agentsLiving = self.sim.getAgents()
        # numLiving = len(self.agentsLiving)
        # for agent, when in deadAgents:
        #     if when < self.minTime:
        #         self.minTime = when
        #     if when > self.maxTime:
        #         self.maxTime = when
        #     total += when
        #     count += 1
        # self.avgTime = (total + numLiving*self.maxSteps) / self.numberAgents
        # if numLiving > 0:
        #     maxTime = self.maxSteps
        # message1Template = "Survival time in steps: Average = {0:5.2f}     Minimum = {1:3d}     Maximum = {2:3d}"
        # message1 = message1Template.format(round(self.avgTime, 2), self.minTime, self.maxTime)
        # message2Template = "Number living = {0:5d}"
        # message2 = message2Template.format(numLiving)
        # message2 = str(self.sim.getDeadAgents())
        # self._addMessage(message1 + '\n' + message2)

        # self._addMessage("DEAD AGENTS")
        # self._addMessage("Genetic String      Lifespan")
        #
        # for i in range(len(self.sim.getDeadAgents())):
        #     deadAgent,timeLived = self.sim.getDeadAgents()[i]
        #     self._addMessage("  " + str(deadAgent.getGeneticString()) + "           " + str(timeLived))

        self.assessFinalResult()


    def assessFinalResult(self):
        """Reports statistics on how the simulation came out."""

        """
        X000000000000000 - Vision [0]
        0X00000000000000 - Smell [1]
        00X0000000000000 - Movement [2]
        000X000000000000 - Aggression [3]
        0000X00000000000 - Sleep Type - Diurnal (0) or Nocturnal (1) [4]
        00000X0000000000 - Color [5]
        000000XX00000000 - Initial Energy [6:7]
        00000000X0000000 - Jump [8]
        000000000X000000 - Swim [9]
        0000000000X00000 - Fly [10]
        00000000000X0000 - Scavenge [11]
        000000000000X000 - Has a sickness [12]
        0000000000000X00 - Disease Resistance [13]
        """

        deadAgents = self.sim.getDeadAgents()
        liveAgents = self.sim.getAgents()
        deadAgentGenetricStrings = []
        ListOfVisions = []
        ListOfSmell = []
        ListOfMovement = []
        ListOfAggression = []
        ListOfSleepType = []
        ListOfColor = []
        ListOfInitialEnergy = []
        ListOfJump = []
        ListOfSwim = []
        ListOfFly = []
        ListOfScavenge = []
        ListOfSickness = []
        ListOfResistance = []




        for i in range(len(deadAgents)):
            deadAgent, timeLived = self.sim.getDeadAgents()[i]
            deadAgentGenetricStrings.append(deadAgent.getGeneticString())

        # print(deadAgentGenetricStrings)

        for j in range(len(deadAgentGenetricStrings)):
            ListOfVisions.append(int(deadAgentGenetricStrings[j][0]))
            ListOfSmell.append(int(deadAgentGenetricStrings[j][1]))
            ListOfMovement.append(int(deadAgentGenetricStrings[j][2]))
            ListOfAggression.append(int(deadAgentGenetricStrings[j][3]))
            ListOfSleepType.append(int(deadAgentGenetricStrings[j][4]))
            ListOfColor.append(int(deadAgentGenetricStrings[j][5]))
            ListOfInitialEnergy.append(int(deadAgentGenetricStrings[j][6:7]))
            ListOfJump.append(int(deadAgentGenetricStrings[j][8]))
            ListOfSwim.append(int(deadAgentGenetricStrings[j][9]))
            ListOfFly.append(int(deadAgentGenetricStrings[j][10]))
            ListOfScavenge.append(int(deadAgentGenetricStrings[j][11]))
            ListOfSickness.append(int(deadAgentGenetricStrings[j][12]))
            ListOfResistance.append(int(deadAgentGenetricStrings[j][13]))

        print("ListOfVisions: ", ListOfVisions)
        print("ListOfSmell: ", ListOfSmell)
        print("ListOfMovement: ", ListOfMovement)
        print("ListOfAggression: ", ListOfAggression)
        print("ListOfSleepType: ", ListOfSleepType)
        print("ListOfColor: ", ListOfColor)
        print("ListOfJump: ", ListOfJump)
        print("ListOfSwim: ", ListOfSwim)
        print("ListOfFly: ", ListOfFly)
        print("ListOfScavenge: ", ListOfScavenge)
        print("ListOfSickness: ", ListOfSickness)
        print("ListOfResistance: ", ListOfResistance)

        WorstVisionTrait = self.most_common(ListOfVisions)
        WorstSmellTrait = self.most_common(ListOfSmell)
        WorstMovementTrait = self.most_common(ListOfMovement)
        WorstAggressionTrait = self.most_common(ListOfAggression)
        WorstSleepTrait = self.most_common(ListOfSleepType)
        WorstColorTrait = self.most_common(ListOfColor)
        WorstJumpTrait = self.most_common(ListOfJump)
        WorstSwimTrait = self.most_common(ListOfSwim)
        WorstFlyTrait = self.most_common(ListOfFly)
        WorstScavengeTrait = self.most_common(ListOfScavenge)
        WorstSicknessTrait = self.most_common(ListOfSickness)
        WorstResistanceTrait = self.most_common(ListOfResistance)

        self._clearMessage()

        self._addMessage("Worst Vision Trait: " + str(WorstVisionTrait))
        self._addMessage("Worst Smell Trait: " + str(WorstSmellTrait))
        self._addMessage("Worst Movement Trait: " + str(WorstMovementTrait))
        self._addMessage("Worst Aggression Trait: " + str(WorstAggressionTrait))
        self._addMessage("Worst Sleep Trait: " + str(WorstSleepTrait))
        self._addMessage("Worst Color Trait: " + str(WorstColorTrait))
        self._addMessage("Worst Jump Trait: " + str(WorstJumpTrait))
        self._addMessage("Worst Swim Trait: " + str(WorstSwimTrait))
        self._addMessage("Worst Fly Trait: " + str(WorstFlyTrait))
        self._addMessage("Worst Scavenge Trait: " + str(WorstScavengeTrait))
        self._addMessage("Worst Sickness Trait: " + str(WorstSicknessTrait))
        self._addMessage("Worst Resistance Trait: " + str(WorstResistanceTrait))
        self._addMessage("Worst Resistance Trait: " + str(WorstResistanceTrait))
        self._addMessage("Worst Resistance Trait: " + str(WorstResistanceTrait))
        self._addMessage("Worst Resistance Trait: " + str(WorstResistanceTrait))
        self._addMessage("Worst Resistance Trait: " + str(WorstResistanceTrait))
        self._addMessage("Worst Resistance Trait: " + str(WorstResistanceTrait))
        self._addMessage("Worst Resistance Trait: " + str(WorstResistanceTrait))
        self._addMessage("Worst Resistance Trait: " + str(WorstResistanceTrait))


    ### =================================================================
    ### Private helper functions
    def most_common(self, list):
        """Takes in a list and returns the value that appears most frequently."""
        if len(list) != 0:
            return max(set(list), key=list.count)
        else:
            return []

    def _buildTkinterGrid(self):
        """This sets up the display of the grid, based on the simulation object.
        Re-called when dimensions changed."""
        self.patchIdToPos = {}
        self.posToPatchId = {}
        self.agentIdToPose = {}

        self.resizeAllImages()

        if self.gridDim * 50 < self.canvasSize:
            self.cellSize = 50
        else:
            self.cellSize = self.canvasSize / self.gridDim

        for row in range(self.gridDim):
            for col in range(self.gridDim):
                (x1, y1, x2, y2) = self._posToCoords(row, col)
                cellColor = self._determinePatchColor()
                currId = self.canvas.create_rectangle(x1, y1, x2, y2, fill=cellColor, outline=cellColor)
                self.patchIdToPos[currId] = (row, col)
                self.posToPatchId[row, col] = currId
                agents = self.sim.agentsAt(row, col)
                stones = self.sim.stonesAt(row,col)
                waters = self.sim.waterAt(row,col)
                pits = self.sim.pitAt(row,col)
                trees = self.sim.treeAt(row,col)
                grasses = self.sim.grassAt(row,col)
                sands = self.sim.sandAt(row, col)
                snows = self.sim.snowAt(row, col)
                mushrooms = self.sim.mushroomAt(row,col)
                # apples = self.sim.appleAt(row, col)
                # fires = self.sim.fireAt(row, col)
                # bones = self.sim.boneAt(row, col)
                # shrubs = self.sim.shrubAt(row, col)

                # print(agents)
                # print(self.sim.foodAt(row,col))
                food = self.sim.foodAt(row,col)
                for fd in food:
                    self.canvas.update()
                    coords = [(x1 + x2)/2, (y1 + y2) / 2]
                    fdId = self.canvas.create_image(coords, image=self.turnipImage)
                    self.agentIdToPose[fdId] = fd.getPose()
                    fd.setVisId(fdId)
                for st in stones:
                    self.canvas.update()
                    # stColor = st.colorNumberToText(st.getColor())
                    # offsetCoords = self._determineObjectCoords(st)
                    # coords = [x1+offsetCoords[0], y1+offsetCoords[1], x2-offsetCoords[2], y2-offsetCoords[3]]
                    # stId = self.canvas.create_rectangle(coords, fill=stColor, width=2)
                    coords = [(x1 + x2) / 2, (y1 + y2) / 2]
                    stId = self.canvas.create_image(coords, image=self.stoneImage)
                    self.agentIdToPose[stId] = st.getPose()
                    st.setVisId(stId)
                for wt in waters:
                    self.canvas.update()
                    coords = [(x1 + x2) / 2, (y1 + y2) / 2]
                    wtId = self.canvas.create_image(coords, image=self.waveImage)
                    self.agentIdToPose[wtId] = wt.getPose()
                    wt.setVisId(wtId)
                for pt in pits:
                    self.canvas.update()
                    coords = [(x1 + x2) / 2, (y1 + y2) / 2]
                    ptId = self.canvas.create_image(coords, image=self.pitImage)
                    self.agentIdToPose[ptId] = pt.getPose()
                    pt.setVisId(ptId)

                for gr in grasses:
                    self.canvas.update()
                    coords = [(x1 + x2) / 2, (y1 + y2) / 2]
                    grId = self.canvas.create_image(coords, image=self.grassImage)
                    self.agentIdToPose[grId] = gr.getPose()
                    gr.setVisId(grId)

                for sa in sands:
                    self.canvas.update()
                    coords = [(x1 + x2) / 2, (y1 + y2) / 2]
                    saId = self.canvas.create_image(coords, image=self.sandImage)
                    self.agentIdToPose[saId] = sa.getPose()
                    sa.setVisId(saId)

                for sn in snows:
                    self.canvas.update()
                    coords = [(x1 + x2) / 2, (y1 + y2) / 2]
                    snId = self.canvas.create_image(coords, image=self.snowImage)
                    self.agentIdToPose[snId] = sn.getPose()
                    sn.setVisId(snId)

                for mu in mushrooms:
                    self.canvas.update()
                    coords = [(x1 + x2) / 2, (y1 + y2) / 2]
                    if mu.getDroppingType() == 0:
                        muId = self.canvas.create_image(coords, image=self.sporesImage)
                        self.agentIdToPose[muId] = mu.getPose()
                        mu.setVisId(muId)
                    elif mu.getDroppingType() == 1:
                        muId = self.canvas.create_image(coords, image=self.mushroomImage)
                        self.agentIdToPose[muId] = mu.getPose()
                        mu.setVisId(muId)

                # for ap in apples:
                #     self.canvas.update()
                #     coords = [(x1 + x2) / 2, (y1 + y2) / 2]
                #     apId = self.canvas.create_image(coords, image=self.appleImage)
                #     self.agentIdToPose[apId] = ap.getPose()
                #     ap.setVisId(apId)

                # for bn in bones:
                #     self.canvas.update()
                #     coords = [(x1 + x2) / 2, (y1 + y2) / 2]
                #     bnId = self.canvas.create_image(coords, image=self.boneImage)
                #     self.agentIdToPose[bnId] = bn.getPose()
                #     bn.setVisId(bnId)

                # for fi in fires:
                #     self.canvas.update()
                #     coords = [(x1 + x2) / 2, (y1 + y2) / 2]
                #     fiId = self.canvas.create_image(coords, image=self.fireImage)
                #     self.agentIdToPose[fiId] = fi.getPose()
                #     fi.setVisId(fiId)

                for tr in trees:
                    self.canvas.update()
                    coords = [(x1 + x2) / 2, (y1 + y2) / 2]
                    if tr.getHasFood() == '-1':
                        trId = self.canvas.create_image(coords, image=self.seedsImage)
                        self.agentIdToPose[trId] = tr.getPose()
                        tr.setVisId(trId)
                    elif tr.getHasFood() == '0':
                        trId = self.canvas.create_image(coords, image=self.treeImage)
                        self.agentIdToPose[trId] = tr.getPose()
                        tr.setVisId(trId)
                    elif tr.getHasFood() == '1':
                        trId = self.canvas.create_image(coords, image=self.treeFruitImage)
                        self.agentIdToPose[trId] = tr.getPose()
                        tr.setVisId(trId)

                # for sh in shrubs:
                #     self.canvas.update()
                #     coords = [(x1 + x2) / 2, (y1 + y2) / 2]
                #     if sh.getHasFood() == '0':
                #         shId = self.canvas.create_image(coords, image=self.shrubImage)
                #         self.agentIdToPose[shId] = sh.getPose()
                #         sh.setVisId(shId)
                #     elif sh.getHasFood() == '1':
                #         shId = self.canvas.create_image(coords, image=self.shrubFruitImage)
                #         self.agentIdToPose[shId] = sh.getPose()
                #         sh.setVisId(shId)

                for ag in agents:
                    self.canvas.update()
                    offsetCoords = self._determineAgentCoords(ag)
                    agColor = self._setAgentColor(ag.getColor())
                    if ag.getAggression() == 1:
                        agOutlineColor = "red"
                    else:
                        agOutlineColor = "blue"

                    if ag.isSick:
                        agOutlineType = (3,5)
                    else:
                        agOutlineType= (1,1)

                    coords = [(x1 + x, y1 + y) for (x, y) in offsetCoords]

                    # print(agColor)
                    newColor = self.tintColor(ag)
                    # print(newColor)

                    if self.sim.gridSize >= 10:
                        agId = self.canvas.create_polygon(coords, outline=agOutlineColor, dash=agOutlineType, fill=newColor, width=(20/self.sim.gridSize))
                    else:
                        agId = self.canvas.create_polygon(coords, outline=agOutlineColor, dash=agOutlineType, fill=newColor,width=(2))
                    self.agentIdToPose[agId] = ag.getPose()
                    ag.setVisId(agId)

                    #TODO: vvv Will be useful when changing agent sprites. Comment out code above, comment in code below

                    # self.canvas.update()
                    # coords = [(x1 + x2) / 2, (y1 + y2) / 2]
                    # self.agentIdToPose[agId] = ag.getPose()
                    # if ag.getPose()[2] == 'n':
                    #     agId = self.canvas.create_image(coords, image=self.fishUpImage)
                    # elif ag.getPose()[2] == 's':
                    #     agId = self.canvas.create_image(coords, image=self.fishDownImage)
                    # elif ag.getPose()[2] == 'e':
                    #     agId = self.canvas.create_image(coords, image=self.fishRightImage)
                    # elif ag.getPose()[2] == 'w':
                    #     agId = self.canvas.create_image(coords, image=self.fishLeftImage)
                    # ag.setVisId(agId)

    def _determineObjectCoords(self, object):
        """Gives offset coordinates based on the direction the object is
        pointing."""
        oneSixth = self.cellSize / 6
        fiveSixths = 5 * oneSixth
        half = self.cellSize / 2
        quarter = self.cellSize / 4
        threeQ = 3 * quarter
        return [oneSixth,oneSixth,oneSixth,oneSixth]

    def _determineAgentCoords(self, agent):
        """Gives offset coordinates based on the direction the agent is
        pointing."""
        (agr, agc, heading) = agent.getPose()
        oneSixth = self.cellSize / 6
        fiveSixths = 5 * oneSixth
        half = self.cellSize / 2
        quarter = self.cellSize / 4
        threeQ = 3 * quarter

        if heading == 'n':
            return [(half, oneSixth), (quarter, fiveSixths), (threeQ, fiveSixths)]
        elif heading == 'e':
            return [(fiveSixths, half), (oneSixth, quarter), (oneSixth, threeQ)]
        elif heading == 's':
            return [(half, fiveSixths), (threeQ, oneSixth), (quarter, oneSixth)]
        elif heading == 'w':
            return [(oneSixth, half), (fiveSixths, threeQ), (fiveSixths, quarter)]
        else:
            print("Bad heading for agent", heading)

    def _determinePatchColor(self):
        """Determines the color of the grid based on the simulation's time attribute."""
        oneAM = "#747474"
        twoAM = "#808080"
        threeAM = "#8c8c8c"
        fourAM = "#999999"
        fiveAM = "#a5a5a5"
        sixAM = "#b2b2b2"
        sevenAM = "#bfbfbf"
        eightAM = "#cccccc"
        nineAM = "#dadada"
        tenAM = "#e7e7e7"
        elevenAM = "#f5f5f5"
        noon = "#f5f5f5"
        onePM = "#e7e7e7"
        twoPM = "#dadada"
        threePM = "#cccccc"
        fourPM = "#bfbfbf"
        fivePM = "#b2b2b2"
        sixPM = "#a5a5a5"
        sevenPM = "#999999"
        eightPM = "#8c8c8c"
        ninePM = "#808080"
        tenPM = "#747474"
        elevenPM = "#686868"
        midnight = "#686868"

        timeColors = []
        timeColors.append(midnight)
        timeColors.append(oneAM)
        timeColors.append(twoAM)
        timeColors.append(threeAM)
        timeColors.append(fourAM)
        timeColors.append(fiveAM)
        timeColors.append(sixAM)
        timeColors.append(sevenAM)
        timeColors.append(eightAM)
        timeColors.append(nineAM)
        timeColors.append(tenAM)
        timeColors.append(elevenAM)
        timeColors.append(noon)
        timeColors.append(onePM)
        timeColors.append(twoPM)
        timeColors.append(threePM)
        timeColors.append(fourPM)
        timeColors.append(fivePM)
        timeColors.append(sixPM)
        timeColors.append(sevenPM)
        timeColors.append(eightPM)
        timeColors.append(ninePM)
        timeColors.append(tenPM)
        timeColors.append(elevenPM)

        cellColor = timeColors[self.sim.time-1]

        return cellColor

    def _determineAgentColor(self, energy):
        """Determines the color of an agent based on its energy."""
        #TODO: Can we delete this function?

        if energy <= 0:
            color = 'black'
        else:
            if energy > 60:
                energy = 60
            ratio = energy / 60
            redColor = int((ratio * 245) + 10)
            color = "#%02x%02x%02x" % (redColor, 0, 0)
        return color

    def _setAgentColor(self, color):
        """Sets an agent's color based on its numeric color attribute."""
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

    def tintColor(self, agent):
        # if agent.isSick:
        #     return 'white'
        # else:
        return agent.colorNumberToText(agent.getColor())

    def _UpdateAgentColor(self, color, energy):
        """Returns an agent's color based on its energy and color attribute."""
        # if energy <= 0:
        #     color = 'black'
        # else:
        color = self._setAgentColor(color)
        return color

    def _disableChanges(self):
        """Turn off access to the edit operations, by setting each of the GUI elements to DISABLED"""
        self.changesEnabled = False
        self.rowsEntry.config(state=DISABLED)
        self.numAgents.config(state=DISABLED)
        self.gridButton.config(state=DISABLED)

        self.stepsEntry.config(state=DISABLED)
        self.delayEntry.config(state=DISABLED)
        self.stepButton.config(state=DISABLED)
        self.runButton.config(state=DISABLED)

    def _enableChanges(self):
        """Turn on access to the edit operations, by setting each GUI element to NORMAL"""
        self.changesEnabled = True
        self.rowsEntry.config(state=NORMAL)
        self.numAgents.config(state=NORMAL)
        self.gridButton.config(state=NORMAL)

        self.stepsEntry.config(state=NORMAL)
        self.delayEntry.config(state=NORMAL)
        self.stepButton.config(state=NORMAL)
        self.runButton.config(state=NORMAL)

    def _disableSearch(self):
        """Turn off the search operations, by setting each GUI element to DISABLED."""
        self.stepSearch.config(state=DISABLED)
        self.runSearch.config(state=DISABLED)
        self.quitSearch.config(state=DISABLED)

    def _enableSearch(self):
        """Turn on the search operations, by setting each GUI element to NORMAL"""
        self.stepSearch.config(state=NORMAL)
        self.runSearch.config(state=NORMAL)
        self.quitSearch.config(state=NORMAL)

    def _removeGridItems(self):
        """A helper that removes all the grid cell objects from the simulation, prior to creating new
        ones when the simulation is reset."""
        for row in range(self.gridDim):
            for col in range(self.gridDim):
                currId = self.posToPatchId[row, col]
                self.canvas.delete(currId)
        for id in self.agentIdToPose:
            self.canvas.delete(id)
        self.canvas.update()
        self.posToPatchId = {}
        self.patchIdToPos = {}
        self.agentIdToPose = {}


    # -------------------------------------------------
    # Utility functions
    def _postMessage(self, messageText):
        """Posts a message in the message box"""
        self.messageVar.set(messageText)
        print("Message text:", messageText)

    def _clearMessage(self):
        """Clears the message in the message box"""
        self.messageVar.set("")
        print("Message cleared")

    def _addMessage(self, messageText):
        """Adds a message to the results frame. """
        oldMessage = self.messageVar.get()
        newMessage = oldMessage + '\n' + messageText
        self.messageVar.set(newMessage)
        # print("New Message", newMessage)

    def _setCellColor(self, cellId, color):
        """Sets the grid cell with cellId, and at row and column position, to have the
        right color.  Note that in addition to the visible color, there is also a colors 
        matrix that mirrors the displayed colors"""
        self.canvas.itemconfig(cellId, fill = color)

    def _setOutlineColor(self, cellId, color):
        """Sets the outline of the grid cell with cellID, and at row and column position, to
        have the right color."""
        self.canvas.itemconfig(cellId, outline=color)

    def resizeAllImages(self):
        """Scales all sprites based on the size of the grid. Uses original 48x48 sizes for any grid with size < 10."""
        if self.sim.gridSize > 10:
            newW = int(480/(self.sim.gridSize))
            newH = int(480 / (self.sim.gridSize))

            ghostImg = Image.open('images/agents/ghost48x48.png')
            ghostImg = ghostImg.resize((newW, newH))
            self.ghostImage = ImageTk.PhotoImage(ghostImg)

            turnipImg = Image.open('images/items/turnip48x48.png')
            turnipImg = turnipImg.resize((newW, newH))
            self.turnipImage = ImageTk.PhotoImage(turnipImg)

            stoneImg = Image.open('images/items/stone.png')
            stoneImg = stoneImg.resize((newW, newH))
            self.stoneImage = ImageTk.PhotoImage(stoneImg)

            mushroomImg = Image.open('images/items/mushroom.png')
            mushroomImg = mushroomImg.resize((newW, newH))
            self.mushroomImage = ImageTk.PhotoImage(mushroomImg)

            treeImg = Image.open('images/items/tree.png')
            treeImg = treeImg.resize((newW, newH))
            self.treeImage = ImageTk.PhotoImage(treeImg)

            treeFruitImg = Image.open('images/items/tree_fruit.png')
            treeFruitImg = treeFruitImg.resize((newW, newH))
            self.treeFruitImage = ImageTk.PhotoImage(treeFruitImg)

            waveImg = Image.open('images/items/wave.png')
            waveImg = waveImg.resize((newW, newH))
            self.waveImage = ImageTk.PhotoImage(waveImg)

            pitImg = Image.open('images/items/pit.png')
            pitImg = pitImg.resize((newW, newH))
            self.pitImage = ImageTk.PhotoImage(pitImg)

            sporesImg = Image.open('images/items/spores.png')
            sporesImg = sporesImg.resize((newW, newH))
            self.sporesImage = ImageTk.PhotoImage(sporesImg)

            seedsImg = Image.open('images/items/seeds.png')
            seedsImg = seedsImg.resize((newW, newH))
            self.seedsImage = ImageTk.PhotoImage(seedsImg)

            grassImg = Image.open('images/items/grass.png')
            grassImg = grassImg.resize((newW, newH))
            self.grassImage = ImageTk.PhotoImage(grassImg)

            sandImg = Image.open('images/items/sand.png')
            sandImg = sandImg.resize((newW, newH))
            self.sandImage = ImageTk.PhotoImage(sandImg)

            snowImg = Image.open('images/items/snow.png')
            snowImg = snowImg.resize((newW, newH))
            self.snowImage = ImageTk.PhotoImage(snowImg)

            fishUpImg = Image.open('images/agents/fishUp.png')
            fishUpImg = fishUpImg.resize((newW, newH))
            self.fishUpImage = ImageTk.PhotoImage(fishUpImg)

            fishDownImg = Image.open('images/agents/fishDown.png')
            fishDownImg = fishDownImg.resize((newW, newH))
            self.fishDownImage = ImageTk.PhotoImage(fishDownImg)

            fishRightImg = Image.open('images/agents/fishRight.png')
            fishRightImg = fishRightImg.resize((newW, newH))
            self.fishRightImage = ImageTk.PhotoImage(fishRightImg)

            fishLeftImg = Image.open('images/agents/fishLeft.png')
            fishLeftImg = fishLeftImg.resize((newW, newH))
            self.fishLeftImage = ImageTk.PhotoImage(fishLeftImg)

            appleImg = Image.open('images/items/apple.png')
            appleImg = appleImg.resize((newW, newH))
            self.appleImage = ImageTk.PhotoImage(appleImg)

            boneImg = Image.open('images/items/bone.png')
            boneImg = boneImg.resize((newW, newH))
            self.boneImage = ImageTk.PhotoImage(boneImg)

            fireImg = Image.open('images/items/fire.png')
            fireImg = fireImg.resize((newW, newH))
            self.fireImage = ImageTk.PhotoImage(fireImg)

            shrubImg = Image.open('images/items/shrub.png')
            shrubImg = shrubImg.resize((newW, newH))
            self.shrubImage = ImageTk.PhotoImage(shrubImg)

            shrubFruitImg = Image.open('images/items/shrub_fruit.png')
            shrubFruitImg = shrubFruitImg.resize((newW, newH))
            self.shrubFruitImage = ImageTk.PhotoImage(shrubFruitImg)

        else:
            ghostImg = Image.open('images/agents/ghost48x48.png')
            self.ghostImage = ImageTk.PhotoImage(ghostImg)

            turnipImg = Image.open('images/items/turnip48x48.png')
            self.turnipImage = ImageTk.PhotoImage(turnipImg)

            stoneImg = Image.open('images/items/stone.png')
            self.stoneImage = ImageTk.PhotoImage(stoneImg)

            mushroomImg = Image.open('images/items/mushroom.png')
            self.mushroomImage = ImageTk.PhotoImage(mushroomImg)

            treeImg = Image.open('images/items/tree.png')
            self.treeImage = ImageTk.PhotoImage(treeImg)

            treeFruitImg = Image.open('images/items/tree_fruit.png')
            self.treeFruitImage = ImageTk.PhotoImage(treeFruitImg)

            waveImg = Image.open('images/items/wave.png')
            self.waveImage = ImageTk.PhotoImage(waveImg)

            pitImg = Image.open('images/items/pit.png')
            self.pitImage = ImageTk.PhotoImage(pitImg)

            sporesImg = Image.open('images/items/spores.png')
            self.sporesImage = ImageTk.PhotoImage(sporesImg)

            seedsImg = Image.open('images/items/seeds.png')
            self.seedsImage = ImageTk.PhotoImage(seedsImg)

            grassImg = Image.open('images/items/grass.png')
            self.grassImage = ImageTk.PhotoImage(grassImg)

            sandImg = Image.open('images/items/sand.png')
            self.sandImage = ImageTk.PhotoImage(sandImg)

            snowImg = Image.open('images/items/snow.png')
            self.snowImage = ImageTk.PhotoImage(snowImg)

            fishUpImg = Image.open('images/agents/fishUp.png')
            self.fishUpImage = ImageTk.PhotoImage(fishUpImg)

            fishDownImg = Image.open('images/agents/fishDown.png')
            self.fishDownImage = ImageTk.PhotoImage(fishDownImg)

            fishRightImg = Image.open('images/agents/fishRight.png')
            self.fishRightImage = ImageTk.PhotoImage(fishRightImg)

            fishLeftImg = Image.open('images/agents/fishLeft.png')
            self.fishLeftImage = ImageTk.PhotoImage(fishLeftImg)

    def _posToId(self, row, col):
        """Given row and column indices, it looks up and returns the GUI id of the cell at that location"""
        return self.posToPatchId[row, col]

    def _idToPos(self, currId):
        """Given the id of a cell, it looks up and returns the row and column position of that cell"""
        return self.patchIdToPos[currId]

    def _posToCoords(self, row, col):
        """Given a row and column position, this converts that into a position on the frame"""
        x1 = col * self.cellSize + 5
        y1 = row * self.cellSize + 5
        # x2 = x1 + (self.cellSize - 2)
        # y2 = y1 + (self.cellSize - 2)
        x2 = x1 + (self.cellSize)
        y2 = y1 + (self.cellSize)
        return (x1, y1, x2, y2)

    def _coordToPos(self, x, y):
        """Given a position in the frame, this converts it to the corresponding row and column"""
        col = (x - 5) / self.cellSize
        row = (y - 5) / self.cellSize
        if row < 0:
            row = 0
        elif row >= self.gridDim:
            row = self.gridDim - 1

        if col < 0:
            col = 0
        elif col >= self.gridDim:
            col = self.gridDim - 1

        return int(row), int(col)

# The lines below cause the simulation to run when this file is double-clicked or sent to a launcher, or loaded
# into the interactive shell.
if __name__ == "__main__":
    numberOfAgents = 5
    s = ALifeGUI(5, numberOfAgents)
    s.setupWidgets()
    s.goProgram()
