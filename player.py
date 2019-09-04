
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
        self.name = player_id.effective_user.first_name

   
    def get_name(self):
        return self.name
    
    def is_bluffing(self,action):
        for card in self.get_cards():
            if(card.is_eligable_action(action)):
                return False

        return True

        # return not ( self.cards[0].is_eligable_action(action) or self.cards[1].is_eligable_action(action) )
    
    def has_card(self,card_name):
        for card in self.get_cards():
            if(card.get_name() == card_name):
                return True
        return False
        # return  ( self.cards[0].get_name() == card_name and self.cards[0].state == "active")  or  ( self.cards[1].get_name() == card_name and  self.cards[0].state == "active" )
    
    def clean_cards(self):
        self.cards = []

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
        card = random.choice(self.get_cards()).deactive_card()
        if(len(self.get_cards()) == 0):
            is_dead = True
            self.state = "Dead"
        else:
            is_dead = False
        return card , is_dead
        
    def get_id(self):
        return self.id

    def get_state(self):
        return self.state
    
    def add_card(self,card):
        self.cards.append(card)

    def set_state(self,state):
        self.state = state
    def get_cards(self):
        active_cards = [ card for card in self.cards if card.state != "in_active"]
        return  active_cards
    def income(self):
        self.coins += 1

        return False
    def tax(self):
        self.coins +=3
     
    
    def steal(self):
        self.coins += 2
        pass

    