#util commands for messing with the database
import sqlite3
DB_FILE ="data/bigData.db"
#----------------when you want to add data to the database------------------------------
#adds to the users table
def addUser(username,password_hash):
    db = sqlite3.connect("data/bigData.db")
    c = db.cursor()
    command = "INSERT INTO users (username,password_hash)VALUES(\"{0}\",\"{1}\");".format(username,password_hash)
    c.execute(command)
    db.commit()
    db.close()

#add a story to the stories table
def addStory(title):
    db = sqlite3.connect("data/bigData.db")
    c = db.cursor()
    command = "INSERT INTO stories (title)VALUES(\"{0}\");".format(title)
    c.execute(command)
    db.commit()
    db.close()
#add a contribution to the table
def addContribution(user_id,story_id,body):
    db = sqlite3.connect("data/bigData.db")
    c = db.cursor()
    command = "INSERT INTO contributions (user_id,story_id,body)VALUES({0},{1},\"{2}\");".format(user_id,story_id,body)
    c.execute(command)
    db.commit()
    db.close()
#--------------------useful for logins---------------------------
#returns username password combo in a dict in the format username:password
def getAllUserData():
    db = sqlite3.connect("data/bigData.db")
    c = db.cursor()
    command  = "SELECT username,password_hash FROM users;"
    c.execute(command)
    userInfo = c.fetchall()
    db.close()
    dict = {}
    for item in userInfo:
        dict[item[0]] = item[1]
    return dict
#returns user id based on username every username is unique so this shouldn't be an issue
def getUserId(username):
    db = sqlite3.connect("data/bigData.db")
    c = db.cursor()
    command = "SELECT id FROM users WHERE username = {0};".format(username)
    c.execute(command)
    user_id = c.fetchall()
    db.close()
    return user_id[0][0]
        
#---------------------useful for determining who contributed to what------------------
#returns list of tuples of story_ids a user has contributed to
def getUserContribution(user_id):
    db = sqlite3.connect("data/bigData.db")
    c = db.cursor()
    command = "SELECT story_id FROM contributions WHERE user_id = {0};".format(user_id)
    c.execute(command)
    stories = c.fetchall()
    db.close()
    return stories

#--------------useful for displaying stories(and their contributors)----------------------------
#retrieves every single story id within the db in a tuple list
def getAllStories():
    db = sqlite3.connect("data/bigData.db")
    c = db.cursor()
    command = "SELECT id FROM stories;"
    c.execute(command)
    ids = c.fetchall()
    db.close()
    return ids
    
#get the stories title based on story id
def getTitle(id):
    db = sqlite3.connect("data/bigData.db")
    c = db.cursor()
    command = "SELECT title FROM stories WHERE id = {0};".format(id)
    c.execute(command)
    title = c.fetchall()
    db.close()
    return title[0][0]

#returns a list of tuples of all the contributions of a particular story in the format (user_id,body)
def getStoryBody(story_id):
    db = sqlite3.connect("data/bigData.db")
    c = db.cursor()
    command = "SELECT user_id,body FROM contributions WHERE story_id = {0};".format(story_id)
    c.execute(command)
    storyBody = c.fetchall()
    db.close()
    return storyBody

#retrieve username based on id
def getUsername(id):
    db = sqlite3.connect("data/bigData.db")
    c = db.cursor()
    command = "SELECT username FROM users WHERE id = {0};".format(id)
    c.execute(command)
    name = c.fetchall()
    db.close()
    return name[0][0]


    
    
    
    
    



    
