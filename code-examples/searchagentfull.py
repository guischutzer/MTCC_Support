class SearchAgent(RandomAgent):

    def declareBlockers(self, legalActions, combatPairings, state):

        pairings = self.chooseBlockers(legalActions, combatPairings, state)

        noBlocks = True
        print("Player " + self.name + " has declared ", end='')
        finalPairings = state.game.combatPairingsFromIDs(pairings)
        for attacker in finalPairings:
            for blocker in finalPairings[attacker]:
                noBlocks = False
                print("")
                print(" - " + blocker.stats() + " blocking " + attacker.stats(), end='')

        if noBlocks:
            print("no blockers.")
        else:
            print("")
        return finalPairings

    def chooseBlockOrder(self, combatPairings, game):

        listOfPairings = utils.intraPermutations(combatPairings)
        maxReward = None
        assignedPairingIDs = {}
        for pairing in listOfPairings:
            newGame = c.deepcopy(game)
            newGame.combatPairings = {}
            pairingIDs = {}
            for attacker in pairing:
                newAttacker = newGame.getPermanentFromID(attacker.ID)
                newGame.combatPairings[newAttacker] = []
                pairingIDs[attacker.ID] = []
                for blocker in pairing[attacker]:
                    newBlocker = newGame.getPermanentFromID(blocker.ID)
                    pairingIDs[attacker.ID].append(blocker.ID)
                    newGame.combatPairings[newAttacker].append(blocker)
            newGame.resolveCombat(newGame.combatPairings)
            state = State(newGame, 'Combat', [])
            reward = state.getReward()
            if maxReward == None or reward >= maxReward:
                maxReward = reward
                assignedPairingIDs = pairingIDs

        return assignedPairingIDs

    def assignBlockOrder(self, combatPairings, game):

        combatPairings = self.chooseBlockOrder(combatPairings, game)

        combatPairings = game.combatPairingsFromIDs(combatPairings)
        for attacker in combatPairings:
            if len(combatPairings[attacker]) > 1:
                print("Player " + self.name + " blocks " + attacker.stats())
                i = 1
                for blocker in combatPairings[attacker]:
                    print(" - " + utils.getOrdinal(i) + " with " + blocker.stats())
                    i += 1

        return combatPairings

    def getChildren(self, state):

        if state.phase == 'Combat':
            return self.combatMaxMin(state)

        return state.getChildren()

    def combatMaxMin(self, state):
        children = []
        game = state.game
        attackConfigurations = game.getAttackingActions()
        noAttacksState = State(game, 'Second Main', state.actionPath + [[]])
        children.append(noAttacksState)
        for attIDs in attackConfigurations:
            newGame = c.deepcopy(game)
            newAttackers = []
            for attID in attIDs:
                newAttackers.append(newGame.getPermanentFromID(attID))
            combatPairings = newGame.attack(newAttackers)
            legalBlocks = newGame.getBlockingActions(newAttackers)
            combatPairingsIDs = self.chooseBlockers(legalBlocks, combatPairings, state, False)
            combatPairings = newGame.getCombatPairingsFromIDs(combatPairingsIDs)
            newGame.resolveCombat(combatPairings)
            children.append(State(newGame, 'Second Main', state.actionPath + [attIDs]))
        return children

    def breadthFirstSearch(self, startState):

        q = queue.Queue()
        q.put(startState)
        maxReward = -200
        actionPath = []

        while not q.empty():

            state = q.get()

            if state.isTerminal():
                reward = state.getReward()
                if reward >= maxReward:
                    maxReward = reward
                    actionPath = state.getPath()
            else:
                for s in self.getChildren(state):
                    q.put(s)

        return actionPath

    def chooseBlockers(self, legalActions, combatPairings, state, printing):
        maxReward = None
        maxRewardPairingsIDs = {}
        for attacker in combatPairings:
            maxRewardPairingsIDs[attacker.ID] = []

        for blocks in legalActions:
            newGame = c.deepcopy(state.game)
            pairingsIDs = {}
            for attacker in combatPairings:
                pairingsIDs[attacker.ID] = []
            for i in range(len(blocks)):
                blocker = newGame.opponent.creatures[i]
                blockedCreature = blocks[i]
                if blockedCreature != None:
                    pairingsIDs[blockedCreature.ID].append(blocker.ID)
            pairingsIDs = self.chooseBlockOrder(pairingsIDs, newGame)
            newPairings = newGame.getCombatPairingsFromIDs(pairingsIDs)
            if printing:
                print("+++++++PREBLOCK+++++++")
                print(pairingsIDs)
                newGame.printGameState()
            newGame.resolveCombat(newPairings)
            newState = State(newGame, 'Combat', [])
            reward = -newState.getReward()
            if printing:
                print("+++++++POSTBLOCK+++++++")
                newGame.printGameState()
                print(reward)
            if maxReward == None or reward > maxReward:
                maxRewardPairingsIDs = pairingsIDs
                maxReward = reward

        if printing:
            print(maxRewardPairingsIDs)
            print(maxReward)
        return maxRewardPairingsIDs

    def chooseBlockOrder(self, combatPairingsIDs, game):

        listOfPairings = utils.intraPermutations(combatPairingsIDs)
        maxReward = None
        assignedPairingsIDs = {}
        for pairingsIDs in listOfPairings:
            newGame = c.deepcopy(game)
            newPairings = {}
            newPairingsIDs = {}
            for attID in pairingsIDs:
                newAttacker = newGame.getPermanentFromID(attID)
                newPairings[newAttacker] = []
                newPairingsIDs[attID] = []
                for blkID in pairingsIDs[attID]:
                    newBlocker = newGame.getPermanentFromID(blkID)
                    newPairingsIDs[attID].append(blkID)
                    newPairings[newAttacker].append(newBlocker)
            newGame.resolveCombat(newPairings)
            state = State(newGame, 'Combat', [])
            reward = state.getReward()
            if maxReward == None or reward >= maxReward:
                maxReward = reward
                assignedPairingsIDs = newPairingsIDs

        return assignedPairingsIDs

    def declareBlockers(self, legalActions, combatPairings, state):

        pairingsIDs = self.chooseBlockers(legalActions, combatPairings, state, True)

        noBlocks = True
        print("Player " + self.name + " has declared ", end='')
        finalPairings = state.game.getCombatPairingsFromIDs(pairingsIDs)
        for attacker in finalPairings:
            for blocker in finalPairings[attacker]:
                noBlocks = False
                print("")
                print(" - " + blocker.stats() + " blocking " + attacker.stats(), end='')

        if noBlocks:
            print("no blockers.")
        else:
            print("")
        return finalPairings

    def assignBlockOrder(self, combatPairings, game):

        combatPairingsIDs = {}
        for attacker in combatPairings:
            combatPairingsIDs[attacker.ID] = []
            for blocker in combatPairings[attacker]:
                combatPairingsIDs[attacker.ID].append(blocker.ID)

        combatPairingsIDs = self.chooseBlockOrder(combatPairingsIDs, game)

        combatPairings = game.getCombatPairingsFromIDs(combatPairingsIDs)
        for attacker in combatPairings:
            if len(combatPairings[attacker]) > 1:
                print("Player " + self.name + " blocks " + attacker.stats())
                i = 1
                for blocker in combatPairings[attacker]:
                    print(" - " + utils.getOrdinal(i) + " with " + blocker.stats())
                    i += 1

        return combatPairings
