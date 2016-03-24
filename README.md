# FSND_P2_swiss_style

This package will create and maintain a PostgreSQL database to track a Swiss-Style tournament. 
For more info on Swiss-Style tournaments look here: https://www.wikipedia.org/en/Swiss-system_tournament

To use, ensure that you have python 2.7 and psql install on your local machine. Additionally this package
requires the below python packages:
   bleach
   psycopg2

1. From CLI, cd to the directory where you downloaded the package and type the following command to 
initize the PostgreSQL database entitled tournament.  The database will have 2 tables (players, matches) 
with the views (match_record, player_records) for ease of access:

   ==> psql \i tournament.sql
   
2. From a python interpreter, import tournament.py to access the following database functions:

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


