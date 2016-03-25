# FSND_P2_swiss_style

This package will create and maintain a PostgreSQL database to track a Swiss-Style tournament.
For more info on Swiss-Style tournaments look here: https://en.wikipedia.org/wiki/Swiss-system_tournament


To use, ensure that you have python 2.7 and psql install on your local machine. Additionally this package requires the python package psycopg2: https://github.com/psycopg/psycopg2

1. To run from CLI, use the below commands. The first command will create a database will have 2 tables (players, matches) along with a few views for ease of access:

   ==> psql -f <path>/tournament.sql
   ==> python <path>/tournament_test.py

2. To use for your own Swiss-Style tournament, import the module tournament.py,which includes the below functions to maintain and update your tournament database.

   connect -- Meant to connect to the database 'tournament' created by the tournament.sql shell command

   deleteMatches -- Remove all the matches records from the database.

   deletePlayers -- Remove all the player records from the database.

   countPlayers -- Returns the number of players currently registered

   registerPlayer -- Adds a player to the tournament database.

   playerStandings -- Returns a list of the players and their win records, sorted by wins.
                  You can use the player standings table created in your .sql file for reference.

   reportMatch -- This is to simply populate the matches table and record the winner and loser as (winner,loser) in the                      insert statement.

   swissPairings -- Returns a list of pairs of players for the next round of a match in the form of tuples
                   (id1, name1, id2, name2) for each match.

###Implementation Details###
The package was implemented with the following features, which may prove useful:

1. Semi-random Byes: if there are an odd number of players in the tournament, tournament.py will choose a player at random each round to be given a bye.  This player will receive a win added to their record.  Once a player has a bye, they will not be eligible for a bye for the rest of the tournament.  Each player can only have one bye in the tournament, at most.

testPairingsOdd in tournament_test.py will test the database's performance in odd-numbered player scenarios.

2. Opponent Match Wins (OMW): currently, the tournament is structure so that ranking is based on the raw number of wins.  For example if player A has 4 wins, and player B has 3 wins, player A is ranked ahead of player B, regardless of how many matches either player has played.

In the event of a tie, players are then ranked by Opponent Match Wins (OMW), the sum of wins by their defeated opponents won.

For example, if player A beat the below 3 players, player A's OMW would be 3:
  player C: 1 win
  player D: 0 wins
  player E: 2 wins

Wins from byes are not counted as part of OMW.
