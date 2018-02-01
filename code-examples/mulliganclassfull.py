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
        self.mulliganValue = [[None, None, None, None, None, None, None, None],
                               [None, None, None, None, None, None, None],
                               [None, None, None, None, None, None],
                               [None, None, None, None, None],
                               [None, None, None, None],
                               [None, None, None],
                               [None, None],
                               [None]]
        self.keepRewards =  [[None, None, None, None, None, None, None, None],
                              [None, None, None, None, None, None, None],
                              [None, None, None, None, None, None],
                              [None, None, None, None, None],
                              [None, None, None, None],
                              [None, None, None],
                              [None, None],
                             [None]]
        self.mulliganProb = [[None, None, None, None, None, None, None],
                             [None, None, None, None, None, None],
                             [None, None, None, None, None],
                             [None, None, None, None],
                             [None, None, None],
                             [None, None],
                             [None]]

    def setLibrary(self, deck):
        self.library = deck

        self.landsInLibrary = 0
        for card in self.library:
            if card.ctype is 'Land':
                self.landsInLibrary += 1

    def mulligan(self):

        if self.mulliganValue[0][0] is None:
            self.mulliganValueIteration()

        if self.verbose:
            print(self.mulliganValue)

        n = len(self.hand)
        if n == 0:
            return True

        keepReward = self.getHandReward(self.hand)
        mullValue = self.getMulliganValue(self.hand)

        if keepReward == mullValue:
            print("\nAgent " + self.name + " has kept this hand.")
            if n < 7:
                self.scry()
            if self.verbose:
                print(str(self.mulliganValue) + "\n")
                print(str(self.mulliganProb) + "\n")
                print(str(self.keepRewards))
            return True

        print("\nAgent " + self.name + " mulligans down to " + str(n - 1) + " cards.")

        while self.hand != []:
            self.library.append(self.hand.pop())

        self.shuffle()
        self.draw(n - 1)


        return False

    def getHandReward(self, hand):

        lands = 0

        for card in hand:
            if card.ctype is 'Land':
                lands += 1

        return self.getKeepReward(len(hand), lands)

    def getKeepReward(self, i, j):

        alpha = 3.5

        if self.keepRewards[7 - i][j] is not None:
            return self.keepRewards[7 - i][j]

        reward = self.landRewards[j] + alpha*i
        self.keepRewards[7 - i][j] = reward

        return reward

    def mulliganValueIteration(self):

        for i in range(7, -1, -1):
            for j in range(i + 1):
                self.mulliganValue[7 - i][j] = self.getKeepReward(i, j)

        for i in range(1, 8):
            mullSum = 0
            for jLine in range(i):
                prob = self.getMulliganProb(i - 1, jLine)
                value = self.mulliganValue[7 - (i - 1)][jLine]
                mullSum += prob * value

            for j in range(i + 1):
                if mullSum >= self.getKeepReward(i, j):
                    self.mulliganValue[7 - i][j] = mullSum

    def getMulliganProb(self, i, j):

        if self.mulliganProb[6 - i][j] is not None:
            return self.mulliganProb[6 - i][j]

        prob = utils.binom(self.landsInLibrary, j)*utils.binom(60 - self.landsInLibrary, i - j)/utils.binom(60, i)
        self.mulliganProb[6 - i][j] = prob

        return prob

    def getMulliganValue(self, hand):

        lands = 0

        for card in hand:
            if card.ctype is 'Land':
                lands += 1

        return self.mulliganValue[7 - len(hand)][lands]
