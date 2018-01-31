class MulliganAgent(Player):

    def __init__(self, ID, onThePlay, verbosity=False):
        self.name = 'Unknown Player'
        self.life = 20
        self.hand = []
        self.library = []
        self.lose = False
        self.ID = ID
        self.creatures = []
        self.lands = []
        self.active = False
        self.graveyard = []
        self.untappedLands = 0
        self.landRewards = []
        self.landDrop = False

        self.verbose = verbosity
        self.onThePlay = onThePlay

        if self.onThePlay:
            self.landRewards = [-7, -3, 3, 4, 2, -1, -4, -6]
        else:
            self.landRewards = [-4,  0, 5, 6, 3,  0, -3, -5]

        self.initMulliganTables()

    def initMulliganTables(self):
        ...
    def setLibrary(self, deck):
        ...
    def mulligan(self):
        ...
    def getHandReward(self, hand):
        ...
    def getKeepReward(self, i, j):
        ...
    def mulliganValueIteration(self):
        ...
    def getMulliganProb(self, i, j):
        ...
    def getMulliganValue(self, hand):
        ...
