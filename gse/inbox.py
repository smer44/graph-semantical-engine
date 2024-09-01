class InboxValue:

    def __init__(self, value):
        self.value = value

    def set(self,value):
        self.value = value

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return f"|{str(self.value)}|"

    def __repr__(self):
        return f"|{repr(self.value)}|"