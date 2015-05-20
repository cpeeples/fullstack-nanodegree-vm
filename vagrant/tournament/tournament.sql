-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE TABLE players (playerid SERIAL NOT NULL PRIMARY KEY, name VARCHAR(26),matchwins INT, matchlosses INT);
CREATE TABLE matches (matchid INT, play1 INTEGER REFERENCES players(playerid), play2 INTEGER REFERENCES players(playerid));


