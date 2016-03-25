#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2
import random
import time


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        DB = psycopg2.connect("dbname=tournament")
        cursor = DB.cursor()
        return DB, cursor
    except:
        print 'There was a error connecting to PostgreSQL database. \
        Please check to ensure that you have run the tournament.sql \
        file to initialize the database.'


def deleteMatches():
    """Remove all the match records from the database."""
    DB, cursor = connect()
    cursor.execute(
        'TRUNCATE matches;'
    )
    DB.commit()
    print 'All match records deleted in SQL database'
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB, cursor = connect()
    cursor.execute(
        'TRUNCATE players CASCADE;'
    )
    print 'WARNING! Deleting player records will also delete match records'
    print 'You have 2 seconds to press CTRL-C to cancel function'
    #time.sleep(2)
    DB.commit()
    print 'All player and match records deleted in SQL database'
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB, cursor = connect()
    cursor.execute(
        'SELECT COUNT(*) FROM players;'
    )
    numPlayers = cursor.fetchone()[0]
    print 'There are a total of {} players'.format(numPlayers)
    DB.close()
    return numPlayers


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    name = (name, )
    insert_query = "INSERT INTO players (player_name) VALUES (%s);"
    DB, cursor = connect()
    cursor.execute(insert_query, name)
    DB.commit()
    lookup_query = "SELECT player_id FROM players WHERE player_name = %s;"
    cursor.execute(lookup_query, name)
    player_id = cursor.fetchone()[0]
    output = (
        'Player {} has been inserted '
        'and his Player ID is {}').format(name[0], player_id)
    print output
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tupls, each of which con
tains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    l = []
    DB, cursor = connect()
    cursor.execute(
        "SELECT player_id, player_name, wins, total_matches FROM player_records;"
    )
    for row in cursor.fetchall():
        l.append(row)
    DB.close()
    return l


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    winner, loser = (winner, ), (loser, )
    query = ("INSERT INTO matches (winning_player_id, losing_player_id)"
             "VALUES (%s, %s);")
    DB, cursor = connect()
    cursor.execute(query, (winner, loser))
    DB.commit()
    print "Match recorded with winner %s and loser %s" % (winner, loser)
    DB.close()

BYE_PLAYERS = []

def give_bye(players):
    """Returns an even number of players and gives the odd man out a bye.

    Takes a list with an odd number of tuples of type (player_id, player_name)
    and returns an even number, with id of bye player added to the list
    BYE_PLAYERS and inputs a victory for bye player with opponent 00000 to
    signify a BYE.

    The odd player out is chosen by a random uniform distribution, however,
    each player can only be given one bye per tournament.
    """
    odd_man_out = None
    while True:
        index = random.randint(0, len(players))
        odd_man_out = players[index][0]
        if odd_man_out not in BYE_PLAYERS:
            BYE_PLAYERS.append(odd_man_out)
            break
    DB, cursor = connect()
    cursor.execute(
        "INSERT INTO players (player_name, player_id) VALUES ('_BYE_', 99999))"
                  )
    cursor.execute(
        'UPDATE *'
    )
    reportMatch(odd_man_out, 99999)
    del players[index]
    return players


def swissPairings():
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
    DB, cursor = connect()
    cursor.execute("select player_id, player_name from player_records")
    rows = cursor.fetchall()
    DB.close()
    if len(rows) % 2 != 0:
        rows = give_bye(rows)
    # zip into tuples of form ((p1_id, p1_name), (p2_id, p2_name))
    players_zipped = zip(rows[0::2], rows[1::2])
    # transform into form (p1_id, p1_name, p2_id, p2_name)
    players_matched = []
    for i in players_zipped:
        players_matched.append(i[0] + i[1])
    return players_matched
