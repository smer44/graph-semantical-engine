

class Activity:
    def __init__(self, name,minutes):
        self.name = name
        self.minutes = minutes

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.name},{self.minutes} m.)"

class NeedQuantityPerDay:
    def __init__(self,name,quantity):
        self.name = name
        self.quantity = quantity

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.quantity},{self.quantity} quantity)"

class NeedShedulePerDay:
    pass



class TakeClass(Activity):  pass
class TakeMeal(Activity):  pass
class Shop(Activity):  pass
class Sleep(Activity):  pass


class Student:

    def __init__(self, name, activity_interests, shedule, needs):
        self.name = name
        self.activity_interests = activity_interests
        self.shedule = shedule
        self.needs = needs

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.name})"









