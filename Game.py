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
    state = "" #Challenging, Over, Acting, Revealing, Starting
    target_player = ""
    
    def __init__(self,player_list,start_time):
        self.id = uuid.uuid4().time_low
        self.last_action_time = start_time
        self.state = "Starting"
        self.target_player = ""
        for p in player_list:
            self.players.append(Player(p))
        for i in range(3):
            self.cards.append(Card('Duke', ['TAX','BLOCK_FOREIGN_AID']))
            self.cards.append(Card('Captain', ['STEAL','BLOCK_STEAL'])) #Block steal
            self.cards.append(Card('Ambassador', ['EXCHANGE','BLOCK_STEAL'])) #Block steal
            self.cards.append(Card('Assassin', ['ASSASINATE']))
            self.cards.append(Card('Contessa', ['BLOCK_ASSASIANTE'])) #Block assassinationi


    def perform(self):
        if(self.action == "TAX"):
            self.players[self.turn].tax()
        if(self.action == "STEAL"):
            profit = self.target_player.get_rubbed()
            self.players[self.turn].set_coins(self.players[self.turn].get_coins() + profit )
        if(self.action == "COUP"):
            self.target_player.kill_one_card()
        if(self.action == "ASSASINATE" ):
            self.target_player.kill_one_card()
        if(self.action == "EXCHANGE"):
            pass

        self.next_turn()

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
    
    def check_challenge(self,player_chat_id):
        playing_player_index = self.turn
        challenging_player_chat_id = player_chat_id

        for player in self.players:
            c = player.get_id().message.chat_id
            if( c == challenging_player_chat_id):
                challenging_player = player
        is_bluffing = self.players[playing_player_index].is_bluffing(self.action)

        if(is_bluffing):
            self.players[playing_player_index].kill_one_card()
            return True
        else:
            challenging_player.kill_one_card()
            return False   

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
        return self.turn
        
    def next_turn(self):
        for i in range(self.turn+1,len(self.players)):
            if(self.players[i].get_state()!= "DEAD"):
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
