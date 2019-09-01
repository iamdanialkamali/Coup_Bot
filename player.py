
class player:
    id = 0
    name = ""
    cards = []
    def __init__(self, *args, **kwargs):

        return super().__init__(*args, **kwargs)
    

    def is_bluffing(self,action):
        return not ( cards[0].is_eligable_action(action) or cards[1].is_eligable_action(action) )

    # def income(self):
    #     self.coins += 1

    #     return False
    
    # def assasinate(self):
    #     return True
    
    # def foreign_aid(self):
    #     pass
    
    # def tax(self):
    #     pass
    
    # def exchange(self):
    #     pass
    
    # def challenge(self):
    #     pass

    # def steal(self,player):
    #     pass

    # def counter(self):
    #     pass
