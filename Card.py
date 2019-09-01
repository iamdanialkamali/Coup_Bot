class card:
    name = ""
    picture = ""
    action = [] 
    def __init__(self, card_name, card_action):
        name = card_name
        action = card_action
    def get_action(self):

        return self.action

    def is_eligable_action(self,action):
        return self.get_action() ==action
