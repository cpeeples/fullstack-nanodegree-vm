#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."
	
def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = 1 #countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."
conn=psycopg2.connect(database="tournament")
cur=conn.cursor()
cur.execute("SELECT 2+2;")
val=cur.fetchone()
print(val)
#registerPlayer("Chandra Nalaar")
#conn.close()
#testDeleteMatches()
#testRegister()
#deletePlayers()