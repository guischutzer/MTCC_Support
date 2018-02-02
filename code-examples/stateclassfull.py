class State:

    def __init__(self, game, phase, actionPath):
        self.game = game
        self.phase = phase
        self.actionPath = actionPath
        if len(actionPath) > 0:
            self.parentAction = actionPath[-1]
        else:
            self.parentAction = [None]
        self.ownLifeTotal = game.activePlayer.life
        self.opponentLifeTotal = game.opponent.life
        self.ownPower = 0
        self.ownTou = 0
        self.opponentPower = 0
        self.opponentTou = 0
        self.landNumber = len(game.activePlayer.lands)
        self.handSize = len(game.activePlayer.hand)
        self.winReward = 100
        self.lossReward = -100
        for creature in game.activePlayer.creatures:
            self.ownPower += creature.curPower
            self.ownTou += creature.curTou
        for creature in game.opponent.creatures:
            self.opponentPower += creature.curPower
            self.opponentTou += creature.curTou

    def isTerminal(self):
        if self.phase == 'End':
            return True
        if self.opponentLifeTotal <= 0 or self.ownLifeTotal <= 0:
            return True
        return False

    def getChildren(self):
        children = []
        if self.phase == 'First Main' or self.phase == 'Second Main':
            for action in self.game.getMainActions():
                game = self.game
                nextPhase = self.phase
                if action[0] != 'Pass':
                    game = c.deepcopy(self.game)
                    game.play(action)
                    game.checkSBA()
                elif self.phase == 'First Main':
                    nextPhase = 'Combat'
                elif self.phase == 'Second Main':
                    nextPhase = 'End'
                children.append(State(game, nextPhase, self.actionPath + [action]))
        else:
            children = self.combatMaxMin()
        return children

    def combatMaxMin(self):
        children = []
        game = self.game
        attackConfigurations = game.getAttackingActions()
        noAttacksState = State(game, 'Second Main', self.actionPath + [[]])
        children.append(noAttacksState)
        for attackers in attackConfigurations:
            newGame = c.deepcopy(game)
            combatPairings = newGame.attack(attackers)
            legalBlocks = newGame.getBlockingActions(attackers)
            combatPairingsIDs = newGame.activePlayer.chooseBlockers(legalBlocks, combatPairings, self)
            combatPairings = newGame.getCombatPairingsFromIDs(combatPairingsIDs)
            newGame.resolveCombat(combatPairings)
            attIDs = []
            for attacker in attackers:
                attIDs.append(attacker.ID)
            children.append(State(newGame, 'Second Main', self.actionPath + [attIDs]))
        return children

    def getReward(self):
        reward = (self.ownLifeTotal - self.opponentLifeTotal)/5 + self.ownPower - self.opponentPower + (self.ownTou - self.opponentTou)/2 + 1.1*self.landNumber + self.handSize
        if self.opponentLifeTotal <= 0:
            return self.winReward + reward
        if self.ownLifeTotal <= 0:
            return self.lossReward + reward
        return reward

    def getPath(self):
        return self.actionPath

    def __str__(self):
        s = "own life: " + str(self.ownLifeTotal)
        s += "\nopp life: " + str(self.opponentLifeTotal)
        s += "\nown power: " + str(self.ownPower)
        s += "\nopp power: " + str(self.opponentPower)
        s += "\naction path: " + str(self.actionPath)
        return s
