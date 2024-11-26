

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

class NEnum:

    items = dict()

    def __init__(self, name):
        if not isinstance(name, str):
            raise ValueError("NEnum.__init__: given name is not str")
        if name in NEnum.items:
            raise ValueError(f"NEnum.__init__: {name=} already used")

        NEnum.items[name] = self
        self.name = name
        self.parent = None


    def chi(self,name):
        child = NEnum(name)
        child.parent = self
        return child

    def gen_parents(self):
        obj = self
        yield obj.name
        while obj.parent is not None:
            obj = obj.parent
            yield obj.name


    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        names =[self.name]
        obj = self
        while obj.parent is not None:
            obj = obj.parent
            names.append(obj.name)
        return ".".join(names)

#---
situation = NEnum("situation")

s_location_based = situation.chi("location_based")
s_loc_outter = s_location_based.chi("s_loc_outter")
s_loc_inner = s_location_based.chi("s_loc_inner")

s_loc_park = s_loc_outter.chi("park")
s_loc_street = s_loc_outter.chi("street")
s_loc_wild = s_loc_outter.chi("s_loc_wild")


s_loc_office = s_loc_inner.chi("s_loc_office")
s_loc_own_home = s_loc_inner.chi("s_loc_own_home")
s_loc_friends_home = s_loc_inner.chi("s_loc_friends_home")
s_loc_appartement_to_investigate = s_loc_inner.chi("s_loc_appartement_to_investigate")

s_shop = s_loc_inner.chi("s_shop")
s_loc_restaurant = s_loc_inner.chi("s_loc_restaurant")







privateness_based = situation.chi("privateness_based")

private_space = privateness_based.chi("private_space")
business_space = privateness_based.chi("business_space")




mass_event_based = situation.chi("mass_event_based")

entarteiment_event = mass_event_based.chi("entarteiment_event")
educational_event = mass_event_based.chi("educational_event")

self_presentation_event = mass_event_based.chi("self_presentation_event")

party = entarteiment_event.chi("party")
entarteiment_event_continuable_end = entarteiment_event.chi("entarteiment_event_continuable_end")
cinema = entarteiment_event.chi("cinema")

s_lesson = educational_event.chi("s_lesson")


#Time - based situation :

time_based = situation.chi("time_based")

morning = time_based.chi("morning")
afternoon = time_based.chi("afternoon")
evening = time_based.chi("evening")
night = time_based.chi("night")

being_late = time_based.chi("being_late")

s_work_time = time_based.chi("work_time")
s_time_deadline = time_based.chi("s_time_deadline")

free_time = time_based.chi("free_time")
free_evening = free_time.chi("free_evening")
free_day = free_time.chi("free_day")
weekend = free_day.chi("weekend")

#---

s_event_based = situation.chi("s_event_based")
s_self_phone_call = s_event_based.chi("self_phone_call")
s_other_phone_call = s_event_based.chi("other_phone_call")
s_waiting_in_line = s_event_based.chi("s_waiting_in_line")


interaction =  situation.chi("interaction")

greeting = interaction.chi("greeting")
farawell = interaction.chi("farawell")
other_jokes_good = interaction.chi("other_jokes_good")
other_jokes_bad =  interaction.chi("other_jokes_bad")

ask_for_help = interaction.chi("ask_for_help")
help_other = interaction.chi("help_other")
help_self = interaction.chi("help_self")
defend_other = interaction.chi("defend_other")

give_item_other = interaction.chi("give_item_other")
take_item_from_other = interaction.chi("take_item_from_other")

s_interaction_argue = interaction.chi("s_interaction_argue")

friend_is_sick = interaction.chi("friend_is_sick")
enemy_is_sick = interaction.chi("enemy_is_sick")


s_weather_based = situation.chi("weather_based")
s_sunny =  s_weather_based.chi("s_sunny")


s_persons_presence_based = situation.chi("persons_presence_based")

s_friends_presence = s_persons_presence_based.chi("friends_presence")
s_romantic_interest_presence = s_persons_presence_based.chi("s_romantic_interest_presence")
s_enemys_presence = s_persons_presence_based.chi("enemys_presence")
s_disliked_presence = s_persons_presence_based.chi("disliked_presence")
s_liked_presence = s_persons_presence_based.chi("liked_presence")
s_strangers_presence = s_persons_presence_based.chi("strangers_presence")
s_colleagues_presence = s_persons_presence_based.chi("colleagues_presence")

s_group_presence = s_persons_presence_based.chi("group_presence")
s_one_on_one_presence = s_persons_presence_based.chi("one_on_one_presence")
s_alone = s_persons_presence_based.chi("alone")


s_self_emotion_based = situation.chi("self_emotion_based")
s_self_happy = s_self_emotion_based.chi("self_happy")
s_self_feel_careless = s_self_emotion_based.chi("s_self_feel_careless")
s_self_excited = s_self_happy.chi("s_self_excited")
s_self_sad = s_self_emotion_based.chi("self_sad")
s_self_high = s_self_emotion_based.chi("self_high")
s_self_stressed = s_self_emotion_based.chi("self_stressed")
s_self_angry = s_self_emotion_based.chi("self_angry")
s_self_dizzy = s_self_emotion_based.chi("self_dizzy")
s_self_bored = s_self_emotion_based.chi("s_self_bored")
s_self_tired = s_self_emotion_based.chi("s_self_tired")
s_self_energized = s_self_emotion_based.chi("s_self_energized")



other_of_mc_emotion_based = situation.chi("other_of_mc_emotion_based")
mc_happy = other_of_mc_emotion_based.chi("mc_happy")
mc_sad = other_of_mc_emotion_based.chi("mc_sad")
mc_high = other_of_mc_emotion_based.chi("mc_high")
mc_stressed = other_of_mc_emotion_based.chi("mc_stressed")
mc_angry = other_of_mc_emotion_based.chi("mc_angry")
mc_dizzy = other_of_mc_emotion_based.chi("mc_dizzy")



persons_absence_based = situation.chi("persons_absence_based")
persons_unexpected_absence_based = persons_absence_based.chi("persons_unexpected_absence_based")

friend_unexpected_absence_based = persons_unexpected_absence_based.chi("friend_unexpected_absence_based")
enemies_unexpected_absence_based = persons_unexpected_absence_based.chi("enemies_unexpected_absence_based")
strangers_unexpected_absence_based = persons_unexpected_absence_based.chi("strangers_unexpected_absence_based")


#ACTIONS:


action = NEnum("action")
a_communicate = action.chi("interaction_action")


a_initiate_conversation = a_communicate.chi("initiate_conversation")
a_initiate_conversation_about_exciting = a_initiate_conversation.chi("a_initiate_conversation_about_exciting")

a_greet_action = a_communicate.chi("greet")
a_make_joke = a_communicate.chi("make_joke")
a_insult = a_communicate.chi("insult")
a_flirt = a_communicate.chi("flirt")
a_confident_flirt = a_flirt.chi("a_confident_flirt")
a_talk_heart_to_heart = a_communicate.chi("talk_heart_to_heart")
a_suggest_friend_go_out = a_communicate.chi("suggest_friend_go_out")
a_ask_help = a_communicate.chi("a_ask_help")


a_task_related = action.chi("task_related")
a_study = a_task_related.chi("study")
a_sit_still_in_class = a_study.chi("sit_still_in_class")
a_work = a_task_related.chi("work")
a_find_shortcut = a_task_related.chi("a_find_shortcut")

a_leave_task_unfinished = a_task_related.chi("leave_task_unfinished")
a_rush_without_planning = a_task_related.chi("rush_without_planning")
a_avoid_task =  a_task_related.chi("a_avoid_task")
a_engage_in_risk =  a_task_related.chi("a_engage_in_risk")


a_task_not_related = action.chi("a_task_not_related")
a_relax = a_task_not_related.chi("a_relax")
a_take_active_fun = a_task_not_related.chi("a_take_active_fun")
a_dance = a_take_active_fun.chi("a_dance")
a_sport_fun = a_take_active_fun.chi("a_sport_fun")
a_plan_adventure = a_take_active_fun.chi("a_plan_adventure")
a_change_action = a_task_not_related.chi("a_change_action")
a_buy_impulsively = a_task_not_related.chi("a_buy_impulsively")
a_convince_continue_fun = a_task_not_related.chi("a_convince_continue_fun")

a_movement = action.chi("a_movement")
a_explore = a_movement.chi("a_explore")#explore is not about movement!!
a_pick_adventurous_from_menu = a_explore.chi("a_pick_adventurous_from_menu")




a_conflict_reaction = action.chi("conflict_reaction")
a_apologize = a_conflict_reaction.chi("apologize")
a_escalate = a_conflict_reaction.chi("escalate")
a_walk_away = a_conflict_reaction.chi("walk_away")
a_take_side_for_argue = a_conflict_reaction.chi("a_take_side_for_argue")

a_physical_need_action = action.chi("physical_needs")
a_eat =  a_physical_need_action.chi("eat")
a_drink =  a_physical_need_action.chi("drink")
a_sleep =  a_physical_need_action.chi("sleep")
a_promenade = a_physical_need_action.chi("promenade")


variable = NEnum("variable")
v_personality_trait = variable.chi("personality_trait")
v_introverted = v_personality_trait.chi("introverted")
v_extroverted = v_personality_trait.chi("extroverted")
v_caring = v_personality_trait.chi("caring")

class DesigionSummand:
    by_situations = dict()

    def __init__(self, situation,action,weight):
        self.situation = situation
        self.action = action
        self.weight = weight
        d = DesigionSummand.by_situations
        row = d.setdefault(self.situation,list())
        row.append(self)

    def __repr__(self):
        return f"{self.situation} -> {self.action}*{self.weight}"

#chloe character:
op1 = DesigionSummand(s_loc_outter,a_take_active_fun,1)
op2 = DesigionSummand(s_loc_outter,a_promenade,1)

ip1 = DesigionSummand(s_loc_inner,a_take_active_fun,1)
ip2 = DesigionSummand(s_loc_inner,a_relax,1)

park1 = DesigionSummand(s_loc_park,a_take_active_fun,1)
park2 = DesigionSummand(s_loc_park,a_talk_heart_to_heart,1)




ex1 = DesigionSummand(v_extroverted,a_take_active_fun,5)

#from changpt:
pa1 = DesigionSummand(party, a_dance, 10)

stra1 = DesigionSummand(s_strangers_presence, a_initiate_conversation,5)
stra2 = DesigionSummand(s_group_presence,a_initiate_conversation_about_exciting,5)

wo1 = DesigionSummand(s_work_time,a_leave_task_unfinished,8)
wo2 = DesigionSummand(s_time_deadline,a_ask_help,7)
wo3 = DesigionSummand(s_work_time,a_find_shortcut,7)


fre1 = DesigionSummand(free_evening,a_suggest_friend_go_out,10)

mle1 = DesigionSummand(being_late,a_rush_without_planning,9)

#
clb = DesigionSummand(s_lesson,a_initiate_conversation,8)

sun1 = DesigionSummand(s_sunny, a_sport_fun,10)

rom1 = DesigionSummand(s_romantic_interest_presence, a_confident_flirt,9)
fri1 =  DesigionSummand(s_friends_presence,a_take_active_fun,10)
fri2 =  DesigionSummand(s_friends_presence,a_initiate_conversation_about_exciting,10)



stre1= DesigionSummand(s_self_stressed,a_avoid_task,3)
stre2= DesigionSummand(s_self_stressed,a_relax,3)


waba1 = DesigionSummand(s_self_bored,a_change_action,8)

sho1 = DesigionSummand(s_shop,a_buy_impulsively,5)

exi = DesigionSummand(s_self_excited,a_plan_adventure,7)
exi2 = DesigionSummand(s_self_happy,a_take_active_fun,10)
exi3 = DesigionSummand(s_self_energized,)

exi4 = DesigionSummand(s_self_feel_careless, a_engage_in_risk,8)

sad1 = DesigionSummand(s_self_sad,a_initiate_conversation,5)


tir1 = DesigionSummand(s_self_tired,a_communicate,5)

arg1 = DesigionSummand(s_interaction_argue,a_make_joke,8)
arg2 = DesigionSummand(s_interaction_argue,a_take_side_for_argue,7)



out1 = DesigionSummand(s_loc_wild,a_explore,7)

#22

wait1 = DesigionSummand(s_waiting_in_line, a_initiate_conversation, 5)


par_end1 = DesigionSummand(entarteiment_event_continuable_end, a_convince_continue_fun,7)

#a_adventours_option for any situation
res1 = DesigionSummand(s_loc_restaurant,a_pick_adventurous_from_menu,7)











class Actor:

    def __init__(self, name, activity_interests, shedule, needs):
        self.name = name
        self.activity_interests = activity_interests
        self.shedule = shedule
        self.needs = needs

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.name})"


    def calc_priority(self, situation, *variables ):
        #returns action
        pass









