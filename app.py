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
user_data = db.get_all_user_data()

def is_logged_in():
    return "id" in session

@app.route("/") #Linking a function to a route
def login():
    if(is_logged_in()):
        #index to 0th because that is the id
        contributed_data = db.get_user_contribution(session["id"]);
        list_contr_story_id = []
        for tuple in contributed_data:
            list_contr_story_id.append(tuple[0])
        allStories = db.get_all_stories()
        title_list = []
        non_title_list = []
        for story_id in list_contr_story_id:
            title_list.append(db.get_title(story_id))
        for story_id in allStories:
            if story_id[0] not in list_contr_story_id:
                non_title_list.append(db.get_title(story_id[0]))
        return render_template("homepage.html", titles = title_list, non_titles = non_title_list)
    else:
        return render_template("login.html")

@app.route("/auth" , methods = ["POST"])
def authenticate():
    username_input = request.form.get("username")
    password_input = request.form.get("password")
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
    if story_id not in [i[0] for i in db.get_all_stories()]:
        return render_template("story_unfound.html")
    additions = db.get_story_body(story_id)
    users = [user[0] for user in additions]
    if session["id"] in users:
        return render_template("story_contributed.html", story_id = story_id, story_body = additions)
    return render_template("story_uncontributed.html", story_id = story_id, story_body = additions)

@app.route("/story/<int:story_id>/add", methods = ["POST"])
def add_contribution(story_id):
    db.add_contribution(session["id"], story_id, request.form.get("addition"))
    flash("Successfully added to the story!")
    return redirect(url_for("view_story", story_id = story_id))



if __name__ == "__main__":
    app.debug = True
    app.run()
