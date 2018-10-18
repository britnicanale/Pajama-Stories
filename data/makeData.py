#makes db file from scratch for testing purposes
import sqlite3

DB_FILE="bigData.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()
#create users
command = "CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE,password_hash TEXT);"
c.execute(command)
#creat contributions
command = "CREATE TABLE contributions(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,story_id INTEGER,body TEXT);"
c.execute(command)
#create stories
command = "CREATE TABLE stories(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT);"
c.execute(command)
db.commit()
db.close()
