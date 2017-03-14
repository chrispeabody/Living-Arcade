import random, pyodbc

#TODO
# 1. Fix randomization values in populateObjectsList
# 2. Figure out what we're doing with HP
# 3. Figure out if/how we're passing numActionButtons down to trigger creation

class Game(object):
    Fitness = 0
    Score = 0

    #Basic Properties to create a game, everything else will be generated later
    def __init__(self, OffScreenEffect, NumActionButtons, Score, objList, NumObj):
        self.ID = random.randint(0,2**(128)) #Sample Space so big collisions aren't a concern
        self.OffScreenEffect = OffScreenEffect
        self.NumActionButtons = NumActionButtons
        self.Score = Score
        self.ObjectList = objList # This is the list of GameObject instances
        self.NumObj = NumObj

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

    def __init__(self, Name, HP, Shape, Color, Opacity):
        self.Name = Name
        self.HP = HP
        self.Shape = Shape
        self.Color = Color
        self.Opacity = Opacity

    def GenerateReactions(self, NumAct):
        self.Triggers = []
        i = random.randint(1,8)

        for trig in range(i):
        	newTrig = Trigger()
        	newTrig.GenerateNew()
        	self.Triggers.append(newTrig)

    def SetFitness(self, fitness):
        self.Fitness = fitness


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
		# I know, this makes the search space look huge, but I think it's okay in this case
        actionset = ["UpPressed", "LeftPressed", "DownPressed", "RightPressed",
					"UpHeld", "LeftHeld", "DownHeld", "RightHeld",
					"UpReleased", "LeftReleased", "DownReleased", "RightReleased",
					"A1Pressed", "A2Pressed", "A3Pressed", "A4Pressed",
					"A1Held", "A2Held", "A3Held", "A4Held",
					"A1Released", "A2Released", "A3Released", "A4Released",
					"CollideWith"+str(random.randint(1,8)), "CollideWithAny",
					"OffScreen"]
		# We need to pass in something to figure out what the num of objects in this game is
		# to change "CollideWith"+str(random.randint(1,len(Triggers array <number of objects in game>))

		# Need to put something here to remove Action button triggers for buttons that were left out
		# or just only add them conditionally. Not to difficult.

        shapes = ["Square","Circle","Triangle","Octogon"] # etc. Add more as Unity team adds support

        reactionset = ["ModScoreBy"+str(random.randint(-100,100)),
						"ModSpeedBy"+str(random.randint(-10,10)),
						"SetSpeedTo"+str(random.randint(-100,100)),
						"ModDirBy"+str(random.randint(-180,180)),
						"SetDirTo"+str(random.randint(0,359)),
						"DestorySelf", "DestroyObj"+str(random.randint(1,8)),
						"CreateObj"+str(random.randint(1,8)),
						"SetShape"+random.choice(shapes),
						"ModColorBy"+str(random.randint(-255,255))+"-"+str(random.randint(-255,255))+"-"+str(random.randint(-255,255)),
						"SetColorTo"+str(random.randint(0,255))+"-"+str(random.randint(0,255))+"-"+str(random.randint(0,255)),
						"ModOpacityBy"+str(random.randint(-100,100)),
						"SetOpacityTo"+str(random.randint(0,100)),
						"NewLevel", "EndGame"]
						# we will add effets for modifying game properties, like off-screen effect, etc.
						# but for now you get the picture.

		# Consult Unity team about arbitrary values, see what seems reasonable
		# I just put temp values in. The numbers will be related to how Unity
		# calulates physics.

		# Same note on DestroyObj and CreateObj as Collide above.
		# The game will likely control where the new things spawn if a create obj is triggered

		# These strings will be stored in database and parsed Unity-side.

        self.action = random.choice(actionset)
        self.reaction = random.choice(reactionset)








