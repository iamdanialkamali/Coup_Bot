from player import Player
from Card import Card
import uuid,random
class Game:
    id = 0
    last_action_time = 0
    turn = 0
    cards = []
    players = []
    state = "" #Challenging, Over, Acting, Revealing, Starting

    def __init__(self,player_list,start_time):
        self.id = uuid.uuid4().time_low
        self.last_action_time = start_time
        self.state = "Starting"
        for p in player_list:
            self.players.append(Player(p))
        for i in range(3):
            self.cards.append(Card('Duke', ['TAX','FOA']))
            self.cards.append(Card('Captain', ['STE','BLK'])) #Block steal
            self.cards.append(Card('Ambassador', ['EXC','BLK'])) #Block steal
            self.cards.append(Card('Assassin', ['ASI']))
            self.cards.append(Card('Contessa', ['BLO'])) #Block assassinationi
    

    def start(self):
        random.shuffle(self.cards)
        for player in self.players:
            player.cards.append(self.cards.pop())
            player.cards.append(self.cards.pop())
            player.coins = 2
        turn = self.players[0].id
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
