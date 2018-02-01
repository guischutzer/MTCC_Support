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
