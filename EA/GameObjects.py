import random

class Game(self):
    Fitness = None
    Score = 0

    #Basic Properties to create a game, everything else will be generated later
    def __init__(self, OffScreenEffect, NumActionButtons, Score):
        self.OffScreenEffect = OffScreenEffect
        self.NumActionButtons = NumActionButtons
        self.Score = Score


    #We don't pass individual objects into the Game
    #We define rules for entire classes of objects, as shown below
    #C = [Number_of_Circles, GameObject_Representing_Circles, [locations_of_circles]]
    #This allows us to tweak individual object spawn rates
    #And ensures all objects sharing a sprite have consistent properties.
    def SetObjectLogs(self, C, S, T, X, Player):
        self.C = C  #Circles
        self.S = S  #Squares
        self.T = T  #Triangles
        self.X = X  #Crosses
        self.Player = Player    #Player

    def SetFitness(self,fitness):
        self.Fitness = fitness


class GameObject(self):
    Fitness = 0

    #All buttons saved as variables
    Up = None
    Left = None
    Down = None
    Right = None
    A1 = None
    A2 = None
    A3 = None
    A4 = None

    def __init__(self, HP, Shape, Color, Opacity, Col_C, Col_S, Col_T, Col_X, Col_P, NumActionButtons, Game):
        self.HP = HP
        self.Shape = Shape
        self.Color = Color
        self.Opacity = Opacity
        self.Col_C = Col_C #Collision with Circles
        self.Col_S = Col_S #Collision with Squares
        self.Col_T = Col_T #Etc.
        self.Col_X = Col_X
        self.Col_P = Col_P
        self.Game = Game
        GenerateActionSet(NumActionButtons)

    def GenerateActionSet(self, NumAct):
        #List of all buttons
        ButtonSet = [self.Up, self.Left, self.Right, self.Down, self.A1, self.A2, self.A3, self.A4]
        ActionSet = ["Game.Score += " + str(random.randint(0,10)), "Self.Destroy()"]
        #Need to work on unity syntax before finishing this

        for i in range(NumAct):
            k = random.randrange(0,len(ButtonSet)-1)
            j = random.choice(ActionSet)
            ButtonSet[k] = j


    #TODO: Function to set individual action, to allow for easy crossover

    def SetFitness(self, fitness):
        self.Fitness = fitness








