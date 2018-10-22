import sqlite3

db = sqlite3.connect("data/bigData.db")
c = db.cursor()
#create users
command = "CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE,password_hash TEXT)"
c.execute(command)
#creat contributions
command = "CREATE TABLE contributions(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,story_id INTEGER,body TEXT)"
c.execute(command)
#create stories
command = "CREATE TABLE stories(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT)"
c.execute(command)
db.commit()
db.close()
