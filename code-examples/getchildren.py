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
