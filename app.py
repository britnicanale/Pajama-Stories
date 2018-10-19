#PJ Cubed -- Jiayang Chen, Jabir Chowdhury, Peter Cwalina, Jason Lin
#SoftDev1 pd07
#P00 -- Da Art of Storytellin'
#2018-10-17

from flask import Flask,render_template,request,session,url_for,redirect,flash
from util import dbCommands as db
import os
import sqlite3
app = Flask(__name__) # instantiates an instance of Flask

app.secret_key = os.urandom(32)
user_data = db.getAllUserData()

def isLoggedIn():
    return "id" in session

@app.route("/") #Linking a function to a route
def login():
    if(isLoggedIn()):
        return render_template("story_contributed.html", additions = [("the duck goes woof","dennis"),("the dog goes meow", "jason"), ("the cat goes quack","kenny")])
    else:
        return render_template("login.html")

@app.route("/auth" , methods = ["POST"])
def authenticate():
    username_input = request.form.get("username")
    password_input = request.form.get("password")
    if username_input in user_data:
        if user_data[username_input]  == password_input:
            id = db.getUserId(username_input)
            session["id"] = id
        else:
            flash("Invalid password, try again!")
    else:
        flash("Invalid username, try again!")
    return redirect(url_for('login'))

@app.route("/logout", methods=["GET"])
def logOut():
    session.pop("id")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.debug = True
    app.run()
