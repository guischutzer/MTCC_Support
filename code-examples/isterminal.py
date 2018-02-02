def isTerminal(self):
    if self.phase == 'End':
        return True
    if self.opponentLifeTotal <= 0 or self.ownLifeTotal <= 0:
        return True
    return False
