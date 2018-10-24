# Pajama Stories

## Contributors
Team Name: PJCubed
### Roster
* [Jiayang Chen](https://github.com/jiayang)
* [Jabir Chowdhury](https://github.com/JabirC)
* [Peter Cwalina](https://github.com/PeterCwalina)
* [Jason Lin](https://github.com/JasonLin43212)

## Requirements
* Python 3 <br>
* SQLite3

## Virtual Environment
To install a virtual environment in your computer, first make sure that you have Python 3 and SQLite3 installed. If you do not have it installed, [go here to learn how to install Python 3](https://realpython.com/installing-python/) or [here to install SQLite3](https://www.sqlite.org/download.html).

Now install your virtual environment
```
$ python3 -m venv <virutal_environment_name>
```
Go to the directory which contains the folder containing your virtual environment and activate it

**For Linux:**
```
$ source <virtual_environment_name>/bin/activate
```
**For Windows:**
```
> <virtual_environment_name>/script/activate
```
## Cloning Our Repository
To get our website, clone it.
```
$ git clone https://github.com/JasonLin43212/Pajama-Stories.git
```
And then go into the repository
```
$ cd Pajama-Stories/
```
## Installing Flask
After activating your virtual environment and changing your directory to inside of
Pajama-Stories/, install all of the required dependencies
```
$ pip install -r requirements.txt
```
## Run the program
Once you are inside of our repository, you can run our website
```
$ python app.py
```
Go to localhost:5000 in your favorite web browser to view the website

### Stopping the website
When you are done viewing the website, close the server using `Ctrl-C` and deactivate your virtual environment
```
$ deactivate
```
