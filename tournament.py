#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2
import bleach


def sanitizeInputs(input):
    """Sanitizes inputs for scripts and apostrophes"""
    input = bleach.clean(input)
    i = 0
    bad_apos = []
    for i in range(len(input)):
        if input[i] == "'":
            bad_apos.append(i)
    for i in bad_apos:
        input = input[:i] + "'" + input[i:]
    return input


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():

    """Remove all the match records from the database."""
    DB = connect()
    DB.cursor().execute(
        'DELETE FROM matches;'
        )
    DB.commit()
    print 'All match records deleted in SQL database'
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    DB.cursor().execute(
        'DELETE FROM players;'
        )
    DB.commit()
    print 'All player records deleted in SQL database'
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute(
        'SELECT COUNT(*) FROM players;'
        )
    numPlayers = c.fetchone()[0]
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
    name = sanitizeInputs(name)
    DB = connect()
    c = DB.cursor()
    # issue how to execute sql command for names with apostrophes i.e. O'Neal
    c.execute(
        "INSERT INTO players (player_name) VALUES ('{}');".format(name)
        )
    DB.commit()
    # possible bug where this execute statement will select another player with
    # the same player_name as the recently inserted player, and will return
    # the wrong id
    c.execute(
        "SELECT player_id FROM players WHERE player_name = '{}';".format(name)
        )
    player_id = c.fetchone()[0]
    output = (
        'Player {} has been inserted '
        'and his Player ID is {}').format(name, player_id)
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
    DB = connect()
    c = DB.cursor()
    c.execute(
      "SELECT player_id, player_name, wins, total_matches FROM player_records;"
             )
    for row in c.fetchall():
        l.append(row)
    DB.close()
    return l


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute(
            ("INSERT INTO matches (winning_player_id, losing_player_id)"
             "VALUES ('{}', '{}');").format(winner, loser)
        )
    DB.commit()

    print ("A match was recorded"
           "with winner {} and loser {}").format(winner, loser)
    DB.close()


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
    DB = connect()
    c = DB.cursor()
    c.execute("select player_id, player_name from player_records")
    rows = c.fetchall()
    DB.close()
    players_matched = []
    for i in range(0, len(rows), 2):
        players_matched.append((rows[i][0], rows[i][1],
                                rows[i+1][0], rows[i+1][1]))
    return players_matched
