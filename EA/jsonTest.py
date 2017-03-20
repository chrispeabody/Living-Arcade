#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Josh
#
# Created:     19/03/2017
# Copyright:   (c) Josh 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import random, json
from GameObjects import *

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

def dumper(obj):
    return obj.__dict__

def ToJson(CurrentGame):
    return json.dumps(CurrentGame,default=dumper,indent=4)

def main():
    pop = InitializePopulation(10,0,None,3,10,10,1)
    with open("jsonTest.txt", "w+") as myfile:
        myfile.write(ToJson(pop[0]))
        myfile.write(ToJson(pop[0].ObjectList[0]))

if __name__ == '__main__':
    main()
