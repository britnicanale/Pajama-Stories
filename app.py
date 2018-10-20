#PJ Cubed -- Jiayang Chen, Jabir Chowdhury, Peter Cwalina, Jason Lin
#SoftDev1 pd07
#P00 -- Da Art of Storytellin'
#2018-10-17

from flask import Flask, render_template, request, session, url_for, redirect, flash
from util import dbCommands as db
import os,sys
import sqlite3

app = Flask(__name__) # instantiates an instance of Flask

app.secret_key = os.urandom(32)
user_data = db.get_all_user_data()

def is_logged_in():
    return "id" in session

@app.route("/") #Root
def login():
    if(is_logged_in()):
        contributed_data = db.get_user_contribution(session["id"]);
        list_contr_story_id = [x[0] for x in contributed_data] # x[0] is the story id
        allStories = db.get_all_stories() # List of all the stories (id)
        print(list_contr_story_id, file=sys.stderr)
        contr_title_list = [db.get_title(str(story_id)) for story_id in list_contr_story_id] # List of all contributed-to story titles
        uncontr_title_list = [db.get_title(str(story_id[0])) for story_id in allStories if story_id not in list_contr_story_id] # List of all uncontributed-to story titles
        return render_template("homepage.html", titles = contr_title_list, non_titles = uncontr_title_list)
    else:
        return render_template("login.html")

@app.route("/auth" , methods = ["POST"])
def authenticate():
    username_input = request.form.get("username")
    password_input = request.form.get("password")
    #Checks if user/pass is valid if not flash reasons why
    if username_input in user_data:
        if user_data[username_input]  == password_input:
            id = db.get_user_id(username_input)
            session["id"] = id
        else:
            flash("Invalid password, try again!")
    else:
        flash("Invalid username, try again!")
    return redirect(url_for('login'))

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("id")
    return redirect(url_for("login"))

@app.route("/story/<int:story_id>")
def view_story(story_id):
    if not is_logged_in():
        return redirect(url_for("login"))
    #If story is not in the list of all stories
    if story_id not in [i[0] for i in db.get_all_stories()]:
        return render_template("story_unfound.html")
    additions = db.get_story_body(story_id) #List of all user additions to specific story
    users = [user[0] for user in additions] #List of all users who made the additions
    if session["id"] in users:
        return render_template("story_contributed.html", story_id = story_id, story_body = additions)
    return render_template("story_uncontributed.html", story_id = story_id, story_body = additions)

@app.route("/story/<int:story_id>/add", methods = ["POST"])
def add_contribution(story_id):
    if not is_logged_in():
        return redirect(url_for("login"))

    db.add_contribution(session["id"], story_id, request.form.get("addition")) #Adds into specific story table: (usr_id, story_id, body of text)
    flash("Successfully added to the story!")
    return redirect(url_for("view_story", story_id = story_id))



if __name__ == "__main__":
    app.debug = True
    app.run()
