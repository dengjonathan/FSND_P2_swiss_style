-- Creates database schema and views for the tournament project.
-- Delete any existing databases name 'tournament' if they exist
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE event (tournament_id text primary key);

CREATE TABLE players (player_name text,
                      player_id serial PRIMARY KEY);


CREATE TABLE matches (match_id serial PRIMARY KEY,
                    winning_player_id integer REFERENCES players(player_id),
                    losing_player_id integer REFERENCES players(player_id));


CREATE VIEW wins AS
SELECT players.player_id,
       count(matches.winning_player_id) AS wins
FROM players
LEFT JOIN matches ON players.player_id = matches.winning_player_id
GROUP BY players.player_id
ORDER BY wins DESC;


CREATE VIEW losses AS
SELECT players.player_id,
       count(matches.losing_player_id) AS losses
FROM players
LEFT JOIN matches ON players.player_id = matches.losing_player_id
GROUP BY players.player_id
ORDER BY losses DESC;

--creates view using views (wins, losses) to show entire match history by player

CREATE VIEW match_record AS
SELECT wins.player_id AS player_id,
       wins.wins AS wins,
       losses.losses AS losses,
       (wins + losses) AS total
FROM wins,
     losses
WHERE wins.player_id = losses.player_id
ORDER BY total DESC;

--adds to match_record view by adding player's name and implements
--Opponent Match Wins column where ties in number of wins
--are decided by by total wins by defeated opponents (OMW), as long as
--those wins did not come from a bye round.


CREATE VIEW player_records AS
SELECT players.player_id AS player_id,
       players.player_name AS player_name,
       match_record.wins AS wins,
       match_record.losses AS losses,
       match_record.total AS total_matches,

      (SELECT sum(wins)
       FROM match_record
       WHERE player_id IN
           (SELECT losing_player_id
            FROM matches
            WHERE winning_player_id = players.player_id
                  and winning_player_id != losing_player_id)) AS omw

FROM players
LEFT JOIN match_record ON players.player_id = match_record.player_id
ORDER BY wins DESC,
         omw DESC;
