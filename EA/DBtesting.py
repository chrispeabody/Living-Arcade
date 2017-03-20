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
##    #adding new ones
##    cursor.execute("insert into Games(gameID, gameJSON, gameFitness) values (?, ?, ?)", newObj.ID, toJSON(newObj), newObj.Fitness)
##    cnxn.commit()
##
##    #deleting old
##    for row in cursor.execute("select gameID"):
##        if row[0] not in gameObjList:
##            cursor.execute("delete from Games where gameID =?",row[0])
##            cursor.execute("delete from gameObjects where parentID=?",row[0])
##    cnxn.commit()

    cnxn = pyodbc.connect('DRIVER={MySQL ODBC 5.3 Unicode Driver};Server=149.56.28.102;port=3306;Database=LivingArcade;user=theUser;password=newPass!!!123')
    cursor = cnxn.cursor()
    flag = cursor.execute("select gameFitness from Games where gameID='Flag'").fetchone()[0]
    print(flag)
    if(flag):
        print("X")









if __name__ == '__main__':
    main()
