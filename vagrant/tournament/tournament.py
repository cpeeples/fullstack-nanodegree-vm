#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    try:
		conn=psycopg2.connect(database="tournament")
    except:
        raise ValueError("I can't connect!")
	"""Connect to the PostgreSQL database.  Returns a database connection."""
    return conn


def deleteMatches():
	conn=connect()
	sql="DELETE from matches;"
	cur=conn.cursor()
	cur.execute(sql)
	conn.commit()
	conn.close()
	"""Remove all the match records from the database."""


def deletePlayers():
#    """Remove all the player records from the database."""
    conn=connect()
    cur=conn.cursor()
    sql="DELETE from players;"
    cur.execute(sql)
    conn.commit()
    conn.close()


def countPlayers():
#   """Returns the number of players currently registered."""
    conn=connect()
    cur=conn.cursor()
    sql="SELECT count(playerid) from players;"
    cur.execute(sql)
    val=cur.fetchone()
    conn.close()
    return val[0]


def registerPlayer(name):
    name=name.replace("'",r"''")
    conn=connect()
    cur=conn.cursor()
    sql="INSERT INTO players(name,matchwins,matchlosses) VALUES(\'%s\',0,0);" % name
    cur.execute(sql)
    conn.commit()
    conn.close()
    """Adds a player to the tournament database.
    
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args: name: the player's full name (need not be unique).
    """
	

def playerStandings():
    conn=connect()
    sql="SELECT playerid, name, matchwins, matchlosses from players order by (matchwins,name) DESC;"
    cur=conn.cursor()
    cur.execute(sql)
    standings=cur.fetchall()
    conn.close()
    return standings
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """


def reportMatch(winner, loser):
    conn=connect()
    cur=conn.cursor()
    sqlsel="SELECT playerid,matchwins,matchlosses from players where playerid=%i;" %winner
    cur.execute(sqlsel)
    (winid,winnerwins,winnermatches)=cur.fetchone()
    sqlsel="SELECT playerid,matchwins,matchlosses from players where playerid=%i;" %loser
    cur.execute(sqlsel)
    (loseid,loserwins,losermatches)=cur.fetchone()
    sqlins="UPDATE players SET matchwins=%i ,matchlosses=%i WHERE playerid=(%i);" % (winnerwins+1,winnermatches+1,winner)
    cur.execute(sqlins)
    sqlins="UPDATE players SET matchwins=%i ,matchlosses=%i WHERE playerid=(%i);" % (loserwins,losermatches+1,loser)
    cur.execute(sqlins)
    conn.commit()
    conn.close()
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
 
 
def swissPairings():
    standings=playerStandings()
    pairs=[]
    p1=None
    n1=None
    for player in standings:
        if p1==None and n1==None:
            p1=player[0]
            n1=player[1]
        else:
            p2=player[0]
            n2=player[1]
            pairs.append((p1,n1,p2,n2))
            p1=None
            n1=None
    return(pairs)
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """


