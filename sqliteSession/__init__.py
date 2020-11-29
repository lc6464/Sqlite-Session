from sqliteSession.sql import Session
import sqlite3

def GetSession(database_name):
	er = Session(sqlite3.connect(database_name, check_same_thread=False))
	er.execute('create table if not exists Session (Session char(36) unique not null, User varchar(64) unique not null, Value BLOB not null)')
	er.commit()
	return er