# Pajama Stories
A collaborative story telling website that would make for great stories that you read while in your pajamas.
Users can create a new story or add on to existing stories based off of what the previous person wrote. After contributing, the user can see the entire story and all of the entries.
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

## Library Used
For our project, we used the [passlib](https://passlib.readthedocs.io/en/stable/) library.

The passlib library contains many hashing algorithm for encrypting passwords. Additionally,
there are functions that verify whether a given input would hash to a certain output.
Overall the passlib library provides algorithms that increase security for the user.

Our team deems the passlib library necessary because it gives our website
a secure password system. Not only will it make it more difficult for
intruders to gain access to other user accounts, but using this library will
help our team gain more knowledge about security and hashing.

In our project, we imported the md5_crypt hashing algorithm and verifying function.
When the user creates an account, we used `md5_crypt.encrypt` to hash the password
and put the hash for that user in the database. When the user logs in,
we used the `md5_crypt.verify` to check whether the password that the user inputs
has the same hash as what is in the database.

## Virtual Environment
Before installing a virtual environment in your computer, make sure that you have Python 3 and SQLite3 installed. If you do not have it installed, [go here to learn how to install Python 3](https://realpython.com/installing-python/) or [here to install SQLite3](https://www.sqlite.org/download.html).

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
`Pajama-Stories/`, install all of the required dependencies
```
$ pip install -r requirements.txt
```
## Run the program
Once you are inside of our repository, you can run our website
```
$ python app.py
```
Go to `localhost:5000` in your favorite web browser to view the website

### Stopping the website
When you are done viewing the website, close the server using `Ctrl-C` and deactivate your virtual environment
```
$ deactivate
```
