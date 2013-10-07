#!/usr/bin/python3
#Author: Emmanuel Odeke <odeke@ualberta.ca>

songTableCreation = \
    "CREATE TABLE song( \
	id integer AUTO_INCREMENT not null,\
	title text not null, \
	artist text,\
	url text, \
	primary key (id),\
	check (id > 0) \
    );"

playTimeTableCreation = \
    "CREATE TABLE playTime( \
	id integer AUTO_INCREMENT not null,\
	pTime text not null, \
	song_id int not null, \
	primary key (id),\
	foreign key (song_id) references song(id), \
	check (id > 0)\
    );"

creationTablesTuple = (songTableCreation, playTimeTableCreation)
