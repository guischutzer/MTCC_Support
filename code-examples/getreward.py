def getReward(self):
    reward = (self.ownLifeTotal - self.opponentLifeTotal)/5
    reward += self.ownPower - self.opponentPower
    reward += (self.ownTou - self.opponentTou)/2
    reward += 1.1*self.landNumber + self.handSize
    if self.opponentLifeTotal <= 0:
        return self.winReward + reward
    if self.ownLifeTotal <= 0:
        return self.lossReward + reward
        return reward
