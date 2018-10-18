#PJ Cubed -- Jiayang Chen, Jabir Chowdhury, Peter Cwalina, Jason Lin
#SoftDev1 pd07
#P00 -- Da Art of Storytellin'
#2018-10-17

from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__) # instantiates an instance of Flask

DB_FILE="data/bigData.db"

db = sqlite3.connect(DB_FILE)
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

@app.route("/") #Linking a function to a route
def home():
    return render_template("story_contributed.html", additions = [("the duck goes woof","dennis"),("the dog goes meow", "jason"), ("the cat goes quack","kenny")])

if __name__ == "__main__":
    app.debug = True
    app.run()
