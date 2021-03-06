from player import Player
from Card import Card
import time
import uuid,random
class Game:
    id = 0
    last_action_time = 0
    turn = 0
    cards = []
    players = []
    action = ""
    reaction_card = ""
    reacting_player = ""
    challenging_player = ""
    state = "" #Challenging, Over, Acting, Revealing, Starting
    target_player = ""
    exchanging_cards = []
    
    def __init__(self,player_list,start_time):
        self.id = uuid.uuid4().time_low
        self.last_action_time = start_time
        self.state = "Starting"
        self.target_player = ""
        self.reaction = ""
        self.challenging_player = ""
        self.exchanging_cards = []
        for p in player_list:
            self.players.append(Player(p))
        for i in range(3):
            self.cards.append(Card('Duke', ['TAX','BLOCK_FOREIGN_AID']))
            self.cards.append(Card('Captain', ['STEAL','BLOCK_STEAL'])) #Block steal
            self.cards.append(Card('Ambassador', ['EXCHANGE','BLOCK_STEAL'])) #Block steal
            self.cards.append(Card('Assassin', ['ASSASINATE']))
            self.cards.append(Card('Contessa', ['BLOCK_ASSASIANTE'])) #Block assassinationi

    def get_cards_for_exchange(self):
        cards = [ card for card in  self.players[self.get_turn()].get_cards() if card.get_state() == "active" ] + self.get_two_random_card()
        self.exchanging_cards = cards

        self.players[self.get_turn()].clean_cards()

        return cards
    
    
    def get_challenging_player(self):
        return self.challenging_player
    def get_exchanging_cards(self):
        return self.exchanging_cards


    def get_two_random_card(self):
        random.shuffle(self.cards)
        random_cards = [
            self.cards.pop(),self.cards.pop()
        ]
        return random_cards


    def check_action_is_exchange(self):
        if(self.action == "EXCHANGE"):
            return  True
        return False
    
    def get_target_player(self):
        return self.target_player
    
    def perform(self):
        if(self.action == "TAX"):
            self.players[self.get_turn()].tax()
            return None , False
        if(self.action == "STEAL"):
            profit = self.target_player.get_rubbed()
            self.players[self.get_turn()].set_coins(self.players[self.get_turn()].get_coins() + profit )
            return None , False
        if(self.action == "COUP"):
            card , is_dead = self.target_player.kill_one_card()
            return card , is_dead
        if(self.action == "ASSASINATE"):
            card , is_dead = self.target_player.kill_one_card()
            return card , is_dead
        if(self.action == "INCOME"):
            self.players[self.get_turn()].income()
            return None , False

        return None , False
        

    def get_reaction_card(self):
        return self.reaction_card

    
    def set_reaction_card(self , reaction_card):
        self.reaction_card = reaction_card


    def get_turn_counter(self):
        return self.turn


    def set_target_player(self,target_player_chat_id):
        
        for player in self.players:
            if(player.get_id().message.chat_id == target_player_chat_id):
                self.target_player = player
                return True
        return False

    
    def check_target_player_need(self):
        if(self.action in ["ASSASINATE","STEAL","COUP"]):
            return True
        else:
            return False
    def check_react_challenge(self):
        if(self.get_target_player().has_card(self.reaction_card)):
            card , is_dead  = self.get_players()[self.get_turn()].kill_one_card()
            return False , card , is_dead
        else:
            card , is_dead  = self.get_target_player().kill_one_card()
            return True , card , is_dead


    def check_challenge(self,player_chat_id):
        playing_player_index = self.get_turn()
        challenging_player_chat_id = player_chat_id

        for player in self.players:
            c = player.get_id().message.chat_id
            if( c == challenging_player_chat_id):
                challenging_player = player
                self.challenging_player = player
        is_bluffing = self.players[playing_player_index].is_bluffing(self.action)

        if(is_bluffing):
            card , is_dead = self.players[playing_player_index].kill_one_card()
           
            return True , card , is_dead 
        else:
            card , is_dead = challenging_player.kill_one_card()
            return False , card , is_dead   

    def check_challenge_possibility(self):
        if(self.action in ['COUP','INCOME']):
            return False
        else:
            self.get_last_action_time = time.time()
            return True

    def get_action(self):
        return self.action
    
    def set_action(self,new_action):
        self.action = new_action
        return 1
    
    def get_turn(self):
        return self.turn % len(self.players)
        
    def next_turn(self):
        self.target_player = ""
        self.action = ""
        self.reaction_card = ""
        self.reacting_player = ""
        self.state = "" #Challenging, Over, Acting, Revealing, Starting
        for i in range(self.turn+1,5000):
            if(self.players[i % len(self.players)].get_state()!= "DEAD"):
                self.turn = i 
                break
        return True

    def start(self):
        random.shuffle(self.cards)
        for player in self.players:
            player.add_card(self.cards.pop())
            player.add_card(self.cards.pop())
            player.coins = 2
        turn = 0
        self.state = "Acting" 

    def get_living_players(self):
      
        return  [player for player in self.players if player.state != "Dead"  ]
    def get_players(self):
        return self.players
    def get_last_action_time(self):    
        return self.last_action_time
    
    def get_state(self):
        return self.state

    def set_state(self,state):
        self.state = state
        
    def set_last_action_time(self,time):
        self.last_action_time = time    
        return 1
    
    def get_id(self):
        return self.id
