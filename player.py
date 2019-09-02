
import random
class Player:
    id = 0
    name = ""
    coins = 0
    cards = []
    state = ""
    def __init__(self, player_id , name = "HI"):
        self.id = player_id 
        self.state = "NONE"
        self.cards = []
        self.coins = 0
        self.name = name

    def get_name(self):
        return self.name
    
    def is_bluffing(self,action):
        return not ( self.cards[0].is_eligable_action(action) or self.cards[1].is_eligable_action(action) )
    
    def has_card(self,card_name):
        return not (( self.cards[0].get_name() == card_name and self.cards[0].state == "active")  or  ( self.cards[1].get_name() == card_name and  self.cards[0].state == "active" ))
    
    def set_coins(self,count):
        self.coins = count
    
    def get_coins(self):
        return self.coins
    
    def get_rubbed(self):
        if(self.coins - 2 >= 0 ):
            self.coins = self.coins - 2    
            return 2
        else:
            profit = self.coins
            self.coins = 0
            return profit
    
    def kill_one_card(self):
        
        return random.choice(self.cards).deactive_card()
        
    def get_id(self):
        return self.id

    def get_state(self):
        return self.state
    
    def add_card(self,card):
        self.cards.append(card)

    def set_state(self,state):
        self.state = state
    def get_cards(self):
        return self.cards
    def income(self):
        self.coins += 1

        return False
    def tax(self):
        self.income +=3
     
    def assasinate(self):
        return True
    
    def foreign_aid(self):
        pass
    
    def tax(self):
        pass
    
    def exchange(self):
        pass
    
    def challenge(self):
        pass

    def steal(self):
        self.coins += 2
        pass

    def counter(self):
        pass
