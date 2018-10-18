#PJ Cubed -- Jiayang Chen, Jabir Chowdhury, Peter Cwalina, Jason Lin
#SoftDev1 pd07
#P00 -- Da Art of Storytellin'
#2018-10-17

from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__) # instantiates an instance of Flask

@app.route("/") #Linking a function to a route
def home():
    return render_template("story_contributed.html", additions = [("the duck goes woof","dennis"),("the dog goes meow", "jason"), ("the cat goes quack","kenny")])

if __name__ == "__main__":
    app.debug = True
    app.run()
