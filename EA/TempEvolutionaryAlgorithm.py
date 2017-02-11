from GameObjects import *
import random, json
from copy import deepcopy

def InitializePopulation(Pop_Size, Score, OffScreenEffect, NumObjects, MaxX, MaxY, HP):
    population = []

    for i in range(Pop_Size):
        log = []
        #Pick the number of used buttons, and initialize GameObject
        NumActionButtons = random.randint(2,4)


        #Initialize all of the GameObjects and properties
        for j in range(NumObjects-1):
            NewLog = [GenerateGameObj(NumActionButtons, HP), (random.randint(0,MaxX),random.randint(0,MaxY))]
            log.append(NewLog)
        Player = [GenerateGameObj(NumActionButtons, HP), (random.randint(0,MaxX),random.randint(0,MaxY))] #Using generic methods to generate the player. Need to decide on what specific methods we want later.
        log.append(Player)

        NewGame = Game(OffScreenEffect, NumActionButtons, Score, log, NumObjects)

        #Put all the information together, and insert into the Population
        population.append(NewGame)

    return population

def GenerateGameObj(NumActionButtons, HP):
    shapes = ["Square","Circle","Triangle","Octogon"] #List can be expanded as unity people gives us more to work with
    Color = (random.randint(0,255),random.randint(0,255),random.randint(0,255)) #(R, G, B)
    Opacity = random.uniform(0,100) #Opacity Percentage
    Shape = random.choice(shapes)
    NewObj = GameObject(Shape+str(Color),HP,Shape,Color,Opacity)
    NewObj.GenerateReactions(NumActionButtons)
    return NewObj

def RecombineGameObject(p1, p2):
    FinalTrigList = []
    #1/3 weighted towards lower fitness object, 2/3s to higher object. If equal, then 50/50 split.
    shapes = [p1.Shape, p2.Shape, max(p1,p2).Shape]
    Shape = random.choice(shapes)

    #Random HP
    HP = random.choice([p1.HP, p2.HP])

    #Average of the RGB values
    Color = ((p1.Color[0]+p2.Color[0])/2, (p1.Color[1]+p2.Color[1])/2, (p1.Color[2]+p2.Color[2])/2)

    MaxTriggers = len(max(p1,p2).Triggers)

    #Average of Opacity
    Opacity = (p1.Opacity + p2.Opacity)/2

    tmp1 = deepcopy(p1.Triggers)
    tmp2 = deepcopy(p2.Triggers)

    #Finds actions the two objects have in common, and ensures that at least one of the reactions for said action is passed on
    for i in tmp1:
        for j in tmp2:
            if(i == j):
                #1/4 chance of adding both to the trigger list
                if(random.random() < 0.25 and len(FinalTrigList) <= MaxTriggers):
                    FinalTrigList.append(i)
                    FinalTrigList.append(j)
                else:
                    #2/3 chance of using the higher fitness trigger
                    if(random.random() >= 0.33 and len(FinalTrigList) <= MaxTriggers):
                        if(p1 > p2):
                            FinalTrigList.append(i)
                        else:
                            FinalTrigList.append(j)
                    elif(len(FinalTrigList) <= MaxTriggers):
                        if(p1 > p2):
                            FinalTrigList.append(j)
                        else:
                            FinalTrigList.append(i)
                if(i in tmp1):
                    tmp1.remove(i)
                if(j in tmp2):
                    tmp2.remove(j)

    #fitness proportional selection from remainder of triggers, up to value in range [0, MaxTriggers]
    fm = float(p1.Fitness + p2.Fitness)
    if(fm == 0):
        fm = 0.5
    NumIterations = random.randint(0, MaxTriggers)
    while(len(FinalTrigList) < NumIterations):
        if(random.random() <= p1.Fitness/fm and len(tmp1) != 0):
            a = random.choice(tmp1)
            FinalTrigList.append(a)
            tmp1.remove(a)
        elif(len(tmp2) != 0):
            a = random.choice(tmp2)
            FinalTrigList.append(a)
            tmp2.remove(a)
        else:
            break

    childObj = GameObject(Shape+str(Color),HP,Shape,Color,Opacity)
    childObj.Triggers = FinalTrigList

    return childObj


def RecombineGame(p1, p2):
    tmpObjList = []
    fm = float(p1.Fitness + p2.Fitness)
    if(fm == 0):
        fm = 0.5
    #Fitness Proportional Selection
    if(random.random() <= p1.Fitness/fm):
        NumObj = p1.NumObj
    else:
        NumObj = p2.NumObj

    #All equal to the highest fitness value
    NumActionButtons = max(p1,p2).NumActionButtons
    OffScreenEffect = max(p1,p2).OffScreenEffect
    Score = max(p1,p2).Score

    for i in range(NumObj):
        #Parental Selection is k-tournament, with k = 3
        tmp1 = kTournament(p1.ObjectList,3)
        tmp2 = kTournament(p2.ObjectList,3)
        #Coordinates are average of old coordinates
        NewObj = [RecombineGameObject(tmp1[0],tmp2[0]), ((tmp1[1][0]+tmp2[1][0])/2, (tmp1[1][1]+tmp2[1][1])/2)]
        tmpObjList.append(NewObj)

    return Game(OffScreenEffect, NumActionButtons, Score, tmpObjList, NumObj)

#Simple k-tournament used for selection of [object, (coordinate)] pairs
def kTournament(objList, k):
    best = False
    for i in range(k):
        choice = random.choice(objList)
        if(best != False):
            if(choice[0] > best[0]):
                best = choice
        else:
            best = choice
    return best

def GameTournament(pop, k):
    best = False
    for i in range(k):
        choice = random.choice(pop)
        if(best != False):
            if(choice > best):
                best = choice
        else:
            best = choice
    return best

#Going to be replaced with code sending this to the Website
#For now it just randomly assigns Fitness values
#Allows us to test if the EA code actually works
def EvaluatePopulation(pop):
    for i in pop:
        i.Fitness = random.randrange(0,10)
        for j in i.ObjectList:
            j[0].Fitness = random.randrange(0,10)
    return pop

def EVOLVE_OR_DIE(Pop_Size, Gen_size, NumEvals, Score, OffScreenEffect, NumObjects, MaxX, MaxY, HP):
    pop = InitializePopulation(Pop_Size, Score, OffScreenEffect, NumObjects, MaxX, MaxY, HP)
    pop = EvaluatePopulation(pop)

    for i in range(0, NumEvals, Gen_size):
        survive = []
        for j in range(0, Gen_size):
            p1 = GameTournament(pop,3)
            p2 = GameTournament(pop,3)
            pop.append(RecombineGame(p1,p2))
            pop = EvaluatePopulation(pop)
        for k in range(0, Gen_size):
            p = GameTournament(pop,3)
            survive.append(p)
            pop.remove(p)
        for l in range(0, Gen_size):
            tmp = random.choice(pop)
            pop.remove(tmp)
        pop += survive
    return pop

def dumper(obj):
    return obj.__dict__

def ToJson(CurrentGame):
    with open("JsonTest.txt", "w+") as myfile:
        json.dump(CurrentGame,myfile,default=dumper,indent=4)

def main():
    pop = EVOLVE_OR_DIE(15, 3, 30, 0, None, 5, 100, 100, 1)
    pop.sort()

    ToJson(pop[0])

if __name__ == '__main__':
    main()
