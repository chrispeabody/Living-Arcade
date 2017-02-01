from GameObjects import *
import random, json

def InitializePopulation(Pop_Size, Score, OffScreenEffect, NumObjectTypes, NumObjects, MaxX, MaxY, HP):
    population = []
    NumCircle = 0
    NumSquare = 0
    NumTriangle = 0
    NumCross = 0

    for i in range(Pop_Size):
        #Pick the number of used buttons, and initialize GameObject
        NumActionButtons = random.randint(2,4)
        NewGame = Game(OffScreenEffect, NumActionButtons, Score)

        #Randomize the size of each object population
        for j in range(NumObjects):
            k = random.randint(1,NumObjectTypes)
            if(k == 1):
                NumCircle += 1
            if(k == 2):
                NumSquare += 1
            if(k == 3):
                NumTriangle += 1
            if(k == 4):
                NumCross += 1

        #Begin the ObjectLog as described in the GameObjects File
        CircleLog = [NumCircle]
        SquareLog = [NumSquare]
        TriangleLog = [NumTriangle]
        CrossLog = [NumCross]

        #Initialize all of the GameObjects and properties
        Circle = GenerateGameObj("Circle", "circle", NumActionButtons, HP)
        Square = GenerateGameObj("Square", "square", NumActionButtons, HP)
        Triangle = GenerateGameObj("Triangle", "triangle", NumActionButtons, HP)
        Cross = GenerateGameObj("Cross", "X", NumActionButtons, HP)
        Player = GenerateGameObj("Player","player", NumActionButtons, HP)
        CircleLog += [Circle]
        SquareLog += [Square]
        TriangleLog += [Triangle]
        CrossLog += [Cross]
        PlayerLog = [1,Player,(random.uniform(0,MaxX),random.uniform(0,MaxY))]



        #Randomizes starting coordinates for all objects. Saves as list of (X,Y) tuples
        C_Coords = []
        for l in range(NumCircle):
            C_Coords.append((random.uniform(0,MaxX),random.uniform(0,MaxY)))
        CircleLog += C_Coords
        S_Coords = []
        for l in range(NumSquare):
            S_Coords.append((random.uniform(0,MaxX),random.uniform(0,MaxY)))
        SquareLog += S_Coords
        T_Coords = []
        for l in range(NumTriangle):
            T_Coords.append((random.uniform(0,MaxX),random.uniform(0,MaxY)))
        TriangleLog += T_Coords
        X_Coords = []
        for l in range(NumCross):
            X_Coords.append((random.uniform(0,MaxX),random.uniform(0,MaxY)))
        CrossLog += X_Coords

        #Put all the information together, and insert into the Population
        NewGame.SetObjectLogs(CircleLog,SquareLog,TriangleLog,CrossLog,PlayerLog)
        population.append(NewGame)

    return population

def GenerateGameObj(Name, Shape, NumActionButtons, HP):
    Color = None #TODO: Color Generating Code
    Opacity = random.uniform(0,100) #Opacity Percentage
    NewObj = GameObject(Name,HP,Shape,Color,Opacity, NumActionButtons)
    NewObj.GenerateReactions(NumActionButtons)
    return NewObj

def ToJson(CurrentGame):
    c = CurrentGame.C[1]
    s = CurrentGame.S[1]
    t = CurrentGame.T[1]
    x = CurrentGame.X[1]
    p = CurrentGame.Player[1]

    CurrentGame.C[1] ="Circle"
    CurrentGame.S[1] = "Square"
    CurrentGame.T[1] = "Triangle"
    CurrentGame.X[1] = "Cross"
    CurrentGame.Player[1] ="Player"

    #I know it's hideous, but it'll save time in the long run
    #In the meantime, try not to look at it

    GameDict = {'ID':CurrentGame.ID,'OffScreenEffect':CurrentGame.OffScreenEffect,'Score':CurrentGame.Score,
    'C':CurrentGame.C,'S':CurrentGame.S,'T':CurrentGame.T,'X':CurrentGame.X,'Player':CurrentGame.Player,
    'Score':CurrentGame.Score,'Fitness':CurrentGame.Fitness}

    SDict = {'Name':s.Name,'HP':s.HP,'Shape':s.Shape,'Color':s.Color,'Opacity':s.Opacity,'Up':s.Up,
    'Left':s.Left,'Right':s.Right,'Down':s.Down,'A1':s.A1,'A2':s.A2,'A3':s.A3,'A4':s.A4,'Col_C':s.Col_C,
    'Col_S':s.Col_S,'Col_T':s.Col_T,'Col_X':s.Col_X,'Col_P':s.Col_P,'Fitness':s.Fitness}

    CDict = {'Name':c.Name,'HP':c.HP,'Shape':c.Shape,'Color':c.Color,'Opacity':c.Opacity,'Up':c.Up,
    'Left':c.Left,'Right':c.Right,'Down':c.Down,'A1':c.A1,'A2':c.A2,'A3':c.A3,'A4':c.A4,'Col_C':c.Col_C,
    'Col_S':c.Col_S,'Col_T':c.Col_T,'Col_X':c.Col_X,'Col_P':c.Col_P,'Fitness':c.Fitness}

    TDict = {'Name':t.Name,'HP':t.HP,'Shape':t.Shape,'Color':t.Color,'Opacity':t.Opacity,'Up':t.Up,
    'Left':t.Left,'Right':t.Right,'Down':t.Down,'A1':t.A1,'A2':t.A2,'A3':t.A3,'A4':t.A4,'Col_C':t.Col_C,
    'Col_S':t.Col_S,'Col_T':t.Col_T,'Col_X':t.Col_X,'Col_P':t.Col_P,'Fitness':t.Fitness}

    XDict = {'Name':x.Name,'HP':x.HP,'Shape':x.Shape,'Color':x.Color,'Opacity':x.Opacity,'Up':x.Up,
    'Left':x.Left,'Right':x.Right,'Down':x.Down,'A1':x.A1,'A2':x.A2,'A3':x.A3,'A4':x.A4,'Col_C':x.Col_C,
    'Col_S':x.Col_S,'Col_T':x.Col_T,'Col_X':x.Col_X,'Col_P':x.Col_P,'Fitness':x.Fitness}

    PDict = {'Name':p.Name,'HP':p.HP,'Shape':p.Shape,'Color':p.Color,'Opacity':p.Opacity,'Up':p.Up,
    'Left':p.Left,'Right':p.Right,'Down':p.Down,'A1':p.A1,'A2':p.A2,'A3':p.A3,'A4':p.A4,'Col_C':p.Col_C,
    'Col_S':p.Col_S,'Col_T':p.Col_T,'Col_X':p.Col_X,'Col_P':p.Col_P,'Fitness':p.Fitness}

    with open("JsonTest.txt", "w+") as myfile:
        json.dump(SDict,myfile,indent=4)

    CurrentGame.C[1] =c
    CurrentGame.S[1] = s
    CurrentGame.T[1] = t
    CurrentGame.X[1] = x
    CurrentGame.Player[1] = p


def main():
    pop = InitializePopulation(10,0,None,3,15,100,100,1)
    ToJson(pop[0])

if __name__ == '__main__':
    main()
