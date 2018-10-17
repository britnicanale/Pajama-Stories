#Jason Lin
#SoftDev1 pd07
#KNN -- TITLE
#201y-mm-dd

from flask import Flask, render_template, request
app = Flask(__name__) # instantiates an instance of Flask

@app.route("/") #Linking a function to a route
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.debug = True
    app.run()
