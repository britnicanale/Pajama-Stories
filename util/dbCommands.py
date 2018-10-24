#util commands for messing with the database
import sqlite3
DB_FILE ="data/bigData.db"
#----------------when you want to add data to the database------------------------------
#adds to the users table
def add_user(username,password_hash):
    '''adds users to use table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "INSERT INTO users (username,password_hash)VALUES(?,?);"
    c.execute(command,(username,password_hash))
    db.commit()
    db.close()

#add a story to the stories table
def add_story(title):
    '''adds a story to stories table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "INSERT INTO stories (title)VALUES(?);"
    c.execute(command,(title,))
    db.commit()
    db.close()
#add a contribution to the table
def add_contribution(user_id,story_id,body):
    '''adds a contribution to the contributions table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "INSERT INTO contributions (user_id,story_id,body)VALUES(?,?,?);"
    c.execute(command,(user_id,story_id,body))
    db.commit()
    db.close()
#--------------------useful for logins---------------------------
#returns username password combo in a dict in the format username:password
def get_all_user_data():
    '''gets all user data into a dict'''
    db = sqlite3.connect(DB_FILE)
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
def get_user_id(username):
    '''gets user id based on username'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id FROM users WHERE username = ?;"
    c.execute(command,(username,))
    user_id = c.fetchall()
    db.close()
    return user_id[0][0]

#---------------------useful for determining who contributed to what------------------
#returns list of tuples of story_ids a user has contributed to
def get_user_contribution(user_id):
    '''gets all of a certain users contributions'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT story_id FROM contributions WHERE user_id = ?;"
    c.execute(command,(user_id,))
    stories = c.fetchall()
    db.close()
    return stories

#--------------useful for displaying stories(and their contributors)----------------------------
#retrieves every single story id within the db in a tuple list
def get_all_stories():
    '''retrieves every single story id within the story table'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT id FROM stories;"
    c.execute(command)
    ids = c.fetchall()
    db.close()
    return ids

#get the stories title based on story id
def get_title(id):
    '''retrieves title based on id given'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT title FROM stories WHERE id = ?;"
    c.execute(command,(id,))
    title = c.fetchall()
    db.close()
    return title[0][0]

#returns a list of tuples of all the contributions of a particular story in the format (user_id,body)
def get_story_body(story_id):
    '''retrives all contributions for a particular story'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT user_id,body FROM contributions WHERE story_id = ?;"
    c.execute(command,(story_id,))
    storyBody = c.fetchall()
    db.close()
    return storyBody

#retrieve username based on id
def get_username(id):
    '''get username based on id'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "SELECT username FROM users WHERE id = ?;"
    c.execute(command,(id,))
    name = c.fetchall()
    db.close()
    return name[0][0]

def search_stories(user_query):
    '''searches for stories based on a query'''
    searching_for = user_query.lower().split()
    story_ids = get_all_stories()
    story_ids_list = [ids[0] for ids in story_ids]
    matched_id = []
    for id in story_ids_list:
        for word in searching_for:
            if word in get_title(id).lower():
                matched_id.append(id)
    matched_id = [x for x in matched_id if matched_id.count(x) == len(searching_for)]
    matched_id = list(set(matched_id))
    return matched_id
