class Card:
    name = ""
    picture = ""
    action = []
    state = "active" 
    def __init__(self, card_name, card_action):
        self.name = card_name
        self.action = card_action
        self.state = "active"
    def get_action(self):

        return self.action

    def is_eligable_action(self,action):
        return action in  self.get_action()   and self.state == "active"

    def deactive_card(self):
        self.state = "in_active"
        return self
