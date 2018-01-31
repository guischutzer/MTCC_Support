class VolcanicHammer(Card):
    def __init__(self, owner):
        self.name = "Volcanic Hammer"
        self.cost = "1R"
        self.supertype = ""
        self.ctype = "Sorcery"
        self.subtype = ""
        self.text = "Volcanic Hammer deals 3 damage to target creature or player."
        self.targets = [["OwnCreature", "OpponentCreature", "Player"]]
        self.owner = owner

    def effect(self, game, targets):
        targets[0].takeDamage(3)
