import player
class Game:
    turn = 0
    cards = []
    players = []
    state = "" #Challenging, Over, Acting, Revealing, Starting

    def _init_(self,player_list):
        state = "Starting"
        turn = player_list[0]
        for p in player_list:
            players.append(Player(p))
        for i in range(3):
            cards.append(Card('Duke', ['TAX','FOA']))
            cards.append(Card('Captain', ['STE','BLK'])) #Block steal
            cards.append(Card('Ambassador', ['EXC','BLK'])) #Block steal
            cards.append(Card('Assassin', ['ASI']))
            cards.append(Card('Contessa', ['BLO'])) #Block assassinationi
