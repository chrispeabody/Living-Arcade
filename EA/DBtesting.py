#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Josh
#
# Created:     14/03/2017
# Copyright:   (c) Josh 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pyodbc

def show_odbc_sources():
	sources = pyodbc.dataSources()
	dsns = sources.keys()
	sl = []
	for dsn in dsns:
		sl.append('%s [%s]' % (dsn, sources[dsn]))
	print('\n'.join(sl))

def main():
##    #show_odbc_sources()
##    cnxn = pyodbc.connect('DRIVER={MySQL ODBC 5.3 Unicode Driver};Server=149.56.28.102;port=3306;Database=LivingArcade;user=theUser;password=newPass!!!123')
##    cursor = cnxn.cursor()
##
##
##    #Updating existing objects
##    for row in cursor.execute("select gameID, gameFitness from Game"):
##        for i in gameObjList:
##            if(i.ID == row.gameID):
##                i.SetFitness(row.gameFitness)
##    for row in cursor.execute("select objId, parentID, objFitness from gameObjects"):
##        for i in gameObjList:
##            if(i.ID == row.parentID):
##                for j in i.objList:
##                    if(j.Name == row.objID):
##                        j.Fitness = row.objFitness
##
##
##
##
##
##    #deleting old
##    for row in cursor.execute("select gameID"):
##        if row[0] not in gameObjList:
##            cursor.execute("delete from Games where gameID =?",row[0])
##            cursor.execute("delete from gameObjects where parentID=?",row[0])
##    cnxn.commit()


##    #uploading a new object to the database.
##    cnxn = pyodbc.connect('DRIVER={MySQL ODBC 5.3 Unicode Driver};Server=149.56.28.102;port=3306;Database=LivingArcade;user=theUser;password=newPass!!!123')
##    cursor = cnxn.cursor()
##    for newObj in population:
##         cursor.execute("insert into Games(gameID, gameJSON, gameFitness) values (?, ?, ?)", newObj.ID, ToJson(newObj), newObj.Fitness)
##         counter = 1
##         for j in newObj.ObjectList:
##            i = j[0]
##            cursor.execute("insert into gameObjects(objID, objJSON, objFitness, parentID) values (?, ?, ?, ?)", i.Name, ToJson(i), i.Fitness, newObj.ID)
##            cursor.execute("update Games set obj"+str(counter)+"ID=? where gameID=?", i.Name, newObj.ID)
##    cnxn.commit()

    cnxn = pyodbc.connect('DRIVER={MySQL ODBC 5.3 Unicode Driver};Server=149.56.28.102;port=3306;Database=LivingArcade;user=theUser;password=newPass!!!123')
    cursor = cnxn.cursor()
    flag = cursor.execute("select gameFitness from Games where gameID='Flag'").fetchone()[0]
    print(flag)
    if(flag):
        print("X")









if __name__ == '__main__':
    main()
