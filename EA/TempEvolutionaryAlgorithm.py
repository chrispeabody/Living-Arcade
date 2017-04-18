from GameObjects import *
import random, json, pyodbc
from copy import deepcopy

cfgfile = "namelists.cfg"

def InitializePopulation(Pop_Size, Score, NumObjects, MaxX, MaxY, HP):
    population = []
    OffScreenEffects = ["Destroy", "Warp", "Bounce", "Stop"]

    for i in range(Pop_Size):
        log = []
        #Pick the number of used buttons, and initialize GameObject
        NumActionButtons = random.randint(2,4)


        #Initialize all of the GameObjects and properties
        for j in range(NumObjects-1):
            NewLog = [GenerateGameObj(NumActionButtons, HP), (random.randint(0,MaxX),random.randint(0,MaxY))]
            log.append(NewLog)
        Player = [GenerateGameObj(NumActionButtons, HP), (random.randint(0,MaxX),random.randint(0,MaxY))] #Using generic methods to generate the player. Need to decide on what specific methods we want later.
        Player[0].Name = getName(cfgFile)
        log.append(Player)

        #Quick and dirty way to randomly generate the regions the player can spawn in, with no duplicates
        PlayerSpawns = []
        for j in range(random.randint(1,12)):
            tmp = random.randint(1,12)
            if(tmp not in PlayerSpawns):
                PlayerSpawns.append(tmp)

        OffScreenEffect = random.choice(OffScreenEffects)

        NewGame = Game(OffScreenEffect, NumActionButtons, Score, log, NumObjects, PlayerSpawns, Player)

        #Put all the information together, and insert into the Population
        population.append(NewGame)

    for i in population:
        for j in i.ObjectList:
            j.UpdateTriggers(i.ObjectList)

    cnxn = pyodbc.connect('DRIVER={MySQL ODBC 5.3 Unicode Driver};Server=149.56.28.102;port=3306;Database=LivingArcade;user=theUser;password=newPass!!!123')
    cursor = cnxn.cursor()
    for newObj in population:
         cursor.execute("insert into Games(gameID, gameJSON, gameFitness) values (?, ?, ?)", newObj.ID, ToJson(newObj), newObj.Fitness)
         counter = 1
         for j in newObj.ObjectList:
            i = j[0]
            cursor.execute("insert into gameObjects(objID, objJSON, objFitness, parentID) values (?, ?, ?, ?)", i.Name, ToJson(i), i.Fitness, newObj.ID)
            cursor.execute("update Games set obj"+str(counter)+"ID=? where gameID=?", i.Name, newObj.ID)
    cnxn.commit()

    return population

def GenerateGameObj(NumActionButtons, HP):
    shapes = ["Square","Circle","Triangle","Pentagon","Hexagon","Octagon"]
    Color = (random.randint(0,255),random.randint(0,255),random.randint(0,255)) #(R, G, B)
    Opacity = random.uniform(0,100) #Opacity Percentage
    Shape = random.choice(shapes)
    #Need to figure out what we want to do with this!
    MinSpawns = [0,0,0,0,0,0,0,0,0,0,0,0]
    #Right now, the max is just a random number between 0 and 5
    MaxSpawns = []
    for i in range(12):
        MaxSpawns.append(random.randint(0,5))
    NewObj = GameObject(Shape+str(Color),HP,Shape,Color,Opacity,MinSpawns,MaxSpawns)
    NewObj.GenerateReactions(NumActionButtons)
    return NewObj

def RecombineGameObject(p1, p2):
    FinalTrigList = []
    #1/3 weighted towards lower fitness object, 2/3s to higher object. If equal, then 50/50 split.
    shapes = [p1.Shape, p2.Shape, max(p1,p2).Shape]
    Shape = random.choice(shapes)

    #Random HP
    HP = random.choice([p1.HP, p2.HP])

    #Max and Min spawns simply takes the one from the greater parent
    MinSpawns = max(p1,p2).MinSpawns
    MaxSpawns = max(p1,p2).MaxSpawns


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

    childObj = GameObject(Shape+str(Color),HP,Shape,Color,Opacity,MinSpawns,MaxSpawns)
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


    newObj = Game(OffScreenEffect, NumActionButtons, Score, tmpObjList, NumObj)
    cnxn = pyodbc.connect('DRIVER={MySQL ODBC 5.3 Unicode Driver};Server=149.56.28.102;port=3306;Database=LivingArcade;user=theUser;password=newPass!!!123')
    cursor = cnxn.cursor()
    cursor.execute("insert into Games(gameID, gameJSON, gameFitness) values (?, ?, ?)", newObj.ID, toJSON(newObj), newObj.Fitness)
    counter = 1
    for i in newObj.objList:
        cursor.execute("insert into gameObjects(objID, objJSON, objFitness) values (?, ?, ?)", i.Name, toJSON(i), i.Fitness, newObj.ID)
        cursor.execute("update Games set obj"+counter+"ID=? where gameID=?", i.Name, newObj.ID)
    cnxn.commit()
    return newObj

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
    cnxn = pyodbc.connect('DRIVER={MySQL ODBC 5.3 Unicode Driver};Server=149.56.28.102;port=3306;Database=LivingArcade;user=theUser;password=newPass!!!123')
    cursor = cnxn.cursor()
    #Updating existing objects
    for row in cursor.execute("select gameID, gameFitness from Game"):
        for i in pop:
            if(i.ID == row.gameID):
                i.SetFitness(row.gameFitness)
    for row in cursor.execute("select objId, parentID, objFitness from gameObjects"):
        for i in pop:
            if(i.ID == row.parentID):
                for j in i.objList:
                    if(j.Name == row.objID):
                        j.Fitness = row.objFitness
    return pop

def EVOLVE_OR_DIE(Pop_Size, Gen_size, NumEvals, Score, NumObjects, MaxX, MaxY, HP):
    pop = InitializePopulation(Pop_Size, Score, NumObjects, MaxX, MaxY, HP)
    pop = EvaluatePopulation(pop)
    cnxn = pyodbc.connect('DRIVER={MySQL ODBC 5.3 Unicode Driver};Server=149.56.28.102;port=3306;Database=LivingArcade;user=theUser;password=newPass!!!123')
    cursor = cnxn.cursor()

    while True:
        survive = []
        #Constantly queries the database to see if the Flag has been set by the frontend
        #If it has, go to the next generation, else wait.
        flag = cursor.execute("select gameFitness from Games where gameID='Flag'").fetchone()[0]

        if(flag):
            #resets the flag
            cursor.execute("update Games set gameFitness=0 where gameID='Flag'")
            for m in range(0, Gen_size):
                p1 = GameTournament(pop,3)
                p2 = GameTournament(pop,3)
                pop.append(RecombineGame(p1,p2))
                #Need some trigger to start this!
                #Otherwise it'll be looping forever.
                #Possibly a flag within the database itself?
                for i in pop:
                    for j in i.ObjectList:
                        j.UpdateTriggers(i.ObjectList)
                pop = EvaluatePopulation(pop)
            for k in range(0, Gen_size):
                p = GameTournament(pop,3)
                survive.append(p)
                pop.remove(p)
            for l in range(0, Gen_size):
                tmp = random.choice(pop)
                pop.remove(tmp)
            pop += survive
    MySQLDelete()
    return pop

def MySQLDelete():
    cnxn = pyodbc.connect('DRIVER={MySQL ODBC 5.3 Unicode Driver};Server=149.56.28.102;port=3306;Database=LivingArcade;user=theUser;password=newPass!!!123')
    cursor = cnxn.cursor()
    for row in cursor.execute("select gameID"):
        if row[0] not in gameObjList:
            cursor.execute("delete from Games where gameID =?",row[0])
            cursor.execute("delete from gameObjects where parentID=?",row[0])
    cnxn.commit()

def dumper(obj):
    return obj.__dict__

def ToJson(CurrentGame):
    return json.dumps(CurrentGame,default=dumper,indent=4)

def main():
    pop = EVOLVE_OR_DIE(15, 3, 30, 0, 5, 100, 100, 1)
    pop.sort()

    print(ToJson(pop[0]))

def getName(cfgFile):
    seed()
    cfg = file(cfgFile, 'r')
    config = list(cfg)
    for i in range(len(config)):
        config[i] = config[i].replace('\r\n','')
    else:
        print("Error, file not found.")
        sys.exit(0)
    SupStartIndex = config.index("SUPERLATIVES") + 1
    AdjStartIndex = config.index("ADJECTIVES") + 1
    NounStartIndex = config.index("NOUNS") + 1
    NumOfSups = AdjStartIndex - 2 - SupStartIndex
    NumOfAdj = NounStartIndex - 2 - AdjStartIndex
    NumOfNouns = config.index("END") - 2 - NounStartIndex
    SupIndex = SupStartIndex+randint(0, NumOfSups)
    AdjIndex = AdjStartIndex+randint(0, NumOfAdj)
    NounIndex = NounStartIndex+randint(0, NumOfNouns)
    if config[SupIndex] == " ":
        name = config[AdjIndex] + " " + config[NounIndex]
    else:
        name =  config[SupIndex] + " " + config[AdjIndex] + " " + config[NounIndex]
    return name;
    

if __name__ == '__main__':
    main()
