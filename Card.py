class card:
    name = ""
    picture = ""
    action = ""
    def __init__(self, *args, **kwargs):

        return super().__init__(*args, **kwargs)

    def get_action(self):

        return self.action

    def is_eligable_action(self,action):
        return self.get_action() == action