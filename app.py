#PJ Cubed -- Jiayang Chen, Jabir Chowdhury, Peter Cwalina, Jason Lin
#SoftDev1 pd07
#P00 -- Da Art of Storytellin'
#2018-10-17

import os
import sqlite3

from flask import Flask, render_template, request, session, url_for, redirect, flash
from passlib.hash import md5_crypt

from util import dbCommands as db

app = Flask(__name__) # instantiates an instance of Flask

app.secret_key = os.urandom(32)
user_data = db.get_all_user_data()

def is_logged_in():
    '''This checks if the user is logged in.'''
    return "id" in session

@app.route("/") #Root
def home():
    '''If the user is not logged in, it redirects to the login page
    If the user is logged in, it will display a list of the stories that
    the user has contributed to and a list of the stories that the user can
    add to. It also allows the user to create a new story. '''
    if(is_logged_in()):
        contributed_data = db.get_user_contribution(session["id"]);
        list_contr_story_id = [x[0] for x in contributed_data] # x[0] is the story id
        allStories = db.get_all_stories() # List of all the stories (id)
        contr_title_list = [(db.get_title(str(story_id)).replace("&#34;",'"'),story_id) for story_id in list_contr_story_id] # List of all contributed-to story titles
        uncontr_title_list = [(db.get_title(str(story_id[0])).replace("&#34;",'"'),story_id[0]) for story_id in allStories if story_id[0] not in list_contr_story_id] # List of all uncontributed-to story titles
        return render_template("homepage.html", titles = contr_title_list, non_titles = uncontr_title_list, user=db.get_username(session["id"]))
    else:
        return redirect(url_for("login"))

@app.route("/login")
def login():
    '''Displays the login page and links to a page to register for a new account.'''
    return render_template("login.html")

@app.route("/auth" , methods = ["POST"])
def authenticate():
    '''Authenticates the username and password that the user has entered in the
    login page. If either one of them is wrong, then it tells them to try again.
    If they are correct, then it creates a session and redirects them to the homepage.'''
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
    '''Deletes the current session and redirects back to login page.'''
    session.pop("id")
    return redirect(url_for("home"))

@app.route("/register")
def register():
    "Displays the page for registering for a new account."
    return render_template("register.html")

@app.route("/registerAuth", methods = ["POST"])
def reg_auth():
    '''Checks if the username that the user registers with is at least
    four characters long and that the passwords that they entered twice
    are the same. If they aren't correct, then tell them to try again.
    If they are correct, create the account and redirect to the login.'''
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
    '''Shows the story to the user. If the user has not contributed, they receive a restricted view of the story.'''
    if not is_logged_in():
        return redirect(url_for("home"))
    #If story is not in the list of all stories
    if story_id not in [i[0] for i in db.get_all_stories()]:
        return render_template("story_unfound.html")
    story_title = db.get_title(story_id).replace("&#34;",'"')
    additions = db.get_story_body(story_id) #List of all user additions to specific story
    contribution_list = [(db.get_username(contr_tuple[0]),contr_tuple[1].replace("&#34;",'"')) for contr_tuple in additions]
    users = [user[0] for user in additions] #List of all users who made the additions
    if session["id"] in users:
        return render_template("story_contributed.html", story_id = story_id, story_body = contribution_list, title=story_title, user=db.get_username(session["id"]))
    return render_template("story_uncontributed.html", story_id = story_id, story_body = contribution_list, title=story_title, user=db.get_username(session["id"]))

@app.route("/story/<int:story_id>/add", methods = ["POST"])
def add_contribution(story_id):
    '''Intermediate function to add the story contribution to the big database. Once added, redirect the user to original story'''
    if not is_logged_in():
        return redirect(url_for("home"))
    addition = request.form.get("addition")

    #Checks for length of input
    if len(addition.split()) < 1 or len(addition.split()) > 600:
        flash("Minimum of 1 and Maximum of 600 characters for the body.")
        return redirect(url_for("view_story", story_id = story_id))

    addition = addition.replace('"',"&#34;")
    db.add_contribution(session["id"], story_id, addition) #Adds into specific story table: (usr_id, story_id, body of text)
    flash("Successfully added to the story!")
    return redirect(url_for("view_story", story_id = story_id))

@app.route("/create")
def create_story():
    '''Displays the form for creating a new story by letting the user make a title
    and the first contribution to that story.'''
    if not is_logged_in():
        return redirect(url_for("home"))

    return render_template("create_story.html", user=db.get_username(session["id"]))

@app.route("/creating", methods = ["POST","GET"])
def creating_story():
    '''Takes in the input from the create_story.html form and checks if the inputs
    are the correct length. If they aren't then it will flash a message and redirect
    the user back to the creating article page. If it is all correct, then it will
    create the story and redirect the user to the page for viewing the story.'''
    if not is_logged_in():
        return redirect(url_for("home"))

    #Get the body and title from the form
    body = request.form.get("body")
    title = request.form.get("title")

    #Checks that their title and body are of the proper length
    if len(body.split()) < 1 or len(body.split()) > 600:
        flash("Minimum of 1 and Maximum of 600 characters for the body.")
        return redirect(url_for("create_story"))
    if len(title.split()) < 1 or len(title.split()) > 40:
        flash("Minimum of 1 and Maximum of 40 characters for the title.")
        return redirect(url_for("create_story"))

    #If it passes the check, then add the story and redirect to view that story
    body = body.replace('"',"&#34;")
    title = title.replace('"',"&#34;")
    db.add_story(title)
    new_story_id = db.get_all_stories()[-1][0]
    db.add_contribution(session["id"],new_story_id, body)
    return redirect(url_for("view_story", story_id = new_story_id))

@app.route("/search", methods = ["GET"])
def search_results():
    '''This takes in the search query from the search bar and attempts to find
    any stories that have a title that include everything that the user searched
    for. If there are no matching stories, it will flash a message that no stories
    were found. Else, it will list out all of the matching stories with links.'''
    if not is_logged_in():
        return redirect(url_for("home"))

    #Takes in what the user inputted as the search query
    query_input = request.args.get("query")
    query_results = db.search_stories(query_input) #Gets list of stories that contain the query
    list_story = []
    for id in query_results:
        list_story.append((db.get_title(id), id))

    #Tells the user if there are no stories that match their query
    if len(query_results) == 0: flash("No Stories Found")
    return render_template("search.html", titles = list_story , user=db.get_username(session["id"]))


if __name__ == "__main__":
    app.debug = True
    app.run()
