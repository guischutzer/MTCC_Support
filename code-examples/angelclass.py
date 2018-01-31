class AngelofMercy(Card):
    def __init__(self,owner):
        self.name = "Angel of Mercy"
        self.cost = "4W"
        self.supertype = ""
        self.ctype = "Creature"
        self.subtype = "Angel"
        self.text = "Flying. When Angel of Mercy enters the battlefield, you gain 3 life. 3/3"
        self.abilities = ["Flying"]
        self.targets = []
        self.owner = owner
        self.power = 3
        self.tou = 3

    def effect(self, game, targets):
        self.owner.gainLife(3)
