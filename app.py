#PJ Cubed -- Jiayang Chen, Jabir Chowdhury, Peter Cwalina, Jason Lin
#SoftDev1 pd07
#P00 -- Da Art of Storytellin'
#2018-10-17

from flask import Flask, render_template, request, session, url_for, redirect, flash
from util import dbCommands as db
from passlib.hash import md5_crypt
import os
import sqlite3

app = Flask(__name__) # instantiates an instance of Flask

app.secret_key = os.urandom(32)
user_data = db.get_all_user_data()

def is_logged_in():
    return "id" in session

@app.route("/") #Root
def home():
    if(is_logged_in()):
        contributed_data = db.get_user_contribution(session["id"]);
        list_contr_story_id = [x[0] for x in contributed_data] # x[0] is the story id
        allStories = db.get_all_stories() # List of all the stories (id)
        contr_title_list = [(db.get_title(str(story_id)),story_id) for story_id in list_contr_story_id] # List of all contributed-to story titles
        uncontr_title_list = [(db.get_title(str(story_id[0])),story_id[0]) for story_id in allStories if story_id[0] not in list_contr_story_id] # List of all uncontributed-to story titles
        return render_template("homepage.html", titles = contr_title_list, non_titles = uncontr_title_list, user=db.get_username(session["id"]))
    else:
        return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/auth" , methods = ["POST"])
def authenticate():
    user_data = db.get_all_user_data() #for updating user_data when there is a new user
    username_input = request.form.get("username")
    password_input = request.form.get("password")
    #Checks if user/pass is valid if not flash reasons why
    if username_input in user_data:
        #verifies the hashed password with given password
        if md5_crypt.verify(password_input, user_data[username_input]):
            id = db.get_user_id(username_input)
            session["id"] = id
        else:
            flash("Invalid password, try again!")
    else:
        flash("Invalid username, try again!")
    return redirect(url_for('home'))

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("id")
    return redirect(url_for("home"))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/registerAuth", methods = ["POST"])
def reg_auth():
    username_input = request.form.get("username")
    password_input = request.form.get("password")
    password_input2 = request.form.get("password2")
    #checks if there is an user with the same username
    if username_input in user_data:
        flash("Username already exists! Please pick another one!")
        return redirect(url_for("register"))
    #checks if the user typed the same passward twice
    elif len(username_input) < 4:
        flash("Username has to be at least 4 characters!")
        return redirect(url_for("register"))
    elif password_input != password_input2:
        flash("Input Same Password in Both Fields!")
        return redirect(url_for("register"))
    else:
        #adds the user's username and a hashed + salted
        #version of his password to database
        db.add_user(username_input, md5_crypt.encrypt(password_input))
        flash("Successfully Registered, Now Sign In!")
        return redirect(url_for('home'))


@app.route("/story/<int:story_id>")
def view_story(story_id):
    if not is_logged_in():
        return redirect(url_for("home"))
    #If story is not in the list of all stories
    if story_id not in [i[0] for i in db.get_all_stories()]:
        return render_template("story_unfound.html")
    additions = db.get_story_body(story_id) #List of all user additions to specific story
    contribution_list = [(db.get_username(contr_tuple[0]),contr_tuple[1]) for contr_tuple in additions]
    users = [user[0] for user in additions] #List of all users who made the additions
    if session["id"] in users:
        return render_template("story_contributed.html", story_id = story_id, story_body = contribution_list, user=db.get_username(session["id"]))
    return render_template("story_uncontributed.html", story_id = story_id, story_body = contribution_list, user=db.get_username(session["id"]))

@app.route("/story/<int:story_id>/add", methods = ["POST"])
def add_contribution(story_id):
    if not is_logged_in():
        return redirect(url_for("home"))

    db.add_contribution(session["id"], story_id, request.form.get("addition")) #Adds into specific story table: (usr_id, story_id, body of text)
    flash("Successfully added to the story!")
    return redirect(url_for("view_story", story_id = story_id))

@app.route("/create")
def create_story():
    if not is_logged_in():
        return redirect(url_for("home"))

    return render_template("create_story.html", user=db.get_username(session["id"]))

@app.route("/creating", methods = ["POST","GET"])
def creating_story():
    if not is_logged_in():
        return redirect(url_for("home"))

    db.add_story(request.form.get("title"))
    new_story_id = db.get_all_stories()[-1][0]
    db.add_contribution(session["id"],new_story_id,request.form.get("body"))
    return redirect(url_for("view_story", story_id = new_story_id))

@app.route("/search", methods = ["GET"])
def search_results():
    if not is_logged_in():
        return redirect(url_for("home"))
    query_input = request.args.get("query")
    query_results = db.search_stories(query_input)
    list_story = []
    for id in query_results:
        list_story.append((db.get_title(id), id))
    if len(query_results) == 0: flash("No Stories Found")
    return render_template("search.html", titles = list_story , user=db.get_username(session["id"]))


if __name__ == "__main__":
    app.debug = True
    app.run()
