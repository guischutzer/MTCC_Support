def mulliganValueIteration(self):

    for i in range(7, -1, -1):
        for j in range(i + 1):
            self.mulliganValue[7 - i][j] = self.getKeepReward(i, j)

    for epoch in range(0, 8):
        for i in range(7, -1, -1):
            for j in range(i + 1):
                mullValue = 0
                for jLine in range(i):
                    prob = self.getMulliganProb(i - 1, jLine)
                    value = self.mulliganValue[7 - (i - 1)][jLine]
                    mullValue += prob * value
                if mullValue >= self.getKeepReward(i, j):
                    self.mulliganValue[7 - i][j] = mullValue
