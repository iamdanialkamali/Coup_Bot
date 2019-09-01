
class Player:
    id = 0
    name = ""
    coins = 0
    cards = []
    state = ""
    def __init__(self, player_id ):
        self.id = player_id 
        self.state = "NONE"

    def is_bluffing(self,action):
        return not ( cards[0].is_eligable_action(action) or cards[1].is_eligable_action(action) )
    
    def get_id(self):
        return self.id

    def get_state(self):
        return self.state

    def set_state(self,state):
        self.state = state
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
