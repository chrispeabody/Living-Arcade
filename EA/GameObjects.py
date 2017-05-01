import random, pyodbc

#TODO
# 1. Fix randomization values in populateObjectsList
# 2. Figure out what we're doing with HP
# 3. Figure out if/how we're passing numActionButtons down to trigger creation

class Game(object):
    Fitness = 0
    Score = 0

    #Basic Properties to create a game, everything else will be generated later
    def __init__(self, Name, OffScreenEffect, NumActionButtons, Score, objList, NumObj, PlayerSpawns, Player):
        self.ID = random.randint(0,2**(32)-1) #Sample Space so big collisions aren't a concern
        self.Name = Name
        self.OffScreenEffect = OffScreenEffect
        self.NumActionButtons = NumActionButtons
        self.Score = Score
        self.ObjectList = objList # This is the list of GameObject instances
        self.NumObj = NumObj
        self.PlayerSpawns = PlayerSpawns
        self.Player = Player

    def SetFitness(self,fitness):
        self.Fitness = fitness

    def __eq__(self, other):
        if isinstance(other, Game):
            return(self.Fitness == other.Fitness)
        return NotImplemented
    def __gt__(self, other):
        if isinstance(other, Game):
            return(self.Fitness > other.Fitness)
        return NotImplemented
    def __lt__(self, other):
        if isinstance(other, Game):
            return(self.Fitness < other.Fitness)
        return NotImplemented


class GameObject(object):
    Fitness = 0
    Triggers = []

    # A list of action-reaction pairs
    Triggers = []

    def __init__(self, Name, HP, Shape, Color, Opacity, MaxSpawns, MinSpawns):
        self.Name = Name
        self.HP = HP
        self.Shape = Shape
        self.Color = Color
        self.Opacity = Opacity
        self.MaxSpawns = MaxSpawns
        self.MinSpawns = MinSpawns

    def GenerateReactions(self, NumAct, Game):
        self.Triggers = []
        i = random.randint(1,8)

        for trig in range(i):
        	newTrig = Trigger()
        	newTrig.GenerateNew(Game.ObjectList)
        	self.Triggers.append(newTrig)

    def SetFitness(self, fitness):
        self.Fitness = fitness

    #This is needed to ensure every "CollideWithObject" trigger is mapped
    #To an appropriate object ID.
    #MUST BE RAN AFTER FOR EACH GAMEOBJ ALL GAMEOBJS ARE CREATED
    def UpdateTriggers(self, ObjList):
        for i in self.Triggers:
            if(i.action == "CollideWithObj"):
                i.action += "("+str(random.choice(ObjList.Name))+")"

            if(i.action == "CollideWithPlayer" and i.Name == "Player"):
                self.Triggers.remove(i)

            if(i.reaction.startswith("DestroyObj")):
                i.reaction += ", "+str(random.choice(ObjList.Name))+")"

            if(i.reaction == "CreateObj"):
                 i.reaction += "("+str(random.randint(0,12)) +", "+str(random.choice(ObjList.Name))+")"

            if(i.reaction == "CreateObjRad"):
                #The direction is given as an angle, distance is just a placeholder value, can be adjusted as needed.
                i.reaction += "("+str(random.random()*360) +", "+ str(random.randint(-100,100))+", "+str(random.choice(ObjList.Name))+")"

            if(i.reaction == "Become" and i.Name != "Player"):
                i.reaction += ", "+str(random.choice(ObjList.Name))+")"
            else:
                self.Triggers.remove(i)

    def __eq__(self, other):
        if isinstance(other, GameObject):
            return(self.Fitness == other.Fitness)
        return NotImplemented
    def __gt__(self, other):
        if isinstance(other, GameObject):
            return(self.Fitness > other.Fitness)
        return NotImplemented
    def __lt__(self, other):
        if isinstance(other, GameObject):
            return(self.Fitness < other.Fitness)
        return NotImplemented



class Trigger:
	# Every trigger has one action and one reaction
    def __init__(self):
        self.action = None
        self.reaction = None

    def __eq__(self, other):
        if isinstance(other, Trigger):
            return(self.action == other.action)
        return NotImplemented

    def GenerateNew(self):

        OffScreenEffects = ["Destroy", "Warp", "Bounce", "Stop"]

		# I know, this makes the search space look huge, but I think it's okay in this case
        actionset = ["Pressed(up)","Pressed(down)","Pressed(left)","Pressed(right)",
                    "Pressed(A1)","Pressed(A2)","Pressed(A3)","Pressed(A4)",
                    "Held(up)","Held(down)","Held(left)","Held(right)","Held(A1)",
                    "Held(A2)","Held(A3)","Held(A4)","Released(up)","Released(down)",
                    "Released(left)","Released(right)","ColideWithAny","CollideWithObj","CollideWithPlayer",
                    "OffScreen(up)","OffScreen(down)","OffScreen(left)","OffScreen(right)",
                    "OffScreen(all)","Destroyed","EnterRegion"]
		# We need to pass in something to figure out what the num of objects in this game is
		# to change "CollideWith"+str(random.randint(1,len(Triggers array <number of objects in game>))

		# Need to put something here to remove Action button triggers for buttons that were left out
		# or just only add them conditionally. Not to difficult.

        shapes = ["Square","Circle","Triangle","Pentagon","Hexagon","Octagon"] # etc. Add more as Unity team adds support

        reactionset = ["DestroySelf","DestroyObj(random","DestroyObj(nearest",
                      "DestroyObj(furthest","DestroyObj(nearestplayer","DestroyObj(furthestplayer",
                      "CreateObj","CreateObjRad","Become","ModScore",
                      "ModXSpeed","ModYSpeed","SetXSpeed","SetYSpeed","ModColor",
                      "SetColor","ModOpacity","SetOpacity","ChangeShape",
                      "ChangeOffscreenEffect","NewLevel","EndGame"]

						# we will add effets for modifying game properties, like off-screen effect, etc.
						# but for now you get the picture.

		# Consult Unity team about arbitrary values, see what seems reasonable
		# I just put temp values in. The numbers will be related to how Unity
		# calulates physics.

		# Same note on DestroyObj and CreateObj as Collide above.
		# The game will likely control where the new things spawn if a create obj is triggered

		# These strings will be stored in database and parsed Unity-side.

        act = random.choice(actionset)
        if(act == "Always"):
            act +="("+str(random.randint(0,100))+")"
        if(act == "EnterRegion"):
            act += "("+str(random.randint(1,12))+")"


        react = random.choice(reactionset)
        if(react == "ModColor"):
            react += "("+str(random.randint(-255,255))+" "+str(random.randint(-255,255))+" "+str(random.randint(-255,255))+")"
        if(react == "SetColor"):
            react += "("+str(random.randint(0,255))+" "+str(random.randint(0,255))+" "+str(random.randint(0,255))+")"
        if(react == "ModScore"):
            react += "(" + str(random.randint(0,100)) + ")"
        if(react == "ModXSpeed" or react == "ModYSpeed"):
            react += "(" + str(random.randint(-10,10)) + ")"
        if(react == "SetXSpeed" or react == "SetYSpeed"):
            react += "(" + str(random.randint(-100,100)) + ")"
        if(react == "ModOpacity"):
            react += "(" + str(random.uniform(-1,1)) + ")"
        if(react == "SetOpacity"):
            react += "(" + str(random.random()) + ")"
        if(react == "ChangeOffScreenEffect"):
            react += "(" + random.choice(OffScreenEffects) + ")"
        if(react == "ChangeShape"):
            react += "(" + random.choice(shapes) + ")"

        self.action = act
        self.reaction = react











