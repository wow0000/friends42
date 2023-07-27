/*
 OLD
 CREATE TABLE IF NOT EXISTS USERS
(
	id           INTEGER PRIMARY KEY,
	name         VARCHAR(12) UNIQUE,
	image        VARCHAR(100),
	image_medium VARCHAR(100),
	pool         VARCHAR(100),
	lang         VARCHAR(3),
	privacy      INTEGER   DEFAULT 0, // DELETE
	active       TIMESTAMP DEFAULT 0,
	ban          INTEGER   DEFAULT 0 // DELETE
);
 NEW
 CREATE TABLE IF NOT EXISTS USERS
(
	id           INTEGER PRIMARY KEY,
	name         VARCHAR(12) UNIQUE,
	image        VARCHAR(100),
	image_medium VARCHAR(100),
	pool         VARCHAR(100),
	lang         VARCHAR(3) DEFAULT 'fr',
	active       TIMESTAMP DEFAULT 0,
	campus		 INTEGER DEFAULT 1 // APPEND
);
*/

ALTER TABLE USERS DROP COLUMN privacy;
ALTER TABLE USERS DROP COLUMN ban;
ALTER TABLE USERS ADD COLUMN campus INTEGER DEFAULT 1;