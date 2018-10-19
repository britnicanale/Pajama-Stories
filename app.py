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
        #index to 0th because that is the id
        contributed_data = db.getUserContribution(session["id"]);
        list_contr_story_id = []
        for tuple in contributed_data:
            list_contr_story_id.append(tuple[0])
        allStories = db.getAllStories()
        title_list = []
        non_title_list = []
        for story_id in list_contr_story_id:
            title_list.append(db.getTitle(story_id))
        for story_id in allStories:
            if story_id[0] not in list_contr_story_id:
                non_title_list.append(db.getTitle(story_id[0]))
        return render_template("homepage.html", titles = title_list, non_titles = non_title_list)
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
