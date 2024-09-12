class InboxCounterValue:

    counter = 0
    def __init__(self, value,id = None):
        self.value = value
        if id is None:
            id = InboxCounterValue.counter
        self.id = id
        InboxCounterValue.counter = id + 1

    def set(self,value):
        self.value = value

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"|#{self.id}:{str(self.value)}|"

    def __repr__(self):
        return f"|#{self.id}:{str(self.value)}|"